---
name: craft-dataset
description: Crafting datasets. Same test, different inputs.
---

# Skill: Craft Dataset

> "Same test, different inputs."

## The Standard

1. **Named Keys**: Descriptive keys make failure output readable.
2. **Separate Files**: Shared datasets live in `tests/Datasets/`.
3. **Same Assertion Semantics**: All cases must have identical assertion logic.

## The Anti-Patterns

| Don't                         | Do                     | Why               |
|-------------------------------|------------------------|-------------------|
| Anonymous arrays              | Named keys             | Readable failures |
| Different assertions per case | Explicit tests         | Clarity           |
| Cartesian explosion           | Max 2 datasets chained | Maintainability   |
| Inline for shared data        | Extract to `Datasets/` | Reuse             |

## Real-World Examples

See [examples.md](examples.md).
