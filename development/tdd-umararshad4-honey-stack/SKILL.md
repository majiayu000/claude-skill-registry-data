---
name: tdd
description: "Use when building or fixing test-first, or the user mentions TDD, red-green or a regression test."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills tdd (SKILL.md, tests.md, mocking.md, refactoring.md); obra/superpowers 7.0.0 skills/test-driven-development (SKILL.md, writing-good-tests.md); cursor/plugins pstack 0.15.25 skills/tdd, skills/principle-test-behavior-not-implementation"
---

# TDD

Tests verify behavior through the public interface. The code underneath can change entirely and the tests should not care. A test that fails when you rename an internal function was testing implementation.

## Vertical slices, not horizontal

One test, then the code that passes it, then the next test. Each cycle answers what the previous one taught you.

```
WRONG (horizontal)            RIGHT (vertical, tracer bullets)
RED:   test1 test2 test3      test1 -> impl1
GREEN: impl1 impl2 impl3      test2 -> impl2
                              test3 -> impl3
```

Writing every test first pins imagined behavior: signatures and data shapes instead of what callers observe. Those tests pass when behavior breaks and fail when it is fine.

## Loop

1. **List the slices.** Name the public interface and the behaviors that matter, most important first: critical paths and complex logic, not every edge case. Use the project's domain words (CONTEXT.md, docs, existing tests). Done when: an ordered behavior list exists.
2. **Tracer bullet.** Write one test for the first behavior through the real path, end to end. Run it and read the failure: it fails because the behavior is missing, not because of a typo, import error or bad setup. Then write the least code that passes, and run it green. Done when: you watched it fail for the right reason, then pass.
3. **Repeat** for the next behavior. Write only enough code for the current test; later tests get their own cycle. Done when: every listed behavior went red, then green.
4. **Refactor on green**, never on red. Candidates are in `references/refactoring.md`. Run the tests after each step. Done when: green after the last step.
5. **Run the project's whole test command**, not only your file. Report every failure by name, including ones you did not cause. Done when: the full-suite output is read.

## Each test

- Name the production change that would make it fail. It should be a bug (wrong branch, missing effect, bad boundary), not a decision like a constant's value or message wording.
- Derive the expected value by hand as a literal. An expectation computed by the code under test always passes.
- Drive it through the interface callers use, and assert what the contract promises, no more and no less.
- Mock only at system boundaries. Read `references/mocking.md` before adding a mock or test helper.
- For good and bad examples, and the mutation check before you finish, read `references/tests.md`.

## Bug fixes and regression tests

1. Reproduce the bug as a failing test at the narrowest cheap seam already used for that code path. For an unclear cause, find the root cause with the `debug` skill first.
2. Run it and confirm it fails for the reported reason. Fix with the smallest change, then rerun.
3. To prove the test guards the fix: revert the fix and watch it fail, then restore it and watch it pass.
4. Report the failing-before run and the passing-after run.

If no cheap test path exists (it would need a broad harness, production-only state, brittle mocks or slow end-to-end setup), use the closest executable check instead, such as a repro script, a command or a browser flow, and say why. No test is better than a test that only exercises mocks.

## When stuck

| Problem | Move |
|---|---|
| Can't see how to test it | Write the call you wish existed, then the assertion, then make it real. |
| Setup is huge or everything needs a mock | The design is too coupled. Name the missing seam (the boundary a test should enter through) and point to `/honey:architecture` for a behavior-preserving refactor that creates it, instead of mocking every collaborator. |
| Test passes on its first run | It tests existing behavior or nothing. Fix the test before writing code. |

## Explicit strict TDD

Applies when the user asks for strict TDD. Response modes do not change the test workflow.

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Production code written before its test gets deleted, not kept as reference or adapted, and is reimplemented from the test. Tests written after the code pass immediately, so they never prove they can catch the bug. Exceptions are throwaway prototypes, generated code and config, and only with the user's say-so.

Start the slice over if a test passes before the code exists, if you can't explain why it failed, or if a test is being deferred to "after".

Otherwise run the same loop, but a slice with no cheap test seam may use the closest executable check (see above) and name it in the receipt.
