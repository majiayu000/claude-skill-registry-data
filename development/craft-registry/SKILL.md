---
name: craft-registry
description: Crafting Registries. Multi-provider handler dispatch.
---

# Skill: Craft Registry

> "A registry knows who handles what. Nothing more."

## The Standard

1. **Interface Contract**: All handlers implement same interface.
2. **Registration**: Handlers register by key (provider name, type, etc.).
3. **Resolution**: Registry returns correct handler for key.
4. **Fail Loud**: Throw on unknown key. No silent nulls.

## The Anti-Patterns

| ❌ Don't              | ✅ Do                       | Why                        |
|----------------------|----------------------------|----------------------------|
| Switch statements    | Registry lookup            | Open for extension         |
| Return null          | Throw on missing           | Fail fast, debug easy      |
| Hard-coded handlers  | Register via config/tagged | Configurable, testable     |
| God class            | Handlers do the work       | Registry only dispatches   |

## Real-World Examples

See [examples/](examples/).
