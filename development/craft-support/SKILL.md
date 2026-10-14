---
name: craft-support
description: Crafting Support namespace code. Reusable, domain-agnostic.
---

# Skill: Craft Support

> "Support is the toolbox. It doesn't know the house you're building."

## The Standard

1. **No Domain Imports**: `grep "use Domain" support/` must be empty.
2. **Contracts First**: Define interfaces for Domain to implement.
3. **Traits for Behavior**: `Has*`, `Interacts*`, `Can*` naming.
4. **Base Classes**: Abstract foundations for Domain to extend.

## The Anti-Patterns

| ❌ Don't                  | ✅ Do              | Why                  |
|--------------------------|-------------------|----------------------|
| Import Domain            | Define Contract   | Dependency inversion |
| Business rules           | Generic utilities | Domain-agnostic      |
| Concrete implementations | Abstract base     | Extensibility        |
| Hardcoded values         | Configuration     | Flexibility          |

## When to Use

See [decide-namespacing](../decide-namespacing/SKILL.md) for Support vs Domain decision.

## Real-World Examples

See [examples.md](examples.md).
