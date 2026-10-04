---
name: abstract-factory
description: Produce families of related objects without specifying their concrete classes.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: creational-pattern
---

# Abstract Factory

Provides an interface for creating families of related objects. Swapping the factory swaps the whole product family consistently — no mixed-family products.

## When to Use

- Code must work with multiple families of related products (e.g., UI themes, cloud providers)
- You want to enforce that products from the same family are used together
- You have a set of factory methods and want to group them behind a single interface

## How to Apply

1. Map out the product types and their variants (families)
2. Define abstract interfaces for every product type
3. Define the `AbstractFactory` interface with a creation method for each product type
4. Implement a concrete factory class for each product family
5. Initialize concrete factories in application startup; inject them where needed

## Example

```ts
interface Button  { paint(): void; }
interface Checkbox { paint(): void; }

interface GUIFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}

class WinFactory implements GUIFactory {
  createButton()   { return new WinButton(); }
  createCheckbox() { return new WinCheckbox(); }
}
class MacFactory implements GUIFactory {
  createButton()   { return new MacButton(); }
  createCheckbox() { return new MacCheckbox(); }
}

class App {
  constructor(private factory: GUIFactory) {}
  build() {
    const btn = this.factory.createButton();
    btn.paint();
  }
}
```

## References

- [refactoring.guru/design-patterns/abstract-factory](https://refactoring.guru/design-patterns/abstract-factory)
