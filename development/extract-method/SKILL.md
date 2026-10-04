---
name: extract-method
description: Pull a code fragment into a named method to improve readability and enable reuse.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Extract Method

A fragment of code can be grouped together, turned into its own method, and replaced with a call to that method.

## When to Use

- Code fragment can be understood at a glance via a good name
- Method is too long (> 10–15 lines)
- Same fragment appears in multiple places (duplication)
- A comment explains *what* a block does — the comment should become the method name

## How to Apply

1. Create a new method; name it after the fragment's **intent** (not mechanics)
2. Copy the fragment into the new method
3. Identify local variables used in the fragment; pass them as parameters
4. If a variable is modified, return it (or use an object)
5. Replace the original fragment with a call to the new method
6. Run tests

## Example

```ts
// Before
function printOrder(order: Order) {
  console.log(`Order #${order.id}`);
  // print items
  let total = 0;
  for (const item of order.items) {
    console.log(`  ${item.name} x${item.qty} = ${item.price * item.qty}`);
    total += item.price * item.qty;
  }
  console.log(`Total: ${total}`);
}

// After
function printOrder(order: Order) {
  console.log(`Order #${order.id}`);
  printItems(order.items);
}

function printItems(items: Item[]) {
  let total = 0;
  for (const item of items) {
    console.log(`  ${item.name} x${item.qty} = ${item.price * item.qty}`);
    total += item.price * item.qty;
  }
  console.log(`Total: ${total}`);
}
```

## References

- [refactoring.guru/extract-method](https://refactoring.guru/extract-method)
