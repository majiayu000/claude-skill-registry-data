---
name: extract-variable
description: Give a name to a complex expression by assigning it to a well-named variable.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Extract Variable

Complex or repeated expressions are hard to read. Assign them to a descriptive variable that explains intent.

## When to Use

- Expression is complex or hard to understand at a glance
- Same expression is used in multiple places within a method
- A sub-expression represents a meaningful concept in the domain
- Boolean conditions with many operators

## How to Apply

1. Identify the expression to extract
2. Declare an immutable variable (`const`/`final`) and assign the expression
3. Name the variable after the **concept** it represents, not its type
4. Replace occurrences of the expression with the variable
5. Run tests

## Example

```ts
// Before
if (order.quantity > 100 && order.itemPrice > 50 && order.employee.seniorityYears > 5) {
  applyDiscount(order);
}

// After
const isLargeOrder = order.quantity > 100;
const isHighValue = order.itemPrice > 50;
const isSeniorEmployee = order.employee.seniorityYears > 5;
if (isLargeOrder && isHighValue && isSeniorEmployee) {
  applyDiscount(order);
}
```

## References

- [refactoring.guru/extract-variable](https://refactoring.guru/extract-variable)
