---
name: craft-expectation-chain
description: Crafting expectation chains. Fluent assertions without traps.
---

# Skill: Craft Expectation Chain

> "Chains compose. Nesting doesn't."

## The Standard

1. **One Subject, Many Assertions**: Chain assertions on the same value.
2. **`and()` for New Subjects**: Switch subjects explicitly.
3. **Break Nested Collections**: `->each->` allows ONE assertion. No deeper.

## The Anti-Patterns

| Don't                            | Do                    | Why              |
|----------------------------------|-----------------------|------------------|
| `->each->prop->each->`           | Separate expectations | Proxy limitation |
| Multiple `expect()` for same value | Chain assertions    | Fluency          |
| Implicit subject switches        | Use `->and()`         | Clarity          |

## Real-World Examples

See [examples.md](examples.md).
