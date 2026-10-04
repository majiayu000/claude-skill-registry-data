---
name: guard-clauses
description: Replace nested conditional logic with early returns (guard clauses) to reduce nesting and clarify intent.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Replace Nested Conditional with Guard Clauses

Deep nesting hides the main logic. Guard clauses handle special/edge cases early and return immediately, leaving the happy path flat and prominent.

## When to Use

- Method has a deeply nested `if/else if/else` chain
- One branch is the normal case; others are exceptions or edge cases
- Readers must scroll through guards to find core logic
- Cyclomatic complexity is high

## How to Apply

1. Identify exceptional conditions (null, invalid state, permissions)
2. For each: add an early `return` (or `throw`) at the top of the method
3. Remove the now-redundant outer `else`
4. Flatten the remaining code
5. Run tests

## Example

```ts
// Before
function getPayAmount(employee: Employee): number {
  if (employee.isSeparated) {
    return 0;
  } else {
    if (employee.isRetired) {
      return retiredAmount(employee);
    } else {
      return normalPayAmount(employee);
    }
  }
}

// After
function getPayAmount(employee: Employee): number {
  if (employee.isSeparated) return 0;
  if (employee.isRetired) return retiredAmount(employee);
  return normalPayAmount(employee);
}
```

## References

- [refactoring.guru/replace-nested-conditional-with-guard-clauses](https://refactoring.guru/replace-nested-conditional-with-guard-clauses)
