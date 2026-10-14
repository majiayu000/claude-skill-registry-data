---
name: craft-collection
description: Crafting custom collections. Domain pipelines.
---

# Skill: Craft Collection

> "Collections are array pipelines for your domain."

## The Standard

1. **Atomic Methods**: One operation per method.
2. **Fluent**: Return `self` for chaining.
3. **Type-Safe**: `@extends Collection<int, Model>`.
4. **Declarative**: Use `filter`, `map`, `reduce`, not loops.

## The Anti-Patterns

| ❌ Don't          | ✅ Do                   | Why                        |
|------------------|------------------------|----------------------------|
| Business logic   | Simple transformations | Collections aren't Actions |
| Database queries | In-memory operations   | Use QueryBuilder for DB    |
| Loops            | Collection methods     | Declarative > imperative   |
| Mixed types      | Homogeneous collection | Type safety                |

## Real-World Examples

See [examples.md](examples.md).
