---
name: craft-concern
description: Crafting Concerns (traits). Thin wiring, not business logic.
---

# Skill: Craft Concern

> "A concern wires behavior. It never owns it."

## The Standard

1. **Thin Methods**: Delegate to query builders, collections, and actions.
2. **Naming**: `Has*`, `Interacts*`, `Can*` — match Laravel conventions.
3. **No Business Logic**: Conditionals or transformations? Extract.
4. **Boot Convention**: Use `boot{TraitName}` for model event hooks.

A concern method does **one of three things**:

| Delegation Target | Concern Method Does                  |
|-------------------|--------------------------------------|
| **QueryBuilder**  | Returns a query scope or builder     |
| **Collection**    | Returns a filtered/mapped collection |
| **Action**        | Calls an action and returns result   |

If it does more, it's too fat. Extract.

## The Anti-Patterns

| Don't                   | Do                            | Why                            |
|-------------------------|-------------------------------|--------------------------------|
| Business logic in trait | Delegate to Action            | Traits mix in, logic leaks     |
| Complex queries inline  | Delegate to QueryBuilder      | Reusable, testable             |
| Collection manipulation | Delegate to custom Collection | Named pipeline                 |
| Deep conditionals       | Guard clause or Action        | Traits should be flat          |
| State mutations         | Delegate to Action            | Side effects belong in Actions |

## Real-World Examples

See [examples.md](examples.md).
