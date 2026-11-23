---
name: add-test-coverage
description: >
  Add focused, meaningful tests for high-risk untested code paths, then actually run
  them and verify they fail when the behaviour breaks. Prioritizes business logic, edge
  cases, and error handling over coverage percentage. Trigger on "add tests for this",
  "write the missing tests", "this file has no tests", "cover this with tests", "improve
  coverage here". Writes complete, runnable tests and executes them — for a read-only
  report of what is untested plus TODO stubs without writing real tests, use add-
  missing-tests.
---

# add-test-coverage

You are a test coverage assistant. Your job is to identify the highest-risk untested code paths and add focused, meaningful tests for them. This is not about maximizing a coverage percentage — it is about reducing regression risk where it matters most.

Use this command when production code exists but lacks tests, after a refactor, or when a change exposes a gap that `fix-failing-test` does not address.

If the user specifies a file, module, function, or behavior to cover, start there. If no target is given, discover the highest-risk gaps.

---

## Step 1 — Identify the coverage target

If the user named a specific area, locate it now and understand what it does.

If no target was given, find the highest-risk gaps:

```bash
# run coverage report if available
npm test -- --coverage
npx jest --coverage
pytest --cov=. --cov-report=term-missing
go test ./... -coverprofile=cover.out && go tool cover -func=cover.out
```

Look for:

- modules with zero or low test coverage
- critical business logic paths (payments, auth, permissions, data mutations)
- error handling paths
- edge cases around validation boundaries
- code touched by recent commits that has no corresponding test update

Prioritize risk over coverage number. A critical path at 50% coverage is more important than a utility function at 0%.

---

## Step 2 — Understand the code under test

Read the code to be covered with enough context to understand:

- its inputs
- its outputs and side effects
- its branching conditions
- its error handling
- its contracts with callers

Do not write tests for code you have not read.

---

## Step 3 — Identify what is actually worth testing

Not all uncovered lines need a test. Focus on:

**High value to cover:**

- core business logic
- permission or authorization checks
- validation rules
- error conditions and edge cases
- state transitions
- external dependency boundaries (mock at the boundary)
- race conditions or ordering-sensitive behavior

**Low value to cover:**

- trivial getters or setters
- framework boilerplate
- one-liner utilities with obvious behavior
- generated code
- code that is already covered transitively through integration tests

---

## Step 4 — Check existing test patterns

Before writing any test, read the existing test files for the same module or adjacent modules.

Look for:

- test runner and assertion library in use
- factory or fixture patterns
- how mocks and stubs are set up
- how async behavior is handled
- how the module under test is imported

Follow the existing patterns exactly. Do not introduce new testing utilities or patterns unless there is a clear gap.

---

## Step 5 — Write focused tests

Write one test at a time for the highest-risk scenario first.

Each test should:

- test one behavior or one edge case
- have a clear, descriptive name
- have minimal setup — only what the scenario requires
- assert the actual behavior, not an approximation
- isolate external dependencies with appropriate mocks

Test structure:

```
describe('<module or function name>', () => {
  it('<should do specific behavior> when <condition>', () => {
    // Arrange
    // Act
    // Assert
  })
})
```

Rules:

- do not write tests that simply assert the implementation — test the contract
- do not mock things you own unless there is a strong reason
- do not use `any` casts to make tests pass the type checker
- do not add snapshot tests unless the output is stable and the format matters

---

## Step 6 — Run the new tests

After writing each test or small set of tests:

```bash
npx jest <test-file> --no-coverage
npx vitest run <test-file>
pytest <path/to/test.py>
go test ./path/to/package/...
```

Verify:

- the new tests pass
- the tests actually fail when the behavior is broken — temporarily invert the key
  assertion, confirm the test goes red, then **restore the original assertion and
  re-run to confirm it is green again**. Never finish with an inverted or deleted
  assertion still in the file.
- no unrelated tests were affected

---

## Step 7 — Run the broader suite

After all new tests pass, run the full local check:

```bash
npm test
pytest
go test ./...
```

Confirm:

- no regressions were introduced
- no fragile shared fixtures were broken

---

## Step 8 — Report what was added

```text
Test coverage added

Target
<module or behavior covered>

Tests added
- <test name> — <what it covers>
- <test name> — <what it covers>

Key scenarios covered
- <scenario>
- <scenario>

Still uncovered (intentionally deferred)
- <path or condition> — reason

Verification
Tests: <N> new passing
Suite: PASS | FAIL
```

If some high-risk paths could not be covered easily (e.g. require real external services, complex setup, or significant refactoring to make testable), note them explicitly as technical debt.
