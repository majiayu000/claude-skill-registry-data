---
name: factory-method
description: Define an interface for creating an object but let subclasses decide which class to instantiate.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: creational-pattern
---

# Factory Method

Defines a method for object creation in a base class, allowing subclasses to override which concrete class is instantiated. Decouples creator from product.

## When to Use

- The exact type of object to create is not known until runtime
- Subclasses should control the type of objects they create
- You want to provide a library/framework extension point for object creation
- Constructor logic is complex and varies by context

## How to Apply

1. Define a common `Product` interface/abstract class
2. Create concrete product classes that implement `Product`
3. Define a `Creator` abstract class with an abstract `createProduct(): Product` factory method
4. Add default behaviour in `Creator` that uses `createProduct()`
5. Create concrete `Creator` subclasses that override `createProduct()` to return specific products

## Example

```ts
interface Button { render(): void; onClick(f: () => void): void; }

class WindowsButton implements Button {
  render() { console.log('Render Windows button'); }
  onClick(f: () => void) { f(); }
}
class WebButton implements Button {
  render() { console.log('<button>'); }
  onClick(f: () => void) { document.addEventListener('click', f); }
}

abstract class Dialog {
  abstract createButton(): Button;       // factory method
  render() { const btn = this.createButton(); btn.render(); }
}

class WindowsDialog extends Dialog { createButton() { return new WindowsButton(); } }
class WebDialog extends Dialog     { createButton() { return new WebButton(); } }
```

## References

- [refactoring.guru/design-patterns/factory-method](https://refactoring.guru/design-patterns/factory-method)
