---
name: craft-factory-state
description: Crafting factory states. DSL for building test state.
---

# Skill: Craft Factory State

> "Factories are a DSL for building state."

## The Standard

1. **States Over Arrays**: Use expressive methods, not inline arrays.
2. **Chain for Composition**: Multiple states combine to tell a story.
3. **Name by Intent**: `revised()` not `withRevisionCount(1)`.

## The Anti-Patterns

| Don't                 | Do                          | Why           |
|-----------------------|-----------------------------|---------------|
| Inline arrays         | Named states                | Readability   |
| Generic names         | Intent-revealing names      | Clarity       |
| Deep nesting in tests | `withDeepHierarchy()` state | Encapsulation |
| Repeat setup          | Extract to state            | DRY           |

## Real-World Examples

See [examples.md](examples.md).
