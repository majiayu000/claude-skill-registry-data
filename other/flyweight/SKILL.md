---
name: flyweight
description: Reduce memory usage by sharing common state among many fine-grained objects.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Flyweight

Extracts the shared (intrinsic) state of many similar objects into a single shared object, while unique (extrinsic) state is passed in on each operation.

## When to Use

- A huge number of similar objects consume too much memory
- Most of the object's state can be made extrinsic (passed from outside)
- Objects can be grouped by their shared intrinsic properties
- Common in game engines (particles, trees, bullets), text editors (character formatting)

## How to Apply

1. Split object state into **intrinsic** (shared, immutable) and **extrinsic** (unique per context)
2. Create a `Flyweight` class holding only intrinsic state
3. Create a `FlyweightFactory` with a cache (`Map`) keyed by intrinsic state
4. Clients retrieve flyweights from the factory; pass extrinsic state when calling operations

## Example

```ts
// Intrinsic state shared across thousands of bullets
class BulletType {
  constructor(readonly color: string, readonly sprite: string) {}
  draw(x: number, y: number) { /* render sprite at (x,y) */ }
}

class BulletFactory {
  private cache = new Map<string, BulletType>();
  get(color: string, sprite: string): BulletType {
    const key = `${color}-${sprite}`;
    if (!this.cache.has(key)) this.cache.set(key, new BulletType(color, sprite));
    return this.cache.get(key)!;
  }
}

// Extrinsic state (position) lives in the game loop, not in the flyweight
const factory = new BulletFactory();
const bullets = Array.from({ length: 10_000 }, (_, i) => ({
  type: factory.get('red', 'bullet.png'),  // shared
  x: Math.random() * 800,                  // unique
  y: i,
}));
bullets.forEach(b => b.type.draw(b.x, b.y));
```

## References

- [refactoring.guru/design-patterns/flyweight](https://refactoring.guru/design-patterns/flyweight)
