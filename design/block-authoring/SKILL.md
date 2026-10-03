---
name: block-authoring
layer: stack
description: Author a placeable layout block that looks right at ANY pane size. The one hard rule — size to the PANE with container queries (@container), never the viewport — plus list/form playbooks and the sizing contract (minWidth etc.) the viability metric reads. Use when adding/converting a croutonLayoutBlocks block, or when a block overflows/breaks in a narrow pane.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Author a block that looks good in any pane

A layout block doesn't live in a known screen — it lives in **whatever pane the
user dragged it to**. So it must respond to **its container, not the viewport**,
and it must **declare how small it's allowed to get**. This skill is the playbook;
the contract it fills in is read by the viability metric (`checkLayoutViability`,
#710) and the deterministic layout pass (#709).

Part of the layout engine (epic #703). A block is registered in
`croutonLayoutBlocks` (see `crouton-core` CLAUDE.md, #704) — this skill is about
how to *build the component* behind that registration.

## The one hard rule: container queries, not viewport media queries

A block's width ≠ the viewport width. A list in a 280px sidebar on a 4K monitor
is *narrow*, even though the viewport is huge. So:

- ✅ Use **`@container`** (Tailwind / Nuxt UI 4 container queries) keyed off a
  container on the block root. Put `@container` on the root element, then size
  children with the `@`-prefixed variants (`@sm:`, `@md:`, `@lg:` …).
- ❌ **Never** use viewport media queries (`sm:`/`md:`/`lg:`) or
  `useBreakpoints`/`window` width for a block's *internal* layout — those track
  the screen, not the pane. (Rejected in #710 for exactly this reason.)

```vue
<template>
  <!-- @container makes the @-variants below resolve against THIS element's width -->
  <div class="@container h-full overflow-auto">
    <div class="grid grid-cols-1 @md:grid-cols-2 gap-4">…</div>
  </div>
</template>
```

Reference implementations in `packages/crouton-core/app/components/`:
`LayoutSpikeList.vue`, `LayoutSpikeForm.vue`, `LayoutSpikeStats.vue` (each uses
`@container`; throwaway spike blocks, but the responsiveness pattern is the model).

## Declare the sizing contract

On the block's `CroutonLayoutBlockDefinition` (in the package's `app.config.ts`
`croutonLayoutBlocks`), declare what it needs. All optional; undeclared ⇒ fully
fluid (`minWidth` 0).

| Field | Use it for |
|-------|------------|
| `minWidth` | **The viability floor (px).** Below this the block breaks → the pane refuses to shrink past it, and the viability check flags it. Set it to the smallest width where the block is still legible after its narrowest container-query state kicks in. |
| `minHeight` | Smallest usable height (px). |
| `maxWidth` | Don't stretch past this (px). |
| `defaultSize` | Preferred size (% of its pane group) when first placed. |
| `resize` | `'free'` (default) · `'fixed'` · `'aspect'`. |
| `aspect` | width/height ratio when `resize: 'aspect'`. |
| `density` | `'compact' \| 'comfortable' \| 'spacious'` hint for the block's own layout. |

Pick `minWidth` *after* you've authored the narrowest container state — it's the
point past which even the collapsed layout stops working, not the desktop width.

## List playbook

- **Column priority + collapse order:** decide which columns drop first as the
  container narrows; keep the identifying column (title) longest.
- **Table → cards threshold:** below a container width, switch a table to stacked
  cards (`@container` variant) — never a broken horizontal scrollbar.
- **Min column widths** so columns don't crush; **sticky header** on scroll.
- **Empty / loading / error states** all sized for the pane (no fixed-px blocks
  that overflow a narrow column).

## Form playbook

- **Two-column ⇄ single-column** at a container threshold (`@md:grid-cols-2` →
  `grid-cols-1`), not a viewport one.
- **Label placement:** top labels survive narrow panes better than left labels.
- **Field grouping** stays intact across the collapse; **primary action** stays
  reachable (sticky footer or end of flow), full-width when narrow.

## General rules

- No fixed pixel widths that can overflow a pane — use intrinsic / fluid sizing.
- **Contain overflow:** `overflow-auto` on the scroll root; the block fills its
  pane (`h-full w-full`) and scrolls internally rather than pushing the pane.
- Honour your own `minWidth` — the declared floor and the narrowest CSS state
  should agree (don't declare 240 if the layout visibly breaks at 300).
- SSR-safe: no `window`/measurement on first render (container queries are pure
  CSS, so they work in SSR — that's another reason to prefer them).

## Check your work

1. Drop the block into a wide pane, then drag it narrow — it should reflow
   (columns collapse / table→cards / 2col→1col) via container queries, **not**
   scroll sideways or crush.
2. The pane should refuse to shrink the block below its `minWidth`.
3. Run the viability metric over a layout that puts the block in a too-small
   pane — `useCroutonLayoutBlocks().checkViability(tree, [1280, 768, 375])` (or
   the pure `checkLayoutViability`) should flag it. See `crouton-core` CLAUDE.md.
