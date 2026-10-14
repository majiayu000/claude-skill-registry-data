---
name: craft-context
description: Crafting Context Objects. Parameter encapsulation for complex operations.
---

# Skill: Craft Context

> "When an action needs too many parameters, the parameters become the object."

## The Standard

1. **Private Constructor**: Direct instantiation blocked. Forces use of named factories.
2. **Named Factories**: `::forProvider()`, `::forBatch()`. Intent in the name.
3. **Self-Validating**: Validate in constructor. Invalid context throws immediately.
4. **Immutable**: `readonly class`. Set once, read many. No setters.

## The Anti-Patterns

| ❌ Don't                     | ✅ Do                          | Why                           |
|-----------------------------|-------------------------------|-------------------------------|
| 5+ action parameters        | Context object                | Clarity, maintainability      |
| Generic constructor         | Named constructors            | Intent is explicit            |
| Mutable context             | Immutable properties          | Prevents bugs in long chains  |
| Array of options            | Typed properties              | IDE support, validation       |

## Real-World Examples

See [examples.md](examples.md).
