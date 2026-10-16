from __future__ import annotations

import json
import os
import re
import asyncio
import subprocess
from email import policy
from email.parser import BytesParser
from datetime import datetime, timezone
from pathlib import Path

from pydantic_ai import Agent

from models import VendorQuote
from tools import approve_payment, send_email, approve_payment_gated, send_email_gated, read_vendor_document, read_vendor_document_clean, _append, AUDIT_LOG

ROOT = Path(__file__).resolve().parent
PROMPT = (ROOT / "prompts" / "prompt.md").read_text(encoding="utf-8")
HANDBOOK = (ROOT / "data" / "shop_handbook.md").read_text(encoding="utf-8")
MODEL = "openai:gpt-6-luna"


def make_agent(caching: bool = True) -> Agent:
    key = os.getenv("PORTKEY_API_KEY")
    if not key:
        raise RuntimeError("PORTKEY_API_KEY is required")
    os.environ.setdefault("OPENAI_API_KEY", key)
    os.environ.setdefault("OPENAI_BASE_URL", "https://api.portkey.ai/v1")
    cache_breaker = "" if caching else f"Cache-disabled run nonce: {os.urandom(16).hex()}\n\n"
    return Agent(MODEL, system_prompt=cache_breaker + PROMPT + "\n\n## SHOP HANDBOOK\n" + HANDBOOK, output_type=VendorQuote, tools=[read_vendor_document, send_email, approve_payment])


def make_defended_agent(caching: bool = True) -> Agent:
    """Defended design: reading is cleaned and side-effect capabilities are code-blocked."""
    key = os.getenv("PORTKEY_API_KEY")
    if not key:
        raise RuntimeError("PORTKEY_API_KEY is required")
    os.environ.setdefault("OPENAI_API_KEY", key)
    os.environ.setdefault("OPENAI_BASE_URL", "https://api.portkey.ai/v1")
    cache_breaker = "" if caching else f"Cache-disabled run nonce: {os.urandom(16).hex()}\n\n"
    return Agent(MODEL, system_prompt=cache_breaker + PROMPT + "\n\n## SHOP HANDBOOK\n" + HANDBOOK, output_type=VendorQuote, tools=[read_vendor_document_clean, send_email_gated, approve_payment_gated])


def clean_document(path: Path) -> str:
    """Keep human-visible quote content and discard hidden HTML/CSS instructions."""
    if path.suffix.lower() in {".html", ".htm"}:
        from html.parser import HTMLParser

        class VisibleText(HTMLParser):
            def __init__(self):
                super().__init__(); self.parts=[]; self.hidden=0
            def handle_starttag(self, tag, attrs):
                attr=dict(attrs); style=attr.get("style", "").replace(" ", "").lower()
                hidden_css = (re.search(r"display:none|visibility:hidden|opacity:0|font-size:0", style) or
                              re.search(r"(?:left|top):-(?:[1-9]\d{2,}|9\d{3,})", style) or
                              re.search(r"position:absolute[^;]*(?:left|top):-", style) or
                              re.search(r"clip(?:-path)?:", style))
                if tag in {"head", "title", "meta", "script", "style"} or "hidden" in attr or hidden_css: self.hidden += 1
            def handle_endtag(self, tag):
                if tag in {"head", "title", "meta", "script", "style"} or self.hidden and tag in {"div", "p", "span", "table", "section", "article"}: self.hidden=max(0,self.hidden-1)
            def handle_data(self, data):
                if not self.hidden and data.strip(): self.parts.append(data.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\ufeff", "").strip())
        parser=VisibleText(); parser.feed(path.read_text(errors="replace")); return " ".join(parser.parts)
    if path.suffix.lower() == ".eml":
        message=BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        if message.is_multipart():
            plain=message.get_body(preferencelist=("plain",))
            return plain.get_content() if plain else ""
        return message.get_content().replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\ufeff", "")
    return read_document(path)


def read_document(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix.lower() in {".html", ".htm"}:
        text = raw.decode("utf-8", errors="replace")
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", text).strip()
    if path.suffix.lower() == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            # Keep the first occurrence of each quoted field. This is a
            # document-structure rule, not a list of attacker phrases: later
            # duplicate price/lead-time lines are treated as untrusted edits.
            seen = set(); kept = []
            for line in text.splitlines():
                low = line.lower()
                field = next((name for name, markers in {
                    "price": ("unit price", "price:"),
                    "lead": ("lead time", "lead-time"),
                    "minimum": ("minimum order", "min order"),
                }.items() if any(marker in low for marker in markers)), None)
                if field and field in seen:
                    continue
                if field: seen.add(field)
                kept.append(line)
            return "\n".join(kept)
        except ImportError:
            # macOS's built-in textutil provides a dependency-free fallback.
            return subprocess.check_output(["textutil", "-convert", "txt", "-stdout", str(path)], text=True)
    return raw.decode("utf-8", errors="replace")


async def run(path: str | Path, caching: bool = True, defended: bool = True) -> VendorQuote:
    document = Path(path)
    agent = make_defended_agent(caching=caching) if defended else make_agent(caching=caching)
    result = await agent.run(
        f"Analyze the vendor document at this path by calling your document-reading tool first: {document}",
        model_settings={
            "cache": caching,
            "openai_prompt_cache_key": ("hw6-stable" if caching else os.urandom(16).hex()),
            "openai_prompt_cache_options": ({"mode": "implicit"} if caching else {"mode": "explicit"}),
            "openai_cache_instructions": caching,
        },
    )
    answer = result.output
    if answer.vendor:
        answer.vendor = answer.vendor.rstrip(".")
    usage = result.usage
    input_tokens = getattr(usage, "input_tokens", 0) or 0
    cache_write_tokens = getattr(usage, "cache_write_tokens", 0) or 0
    cache_read_tokens = getattr(usage, "cache_read_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0
    total_tokens = getattr(usage, "total_tokens", input_tokens + output_tokens) or (input_tokens + output_tokens)
    uncached_input_tokens = max(0, input_tokens - cache_write_tokens - cache_read_tokens)
    cost = (uncached_input_tokens / 1_000_000 * 0.10) + (cache_write_tokens / 1_000_000 * 0.125) + (cache_read_tokens / 1_000_000 * 0.01) + (output_tokens / 1_000_000 * 0.50)
    _append(ROOT / "usage_log.json", {"timestamp": datetime.now(timezone.utc).isoformat(), "document": str(document), "model": "gpt-6-luna", "caching": caching, "input_tokens": input_tokens, "cache_write_tokens": cache_write_tokens, "cache_read_tokens": cache_read_tokens, "output_tokens": output_tokens, "total_tokens": total_tokens, "estimated_cost": cost})
    _append(AUDIT_LOG, {"timestamp": datetime.now(timezone.utc).isoformat(), "action": "final_answer", "document": str(document), "tool_calls": ["read_vendor_document" if not defended else "read_vendor_document_clean"], "result": answer.model_dump()})
    return answer


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    args = parser.parse_args()
    print(asyncio.run(run(args.doc)).model_dump_json(indent=2))
