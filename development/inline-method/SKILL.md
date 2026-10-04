---
name: inline-method
description: Replace a call to a trivial method with the method's body directly.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Inline Method

When a method body is as clear as its name, remove the method and inline the body at the call site.

## When to Use

- Method body is a single line or completely obvious
- Method is called only once and adds no clarity
- Excessive indirection makes code harder to follow
- Prelude to reorganising code into a more sensible structure

## How to Apply

1. Check the method is not polymorphic (no subclass overrides it)
2. Find all call sites
3. Replace each call with the method body
4. Run tests
5. Delete the method

## Example

```ts
// Before
function getRating(driver: Driver): number {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}
function moreThanFiveLateDeliveries(driver: Driver): boolean {
  return driver.lateDeliveries > 5;
}

// After
function getRating(driver: Driver): number {
  return driver.lateDeliveries > 5 ? 2 : 1;
}
```

## References

- [refactoring.guru/inline-method](https://refactoring.guru/inline-method)
