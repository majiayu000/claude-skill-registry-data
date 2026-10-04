---
name: bridge
description: Decouple an abstraction from its implementation so both can vary independently.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Bridge

Splits a large class (or set of closely related classes) into two separate hierarchies — abstraction and implementation — that can be developed independently.

## When to Use

- A class has multiple orthogonal dimensions that need to vary independently (e.g., Shape × Renderer)
- You want to avoid a "class explosion" from combining two dimensions via inheritance
- You want to switch implementations at runtime
- Both the abstraction and its implementation should be extensible via subclassing

## How to Apply

1. Identify the two orthogonal dimensions
2. Define an `Implementor` interface for one dimension
3. Create concrete `Implementor` classes
4. Create an `Abstraction` class that holds a reference to an `Implementor`
5. Optionally extend `Abstraction` for the other dimension's variations

## Example

```ts
// Implementor dimension: rendering device
interface Renderer { renderCircle(radius: number): void; }
class VectorRenderer implements Renderer { renderCircle(r: number) { console.log(`Vector circle r=${r}`); } }
class RasterRenderer implements Renderer { renderCircle(r: number) { console.log(`Raster circle r=${r}`); } }

// Abstraction dimension: shape
abstract class Shape {
  constructor(protected renderer: Renderer) {}
  abstract draw(): void;
}
class Circle extends Shape {
  constructor(renderer: Renderer, private radius: number) { super(renderer); }
  draw() { this.renderer.renderCircle(this.radius); }
}

// Runtime: swap renderer without changing shapes
new Circle(new VectorRenderer(), 5).draw();
new Circle(new RasterRenderer(), 5).draw();
```

## References

- [refactoring.guru/design-patterns/bridge](https://refactoring.guru/design-patterns/bridge)
