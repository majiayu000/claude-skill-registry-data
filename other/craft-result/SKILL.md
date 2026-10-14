---
name: craft-result
description: Crafting Result Objects. Rich outcomes beyond success/failure.
---

# Skill: Craft Result

> "A boolean tells you what happened. A Result tells you why."

## The Standard

1. **Named Constructors**: `::success()`, `::failed()`, `::skipped()`. Never bare constructor.
2. **Carry Context**: Include data, messages, metrics. Results are informative.
3. **Immutable**: Results don't change after creation.
4. **Chainable Checks**: `$result->isSuccess()`, `$result->wasSkipped()`.

## The Anti-Patterns

| ❌ Don't                | ✅ Do                        | Why                          |
|------------------------|-----------------------------|-----------------------------|
| Return bool            | Return Result object        | No context on failure        |
| Throw on expected fail | Return `Result::failed()`   | Expected != exceptional      |
| Array with status key  | Typed Result class          | Type safety, IDE support     |
| Log inside action      | Return Result, log outside  | Action stays pure            |

## Real-World Examples

See [examples/](examples/).
