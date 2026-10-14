---
name: craft-trait
description: Crafting model traits. The trait-first integration pattern for Laravel packages.
---

# Skill: Craft Trait

> "A trait is a contract without the ceremony. Add it, and the model gains superpowers."

## The Standard

1. **Boot Methods**: `boot{TraitName}()` hooks into the Eloquent lifecycle. Static method. Register `creating`, `deleting`, `updating` listeners here. Nothing else.

2. **Initialize Methods**: `initialize{TraitName}()` runs on every model instance. Property setup only -- `mergeCasts`, `$fillable` additions, attribute defaults.

3. **Relationships**: Traits define Eloquent relationships that become available on the model. Use `morphToMany` or `morphMany` for polymorphic packages. Always type the return.

4. **Query Scopes**: `scope{Name}()` methods for filtering. Accept the query builder as the first argument, parameters after.

5. **Configuration via Abstract Methods**: Require the model to provide its own configuration. The trait defines the contract, the model fulfills it.

6. **Optional Overrides**: Provide default (usually empty) implementations for optional configuration. Override only when needed.

7. **Accessor/Mutator Interception**: Override `getAttributeValue()` and `setAttribute()` for transparent behavior. Call `parent::` for non-intercepted attributes.

8. **Trait Naming Convention**: Two patterns from Taylor's first-party packages:
   - **Adjective**: `Searchable`, `Billable` -- describes what the model becomes.
   - **Has{Thing}**: `HasApiTokens`, `HasFeatures` -- describes what the model gains.

9. **Concerns Decomposition**: When a trait grows large, split into a `Concerns/` directory and compose them into one user-facing trait. Cashier's `Billable` composes 6 concern traits. Each concern is focused. The user adds one trait.

10. **Utility Traits**: Beyond model traits, consider `Conditionable` (adds `when()`/`unless()` to builders), `Tappable` (adds `tap()` for inspection), and `Macroable` (adds runtime extension via `macro()`/`mixin()`). These are foundational Laravel traits that any class can use.

## The Anti-Patterns

| Don't                                                | Do                                                     | Why                                            |
|------------------------------------------------------|--------------------------------------------------------|------------------------------------------------|
| Require constructor injection                        | Use boot/initialize methods                            | Models don't support constructor DI            |
| Side effects in boot beyond event hooks              | Limit boot to event registration                       | Boot runs on every model load -- keep it light |
| Trait methods named `create()`, `update()`, `save()` | Prefix with domain verbs: `assignRole()`, `addMedia()` | Collides with Eloquent methods                 |
| Forget the trait name prefix on boot/initialize      | `boot{TraitName}()`, `initialize{TraitName}()`         | Multiple traits need unique method names       |
| Return untyped relationships                         | Always type: `BelongsToMany`, `MorphMany`              | IDE autocompletion and static analysis         |
| Hardcode model classes in relationships              | Use `config()` for model resolution                    | Users must be able to swap models              |
| One monolithic trait with 500+ lines                 | Split into `Concerns/` and compose                     | Each concern focused, one user-facing trait    |

## Real-World Examples

See [examples.md](examples.md).
