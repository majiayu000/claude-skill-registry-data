---
name: replace-conditional-polymorphism
description: Replace a type-switch or repeated type-checks with polymorphism so each subclass handles its own behaviour.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Replace Conditional with Polymorphism

When you switch on a type code to perform different behaviour, adding a new type means editing every switch. Polymorphism moves each case into its own class.

## When to Use

- A `switch` or chain of `if/else if` checks a type/kind field
- The same type check appears in multiple places
- Adding a new type requires touching many methods
- Objects already differ by a type field that drives behaviour

## How to Apply

1. Create a superclass or interface with the method that varies
2. Create a subclass for each type-code value
3. Move the corresponding `case` logic into each subclass's override
4. Replace the conditional dispatch with a polymorphic call
5. Run tests; remove the original conditional

## Example

```ts
// Before
function speed(bird: Bird): number {
  switch (bird.type) {
    case 'EuropeanSwallow': return 35;
    case 'AfricanSwallow': return Math.max(0, 40 - 2 * bird.numberOfCoconuts);
    case 'NorwegianBlueParrot': return bird.isNailed ? 0 : 10 + bird.voltage / 10;
  }
}

// After
abstract class Bird { abstract speed(): number; }
class EuropeanSwallow extends Bird { speed() { return 35; } }
class AfricanSwallow extends Bird { speed() { return Math.max(0, 40 - 2 * this.numberOfCoconuts); } }
class NorwegianBlueParrot extends Bird { speed() { return this.isNailed ? 0 : 10 + this.voltage / 10; } }
```

## References

- [refactoring.guru/replace-conditional-with-polymorphism](https://refactoring.guru/replace-conditional-with-polymorphism)
