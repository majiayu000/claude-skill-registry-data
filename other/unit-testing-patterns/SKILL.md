---
name: unit-testing-patterns
description: Unit testing patterns for backend and frontend. AAA structure, effective mocking, test isolation.
type: pattern
tier: library
domains: [testing]
trigger: "unit test, mock, stub, spy, isolated test, vitest, jest"
---

## The AAA Pattern

Every test follows Arrange-Act-Assert:

```typescript
it('creates a user with hashed password', async () => {
  // ARRANGE — set up inputs and mocks
  const dto = { email: 'test@example.com', password: 'plaintext' };
  const mockRepo = { save: vi.fn().mockResolvedValue({ id: '1', ...dto }) };
  const service = new UserService(mockRepo);

  // ACT — call the thing under test
  const user = await service.createUser(dto);

  // ASSERT — verify the outcome
  expect(user.id).toBe('1');
  expect(mockRepo.save).toHaveBeenCalledWith(
    expect.objectContaining({ email: dto.email })
  );
  expect(mockRepo.save.mock.calls[0][0].password).not.toBe('plaintext');
});
```

## What to Mock

**Mock:** External I/O — database, network, filesystem, timers, random values

**Don't mock:** Pure functions, your own business logic, constants

```typescript
// GOOD: mock the database (I/O)
vi.mock('./db', () => ({ findUser: vi.fn() }));

// BAD: mock your own service (you'd be testing the mock, not the code)
vi.mock('./userService');
```

## Mocking Strategies

### Spies (observe without replacing)
```typescript
const logSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
// ... do something
expect(logSpy).toHaveBeenCalledWith(expect.stringContaining('Error'));
logSpy.mockRestore();
```

### Stubs (replace with controlled value)
```typescript
const getTimeSpy = vi.spyOn(Date, 'now').mockReturnValue(1234567890);
```

### Module mocks
```typescript
vi.mock('./email-service', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true }),
}));
```

## Test Isolation

```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: ReturnType<typeof createMockRepo>;

  beforeEach(() => {
    // Fresh instance per test — no shared state
    mockRepo = createMockRepo();
    service = new UserService(mockRepo);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
});
```

## Assertion Best Practices

```typescript
// Be specific — assert exact values when meaningful
expect(result.count).toBe(3); // not toBeTruthy()

// Use asymmetric matchers for dynamic values
expect(result).toEqual(expect.objectContaining({
  id: expect.any(String),
  createdAt: expect.any(Date),
  name: 'Alice',
}));

// Test error type specifically
await expect(service.delete('nonexistent')).rejects.toThrow(NotFoundError);

// Don't over-assert (don't test internals)
// BAD: testing private method was called
// GOOD: testing the public observable outcome
```

## Test Naming

```typescript
// Format: [unit] [scenario] [expected result]
it('returns null when user is not found')
it('throws UnauthorizedError when password is wrong')
it('sends welcome email after registration')
it('does not send email when dry-run mode is enabled')
```

## File Organization

```
src/
  users/
    users.service.ts
    users.service.test.ts     ← co-located
    users.repository.ts
    users.repository.test.ts  ← co-located
```

## Coverage Thresholds

Minimum per module: 80%
Critical paths (auth, payments): 95%

```typescript
// vitest.config.ts
coverage: {
  thresholds: { lines: 80, functions: 80, branches: 75 }
}
```
