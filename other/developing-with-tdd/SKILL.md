---
name: developing-with-tdd
description: Test-Driven Development for backend code. Red-Green-Refactor cycle with practical patterns.
type: workflow
tier: library
domains: [backend, testing]
trigger: "tdd, test-driven, red-green-refactor, write test first, failing test"
---

## TDD Cycle

**Red → Green → Refactor**

1. **Red:** Write a failing test that describes desired behavior
2. **Green:** Write the minimum code to make it pass (no gold-plating)
3. **Refactor:** Improve the code without changing behavior (tests stay green)

Never skip to Green without a failing Red test first.

## Practical Rules

**Rule 1: One test at a time**
Write one failing test. Make it pass. Only then write the next test.

**Rule 2: Minimum viable production code**
In Green phase, write only what's needed to pass the test. No future-proofing.

**Rule 3: Test behavior, not implementation**
Bad: `expect(user._hash).toBeDefined()`
Good: `expect(await user.verifyPassword('secret')).toBe(true)`

**Rule 4: Fast tests**
Unit tests must run in <100ms. Use mocks for I/O (database, network, filesystem).

## Structure

```
src/
  auth/
    auth.service.ts         ← Implementation
    auth.service.test.ts    ← Tests (co-located)
```

## Test Template (TypeScript/Vitest)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    service = new AuthService({ /* mock deps */ });
  });

  describe('login()', () => {
    it('returns a JWT token for valid credentials', async () => {
      // Arrange
      const credentials = { email: 'user@test.com', password: 'correct' };
      // Act
      const result = await service.login(credentials);
      // Assert
      expect(result.token).toMatch(/^eyJ/);
    });

    it('throws for invalid password', async () => {
      await expect(service.login({ email: 'user@test.com', password: 'wrong' }))
        .rejects.toThrow('Invalid credentials');
    });
  });
});
```

## Mocking External Dependencies

```typescript
// Mock the database
const mockUserRepo = {
  findByEmail: vi.fn().mockResolvedValue({ id: '1', email: 'user@test.com', passwordHash: '$2b...' }),
};
```

## When to Stop TDD

- Configuration files
- Simple data transformations (use property-based testing instead)
- Exploratory code (spike) — delete tests after learning, rewrite properly

## Definition of Done

- [ ] All tests pass
- [ ] No test mocks real behavior (only I/O)
- [ ] Coverage ≥ 80% on the changed module
- [ ] Tests run in < 1 second total
