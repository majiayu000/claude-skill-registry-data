---
name: tdd
description: Test-driven development. Use when the user explicitly wants test-first work, red-green-refactor, or asks to use TDD.
---

# Test Driven Development

TDD is a short red, green, refactor loop. Use it only when the request calls for test-first work.

## Choose the seam

Test behavior through the public interface where the outcome is observed. State the seam before writing the test. Ask Charlie only when seam placement changes architecture, product scope, or another choice that belongs to him. Otherwise choose the strongest existing seam and proceed.

Read [`tests.md`](tests.md) for examples and [`mocking.md`](mocking.md) when a collaborator may need substitution.

A useful test:

1. Describes behavior in domain language.
2. Can fail when that behavior is wrong.
3. Gets expected values from a source independent of the implementation.
4. Survives internal refactoring.
5. Uses the narrowest level that still exercises the real contract.

Mocks are useful at slow, nondeterministic, or external boundaries. Do not mock internal collaborators merely to make the test easy. Use as many assertions as one behavior needs, while keeping unrelated outcomes in separate tests.

## Run the loop

1. Write one test for one behavior.
2. Run it and confirm it fails for the expected reason.
3. Write the smallest complete implementation that makes it pass.
4. Run the focused test and the relevant surrounding checks.
5. Refactor while green when the current design has clear duplication or poor naming.
6. Repeat for the next behavior.

Do not write a whole imagined test suite before implementation. Work in vertical slices so each result can change the next test.

A red test caused by setup, syntax, or the wrong path proves nothing. Fix the test until it fails on the missing behavior. A green test that also passes against the unfixed behavior proves nothing either.

Finish with the behavior implemented, every changed test green, and the observed proof stated without claiming more than the checks establish.
