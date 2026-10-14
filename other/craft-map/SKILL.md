---
name: craft-map
description: Show what exists, where it lives, and what each part is for. Use for a directory tree, a codebase layout, a component hierarchy. Not for sequence (craft-flow) or who acts (craft-swimlane).
when_to_use: directory visualization, tree listing, codebase overview
---

# Skill: Craft Map

> "Show structure, not noise."

## The Principles

- **Annotate** — Each item gets `→ purpose`
- **Collapse** — Use `...` or `*/` for patterns
- **Group** — Blank lines between sections
- **Summarize** — End with count table

## The Format

```
directory/                        # Top-level
├── folder/                       → purpose
│   ├── file.ext                  → what it does
│   └── ...                       → N more
│
└── pattern-*/                    → wildcard
```

## The Rules

1. Max 4 levels unless specified
2. Right-align annotations with `→`
3. Use `#` for section comments in tree
4. Always end with summary table

## Tools

Use `Glob` to discover structure, `Read` for context.

## See Also

- `examples.md` — full examples
