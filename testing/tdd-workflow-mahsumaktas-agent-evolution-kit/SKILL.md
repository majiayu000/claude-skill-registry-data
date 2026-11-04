---
name: tdd-workflow
description: "Test-Driven Development workflow. Write tests BEFORE implementation code."
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write the minimum code to make it pass.

**Core principle:** If you did not watch the test fail, you do not know whether you are testing the right thing.

**Violating the letter of these rules violates their spirit.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavioral changes

**Exceptions (ask the user):**
- Throwaway prototypes
- Generated code
- Configuration files

If you are thinking "I will skip TDD just this once" — stop. That is rationalization.

## Iron Rule

```
NO PRODUCTION CODE WITHOUT A FAILING TEST
```

Wrote code before the test? DELETE IT. Start over.

**No exceptions:**
- Do not keep it "for reference"
- Do not "adapt" it while writing tests
- Do not even look at it
- Delete means delete

Implement from scratch, starting from tests. Period.

## Red-Green-Refactor Cycle

```
RED (Write a failing test)
  |
  v
Fails correctly? --NO--> Fix the test
  |
  YES
  |
  v
GREEN (Write minimum code)
  |
  v
All tests pass? --NO--> Fix the code
  |
  YES
  |
  v
REFACTOR (Clean up)
  |
  v
Still green? --NO--> Revert the refactor
  |
  YES
  |
  v
Next test --> Return to RED
```

### RED -- Write a Failing Test

Write one minimal test that shows what should happen.

**Good:**
```typescript
test('retries failed operations 3 times', async () => {
  let attemptCount = 0;
  const operation = () => {
    attemptCount++;
    if (attemptCount < 3) throw new Error('failed');
    return 'success';
  };

  const result = await retry(operation);

  expect(result).toBe('success');
  expect(attemptCount).toBe(3);
});
```
Clear name, tests real behavior, tests one thing.

**Bad:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retry(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```
Vague name, tests the mock instead of the code.

**Requirements:**
- One behavior per test
- Clear, descriptive name
- Real code (avoid mocks unless unavoidable)

### RED Verify -- Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

Check:
- Test fails (not errors)
- Failure message is what you expected
- It fails because the feature is missing (not because of a typo)

**Test passes?** You are testing existing behavior. Fix the test.

**Test errors?** Fix the error, re-run until it fails correctly.

### GREEN -- Minimum Code

Write the simplest code that makes the test pass.

**Good:**
```typescript
async function retry<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass.

**Bad:**
```typescript
async function retry<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI -- do not add things that were not asked for
}
```
Over-engineering.

Do not add features beyond the test. Do not refactor other code. Do not "improve" anything.

### GREEN Verify -- Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Check:
- Test passes
- Other tests still pass
- Output is clean (no errors, no warnings)

**Test fails?** Fix the code, not the test.
**Other tests fail?** Fix them now.

### REFACTOR -- Clean Up

Only after green:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Do not add behavior.

### Repeat

Next failing test for the next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | Tests one thing. If the name contains "and", split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes the behavior | `test('test1')` |
| **Shows intent** | Reveals the desired API | Hides what the code should do |

## Why Order Matters

**"I will write tests afterward to verify my work"**

Tests written after pass immediately. Passing immediately proves nothing:
- You might be testing the wrong thing
- You might be testing the implementation, not the behavior
- You will miss edge cases you did not think of
- You never saw the test catch an error

Test-first forces you to see the test fail, proving it actually tests something.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "No need to test, it is too simple" | Simple code breaks too. The test takes 30 seconds. |
| "I will test later" | Tests that pass immediately prove nothing. |
| "Tests written after serve the same purpose" | After = "what does this do?" Before = "what should it do?" |
| "I already tested manually" | Ad-hoc is not systematic. No record, not repeatable. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep it as reference, write test-first" | You will adapt it. That is test-after in disguise. Delete means delete. |
| "I need to explore first" | Fine. Throw away the exploration, then start with TDD. |
| "Test is hard = design is unclear" | Listen to the test. Hard to test = hard to use. |
| "TDD slows me down" | TDD is faster than debugging. Pragmatic = test-first. |
| "Manual testing is faster" | Manual testing does not prove edge cases. You re-test on every change. |
| "Existing code has no tests" | You are improving. Add tests for the code you are changing. |

## Red Flags -- STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Cannot explain why the test fails
- Tests added "later"
- "Just this once" rationalization
- "I already tested manually"
- "Keep it as reference" or "adapt the existing code"
- "I spent X hours, deleting is wasteful"
- "TDD is dogmatic, I am pragmatic"
- "This is different because..."

**All of these mean: Delete the code. Restart with TDD.**

## Verification Checklist

Before marking work as complete:

- [ ] Every new function/method has a test
- [ ] I watched every test fail BEFORE implementing
- [ ] Every test failed for the expected reason (missing feature, not typo)
- [ ] I wrote the minimum code to make each test pass
- [ ] All tests pass
- [ ] Output is clean (no errors, no warnings)
- [ ] Tests use real code (mocks only when unavoidable)
- [ ] Edge cases and error paths are covered

Cannot check all boxes? You skipped TDD. Start over.

## Debug Integration

Bug found? Write a failing test that reproduces the bug. Follow the TDD cycle. The test proves the fix and prevents regression.

Never fix a bug without a test.

**REQUIRED SKILL:** `systematic-debugging` (when the test fails unexpectedly)
