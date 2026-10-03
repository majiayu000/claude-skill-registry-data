---
name: tdd
description: "Discipline skill — TDD red-green-refactor cycle. Use when implementing any feature or bugfix, before writing implementation code."
user-invocable: true
---

# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## Usage

`/tdd`

Invoke this skill before implementing any feature or bugfix. It establishes the discipline for your implementation session.

## When to use

- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the user):** throwaway prototypes, generated code, configuration files.

## The Iron Law

```text
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## Red-Green-Refactor

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Requirements:**

- One behavior per test
- Clear name that describes behavior
- Real code (no mocks unless unavoidable)

**Run the test. Confirm:**

- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

Test passes? You're testing existing behavior. Fix the test.

### GREEN - Minimal Code

Write the simplest code to pass the test.

Don't add features, refactor other code, or "improve" beyond the test.

**Run the test. Confirm:**

- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

Test fails? Fix code, not test.

### REFACTOR - Clean Up

After green only:

- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next behavior.

## Good Tests

| Quality          | Good                                | Bad                                                 |
| ---------------- | ----------------------------------- | --------------------------------------------------- |
| **Minimal**      | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear**        | Name describes behavior             | `test('test1')`                                     |
| **Shows intent** | Demonstrates desired API            | Obscures what code should do                        |

## Common Rationalizations

| Excuse                           | Reality                                                                 |
| -------------------------------- | ----------------------------------------------------------------------- |
| "Too simple to test"             | Simple code breaks. Test takes 30 seconds.                              |
| "I'll test after"                | Tests passing immediately prove nothing.                                |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested"        | Ad-hoc is not systematic. No record, can't re-run.                      |
| "Deleting X hours is wasteful"   | Sunk cost fallacy. Keeping unverified code is technical debt.           |
| "Need to explore first"          | Fine. Throw away exploration, start with TDD.                           |
| "Test hard = design unclear"     | Listen to the test. Hard to test = hard to use.                         |
| "TDD will slow me down"          | TDD is faster than debugging.                                           |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Rationalizing "just this once"
- "I already manually tested it"
- "Keep as reference"

**All of these mean: Delete code. Start over with TDD.**

## Bug Fix Flow

1. Write failing test reproducing the bug
2. Verify RED (test fails as expected)
3. Implement minimal fix
4. Verify GREEN (test passes, all tests pass)
5. Refactor if needed

Never fix bugs without a test.

## When Stuck

| Problem                  | Solution                                              |
| ------------------------ | ----------------------------------------------------- |
| Don't know how to test   | Write wished-for API. Write assertion first.          |
| Test too complicated     | Design too complicated. Simplify interface.           |
| Must mock everything     | Code too coupled. Use dependency injection.           |
| Test setup huge          | Extract helpers. Still complex? Simplify design.      |

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## Related Skills

- `/debug` — systematic debugging when tests reveal unexpected failures
- `/verify` — verification before claiming work is complete
