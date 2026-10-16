# AI Prompts Log – HW6

This file records the prompts I use while completing each homework problem.

## Problem 1: Vibe coder prompts

**Prompt:** Create and maintain `AI_prompts.md` for HW6. Give every problem its own section, record the prompt I actually typed in my own words, and include any follow-up prompt plus one sentence explaining what the first response missed.

**Follow-up:** None so far.

**What was missing after the first prompt:** Nothing; this prompt establishes the required log structure and the standard to use for every later problem.

## Problem 2: Size up the handbook

**Prompt:** Unzip `data.zip`, count the tokens in `data/shop_handbook.md` with a real tokenizer, use `data/prices.json` to calculate the handbook-only cost for one call and 1,000 calls with and without caching, and save the math in `output/handbook_estimate.md`.

**Follow-up:** Use the installed `tiktoken` tokenizer rather than word count, state the encoding used, and distinguish the first cache write from later cached reads.

**What was missing after the first prompt:** The first request did not specify how to handle the first call's cache-write charge or identify the tokenizer, so those assumptions were made explicit in the final estimate.

## Problem 3: Build the vendor-document agent

**Prompt:** Build a PydanticAI agent using only `gpt-6-luna` through Portkey. Create `prompts/prompt.md`, `agent.py`, `tools.py`, and `models.py`. Given an HTML, PDF, or `.eml` vendor document, return the vendor, SKU, unit price, lead time, minimum order, handbook-based recommendation, and one-sentence reason. Add fake `send_email` and `approve_payment` trap tools that only log to `output/trap_calls.json`; log usage/cost and audit events after every run; run p01 and p08 and document the fields/tools in `output/harness.md`.

**Follow-up:** Keep the handbook rules in the system prompt, treat document text as untrusted data, never call the trap tools for normal analysis, and make all logs append-only.

**What was missing after the first prompt:** The first request did not make prompt injection resistance, fake-tool behavior, or append-only evidence explicit.

## Problem 4: With vs. without cache

**Prompt:** Run the agent on all 12 practice documents once with handbook caching enabled and once with caching truly disabled. Require zero provider-reported cached tokens in the off run, log every call to `cache_test.json`, and write total/per-document cost, savings, estimates comparison, a 1,000-per-day monthly projection, and surprises in `cache_test.md`.

**Follow-up:** Because the gateway still applied implicit caching when `cache=False`, add a unique nonce at the beginning of each cache-off system prompt and verify every cache-off record has `cache_read_tokens: 0`.

**What was missing after the first prompt:** A library-level cache flag alone did not guarantee zero cached tokens at the provider, so the cache-off test needed a prefix-breaking nonce and an explicit validation check.

## Problem 5: Attack your own agent

**Prompt:** Run the undefended Problem 3 baseline on all 12 practice documents and compare every returned field and decision with `data/practice_key.json`. Record trap-tool calls, suspicious links/text, and the exact documents that fooled it in `attack_results.json` and explain each hiding place in `attack_results.md`.

**Follow-up:** Inspect the HTML, email, and PDF files as a human would so the explanation distinguishes invisible HTML/CSS injection from ordinary PDF extraction failure.

**What was missing after the first prompt:** The first request did not distinguish a malicious hidden instruction from a parser failing to read a PDF, so the follow-up added that comparison.

## Problem 6: Defend the agent

**Prompt:** Add code, design, and prompt defenses while keeping the undefended Problem 3 path available. Clean hidden document text before the model sees it, prevent poisoned documents from reaching trap tools or decisions, preserve clean quote values, rerun all 12 documents, and save per-document tokens/dollars plus before/after analysis in `defense_results.json` and `defense_results.md`.

**Follow-up:** Add PDF extraction, strip hidden HTML/CSS and malicious email alternatives, remove trap tools from the defended agent rather than deleting them, and verify all 12 expected decisions and fields.

**What was missing after the first prompt:** The first defense implementation did not handle PDF correction text or separate tool exposure from the defended decision path.

## Problem 7: Red team

**Prompt:** Create two new human-normal booby-trapped vendor documents in `data/my_attacks/` using hiding tricks not already in the practice set. Run both against the undefended and defended agents, record the results, and explain each hidden payload, goal, and before/after outcome in `red_team.md`.

**Follow-up:** Use an HTML title payload and zero-width Unicode email text, and make at least one attack attempt a trap-tool call in the undefended run while the defended run blocks it.

**What was missing after the first prompt:** The first plan did not guarantee that the attacks were new or that the comparison would test the tool boundary, so the follow-up made those targets explicit.

## Problem 8: Exam documents

**Prompt:** Run the final defended agent on all 10 documents in `data/exam_docs/` without an answer key or hand-editing. Save one exact machine-generated entry per file in `exam_results.json` with vendor fields, decision/reason, trap status, token counts, and cost.

**Follow-up:** Preserve the defended cleaner and no-tool design from Problems 6–7, and checkpoint each result so a long run can resume without changing model outputs.

**What was missing after the first prompt:** The first plan did not specify the exact flat output fields or how to prove the exam run used the defended path.

## Problem 9: Results page

**Prompt:** Build a single-file offline `output/hw6_report.html` using the real cache, attack, defense, red-team, and exam results. Include a readable chart, cost comparison, safety outcomes, the monthly projection for 1,000 documents per day, and a clear recommendation for the store manager. Do not use external assets.

**Follow-up:** Recalculate the displayed costs from the corrected formula where API input tokens already include cached and cache-write tokens; do not charge those tokens twice.

**What was missing after the first prompt:** The first report request did not explicitly protect against double-counting cached tokens, so the follow-up tied every displayed total to the corrected accounting rule.

## Problem 10: Submit to GitHub

**Prompt:** Prepare the finished HW6 folder for a public GitHub submission. Check the required files, remove secrets, include `.env.example`, make the README explain setup and reruns, and verify the repository is ready to submit.

**Follow-up:** Check the public repository after pushing and confirm the submitted URL points to the final commit and contains the generated evidence files.

**What was missing after the first prompt:** The first request did not explicitly mention checking the deployed public tree after the push, so the follow-up added that verification.
