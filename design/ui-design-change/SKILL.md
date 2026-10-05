---
name: ui-design-change
description: Use when modifying CSS, layout, components, icons, client-side JavaScript behavior, accessibility, responsive behavior, or design tokens.
---

# UI And Design Changes

## Read First

- `/ops/style-design.md`
- `/ops/requirements.md`
- Relevant ADRs for the component or behavior being changed.

## Rules

- No silent UX or visual design changes.
- Document IA, token, component, or behavior changes in `/ops` or an ADR before implementation.
- Use existing CSS tokens and component patterns.
- JavaScript must remain ESM.
- Icons in `src/assets/icons/` must have `viewBox` and inherit `currentColor`.
- Preserve accessibility: focus states, labels, keyboard behavior, and reduced-motion behavior.

## Checks

- `npm run check:assets`
- `npm run build`
- `npm run test:playwright`

## Pipeline

Check the result on localhost with [preview-site](../preview-site/SKILL.md), then [release-check](../release-check/SKILL.md) — layout and client JS changes need `npm run test:playwright`.

Design rules that outlive the change belong in `/ops/style-design.md` or an ADR via [ia-nav-adr](../ia-nav-adr/SKILL.md).
