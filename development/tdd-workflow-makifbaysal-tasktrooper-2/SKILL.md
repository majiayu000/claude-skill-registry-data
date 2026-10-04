---
name: tdd-workflow
category: testing
description: Test-first discipline and what makes a test worth keeping. Use when implementing any feature or bug fix, before writing production code, and whenever writing or changing a test.
source: obra/superpowers (MIT), adapted
---
# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Start over. Don't keep it as "reference", don't "adapt" it while writing tests — delete means delete, implement fresh from the test.

## When to Use

Always: new features, bug fixes, refactoring, behavior changes. Thinking "skip TDD just this once"? Stop. That's rationalization.

**Exceptions — no new test required:** pure config, copy/text, or asset edits, and generated code you did not hand-write. Say so explicitly in your closing message; this matches the standing acceptance criteria's own exemption, it does not replace it.

## Red-Green-Refactor

### RED — write one failing test
- One behavior per test, clear name that describes the behavior.
- Test real code; mocks only when unavoidable (external services). The mock earns no assertions of its own — assert on what your code does with its result, not that the mock was called.
- **Before writing the body, name the production change that would make this test fail.** If you can't name one, you're not testing behavior yet.
- **Derive the expected value independently, by hand** — a literal, not a recomputation. ❌ `expect(build(x)).toBe(build(x))` tests nothing; it recomputes the answer the way the code does, so it passes no matter what. ✅ `expect(build({id:1})).toBe("item-1")`.
- Bad: a test whose assertions only exercise the mock, not the code under test.

### Verify RED — watch it fail (MANDATORY, never skip)
- Run it with the stack's focused command, not the whole suite: `go test ./pkg/... -run TestName`, `npx vitest run path/to.test.tsx`, `flutter test test/x_test.dart`, `./mvnw -q test -Dtest=ClassName`.
- Confirm it FAILS (not errors) and fails because the feature is missing — not a typo or compile error.
- Test passes immediately? It tests existing behavior — fix the test.
- Test errors? Fix the error and re-run until it fails correctly.

### GREEN — minimal code
- Write the simplest code that makes the test pass. Nothing extra (YAGNI).
- No extra options, no speculative parameters, no "while I'm here" improvements.

### Verify GREEN — watch it pass (MANDATORY)
- Run the focused test, then the surrounding suite. **"Other tests" means the whole project's suite, not just your file or package** — a failure that run shows, including one you didn't cause, goes in your closing message by name; it is not silently someone else's problem.
- All green, output pristine (no warnings).
- Test fails? Fix the code, not the test. Other tests fail? Fix now, not later.

### REFACTOR — only while green
- Remove duplication, improve names, extract helpers. No new behavior.
- Then write the next failing test — one test, one implementation step (a vertical slice). Writing every test up front and implementing after ("horizontal slicing") loses the fail-for-the-right-reason check on each one individually.

## No change detectors

Don't assert class names, exact copy, constants, or private structure — a renamed field or a reworded label breaks the test without the behavior changing. Assert the behavior the test's name promises. For pure styling or layout work, the frontend four-width check is the test; a pixel-diff snapshot is not a substitute.

## The mutation check, before finishing

Before you call the step done, ask: if I introduced a wrong constant, flipped a branch, dropped a side effect, returned empty instead of the value, or skipped a validation (zero / empty / nil / unauthorised / malformed) — would ONE of my tests fail? If a mutation like that survives every test green, the test suite has a gap, not full coverage. This is what the run's advisory mutation score is checking for; a high line-coverage number with a low mutation score means assertions are missing, not lines.

## Resumed run (in_progress) with a previous run's untested diff

Don't delete the existing diff. Write the test the code is missing, then prove it CAN fail: temporarily revert just the covered lines (`git stash push <file>` or a targeted edit), run the test (MUST FAIL), restore (`git stash pop`), run again (passes). Then continue from there — this is the same Verify RED discipline applied after the fact, not an exception to it.

## Worked Example

Feature: `slugify(title)` lowercases and hyphenates.

```
RED   test: slugify("Hello World") == "hello-world"
      run → FAIL: slugify is not defined            ← watched it fail, right reason
GREEN func slugify(s) { return strings.ReplaceAll(strings.ToLower(s), " ", "-") }
      run → PASS                                     ← watched it pass
RED   test: slugify("A  B") == "a-b" (collapse runs)
      run → FAIL: got "a--b"                         ← new behavior, fails first
GREEN collapse whitespace before replacing
      run → PASS
REFACTOR extract the whitespace regex, suite still green
```

Each behavior earned its own failing test first. The second test caught a real gap the first implementation missed — which is the whole point of writing it before the code.

## Bug Fixes

A bug fix starts with a failing test that reproduces the bug. The test proves the fix and prevents regression. Never fix a bug without a reproducing test.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks too. The test takes 30 seconds. |
| "I'll test after" | Tests written after pass immediately and prove nothing. |
| "Already manually tested" | Ad-hoc is not systematic: no record, cannot re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Unverified code is technical debt. |
| "Keep it as reference" | You will adapt it — that is testing after. Delete it. |
| "TDD will slow me down" | TDD is faster than debugging in review/QA and revision cycles. |
| "Test is hard to write" | Hard to test = hard to use. Simplify the design. |
| "The expectation and the code share the formula, that's fine" | That's a change detector, not a test — it passes no matter what the code does. |

## Red Flags — STOP and start over

- Code written before its test
- Test passes on the first run
- You cannot explain why the test failed
- An assertion computed the same way the code computes it
- "Tests later", "just this once", "this is different because..."

All of these mean: delete the code, start from the test.

## Checklist before moving the task forward

- [ ] Every new function/behavior has a test
- [ ] Watched each test fail for the expected reason
- [ ] Wrote minimal code to pass
- [ ] Whole suite green, output pristine
- [ ] Edge cases and error paths covered
- [ ] A plausible mutation to the change would fail at least one test

Can't check every box? You skipped TDD. Start over.
