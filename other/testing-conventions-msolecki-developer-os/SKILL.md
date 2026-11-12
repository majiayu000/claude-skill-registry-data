---
name: testing-conventions
description: Pin the contract in tests with absolute-instant fixtures and partial module mocks. Use when writing or reviewing test files (*.test.*, *.spec.*, tests/, e2e/).
license: MIT
compatibility: "Claude Code"
---

# Tests — pin the contract, remove the ambient dependency

- A test pins the contract, not current behavior. If a test "passes after fixing the test," verify that you did not encode a bug; a red test may describe the correct contract.
- A fixture must pin an absolute instant (`2030-01-01T08:00:00Z`), never a local-time literal. An ambient-timezone fixture hides a contract mismatch until CI runs in a different timezone from your machine.
- Mock a module with a partial built on the original (for example Vitest's `importOriginal`), never an exhaustive hand-written stub. A stub with fixed bounds is a latent failure that fires the day the module gains an export, and one new export can break every suite that stubs it.
- A regression test must fail on the unfixed code: run it before the fix and see it red. A test written after the fix and only ever seen green may not exercise the bug at all.
- Do not fake the boundary that could be wrong. A fake database that returns ready records hides a broken query; test that path against a real test database or the real call.
- A failure message names the missing record or shows the actual response, so the next reader can fix it without rerunning. Never raise retries or timeouts to hide a flaky test; find the race instead.
