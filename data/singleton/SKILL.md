---
name: singleton
description: Ensure a class has only one instance and provide a global access point to it.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: creational-pattern
---

# Singleton

Guarantees a class has exactly one instance and provides a global access point. Use sparingly — it is essentially a global variable and makes testing harder.

## When to Use

- Exactly one shared resource is needed (logger, config, connection pool, registry)
- Global state must be controlled and lazy-initialized
- Multiple instances would cause incorrect behaviour (e.g., conflicting writes)

## When NOT to Use

- You just want convenient global access — prefer dependency injection instead
- The class has mutable state accessed across threads without synchronisation

## How to Apply

1. Make the constructor private
2. Add a static field to hold the single instance
3. Add a static `getInstance()` method that creates the instance on first call (lazy init)
4. For thread safety, use double-checked locking or language-level initialisation

## Example

```ts
class Database {
  private static instance: Database;
  private constructor(private url: string) {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database(process.env.DB_URL!);
    }
    return Database.instance;
  }

  query(sql: string) { /* … */ }
}

// Usage
const db = Database.getInstance();
db.query('SELECT 1');
```

## References

- [refactoring.guru/design-patterns/singleton](https://refactoring.guru/design-patterns/singleton)
