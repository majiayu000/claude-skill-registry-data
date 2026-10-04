---
name: qa-automation
description: "Writing and running automated tests: unit and integration design, fixtures, mocks vs real dependencies, coverage, flake hunting, CI integration. Use when adding, running, fixing, or debugging tests with pytest, vitest, jest, or mocha. Browser, CLI, and HTTP end-to-end flows belong to e2e-qa."
license: MIT
allowed-tools: Bash
metadata:
  display-name: "QA Automation"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "testing unit integration fixtures"
---

# QA automation

## What "test" means here
- **Unit**: pure functions or single classes, no I/O, no network, no clock.
- **Integration**: real dependencies (db, fs, queue) inside the process. Mocks at the system boundary only.
- **E2E**: real running app, hit through its public interface (HTTP, browser, CLI). Covered in the `e2e-qa` skill.

Pick the cheapest level that catches the bug. Most coverage should be unit; a thin layer of integration; a few critical E2E flows. Inverted pyramid = slow, flaky CI.

## Writing a test
- Arrange / Act / Assert structure. One concept per test. If the test name needs "and," it's two tests.
- Test the behavior, not the implementation. "Renders the user's name" beats "calls `formatName()` once."
- Public API only. Don't reach into private state to assert.
- Names describe the scenario AND the expected outcome: `returns_400_when_email_missing`, not `test_email_validation`.
- Fixtures over `beforeEach` setup magic. Explicit data in the test body wins for readability when small.

## Mocks vs reals - the heuristic
- Database, filesystem, in-process queue: use the real thing (sqlite-in-memory, tmp dir, in-memory queue). Fast and faithful.
- HTTP to your own service: real, in a test harness.
- HTTP to a third party: stub at the boundary (`nock`, `respx`, `MSW`). Record real responses once; replay forever.
- Time: inject a clock or use `vi.useFakeTimers()` / `freezegun` / `time-machine`. Never `await sleep(100)` to "wait for" something.
- Randomness: seed it.

Mocking persistence is a known footgun - schema drift between mock and real DB hides real bugs. Default to a real in-memory DB for any test that touches persistence.

## Stack-specific

### Vitest (TypeScript)
- `vitest run` for CI; `vitest` (watch) for dev.
- `expect.soft()` lets multiple assertions report in one run - use sparingly.
- `vi.mock()` for module replacement; reset with `vi.restoreAllMocks()` in `afterEach`.
- `--coverage` uses v8 by default. Aim for meaningful coverage on changed lines, not a global %.
- For React: `@testing-library/react` - query by accessible role/label, not test-ids.

### Jest (TypeScript / JavaScript)
- Similar discipline to Vitest. `jest --watchAll` for dev; `jest --ci` for CI.
- `jest.mock()` is hoisted - order matters less, but resetting via `beforeEach(() => jest.resetAllMocks())` keeps tests isolated.
- Snapshots: commit them, review diffs carefully, never `--update-snapshot` reflexively.

### Pytest (Python)
- `pytest -x --ff` during dev (stop on first fail, prioritize last failures).
- Fixtures with `@pytest.fixture` and explicit scope (`function`/`module`/`session`). Avoid `autouse=True` except for global setup.
- `pytest.mark.parametrize` over loops in test bodies - each row gets its own pass/fail.
- `pytest -k "name"` to run a subset; `-m "marker"` for tagged groups.
- `pytest-randomly` to surface order dependencies; `pytest-xdist` for parallelism.

### HTTP / API integration (any language)
- Spin up the real app on an ephemeral port; hit it with `supertest` / `httpx` / `requests`. No mocking your own server.
- Database: per-test transaction that rolls back, or a fresh in-memory schema per test file.
- Auth: factor out a `login()` helper; don't copy-paste the JWT flow into every test.

## Coverage discipline
- Coverage % alone is meaningless. A 100%-covered function with assertions like `expect(result).toBeDefined()` is worthless.
- Focus on: the function's preconditions, branches, error paths, edge values (empty, max, negative, unicode).
- Lines you can't easily cover (truly unreachable defensive checks) - delete them. Don't add tests to chase the metric.

## Flake hunting
A flaky test is broken. Don't retry it in CI; fix it.
- Common causes: timing (`sleep`, race conditions), shared state across tests, real network, non-deterministic ordering, time-of-day logic.
- Reproduce locally with `--shuffle` / `pytest-randomly` and `--repeat-each=20`.
- If the underlying code is genuinely racy, the test surfaced a real bug - fix the code.

## Adding tests to existing code
1. Write the test first - for a real bug, write the failing test that reproduces it before fixing.
2. Run only that test until green.
3. Run the surrounding suite to check you didn't break neighbors.
4. Run the full suite at least once before committing.

## CI integration
- Tests must pass deterministically on a clean checkout, no env vars beyond what `.env.example` documents.
- Snapshot/golden files: commit them; review the diff carefully on changes.
- Don't `--ignore` failing tests to merge a PR. Fix or delete.
