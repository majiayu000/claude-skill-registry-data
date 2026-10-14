---
name: craft-controller
description: Crafting thin controllers. Traffic cops, not business logic.
---

# Skill: Craft Controller

> "Controllers are traffic cops, not detectives."

## The Standard

1. **CRUDDY**: `index`, `show`, `store`, `update`, `destroy`.
2. **Single-Action**: `__invoke` for complex operations.
3. **Thin**: No business logic. Delegate to Actions.
4. **Transaction Owner**: `DB::transaction()` belongs here.

## The Anti-Patterns

| ❌ Don't                      | ✅ Do                      | Why                        |
|------------------------------|---------------------------|----------------------------|
| Business logic in controller | Delegate to Action        | Single responsibility      |
| Raw queries in controller    | Use QueryBuilder/scopes   | Controllers don't query    |
| Transaction in Action        | Transaction in Controller | Enables Action composition |
| Deep conditionals            | Early returns             | Flat, readable flow        |

## Real-World Examples

See [examples.md](examples.md).
