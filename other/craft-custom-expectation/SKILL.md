---
name: craft-custom-expectation
description: Crafting custom expectations. When and how to extract.
---

# Skill: Craft Custom Expectation

> "Extract when patterns repeat."

## The Standard

1. **Rule of Three**: Extract when the same pattern appears 3+ times.
2. **Separate File**: Put all custom expectations in `tests/Expectations.php`.
3. **Return $this**: Always return `$this` to enable chaining.

## The Anti-Patterns

| Don't                | Do                             | Why                     |
|----------------------|--------------------------------|-------------------------|
| Extract single-use   | Keep inline                    | Clarity over abstraction |
| Forget `return $this` | Always return                 | Chaining breaks         |
| Scatter across files | Centralize in `Expectations.php` | Discoverability       |
| Reinvent built-ins   | Use Pest's expectations        | Maintenance             |

## Real-World Examples

See [examples.md](examples.md).
