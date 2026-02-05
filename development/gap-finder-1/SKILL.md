---
name: gap-finder-1
description: Triggered by start-gap-finder.
---

# Plan Gap Identifier

Generate a raw list of potential conceptual gaps. Don't filter yet.

## What to look for

Terms or claims used but never defined/justified — things that block understanding.

## Rules

1. One line per gap — no sub-bullets
2. Approach-level, not implementation
3. Flag, don't fix — just name the term
4. Max 20 items

## Output format

```
# Step 1: Raw Gaps

- [Line 42] "foo" - undefined
- [Line 87] "X enables Y" - asserted
- [Line 103] "threshold" - unjustified
```

Tags: `undefined` | `unexplained` | `asserted` | `unjustified` | `unclear`

## Anti-patterns

- No question marks
- No "vs" comparisons
- No analysis of WHY it's a gap
- No parenthetical elaboration
