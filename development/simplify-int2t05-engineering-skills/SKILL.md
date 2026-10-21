---
name: simplify
description: Improve scoped code clarity without changing behavior. Triggers on "simplify", "简化".
---

# Code Simplification

## When to use

- Improve scoped code clarity without changing behavior.

**Not for:** refactoring for structural moves; implement for unfinished behavior.

## Steps

1. Understand behavior, callers, tests and reasons for the current structure.

2. Find concrete redundancy or indirection; avoid unrelated cleanup.

3. Apply the smallest behavior-preserving change and check affected behavior.

4. Review clarity and invariant preservation; route feature completion to implement rather than treating it as cleanup.

## Verify

- Behavior and checks remain unchanged; every edit serves scoped simplification.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [clean-code.md](../../../references/clean-code.md) — meaningful names, small functions, comments, error handling (Uncle Bob)
- [references/opportunities.md](references/opportunities.md) — full simplification-opportunities tables (structural / naming / redundancy) + language-specific examples (TypeScript, Python, React/JSX)
