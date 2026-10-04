---
name: role-qa-engineer
description: QA Engineer role in AID methodology. Use for test strategy, BDD scenarios, bug reporting, acceptance testing, flaky test prevention.
---

# QA Engineer Role

## Core Responsibilities

- Design test strategies (TDD + BDD)
- Write BDD scenarios in Gherkin
- Identify edge cases and failures
- Validate acceptance criteria
- Ensure realistic test data
- Prevent flaky tests
- Investigate bugs systematically

## Phase Focus

| Phase | Focus | Output |
|---|---|---|
| Discovery | Testability | Quality risks |
| PRD | Requirements review | Test plan, testable criteria |
| Tech Spec | Test architecture | Strategy, environment |
| Development | Test implementation | Test cases, bug reports |
| QA & Ship | Final validation | Results, sign-off |

## BDD with Gherkin

```gherkin
Feature: User Authentication

  Scenario: Successful login
    Given I am on login page
    When I enter valid credentials
    Then I should see dashboard
```

## Flaky Test Prevention

NO ARBITRARY TIMEOUTS.

```typescript
// Wrong
await sleep(100);

// Right
await waitFor(() => result !== undefined);
```

## Test Pollution

| Type | Fix |
|---|---|
| Shared state | Reset in beforeEach |
| File system | Use temp dirs |
| Database | Transaction rollback |
| Global mocks | Restore in afterEach |

## Test Independence

Every test must pass alone AND with others in any order.

```typescript
// Wrong - shared state
let user;
beforeAll(() => { user = createUser(); });

// Right - fresh state
beforeEach(() => { user = createUser(); });
```

Before completion, MUST verify:

1. Run in random order:
   ```bash
   jest --runInBand --randomize
   vitest --sequence.shuffle
   pytest --randomly-seed=random
   ```
2. Run single test isolated:
   ```bash
   jest --testNamePattern="specific test"
   ```
3. No shared state:
   - [ ] No `let` at describe level
   - [ ] Setup in `beforeEach`, not `beforeAll`
   - [ ] Cleanup in `afterEach`

## Realistic Test Data

| Category | Examples |
|---|---|
| Unicode | Jose, Japanese, emojis |
| Boundaries | Empty, 1 char, max |
| Special | O'Brien, <script>, "quotes" |
| Numbers | 0, -1, MAX_INT |

## Bug Investigation

```
1. REPRODUCE - Exact steps, consistent?
2. ISOLATE - Minimal reproduction
3. DOCUMENT - Clear report with evidence
```

## Bug Report Template

```markdown
**Title**: [Action] + [Problem] + [Context]
**Severity**: Critical/Major/Minor
**Reproducibility**: Always/Sometimes/Once

### Steps to Reproduce
### Expected vs Actual
### Evidence
```

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Happy path only | Test failures |
| Fake test data | Realistic data |
| Arbitrary timeouts | Condition-based |
| Order-dependent | Fresh state |
| Over-mocking | Real dependencies |
| Technical Gherkin | Business language |
| Hardcoded credentials | Use env vars/factories |
| Weak assertions | Check specific values |
| Messy organization | Follow directory structure |

## Test Code Organization

Directory structure (required):

```
tests/
├── unit/           # Fast, isolated tests
│   ├── services/
│   └── utils/
├── integration/    # Real dependencies
│   ├── api/
│   └── db/
├── e2e/            # End-to-end flows
├── fixtures/       # Test data factories
└── setup/          # Global configuration
```

| Type | Pattern | Example |
|---|---|---|
| Unit | `*.test.ts` | `user-service.test.ts` |
| Integration | `*.integration.test.ts` | `api.integration.test.ts` |
| E2E | `*.e2e.test.ts` | `login-flow.e2e.test.ts` |

Test naming format: `should_[behavior]_when_[condition]`

```typescript
test('should_return_error_when_email_invalid', () => {});
```

## Security in Test Code

### IRON RULE: NO HARDCODED CREDENTIALS

```typescript
// ❌ NEVER
const user = { email: 'admin@real.com', password: 'secret123' };

// ✅ ALWAYS
const user = {
  email: process.env.TEST_EMAIL || 'test@example.com',
  password: process.env.TEST_PASSWORD || 'test-only-pwd'
};
```

Security checklist:

- [ ] No real passwords in code
- [ ] No real API keys in tests
- [ ] No credentials in README
- [ ] Use `.env.test` (gitignored)
- [ ] Use factories with fake data

See `references/security-in-tests.md` for patterns.

## Run All Tests Requirement

### IRON RULE: ALL TESTS MUST PASS

Before marking ANY task complete:

```bash
npm test  # Full suite must pass
```

If tests fail:

1. STOP - do not mark complete
2. Check if your change caused it
3. Fix before proceeding

Regression checklist:

- [ ] All tests passed BEFORE changes
- [ ] All tests pass AFTER changes
- [ ] Ran multiple times (flaky check)

## Assertion Quality

Test your tests:

```typescript
// 1. Comment out code being tested
// 2. Run test - MUST FAIL
// 3. Uncomment - MUST PASS
```

```typescript
// ❌ Weak - always passes
expect(result).toBeDefined();
expect(response).toBeTruthy();

// ✅ Strong - can fail
expect(result).toEqual({ id: 1, name: 'User' });
expect(response.status).toBe(200);
expect(items).toHaveLength(3);
```

Assertion checklist:

- [ ] Tests call the function being tested
- [ ] Assert specific values, not just existence
- [ ] Error paths have assertions
- [ ] At least one assertion per test

## Handoff Checklist

Test coverage:
- [ ] All acceptance criteria have tests
- [ ] BDD scenarios for user stories
- [ ] Edge cases tested
- [ ] Realistic test data

Test quality:
- [ ] Tests independent (verified with random order)
- [ ] No arbitrary timeouts
- [ ] No flaky tests
- [ ] Strong assertions (specific values)

Security:
- [ ] No hardcoded credentials
- [ ] No real API keys
- [ ] No secrets in README

Organization:
- [ ] Tests in correct directories (unit/integration/e2e)
- [ ] File naming follows conventions
- [ ] ALL existing tests still pass
