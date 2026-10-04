---
name: testing
description: Generates test cases, creates mocks, identifies edge cases, analyzes coverage gaps, and supports property-based, mutation, and contract testing. Use when writing tests, improving coverage, detecting flaky tests, or implementing advanced testing strategies.
---

# Testing

Comprehensive test generation and analysis including property-based, mutation, and contract testing.

## Quick Start

**Generate tests for a function:**
```
Generate unit tests for the calculateDiscount function in src/utils/pricing.js
```

**Property-based testing:**
```
Create property-based tests for the data validation module
```

**Find coverage gaps:**
```
Analyze test coverage and identify missing test cases for the auth module
```

## Capabilities

### 1. Test Case Generation

Generate comprehensive test suites from code analysis.

#### Unit Test Template (JavaScript/Jest)

```javascript
describe('functionName', () => {
  beforeEach(() => {
    // Reset state, mocks
  });

  describe('when given valid input', () => {
    it('should return expected result', () => {
      // Arrange
      const input = {};
      const expected = {};

      // Act
      const result = functionName(input);

      // Assert
      expect(result).toEqual(expected);
    });
  });

  describe('when given invalid input', () => {
    it('should throw error for null input', () => {
      expect(() => functionName(null)).toThrow('Input cannot be null');
    });
  });

  describe('edge cases', () => {
    it('should handle empty array', () => {});
    it('should handle maximum values', () => {});
  });
});
```

#### Test Generation Workflow

```
1. Analyze function signature
   - Parameters and types
   - Return type
   - Thrown exceptions

2. Identify code paths
   - Conditionals (if/else, switch)
   - Loops
   - Early returns
   - Error handling

3. Generate test cases for:
   - Happy path (valid inputs)
   - Edge cases (boundaries, empty, null)
   - Error cases (invalid inputs)
```

#### Test Naming Conventions

| Pattern | Example |
|---------|---------|
| `should_ExpectedBehavior_When_StateUnderTest` | `should_ReturnTrue_When_UserIsAdmin` |
| `methodName_StateUnderTest_ExpectedBehavior` | `login_WithValidCredentials_ReturnsToken` |
| `given_When_Then` | `givenValidUser_WhenLogin_ThenReturnsToken` |

See [references/test-patterns.md](references/test-patterns.md) for framework-specific patterns.

---

### 2. Property-Based Testing

Generate inputs that test invariants and properties.

#### Concept

Instead of specific test cases, define properties that should always hold:
- "Sorting a list twice gives the same result as sorting once"
- "Parsing then serializing returns original value"
- "Length of filtered array <= length of original"

#### JavaScript/TypeScript (fast-check)

```javascript
import fc from 'fast-check';

describe('sort function', () => {
  it('should be idempotent', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted1 = sort(arr);
        const sorted2 = sort(sorted1);
        expect(sorted1).toEqual(sorted2);
      })
    );
  });

  it('should preserve length', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        expect(sort(arr).length).toBe(arr.length);
      })
    );
  });

  it('should produce ordered output', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = sort(arr);
        for (let i = 1; i < sorted.length; i++) {
          expect(sorted[i]).toBeGreaterThanOrEqual(sorted[i - 1]);
        }
      })
    );
  });
});
```

#### Python (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sort(sort(xs)) == sort(xs)

@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sort(xs)) == len(xs)

@given(st.text(), st.text())
def test_string_concat_associative(a, b):
    assert len(a + b) == len(a) + len(b)

# Custom strategies
@given(st.builds(User, name=st.text(min_size=1), age=st.integers(0, 150)))
def test_user_serialization(user):
    serialized = user.to_json()
    deserialized = User.from_json(serialized)
    assert user == deserialized
```

See [references/property-testing.md](references/property-testing.md) for more patterns.

---

### 3. Mutation Testing

Verify test effectiveness by introducing bugs.

#### Concept

Mutation testing modifies code and checks if tests fail:
1. Create "mutant" (modified code)
2. Run tests
3. If tests pass, they're not effective (mutant "survives")
4. If tests fail, mutant is "killed" (good)

#### JavaScript (Stryker)

```bash
# Install
npm install --save-dev @stryker-mutator/core

# Configure stryker.conf.json
{
  "packageManager": "npm",
  "reporters": ["html", "clear-text", "progress"],
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "mutate": ["src/**/*.ts", "!src/**/*.spec.ts"]
}

# Run
npx stryker run
```

**Mutation types:**
| Operator | Original | Mutant |
|----------|----------|--------|
| Arithmetic | `a + b` | `a - b` |
| Conditional | `a > b` | `a >= b` |
| Boolean | `true` | `false` |
| String | `"foo"` | `""` |
| Array | `[].push()` | `[].pop()` |

#### Python (mutmut)

```bash
# Install
pip install mutmut

# Run
mutmut run --paths-to-mutate=src/

# View results
mutmut results
mutmut show 1  # Show specific mutant
```

See [references/mutation-testing.md](references/mutation-testing.md) for setup guides.

---

### 4. Visual Regression Testing

Screenshot comparison for UI changes.

#### Playwright

```javascript
import { test, expect } from '@playwright/test';

test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});

test('component visual regression', async ({ page }) => {
  await page.goto('/components/button');
  const button = page.locator('[data-testid="primary-button"]');
  await expect(button).toHaveScreenshot('primary-button.png');
});

// With threshold for minor differences
test('dashboard with threshold', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100
  });
});
```

#### Cypress

```javascript
// cypress/e2e/visual.cy.js
describe('Visual Regression', () => {
  it('matches homepage snapshot', () => {
    cy.visit('/');
    cy.matchImageSnapshot('homepage');
  });

  it('matches component snapshot', () => {
    cy.visit('/components');
    cy.get('[data-testid="card"]').matchImageSnapshot('card');
  });
});
```

---

### 5. Load/Stress Testing

Generate performance tests.

#### k6 Load Test

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100
    { duration: '2m', target: 200 }, // Ramp to 200
    { duration: '5m', target: 200 }, // Stay at 200
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // <1% failures
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

#### Artillery

```yaml
# artillery.yml
config:
  target: 'https://api.example.com'
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50
  defaults:
    headers:
      Authorization: 'Bearer {{ $env.API_TOKEN }}'

scenarios:
  - name: 'User flow'
    flow:
      - get:
          url: '/users'
          capture:
            - json: '$.data[0].id'
              as: 'userId'
      - get:
          url: '/users/{{ userId }}'
```

---

### 6. Contract Testing (Pact)

Verify API contracts between services.

#### Consumer Test (JavaScript)

```javascript
import { Pact } from '@pact-foundation/pact';

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserService',
});

describe('User API Contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('gets a user by ID', async () => {
    await provider.addInteraction({
      state: 'user 1 exists',
      uponReceiving: 'a request for user 1',
      withRequest: {
        method: 'GET',
        path: '/users/1',
        headers: { Accept: 'application/json' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: 1,
          name: Matchers.string('John'),
          email: Matchers.email(),
        },
      },
    });

    const user = await userClient.getUser(1);
    expect(user.id).toBe(1);
  });
});
```

#### Provider Verification

```javascript
const { Verifier } = require('@pact-foundation/pact');

describe('Pact Verification', () => {
  it('validates the expectations of UserService', () => {
    return new Verifier({
      provider: 'UserService',
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/frontend-userservice.json'],
      stateHandlers: {
        'user 1 exists': () => {
          // Set up test data
          return db.createUser({ id: 1, name: 'John' });
        },
      },
    }).verifyProvider();
  });
});
```

---

### 7. Flaky Test Detection

Identify and fix unreliable tests.

#### Detection Patterns

**Time-dependent:**
```javascript
// FLAKY: Depends on current time
it('shows recent items', () => {
  const items = getRecentItems();
  expect(items[0].date).toBe(new Date());
});

// FIXED: Mock time
it('shows recent items', () => {
  jest.useFakeTimers().setSystemTime(new Date('2024-01-15'));
  const items = getRecentItems();
  expect(items[0].date).toEqual(new Date('2024-01-15'));
});
```

**Race conditions:**
```javascript
// FLAKY: Race condition
it('loads data', async () => {
  loadData();
  expect(getData()).toHaveLength(10); // May not be loaded yet
});

// FIXED: Proper async handling
it('loads data', async () => {
  await loadData();
  expect(getData()).toHaveLength(10);
});
```

**Order-dependent:**
```javascript
// FLAKY: Depends on test order
let counter = 0;
it('increments counter', () => {
  counter++;
  expect(counter).toBe(1); // Fails if another test ran first
});

// FIXED: Reset in beforeEach
beforeEach(() => { counter = 0; });
```

#### Detection Tools

```bash
# Run tests multiple times
npx jest --runInBand --repeat 10

# Playwright retry mode
npx playwright test --retries=3 --reporter=json

# Detect with specific tooling
npx jest-flaky-test-detector
```

---

### 8. Snapshot Testing

Capture and compare output snapshots.

```javascript
// Component snapshot
it('renders correctly', () => {
  const tree = renderer.create(<Button label="Click me" />).toJSON();
  expect(tree).toMatchSnapshot();
});

// Data snapshot
it('transforms data correctly', () => {
  const result = transformData(inputData);
  expect(result).toMatchSnapshot();
});

// Inline snapshot
it('formats message', () => {
  expect(formatMessage('Hello')).toMatchInlineSnapshot(`"[INFO] Hello"`);
});
```

---

### 9. Test Data Generation

Generate realistic test data.

#### Factories

```javascript
// factories/user.factory.js
import { faker } from '@faker-js/faker';

export const createUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  role: 'user',
  createdAt: faker.date.past(),
  ...overrides,
});

export const createAdminUser = (overrides = {}) =>
  createUser({ role: 'admin', ...overrides });

// Usage
const users = Array.from({ length: 10 }, createUser);
const admin = createAdminUser({ name: 'Admin User' });
```

#### Database Seeding

```javascript
// seeds/test-data.js
module.exports = {
  users: [
    { id: 1, email: 'alice@test.com', role: 'admin' },
    { id: 2, email: 'bob@test.com', role: 'user' },
  ],
  orders: [
    { id: 1, userId: 2, total: 99.99, status: 'completed' },
  ],
};
```

---

### 10. Test Coverage Gap Analysis

Identify untested code paths.

```bash
# Generate coverage report
npm test -- --coverage

# Jest specific thresholds
jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80}}'

# Python
pytest --cov=src --cov-report=html --cov-fail-under=80
```

**Gap categories:**
| Type | Description | Priority |
|------|-------------|----------|
| Error paths | Exception handling not tested | High |
| Branch coverage | Else clauses not executed | High |
| Edge cases | Boundary conditions | Medium |
| Integration points | External calls | Medium |

---

## Test Organization

### Directory Structure

```
tests/
├── unit/                    # Unit tests mirror src structure
│   ├── services/
│   └── utils/
├── integration/             # Integration tests
│   ├── api/
│   └── database/
├── e2e/                     # End-to-end tests
├── fixtures/                # Test data
├── mocks/                   # Mock implementations
└── helpers/                 # Test utilities
```

### Test Pyramid

```
        /\
       /  \      E2E Tests (few, slow, high confidence)
      /----\
     /      \    Integration Tests (medium)
    /--------\
   /          \  Unit Tests (many, fast)
  /------------\
```

---

## Hook Integration

### PostToolUse Hook - Auto-Test Suggestions

After code changes, suggest relevant tests:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "command": "suggest-tests.sh"
    }]
  }
}
```

**Script example:**
```bash
#!/bin/bash
# suggest-tests.sh

CHANGED_FILE="$1"

# Find corresponding test file
TEST_FILE=$(echo "$CHANGED_FILE" | sed 's/src/tests/' | sed 's/\.ts$/.test.ts/')

if [ ! -f "$TEST_FILE" ]; then
  echo "SUGGEST: No test file found for $CHANGED_FILE"
  echo "  Create: $TEST_FILE"
fi

# Check if function was added
if git diff --cached "$CHANGED_FILE" | grep -q "^+.*function"; then
  echo "SUGGEST: New function added - consider adding unit tests"
fi

# Check coverage
coverage=$(npm test -- --coverage --collectCoverageFrom="$CHANGED_FILE" 2>/dev/null | grep -oP '\d+(?=%)')
if [ "$coverage" -lt 80 ]; then
  echo "SUGGEST: Coverage below 80% for $CHANGED_FILE"
fi
```

**Hook response pattern:**
```typescript
interface TestSuggestion {
  type: 'missing_test' | 'low_coverage' | 'new_function';
  file: string;
  suggestions: string[];
  priority: 'high' | 'medium' | 'low';
}
```

### PreToolUse Hook - Test Validation

Before commits, ensure tests pass:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "command": "validate-tests.sh",
      "condition": "contains(input, 'git commit')"
    }]
  }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Unit Tests
        run: npm test -- --coverage

      - name: Integration Tests
        run: npm run test:integration

      - name: Mutation Testing
        run: npx stryker run

      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E Tests
        run: npx playwright test

      - name: Upload Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run tests for changed files
changed=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|js)$')

for file in $changed; do
  test_file=$(echo "$file" | sed 's/src/tests/' | sed 's/\.ts$/.test.ts/')
  if [ -f "$test_file" ]; then
    npm test -- "$test_file" --passWithNoTests || exit 1
  fi
done
```

## Reference Files

- [references/test-patterns.md](references/test-patterns.md) - Framework-specific test patterns
- [references/mock-patterns.md](references/mock-patterns.md) - Advanced mocking strategies
- [references/property-testing.md](references/property-testing.md) - Property-based testing patterns
- [references/mutation-testing.md](references/mutation-testing.md) - Mutation testing setup guides

## Scripts

- [scripts/generate_tests.py](scripts/generate_tests.py) - Generate test stubs from code analysis
- [scripts/coverage_report.py](scripts/coverage_report.py) - Enhanced coverage analysis
