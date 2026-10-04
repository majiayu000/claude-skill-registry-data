---
name: testing
description: Testing strategies and best practices — TDD workflow, test pyramid, unit/integration/e2e patterns, and writing maintainable tests across languages.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# testing

Testing strategies and best practices — TDD workflow, test pyramid, unit/integration/e2e patterns, and writing maintainable tests across languages.

## Instructions

Apply these testing practices when writing or reviewing tests:

## Guidelines

### Type Safety in Tests

- Test helpers, factories, and fixtures must be fully typed — no `any` in test setup
- Use typed mocks: prefer `jest.mocked<T>()` / `vi.mocked<T>()` over casting to `any`
- Assert on precise types where possible to catch type regressions alongside logic regressions

### Test Quality Rules

- **One logical behaviour per test** — tests that assert multiple unrelated things are hard to diagnose when they fail
- **No magic values in assertions** — extract expected values into named constants with explanatory names
- **Tests are first-class code**: apply the same quality rules (naming, size limits, DRY) to test files as to production code
- **Deterministic only**: no `Date.now()`, `Math.random()`, network calls, or filesystem side-effects in unit tests — mock or inject them

### Coverage Requirements

| Layer | Minimum coverage |
|-------|-----------------|
| Business logic (services) | ≥ 80% |
| Utility functions | ≥ 90% |
| Controllers / route handlers | ≥ 70% |
| Generated / boilerplate code | exempt |

### CI Requirements

- Tests **must** run in CI on every push and pull request
- Failing tests **must** block merge — no bypassing the test gate
- Unit + integration test suite must complete in < 5 minutes; E2E runs in a separate, optional stage

---

### The Test Pyramid

Follow the classic test pyramid for a balanced, fast, and reliable test suite:

```
        /\
       /e2e\       ← few, slow, high confidence
      /------\
     /integr-\     ← moderate, medium speed
    /----------\
   /  unit tests \ ← many, fast, isolated
  /______________\
```

- **Unit tests** (70%): test a single function/class in isolation; mock all dependencies
- **Integration tests** (20%): test interactions between components (DB, services, APIs)
- **E2E tests** (10%): test full user flows through the real system; use sparingly

### TDD Workflow (Red–Green–Refactor)

1. **Red** – write a failing test that describes the desired behaviour
2. **Green** – write the minimal code to make the test pass
3. **Refactor** – clean up the code without breaking the tests

### Writing Good Tests

**Structure with AAA (Arrange–Act–Assert):**
```js
it('should return the total price including tax', () => {
  // Arrange
  const cart = new Cart([{ price: 100 }, { price: 50 }]);
  const taxRate = 0.2;

  // Act
  const total = cart.totalWithTax(taxRate);

  // Assert
  expect(total).toBe(180);
});
```

**Test naming conventions:**
```
should <do something> when <condition>
given <context>, when <action>, then <outcome>
```

**Principles:**
- **One assertion per test** (or one logical concept)
- **Deterministic** — no reliance on system time, random numbers, or external services
- **Isolated** — tests must not depend on execution order
- **Fast** — unit tests should complete in milliseconds
- **Readable** — test code is documentation; prioritise clarity

### Mocking & Stubbing

- Mock at the boundary: mock external services, databases, and APIs — not internal functions
- Prefer dependency injection over module mocking where possible
- Verify mock calls only when the interaction itself is the behaviour under test

```js
// Prefer: inject a mock via constructor/parameter
const service = new OrderService({ emailClient: mockEmailClient });

// Avoid: mock an internal module unless necessary
jest.mock('../internal/utils');
```

### Coverage Guidelines

- Aim for **≥ 80%** line/branch coverage on business logic
- Do NOT write tests just to hit a coverage number — meaningless tests are worse than no tests
- Use coverage reports to find **untested edge cases**, not as a target metric
- Exclude generated code, config files, and boilerplate from coverage reports

### Integration Testing Patterns

- Use **testcontainers** to spin up real DB/Redis/etc. in CI
- Use **database transactions** that roll back after each test for isolation
- Use contract testing (e.g., Pact) for service-to-service boundaries

### E2E Testing Guidelines

- Write E2E tests for the most critical user journeys only
- Use stable selectors (`data-testid`) over CSS classes or text
- Keep E2E tests independent and idempotent (seed + clean up their own data)

## Examples

**Node.js (Vitest/Jest):**
```js
describe('calculateDiscount', () => {
  it('should apply 10% discount for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(135);
  });

  it('should return full price for orders under $100', () => {
    expect(calculateDiscount(80)).toBe(80);
  });

  it('should throw for negative amounts', () => {
    expect(() => calculateDiscount(-10)).toThrow('Amount must be positive');
  });
});
```

**Python (pytest):**
```python
def test_discount_applied_for_large_orders():
    assert calculate_discount(150) == 135

def test_no_discount_for_small_orders():
    assert calculate_discount(80) == 80

def test_raises_for_negative_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        calculate_discount(-10)
```

## References

- [The Practical Test Pyramid (Ham Vocke)](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Testing Library](https://testing-library.com/)
- [Testcontainers](https://testcontainers.com/)
- [Vitest](https://vitest.dev/)
- [pytest](https://docs.pytest.org/)
