---
name: test-writer
description: Generate or extend comprehensive test suites — unit, integration, E2E, and contract tests — for any language or framework. Use when the user asks to write tests, add coverage, test a specific function or module, set up a test framework, generate test cases from code, or validate behaviour with automated tests.
---

# Test Writing

Approach every test as a senior engineer who has been burned by tests that passed but shipped broken software. Tests are not a checkbox — they are executable specifications of what the code must do. A test suite that gives false confidence is worse than no tests at all.

Your job is not to maximize line coverage. Your job is to make it impossible for a regression to ship undetected.

---

## Test Writing Principles

- **Tests are specifications, not afterthoughts.** A test describes a contract: given this input, this system must produce this output. Write the contract clearly before implementing it.
- **Test behaviour, not implementation.** Tests that know how a function works internally are brittle. Tests that only know what a function does are durable. Never test private methods directly.
- **One concept per test.** A test that asserts three things is three tests. When it fails, you will not know which of the three broke.
- **The sad path deserves equal effort.** Most bugs live in error paths, edge cases, and boundary conditions — not in the happy path that the developer thought about when writing the code.
- **Tests must be independent.** No test should depend on the execution order of other tests, or on shared mutable state. Every test sets up its own data and tears it down.
- **Fast tests run. Slow tests get skipped.** Keep unit tests under 50ms each. Isolate anything slow (DB, network, filesystem) behind mocks or test containers.
- **A flaky test is a lie.** A test that sometimes passes and sometimes fails provides no signal. Fix or delete it — never commit a known-flaky test.

---

## Step 0: Before Writing Any Test

1. **Read the code under test** — understand the function's contract: what does it take, what does it return, what side effects does it have?
2. **Identify all exit paths** — draw a mental decision tree: every `if`, every `try/catch`, every early return is a branch that needs coverage
3. **Name the test cases first** — list every scenario you will test in plain English before writing a single line of test code
4. **Identify dependencies** — what does this code call externally (DB, API, filesystem, clock, random)? These must be controlled in tests
5. **Choose the right test type** — not everything needs a unit test; decide whether this is a unit, integration, E2E, or contract test before starting

---

## Test Types & When to Use Each

### Unit Tests
**What:** Test a single function or class in complete isolation. All dependencies mocked.
**When:** Business logic, utility functions, data transformations, validation, algorithms.
**Speed target:** < 50ms per test. Should run in seconds for the full suite.
**Rule:** If it touches the network, disk, or a real database, it is not a unit test.

### Integration Tests
**What:** Test multiple components working together. May use a real database (container) or real file system.
**When:** Repository layer, service layer wired to a real DB, message queue consumers, API handlers end-to-end.
**Speed target:** < 5 seconds per test. Run in CI, not on every file save.
**Rule:** Each test must clean up its own data. Never leave test state in the DB.

### End-to-End (E2E) Tests
**What:** Test the full system from the user's perspective — real browser, real HTTP, real database.
**When:** Critical user journeys (sign up, checkout, core workflow). Not for every feature.
**Tools:** Playwright (preferred), Cypress.
**Rule:** Keep the E2E suite small and focused on journeys that cannot be caught by integration tests.

### Contract Tests
**What:** Verify that a service's API matches the contract its consumers depend on.
**When:** Microservices, public APIs, SDK interfaces, any boundary where two teams own either side.
**Tools:** Pact (consumer-driven contract testing).
**Rule:** Contract tests live with the consumer. The provider runs them in CI before merging.

### Snapshot Tests
**What:** Capture rendered output and alert when it changes.
**When:** UI components, serialised data structures, generated files.
**Rule:** Snapshots must be reviewed on update — never auto-accept snapshot diffs without reading them.

---

## Test Structure (Arrange / Act / Assert)

Every test follows this structure, always:

```
describe('<ModuleName>', () => {
  describe('<methodName>', () => {

    it('<does something specific> when <condition>', () => {
      // ARRANGE — set up all inputs, mocks, and state
      const input = ...
      mockDependency.returns(...)

      // ACT — call the thing under test, once
      const result = functionUnderTest(input)

      // ASSERT — verify the outcome, one concept
      expect(result).toEqual(expectedOutput)
    })

  })
})
```

**Naming rules:**
- Test names must read as complete sentences: `it('returns null when user is not found')`
- Never name a test `it('works')` or `it('test 1')`
- The test name is the failure message — make it diagnostic

---

## Test Case Generation Checklist

For every function or method, generate tests covering:

**Happy Path**
- [ ] Valid input — expected output
- [ ] All optional parameters provided
- [ ] Minimum valid input (empty string, zero, single item)
- [ ] Maximum valid input (large string, max int, large array)

**Input Validation**
- [ ] Missing required input / null / undefined
- [ ] Wrong type (string where number expected, etc.)
- [ ] Empty string / empty array / empty object
- [ ] Negative numbers where positive expected
- [ ] Zero where non-zero expected
- [ ] Values at boundary (e.g., max length + 1)

**Error / Failure Paths**
- [ ] Dependency throws an error
- [ ] Dependency returns null / empty / unexpected shape
- [ ] Dependency times out
- [ ] Network unavailable
- [ ] Database constraint violation

**Business Logic Edge Cases**
- [ ] Exactly at boundary condition (off-by-one)
- [ ] Both sides of every boolean condition
- [ ] First and last item in a collection
- [ ] Duplicate values in a collection
- [ ] Concurrent/parallel execution (if applicable)

---

## Mocking Standards

**Mock at the boundary, not in the middle.**
- Mock external services (HTTP APIs, databases, queues, email providers) — not internal functions
- Mock the clock (`Date.now()`, `new Date()`) whenever time affects behaviour
- Mock randomness (`Math.random()`, `uuid()`) when IDs or tokens affect assertions
- Never mock the module you are testing

**Mock fidelity rules:**
- A mock must honour the same contract as the real dependency: same return shape, same error types
- A mock that returns `{}` when the real dependency returns `{ id: string, name: string }` will mask real bugs
- Use factory functions for mock data — never inline raw objects scattered across test files

**Framework-specific mocking:**
```typescript
// Jest / Vitest
jest.mock('./emailService')
vi.spyOn(userRepository, 'findById').mockResolvedValue(mockUser)

// Python (pytest)
@patch('app.services.email.send')
def test_sends_welcome_email(mock_send):
    ...

// Go
type MockRepo struct{ ... }
func (m *MockRepo) FindByID(id string) (*User, error) { ... }
```

---

## Test Data Management

**Use factories, never raw literals.**

```typescript
// Bad — brittle, hard to maintain, hides what matters
const user = { id: '123', name: 'John', email: 'john@example.com', role: 'admin', createdAt: new Date() }

// Good — factory with sensible defaults, override only what matters for this test
const user = createUser({ role: 'admin' })
```

**Factory rules:**
- Every domain entity has a factory function / builder
- Factories provide valid defaults for all required fields
- Tests override only the fields that matter for the scenario being tested
- Factory-generated IDs must be unique per test run (use a counter or UUID)

**Database fixtures:**
- Seed data is created in `beforeEach` / `setup`, destroyed in `afterEach` / `teardown`
- Never share mutable fixture state between tests
- Use transactions that rollback instead of manual cleanup where the DB supports it

---

## Coverage Standards

**Coverage is a floor, not a goal.**

| Layer | Minimum coverage |
|-------|-----------------|
| `services/` (business logic) | 80% line, 70% branch |
| `utils/` (pure functions) | 90% line |
| Auth / payments / security paths | 100% line, 100% branch |
| `api/` (route handlers) | 70% line (integration tests cover the rest) |
| `repositories/` (data access) | Covered by integration tests, not unit tests |

**Coverage does not mean correctness.** 100% line coverage with weak assertions is worthless. Always ask: does this test actually catch a regression if the implementation changes?

**Mutation testing** — the gold standard: tools like Stryker (JS/TS), mutmut (Python), or go-mutesting modify the source code and check if tests detect the change. If a mutant survives, the test suite has a blind spot.

---

## CI Integration

Every test suite must be runnable in CI with a single command:

```bash
# Examples by stack
bun test                    # Bun
npm test / yarn test        # Node
pytest                      # Python
go test ./...               # Go
./gradlew test              # Java/Kotlin
dotnet test                 # C#
cargo test                  # Rust
```

**CI pipeline rules:**
- Tests run on every PR before merge — no exceptions
- Failing tests block merge — no bypass without explicit approval
- Test results published as CI artifacts (JUnit XML, coverage HTML)
- Coverage gate enforced: PRs that drop coverage below the threshold are flagged
- Test run time tracked — alert when suite exceeds 10 minutes

---

## Framework Quick Reference

### TypeScript / JavaScript
```typescript
// Jest / Vitest structure
import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('UserService', () => {
  let userService: UserService
  let mockRepo: MockUserRepository

  beforeEach(() => {
    mockRepo = createMockUserRepository()
    userService = new UserService(mockRepo)
  })

  describe('findById', () => {
    it('returns the user when found', async () => {
      const expected = createUser({ id: '1' })
      mockRepo.findById.mockResolvedValue(expected)

      const result = await userService.findById('1')

      expect(result).toEqual(expected)
    })

    it('throws UserNotFoundError when user does not exist', async () => {
      mockRepo.findById.mockResolvedValue(null)

      await expect(userService.findById('99')).rejects.toThrow(UserNotFoundError)
    })
  })
})
```

### Python (pytest)
```python
import pytest
from unittest.mock import AsyncMock, patch
from app.services.user import UserService
from tests.factories import create_user

class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_repo = AsyncMock()
        self.service = UserService(repo=self.mock_repo)

    async def test_find_by_id_returns_user_when_found(self):
        expected = create_user(id="1")
        self.mock_repo.find_by_id.return_value = expected

        result = await self.service.find_by_id("1")

        assert result == expected

    async def test_find_by_id_raises_when_not_found(self):
        self.mock_repo.find_by_id.return_value = None

        with pytest.raises(UserNotFoundError):
            await self.service.find_by_id("99")
```

### Go
```go
func TestUserService_FindByID(t *testing.T) {
    t.Run("returns user when found", func(t *testing.T) {
        expected := fixtures.CreateUser(t, fixtures.WithID("1"))
        mockRepo := &MockUserRepo{FindByIDFunc: func(id string) (*User, error) {
            return expected, nil
        }}
        svc := NewUserService(mockRepo)

        result, err := svc.FindByID("1")

        require.NoError(t, err)
        assert.Equal(t, expected, result)
    })

    t.Run("returns error when user not found", func(t *testing.T) {
        mockRepo := &MockUserRepo{FindByIDFunc: func(id string) (*User, error) {
            return nil, ErrNotFound
        }}
        svc := NewUserService(mockRepo)

        _, err := svc.FindByID("99")

        assert.ErrorIs(t, err, ErrNotFound)
    })
}
```

---

## Definition of Done — Test Suite

A test suite is not done until:

- [ ] Every public function has at least one test
- [ ] Happy path covered for all functions
- [ ] All error / failure paths covered
- [ ] All boundary conditions covered
- [ ] No hardcoded test data — factories used throughout
- [ ] All external dependencies mocked in unit tests
- [ ] Integration tests clean up their own data
- [ ] Test names read as complete diagnostic sentences
- [ ] `npm test` / `pytest` / `go test ./...` passes with zero failures
- [ ] Coverage meets the layer-specific minimums
- [ ] No `it.only`, `fit`, `fdescribe`, `test.only`, `pytest.mark.only` left in committed code
- [ ] No skipped tests without a documented reason and tracking issue
- [ ] CI pipeline runs the full suite on every PR
