---
name: craft-model
description: Crafting the Eloquent model. Source of truth.
---

# Skill: Craft Model

> "The Model is the heart. Everything else is plumbing."

## The Standard

1. **$dataClass**: Define the DTO representation.
2. **Casts**: Enums, Value Objects, dates. Never raw strings for state.
3. **Relationships**: Define all. Use `ofMany` for latest/oldest.
4. **Custom Builder**: Register via `newEloquentBuilder()`.
5. **Custom Collection**: Register via `newCollection()`.

## The Anti-Patterns

| ❌ Don't           | ✅ Do                                 | Why                      |
|-------------------|--------------------------------------|--------------------------|
| No $dataClass     | Define `protected string $dataClass` | Type-safe representation |
| String status     | Enum cast                            | Type safety              |
| Scopes in Model   | Custom QueryBuilder                  | Separation               |
| Fat Model methods | Actions for logic                    | Single responsibility    |

## Real-World Examples

See [examples.md](examples.md).
