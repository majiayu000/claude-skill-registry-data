---
name: decorator
description: Attach new behaviour to objects at runtime by wrapping them in decorator objects.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Decorator

Wraps an object to extend its behaviour without modifying the original class or using inheritance. Decorators are composable — stack multiple wrappers for combined effects.

## When to Use

- You need to add behaviour to individual objects without affecting others of the same class
- Extension by subclassing is impractical due to combinatorial explosion
- Behaviour should be composable and removable at runtime
- Cross-cutting concerns: logging, caching, validation, rate-limiting

## How to Apply

1. Define a `Component` interface with the core operation
2. Create a `ConcreteComponent` that implements `Component`
3. Create a `BaseDecorator` implementing `Component` and holding a wrapped `Component`
4. Create concrete decorators extending `BaseDecorator`, adding behaviour before/after the delegate call
5. Wrap components with decorators at the composition root

## Example

```ts
interface DataSource { write(data: string): void; read(): string; }

class FileDataSource implements DataSource {
  constructor(private filename: string) {}
  write(data: string) { /* write to file */ }
  read(): string { return ''; /* read from file */ }
}

class EncryptionDecorator implements DataSource {
  constructor(private wrapped: DataSource) {}
  write(data: string) { this.wrapped.write(encrypt(data)); }
  read(): string      { return decrypt(this.wrapped.read()); }
}

class CompressionDecorator implements DataSource {
  constructor(private wrapped: DataSource) {}
  write(data: string) { this.wrapped.write(compress(data)); }
  read(): string      { return decompress(this.wrapped.read()); }
}

// Stack decorators
const source = new CompressionDecorator(new EncryptionDecorator(new FileDataSource('data.bin')));
source.write('hello');
```

## References

- [refactoring.guru/design-patterns/decorator](https://refactoring.guru/design-patterns/decorator)
