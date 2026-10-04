---
name: adapter
description: Convert the interface of a class into another interface that clients expect, enabling incompatible interfaces to work together.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Adapter

Wraps an existing class in a new interface so it can work with code that expects a different interface. Acts as a translator between two incompatible interfaces.

## When to Use

- Integrating a third-party library with an incompatible interface
- Reusing existing classes that can't be modified
- Multiple classes with similar behaviour but different interfaces must be used uniformly
- Gradual migration between old and new interfaces

## How to Apply

1. Define the `Target` interface that clients expect
2. Identify the `Adaptee` class with the incompatible interface
3. Create an `Adapter` class that implements `Target` and holds a reference to `Adaptee`
4. Implement each `Target` method by translating the call to the appropriate `Adaptee` method
5. Clients use the `Adapter` via the `Target` interface

## Example

```ts
// Existing (Adaptee) — uses XML
class XmlAnalytics {
  analyzeXml(xml: string): object { return {}; /* parse xml */ }
}

// Target interface clients expect
interface Analytics {
  analyze(data: object): object;
}

// Adapter
class AnalyticsAdapter implements Analytics {
  constructor(private adaptee: XmlAnalytics) {}
  analyze(data: object): object {
    const xml = JSON.stringify(data); // convert to xml format
    return this.adaptee.analyzeXml(xml);
  }
}

// Client code
const analytics: Analytics = new AnalyticsAdapter(new XmlAnalytics());
analytics.analyze({ users: 42 });
```

## References

- [refactoring.guru/design-patterns/adapter](https://refactoring.guru/design-patterns/adapter)
