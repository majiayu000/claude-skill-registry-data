---
name: visitor
description: Separate an algorithm from the object structure it operates on, allowing new operations without modifying the classes.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Visitor

Lets you add new operations to an object structure without modifying its classes, by having each element "accept" a visitor and dispatch to the right visitor method.

## When to Use

- You need to perform many distinct, unrelated operations on an object structure
- Adding these operations to the classes would pollute them
- The object structure is stable but operations on it change frequently
- Traversal and operation should be separated (ASTs, document models, UI trees)

## How to Apply

1. Define a `Visitor` interface with a `visit(element)` overload for each element type
2. Each element class implements `accept(visitor: Visitor)` which calls `visitor.visit(this)`
3. Create concrete visitor classes that implement the operations
4. Traverse the structure and call `accept()` on each element — visitor handles the type dispatch

## Example

```ts
interface Visitor {
  visitCircle(c: Circle): void;
  visitRectangle(r: Rectangle): void;
}

interface Shape { accept(v: Visitor): void; }

class Circle implements Shape {
  constructor(readonly radius: number) {}
  accept(v: Visitor) { v.visitCircle(this); }
}
class Rectangle implements Shape {
  constructor(readonly w: number, readonly h: number) {}
  accept(v: Visitor) { v.visitRectangle(this); }
}

class AreaCalculator implements Visitor {
  total = 0;
  visitCircle(c: Circle)         { this.total += Math.PI * c.radius ** 2; }
  visitRectangle(r: Rectangle)   { this.total += r.w * r.h; }
}

const shapes: Shape[] = [new Circle(5), new Rectangle(4, 6)];
const calc = new AreaCalculator();
shapes.forEach(s => s.accept(calc));
console.log(calc.total); // ~102.54
```

## References

- [refactoring.guru/design-patterns/visitor](https://refactoring.guru/design-patterns/visitor)
