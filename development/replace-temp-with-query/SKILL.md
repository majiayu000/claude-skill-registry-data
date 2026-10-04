---
name: replace-temp-with-query
description: Replace a local variable that caches an expression with a method call so the expression becomes reusable.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Replace Temp with Query

A local variable that stores an expression result can be replaced with a method — making the logic reusable and the code self-documenting.

## When to Use

- A temp variable is assigned once, then only read (never reassigned)
- The expression is complex enough to deserve a name
- The value is needed in multiple methods of the class
- Preparing for Extract Method (temps inside a long method block extraction)

## How to Apply

1. Ensure the temp is assigned exactly once and not modified afterward
2. Extract the right-hand side expression into a method
3. Replace the temp variable usages with calls to the new method
4. Remove the temp variable declaration
5. Run tests

## Example

```ts
// Before
function getPrice(): number {
  const basePrice = quantity * itemPrice;
  const discount = basePrice > 1000 ? basePrice * 0.05 : 0;
  return basePrice - discount;
}

// After
function getPrice(): number {
  return basePrice() - discount();
}
function basePrice(): number { return this.quantity * this.itemPrice; }
function discount(): number { return this.basePrice() > 1000 ? this.basePrice() * 0.05 : 0; }
```

## References

- [refactoring.guru/replace-temp-with-query](https://refactoring.guru/replace-temp-with-query)
