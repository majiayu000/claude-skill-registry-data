---
name: craft-dto
description: Crafting DTOs with Spatie Laravel Data v4.
---

# Skill: Craft DTO

> "Type safety isn't a luxury; it's requirements documentation."

## Before You Start

1. **Read the docs**: [spatie.be/docs/laravel-data/v4](https://spatie.be/docs/laravel-data/v4)
2. **Explore the namespace**: `vendor/spatie/laravel-data/src` to avoid hallucination.

## The Standard

1. **Two Types**: `Create{Model}{Suffix}` (input) vs `{Model}{Suffix}` (output/representation).
2. **The Repo Declares `{Suffix}`**: `DTO` or `Data` — whichever already dominates. Consistency with the codebase beats any plugin preference.
3. **Upsert Pairs 1:1**: `Upsert{Model}{Suffix}` ↔ `Upsert{Model}Action`. Matching names, one `Optional` id.
4. **Native Collection**: Prefer `Collection` over `DataCollection`. Use `$data->all()`.
5. **Lazy Relations**: `#[AutoWhenLoadedLazy]` for conditional relationship inclusion.
6. **Immutable**: Mutate via `->with()`, never direct assignment.

## The Anti-Patterns

| ❌ Don't | ✅ Do | Why |
|----------|-------|-----|
| `DataCollection` | Native `Collection` | v4 preferred for basic nesting. |
| `#[Required]` on a typed property | Non-nullable type, no default | v4 derives required-ness from the type. |
| `$dto->except('id')->toArray()` | `$dto->all()` | Cleaner. Handle Optional in action. |
| Omit `#[AutoWhenLoadedLazy]` | Always use on relations | Avoids triggering lazy loads. |
| `#[WithCast]` on output DTO | Only on request DTOs | Casts are for input direction only. |
| Guess API | Read docs + namespace | Avoid hallucination. |
| Direct mutation | `->with()` | Immutability. |

## Real-World Examples

See [examples/](examples/).
