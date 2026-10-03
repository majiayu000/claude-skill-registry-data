---
name: codex-frontend-implementation
description: Use when implementing web UI in React, Next.js, Tailwind, CSS, or GSAP against an approved design, fast-path brief, or prototype UX contract.
load_priority: on-demand
version: "18.1.0"
---

## TL;DR
Implement the brief. Honor incumbent tokens and `DESIGN.md`. Load stack recipes, then at most two craft files. Do not invent a new art direction.

# Frontend Implementation

## Activation
- After `codex-frontend-design` fast, prototype, or studio path.
- `$create` UI work routed to `frontend-specialist`.
- Prompts naming React, Next, Tailwind, shadcn, GSAP, CSS, components.

## Load order
1. `references/frontend-rules.md`
2. Stack recipe: `references/react-tailwind-shadcn.md` and/or `references/nextjs-app-router.md`
3. `references/accessibility-rules.md`
4. Optional craft file from `craft/` matching the requested effect
5. Starter tokens: `starters/design-system.css` (OKLCH, no Inter default)

## Rules
- Match the brief. Do not swap palettes to look busy.
- Prefer transform/opacity motion; honor `prefers-reduced-motion`.
- Every control needs states from `../codex-frontend-design/references/component-states.md`.
- Product facts > anti-slop > wow recipes.
- After substantial UI, run `$visual-gate`.

## Craft library
Curated technique skills live in `craft/`. See `craft/PROVENANCE.md`. Load one file, not the whole folder.
