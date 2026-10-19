---
name: test-writer
description: Use when asked to write tests, add unit or integration tests, increase test coverage, test existing untested code, or cover a bug fix with a regression test — Jest, Vitest, pytest, JUnit, Go test, Playwright and others.
---

# Test Writer

## Overview

Write tests that would fail if the behavior broke. Match the project's existing test framework and style, test behavior through public interfaces, and run every test you write.

## Method

1. **Learn the project's testing setup:** framework and runner (from config and `package.json`/`pyproject.toml`/`pom.xml`), where tests live, naming, helpers, fixtures, factories. Read two existing tests and copy their style. If there are no tests, pick the standard for the stack and say so.
2. **Decide what to test** for the target code:
   - Main success path.
   - Each branch and error path.
   - Boundaries: empty, zero, one, many, max, null/undefined, invalid types, unicode, time zones.
   - Contracts other code depends on (return shape, thrown errors, emitted events).
3. **Choose the level:** unit for pure logic, integration where the risk is in wiring (database, HTTP, queues), end-to-end only for critical user journeys.
4. **Write each test** as Arrange / Act / Assert with one behavior per test and a name that states it: `returns 0 when the cart is empty`.
5. **Run them.** Every new test must pass. Then break the code under test on purpose (or check the assertion against a wrong value) to confirm the test can fail. Revert.
6. **Report** what is covered and what is not.

## Rules

| Rule | Why |
|---|---|
| Assert on outputs and observable effects, not private internals | Tests survive refactoring |
| Mock only what you do not own or what is slow or non-deterministic (network, clock, randomness) | Over-mocking tests the mocks |
| Prefer real collaborators and in-memory or containerized databases for integration tests | Catches wiring bugs |
| Make tests deterministic: fixed clock, seeded randomness, no order dependence | Flaky tests get ignored |
| Specific assertions (`toEqual({ total: 1250 })`), not `toBeTruthy()` | Weak assertions pass on wrong results |
| A bug fix gets a regression test that fails without the fix | The bug stays fixed |

## Output

The test files, then:

```
Added: <N> tests in <files>
Covers: <behaviors and edge cases>
Not covered: <what and why>
Run: <command> → <N passed>
```

## Common mistakes

- Tests that mirror the implementation line by line and break on every refactor.
- Snapshot tests of large objects that nobody reads.
- Asserting that a mock was called instead of checking the result.
- Writing tests and not running them.
- Testing framework code or trivial getters instead of the logic that can break.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
