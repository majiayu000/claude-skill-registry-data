---
name: test
description: "Detects the repository's test runner, runs the suite and adds missing tests for changed code including edge cases and failure paths. Use when tests should run or be extended, a change lacks coverage, or someone asks to run or add tests."
---

# Test

Run the repository's tests and make sure changed behaviour is covered.

## When to use

- After changing code, before committing or opening a pull request.
- When a change has no tests yet.
- When a test fails and the cause is unclear.

## Steps

1. Detect the runner instead of assuming one: `task test:<suite>` targets, `go test`,
   `pytest` or `unittest`, `helm unittest`, `tofu test`, `vitest`. Prefer the task targets.
2. Run the full suite once for a baseline. If it is already red before the change, say so
   instead of attributing the failure to the change.
3. For each changed behaviour, check whether a test asserts it. Add missing tests next to
   the existing ones, in the repository's established style.
4. Cover deliberately: the happy path, boundaries (empty, zero, one, maximum, unicode,
   very large), failure paths (errors, timeouts, cancelled context, denied permission,
   malformed input), and idempotency for a reconciler or a migration.
5. Assert behaviour, not implementation details.
6. Run the suite again. Report the real output. If something still fails, show the
   failure and state whether it relates to the change.

Never delete or skip a failing test to make a run pass. Fix the cause or report it.

## Guardrails

- Runner detected, not assumed. No second runner introduced.
- Baseline run done before judging a failure as caused by the change.
- New behaviour covered, including failure paths and boundaries.
- Tests deterministic and independent of each other.
- Final result reported verbatim. No failing test removed or skipped to pass.

## References

- `lint` for formatting and static checks before the suite runs.
- `testing-conventions` for when a test is written, what earns one and test form.
