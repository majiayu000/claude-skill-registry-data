---
name: craft-null-object
description: Crafting Null Objects. Safe defaults instead of null checks.
---

# Skill: Craft Null Object

> "Instead of checking for null everywhere, return an object that behaves safely."

## The Standard

1. **Null Object behaves like real object**: Same interface, safe defaults.
2. **`withDefault()` for relationships**: Laravel's built-in null object pattern.
3. **Custom Null classes for complex behavior**: When defaults need methods.

## The Anti-Patterns

| ❌ Don't                           | ✅ Do                            | Why                           |
|-----------------------------------|----------------------------------|-------------------------------|
| `$user ? $user->name : 'Guest'`   | `$user->name` with null object   | Eliminate null checks         |
| Null checks in every template     | `withDefault()` on relationship  | Single source of truth        |
| `optional()` for everything       | Null object for repeated access  | `optional()` is for one-offs  |

## Real-World Examples

See [examples.md](examples.md).
