---
name: craft-query
description: Crafting QueryBuilders. Eloquent power, not Repositories.
---

# Skill: Craft Query

> "Eloquent is a superpower. Don't hide it behind a Repository."

## The Standard

1. **No Repositories**: Use Custom QueryBuilders.
2. **Atomic Methods**: Composable (`->pending()->forUser($u)`).
3. **Return Self**: Always `return $this` for chaining.
4. **Descriptive Names**: `pending()`, not `wherePending()`.

## The Anti-Patterns

| ❌ Don't                  | ✅ Do                     | Why                                 |
|--------------------------|--------------------------|-------------------------------------|
| Repository pattern       | QueryBuilder             | Eloquent is already the abstraction |
| One-off scope methods    | Reusable builder methods | DRY                                 |
| `whereStatus('pending')` | `pending()`              | Semantic clarity                    |
| Update logic in builder  | Actions for mutations    | Builders query, Actions mutate      |

## Real-World Examples

See [examples.md](examples.md).
