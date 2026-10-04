---
name: template-method
description: Define the skeleton of an algorithm in a base class, deferring specific steps to subclasses.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Template Method

Defines an algorithm's structure (skeleton) in a base class. Invariant steps are implemented there; variant steps are left abstract or provide default implementations that subclasses override.

## When to Use

- Multiple classes share the same algorithm structure but differ in specific steps
- Duplication of the algorithm skeleton across subclasses should be eliminated
- Extension points (hooks) should be provided without allowing the overall structure to be changed
- Framework/library code provides the algorithm; application code fills in steps

## How to Apply

1. Identify invariant parts (always the same) and variant parts (differ by subclass) of the algorithm
2. Create an abstract base class with the `templateMethod()` that calls the steps in order
3. Invariant steps are fully implemented in the base class
4. Variant steps are declared `abstract` or given a no-op/default implementation (hooks)
5. Subclasses override only the variant steps

## Example

```ts
abstract class DataMigration {
  // Template method — defines the skeleton
  run() {
    this.readData();
    const processed = this.processData();
    this.writeData(processed);
    this.sendReport();  // hook — optional override
  }

  abstract readData(): void;
  abstract processData(): object[];
  abstract writeData(data: object[]): void;

  protected sendReport() { /* default: do nothing */ }
}

class CsvMigration extends DataMigration {
  readData()                { console.log('Read CSV'); }
  processData(): object[]   { return []; }
  writeData(d: object[])    { console.log('Write to DB'); }
  override sendReport()     { console.log('Email report'); }
}
```

## References

- [refactoring.guru/design-patterns/template-method](https://refactoring.guru/design-patterns/template-method)
