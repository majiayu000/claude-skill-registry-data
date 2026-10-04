---
name: test-driven
description: TDD methodology for production-quality tests. Write tests FIRST driven by PRD, Tech Spec, Implementation Plan. Covers minimal mocking, realistic test data, strong assertions, test independence.
---

# Test-Driven Development Skill

Write tests FIRST, driven by project documents.

## Critical: Document-Driven Testing

Before writing any test:
1. Read latest PRD: docs/prd/[latest].md
2. Read latest Tech Spec: docs/tech-spec/[latest].md
3. Read Implementation Plan: docs/implementation-plan/[latest].md
4. CONFIRM with user: "Is [filename] the current document?"

## Test Pyramid

Layers listed top (fewest tests, slowest, highest business value) to bottom (most tests, fastest). MORE tests at bottom, FEWER at top.

| Layer | Source | Location | Tools | Speed |
|-------|--------|----------|-------|-------|
| **Cucumber** (acceptance) | PRD feature files | features/ | Cucumber.js | Slow |
| GUI/E2E (visual, flows) | Test plan | tests/e2e/ | DevTools MCP | Slow |
| Integration (API, database) | Tech spec APIs | tests/integration/ | Supertest, real DB | Medium |
| Unit (functions, logic) | Implementation | tests/unit/ | Jest, Vitest | Fast |

> **Key Principle:** Cucumber tests ARE your acceptance criteria. The `.feature` files from PRD (Phase 1) are your tests. Your job in Phase 4 is to implement the step definitions that make them pass — you do NOT write acceptance test specs in Phase 4, they already exist. Requirements = tests.

## TDD Cycle

```
RED (Write failing test) -> GREEN (Make pass) -> REFACTOR (Clean up) -> REPEAT
```

| Phase | Action | Rule |
|-------|--------|------|
| RED | Write failing test | MUST fail first |
| GREEN | Minimal code to pass | No extra features |
| REFACTOR | Clean up | Tests still pass |

## BDD Test Execution (Cucumber)

Cucumber executes the acceptance criteria written during Phase 1 (PRD). Each `.feature` file in `features/` becomes an executable test.

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `npm run cucumber` | Local development | Runs all features with progress bar |
| `npm run cucumber:dry` | After writing features | Validates Gherkin syntax, shows undefined steps |
| `npm run test:bdd` | Before PR | Runs all + generates HTML report |
| `npm run test:smoke` | Quick check | Runs only @smoke tagged scenarios |
| `npm run test:critical` | Release gate | Runs only @critical scenarios |

### TDD with Cucumber

```
1. Write feature (Phase 1 - PRD)  → features/auth/login.feature
2. Run dry-run                    → npm run cucumber:dry → See undefined steps
3. Implement steps                → features/step-definitions/auth.steps.ts
4. Run tests                      → npm run cucumber → Should pass
5. Generate report                → npm run test:bdd → Review HTML report
```

### Tag Filtering

```bash
# Run scenarios by tag
npx cucumber-js --tags "@critical"
npx cucumber-js --tags "@smoke or @critical"
npx cucumber-js --tags "not @wip and not @manual"

# Run specific feature file
npx cucumber-js features/auth/login.feature
```

## API Contract Testing (from Tech Spec)

Assert exact response shapes, including status codes and error paths. Full patterns: `references/integration-testing.md`.

```typescript
describe('POST /api/auth/login', () => {
  test('accepts valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@example.com', password: 'SecurePass123!' })
      .expect(200);

    expect(response.body).toEqual({
      token: expect.stringMatching(/^eyJ/),
      user: { id: expect.stringMatching(/^usr_/), email: 'user@example.com' },
      expiresIn: 3600
    });
  });

  test('returns 401 for invalid password', async () => {
    await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@example.com', password: 'wrong' })
      .expect(401);
  });
});
```

## Database Integration Testing

Use a real DB, reset state per test, assert constraints. More: `references/integration-testing.md`, `references/test-data-factories.md`.

```typescript
describe('UserRepository', () => {
  beforeEach(async () => { await prisma.user.deleteMany(); });

  test('creates user with required fields', async () => {
    const user = await userRepository.create({ email: 'new@example.com', name: 'New User' });
    const dbUser = await prisma.user.findUnique({ where: { id: user.id } });
    expect(dbUser?.email).toBe('new@example.com');
  });

  test('enforces unique email', async () => {
    await userRepository.create({ email: 'existing@example.com' });
    await expect(userRepository.create({ email: 'existing@example.com' }))
      .rejects.toThrow('Email already exists');
  });
});
```

## Unit Testing (Business Logic)

Cover the rule plus its boundary. More: `references/test-patterns.md`, `references/test-writing-guide.md`.

```typescript
describe('calculateTotal', () => {
  test('applies percentage discount', () => {
    const items = [{ price: 100, quantity: 2 }, { price: 50, quantity: 1 }];
    expect(calculateTotal(items, { discountPercent: 10 })).toBe(225);
  });

  test('handles empty cart', () => {
    expect(calculateTotal([], {})).toBe(0);
  });
});
```

## GUI Testing (DevTools MCP)

Drive the real UI through `mcp.devtools` and assert on resulting URL/text. Full operation set (navigation, forms, visual, accessibility, performance): `references/gui-testing-mcp.md`.

```typescript
describe('Login Page', () => {
  test('successful login redirects to dashboard', async () => {
    await mcp.devtools.navigate('http://localhost:3000/login');
    await mcp.devtools.type('#email', 'user@example.com');
    await mcp.devtools.type('#password', 'SecurePass123!');
    await mcp.devtools.click('#submit-btn');
    await mcp.devtools.waitForNavigation();
    expect(await mcp.devtools.getCurrentUrl()).toBe('http://localhost:3000/dashboard');
  });

  test('shows error for invalid credentials', async () => {
    await mcp.devtools.navigate('http://localhost:3000/login');
    await mcp.devtools.type('#password', 'wrong');
    await mcp.devtools.click('#submit-btn');
    await mcp.devtools.waitForSelector('.error-message');
    expect(await mcp.devtools.getText('.error-message')).toBe('Invalid email or password');
  });
});
```

## Test File Organization

```
tests/
  unit/services/, utils/, models/
  integration/api/, repositories/
  e2e/flows/, visual/, accessibility/
  factories/
  setup/database.ts, mcp.ts
```

## Document-to-Test Mapping (Gherkin-First)

PRD → Tests:

| PRD Artifact | Test Type | File Location | Created In |
|--------------|-----------|---------------|------------|
| User Stories | **Cucumber feature files** | `features/*.feature` | Phase 1 (PRD) |
| Acceptance Criteria | **Cucumber scenarios** | Inside `.feature` files | Phase 1 (PRD) |
| Error Scenarios | @error-handling scenarios | Inside `.feature` files | Phase 1 (PRD) |
| Edge Cases | @edge-case scenarios | Inside `.feature` files | Phase 1 (PRD) |

Tech Spec → Tests:

| Tech Spec Artifact | Test Type | File Location | Created In |
|--------------------|-----------|---------------|------------|
| API Contracts | Integration tests | `tests/integration/api/` | Phase 4 (Dev) |
| Database Schema | DB integration tests | `tests/integration/db/` | Phase 4 (Dev) |
| Error Responses | Error scenario tests | `tests/integration/errors/` | Phase 4 (Dev) |
| Business Logic | Unit tests | `tests/unit/` | Phase 4 (Dev) |

## Commands

Cucumber commands: see the BDD Test Execution table above.

```bash
# Unit/Integration Tests
npm test                           # All tests
npm test -- --testPathPattern=unit # Unit only
npm test -- --testPathPattern=integration
npm run test:e2e                   # GUI tests
npm test -- --coverage
```

## Checklist Before Writing Tests

Cucumber (from PRD):
- [ ] Feature files exist in `features/` directory
- [ ] `npm run cucumber:dry` shows undefined steps to implement
- [ ] Research backing comments in feature files
- [ ] Appropriate @tags on all scenarios

Other Tests:
- [ ] Found latest PRD, Tech Spec, Plan
- [ ] Confirmed with user
- [ ] Extracted API contracts (Backend tests)
- [ ] Extracted error scenarios
- [ ] Identified test phases

## Anti-Patterns

Detail and fixes: `references/anti-patterns.md`. Review gate: `references/review-checklist.md`.

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Testing implementation | Brittle | Test behavior/outcomes |
| Unrealistic mock data | Miss edge cases | Use realistic factories |
| Only happy path | Miss errors | Test edge cases & errors |
| Order-dependent tests | Flaky | Make independent |
| Over-mocking | Miss bugs | Real integrations (<20% mocking) |
| Weak assertions | False positives | Assert exact values |
