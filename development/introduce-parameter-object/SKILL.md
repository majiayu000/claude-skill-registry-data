---
name: introduce-parameter-object
description: Replace a recurring group of parameters with a single data object.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Introduce Parameter Object

When several parameters always travel together across multiple methods, group them into a single object. This reduces signature size, prevents inconsistency, and opens the door for domain logic on the new object.

## When to Use

- Two or more parameters always appear together in method signatures
- Methods share the same "cluster" of parameters
- The parameter group represents a coherent domain concept (e.g., date range, coordinates, pagination)

## How to Apply

1. Create a value object/data class to hold the parameter group
2. Add the new class as a parameter to one method
3. Remove the individual parameters now covered by the object
4. Migrate remaining methods to use the new object
5. Look for behaviour that belongs on the new object and move it there
6. Run tests

## Example

```ts
// Before
function readingsOutsideRange(readings: number[], min: number, max: number) { … }
function countInRange(data: number[], min: number, max: number) { … }

// After
class NumberRange {
  constructor(readonly min: number, readonly max: number) {}
  includes(n: number) { return n >= this.min && n <= this.max; }
}
function readingsOutsideRange(readings: number[], range: NumberRange) { … }
function countInRange(data: number[], range: NumberRange) { … }
```

## References

- [refactoring.guru/introduce-parameter-object](https://refactoring.guru/introduce-parameter-object)
