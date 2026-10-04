---
name: testing
description: Design and write automated tests (unit, integration, end-to-end) using TDD where appropriate.
category: development
aliases:
- tdd
- unit-test
- integration-test
- write-tests
- test-coverage
triggers:
- write tests for this
- add tests
- how do I test this
- TDD
- test coverage
- unit test this
keywords:
- test
- tdd
- unit
- integration
- coverage
- assert
- fixture
- mock
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- development
- integration
- tdd
- test
- testing
- unit
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: write
credential_access: false
destructive_operations: false
---

# Testing

## Purpose

Design and write automated tests that catch real bugs and document intended behavior. Choose
the right level of test for each concern.

## When to Use

- Adding new code (write tests first or alongside)
- Reproducing a bug (write a failing test, then fix)
- Refactoring (tests pin current behavior)
- User asks how to test something

## When NOT to Use

- The user is prototyping and explicitly opts out
- The code has no interfaces to test (rare)

## Capabilities

- Unit tests for pure logic
- Integration tests for module boundaries
- End-to-end tests for user flows
- Property-based / fuzz testing
- Mocking and fixtures
- Test pyramid thinking

## Inputs

- The code to test
- Framework / language
- What matters to verify

## Workflow

1. **Identify the assertion.** What property must hold?
2. **Pick the test level.** Pure unit if possible; integration where module interaction matters.
3. **Write the test first when design is unclear (TDD).** Otherwise, write tests alongside.
4. **Make tests deterministic.** No time, randomness, or network dependence unless explicitly handled.
5. **Name tests by behavior.** `test_<thing>_<expected>_<when>`.
6. **Run tests, then refactor.** Red → green → refactor.

## Tools

- Test framework (pytest, Jest, etc.)
- Coverage tool
- Property-based library (optional)

## Examples

**User:** "Add tests for this function."
**Response:** "What's the contract? I'll write tests for the happy path, one boundary case, and one error case. Then we run them."

## Safety

- Don't test trivial getters
- Don't mock what you don't own — wrap it

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `coding` (always)
- `refactoring` (the safety net)
- `tdd` (a discipline)
- `debugging` (regression tests)