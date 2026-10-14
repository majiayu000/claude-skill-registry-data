---
name: test-driven-development
description: Enforces RED-GREEN-REFACTOR cycle — write a failing test first, write minimal code to pass, then refactor. Use when implementing new features, fixing bugs, or adding regression coverage. Prevents untestable code and false confidence from untested changes.
---

# Test-Driven Development

## Problem it solves

Code without tests creates a false sense of progress. Changes are declared correct because "they look right" rather than because a test proves they work. This causes:
- Regression bugs from untested changes
- Untestable code (tight coupling, hidden dependencies, side effects)
- False confidence — "tests pass" when tests don't actually cover the change
- No safety net for future refactoring
- Time lost manually verifying what a test could verify automatically

## Protocol

### 1. RED — Write a failing test first

Before writing any implementation code, write a test that defines the desired behavior:

- Write one test at a time — the smallest test that expresses the next requirement
- The test should fail for the right reason (the feature doesn't exist yet, not because of a bug in the test itself)
- Run the test and confirm it fails before writing implementation code
- Test naming: `test_<feature>_<scenario>` or `it_<should_do_what>`

Example cycle:
```python
# 1. Write the test
def test_add_returns_sum():
    result = add(2, 3)
    assert result == 5
# 2. Run it — fails because `add` doesn't exist yet (RED)
```

### 2. GREEN — Write minimal code to pass

Write the simplest possible implementation to make the test pass:

- Do not add features beyond what the test requires
- Do not refactor yet
- Duplication is acceptable at this stage
- The goal is a passing test, not perfect code

```python
# 3. Minimal implementation
def add(a, b):
    return a + b
# 4. Run it — passes (GREEN)
```

### 3. REFACTOR — Clean up while keeping tests green

With the safety net of passing tests, refactor the code:

- Remove duplication
- Improve naming
- Extract helper functions
- Optimize if needed, but only if tests still pass
- Run tests after each refactoring step to confirm nothing broke

### 4. Repeat

Add the next test, watch it fail (RED), implement (GREEN), refactor. Each cycle should be 1-5 minutes.

### 5. Test coverage expectations

- Cover happy path, edge cases, and error paths
- Test public API, not private implementation details
- One assertion per test (or a small number of related assertions)
- Tests should be independent and idempotent
- Use the project's existing test framework and conventions

### 6. Bug fixes follow TDD too

When fixing a bug:
1. Write a test that reproduces the bug — it fails (RED)
2. Fix the code — the test passes (GREEN)
3. Refactor if needed — tests still pass
This guarantees the bug is fixed and won't regress.

## Detection triggers

Activate when:
- Implementing a new function, class, or module
- Fixing a bug
- Adding a feature to existing code
- User says "write tests" or "add coverage"
- The project has a test framework configured
- Starting any implementation that could reasonably be tested

## When NOT to use

- Prototyping or exploration (write the spike, then TDD the real version)
- UI/visual changes where tests aren't practical (use snapshot or visual testing instead)
- Configuration changes
- The project has no test framework and adding one isn't in scope
- User explicitly says "no tests needed"

## Cross-references

- **spec-driven-development** — The spec defines what the tests should cover. Write the spec first, then TDD against it.

- **anti-premature-termination** — Passing tests are a completion criterion. Do not declare done until tests pass.

- **follow-existing-patterns** — Tests must match the project's existing test framework, naming conventions, and file layout.

- **code-review** — Review should check that tests exist and follow TDD principles.
