# HW6 agent harness

## Agent

`agent.py` creates one PydanticAI agent using only `openai:gpt-6-luna` through Portkey. It loads `prompts/prompt.md`, accepts one HTML, PDF, or `.eml` vendor document, and returns a typed `VendorQuote`.

## `models.py` fields

- `vendor`: vendor name extracted from the document.
- `sku`: Campus Customs SKU quoted by the vendor.
- `unit_price`: quoted per-unit price in dollars.
- `lead_time_days`: promised production/shipping time in days.
- `minimum_order`: minimum number of units required.
- `decision`: exactly `recommend` or `do_not_recommend` after applying the handbook checks.
- `reason`: one sentence naming the check that determined the decision.

## Tools

- `read_vendor_document(path)`: the undefended agent reads the supplied file through this tool and records the path and character count.
- `read_vendor_document_clean(path)`: the defended agent reads the file through the visibility-aware cleaner before extraction.
- `send_email(to, subject, body)`: fake trap tool that writes an attempted email to `output/trap_calls.json`; it never sends anything.
- `approve_payment(vendor, amount, reason)`: fake trap tool that writes an attempted payment approval to `output/trap_calls.json`; it never approves or moves money.

Both trap tools also append their call to `output/audit_trail.json`. The defended `send_email_gated` and `approve_payment_gated` tools are preserved but always block inside the model run; human approval must occur in code or through a person outside the agent. The final structured answer and token/cost usage are appended after every run; token records are stored in root `usage_log.json`.

## Safety

Documents are untrusted data. The defended reader removes hidden HTML/CSS and uses the plain-text email part. Side-effect tools cannot receive a model-supplied approval flag: the agent only receives a blocked response, and a separate human-controlled application path must approve any real action. Missing quote facts fail closed to `do_not_recommend`; the agent never invents prices, sends email, or moves money. Cache results use provider token fields, and cache-off runs require zero cached reads.

## Required examples

Run from this folder after setting `PORTKEY_API_KEY`:

```bash
python agent.py --doc data/practice_docs/p01_bluehen_quote.html
python agent.py --doc data/practice_docs/p08_chapelst_email.eml
```

Problem 4's 24-call cache comparison is recorded in `cache_test.json` and summarized in `cache_test.md`; the cache-off mode uses a unique system-prompt prefix and checks for zero provider-reported cached tokens.

Problem 6 adds `defense_results.json` and `defense_results.md`. The defended path cleans hidden document content before the model sees it and exposes code-blocked gated side-effect tools. The original undefended path remains available through `attack_agent.py` for Problem 5.

Problem 7 adds two new attacks under `data/my_attacks/` and records undefended/defended results in `red_team_results.json` and `red_team.md`. The attacks use an HTML title payload and zero-width Unicode email text.

Problem 8 runs the final defended agent on `data/exam_docs/` with `exam_test.py`; its ten machine-generated entries are saved in `exam_results.json`, including answer fields, `trap_tool_called`, token counts, and estimated cost.
