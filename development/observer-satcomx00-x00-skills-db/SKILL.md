---
name: observer
description: Define a one-to-many dependency so that when one object changes state all its dependents are notified automatically.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Observer

Lets objects (observers/subscribers) register interest in another object (subject/publisher). When the subject changes, all observers are notified automatically.

## When to Use

- Changes to one object require updating an unknown number of others
- An object should notify others without making assumptions about who they are
- Event-driven architectures, reactive state management, MVC (Model notifies View)
- Decoupling producers from consumers of events

## How to Apply

1. Define an `Observer` interface with an `update(event)` method
2. Define a `Subject` interface with `subscribe()`, `unsubscribe()`, and `notify()` methods
3. Implement concrete `Subject` that manages its observer list and calls `notify()` on state change
4. Implement concrete observers that react in `update()`

## Example

```ts
interface Observer { update(data: unknown): void; }

class EventEmitter {
  private listeners = new Map<string, Set<Observer>>();

  on(event: string, obs: Observer) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(obs);
  }
  off(event: string, obs: Observer) { this.listeners.get(event)?.delete(obs); }
  emit(event: string, data?: unknown) {
    this.listeners.get(event)?.forEach(o => o.update(data));
  }
}

class StockTicker extends EventEmitter {
  private price = 0;
  setPrice(p: number) { this.price = p; this.emit('price', p); }
}

const ticker = new StockTicker();
ticker.on('price', { update: (p) => console.log(`Alert: price = ${p}`) });
ticker.setPrice(42); // Alert: price = 42
```

## References

- [refactoring.guru/design-patterns/observer](https://refactoring.guru/design-patterns/observer)
