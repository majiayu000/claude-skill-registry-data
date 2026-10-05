---
name: testing-tdd
description: Writes tests following TDD Red-Green-Refactor cycle. Language-agnostic methodology with Arrange-Act-Assert structure. Use when implementing features test-first.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [feature-or-module-to-test]
  stability: development
  last-verified-cc-version: 1.0.34
---

# Test-Driven Development

**Target**: $ARGUMENTS

Writes **focused, behavior-driven tests** following the TDD Red-Green-Refactor cycle. Language-agnostic — works with any test framework (pytest, vitest, jest, cargo test, etc.).

## Quick Reference

- TDD cycle + anti-patterns: `references/tdd-best-practices.md`
- What to test/skip + mocking strategy: `references/testing-strategy.md`

## TDD Cycle

1. **RED** — Write a failing test that describes the expected behavior
2. **GREEN** — Write minimal code to make the test pass
3. **REFACTOR** — Improve code quality while tests stay green
4. Repeat

**Never skip RED.** Every feature starts with a failing test.

## Test Structure: Arrange-Act-Assert

Every test has three phases:

```text
ARRANGE — Set up test data and dependencies
ACT     — Execute the behavior under test
ASSERT  — Verify the outcome
```

## What to Test (KISS/DRY/YAGNI)

**High-Value** (test these):

- Business logic — algorithms, calculations, decision rules
- Integration points — API handling, external service interactions
- Edge cases — empty inputs, error propagation, boundary conditions
- Contracts — response formats, data transformations

**Avoid** (skip these):

- Library behavior — framework internals, third-party validation
- Trivial assertions — existence checks, type checks, default values
- Implementation details — internal state, private methods
- Styling/layout — CSS, class names

See `references/testing-strategy.md` → "Patterns to Remove" for full list.

## Decision Checklist

Before writing a test:

1. Does this test **behavior** (write it) or **implementation** (skip it)?
2. Would this catch a **real bug** (write it) or is it **trivial** (skip it)?
3. Is this testing **our code** (write it) or **a library** (skip it)?

## Mocking Strategy

- Mock external dependencies (APIs, network, filesystem)
- Mock non-deterministic values (time, random, UUIDs)
- Use real services when in-memory alternatives exist
- Constrain mocks to real interfaces (typed mocks, spec=)
- Never mock internal functions in the same module

## Quality Gates

- [ ] Every feature starts with a failing test (RED)
- [ ] Tests use Arrange-Act-Assert structure
- [ ] No tests for library internals or implementation details
- [ ] Mocks use spec/type constraints (no untyped mocks)
- [ ] Test names describe behavior, not methods
- [ ] All tests pass before committing
