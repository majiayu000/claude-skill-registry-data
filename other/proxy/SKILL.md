---
name: proxy
description: Provide a substitute that controls access to another object, adding behaviour such as caching, access control, or lazy initialisation.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Proxy

Wraps a real object and controls access to it. The proxy and the real object share the same interface so clients cannot tell the difference.

## When to Use

- **Virtual proxy**: defer expensive object creation until first use (lazy initialisation)
- **Protection proxy**: add access control checks before delegating
- **Caching proxy**: cache results of expensive operations
- **Remote proxy**: represent an object in a different address space (RPC, REST)
- **Logging proxy**: record calls for auditing

## How to Apply

1. Create a `Subject` interface with the operation(s) to proxy
2. Implement `RealSubject` (the actual object)
3. Create `Proxy` implementing `Subject`, holding a reference to `RealSubject`
4. In the proxy's methods, add your cross-cutting logic and delegate to `RealSubject`
5. Clients accept `Subject` — swap `RealSubject` for `Proxy` transparently

## Example

```ts
interface DataService { getData(key: string): string; }

class RealDataService implements DataService {
  getData(key: string): string { /* expensive DB query */ return `data:${key}`; }
}

class CachingProxy implements DataService {
  private cache = new Map<string, string>();
  constructor(private real: RealDataService) {}

  getData(key: string): string {
    if (!this.cache.has(key)) {
      this.cache.set(key, this.real.getData(key));
    }
    return this.cache.get(key)!;
  }
}

// Client code is unchanged
const svc: DataService = new CachingProxy(new RealDataService());
svc.getData('user:1');  // queries DB
svc.getData('user:1');  // served from cache
```

## References

- [refactoring.guru/design-patterns/proxy](https://refactoring.guru/design-patterns/proxy)
