---
name: go
description: The main entry point for all coding tasks. Refines your raw prompt into an expert-level prompt, then builds using TDD with full verification. Use this for everything.
argument-hint: "<your task in plain English, e.g. 'build transcript store' or 'fix the cors bug'>"
allowed-tools: Read Glob Grep Write Edit Bash(poetry run pytest *) Bash(poetry run uvicorn *) Bash(curl *) Bash(npm *)
---

You received a raw prompt from a non-technical user. You MUST refine it first, then execute it using the full build workflow.

**Raw input:** $ARGUMENTS

---

## Phase 1: Refine the Prompt

Transform the raw input by adding:

1. **Scope** — Check CLAUDE.md build order to identify the F-number, exact file paths, and which services are involved.

2. **References** — Point to existing patterns to follow:
   - Services: follow `services/ingestion/service.py`
   - Schemas: follow `schemas/test_cases.py`
   - Routes: follow `routes/test_cases.py`

3. **LLD mapping** — Which PRD feature, LLD section, data models, API endpoints

4. **Dependencies** — What's already built that this connects to

5. **Verification** — Tests to write, endpoints to curl, commands to run

Show the refined prompt:

> **Refined prompt:** [your enhanced version]

---

## Phase 2: Map to PRD + LLD

Before writing any code:
1. Find the F-number in @docs/PRD.md
2. Find the matching component in @docs/LLD.md Section 2 — confirm exact file path, data model (Section 4), and API endpoint (Section 3)
3. State: **"Building [component] at [path], covering [F-number]."**

---

## Phase 3: Write the Test FIRST (RED)

Create `service-one/src/tests/test_<module>.py` BEFORE the implementation.

Tests must cover:
- Happy path — normal input → expected output
- Edge case — empty input, missing fields, boundary values
- Error path — invalid input, downstream failure

Mock all external dependencies (LLM, DB, HTTP). Run to confirm FAILS:
```
poetry run pytest service-one/src/tests/test_<module>.py -v
```

---

## Phase 4: Implement (GREEN)

Write minimum code to make tests pass. Follow these rules:
- All I/O functions must be `async`
- Pydantic v2 models for request/response — no raw dicts
- LLM calls only through `api/llm/interfaces.py`
- `temperature=0` on evaluation/judge calls
- `flush()` not `commit()` — session dependency handles transactions
- File paths must match LLD Section 2 exactly
- No hardcoded secrets — use `os.getenv()`

Run tests to confirm GREEN:
```
poetry run pytest service-one/src/tests/test_<module>.py -v
```

---

## Phase 5: Production Checklist

Before declaring done:
- [ ] No `requests.get/post` — use `httpx` async
- [ ] No blocking DB calls in `async def`
- [ ] All HTTP calls have `timeout=` set
- [ ] No hardcoded secrets
- [ ] Health endpoints untouched
- [ ] No direct SDK imports in service code

---

## Phase 6: Explain in Plain English

Tell the owner:
1. **What was built** — one sentence, no jargon
2. **Where it lives** — file paths
3. **Which requirement** — F-number
4. **How to verify** — command or endpoint

---

## Phase 7: Show Git Commands (never execute)

```bash
git add <specific files>
git commit -m "feat(F<number>): <short description>"
git push origin stage
```
