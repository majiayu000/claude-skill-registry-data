---
name: tdd
description: Use when implementing features or fixing bugs test-first, when user mentions "red-green-refactor", when test discipline is required for a specific task, when incremental-implementation needs TDD enforcement, or when a behavior change needs a failing test before any code is written.
---

# Test-Driven Development

## Overview

Tests verify behavior through public interfaces, not implementation details. One failing test → minimum code to pass → repeat. Never write all tests first. See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## When to Use

- Implementing a task from `.forge/tasks.yaml` that needs test-first discipline
- Any feature or bug fix where behavior must be proven before merging
- User explicitly asks for TDD or red-green-refactor

## When NOT to Use

- Writing tests retroactively for already-working code — that's a different activity
- Exploratory spike to understand a problem space — spike first, then TDD the result
- Config changes with no behavioral assertions possible

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll write tests after the implementation works" | Then you test implementation shape, not behavior |
| "Writing all tests first is TDD" | That's horizontal slicing — produces brittle tests |
| "This behavior is obvious, no test needed" | Obvious behaviors are the ones that silently break |
| "I need to mock my own modules to test this" | Your interface boundaries need rethinking |
| "The test is too hard to write" | The interface is too hard to use — fix the interface |

## Red Flags

- Test names describe HOW not WHAT ("calls paymentService.process")
- Test mocks internal collaborators owned by the same codebase
- Test breaks on refactor when behavior didn't change
- All tests written before any implementation ("horizontal slicing")
- Test verifies through side effects or database state instead of interface
- `.forge/testing-strategy.md` exists but was not read before writing the first test (its per-module coverage decisions override TDD defaults)

## Precedence with testing-strategy

If `.forge/testing-strategy.md` exists, **read it first.** It is the authoritative source for per-module test policy. TDD's default is "every behavior gets a test"; the strategy may carve exceptions:

- Module marked **integration-only** → skip unit tests for that module; write the integration test instead. The RED step is still required — it just lives at the integration layer.
- Module marked **contract-only** (verified by consumer-driven contracts) → write the contract test, not a unit test.
- Module marked **no-test** (rare; usually trivial glue) → document the exception in your commit message and skip the test step. If you find yourself doing this often, the strategy is too permissive — file `/feedback` targeting `.forge/testing-strategy.md`.

When testing-strategy and a task's `acceptance_criteria` disagree about coverage, the task's acceptance criteria win for that task — but file `/feedback` targeting `.forge/testing-strategy.md` so the strategy gets updated next sprint.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.**

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED → GREEN: test1 → impl1
  RED → GREEN: test2 → impl2
  RED → GREEN: test3 → impl3
```

Each test responds to what you learned from the previous implementation cycle.

## Workflow

### 1. Plan before coding

- [ ] Read `.forge/testing-strategy.md` if it exists; note per-module coverage exceptions
- [ ] Confirm public interface changes with user (or with task's contract from `.forge/contracts/`)
- [ ] List behaviors to test — not implementation steps
- [ ] Design interface for [testability](interface-design.md)
- [ ] Identify [deep module](deep-modules.md) opportunities
- [ ] Get user approval before writing the first test

### 2. Tracer bullet (2-stage RED required)

Write ONE test that proves the end-to-end path works. **RED must be observed twice**: first as an existence failure, then as a behavior failure.

```
RED-1 (existence): Write test for first behavior → expect ERR_MODULE_NOT_FOUND
                   / NameError / "function not defined" — the module or symbol
                   the test imports doesn't exist yet. This proves the test
                   ran. It does NOT prove the test discriminates correct from
                   incorrect implementations.

STUB:              Create the file / function / class with the correct
                   signature, returning a deliberately wrong value (empty
                   string, 0, null, []). Just enough to satisfy the import.

RED-2 (behavior):  Re-run the test → expect AssertionError. The test now
                   fails on a behavior mismatch, not a missing symbol. This
                   proves the test would CATCH a wrong implementation —
                   not just a missing one.

GREEN:             Replace the stub with the real implementation. Test passes.
```

**Why two stages.** A single-stage RED (existence failure → write whole implementation) leaves you unable to distinguish "the test failed because the implementation is wrong" from "the test failed because of a typo in the import path." Most failing tests look the same from far away. The 2-stage pattern proves the test has *discriminating power*: it rejects a wrong-value stub of the correct shape. If RED-2 doesn't fail with an AssertionError, the test isn't really testing the behavior — it's testing the existence of the symbol.

This pattern was promoted from emergent practice to documented gold standard after the v3.2.0 dry-run (issue #36). Strict TDD literature varies on whether import-fail counts as RED; the behavior-fail standard removes the ambiguity.

### 3. Incremental loop

For each remaining behavior:

```
RED-1 (existence — usually skipped after the tracer bullet): file/module exists
RED-2 (behavior): Write next test → AssertionError (real behavior mismatch)
GREEN:            Minimum code to pass → passes
REPEAT
```

After the first cycle, the file usually exists already so RED-1 collapses into RED-2 immediately. The discipline still applies: the test that fails must fail on an *assertion*, not on a missing import or syntax error.

Rules: one test at a time, only enough code for the current test, no speculative features.

### 4. Refactor

After all tests pass — see [refactoring.md](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Run tests after each refactor step
- [ ] **Never refactor while RED**

## Per-Cycle Checklist

- [ ] Test describes behavior (WHAT), not implementation (HOW)
- [ ] Test uses public interface only — no private method access
- [ ] Test would survive internal refactor without breaking
- [ ] Implementation is minimal — no speculative features
- [ ] Test name reads like a specification sentence

## Verification

- [ ] All behaviors listed in Step 1 have a passing test
- [ ] **RED was observed as a behavior failure (AssertionError / expected-vs-actual mismatch), not merely a module-not-found or symbol-undefined error.** For the first behavior of a new module: RED-1 (existence) → write stub with correct signature returning wrong value → RED-2 (assertion mismatch) → GREEN. The 2-stage pattern proves the test has discriminating power.
- [ ] No tests mock internal collaborators
- [ ] Full test suite passes (not just new tests)
- [ ] Refactor pass complete — no duplication, no shallow modules
- [ ] If task from tasks.yaml: all acceptance criteria verified

## Fit-Check

Before declaring done, emit one of:

- A short list of specific fit issues observed (e.g., "TDD overhead exceeded the work for this single-config-line change — recommend skipping the test layer next time" / "Behavior was hard to test through public interface; suggests the interface needs rethinking, not the test").
- The explicit line: **"No fit issues observed for this use case."**

Silence is not allowed. See [docs/skill-anatomy.md#fit-check](../../docs/skill-anatomy.md#fit-check-the-meta-honesty-step).
