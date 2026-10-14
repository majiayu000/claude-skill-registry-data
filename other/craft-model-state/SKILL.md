---
name: craft-model-state
description: Crafting model states. Explicit state machines.
---

# Skill: Craft Model State

> "States are not strings. They are behavior."

## The Standard

1. **Abstract Base**: One per entity. Defines `config()` with transitions.
2. **Concrete States**: One class per state. Behavior lives here.
3. **Custom Transitions**: Side effects in transition classes, not models.
4. **Co-location**: `Domain/Entity/States/`, not `App/States/`.

## The Anti-Patterns

| ❌ Don't | ✅ Do | Why |
|----------|-------|-----|
| Enum for stateful behavior | State classes | Behavior belongs with state |
| Transitions in model | Custom transition classes | Single responsibility |
| Fat abstract state | Thin base, behavior in concrete | Each state is unique |

## Real-World Examples

See [examples.md](examples.md).
