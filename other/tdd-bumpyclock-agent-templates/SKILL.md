---
name: tdd
description: "Test-first development. Use when the user or repository explicitly requires TDD."
---

# Test-first development

Use TDD only when the user or repository requests test-first work and there is an observable behavior with an independent expectation.
Do not manufacture tests for mechanical configuration, wiring, or type changes that would only restate the implementation; use relevant existing checks instead.

TDD is the red-to-green loop: one failing test, then enough implementation to pass it.

## Test quality and seams

Before writing tests, read [Test behavior, not implementation](../../programming/references/principles/principle-test-behavior-not-implementation.md).
It owns test quality, user-confirmed seams, domain vocabulary, anti-patterns, and mocking guidance.
Apply those rules before and during every cycle, not as a cleanup pass after implementation.

## Work in vertical slices

1. Select one requested behavior at a user-confirmed seam and a plausible failure that one focused test should detect.
   Use a thin path through relevant consumers when integration is part of the uncertainty; this does not require a browser or full-system test.
2. **Red:** add or select the test and run it before changing the implementation.
   Confirm that it fails for the intended behavior, not a syntax, setup, or dependency error.
   If it already passes, determine whether the behavior exists or the assertion cannot distinguish it; do not break correct code to manufacture red.
3. **Green:** implement the smallest complete behavior for that slice, run the focused check, and correct supported failures.
   Do not weaken useful assertions to obtain a pass or anticipate future tests with speculative features.

Use one seam, one test, and one minimal implementation per cycle.
Continue through remaining requested behaviors instead of writing a batch of speculative tests before any implementation.
Let each completed slice inform the next test.

## Refactoring boundary

Refactoring is not part of the red-to-green implementation loop.
Defer it to the review stage; use [Code review](../code-review/SKILL.md) for that work.

## Completion

Complete the requested behavior through its consumers and correct material gaps exposed by relevant checks.
Broaden validation only for affected integrations, failures, or unresolved risks; reuse sufficient evidence after the latest relevant change.
If a runner is unavailable, use an equivalent that preserves the required semantics and restrictions or report the missing red/green observation. An unrun check is not a pass.
Report delivered behavior, observed check results, and remaining limits.
