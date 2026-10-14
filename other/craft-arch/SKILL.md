---
name: craft-arch
description: Crafting arch tests. Structure as code.
---

# Skill: Craft Arch

> "Architecture as code."

## The Standard

1. **Presets First**: Use `php()`, `security()`, `laravel()` before custom rules.
2. **Namespace Constraints**: Enforce inheritance, traits, dependencies.
3. **Ignore Sparingly**: Document why when using `->ignoring()`.

## The Anti-Patterns

| Don't                    | Do                      | Why                |
|--------------------------|-------------------------|--------------------|
| Skip presets             | Start with presets      | Low-hanging fruit  |
| Over-constrain           | Meaningful rules only   | Noise              |
| Silent ignores           | Document ignores        | Traceability       |
| Test behavior with arch  | Use arch for structure  | Different concerns |

## Real-World Examples

See [examples.md](examples.md).
