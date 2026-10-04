---
name: two-colour-focus-ring
description: >-
  Use when a keyboard focus indicator disappears on some states — a ring invisible on a selected or
  filled element but fine at rest, a ring clipped by a scrolling container, or a focus style being
  designed for a control that can sit on more than one background fill.
---

# Two-colour focus ring

## Profile keys consumed

- `framework.ui`
- `architecture.source_root`
- `capabilities.accessibility_audit`
- `capabilities.visual_testing`
- `make.a11y`
- `make.test_visual`

## Overview

A single-colour focus ring vanishes whenever the element under it happens to be that colour — a dark
ring on a dark selected disc, a white ring on a white surface. Stacking a light layer and a dark
layer in one `box-shadow` guarantees that at least one layer contrasts with whatever is underneath.

## When to use

- A focusable element renders on two or more fills (selected versus rest, brand fill versus surface,
  light column versus dark column).
- The focus indicator is visible in one state of a component and gone in another.
- A focus ring is clipped because the element lives inside an `overflow` container.
- An accessibility review flags WCAG 2.4.7 Focus Visible (AA) or 2.4.13 Focus Appearance (AAA) on a
  component with variable fills.
- Not for: controls with a single, fixed background — one ring against a known fill is simpler and
  correct there.

## Verification gate

The pattern itself is unconditional — it is CSS in the styling layer named by `framework.ui`. Its
two verification steps are gated, and only by a capability flag. Run the accessibility check
through the target mapped by `make.a11y`; when that key is `null` the plugin substitutes its
bundled a11y lane, so the check still runs — a null mapping is never a reason to skip it. Skip
that step with a recorded note only when `capabilities.accessibility_audit` is `false`. Re-record
the affected snapshots through the target mapped by `make.test_visual`, and skip that step with a
recorded note when `capabilities.visual_testing` is `false`.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — the same MUI plus Emotion `'&:focus-visible'` styling in module and component
  `styles.ts` files, but every ring today is a single `outline` rule; palette tokens live in the
  styles directory under the source root (a `colors.ts` plus a `theme.ts`), so both layers have to
  be added.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the principle
  transfers, but the shared MUI app-theme component carries no focus-ring overrides today, so the
  tokens have to be introduced with the ring.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  single-colour rings are the default in component `styles.ts` files, with the two-layer form used
  where fills vary; tokens come from the library's colour-theme component.

## Core pattern

Always kill the native outline in the same rule that paints the ring, and build both layers from
palette tokens rather than literal hex.

```ts
// Outset: the element is not inside a clipping container.
// Inner light layer contrasts with a saturated or dark fill; outer dark layer with the page.
const FOCUS_RING_INNER: string = `inset 0 0 0 2px ${palette.white.main}`;
const FOCUS_RING_OUTER: string = `0 0 0 2px ${palette.darkPrimary.main}`;
const FOCUS_RING: string = `${FOCUS_RING_INNER}, ${FOCUS_RING_OUTER}`;

// Applied where the ring belongs, with the browser default suppressed.
'&:focus-visible': { outline: 'none', boxShadow: FOCUS_RING },
```

When the element sits in a scrolling container that would clip an outset ring, nest both layers
inward at different spreads. The first shadow in the list paints on top, so ordering decides which
colour is the outer band:

```ts
// Inset: dark paints 0-2px over white at 2-4px, so the ring reads on light and dark alike.
const FOCUS_RING_OUTER: string = `inset 0 0 0 2px ${palette.darkPrimary.main}`;
const FOCUS_RING_INNER: string = `inset 0 0 0 4px ${palette.white.main}`;
export const FOCUS_RING: string = `${FOCUS_RING_OUTER}, ${FOCUS_RING_INNER}`;
```

An inset ring eats into the element's own padding, so reserve room for the full spread — the padding
must be wide enough that the ring never lands on a glyph, a photo, or text.

## Secondary indicators

A status marker such as "today" can share the element as a thinner inset ring
(`inset 0 0 0 1px ${palette.primary.main}`), rendered only while the element is neither focused nor
selected, so the thicker focus ring always wins visual priority.

## Common mistakes

- Hardcoding hex values instead of palette tokens, so a theme change breaks the contrast that
  justified the pattern.
- Removing the native outline without painting a replacement in the same rule, which leaves a state
  with no indicator at all.
- Using an outset ring inside a scrolling column, where it is clipped and the element looks
  unfocused at the container edge.
- Reversing the shadow order and expecting the same appearance — the first entry paints on top.
- Applying the two-layer ring to every control, which adds weight where a single ring already
  contrasts.
- Verifying only the rest state; check the ring in the selected, hovered, and disabled fills too.
- Reading a `null` `make.a11y` as permission to skip the accessibility check — that mapping selects
  the bundled a11y lane, so run it and gate only on `capabilities.accessibility_audit`.
