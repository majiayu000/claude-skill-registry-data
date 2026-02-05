---
name: logseq-format
description: Use ONLY when user mentions converting/using/writing in "logseq format" or similar (must mention "logseq")
---

# logseq Format

Format content for logseq, an outliner-based knowledge management tool.

## Core Principles

- **Everything is a bullet**: logseq is outliner-first. All content lives in bullet points.
- **Hierarchy matters**: Use indentation (2 spaces or 1 tab per level) to create structure.
- **Top-level = main ideas**: Start with high-level concepts as top-level bullets (no indentation).

## Formatting Rules

### Top-Level List Structure

```markdown
- First main topic
  - Sub-point with details
  - Another sub-point
    - Deeper nesting for specifics
- Second main topic
  - Related details
- Third main topic
```

### Markup Syntax

- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Highlight**: `^^highlighted^^`
- **Code inline**: `` `code` ``
- **Code block**: Triple backticks with language
- **Links to pages**: `[[Page Name]]`
- **Tags**: `#tag` or `#[[multi word tag]]`
- **Block references**: `((block-id))`
- **TODO markers**: `TODO`, `DOING`, `DONE`, `LATER`, `NOW`

### Properties (metadata)

```markdown
- Main topic
  property-name:: value
  another-property:: another value
  - Content continues here
```

### Example Output

```markdown
- Project Planning #project
  status:: active
  priority:: high
  - Define **scope** and objectives
    - List all deliverables
    - Set clear timeline with [[Q1 Goals]]
  - Identify stakeholders
    - TODO Schedule kickoff meeting
    - Gather requirements from [[Product Team]]
  - Risk assessment
    - Document potential blockers
    - Create mitigation strategies
```

## Best Practices

1. **Start broad, go deep**: Top-level bullets = chapters, nested bullets = details
2. **One idea per bullet**: Keep bullets focused and atomic
3. **Use properties sparingly**: Add metadata only when it adds value for queries
4. **Link liberally**: Connect related concepts with `[[page links]]`
5. **Indent consistently**: Use 2 spaces per indentation level
6. **Frontload importance**: Put most important info at the top of each branch
