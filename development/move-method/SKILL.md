---
name: move-method
description: Move a method to the class it uses most so that related behaviour lives together.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Move Method

If a method references another class more than its own, it belongs in that other class. Move it to reduce coupling and increase cohesion.

## When to Use

- A method uses data or methods from another class more than from its own
- Moving the method reduces the coupling between two classes
- Two classes are too tightly coupled and need to be separated
- Method is called frequently by another class

## How to Apply

1. Check that source class does not subclass or override the method
2. Declare the method in the target class; copy the body
3. If the method needs source class data, pass the source as a parameter
4. Adjust the source class method to delegate to the new location, or replace with a direct call
5. Run tests; remove the original if it is no longer needed

## Example

```ts
// Before — Account.overdraftCharge uses AccountType heavily
class Account {
  type: AccountType;
  daysOverdrawn: number;
  overdraftCharge(): number {
    if (this.type.isPremium) {
      const base = 10;
      return this.daysOverdrawn > 7 ? base + (this.daysOverdrawn - 7) * 0.85 : base;
    }
    return this.daysOverdrawn * 1.75;
  }
}

// After
class AccountType {
  overdraftCharge(daysOverdrawn: number): number {
    if (this.isPremium) {
      const base = 10;
      return daysOverdrawn > 7 ? base + (daysOverdrawn - 7) * 0.85 : base;
    }
    return daysOverdrawn * 1.75;
  }
}
class Account {
  overdraftCharge(): number { return this.type.overdraftCharge(this.daysOverdrawn); }
}
```

## References

- [refactoring.guru/move-method](https://refactoring.guru/move-method)
