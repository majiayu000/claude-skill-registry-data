---
name: decompose-conditional
description: Extract complex condition logic and branches into clearly named methods.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Decompose Conditional

Complex conditionals make code hard to follow. Extract the condition and each branch into descriptively named methods.

## When to Use

- `if`/`else` branches contain several lines of logic
- The condition itself is a complex boolean expression
- Different branches represent distinct business rules
- Code readers must mentally trace logic rather than read intent

## How to Apply

1. Extract the condition into a method named after what it checks
2. Extract the `then`-branch body into its own method
3. Extract the `else`-branch body into its own method
4. Replace the original conditional with calls to these methods
5. Run tests

## Example

```ts
// Before
function charge(date: Date, quantity: number): number {
  if (date >= SUMMER_START && date <= SUMMER_END) {
    return quantity * summerRate + summerServiceCharge;
  } else {
    return quantity * winterRate + winterServiceCharge;
  }
}

// After
function charge(date: Date, quantity: number): number {
  return isSummer(date) ? summerCharge(quantity) : winterCharge(quantity);
}
function isSummer(date: Date): boolean { return date >= SUMMER_START && date <= SUMMER_END; }
function summerCharge(qty: number): number { return qty * summerRate + summerServiceCharge; }
function winterCharge(qty: number): number { return qty * winterRate + winterServiceCharge; }
```

## References

- [refactoring.guru/decompose-conditional](https://refactoring.guru/decompose-conditional)
