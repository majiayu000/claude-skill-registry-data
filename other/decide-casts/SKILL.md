---
name: decide-casts
description: When to use Eloquent Cast vs Accessor. Value representation decisions.
---

# Skill: Casts

> "Casts change storage format. Accessors change presentation."

## The Decision

**Use Cast when:**
- Value requires different storage format (int → Money)
- Transformation applies on both read AND write
- Value Object should be reusable across models

**Use Accessor when:**
- Computed from other attributes
- Read-only transformation
- Depends on model state/context

## The Heuristic

Ask: *"Does this transform how data is stored, or how it's displayed?"*

- **Storage** → Cast
- **Display** → Accessor

## The Quick Test

| Ask Yourself                 | Answer | Use      |
|------------------------------|--------|----------|
| Reusable across models?      | Yes    | Cast     |
| Needs read + write?          | Yes    | Cast     |
| Depends on other attributes? | Yes    | Accessor |
| Computed value?              | Yes    | Accessor |

## Real-World Examples

For concrete examples, see [examples.md](examples.md).
