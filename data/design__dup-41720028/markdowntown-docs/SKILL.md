---
name: markdowntown-docs
description: Use this when writing or updating docs/ content, UX specs, or cross-linking guides in markdowntown.
---

# Docs + content updates

## When to use
- Editing or adding docs under `docs/`.
- Aligning terminology across UX, architecture, and product guides.
- Updating user-facing flow documentation.

## Workflow
1. **Pick the right home**
   - UX flow or copy guidance → `docs/ux`.
   - Visual/UI guidance → `docs/design` or `docs/ui`.
   - Technical system notes → `docs/architecture`.
   - User-facing walkthroughs → `docs/USER_GUIDE.md`.

2. **Keep terminology consistent**
   - Use “Scan”, “Workbench”, “Library”, “Translate”, “Docs”.
   - Distinguish **AGENTS.md** (repo file) vs **agents.md** (export output).

3. **Cross-linking**
   - Link related docs when a flow spans multiple surfaces (e.g., UX → Architecture).
   - Avoid duplicating long explanations; point to canonical docs.

4. **Editing checklist**
   - Maintain concise headings, short paragraphs, and action-oriented language.
   - Update any references, diagrams, or CTA text if UI changed.

## References
- codex/skills/markdowntown-docs/references/docs-map.md
- codex/skills/markdowntown-docs/references/content-style.md

## Guardrails
- Keep SKILL.md concise; move long detail to references.
- Always log follow-up tasks for gaps you notice.
