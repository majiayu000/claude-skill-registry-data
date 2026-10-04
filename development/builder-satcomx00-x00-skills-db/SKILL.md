---
name: builder
description: Construct complex objects step by step, separating construction from representation.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: creational-pattern
---

# Builder

Separates the construction of a complex object from its representation so the same construction process can produce different results. Eliminates "telescoping constructors".

## When to Use

- Object construction requires many optional/configurable parameters
- The same construction steps must produce different representations
- You need step-by-step construction with validation at each step
- Constructors with 4+ parameters (especially many of the same type)

## How to Apply

1. Define the `Product` class (the complex object)
2. Create a `Builder` interface declaring steps for each part
3. Implement one or more concrete `Builder` classes
4. Optionally add a `Director` class to encode common construction sequences
5. Client uses the builder (via director or directly) and calls `build()` to get the product

## Example

```ts
class QueryBuilder {
  private table = '';
  private conditions: string[] = [];
  private limit?: number;

  from(table: string)      { this.table = table; return this; }
  where(cond: string)      { this.conditions.push(cond); return this; }
  take(n: number)          { this.limit = n; return this; }

  build(): string {
    let q = `SELECT * FROM ${this.table}`;
    if (this.conditions.length) q += ` WHERE ${this.conditions.join(' AND ')}`;
    if (this.limit) q += ` LIMIT ${this.limit}`;
    return q;
  }
}

const sql = new QueryBuilder()
  .from('users')
  .where('active = true')
  .take(10)
  .build();
// SELECT * FROM users WHERE active = true LIMIT 10
```

## References

- [refactoring.guru/design-patterns/builder](https://refactoring.guru/design-patterns/builder)
