---
name: keep-elements-in-flow
description: |
  Keep UI elements in normal flow for resilient, content-driven layouts. Use when building or reviewing overlapping cards, preview stacks, localized actions, responsive surfaces, corner badges and other pinned overlays, or code with many fixed dimensions and hand-written offsets on absolutely positioned children. Prefer Flexbox, Grid, negative margins, and content-driven sizing; use relative positioning for stacking; and when an element must leave the flow, position a zero-size anchor container instead of writing coordinates on the element itself.
---

# Keep Elements In Flow

## Rule

Keep elements in normal flow whenever their size or position should influence surrounding content.
Use negative margins for in-flow overlap. Use `relative` when stacking needs it, and use `absolute`
only when an element is intentionally independent of the layout and should not reserve space.

This is a default, not an absolute ban on fixed dimensions or absolute positioning.

## Why

In-flow layouts let the browser perform the layout work:

- Parent height follows content automatically.
- Siblings move when text wraps or content changes.
- Buttons can grow for larger fonts and translated labels.
- Flexbox and Grid preserve alignment across container widths.
- DevTools exposes a clear box model instead of a collection of unrelated coordinates.

An absolute child is removed from normal flow. Its parent and siblings behave as if it does not
exist, so the author must manually reserve space, maintain offsets, and handle content growth.

## Minimal Comparison

Avoid turning a content-driven surface into a coordinate canvas:

```tsx
// Brittle: the parent height, preview position, and action width are all manually coordinated.
<section className="relative h-64">
  <header className="absolute inset-x-0 top-5 text-center">...</header>
  <div className="absolute inset-x-0 top-20 flex justify-center">...</div>
  <button className="absolute bottom-5 left-1/2 w-28 -translate-x-1/2">Action</button>
</section>;
```

Let content establish the geometry and use layout-aware overlap:

```tsx
<section className="relative py-5">
  <header className="text-center">...</header>

  <div className="flex items-center justify-center pt-8">
    <Preview className="z-10 -mr-3" />
    <Preview className="z-20" />
    <Preview className="z-30 -ml-3" />
  </div>

  <button className="relative z-40 mx-auto -mt-7 block h-7 px-4">Action</button>

  <button className="absolute top-3 right-3" aria-label="Dismiss">
    <IconX />
  </button>
</section>;
```

The action remains in flow. Its negative top margin creates the overlap, its fixed height preserves
the control contract, and horizontal padding lets its width adapt to text. Its `relative` position
only enables explicit stacking. The dismiss button stays absolute because it is a true corner
overlay and should not create a separate layout row.

## What Participates In Layout

| Technique                           | Reserves or changes layout space | Typical use                                        |
| ----------------------------------- | -------------------------------- | -------------------------------------------------- |
| Normal flow, Flexbox, Grid          | Yes                              | Primary composition                                |
| Width, height, padding, gap, margin | Yes                              | Box sizing and spacing                             |
| Negative margin                     | Yes                              | Pull in-flow elements into overlap                 |
| CSS `zoom`                          | Yes                              | Scale previews when scaled size must affect layout |
| `position: relative`                | Keeps the original box in flow   | Stacking and positioned containing blocks          |
| `position: absolute` or `fixed`     | No                               | True overlays and viewport layers                  |
| `transform`                         | No                               | Rotation, animation, and visual-only movement      |

`position: relative` preserves the element's original layout slot. Use it for stacking or as the
containing block for an absolute child, not to create layout overlap. A relative `top` or `left`
offset changes only where the element paints, so use margins or layout primitives when siblings must
react to the movement.

## Fixed And Adaptive Dimensions

Choose fixed dimensions only when they are part of the component contract.

- Buttons usually use a fixed `h-*` and horizontal `px-*`; width follows content.
- Text containers usually adapt in both axes within deliberate min/max bounds.
- Icons, avatars, media frames, and calibrated preview tiles may use fixed dimensions.
- Fixed button width is appropriate only when equal-width controls are a real requirement.
- Adaptive button height is an exception for intentionally wrapping or multi-line actions.

Account for larger font settings, localization, optional content, and narrow containers before
writing a fixed `w-*` or parent `h-*`.

## When Absolute Is Correct

Use absolute positioning when the element should not influence surrounding geometry:

- A dismiss button pinned to a card corner.
- A badge attached to another element.
- A tooltip, popover, menu, or modal layer.
- Decorative artwork or a non-interactive visual layer.
- A viewport-fixed control.

Give the containing block `relative`, and reserve any required safe area in the in-flow content so
the overlay does not cover text or controls.

## Anchor Containers

Leaving the flow does not mean writing coordinates on the element itself. Position an absolute
zero-size **anchor** at the reference point and let its child lay out from there in flow.

```tsx
// Brittle: the offsets are hand-derived from the badge's current size.
<div className="relative">
  <Card />
  <Badge className="absolute -top-1.5 -right-2.5" />
</div>;
```

```tsx
// Anchored: the anchor marks the corner; the badge stays centered on it at any size.
<div className="relative">
  <Card />
  <div className="absolute top-0 right-0 flex size-0 items-center justify-center">
    <Badge className="shrink-0 whitespace-nowrap" />
  </div>
</div>;
```

A `size-0` box has no area, so it reserves no space and its own center is the anchor point.
`items-center justify-center` centers the overflowing child on that point, so the badge can change
size, gain a second digit, or become an icon without any offset being recomputed. Tune placement by
moving the anchor, never the child.

## An Absolute Container Is Still A Layout Container

Choose how many axes the anchor measures:

| Anchor                                             | Provides                                                       |
| -------------------------------------------------- | -------------------------------------------------------------- |
| `absolute top-0 right-0 size-0` + flex centering   | A single point to align on                                     |
| `absolute inset-y-0 right-0 w-0 flex items-center` | An edge column: height from the parent, `gap` between children |
| `absolute inset-x-0 top-0 h-0 flex justify-center` | An edge row: width from the parent                             |
| `absolute inset-0`                                 | A full region with normal alignment and padding                |

A zero axis means "measure nothing, just give me this line or point". A stretched axis borrows the
parent's size, so the anchor can align, center, and distribute children like any flex container.
Either way the wrapper carries the geometry and the content keeps its own intrinsic size.

An in-flow wrapper can make the same per-axis choice — see `zero-height-side-element`, where a
`flex h-0 items-center` wrapper measures zero in the block axis while remaining a normal flex child
in the inline axis. Both are the same mechanism aimed at different questions:

- Does the element sit _beside_ its siblings and own a slot in the row — a trailing toggle, action
  button, or status badge? It has to reserve inline space so long labels truncate instead of running
  underneath it. Use an in-flow wrapper and zero out only the axis you want to opt out of.
- Does the element sit _on_ the thing it annotates — a notification count, unread dot, or corner
  dismiss button? It should reserve nothing and may hang outside its target's box. Use an absolute
  anchor.

The element's type is a hint, not the rule: a badge in a settings row is a trailing sibling, while
the same badge on an avatar is an overlay. Decide by whether siblings must move for it.

Constraints to check: the containing block needs `relative`; children of a zero-size flex anchor
need `shrink-0` (and `whitespace-nowrap` for text) because the container's inline size is `0`; and an
ancestor with `overflow-hidden` or `overflow-clip` will cut off anything painting outside the box.

## Review Questions

1. Should this element reserve space in its parent?
2. Should siblings move when its content grows or wraps?
3. Can Flexbox, Grid, `gap`, `mx-auto`, or padding express the relationship?
4. Can a negative margin create the overlap while preserving flow?
5. Is a fixed width or height a real component contract or an unexamined coordinate?
6. Is the absolute element a true overlay that should remain independent of content?
7. If it must be out of flow, can a zero-size anchor own the position so the child only owns its own
   size?

If the first two answers are yes, keep the element in flow.
