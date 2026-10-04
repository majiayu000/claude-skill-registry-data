---
name: testing-quality-engineering
description: Patterns for unit, integration, and E2E testing across modern stacks. Covers TDD workflow, mocking strategies, test architecture, and coverage analysis. Use when writing tests, setting up test infrastructure, or auditing test coverage.
version: "1.0.0"
verified_date: 2026-04-30
category: core
---

# Testing & Quality Engineering

## Purpose
Provide deterministic, production-grade testing patterns that transform the AUDIT phase from a manual review into an automated verification gate. This skill ensures every non-trivial feature has measurable correctness guarantees before shipping.

## When to Use This Skill
Use when:
- Writing unit, integration, or end-to-end tests for any feature
- Setting up test infrastructure (Vitest, Jest, Playwright, Pytest)
- Debugging flaky or failing test suites
- Auditing test coverage gaps on an existing codebase
- Implementing TDD workflows on a new feature

Do NOT use when:
- The task is a trivial one-liner with no branching logic (Fast Path)
- The task is pure UI polish with no behavioral change

## Phase 1: Test Strategy Selection

Choose the correct testing layer before writing any test code:

| Layer | Tool (JS/TS) | Tool (Python) | Use When |
|-------|-------------|---------------|----------|
| Unit | Vitest / Jest | Pytest | Pure functions, utilities, transformers, validators |
| Integration | Vitest + Supertest | Pytest + httpx | API routes, service interactions, DB queries |
| E2E | Playwright | Playwright / Selenium | Full user flows, critical paths, auth flows |
| Component | React Testing Library | — | UI component behavior (not visual styling) |

**Rule**: Start with the narrowest layer that proves correctness. Do not write E2E tests for logic that a unit test covers.

## Phase 2: Test Architecture

### File Organization
```
src/
  utils/
    formatPrice.ts
    formatPrice.test.ts          ← co-located unit test
  services/
    orderService.ts
    orderService.test.ts         ← co-located integration test
tests/
  e2e/
    checkout.spec.ts             ← E2E tests in dedicated directory
  fixtures/
    mockOrder.ts                 ← shared test fixtures
  helpers/
    setupTestDb.ts               ← test infrastructure helpers
```

### Naming Conventions
- Test files: `<module>.test.ts` (unit/integration) or `<flow>.spec.ts` (E2E)
- Test descriptions: `describe('<Unit>')` → `it('should <expected behavior> when <condition>')`
- No vague names: ❌ `it('works')` → ✅ `it('should return 0 when cart is empty')`

### Test Structure (AAA Pattern)
Every test follows Arrange → Act → Assert:
```typescript
it('should calculate total with tax', () => {
  // Arrange
  const items = [{ price: 100, qty: 2 }];
  const taxRate = 0.1;

  // Act
  const total = calculateTotal(items, taxRate);

  // Assert
  expect(total).toBe(220);
});
```

## Phase 3: Mocking Strategy

### When to Mock
- External APIs and network calls — **always mock**
- Database in unit tests — **mock the repository layer**
- Database in integration tests — **use a test database or in-memory DB**
- Time/dates — **mock `Date.now()` or use `vi.useFakeTimers()`**
- File system — **mock `fs` or use a temp directory**

### When NOT to Mock
- Pure utility functions — test them directly
- The module under test — never mock what you are testing
- Simple data transformations — use real inputs

### Mock Hierarchy
1. **Dependency injection** (preferred) — pass dependencies as arguments
2. **Module mocking** (`vi.mock()` / `jest.mock()`) — when DI isn't available
3. **Spy/stub** (`vi.spyOn()`) — when you need to observe calls without replacing
4. **Manual mocks** (`__mocks__/`) — for complex third-party libraries

### Anti-Pattern: Over-Mocking
If a test mocks more than 3 dependencies, the code under test likely has too many responsibilities. Refactor the code, not the test.

## Phase 4: Coverage & Quality Gates

### Coverage Targets
| Metric | Minimum | Ideal |
|--------|---------|-------|
| Line coverage | 70% | 85%+ |
| Branch coverage | 60% | 80%+ |
| Critical paths | 100% | 100% |

### What to Cover (Priority Order)
1. Business logic and domain rules
2. Input validation and edge cases
3. Error handling and failure modes
4. API contract conformance
5. Auth/permission boundaries

### What NOT to Cover
- Auto-generated code (Prisma client, GraphQL codegen)
- Framework boilerplate (Next.js config, Vite config)
- Pure type definitions
- Third-party library internals

## Phase 5: TDD Workflow

When the user requests TDD or the feature has complex branching logic:

1. **Red**: Write a failing test that describes the expected behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Clean up implementation without changing behavior
4. **Repeat**: Next test case

**TDD is not mandatory for all tasks.** Use it when:
- The feature has complex conditional logic
- The API contract is well-defined but the implementation is unclear
- Debugging a regression (write the failing test first, then fix)

## Output Format / Delivery
- Test files co-located with source or in `tests/` directory
- Coverage report summary if coverage tooling is configured
- Clear pass/fail status of the test suite

## Behavior Rules
1. **Tests must be deterministic.** No random data, no reliance on execution order, no network calls.
2. **Tests must be fast.** Unit tests < 5s total. Integration tests < 30s. E2E tests < 2min.
3. **Tests must be independent.** Each test sets up and tears down its own state.
4. **No testing implementation details.** Test behavior, not internal method calls or state shape.
5. **Failing tests are bugs.** A red test suite is never acceptable in a delivered branch.

## Safety Guardrails
1. **Snapshot Overuse Patch**: Do not use snapshot tests for dynamic content, API responses, or anything with timestamps/IDs. Snapshots are for stable UI component structure only.
2. **Flaky Test Patch**: If a test fails intermittently, it must be quarantined immediately and fixed — not retried or ignored.
3. **Test-in-Production Patch**: Never use production databases, APIs, or credentials in test runs. All external services must be mocked or use dedicated test instances.
4. **Coverage Theater Patch**: Do not write trivial tests (testing that `1 + 1 === 2`) to inflate coverage numbers. Every test must assert meaningful behavior.

## Maintenance Notes
- Created 2026-04-30 as part of the Engineering Rigor gap analysis.
- Complements `backend-dev-guidelines` (which says "write tests" but doesn't define how).
- Complements `spec-driven-build` (which defines what to build but not how to verify it).
