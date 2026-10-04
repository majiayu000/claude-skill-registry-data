---
name: mediator
description: Reduce direct dependencies between objects by routing communication through a central mediator.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Mediator

Centralises communication between components so they don't reference each other directly. Components only know the mediator, not each other — reducing coupling from O(n²) to O(n).

## When to Use

- Many objects communicate in complex ways, creating tight coupling
- Reusing components is hard because they carry too many references
- A UI form with many interacting controls (enabling/disabling fields based on others)
- Chat rooms, event buses, air traffic control, workflow engines

## How to Apply

1. Define a `Mediator` interface with a `notify(sender, event)` method
2. Create a `ConcreteMediator` that knows all components and coordinates their interactions
3. Components hold a reference to the mediator and call `mediator.notify(this, event)` instead of calling each other
4. Move interaction logic from components into the mediator

## Example

```ts
interface Mediator { notify(sender: Component, event: string): void; }

abstract class Component { constructor(protected mediator: Mediator) {} }

class AuthForm extends Component {
  login() { this.mediator.notify(this, 'login'); }
}
class Dashboard extends Component {
  show() { console.log('Dashboard visible'); }
}

class AppMediator implements Mediator {
  constructor(private auth: AuthForm, private dash: Dashboard) {}
  notify(_sender: Component, event: string) {
    if (event === 'login') this.dash.show();
  }
}

const auth = new AuthForm(null!);
const dash = new Dashboard(null!);
const med  = new AppMediator(auth, dash);
(auth as any).mediator = med;
(dash as any).mediator = med;
auth.login(); // → Dashboard visible
```

## References

- [refactoring.guru/design-patterns/mediator](https://refactoring.guru/design-patterns/mediator)
