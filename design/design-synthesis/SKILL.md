---
name: design-synthesis
description: Use when user says "synthesize designs", "show design patterns", "UI patterns", "UX patterns", "update design docs", or asks about UI/UX design decisions - generates two markdown files summarizing UI/UX patterns from implemented stories and anti-patterns from rejected or problematic UI/UX stories.
disable-model-invocation: true
---

# Design Synthesis Skill

Generate `patterns.md` and `anti-patterns.md` in `.claude/data/design/`.

## Workflow

### Step 1: Check Prerequisites

```bash
python .claude/scripts/design_synthesis_helpers.py prereq
```

**Exit early if:**
- `needs_patterns_update` = false AND `needs_anti_patterns_update` = false (counts unchanged)
- No relevant story data (`ui_implemented_count` = 0 AND `ui_rejected_count` = 0)

### Step 2: Spawn Parallel Agents

Launch agents for files that need updating (haiku model):

**Agent 1 (patterns)** - Only if `needs_patterns_update` is true:
- Query: `python .claude/scripts/design_synthesis_helpers.py patterns`
- Read existing `.claude/data/design/patterns.md` for context (if exists)
- Write `.claude/data/design/patterns.md` with sections:
  - **Design Philosophy** - Core UI/UX principles guiding the project
  - **Component Patterns** - Reusable UI component patterns
  - **Interaction Patterns** - Standard user interaction flows
  - **Layout Conventions** - Consistent layout approaches
  - **Accessibility Standards** - A11y requirements and patterns
  - Footer with timestamp

**Agent 2 (anti-patterns)** - Only if `needs_anti_patterns_update` is true:
- Query: `python .claude/scripts/design_synthesis_helpers.py anti-patterns`
- Read existing `.claude/data/design/anti-patterns.md` for context (if exists)
- Write `.claude/data/design/anti-patterns.md` with sections:
  - **Rejected Approaches** - UI/UX ideas explicitly rejected (with rejection reasons)
  - **Usability Issues** - Known usability problems to avoid
  - **Visual Anti-Patterns** - Visual design mistakes to avoid
  - **Interaction Anti-Patterns** - Poor interaction patterns to avoid
  - **Performance Concerns** - UI patterns that cause performance issues
  - Footer with timestamp

### Step 3: Update Metadata

After agents complete, update the synthesis metadata:

```bash
python .claude/scripts/design_synthesis_helpers.py update-meta
```

This records current counts so future prereq checks can skip synthesis when nothing has changed.

## Key Rules

- Spawn agents in parallel, never sequentially
- Use Python sqlite3 module, NOT sqlite3 CLI
- Include rejection reasons in anti-patterns bullets
- Read existing files first to preserve accumulated context
- Always run update-meta after successful synthesis
- Focus on UI/UX-related stories (search for keywords: ui, ux, design, layout, component, button, form, modal, dialog, menu, navigation, style, theme, color, font, icon, responsive, accessibility, a11y)
