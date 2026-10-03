---
name: testing-qa
description: Automate the generation and maintenance of unit, integration, and end-to-end tests, as well as test data generation and debugging. Use when writing tests for new features, maintaining existing tests after API/UI changes, generating synthetic test data, or debugging test failures. Essential for ensuring code quality and preventing regressions.
license: MIT
metadata:
  author: AC Framework
  version: "1.0"
---

# Testing & QA

Automated test generation, maintenance, and quality assurance for comprehensive code validation.

## When to Use This Skill

Use this skill when:
- Writing tests for new features or components
- Maintaining existing tests after API or UI changes
- Generating synthetic test data for development/testing
- Debugging failing tests or investigating coverage gaps
- Setting up test infrastructure for a project
- Running test suites and analyzing results

## Instructions

### Step 1: Analyze Test Requirements

1. **Review the specification** or change document
2. **Identify testable components**:
   - Business logic functions
   - API endpoints
   - UI components/interactions
   - Integration points
3. **Determine test types needed**:
   - Unit tests (isolated functions)
   - Integration tests (component interactions)
   - E2E tests (user workflows)

### Step 2: Generate Test Cases

For each component, generate tests covering:

**Unit Tests**:
- Happy path (normal operation)
- Edge cases (empty input, max values, nulls)
- Error cases (exceptions, invalid inputs)
- Boundary conditions

**Integration Tests**:
- Component interactions
- Data flow between modules
- API contract validation
- Database operations

**E2E Tests**:
- Critical user workflows
- Multi-step processes
- Cross-browser compatibility (if applicable)
- Mobile responsiveness (if applicable)

### Step 3: Create Test Files

Follow project conventions:

```
test-file-naming:
  unit: "*.test.js" or "*.spec.js"
  integration: "*.integration.test.js"
  e2e: "*.e2e.test.js" or in "e2e/" folder

test-structure:
  describe: "Component/Feature name"
  it: "should [expected behavior] when [condition]"
```

### Step 4: Generate Test Data

Create realistic test data:

**Static Data**:
```javascript
const mockUsers = [
  { id: 1, name: "John Doe", email: "john@example.com" },
  { id: 2, name: "Jane Smith", email: "jane@example.com" }
];
```

**Dynamic Data** (using factories):
```javascript
const generateUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  name: faker.name.fullName(),
  email: faker.internet.email(),
  ...overrides
});
```

**Synthetic Data for Load Testing**:
- Large datasets for performance testing
- Edge case data (max length strings, special characters)
- Internationalization test data (Unicode, RTL languages)

### Step 5: Implement Tests

Write tests following best practices:

**Arrange-Act-Assert Pattern**:
```javascript
test('should calculate total price with tax', () => {
  // Arrange
  const cart = { items: [{ price: 100, quantity: 2 }] };
  const taxRate = 0.08;
  
  // Act
  const total = calculateTotal(cart, taxRate);
  
  // Assert
  expect(total).toBe(216); // 200 + 16 tax
});
```

**Mock External Dependencies**:
```javascript
jest.mock('../api/client', () => ({
  fetchUser: jest.fn()
}));

beforeEach(() => {
  fetchUser.mockResolvedValue({ id: 1, name: 'Test User' });
});
```

### Step 6: Run Tests and Debug

1. **Execute test suite**:
   ```bash
   npm test
   # or
   npm run test:unit
   npm run test:integration
   npm run test:e2e
   ```

2. **Analyze failures**:
   - Read error messages carefully
   - Check stack traces
   - Verify mocks are set up correctly
   - Compare expected vs actual values

3. **Debug failing tests**:
   - Add console.log for debugging
   - Use debugger statement
   - Check test isolation (beforeEach/afterEach)
   - Verify async handling (await, done callback)

### Step 7: Maintain Tests

When APIs or UI changes:

1. **Identify affected tests** (run test suite)
2. **Update test expectations** to match new behavior
3. **Add new tests** for new functionality
4. **Remove obsolete tests** for removed features
5. **Update mocks** to match new interfaces

### Step 8: Coverage Analysis

1. **Run coverage report**:
   ```bash
   npm run test:coverage
   ```

2. **Identify gaps**:
   - Uncovered branches (if/else conditions)
   - Missing edge cases
   - Untested error paths

3. **Add tests** to cover gaps

## Integration with OpenSpec

- Use `openspec-verify-change` to validate tests pass
- Link test files to tasks in tasks.md
- Include test requirements in design.md
- Reference test coverage in verification reports

## Guardrails

- **Test behavior, not implementation** - Tests should verify what code does, not how
- **One assertion per test** (ideally) - Makes failures clearer
- **Keep tests fast** - Unit tests should run in milliseconds
- **Mock external systems** - Don't hit real databases/APIs in unit tests
- **Clean up after tests** - Use afterEach to reset state
- **Don't test framework code** - Focus on business logic

## Common Patterns

**Testing Async Code**:
```javascript
test('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user).toEqual({ id: 1, name: 'John' });
});
```

**Testing React Components**:
```javascript
import { render, screen, fireEvent } from '@testing-library/react';

test('should toggle visibility on click', () => {
  render(<ToggleButton />);
  const button = screen.getByRole('button');
  
  fireEvent.click(button);
  expect(screen.getByText('Visible')).toBeInTheDocument();
  
  fireEvent.click(button);
  expect(screen.queryByText('Visible')).not.toBeInTheDocument();
});
```

**Testing API Endpoints**:
```javascript
import request from 'supertest';
import app from '../app';

test('POST /api/users should create user', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ name: 'John', email: 'john@example.com' });
    
  expect(response.status).toBe(201);
  expect(response.body).toHaveProperty('id');
});
```

## Requirements

- Access to test runner (Jest, Mocha, Vitest, etc.)
- Test utilities (@testing-library/react, supertest, etc.)
- Code coverage tool (Istanbul, c8, etc.)
- Access to the codebase being tested

## See Also

- `test-generator` - Generate initial test suite
- `openspec-verify-change` - Validate implementation with tests
- `systematic-debugging` - Debug failing tests
- `secure-coding-cybersecurity` - Security-focused testing
