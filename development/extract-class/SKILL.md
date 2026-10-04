---
name: extract-class
description: Split a class that holds too many responsibilities into two focused classes.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: refactoring
---

# Extract Class

A class that has grown beyond its original purpose accumulates fields and methods that belong to a distinct concept. Extract them into a new class.

## When to Use

- Class has more than one reason to change (violates SRP)
- A subset of fields/methods are always used together
- A natural sub-concept emerges when describing the class
- Class name no longer accurately describes its full responsibility

## How to Apply

1. Identify the cohesive subset of fields and methods to extract
2. Create the new class with a meaningful name
3. Move the fields first (update references in old class via the new object)
4. Move the methods one by one; run tests after each move
5. Decide the visibility (public field or private with accessor)
6. Run tests

## Example

```ts
// Before
class Person {
  name: string;
  officeAreaCode: string;
  officeNumber: string;
  telephoneFor() { return `(${this.officeAreaCode}) ${this.officeNumber}`; }
}

// After
class TelephoneNumber {
  areaCode: string;
  number: string;
  toString() { return `(${this.areaCode}) ${this.number}`; }
}
class Person {
  name: string;
  office = new TelephoneNumber();
  telephoneFor() { return this.office.toString(); }
}
```

## References

- [refactoring.guru/extract-class](https://refactoring.guru/extract-class)
