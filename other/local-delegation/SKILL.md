---
name: local-delegation
description: Use when the user wants an AI coding agent to offload suitable low-risk, bounded codebase browsing, inventory, extraction, log triage, or simple single-file reasoning tasks to a local LM Studio model while keeping high-level reasoning and final decisions in the main model.
---

# Local Delegation

Use a local LM Studio model as a scout for bounded grunt work. The main model owns planning, judgment, implementation choices, verification, and the final answer.

This skill applies only while it is active for the current task/session unless the surrounding agent framework keeps it in context. Reusable activation phrase: "local delegation mode on".

Bounded means bounded by task scope, not tiny local token use. Spend local tokens generously when they reduce high-cost model context and attention.

## Delegate / Avoid

Good local tasks:

- Repo orientation, directory summaries, and entry-point discovery.
- Grep-heavy inventories, lists, counts, tables, and `file:line` extraction.
- Log or command-output triage.
- References to symbols, env vars, routes, APIs, TODOs, config keys, and literals.
- First-pass review of one named low-risk file or small directory.
- Narrow "read these files and summarize what matters" tasks.
- Candidate evidence, leads, or summaries for the main model to inspect.

Do not delegate:

- Final architecture decisions or ambiguous product tradeoffs.
- Security, privacy, auth, crypto, data-loss, migrations, billing, compliance, or other high-risk conclusions.
- Multi-file causal debugging where correctness depends on subtle interactions.
- Tasks requiring hidden/current conversation context the local model does not have.
- User-facing final answers without main-model review.
- Code edits unless explicitly requested and safely supported.
- Anything where a wrong answer would be expensive and hard to detect.

For high-risk areas, local delegation may still be useful for first-pass inventories, but verify the relevant evidence directly before drawing conclusions.

## Tools

The skill is self-contained. Scripts are bundled under `scripts/`, adapted from `alisorcorp/ask-local`, with the MIT notice in `LICENSE.ask-local.txt`. Resolve paths relative to this skill directory.

- `scripts/query_lm.py`: prompt-only helper and model/server preflight.
- `scripts/agent_lm.py`: tool-calling local agent with `list_dir`, `grep`, and `read_file`.

Server preflight:

```bash
python3 <skill-dir>/scripts/query_lm.py --list-models
```

If this cannot reach LM Studio, tell the user the GUI can be open while the Local Server is stopped. Ask them to start it in LM Studio's Developer tab, usually on port `1234`. If they use another port, pass `--url http://localhost:<port>`. Do not retry delegation until the server is running.

## Model Choice

Honor explicit user model preferences first. If the user names a model and LM Studio lists it, pass it exactly with `--model`. If it is not loaded, do not silently substitute; report that and list loaded model IDs.

Without a user preference, choose a loaded chat/instruct model from `--list-models`, pass it explicitly with `--model`, and mention the choice briefly. Avoid embedding-only models for browsing/log triage, especially IDs containing `embed`, `embedding`, or `nomic-embed`, unless the task explicitly asks for embeddings.

Do not rely on the scripts' default model unless that exact model is loaded.

## Run

For codebase browsing:

```bash
python3 <skill-dir>/scripts/agent_lm.py --dir <DIR> --model <MODEL> [flags] "task description"
```

For piped logs/output:

```bash
some-command | python3 <skill-dir>/scripts/query_lm.py --model <MODEL> "classify these errors into buckets"
```

Useful flags:

- `--read-budget N`: max `read_file` calls; `list_dir` and `grep` are free. This is a circuit breaker, not a cost limit.
- `--max-tokens N`: raise freely for dense local summaries.
- `--max-turns N`: prevents runaway local agent loops.
- `--think`: use for harder local reasoning.
- `--quiet`: suppress progress logs when clean output matters.
- `--url URL`: LM Studio server URL.

Budget starting points:

- Tiny lookup: `--read-budget 5-10 --max-tokens 2000-4000`.
- Single file/small directory: `--read-budget 10-20 --max-tokens 4000-8000`.
- Repo scout review: `--read-budget 25-50 --max-tokens 8000-12000`.
- Large inventory: `--read-budget 50+ --max-tokens 10000-16000`.

Prefer `grep` and `list_dir` first for precision, not because local tokens are expensive. If output reports read-budget exhaustion or truncation, rerun with a larger budget/token cap or a narrower task.

## Prompt Shape

Do not paste large file contents into the local prompt. Name paths, files, symbols, or patterns and let the local model use its tools.

Use bounded, context-light prompts:

```text
In <repo/path>, <bounded task>.
Return compact structured output.
Include file:line citations where relevant.
Do not propose edits unless asked.
Mark uncertainty, skipped files, truncation, and incomplete coverage.
```

Examples:

```text
Find all env vars read in this repo. Return file:line, variable name, default value if present.
```

```text
Inventory API routes under app/api: method, path, auth check, one-line purpose.
```

```text
Read src/foo.ts and list likely edge cases. Do not propose a patch.
```

```text
Summarize this build log into blocking errors, likely root causes, and commands to retry.
```

## Verify And Report

Local output does not need to be final-answer quality to be useful. Rough summaries, imperfect citations, and plausible leads are acceptable for exploratory grunt work.

Treat local output as notes, not truth. Spot-check `file:line` claims and directly verify any claim that matters, especially before code changes or high-risk conclusions. Never let local output replace tests, type checks, security review, or main-model reasoning.

Report lightweightly: mention local delegation when it shaped the work, include the selected model and any confidence limits or warnings, and summarize only what matters.
