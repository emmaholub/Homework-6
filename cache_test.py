from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from agent import run

ROOT = Path(__file__).resolve().parent
DOCS = sorted((ROOT / "data" / "practice_docs").glob("p*.html")) + sorted((ROOT / "data" / "practice_docs").glob("p*.pdf")) + sorted((ROOT / "data" / "practice_docs").glob("p*.eml"))


async def main() -> None:
    output_path = ROOT / "cache_test.json"
    records = json.loads(output_path.read_text()) if output_path.exists() else []
    completed = {(r.get("document"), r.get("caching")) for r in records}
    for caching in (True, False):
        for path in DOCS:
            key = (str(path.relative_to(ROOT)), caching)
            if key in completed:
                continue
            try:
                answer = await run(path, caching=caching)
                after = json.loads((ROOT / "usage_log.json").read_text())
                usage = after[-1]
                record = {"timestamp": datetime.now(timezone.utc).isoformat(), "document": str(path.relative_to(ROOT)), "caching": caching, "status": "ok", "usage": usage, "answer": answer.model_dump()}
            except Exception as exc:
                record = {"timestamp": datetime.now(timezone.utc).isoformat(), "document": str(path.relative_to(ROOT)), "caching": caching, "status": "error", "error": f"{type(exc).__name__}: {exc}"}
            records.append(record)
            output_path.write_text(json.dumps(records, indent=2) + "\n")
            print(record["document"], "cache=" + str(caching), record["status"], flush=True)
    print(json.dumps({"runs": len(records), "documents": len(DOCS), "cache_off_zero_reads": all(not x["caching"] and x["usage"]["cache_read_tokens"] == 0 or x["caching"] for x in records)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
