---
name: iterator
description: Traverse elements of a collection without exposing its internal representation.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Iterator

Provides a uniform way to sequentially access elements of a collection regardless of how the collection is structured (array, tree, graph, etc.).

## When to Use

- You want to hide the internal structure of a collection from consumers
- Multiple traversal algorithms must be supported for the same collection
- A unified interface is needed across different collection types
- Lazy / infinite sequences (generate elements on demand)

## How to Apply

1. Define an `Iterator` interface with `hasNext()` and `next()` methods
2. Define an `Iterable` interface with `createIterator()` returning an `Iterator`
3. Implement concrete iterator classes (one per traversal strategy or collection type)
4. The collection implements `Iterable` and returns the appropriate iterator
5. In modern languages, implement the language's native iterable protocol (`Symbol.iterator`, `__iter__`)

## Example

```ts
class Range {
  constructor(private start: number, private end: number) {}

  [Symbol.iterator](): Iterator<number> {
    let current = this.start;
    const end = this.end;
    return {
      next(): IteratorResult<number> {
        return current <= end
          ? { value: current++, done: false }
          : { value: undefined as any, done: true };
      },
    };
  }
}

for (const n of new Range(1, 5)) {
  console.log(n); // 1 2 3 4 5
}
```

## References

- [refactoring.guru/design-patterns/iterator](https://refactoring.guru/design-patterns/iterator)
