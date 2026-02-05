---
name: test-driven-workflow
description: "Use when implementing features or fixing bugs. Enforces Test-Driven Development (TDD) Red-Green-Refactor cycle. Supports Vitest, Jest, and similar frameworks."
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
version: 1.0.0
last_verified: "2026-01-01"
tags: ["testing", "tdd", "quality", "workflow"]
related-skills: ["api-endpoint-design", "pr-review-standards"]
---

# Skill: Test-Driven Workflow

## Purpose
Prevent "Groundhog Day" loops where the agent writes code that breaks existing functionality. Establish a disciplined TDD practice that ensures correctness before implementation.

## 1. Negative Knowledge (Anti-Patterns)

| Failure Pattern | Context | Why It Fails |
| :--- | :--- | :--- |
| Mocking too much | Mocked entire service layer | Tests pass but integration fails in production |
| Sleep/Wait in tests | Used `setTimeout` for async | Flaky tests on CI, slow test suite |
| Testing implementation details | Tested private methods | Brittle tests break on refactors |
| No test isolation | Shared state between tests | Tests pass/fail based on execution order |
| Generic test names | `test('it works')` | Can't identify what broke when test fails |
| Skipping edge cases | Only tested happy path | Production bugs from unexpected inputs |
| Writing tests after code | Wrote code first, tests later | Tests don't catch design flaws, low coverage |

## 2. Verified TDD Cycle

### The Red-Green-Refactor Loop

```
1. RED    → Write a failing test
2. GREEN  → Write minimal code to pass
3. REFACTOR → Improve code while keeping tests green
4. REPEAT
```

### Detailed Procedure

#### Phase 1: RED - Write Failing Test
```typescript
// tests/services/UserService.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { UserService } from '@/services/UserService';
import { MockUserRepository } from '@/tests/mocks/UserRepository';

describe('UserService.createUser', () => {
  let service: UserService;
  let mockRepo: MockUserRepository;

  beforeEach(() => {
    mockRepo = new MockUserRepository();
    service = new UserService(mockRepo);
  });

  it('should create a new user with valid input', async () => {
    const input = {
      email: 'test@example.com',
      name: 'Test User',
      role: 'user' as const
    };

    const result = await service.createUser(input);

    expect(result).toMatchObject({
      email: input.email,
      name: input.name,
      role: input.role
    });
    expect(result.id).toBeDefined();
  });

  it('should throw error if user already exists', async () => {
    mockRepo.setExistingUser({ email: 'test@example.com' });

    await expect(
      service.createUser({
        email: 'test@example.com',
        name: 'Test',
        role: 'user'
      })
    ).rejects.toThrow('User already exists');
  });
});
```

**Verify it fails:**
```bash
npm test -- UserService.test.ts
# Expected: FAIL - UserService not implemented yet
```

#### Phase 2: GREEN - Minimal Implementation
```typescript
// src/services/UserService.ts
export class UserService {
  constructor(private userRepo: UserRepository) {}

  async createUser(input: CreateUserInput): Promise<UserResponse> {
    const existing = await this.userRepo.findByEmail(input.email);
    if (existing) {
      throw new Error('User already exists');
    }

    const user = await this.userRepo.create(input);
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role,
      createdAt: user.createdAt
    };
  }
}
```

**Verify it passes:**
```bash
npm test -- UserService.test.ts
# Expected: PASS - All tests green
```

#### Phase 3: REFACTOR - Improve Code
- Extract validation to helper
- Improve error messages
- Add logging
- Optimize performance

**Re-run tests:**
```bash
npm test -- UserService.test.ts
# Expected: PASS - Tests still green after refactoring
```

## 3. Testing Strategy

### What to Test

#### Unit Tests (Fast, Isolated)
- ✅ Business logic in services
- ✅ Data transformation functions
- ✅ Validation logic
- ✅ Error handling
- ✅ Edge cases and boundary conditions

#### Integration Tests (Moderate Speed)
- ✅ API endpoints (request → response)
- ✅ Database interactions
- ✅ External service integrations
- ✅ Authentication flows

#### E2E Tests (Slow, Comprehensive)
- ✅ Critical user journeys
- ✅ Multi-step workflows
- ✅ System-wide features

### What NOT to Test

- ❌ Framework internals (Express, React, etc.)
- ❌ Third-party library behavior
- ❌ Getters/setters with no logic
- ❌ Constants and configuration
- ❌ Private implementation details

## 4. Test Quality Checklist

Before committing tests, verify:

- [ ] **Specific names**: Test names describe exact behavior
  - ✅ `should return 401 when token is expired`
  - ❌ `test auth`

- [ ] **Isolated**: Each test is independent, no shared state
  - ✅ Use `beforeEach` to reset state
  - ❌ Tests depend on execution order

- [ ] **Fast**: Unit tests run in milliseconds
  - ✅ Use mocks for I/O operations
  - ❌ Use real database/network in unit tests

- [ ] **Deterministic**: Tests always produce same result
  - ✅ Mock `Date.now()`, random functions
  - ❌ Use `setTimeout`, rely on timing

- [ ] **Minimal mocking**: Only mock external dependencies
  - ✅ Mock database, API clients
  - ❌ Mock internal services (use real ones)

- [ ] **Arrange-Act-Assert**: Clear test structure
  ```typescript
  it('should ...', () => {
    // Arrange - Set up test data
    const input = { ... };

    // Act - Execute the code under test
    const result = service.method(input);

    // Assert - Verify the result
    expect(result).toBe(expected);
  });
  ```

## 5. Failed Attempts (Negative Knowledge Evolution)

### ❌ Attempt: 100% code coverage goal
**Context:** Aimed for 100% line coverage
**Failure:** Wrote meaningless tests for trivial code, wasted time
**Learning:** Focus on critical paths and edge cases, not coverage metrics

### ❌ Attempt: Testing framework internals
**Context:** Wrote tests for React component rendering details
**Failure:** Tests broke on framework updates, high maintenance
**Learning:** Test behavior and public API, not implementation

### ❌ Attempt: Shared test fixtures
**Context:** Created shared test data to reduce duplication
**Failure:** Modifying fixtures broke unrelated tests
**Learning:** Each test should define its own data (factories are OK)

### ❌ Attempt: Real database for unit tests
**Context:** Used actual PostgreSQL for service tests
**Failure:** Tests slow (2s+ each), race conditions, cleanup issues
**Learning:** Use in-memory DB for integration tests, mocks for unit tests

## 6. Testing Tools & Best Practices

### Recommended Stack
- **Test Runner**: Vitest (fast, ESM-native) or Jest
- **Assertions**: Built-in expect
- **Mocking**: MSW for API mocking, built-in mocks for modules
- **Coverage**: c8 or Istanbul
- **E2E**: Playwright or Cypress

### Test Organization
```
tests/
├── unit/
│   ├── services/
│   ├── utils/
│   └── helpers/
├── integration/
│   ├── api/
│   └── database/
├── e2e/
│   └── journeys/
└── mocks/
    ├── repositories/
    └── services/
```

### Running Tests
```bash
# Run all tests
npm test

# Run specific test file
npm test -- UserService.test.ts

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run only unit tests
npm test -- tests/unit
```

## 7. TDD Workflow for Agents

When implementing a new feature:

1. **Start with test file**: Create `tests/unit/<module>.test.ts` BEFORE implementation
2. **Write failing test**: Describe expected behavior
3. **Run test**: Verify it fails (RED)
4. **Implement**: Write minimal code to pass
5. **Run test**: Verify it passes (GREEN)
6. **Refactor**: Improve code quality
7. **Run test**: Verify still passes
8. **Commit**: Save working state
9. **Repeat**: Next test case

### Example Session
```
Agent: "I'll implement user registration with TDD"

1. Create tests/unit/services/UserService.test.ts
2. Write test: "should create user with valid input"
3. Run: npm test -- UserService.test.ts
   Output: FAIL - UserService not defined
4. Create src/services/UserService.ts with minimal implementation
5. Run: npm test -- UserService.test.ts
   Output: PASS
6. Write test: "should reject duplicate email"
7. Run: FAIL - no duplicate check
8. Add duplicate check logic
9. Run: PASS
10. Commit: "feat: add user registration with duplicate email check"
```

## 8. Governance
- **Token Budget:** ~450 lines (within 500 limit)
- **Dependencies**: Vitest/Jest, testing framework of project
- **Pattern Origin**: Test-Driven Development (Kent Beck)
- **Maintenance**: Update as testing practices evolve
- **Verification Date**: 2026-01-01
