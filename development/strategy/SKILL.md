---
name: strategy
description: Define a family of algorithms, encapsulate each one, and make them interchangeable at runtime.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Strategy

Extracts algorithms into separate classes behind a common interface. The client/context picks a strategy at runtime without knowing implementation details.

## When to Use

- Multiple variants of an algorithm exist and need to be swapped
- A class has a large conditional that selects algorithm variants
- Algorithm implementation details must be isolated from code that uses it
- Dependency injection of behaviour (sorting, pricing, routing, validation)

## How to Apply

1. Define a `Strategy` interface with the algorithm's method
2. Implement a concrete strategy class for each variant
3. The `Context` class holds a `Strategy` reference, injected via constructor or setter
4. Context delegates algorithm execution to the current strategy
5. Client selects and injects the appropriate strategy

## Example

```ts
interface SortStrategy { sort(data: number[]): number[]; }

class BubbleSort implements SortStrategy {
  sort(data: number[]) { /* bubble sort */ return [...data].sort((a, b) => a - b); }
}
class QuickSort implements SortStrategy {
  sort(data: number[]) { /* quick sort */ return [...data].sort((a, b) => a - b); }
}

class Sorter {
  constructor(private strategy: SortStrategy) {}
  setStrategy(s: SortStrategy) { this.strategy = s; }
  sort(data: number[]) { return this.strategy.sort(data); }
}

const sorter = new Sorter(new BubbleSort());
sorter.sort([3, 1, 2]);       // uses bubble sort

sorter.setStrategy(new QuickSort());
sorter.sort([30, 10, 20]);    // uses quick sort
```

## References

- [refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy)
