---
name: elysium-visual-fix
description: Fix a specific visual/UI issue on a page without redesigning surrounding elements. Follows inspect-report-plan-diff-approve workflow.
---

# Elysium Visual Fix

Fix one isolated visual issue per invocation. Do not redesign surrounding elements.

## Rules

- One visual fix per task. Do not bundle multiple fixes.
- Do not change elements outside the reported issue.
- Do not introduce new design patterns, colors, or variables.
- Use existing variables from `css/global.css`.
- Do not add inline styles.
- Do not stack `backdrop-filter` layers.
- Keep the visual language premium, calm, dark, polished.
- Preserve travelling line implementation if touching affected components.

## Workflow

1. **Identify** — Confirm the exact element, file, and line with the issue.
2. **Read context** — Read the relevant CSS/JS files to understand current state.
3. **Check design tokens** — Read `css/global.css` to use correct variables.
4. **Plan** — Describe the fix in one sentence. State which file(s) will change.
5. **Show diff** — Show the exact changes before applying.
6. **Wait for approval** — Do not apply changes until approved.
7. **Apply** — Make the change only after approval.
8. **Do not commit** — Leave committing to the user.

## Known Fixes to Apply When Relevant

- Arc sidebar icon transparency: `mix-blend-mode: screen`
- No `orderpanelbg.webp` references
- No stacked `backdrop-filter`
- Travelling line needs `@property --arc-trace-angle`
- Videos need `muted autoplay loop playsinline`
- Valorant rank icon dark backgrounds: `mix-blend-mode: screen`

## What Not to Do

- Do not redesign cards, layout, or sections.
- Do not change fonts or typography scale.
- Do not add animations unless the fix specifically requires it.
- Do not move CSS between files (e.g., page CSS into global).
- Do not combine visual fixes with migration or backend work.
