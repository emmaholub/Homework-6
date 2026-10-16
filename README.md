# HW6 — Campus Customs Vendor Document Agent

This project evaluates a PydanticAI vendor-document agent using the `gpt-6-luna` model through Portkey. The complete `data/` folder is included, including the practice documents, exam documents, handbook, answer key, prices, and `data/my_attacks/` red-team documents.

## Setup

Use Python 3.12 or newer and install the required packages used by the course environment. Then create a local environment file without committing it:

```bash
cp .env.example .env
# edit .env and set PORTKEY_API_KEY
source .env
```

The real `.env` is excluded by `.gitignore`; only `.env.example` belongs in GitHub.

## How to run one document

From the HW6 folder, run the required CLI form:

```bash
python agent.py --doc data/practice_docs/p01_bluehen_quote.html
python agent.py --doc data/practice_docs/p08_chapelst_email.eml
```

The agent reads the file through its document-reading tool, returns a typed vendor quote, and appends usage and audit information. The defended path is used by default; `attack_agent.py` preserves the undefended comparison required for the attack experiment.

## Reproduce the analyses

```bash
python cache_test.py       # 12 documents with caching on/off
python attack_agent.py     # undefended practice-document comparison
python defense_test.py    # defended practice-document comparison
python red_team_test.py   # two documents in data/my_attacks/
python exam_test.py       # defended run on data/exam_docs/
```

The result JSON files and explanations are in the project root. The self-contained offline report is `output/hw6_report.html`; double-click it to open it without a server or internet connection. `output/harness.md` documents the fields, tools, safety controls, and run commands.

## Evidence and safety

`output/audit_trail.json` is append-only. The email and payment capabilities are retained for the assignment’s trap-tool tests, but the defended gated versions always block inside the model run. Any real email or payment requires approval from code or a person outside the agent. Documents are treated as untrusted data, and missing quote facts fail closed to `do_not_recommend`.

Do not commit API keys, `.env`, virtual environments, or cache files. The full `data/` folder should remain committed so graders can rerun the agent.
