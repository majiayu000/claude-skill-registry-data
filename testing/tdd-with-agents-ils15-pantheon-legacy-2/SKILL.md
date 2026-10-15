---
name: tdd-with-agents
description: "TDD enforcement with RED→GREEN→REFACTOR cycle and advanced testing patterns. Use for test-driven development across all layers."
context: fork
globs: []
alwaysApply: false
---

# TDD with Agents

Enforce RED → GREEN → REFACTOR cycle across all implementation agents. Includes advanced testing patterns for E2E, load, mutation, and contract testing.

---

## Core Principle

> **Write the test FIRST. Watch it fail. Write minimal code to pass. Refactor with confidence.**

---

## TDD Cycle (RED → GREEN → REFACTOR)

### RED — Write Failing Test
- Write test for the behavior you want
- Run it → **must fail** (confirms test works)
- Test should be specific: one assertion per test

### GREEN — Make It Pass
- Write **minimal** code to pass the test
- No extra features, no premature optimization
- If it feels hard → design problem; refactor test

### REFACTOR — Improve Without Breaking
- Clean up code while tests stay green
- Extract functions, rename, remove duplication
- Tests are your safety net

---

## Testing by Layer

### Backend (Hermes)
```python
# Unit: service logic
def test_calculate_discount_applies_percentage():
    result = calculate_discount(100, 10)
    assert result == 90.0

# Integration: API endpoint
def test_get_user_returns_404_for_missing():
    response = client.get("/users/nonexistent")
    assert response.status_code == 404

# Database: repository
def test_user_repository_saves_and_retrieves():
    repo.save(User(id="1", name="Test"))
    assert repo.find("1").name == "Test"
```

### Frontend (Aphrodite)
```typescript
// Test behavior, not implementation
test('shows error message on invalid form', async () => {
  render(<LoginForm />)
  await userEvent.click(screen.getByText('Submit'))
  expect(screen.getByText('Email is required')).toBeInTheDocument()
})
```

### Database (Demeter)
```python
def test_migration_creates_users_table():
    alembic upgrade(head)
    assert inspector.has_table('users')

def test_migration_rollback_drops_table():
    alembic upgrade(head)
    alembic downgrade(-1)
    assert not inspector.has_table('users')
```

---

## Advanced Testing Patterns

### E2E Testing (Playwright)
```typescript
test('user can complete full signup flow', async ({ page }) => {
  await page.goto('/signup')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'secure123')
  await page.click('button[type="submit"]')
  await expect(page.locator('.welcome-banner')).toBeVisible()
})
```

### Load Testing (k6/Locust)
```javascript
// k6 script
export const options = { vus: 50, duration: '30s' }
export default function () {
  http.get('http://localhost:8000/api/users')
}
```

### Contract Testing (Pact)
```python
# Provider verifies consumer contract
@pact.verify_provider
def test_provider_satisfies_consumer_contract():
    # Verify all interactions from pact file
    pass
```

### Mutation Testing
- Mutate source code (change `>` to `<`, remove conditions)
- Run tests → should fail (mutation killed)
- If tests pass → test is weak; improve it

### Visual Regression
```typescript
test('homepage looks the same', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveScreenshot('homepage.png')
})
```

---

## Coverage Rules

- **Minimum: 80%** for all code
- **Critical paths: 100%** (auth, payments, data integrity)
- **No snapshot testing** — test behavior, not output shape
- **Test edge cases**: empty input, null, boundary values, errors

---

## Agent Responsibilities

| Agent | Tests |
|-------|-------|
| **Hermes** | Unit + integration for FastAPI endpoints, services, middleware |
| **Aphrodite** | Component behavior tests with React Testing Library |
| **Demeter** | Migration upgrade/downgrade, query correctness |
| **Themis** | Verifies coverage ≥80%, edge cases tested, error conditions |

---

## Workflow

```
1. Zeus/Athena defines feature with testable acceptance criteria
2. Hermes writes failing test (RED)
3. Hermes implements minimal code (GREEN)
4. Hermes refactors (REFACTOR)
5. Aphrodite writes frontend tests in parallel
6. Themis reviews: coverage, edge cases, correctness
7. If coverage <80% → NEEDS_REVISION
```

---

## Anti-Patterns

- ❌ Writing code before test
- ❌ Testing implementation details (private methods, internal state)
- ❌ Mocking everything (test real behavior where possible)
- ❌ Skipping RED step (test must fail first)
- ❌ Ignoring flaky tests (fix or delete)
