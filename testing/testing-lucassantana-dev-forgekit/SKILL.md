---
name: testing
description: >-
  Test generation is repetitive but critical. Developers skip tests because
  writing edge cases is tedious. AI agents can generate tests quickly but often
  produce brittle, unrealistic tests that provide false confidence. Tests that
  mock internals, use fake data like "foo@example.com", or test implementation
  details break on every refactor.
---
# AI-Assisted Test Generation

> Write the test description. Let AI generate variations. Always verify the assertions.

## The Problem

Test generation is repetitive but critical. Developers skip tests because writing edge cases is tedious. AI agents can generate tests quickly but often produce brittle, unrealistic tests that provide false confidence. Tests that mock internals, use fake data like "foo@example.com", or test implementation details break on every refactor.

The insight: AI is excellent at generating test variations once you provide a golden example. Use AI to scale test coverage, but write the first test yourself to establish quality standards.

## The Pattern

### The 80/20 Rule for AI Test Generation

**You write (20% effort):**
- Business logic tests (core algorithms, workflows, state machines)
- First test in a new suite (establishes pattern)
- Complex integration tests (multi-step flows)
- Tests requiring domain knowledge

**AI writes (80% effort):**
- Edge case variations (null, empty, boundary conditions)
- Permission matrix tests (role × action combinations)
- Input validation tests (invalid formats, types, ranges)
- Error handling paths
- Regression tests for fixed bugs

### The Golden Test Pattern

Write one high-quality test, then ask AI to generate variations.

**Step 1: Write the golden test**
```typescript
describe('UserService.createUser', () => {
  it('creates user with valid data', async () => {
    const input = {
      email: 'jane.doe@company.com',
      name: 'Jane Doe',
      role: 'editor'
    };

    const user = await userService.createUser(input);

    expect(user).toMatchObject({
      email: 'jane.doe@company.com',
      name: 'Jane Doe',
      role: 'editor',
      id: expect.any(String),
      createdAt: expect.any(Date)
    });

    const saved = await db.users.findById(user.id);
    expect(saved.email).toBe('jane.doe@company.com');
  });
});
```

**Step 2: Ask AI to generate variations**
```
Generate edge case tests for UserService.createUser following the pattern above:
1. Missing required fields (email, name)
2. Invalid email format
3. Duplicate email
4. Invalid role (not in enum)
5. Empty strings for email/name
6. Null values
7. Extra fields in input (should be ignored)

Use realistic data like the golden test (not foo/bar). Each test should verify both the thrown error and that nothing was saved to the database.
```

**Step 3: Review and refine**
Verify AI tests check:
- Correct error type and message
- Database state (nothing saved on error)
- No side effects (no emails sent, no events emitted)

### TDD with AI: Description-First Testing

Write test descriptions as TODO comments, let AI implement.

**Step 1: Write test descriptions**
```typescript
describe('TeamService.deleteTeam', () => {
  // Happy path
  it('deletes team and all members when user is owner');

  // Permissions
  it('throws 403 when user is not owner');
  it('throws 403 when user is admin but not owner');

  // Edge cases
  it('throws 404 when team does not exist');
  it('throws 400 when team has active projects');

  // Cascading
  it('deletes all team members when team is deleted');
  it('deletes all team invitations when team is deleted');

  // Idempotency
  it('returns success when deleting already-deleted team');
});
```

**Step 2: Ask AI to implement**
```
Implement the test descriptions in @services/team.test.ts.

Context:
- TeamService.deleteTeam(teamId, userId) deletes team
- Throws TeamNotFoundError, ForbiddenError, InvalidStateError
- Should delete team_members and team_invitations rows (cascade)
- Database schema: @db/schema.ts
- Error types: @lib/errors.ts

Follow the pattern from @services/user.test.ts:
- Realistic data (real names, not foo/bar)
- Setup test data in beforeEach
- Cleanup in afterEach
- Test both return value and database state
```

### Test Quality Signals

**Good tests (let AI generate):**
- Test behavior, not implementation
- Use realistic data
- Verify observable outcomes (DB state, API response, events)
- Independent (no shared state between tests)
- Fast (<100ms per test)

**Bad tests (don't let AI generate):**
- Mock internal functions (brittle)
- Use foo/bar/test123 data (unrealistic)
- Test private methods (implementation detail)
- Depend on test execution order
- Slow (>1 second per test)

**AI-generated test review checklist:**
```
Review these AI-generated tests:

Quality checks:
- [ ] Realistic data (real names, emails, not foo/bar)
- [ ] Tests behavior (what) not implementation (how)
- [ ] Verifies observable outcomes (DB, API, events)
- [ ] No mocking of internal functions
- [ ] Each test is independent
- [ ] Fast execution (<100ms per test)
- [ ] Clear failure messages

If any check fails, regenerate the test with explicit constraints.
```

### Coverage Targets That Matter

**Target: >80% coverage, but:**
- Exclude trivial code (getters, setters, enums, types)
- Exclude generated code (Prisma client, GraphQL types)
- Focus on business logic and user-facing code

**Don't test:**
```typescript
// Trivial getter
get userId() {
  return this._userId;
}

// Simple enum
enum Role {
  ADMIN = 'admin',
  USER = 'user'
}

// Type definition
interface User {
  id: string;
  email: string;
}
```

**Do test:**
```typescript
// Business logic
function calculateDiscount(user: User, cart: Cart): number {
  if (user.role === 'premium' && cart.total > 100) {
    return cart.total * 0.2;
  }
  return 0;
}

// User-facing behavior
async function createUser(input: CreateUserInput): Promise<User> {
  validate(input);
  const existing = await findByEmail(input.email);
  if (existing) throw new DuplicateEmailError();
  return db.users.create(input);
}
```

### Permission Matrix Testing

Use AI to generate permission tests from a matrix.

**Define the matrix:**
```typescript
const actions = ['create', 'read', 'update', 'delete'];
const roles = ['viewer', 'editor', 'admin', 'owner'];
const permissions = {
  viewer: ['read'],
  editor: ['read', 'update'],
  admin: ['create', 'read', 'update', 'delete'],
  owner: ['create', 'read', 'update', 'delete']
};
```

**Ask AI to generate tests:**
```
Generate permission tests for TeamService from this matrix:

```typescript
${permissions}
```

For each role × action combination:
- If permitted: verify action succeeds
- If forbidden: verify ForbiddenError is thrown

Use the test pattern from @services/user.test.ts (setup in beforeEach, realistic data).
```

**Result: 16 tests (4 roles × 4 actions) generated in seconds.**

### Regression Test Generation

When fixing a bug, let AI generate the regression test.

**Bug report:**
```
Bug: Users can delete teams they don't own
Reproduce:
1. User A creates team
2. User B calls DELETE /api/teams/:id
3. Team is deleted (should be 403)

Root cause: Missing permission check in TeamService.deleteTeam
```

**Regression test prompt:**
```
Generate a regression test for this bug:

Bug: Users can delete teams they don't own

Test should:
1. Create team as user A
2. Attempt delete as user B
3. Verify ForbiddenError is thrown
4. Verify team still exists in database

Follow pattern from @services/team.test.ts (realistic data, check DB state).
```

### Snapshot Testing for Complex Output

AI is good at generating snapshot tests for complex output (HTML, JSON, formatted text).

**Prompt:**
```
Generate snapshot tests for formatUserProfile(@lib/format.ts):

Input: User object (id, email, name, role, createdAt, lastLoginAt)
Output: Formatted string with user details

Generate snapshots for:
1. Admin user with recent login
2. Regular user with no login
3. User with very long name (>50 chars)
4. User with special characters in name

Use realistic data. Follow pattern from @lib/format.test.ts.
```

## Anti-Patterns

### 1. Brittle Tests That Mock Internals

**Bad AI-generated test:**
```typescript
it('creates user', async () => {
  const mockValidate = jest.spyOn(userService, '_validateEmail');
  const mockSave = jest.spyOn(db.users, 'create');

  await userService.createUser({email: 'test@example.com'});

  expect(mockValidate).toHaveBeenCalledWith('test@example.com');
  expect(mockSave).toHaveBeenCalled();
});
```

**Why bad:**
- Mocks internal functions (_validateEmail is private)
- Tests implementation (how), not behavior (what)
- Breaks on refactor even if behavior unchanged

**Fix:**
```typescript
it('creates user with valid email', async () => {
  const user = await userService.createUser({
    email: 'jane@company.com',
    name: 'Jane Doe'
  });

  expect(user.email).toBe('jane@company.com');

  const saved = await db.users.findById(user.id);
  expect(saved).toBeDefined();
});
```

### 2. Unrealistic Test Data

**Bad AI-generated test:**
```typescript
it('creates user', async () => {
  const user = await userService.createUser({
    email: 'foo@bar.com',
    name: 'Test User',
    role: 'test'
  });
  expect(user.id).toBe('123');
});
```

**Why bad:**
- foo@bar.com is not realistic (real email format but fake domain)
- "Test User" is placeholder name
- Role "test" doesn't exist
- Hardcoded ID (won't work in real DB)

**Fix:**
```typescript
it('creates user', async () => {
  const user = await userService.createUser({
    email: 'jane.doe@company.com',
    name: 'Jane Doe',
    role: 'editor'
  });

  expect(user.id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
  expect(user.email).toBe('jane.doe@company.com');
});
```

### 3. Testing Trivial Code

**Bad:**
```
Generate tests for all getters in User class:
- getId()
- getEmail()
- getName()
- getRole()
- getCreatedAt()
```

**Why bad:**
- Getters are trivial (no logic to test)
- Tests add no value
- Coverage metric goes up but quality doesn't

**Fix:**
```
Only test User methods with business logic:
- isAdmin() (checks role + permissions)
- canDeleteTeam(teamId) (complex permission logic)
- getDisplayName() (formats name with fallback)

Skip trivial getters.
```

### 4. Over-Mocking

**Bad AI-generated test:**
```typescript
it('sends welcome email', async () => {
  const mockDb = {users: {create: jest.fn().mockResolvedValue({id: '123'})}};
  const mockEmail = {send: jest.fn()};
  const mockLogger = {info: jest.fn()};
  const mockQueue = {enqueue: jest.fn()};

  const service = new UserService(mockDb, mockEmail, mockLogger, mockQueue);
  await service.createUser({email: 'test@example.com'});

  expect(mockEmail.send).toHaveBeenCalled();
});
```

**Why bad:**
- Mocks everything (no real code runs)
- Tests mock behavior, not real behavior
- Passes even if real code is broken

**Fix:**
```typescript
it('sends welcome email', async () => {
  const user = await userService.createUser({
    email: 'jane@company.com',
    name: 'Jane Doe'
  });

  // Check email was queued (real queue)
  const emails = await emailQueue.getAll();
  expect(emails).toContainEqual({
    to: 'jane@company.com',
    subject: 'Welcome to Platform',
    template: 'welcome'
  });
});
```

**When to mock:**
- External APIs (Stripe, SendGrid) to avoid real charges
- Slow operations (image processing, file uploads)
- Non-deterministic operations (random, Date.now)

**When NOT to mock:**
- Database (use test database)
- Internal functions
- Business logic

### 5. Testing Implementation Details

**Bad AI-generated test:**
```typescript
it('calls validateEmail before saving', async () => {
  const validateSpy = jest.spyOn(userService, 'validateEmail');

  await userService.createUser({email: 'test@example.com'});

  expect(validateSpy).toHaveBeenCalledBefore(dbSpy);
});
```

**Why bad:**
- Tests call order (implementation detail)
- Breaks if refactored to validate differently
- Doesn't test the actual requirement (invalid emails are rejected)

**Fix:**
```typescript
it('rejects invalid email format', async () => {
  await expect(
    userService.createUser({email: 'invalid-email'})
  ).rejects.toThrow(ValidationError);
});
```

### 6. No Assertion on Database State

**Bad AI-generated test:**
```typescript
it('creates user', async () => {
  const user = await userService.createUser({email: 'test@example.com'});
  expect(user.id).toBeDefined();
});
```

**Why bad:**
- Only tests return value
- Doesn't verify data was actually saved
- Could pass even if DB write failed silently

**Fix:**
```typescript
it('creates user', async () => {
  const user = await userService.createUser({
    email: 'jane@company.com',
    name: 'Jane Doe'
  });

  expect(user.id).toBeDefined();

  const saved = await db.users.findById(user.id);
  expect(saved.email).toBe('jane@company.com');
  expect(saved.name).toBe('Jane Doe');
});
```

### 7. Ignoring Test Failures

**Bad:**
```
AI generated 50 tests. 5 are failing but I'll merge anyway since coverage went up.
```

**Why bad:**
- Failing tests mean the code is wrong OR the test is wrong
- Merging failing tests creates false negatives
- Future developers ignore failing tests

**Fix:**
```
Review each failing test:
1. Is the test correct? (does it test the right thing?)
2. Is the code correct? (does it have a bug?)
3. Fix either the test or the code
4. Only merge when all tests pass
```

## Practical Workflow

### Test Generation Workflow

**Step 1: Write the first test (5 minutes)**
```typescript
describe('PaymentService.processRefund', () => {
  it('refunds payment and updates order status', async () => {
    const order = await createTestOrder({status: 'completed', paid: true});

    const refund = await paymentService.processRefund(order.id, 'customer_request');

    expect(refund).toMatchObject({
      orderId: order.id,
      amount: order.total,
      status: 'processed',
      reason: 'customer_request'
    });

    const updated = await db.orders.findById(order.id);
    expect(updated.status).toBe('refunded');
  });
});
```

**Step 2: Generate variations (2 minutes)**
```
Generate edge case tests for PaymentService.processRefund following the pattern above:

1. Order not found (404)
2. Order not paid (400)
3. Order already refunded (400)
4. Partial refund (amount < total)
5. Payment provider failure (retry logic)
6. Invalid refund reason

Use realistic data. Verify both response and database state.
```

**Step 3: Review AI tests (3 minutes)**
- Verify realistic data
- Check error types and messages
- Confirm database state checks
- Run tests and verify they pass

**Step 4: Add to suite (1 minute)**
- Total time: ~10 minutes for 7 tests
- Without AI: ~30-40 minutes

### Test Quality Review Checklist

When reviewing AI-generated tests:

- [ ] Realistic data (real names, emails, not foo/bar/test)
- [ ] Tests behavior (what), not implementation (how)
- [ ] No mocking of internal functions
- [ ] Verifies database state, not just return value
- [ ] Each test is independent (no shared state)
- [ ] Clear test names (describe exact scenario)
- [ ] Covers edge cases (null, empty, boundary)
- [ ] Fast execution (<100ms per test)
- [ ] All tests pass

If any check fails, regenerate with explicit constraints.

## Measuring Test Quality

**Coverage is not enough. Track:**
- **Mutation score:** Run mutation testing (Stryker, pit). Target: >80%
- **Flake rate:** Tests that fail randomly. Target: 0%
- **Test execution time:** Target: <5 minutes for full suite
- **Test maintenance cost:** Time spent fixing broken tests. Target: <10% of dev time

If mutation score is low: tests aren't catching bugs, add better assertions.

If flake rate is high: tests have race conditions or shared state.

If tests are slow: too much mocking, slow setup, or testing too much.

If maintenance is high: tests are brittle (testing implementation, too many mocks).

AI can scale test quantity quickly. You must ensure quality. Write the golden test, verify the variations, always check the database state.
