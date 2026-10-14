---
name: craft-organization
description: Crafting test structure. File layout for large suites.
---

# Skill: Craft Organization

> "Structure scales. Chaos doesn't."

## The Standard

1. **Separate Concerns**: `Pest.php` for config, `Expectations.php` for custom assertions, `Datasets/` for shared data.
2. **Split at 5**: When a behavioral domain reaches 5+ tests, extract to its own file.
3. **Group Slow Tests**: Isolate slow tests for selective execution.

## The Anti-Patterns

| Don't                 | Do                   | Why             |
|-----------------------|----------------------|-----------------|
| One massive test file | Split by capability  | Maintainability |
| Split by model        | Split by behavior    | Zero overlap    |
| Mix config with tests | Separate `Pest.php`  | Clarity         |
| Run slow tests always | Group and exclude    | Fast feedback   |

## Real-World Examples

See [examples.md](examples.md).
