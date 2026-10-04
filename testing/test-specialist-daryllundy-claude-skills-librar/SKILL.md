---
name: test-specialist
description: Test suite writing, coverage improvement, and testing strategy for unit,
  integration, and end-to-end tests. Use when asked to write unit tests, add integration
  tests, set up end-to-end testing (Playwright, Cypress), improve test coverage, implement
  TDD for a new feature, mock external dependencies, or fix flaky tests.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: quality
  tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e
  - tdd
  - coverage
  - playwright
  - jest
  - pytest
---

# Test Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write tests`, `unit test`, `integration test`.
- The requested work fits this skill's lane: Unit tests, integration tests, E2E tests, TDD, fixing flaky tests, coverage improvement.
- The request needs this domain's specific workflow, checks, or deliverable shape rather than a neighboring specialist.

## First actions
1. `Glob('**/*.test.*', '**/*.spec.*', '**/tests/**', '**/jest.config.*', '**/pytest.ini', '**/playwright.config.*')` — identify test framework and find existing tests
2. `Read` a few existing test files to understand patterns, naming conventions, and helper utilities
3. Identify: test framework, coverage tool, CI integration for tests

## Decision rules
- Test the behavior, not the implementation — tests should not break when internal implementation changes but external behavior doesn't
- For mocking: mock at the boundary (HTTP layer, database layer) not deep inside the implementation
- For flaky tests: identify root cause (timing, shared state, external dependency) before fixing

## Output contract
- Tests follow existing naming conventions (`describe` / `it` or class-based)
- Each test: one assertion concept per test; clear failure messages
- For new test files: include a brief comment explaining what the test suite covers

## Constraints
- NEVER write tests that depend on execution order
- NEVER mock the thing being tested

## Reference
- `references/legacy-agent.md`: testing patterns by language/framework, mocking strategies, coverage analysis, TDD workflow, E2E test patterns
