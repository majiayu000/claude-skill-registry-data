---
name: tdd
description: Red/Green TDD protocol — write a failing test first, implement the minimum to pass, then refactor. Use for any new feature or bug fix.
---

# Red/Green TDD Protocol

## The sequence (never skip RED)

1. **RED** — write a test that exercises the behavior you're about to add
   or fix. Run it. Confirm it FAILS for the reason you expect (not a typo,
   not a missing import — the actual missing behavior).
2. **GREEN** — write the minimum code that makes the test pass. Resist the
   urge to also handle cases nobody asked for yet.
3. **REFACTOR** — with the safety net of a passing test, clean up
   duplication or naming. Re-run the test after every refactor step.

## Why RED matters

A test written after the implementation can pass for the wrong reason (it
might not actually exercise the new code path). Seeing it fail first is the
only proof the test is meaningful.

## Test structure conventions

<Fill in once your project has a test runner and a convention. Example
shape for a TypeScript + vitest project:>

- Unit tests live next to the source file: `foo.ts` → `foo.test.ts`, or in
  a sibling `__tests__/` directory.
- Name tests by behavior, not by implementation detail:
  `"returns null when input is empty"`, not `"test1"`.
- One assertion concept per test — multiple `expect()` calls checking the
  same behavior are fine; testing two unrelated behaviors in one test is
  not.

## Mocking

<Fill in your project's stance. Common defaults: mock external I/O
(network, filesystem, clock) at the boundary; don't mock the thing you're
actually testing; prefer real objects over mocks for your own code's
collaborators when the real thing is fast and deterministic.>

## Regression tests

Every bug fix gets a test that reproduces the bug BEFORE the fix (watch it
fail), then passes after. This is the same RED/GREEN sequence applied to a
defect instead of a new feature.

## Running the suite

<Fill in your actual test command, e.g. `bun test`, `npm test`, `pytest`,
`go test ./...`.> Run the full area's suite before committing — not just
the one test file you touched.
