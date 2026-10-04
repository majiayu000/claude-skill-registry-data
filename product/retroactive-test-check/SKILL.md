---
name: retroactive-test-check
description: Use when adding a test to an existing codebase for behavior that is already implemented. Ensures the test is meaningful by mutation-verifying it — breaking the production code to confirm the test fails for the expected reason. Triggers when the user says "add a test for existing behavior", "backfill test coverage", "the test passes on first run", or any scenario where a test is written without a corresponding new production change.
---

# Retroactive Test Coverage Verification

When adding tests for behavior that is already implemented (the test passes on first run without any code changes), you MUST verify the test is meaningful by performing mutation-style verification.

## When This Applies

- Adding acceptance tests for features completed in prior work
- Adding unit tests for existing functions
- Backfilling test coverage for untested code
- Any scenario where the test passes before you write implementation code

## Required Process

1. **Write the test** and confirm it passes.
2. **Break the behavior** — make a targeted change to the implementation that should cause the test to fail (e.g., remove a header, change a status code, return a wrong value).
3. **Run the test** and verify it fails **for the expected reason** — the failure message should clearly indicate the broken behavior, not an unrelated error.
4. **Restore the implementation** to its original state.
5. **Run the test** again and verify it passes.

## What "Break the Behavior" Means

Make the smallest change that invalidates what the test asserts. Examples:

- Test asserts a 401 status → change the status to 403
- Test asserts a header value → remove that header
- Test asserts a return value → change the return value
- Test asserts an error message → change the message

If the test has multiple assertions covering different aspects, verify at least one mutation per distinct behavior being tested.

## Common Failure Modes (why first-run-green is a yellow flag)

- Assertions on the wrong variable, or a truthy check that passes on any non-null value
- `expect` inside an unreached branch (async not awaited, early return, try/catch swallowing)
- Mocks that replace the real behavior and then assert on the mock's own return value
- The "new" case is already covered by an existing code path the test happens to hit, so your specific scenario never actually runs
- File isn't in the test suite's include pattern, or the `it`/`test` is inside a `describe.skip`
- Zero-assertion test ("passes" vacuously)
- Async gotcha: unawaited promises let the test finish green before anything throws

## Why

A test that passes without ever failing proves nothing. Mutation verification is lightweight and provides confidence that the test suite will actually catch regressions.
