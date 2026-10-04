---
name: test-driven-development
description: Use when implementing any feature, bugfix, refactor, or behavior change, before writing implementation code.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (ask the user first):** throwaway prototypes, generated code, config files.

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

    NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

Wrote code before the test? Delete it. Start over. No exceptions — don't keep it "as
reference," don't "adapt" it while writing tests, don't even look at it. Implement fresh from
the test.

## Red → Green → Refactor

### RED — write a failing test
One minimal test for one behavior. Clear name. Tests real behavior — avoid mocks unless
unavoidable. In ExUnit:

```elixir
test "rejects an empty email" do
  assert {:error, changeset} = Accounts.register_user(%{email: ""})
  assert "can't be blank" in errors_on(changeset).email
end
```

A name with "and" in it is two tests — split it.

### Verify RED — watch it fail (MANDATORY, never skip)
Run the focused test: `mix test test/path/to_test.exs:LINE`. Confirm:
- It **fails** (not errors) — a compile error or typo is not a real RED; fix and re-run until
  it fails for the right reason.
- The failure is because the feature is **missing**, not because the test is wrong.
- A test that **passes immediately** is testing existing behavior — fix the test.

### GREEN — minimal code to pass
Simplest code that makes the test pass. Don't add options, flags, or "improvements" beyond
what the test demands (YAGNI).

### Verify GREEN — watch it pass (MANDATORY)
Re-run the focused test. Confirm it passes, neighbors still pass, and output is **pristine**
(no warnings or noise — this project compiles warnings-as-errors). Test fails? Fix the code,
not the test.

### REFACTOR — clean up (only while green)
Remove duplication, improve names, extract helpers. Add no behavior. Keep tests green.

Then repeat for the next behavior.

## Why Order Matters

- **"I'll write tests after to verify it works"** — tests written after pass immediately, which
  proves nothing: they might test the wrong thing, test the implementation rather than behavior,
  or miss the edge case you forgot. You never saw the test catch a bug.
- **"Tests-after achieve the same goal"** — no. Tests-after answer "what does this do?";
  tests-first answer "what *should* this do?" Tests-after are biased by the code you already
  wrote.
- **"Deleting hours of work is wasteful"** — sunk cost. The waste is keeping code you can't
  trust. Working code without real tests is technical debt.
- **"I already manually tested it"** — ad-hoc ≠ systematic. No record, can't re-run, easy to
  forget cases under pressure.

## Red Flags — STOP and start over

Code before test · test after implementation · test passes immediately · can't explain why a
test failed · "just this once" · "keep as reference" · "I already manually tested it" · "it's
about spirit not ritual" · "this is different because…". All of these mean: delete the code,
restart with TDD.

## When Stuck

| Problem | Solution |
|---|---|
| Don't know how to test | Write the wished-for API in the test first. Ask the user. |
| Test too complicated | The design is too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Inject dependencies instead. |

## Debugging Integration

Bug found? Write a failing test that reproduces it first, then follow Red → Green. The test
proves the fix and prevents regression. Never fix a bug without a test.

## Verification Checklist (before marking work complete)

- [ ] Every new function/behavior has a test
- [ ] Watched each test fail before implementing
- [ ] Each failed for the expected reason (feature missing, not a typo)
- [ ] Wrote minimal code to pass
- [ ] All tests pass; output pristine (no warnings)
- [ ] Tests use real code (mocks only if unavoidable); edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over. No exceptions without the user's permission.
