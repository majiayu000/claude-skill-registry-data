---
name: avoid-layout-magic-numbers
description: Avoid unexplained hard-coded widths, heights, and offsets in UI layouts. Use when implementing or reviewing fixed dimensions, pixel offsets, calc() subtractions, or components that only work at one container size. Prefer intrinsic sizing and parent-owned constraints; allow fixed dimensions when they are an intentional component, media, or interaction contract.
---

# Avoid Layout Magic Numbers

## Rule

Default to content-driven size and structural layout relationships. A fixed value is justified only
when it represents an explicit design token or component contract—not when it compensates for the
current content, parent size, or position of another element.

The problem is not the literal number. It is the hidden dependency.

## Default Ownership

| Component kind                    | Inline size (width)                                                | Block size (height)                                       |
| --------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------- |
| Button and other leaf controls    | Fit content with inline padding; parent opts into fill             | Content and padding, or a deliberate control-height token |
| Card, panel, section, list        | Supplied by the parent, grid, flex context, or Storybook decorator | Fit content                                               |
| Page or layout container          | Available space with deliberate min/max bounds                     | Content or an explicit viewport/layout contract           |
| Icon, avatar, media frame, canvas | Component or media contract                                        | Component or aspect-ratio contract                        |

These are defaults, not universal bans. A wrapping button may need adaptive height; a single-line
control family may need a fixed height. A card should not own `300px × 200px` merely because one
mockup happened to use that frame.

## Decision Order

Before adding a fixed width, height, or offset:

1. Identify who owns that axis: the component, its parent, or its content.
2. Express the relationship with normal flow, Flexbox, Grid, `gap`, padding, alignment,
   `aspect-ratio`, or min/max constraints.
3. If a fixed value remains, tie it to a named token, prop, variant, media ratio, or documented
   interaction requirement.
4. Keep siblings independent. Do not position one element with a number derived from another
   element's current dimensions.

Prefer:

```tsx
// The host owns the available width; the card owns its content and internal spacing.
<div className="w-full max-w-md">
  <Card className="p-4" />
</div>

// A single-line control has a deliberate height contract and content-driven width.
<button className="h-10 px-4">{label}</button>
```

Avoid:

```tsx
// These values silently assume one host, one content length, and one font scale.
<Card className="h-[200px] w-[300px]" />

// 237px hides coordination with unrelated header, toolbar, and footer dimensions.
<main className="h-[calc(100vh-237px)]" />
```

Use an explicit layout relationship instead of the subtraction, for example a grid with
`grid-template-rows: auto minmax(0, 1fr) auto`.

## Legitimate Fixed Values

Fixed dimensions are appropriate when changing them would violate a real contract:

- design-system control heights and touch targets;
- icons, avatars, thumbnails, aspect-ratio frames, charts, or drawing canvases;
- overlays, virtualized viewports, drag bounds, or animation geometry that requires a known box;
- exact visual fixtures whose purpose is to test a specific size.

Even then, prefer tokens or component variants over scattered literals, and define overflow,
localization, font scaling, and narrow-container behavior.

## Review Test

Ask: **what breaks if this number changes, and where is that relationship expressed?**

If the answer depends on another element, one sample string, one viewport, or visual coincidence,
replace the number with a layout relationship. If the answer is a clear component or design
contract, keep it and make that contract visible in the API or token name.
