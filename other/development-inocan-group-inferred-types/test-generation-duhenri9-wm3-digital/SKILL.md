---
name: test-generation
description: Generate comprehensive test cases for code
phases: [E, V]
---

# Test Generation

## When to Use
Use this skill when writing tests or when asked to add test coverage.

## Test Categories

### 1. Unit Tests
- Test individual functions/methods
- Mock dependencies
- Cover edge cases

### 2. Integration Tests
- Test component interactions
- Real dependencies when possible
- Database transactions

### 3. Edge Cases to Cover
- Empty inputs
- Null/undefined values
- Maximum/minimum values
- Invalid types
- Concurrent access
- Network failures

## Test Structure (AAA Pattern)
```
// Arrange - Set up test data and conditions
// Act - Execute the code under test
// Assert - Verify the results
```

## Naming Convention
```
[methodName]_[scenario]_[expectedResult]
```

Example: `calculateTotal_emptyCart_returnsZero`

## Coverage Goals
- Statements: 80%+
- Branches: 75%+
- Functions: 90%+
- Lines: 80%+