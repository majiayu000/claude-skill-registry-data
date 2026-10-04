---
name: state
description: Allow an object to alter its behaviour when its internal state changes — the object will appear to change its class.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# State

Encapsulates each state in its own class. The context delegates behaviour to the current state object instead of using a large conditional.

## When to Use

- An object behaves differently depending on its current state
- State-specific behaviour would otherwise require large `if/switch` blocks
- Transitions between states need to be made explicit and maintainable
- Finite state machines (order status, document workflow, connection lifecycle)

## How to Apply

1. Define a `State` interface with methods for each state-dependent behaviour
2. Create a concrete state class for each possible state
3. The `Context` class holds a reference to the current `State` and delegates calls to it
4. States may trigger transitions by calling `context.setState(newState)`

## Example

```ts
interface TrafficLightState { next(ctx: TrafficLight): void; color(): string; }

class RedState implements TrafficLightState {
  color() { return 'RED'; }
  next(ctx: TrafficLight) { ctx.setState(new GreenState()); }
}
class GreenState implements TrafficLightState {
  color() { return 'GREEN'; }
  next(ctx: TrafficLight) { ctx.setState(new YellowState()); }
}
class YellowState implements TrafficLightState {
  color() { return 'YELLOW'; }
  next(ctx: TrafficLight) { ctx.setState(new RedState()); }
}

class TrafficLight {
  private state: TrafficLightState = new RedState();
  setState(s: TrafficLightState) { this.state = s; }
  next()  { this.state.next(this); }
  color() { return this.state.color(); }
}

const light = new TrafficLight();
console.log(light.color()); // RED
light.next();
console.log(light.color()); // GREEN
```

## References

- [refactoring.guru/design-patterns/state](https://refactoring.guru/design-patterns/state)
