---
name: integration
description: Run integration and e2e tests after unit tests pass. Use after /supergraph:fix when unit tests are green.
mcp: codebase-memory-mcp
---

# /supergraph:integration

Integration + e2e tests. Validates modules work together. Run AFTER unit tests pass.

## Usage

`/supergraph:integration` | `plan auth-login` | `plan auth-login task 3`

## Prerequisites

- Unit tests passing (`$TEST_CMD` green)
- `/supergraph:fix` completed

## Steps

### 0. Announce
"🔗 /supergraph:integration — running integration and e2e tests..."

### 1. Get Commands
Read from plan `## Environment Context` or `.supergraph-env`. Missing → STOP, run `/supergraph:scan` first.

### 2. Verify Unit Tests Pass
```bash
$TEST_CMD
```
If unit tests FAIL → STOP: "Unit tests must pass before integration. Run `/supergraph:fix` first."

### 3. Detect Integration Setup
Check for integration configuration:

| Config | Command |
|---|---|
| `jest.integration.config.js` | `npx jest --config jest.integration.config.js` |
| `vitest.integration.config.ts` | `npx vitest --config vitest.integration.config.ts` |
| `pytest.ini` with `[integration]` or `-m integration` | `pytest -m integration` |
| `cypress.config.js` / `cypress.config.ts` | `npx cypress run` |
| `playwright.config.js` / `playwright.config.ts` | `npx playwright test` |
| `docker-compose.test.yml` | `docker compose -f docker-compose.test.yml up --abort-on-container-exit` |
| `*.integration.test.ts` / `*.integration.spec.ts` pattern | `npx jest --testPathPattern="integration"` |

If none found → skip: "No integration/e2e config found — skipping."

### 4. Run Integration Tests
Max 3 retries. On failure:

**4b. Serena (optional):** See `serena/SKILL.md:Setup` — `find_referencing_symbols`/`get_diagnostics_for_file` per failing module to surface mismatches. Skip if unavailable.

Trace failure to source module, fix, re-run.

### 5. Run E2E & Web QA Automation
- **Web/Frontend Projects**: ALWAYS automatically invoke `/supergraph:playwright-tester` to generate or verify QA matrix coverage (Happy path, Sad path, Boundary, Network 500 error injection, Auth/RBAC) before proceeding.
- **CLI/Command Runner**: Run `npx playwright test`. Max 2 retries (e2e is inherently flaky). Flaky tests: annotate with `@flaky` / `test.slow()` / `@pytest.mark.flaky` per framework — do not block merge on known-flaky tests.

### 6. Graph Validation
For `CBM_PROJECT` via `codebase-memory-mcp` (see `references/codebase-memory-contract.md`) — `search_graph`/`trace_path` + recipes `dependencies/cross-boundary/test-gaps`; fall back to Serena/filesystem if empty.

### 7. Update Plan Status
Pass → mark in-progress tasks `Status: completed`.
Fail after 3 retries → mark `stuck`, append failure log.

### 8. Report
```
✅ /supergraph:integration complete
- Unit: PASS | Integration: PASS|FAIL|SKIP | E2E: PASS|FAIL|SKIP
- Cross-module flows: N/M covered | Surprising connections: [list/none]
- Plan status: updated|none
- Next: /supergraph:verify → /supergraph:review
```

## Rules
- Unit tests MUST pass BEFORE running integration
- Integration failures take priority over e2e (fix foundation first)
- Max 3 retries integration, 2 retries e2e
- Never block merge on `@flaky`-annotated e2e tests
- Always update plan status after completion
- After integration pass → `/supergraph:verify` → `/supergraph:review`
