---
name: figma
description: "Figma router: Code Connect, screens, design systems, FigJam, use_figma."
disable-model-invocation: true
---

# Figma Skill Index

Router for tasks involving Figma canvas edits, file creation, screen generation, design-system work, Code Connect, or translating designs into code.

## Skill routing (`read_when` hints)

| Skill | `read_when` |
| --- | --- |
| `figma-create-new-file/SKILL.md` | Need blank design or FigJam file before other Figma work |
| `figma-use/SKILL.md` | Need to call `use_figma`, inspect file programmatically, or create/edit/delete nodes, variables, components, auto-layout, fills, bindings |
| `figma-generate-design/SKILL.md` | Need to build/update full page, screen, or multi-section layout from code or description. Load with `figma-use` |
| `figma-generate-library/SKILL.md` | Need to build/update design system from codebase. Load with `figma-use` |
| `figma-implement-design/SKILL.md` | Need to translate Figma design into production code |
| `figma-code-connect/SKILL.md` | Need to create/update `.figma.ts` or `.figma.js` mappings |
| `figma-create-design-system-rules/SKILL.md` | Need project-specific Figma-to-code rules for Claude, Codex, Cursor, or similar agents |

## Composition guidance

- Start with most specific workflow skill; add `figma-use` whenever any step requires `use_figma`
- Common stacks:
  - `figma-create-new-file` → `figma-use`
  - `figma-generate-design` + `figma-use`
  - `figma-generate-library` + `figma-use`
  - `figma-implement-design` + `figma-code-connect` (only when mapping also requested)
