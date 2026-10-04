---
name: generate-design-md
description: Generate, refactor, or update a DESIGN.md file, the Google Labs open format that documents a project's design system as machine-readable tokens in YAML front matter plus human-readable rationale in the Markdown body. Auto-detects create mode when no DESIGN.md exists, scaffolding from the codebase, or update mode when one exists, syncing it with new styles or a diff. Use when user says "create a DESIGN.md", "generate a design.md", "document the design system", "write design tokens doc", "extract our design system into DESIGN.md", "update DESIGN.md after these style changes", or hands over CSS, Tailwind config, or theme files and asks to capture the visual language.
argument-hint: >
  Optional path to a source of truth — a CSS file, `tailwind.config.*`,
  theme module, Figma export, or a diff (`git diff HEAD~1`) — to scope
  extraction. Omit to scan the whole repo for style sources.
---

# generate-design-md

Produce a `DESIGN.md` per the Google Labs spec: YAML front matter of design
tokens + Markdown body of rationale. One file, repo root, version controlled
next to code.

## Flow

```mermaid
flowchart TD
  A[Start] --> B{DESIGN.md at repo root<br/>or diff passed?}
  B -- yes --> U[Update mode:<br/>patch affected tokens/sections only,<br/>preserve wording & order]
  B -- no --> C[Create mode: scaffold]
  U --> G[Gather real design system]
  C --> G
  G --> Y[Write YAML front matter<br/>see references/authoring.md]
  Y --> M[Write Markdown body<br/>8 sections, fixed order]
  M --> L[Lint]
  L --> R[Report]
```

## 1. Gather the real design system

Document what the code does, not an ideal. Sources, priority order:

| #   | Source                                                                                      |
| --- | ------------------------------------------------------------------------------------------- |
| 1   | `tailwind.config.*` / `theme` extend (colors, fontFamily, spacing, borderRadius, boxShadow) |
| 2   | CSS custom properties (`:root { --color-*, --space-* }`), `@theme` blocks                   |
| 3   | Design-token files (`tokens.json`, DTCG, Style Dictionary)                                  |
| 4   | SCSS/Less vars, styled-components / vanilla-extract themes                                  |
| 5   | Component files — recurring className patterns, variant props                               |
| 6   | Figma export / screenshots the user supplies                                                |

Use `grep` / `rag-rat` / `codebase-memory-mcp` for targeted extraction — don't read whole files when a
pattern search finds the tokens.

## 2. Write front matter + body

Full template, front-matter rules, and the section table are in
**`references/authoring.md`**. Complete worked example in
**`references/example-DESIGN.md`**. Format spec + all 11 lint rules in
**`references/spec.md`**.

## 3. Lint

```bash
npx @google/design.md lint DESIGN.md
```

Fix `broken-ref` errors (exit 1). Resolve warnings or justify. In update mode,
`npx @google/design.md diff old new` to confirm no regressions.

## 4. Report

Mode used · token counts (colors / typography / spacing / components) ·
sections written vs omitted · lint result.
