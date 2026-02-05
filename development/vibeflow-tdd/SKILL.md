---
name: vibeflow-tdd
description: Execute TDD Red-Green-Refactor cycle. Use when implementing features with test-driven development.
---

# VibeFlow TDD Cycle

## When to Use
- When implementing new features
- When fixing bugs with regression tests
- When refactoring with test coverage

## The Red-Green-Refactor Cycle

### Phase 1: Red (Write Failing Tests)

**Goal**: Define expected behavior through tests that don't pass yet.

1. Read the issue file and acceptance criteria
2. Create test files:
   - Unit tests: `tests/` or `src/**/__tests__/`
   - Integration tests: `tests/integration/`
   - E2E tests: `e2e/` or `tests/e2e/`
3. Write tests that define expected behavior
4. Run tests and confirm they fail (RED)
5. Commit: `test: Add failing tests for <feature>`

**Checklist**:
- [ ] Tests cover all acceptance criteria
- [ ] Tests cover edge cases
- [ ] Tests are independent (no shared state)
- [ ] Test names are descriptive

### Phase 2: Green (Make Tests Pass)

**Goal**: Write minimal code to pass all tests.

1. Write the simplest code that makes tests pass
2. Run tests after each small change
3. Do NOT over-engineer at this stage
4. Do NOT add features not covered by tests
5. Commit: `feat: Implement <feature>`

**Checklist**:
- [ ] All tests pass (GREEN)
- [ ] No new tests added in this phase
- [ ] Implementation is minimal

### Phase 3: Refactor (Improve Code Quality)

**Goal**: Improve code structure while keeping tests green.

1. Identify code smells:
   - Duplication
   - Long functions
   - Poor naming
   - Missing abstractions
2. Make one refactoring change at a time
3. Run tests after EVERY change
4. Keep tests GREEN throughout
5. Commit: `refactor: Improve <feature> code structure`

**Checklist**:
- [ ] All tests still pass
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Functions are small and focused
- [ ] Names are clear and descriptive
- [ ] No dead code

## Common Test Patterns

### Unit Test Pattern
```
describe('<Component/Function>', () => {
  it('should <expected behavior> when <condition>', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

### Edge Cases to Consider
- Empty inputs
- Null/undefined values
- Boundary values
- Error conditions
- Concurrent operations

## Examples

- "Implement user login with TDD"
- "Add validation with TDD cycle"
- "Refactor payment module keeping tests green"

