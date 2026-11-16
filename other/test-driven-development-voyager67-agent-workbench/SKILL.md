---
name: test-driven-development
description: Implement a behavior change with a test-first loop when the contract can be tested. Use for bug fixes and regressions; adapt when the project cannot support a true red-green cycle.
---

# Test-Driven Development

Use the project's existing test framework and conventions.

1. Inspect the implementation, nearby tests, fixtures, and documented commands.
2. Define the observable contract and the edge cases that matter.
3. Add the smallest focused test that demonstrates the missing or incorrect behavior.
4. Run it and confirm it fails for the intended reason.
5. Implement the minimum change that makes the test pass.
6. Run the focused test, then the relevant suite and additional checks justified by the change.
7. Refactor only when clarity improves without changing behavior; rerun affected tests.

Prefer deterministic tests that exercise public behavior. Avoid broad mocks, brittle snapshots, arbitrary sleeps, or tests that pass without reaching the changed path. For exploratory work or an untestable UI path, state why strict TDD is impractical and use the strongest available verification. Never claim a red-green cycle happened unless you observed it.
