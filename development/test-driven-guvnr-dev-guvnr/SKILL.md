---
name: test-driven
description: Implement test-driven development (TDD) practices. Write tests first, then implementation.
---

# Test-Driven Development Skill

This skill guides test-driven development practices, ensuring code quality through comprehensive testing.

## When to Use

Activate this skill when:

- Implementing new features
- Fixing bugs (write regression test first)
- Refactoring existing code
- The user requests TDD approach

## TDD Workflow

```
┌─────────────────┐
│  1. Write Test  │ ← Start here
│    (Red)        │
└────────┬────────┘
         ▼
┌─────────────────┐
│  2. Write Code  │
│    (Green)      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  3. Refactor    │
│    (Clean)      │
└────────┬────────┘
         │
         └──────────────▶ Repeat
```

## The Three Rules of TDD

1. **Write no production code except to pass a failing test**
2. **Write only enough of a test to demonstrate a failure**
3. **Write only enough production code to pass the test**

## Test Categories

| Type            | Scope                  | Speed  | When to Write           |
| --------------- | ---------------------- | ------ | ----------------------- |
| **Unit**        | Single function/class  | Fast   | Every function          |
| **Integration** | Component interactions | Medium | Every integration point |
| **E2E**         | Full user workflows    | Slow   | Key user journeys       |
| **Regression**  | Known bug scenarios    | Fast   | Every bug fix           |

## Writing Good Tests

### Test Structure (Arrange-Act-Assert)

```javascript
test('should calculate total with tax', () => {
  // Arrange - Set up test data
  const cart = new Cart();
  cart.addItem({ price: 100, quantity: 2 });

  // Act - Execute the code under test
  const total = cart.calculateTotal({ taxRate: 0.1 });

  // Assert - Verify the result
  expect(total).toBe(220);
});
```

### Naming Conventions

```javascript
// Pattern: should [expected behavior] when [condition]
test('should return empty array when no items match filter');
test('should throw error when user not authenticated');
test('should update cache when data changes');
```

### What to Test

- **Happy path**: Normal expected usage
- **Edge cases**: Empty inputs, boundaries, limits
- **Error conditions**: Invalid inputs, failures
- **State changes**: Before and after operations

### What NOT to Test

- Third-party library internals
- Language/framework features
- Trivial getters/setters
- Implementation details (test behavior)

## Test Patterns

### Testing Async Code

```javascript
test('should fetch user data', async () => {
  const user = await fetchUser(123);
  expect(user.name).toBe('John');
});
```

### Testing Errors

```javascript
test('should throw on invalid input', () => {
  expect(() => validate(null)).toThrow('Input required');
});
```

### Using Mocks

```javascript
test('should call API with correct params', () => {
  const mockApi = jest.fn().mockResolvedValue({ data: [] });

  await fetchData(mockApi, { page: 1 });

  expect(mockApi).toHaveBeenCalledWith('/data?page=1');
});
```

## Code Coverage Guidelines

| Metric            | Target | Priority |
| ----------------- | ------ | -------- |
| Line coverage     | 80%+   | High     |
| Branch coverage   | 75%+   | High     |
| Function coverage | 90%+   | Medium   |
| Critical paths    | 100%   | Critical |

## Refactoring with Tests

When refactoring:

1. Ensure existing tests pass
2. Don't change tests and code simultaneously
3. Make small, incremental changes
4. Run tests after each change
5. If tests break, you changed behavior (not just structure)

## Commands

```bash
npm test              # Run all tests
npm test -- --watch   # Watch mode
npm test -- --coverage # Coverage report
npm test -- path/to/test.js # Single file
```

## Troubleshooting

### Tests Are Slow

- Mock external dependencies
- Use in-memory databases
- Parallelize test execution
- Focus unit tests, fewer E2E

### Tests Are Flaky

- Avoid time-dependent assertions
- Use deterministic test data
- Properly await async operations
- Isolate test state

### Hard to Test Code

- Refactor for testability
- Extract dependencies
- Use dependency injection
- Reduce coupling
