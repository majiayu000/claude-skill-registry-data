---
name: tdd
description: Apply when adding new behavior or fixing a bug. Red-green-refactor cycle, test-first discipline, when TDD doesn't pay.
license: MIT
version: 1.0.0
tokens_target: 1800
triggers:
  - test-driven development
  - red green refactor
  - test first
loads_after:
  - code-quality
supersedes: []
---

# Sub-Skill: Test-Driven Development

**Purpose:** Prevents the common failure mode where agents write implementation first and tests second — producing tests that validate the code as-written rather than the intended behavior.

## Rules

### The Red-Green-Refactor Cycle

1. **MUST: Always write a failing test before writing production code.** The test defines the desired behavior. If you cannot articulate a failing test, you do not yet understand the requirement. Reference: ERR-2026-017.

2. **MUST: Never write more production code than necessary to pass the current failing test.** Resist the urge to implement the full feature. One test, one behavior, one pass. Then refactor.

3. **SHOULD: After each green test, look for refactoring opportunities before writing the next test.** Refactoring under green tests is safe. Refactoring without tests is gambling.

4. **AVOID: Writing multiple tests at once before making any pass.** One failing test at a time keeps feedback loops tight and prevents losing track of which behavior you are implementing.

### Test Design

5. **SHOULD: Name tests to describe the scenario and expected outcome, not the function under test.** `test_empty_cart_returns_zero_total` not `test_calculate_total`. The name is documentation.

6. **MUST: Ensure each test is independent and can run in any order.** Shared mutable state between tests causes flaky suites. Use setup/teardown or fresh fixtures per test.

7. **SHOULD: Test behavior, not implementation.** Assert on outputs and observable side effects, not internal method calls. Implementation-coupled tests break on every refactor.

8. **AVOID: Testing private methods directly.** Test through the public API. If a private method needs its own tests, it probably belongs in a separate module.

### Coverage and Boundaries

9. **SHOULD: Cover the happy path, at least one edge case, and at least one error case per public function.** Three tests minimum per meaningful behavior.

10. **AVOID: Chasing 100% line coverage as a goal.** Coverage measures execution, not correctness. A test that executes code without asserting anything is worthless. Aim for high branch coverage on business logic.

11. **SHOULD: Use test doubles (mocks, stubs, fakes) only at architectural boundaries.** Mock the database, the network, the file system — not your own classes. Over-mocking makes tests brittle and meaningless.

### When NOT to TDD

12. **AVOID: TDD for exploratory prototypes and throwaway spikes.** When you do not yet know what the interface should be, experimentation is more valuable than premature tests. Delete the spike afterward.

13. **SHOULD: Use TDD for bug fixes — always.** Write a test that reproduces the bug first. Green means the bug is fixed. This prevents regressions permanently.

14. **AVOID: TDD for pure configuration, static markup, or generated code.** If there is no branching logic, there is nothing meaningful to test-drive.

### Discipline

15. **MUST: Never commit code where all tests pass but you skipped the red step.** If you wrote production code first and tests second, those tests may not actually exercise the new behavior. Rewrite them.

## See also

- `skills/code-quality/SKILL.md` — General quality rules including testing conventions
- `skills/python/SKILL.md` — Python-specific pytest patterns (rules 16–23)

## Why This Sub-Skill Earns Stars

LLM agents almost universally write code first and tests second — or skip tests entirely. This produces tests that validate the implementation rather than the specification, meaning bugs in the implementation are "verified" by the test. The red-green-refactor discipline catches this: if you never saw the test fail, you cannot trust that it tests anything real.
