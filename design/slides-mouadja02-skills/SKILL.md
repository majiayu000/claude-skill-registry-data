---
name: slides
description: >-
  Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting
  formulas, and contextual slide strategies. Use when a presentation should be built as an HTML deck
  rather than a PowerPoint file.
argument-hint: "[topic] [slide-count]"
metadata:
  author: claudekit
  version: "1.0.0"
license: MIT
source: "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
attribution: "nextlevelbuilder/ui-ux-pro-max-skill by Next Level Builder"
---

> **Attribution:** Sourced from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) by [Next Level Builder](https://nextlevelbuilder.io), licensed MIT. Modified for this collection.

# Slides

Strategic HTML presentation design with data visualization.

<args>$ARGUMENTS</args>

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments
