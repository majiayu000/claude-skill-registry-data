---
name: tdd-master-workflow
description: Test-Driven Development workflow, red-green-refactor cycle, test organization, and advanced TDD patterns
---

# TDD Master Workflow Skill

This skill provides comprehensive TDD guidance.

## Red-Green-Refactor Cycle

1. Write a failing test (Red)
2. Make it pass with minimal code (Green)
3. Refactor while keeping tests passing
4. Repeat

## Test Organization

- Unit tests: fast, isolated, deterministic
- Integration tests: real dependencies, slower
- Contract tests: API boundaries
- E2E tests: critical user journeys

## Advanced Patterns

- Test doubles: mocks, stubs, fakes, spies
- Property-based testing
- Mutation testing
- Contract testing (Pact)
- Snapshot testing for UI

## Workflow Integration

- Pre-commit test runs
- CI pipeline stages
- Coverage thresholds
- Flaky test quarantine
