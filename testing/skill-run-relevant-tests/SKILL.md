---
name: Run Relevant Tests
description: "Identify and run only the test suites affected by the current change set. Triggers on phrases like 'run relevant tests', 'did I break anything', 'test my changes', or after edits to api/ or frontend/ source files. Maps changed files to pytest and Jest targets, executes them, and surfaces failures with file:line citations and fix suggestions."
model: inherit
---

## Purpose

Eliminate the friction of "did I break anything" without waiting for full CI. The skill maps changed files to the minimal set of pytest and Jest targets that exercise them, runs those targets, and parses results. It is the local pre-push smoke test.

## When to Invoke

- Before pushing a branch.
- After completing a focused refactor.
- When a developer asks "did I break anything" or "test my changes".
- Inside a PR review session to verify a fix.

## When NOT to Invoke

- For documentation-only PRs.
- As a substitute for full CI — the skill explicitly runs a subset.
- When the workspace has uncommitted unrelated changes (warn first).

## Inputs

- **base_ref** (optional): git ref to compare against (default: `origin/main`).
- **scope** (optional): `api`, `frontend`, or `all` (default: inferred from changed files).
- **mode** (optional): `fast` (default — run only direct tests) or `deep` (include reverse-dependency tests).

## Procedure

1. Run `git diff --name-only <base_ref>...HEAD` plus unstaged changes. Refuse if the workspace is dirty with unrelated paths and the user did not pass `--force`.
2. Classify each changed file:
   - `api/src/**/*.py` → look for sibling under `api/tests/src/<same-relative-path>` and a `test_<basename>.py` under that mirrored tree.
   - `api/tests/**/*.py` → run that file.
   - `frontend/src/**/*.{ts,tsx}` → look for sibling `*.test.ts(x)` in the same directory; if none, search `frontend/tests/`.
   - `frontend/tests/**/*` → run that file.
   - `api/openapi.generated.yml` → run contract test suite if present.
   - `api/src/db/migrations/versions/*.py` → run `api/tests/src/db/test_migrations.py`.
3. In `deep` mode, also collect reverse importers via ripgrep and add their tests.
4. Build the execution plan:
   - API: `cd api && uv run pytest <files> -x --no-header`
   - Frontend: `cd frontend && npm test -- <files> --runInBand`
5. Print the plan, request confirmation if more than 50 test files, then execute.
6. Parse output for FAILED / PASSED counts. For each failure, capture file, line, and assertion.
7. Cross-reference each failure with the changed file that most likely caused it (heuristic: shortest path distance).
8. Emit the Output Format.

## Outputs

```
Run Relevant Tests — base=origin/main mode=fast
Changed files: 4
Test plan:
  api/tests/src/api/opportunities_v1/test_opportunity_routes.py
  api/tests/src/services/opportunities/test_search_service.py
  frontend/src/components/search/SearchBar.test.tsx

Execution:
  api    : 12 passed, 1 failed in 4.2s
  frontend: 8 passed in 6.1s

Failures (1):
  [FAIL] api/tests/src/api/opportunities_v1/test_opportunity_routes.py::test_search_returns_status
         L42  AssertionError: assert 'draft' in response['legacyStatus']
         Likely cause: api/src/api/opportunities_v1/opportunity_schemas.py (legacyStatus removed)
         Fix:  update test to use `status` field

Suggested next: /skill-openapi-sync (schema drift suspected)
```

## Safety

- Never modifies source or test files.
- Refuses to run if more than 50 test files are selected without confirmation.
- Never runs migrations against a real DB; uses the configured test DB only.
- Never sets environment variables containing secrets.
- FedRAMP: never logs request bodies that may contain PII.

## Examples

**Example 1 — API service tweak**
Change to `api/src/services/opportunities/search_service.py`. Skill runs the matching service test and route test, returns green in 4 seconds.

**Example 2 — Frontend component edit**
Change to `SearchBar.tsx`. Skill runs `SearchBar.test.tsx` plus any integration test importing it (deep mode).

**Example 3 — Mixed change**
Change touches both API schema and frontend type. Skill runs both suites and recommends `skill-openapi-sync`.

## Related

- `.cursor/skills/skill-impact-analysis/` — see what would be affected before running.
- `.cursor/skills/skill-openapi-sync/` — when failures point at schema drift.
- `.cursor/agents/regression-detector.md` — for failures suspected to be flakes.
