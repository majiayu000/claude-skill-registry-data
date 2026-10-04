---
name: prototype
description: Create new objects by copying (cloning) an existing object instead of constructing from scratch.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: creational-pattern
---

# Prototype

Delegates object creation to the object itself via a `clone()` method. Useful when construction is expensive or complex and variations of an existing object are needed.

## When to Use

- Object creation is expensive (DB reads, network calls, heavy computation) and cloning is cheaper
- You need many objects that are slight variations of a base object
- Classes to instantiate are specified at runtime
- Avoid subclassing just to configure an object

## How to Apply

1. Create a `Cloneable` / `Prototype` interface with a `clone()` method
2. Implement `clone()` in each concrete class (copy all fields; deep-copy mutable nested objects)
3. Optionally maintain a prototype registry (`Map<string, Prototype>`) for named prototypes
4. Clients call `clone()` instead of `new`

## Example

```ts
interface Prototype<T> { clone(): T; }

class Shape implements Prototype<Shape> {
  constructor(
    public color: string,
    public x: number,
    public y: number,
  ) {}

  clone(): Shape { return new Shape(this.color, this.x, this.y); }
}

// Cheap variant creation
const base = new Shape('red', 0, 0);
const copy = base.clone();
copy.x = 10;   // base is unaffected
```

## References

- [refactoring.guru/design-patterns/prototype](https://refactoring.guru/design-patterns/prototype)
