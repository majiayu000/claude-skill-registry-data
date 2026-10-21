---
name: tdd
description: Use when implementing any feature, bug fix or behaviour change, before writing production code, or when the user mentions test-first, red-green-refactor or TDD. Runs the red-green-refactor loop at agreed seams and keeps every test honest.
license: MIT
metadata:
  plugin: book-of-engineering
  kind: practice
  credits:
    - skill: test-driven-development
      author: Jesse Vincent
      url: https://github.com/obra/superpowers/tree/main/skills/test-driven-development
      license: MIT
    - skill: tdd
      author: Matt Pocock
      url: https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd
      license: MIT
---

# Test-driven development

Write the test first. Watch it fail. Write the minimal code that makes it pass. Clean up. Repeat.

**Core principle:** if you did not watch the test fail, you do not know that it tests the right thing.

## When this applies

Always: new features, bug fixes, refactors, behaviour changes.

Exceptions, only with the user's agreement: throwaway prototypes, generated code, configuration files.

Thinking "skip TDD just this once"? That is a rationalization. See the table below.

## The iron law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it and start over from the test. Do not keep it "as reference", do not adapt it while writing tests, do not look at it. Implement fresh from the tests.

## Before the loop: agree the seams

A **seam** is the public boundary you test at: the interface where behaviour is observable without reaching inside. Tests live at seams, never against internals.

Before the first test, write down which seams you will test and confirm them with the user when the interface is new or unclear. Give each proposed seam one line on what it catches and what it misses. Testing effort then lands on critical paths and real logic instead of every edge of every private function.

If the shape of the interface is itself in question, settle that first: a module that is hard to test is hard to use.

## The loop: red, green, refactor

Work in **vertical slices**: one test, one minimal implementation, then the next test. Do not write all tests first and then all code. Bulk tests verify imagined behaviour and commit you to a structure before you understand the implementation. Each test is a tracer bullet that responds to what the last cycle taught you.

### RED: write one failing test

One behaviour, a clear name that states the behaviour, real code rather than mocks wherever possible.

```typescript
// Good: clear name, exercises real code, one behaviour
test('retries a failing operation up to 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  const result = await retryOperation(operation);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});

// Bad: vague name, asserts on the mock instead of the code
test('retry works', async () => {
  const mock = jest.fn().mockRejectedValueOnce(new Error()).mockRejectedValueOnce(new Error()).mockResolvedValueOnce('ok');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```

Before writing the body, name the production change that would make this test fail. If you cannot name one, redesign the test around an observable behaviour. See [writing-good-tests.md](writing-good-tests.md).

### Verify RED: watch it fail

Mandatory. Run the test and confirm:

- it fails, it does not error;
- it fails for the expected reason (the feature is missing), not a typo or an import problem;
- the failure message is the one you expected.

Test passes immediately? You are testing existing behaviour; fix the test. Test errors? Fix the error and re-run until it fails correctly.

### GREEN: write the minimal code

The simplest code that makes this test pass. No extra parameters, no options object, no features the test did not ask for, no refactoring of other code.

```typescript
// Good: just enough
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try { return await fn(); } catch (e) { if (i === 2) throw e; }
  }
  throw new Error('unreachable');
}

// Bad: maxRetries, backoff strategy, onRetry callback. Nothing asked for them.
```

### Verify GREEN: watch it pass

Mandatory. Run the test and confirm it passes, the rest of the suite still passes, and the output is clean (no errors, no warnings).

"The rest of the suite" means the project's test command, not only your file. Run it before calling the change done, even when the task named a single test file. A failure that run shows goes in your report by name, including one you did not cause. A red test you watched scroll past and did not mention is a report falsified by omission.

Test fails? Fix the code, not the test. Other tests fail? Fix them now.

### REFACTOR: clean up, stay green

Only after green: remove duplication, improve names, extract helpers. Do not add behaviour. Keep the tests green throughout.

### Repeat

Write the next failing test for the next slice of behaviour.

## Good tests

| Quality | Good | Bad |
|---|---|---|
| Minimal | One behaviour. An "and" in the name means split it. | `test('validates email and domain and whitespace')` |
| Clear | The name states the behaviour. | `test('test1')` |
| Shows intent | Demonstrates the desired API. | Obscures what the code should do |
| Independent | Expected values are hand-derived literals. | Expected value recomputed with the code under test |
| At a seam | Observes behaviour through the public interface. | Mocks internal collaborators, queries the database to check a write |

The full rules, including when a mock is justified and how to check a test file before finishing, are in [writing-good-tests.md](writing-good-tests.md). Read it whenever you write or change a test, add a mock, or add a test helper.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. The test takes thirty seconds. |
| "I'll test after" | Tests written after pass immediately, which proves nothing. You never watched them fail, so you never proved they can catch the bug. |
| "Tests after achieve the same goal" | Tests-after answer "what does this do?"; tests-first answer "what should this do?". Tests-after are biased by the code you already wrote. |
| "Already manually tested" | Manual testing leaves no record and cannot be re-run. Automated tests run the same way every time. |
| "Deleting X hours of work is wasteful" | That time is spent either way. Keeping code you cannot trust is the waste. |
| "Keep it as reference" | You will adapt it. That is testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw the exploration away, then start with a test. |
| "Hard to test means the design is unclear" | Correct. Listen to the test and simplify the interface. |
| "TDD will slow me down" | TDD is the pragmatic path: it catches bugs before commit and lets you refactor without fear. Debugging in production is slower. |
| "Existing code has no tests" | You are improving it. Add tests for the behaviour you touch. |

## Red flags: stop and start over

Code before test. Test after implementation. Test passes immediately. Cannot explain why the test failed. Tests added "later". "Just this once". "I already tested it manually". "Spirit, not ritual". "Keep as reference". "Already spent X hours". "This is different because...".

All of these mean: delete the code, start over from a failing test.

## When stuck

| Problem | Solution |
|---|---|
| Do not know how to test it | Write the wished-for API. Write the assertion first. Ask the user. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Inject dependencies at the boundary. |
| Test setup huge | Extract helpers. Still complex? Simplify the design. |

## Bugs

Found a bug? Write a failing test that reproduces it, then follow the loop. The test proves the fix and prevents the regression. Never fix a bug without a test.

## Checklist before marking work complete

- [ ] Seams were agreed before the first test.
- [ ] Every new behaviour has a test, and each test was watched failing before the implementation.
- [ ] Each test failed for the expected reason.
- [ ] Each implementation was the minimal code for its test.
- [ ] The whole project suite passes with clean output.
- [ ] Tests exercise real code; mocks only at system boundaries.
- [ ] Edge cases and error paths are covered.
- [ ] The mutation check in [writing-good-tests.md](writing-good-tests.md) was run on each test file.

Cannot tick every box? You skipped TDD. Start over.

```
Production code  ->  a test exists and failed first
Otherwise        ->  not TDD
```
