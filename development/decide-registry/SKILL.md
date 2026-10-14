---
name: decide-registry
description: When to use the Registry pattern for runtime extensibility.
---

# Skill: Registry

> "Register once, resolve anywhere."

## The Decision

**Use Registry when:**
- Need to add/remove implementations at runtime
- Strategies or handlers are resolved by identifier
- Plugin-like extensibility is required
- UI needs to display available options

**Use Direct DI when:**
- Single implementation per interface
- No runtime discovery needed
- Static, compile-time binding is fine

## The Heuristic

Ask: *"Do I need to discover or extend implementations at runtime?"*

- **Yes, dynamic** → Registry
- **No, fixed** → Direct DI

## The Quick Test

| Scenario                               | Use       |
|----------------------------------------|-----------|
| User selects from available strategies | Registry  |
| Third-party can add implementations    | Registry  |
| Need `all()` or `getOptions()` methods | Registry  |
| One implementation, injected directly  | Direct DI |
| Known at compile time                  | Direct DI |

## The Pattern

```php
class StrategyRegistry {
    public function register(StrategyInterface $s): void;
    public function resolve(string $id): ?StrategyInterface;
    public function all(): Collection;
}
```

## Real-World Examples

For concrete examples from Laravel, Spatie, and production code, see [examples.md](examples.md).
