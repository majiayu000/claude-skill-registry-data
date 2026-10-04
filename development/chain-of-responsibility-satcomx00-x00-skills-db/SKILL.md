---
name: chain-of-responsibility
description: Pass a request along a chain of handlers; each handler decides to process or forward it.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Chain of Responsibility

Chains handlers in sequence. Each handler either processes the request or passes it to the next handler, decoupling sender from receivers.

## When to Use

- More than one object may handle a request and the handler isn't known a priori
- You want to issue a request to one of several handlers without specifying the receiver explicitly
- Handlers should be configurable and composable at runtime
- Middleware pipelines (HTTP, event processing, validation)

## How to Apply

1. Define a `Handler` interface with `handle(request)` and `setNext(handler)` methods
2. Create a `BaseHandler` that stores the next handler and delegates by default
3. Create concrete handlers that either process the request or call `super.handle()`
4. Build the chain at runtime; pass the request to the first handler

## Example

```ts
interface Handler { setNext(h: Handler): Handler; handle(n: number): string; }

abstract class BaseHandler implements Handler {
  private next?: Handler;
  setNext(h: Handler): Handler { this.next = h; return h; }
  handle(n: number): string { return this.next?.handle(n) ?? `Unhandled: ${n}`; }
}

class SmallHandler extends BaseHandler {
  handle(n: number) { return n < 10 ? `Small handled ${n}` : super.handle(n); }
}
class MediumHandler extends BaseHandler {
  handle(n: number) { return n < 100 ? `Medium handled ${n}` : super.handle(n); }
}

// Build chain
const small = new SmallHandler();
small.setNext(new MediumHandler());

console.log(small.handle(5));    // Small handled 5
console.log(small.handle(50));   // Medium handled 50
console.log(small.handle(500));  // Unhandled: 500
```

## References

- [refactoring.guru/design-patterns/chain-of-responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility)
