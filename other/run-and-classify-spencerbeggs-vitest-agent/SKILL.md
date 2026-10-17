---
name: run-and-classify
description: Invoke run_tests via MCP and surface stable / new-failure / flaky / recovered classifications. Use any time you need to know the current state of the test suite, especially before deciding whether to advance a TDD phase.
---

# Run and classify

1. Call `run_tests({ project?, files? })` — by default this runs the full suite via Vitest's programmatic API. There is no `file` (singular) or `filter` field; an unknown key is silently dropped and the whole suite runs instead of the intended subset.
2. The reporter writes `test_runs` and `test_history` rows.
3. Call `test_status({ project? })` to read the per-test classifications.

## Decision matrix

- **stable**: nothing to do. The test passed and has been passing.
- **new-failure**: investigate. Use `interpret-test-failure` and `record-hypothesis-before-fix` before editing production code.
- **persistent**: a real bug or a flawed test. Resist the urge to disable; record a hypothesis and triangulate.
- **flaky**: do not silence. Investigate the source of nondeterminism (timing, shared state, external resources). The system records flaky classifications so the human reviewer can see them.
- **recovered**: a previously-failing test now passes. Note in a hypothesis whether your last edit caused the recovery (intended) or whether the recovery is unrelated (concerning — investigate).

## Reusable outside TDD

Every workflow that runs tests uses this. The orchestrator depends on it for phase-transition evidence.
