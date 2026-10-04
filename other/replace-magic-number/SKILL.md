---
name: replace-magic-number
description: Replace a bare numeric or string literal with a named symbolic constant.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Replace Magic Number with Symbolic Constant

Bare literals (numbers, strings) scattered through code are "magic" — their meaning is unclear and they must be updated in every occurrence if they change.

## When to Use

- A literal value has domain meaning (e.g., `3.14159`, `0.2`, `"ACTIVE"`)
- The same literal appears in more than one place
- The literal is part of a formula or business rule
- Code reviewers cannot understand the value without context

## How to Apply

1. Declare a constant with a descriptive ALL_CAPS (or language-idiomatic) name
2. Replace all occurrences of the literal with the constant
3. Run tests

## Example

```ts
// Before
function annualSalary(monthlySalary: number): number {
  return monthlySalary * 12;
}
function applyTax(amount: number): number {
  return amount * 1.2;
}

// After
const MONTHS_PER_YEAR = 12;
const VAT_MULTIPLIER = 1.2;

function annualSalary(monthlySalary: number): number {
  return monthlySalary * MONTHS_PER_YEAR;
}
function applyTax(amount: number): number {
  return amount * VAT_MULTIPLIER;
}
```

## References

- [refactoring.guru/replace-magic-number-with-symbolic-constant](https://refactoring.guru/replace-magic-number-with-symbolic-constant)
