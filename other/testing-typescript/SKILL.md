---
name: testing-typescript
description: Writes tests following TDD (using vitest and @testing-library/react) best practices. Use when writing unit tests, integration tests, or component tests in TypeScript.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [test-scope or component-name]
  stability: stable
  content-hash: sha256:9d120f8a107caa25d18f6a308f85fb8ddaf7d09c4b57c3b62d2c414fba14c6cf
---

# TypeScript Testing

**Target**: $ARGUMENTS

Writes **focused, behavior-driven tests** following project testing strategy.

## Quick Reference

**TDD methodology** (language-agnostic): See `tdd-core` plugin (`testing-tdd` skill)

**TypeScript-specific documentation**: `references/`

- `references/testing-strategy-ts.md` — TypeScript tools (vitest, @testing-library/react, MSW)
- `references/tdd-best-practices-ts.md` — TypeScript TDD examples (extends tdd-core)

## Quick Decision

**vitest (default)**: Use `it`/`test` for known cases, `vi.mock` for module mocking. Works at unit/integration levels.

**@testing-library/react (components)**: Use for React component behavior testing with render, screen, userEvent.

See `references/testing-strategy-ts.md` for full methodology comparison.

## TDD Essentials (Quick Reference)

**Cycle**: RED (failing test / type error) -> GREEN (minimal pass) -> REFACTOR (clean up)

**Structure**: Arrange-Act-Assert (AAA)

```typescript
it('calculates order total from item prices', () => {
  // ARRANGE
  const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
  const calculator = new OrderCalculator();

  // ACT
  const total = calculator.total(items);

  // ASSERT
  expect(total).toBe(25);
});
```

## Component Testing Priorities

| Priority | Area | Example |
| -------- | ---- | ------- |
| CRITICAL | User interactions | Button click triggers handler |
| CRITICAL | Conditional rendering | Error state shows message |
| HIGH | Form validation | Invalid input shows error |
| HIGH | Async data loading | Loading -> success/error states |

## What to Test (KISS/DRY/YAGNI)

**High-Value**: Business logic, error paths, component behavior, async flows, custom hooks

**Avoid**: Type system behavior, library internals, CSS styling, implementation details

See `references/testing-strategy-ts.md` -> "Patterns to Remove" for full list.

## Naming Convention

**Format**: `{module} > {component} > {behavior}`

```typescript
describe('UserService', () => {
  it('creates a new user with valid data', () => { ... });
  it('rejects duplicate email addresses', () => { ... });
});
```

## Execution

```bash
npx vitest                          # Watch mode (default)
npx vitest run                      # Single run
npx vitest run src/utils            # Filter by path
npx vitest run --reporter=verbose   # Verbose output
npx vitest --ui                     # Browser UI
```

## Quality Gates

- [ ] All tests pass (`npx vitest run`)
- [ ] TDD Red-Green-Refactor followed
- [ ] Arrange-Act-Assert structure used
- [ ] Naming convention followed
- [ ] Behavior-focused (not implementation)
- [ ] No library/framework behavior tested
- [ ] Mocks use `vi.mock()` with proper restore (`vi.restoreAllMocks()`)
