---
name: tidying
description: Guide structural code improvements using Kent Beck's Tidy First methodology. Use when seeing messy code, before making behavioral changes, after completing features, or discussing when to clean up code.
---

# INSTRUCTIONS

Apply Kent Beck's "Tidy First?" philosophy: small, safe structural changes that improve code without changing behavior. Tidying is separate from feature work and gets its own commits.

- **Behavior Contract**: See `behavior-contract.md` for complete definition of "behavior" (inputs, validation, outputs, side effects, errors) and structural vs behavioral change examples
- **Context Boundaries**: See `context-boundaries.md` for what's safe to tidy in frontend/backend/CLI/library contexts (behavior boundary differs by context!)

## Core Principle

> "Tidying is a special kind of refactoring... tidying is small, and you never need to tidy."

Tidyings are:
- **Small**: Minutes, not hours
- **Safe**: Structure only, no behavior change
- **Optional**: You choose when (or if) to tidy
- **Separate**: Own commits, distinct from behavioral changes

## The Three Timings

| Timing | Trigger | Flow |
|--------|---------|------|
| **Tidy First** | Code is hard to change | `/tidy:first` → `refactor:` commit → behavioral change → `feat:/fix:` commit |
| **Tidy After** | Feature revealed better structure | behavioral change → `feat:/fix:` commit → `/tidy:after` → `refactor:` commit |
| **Tidy Later** | Tidying too big or off-focus | Note opportunity → backlog/TODO → continue current work |

## Decision Framework

```
1. Does this code need to change for my current task?
   No  → Tidy Later (or never)
   Yes ↓
2. Would tidying make my change easier/safer?
   No  → Make behavioral change, consider Tidy After
   Yes ↓
3. Is the tidying small (< 15 minutes)?
   No  → Tidy Later, make behavioral change anyway
   Yes → Tidy First, then make behavioral change
```

## When NOT to DRY

> "Duplication is far cheaper than the wrong abstraction." — Sandi Metz

Keep code inline when:
- Pattern is simple and self-explanatory (`vec![]`, `None`, error returns)
- Abstraction adds indirection without clarity
- Repetitions might evolve differently
- grep/search is easier with inline code

## Reference

Based on: *Tidy First?* by Kent Beck (2023)
