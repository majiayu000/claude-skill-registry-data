---
name: test-driven-development
description: Write code using the red-green-refactor TDD cycle with proper test design
triggers: [tdd, test first, write tests, red green refactor, test driven]
audience: engineer
---

# Test-Driven Development

## Context
TDD is a discipline where you write a failing test before writing the implementation. It produces better-designed, more modular code and a safety net for future changes. This skill guides the full red-green-refactor loop and applies to unit, integration, and contract testing.

Use this skill when:
- Starting any new feature or behavior
- Fixing a bug (write a failing test that proves the bug exists first)
- Designing an API or public interface

## Instructions

### The Loop
Follow this cycle strictly — do not skip steps:

1. **RED — Write a failing test.**
   - Write the simplest test that specifies one behavior.
   - The test must fail for the *right reason* (missing implementation, not an error).
   - Name the test to describe the behavior: `it("returns empty array when no results found")`.
   - Run the test. Confirm it is red.

2. **GREEN — Write the minimum code to make it pass.**
   - Write the simplest possible implementation — do not over-engineer.
   - Hardcoding a return value to pass a single test is valid at this stage.
   - Run the test. Confirm it is green.
   - Do not refactor yet.

3. **REFACTOR — Clean up without breaking the test.**
   - Now apply the refactoring skill to improve the design.
   - Tests must stay green throughout.
   - Only refactor what you just wrote.

4. **Repeat** for the next behavior.

### Test Design Guidelines
- **One assertion per test** (or one logical behavior). Tests that assert many things are hard to diagnose.
- **Arrange-Act-Assert (AAA):** Structure every test in three clearly separated sections.
- **Test behavior, not implementation.** Tests should not break when internal structure changes but behavior stays the same.
- **Use the Test Pyramid:** Prefer many fast unit tests, fewer integration tests, minimal end-to-end tests.
- **Avoid testing private methods** directly — if a private method needs its own test, it likely belongs in a new class.
- **Use test doubles wisely:** Mocks for collaborators you own; fakes for infrastructure (databases, HTTP); avoid mocking what you don't own.

### For Bug Fixes
1. Write a test that fails and demonstrates the bug.
2. Confirm the test is red.
3. Fix the bug.
4. Confirm the test is now green.
5. The test now lives in the suite as a regression guard.

## Principles
- Source: [Test Pyramid — Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- Source: [Mocks Aren't Stubs — Martin Fowler](https://martinfowler.com/articles/mocksArentStubs.html)
- Key idea: *"TDD doesn't drive good design — it drives testable design. Good design is still your responsibility."*

## Output Format
When applying this skill, the agent should:
- Write the failing test first (with the test name describing behavior)
- Show it failing with a clear reason
- Write the minimum implementation
- Show it passing
- Apply any refactoring and confirm still green
