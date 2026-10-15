---
name: focus-outline-shape
description: |
  The painted shape of a focus ring is determined by the focused element's own border box, its own `border-radius`, the offset/width pair, and every clip between that box and the screen — not by the component's visual appearance. Use when adding or reviewing `:focus-visible` styles on buttons, cards, rows, links, or list items, and especially when a focus ring looks wrong: corners cut off, ring broken into four straight segments, ring missing on one side, ring completely invisible, ring larger than the visible control, or a wrapped link's ring appearing as two separate rectangles.
---

# Focus Outline Shape

A focus ring is not a component-level decoration. It is a paint operation on **one specific box**, and
four independent inputs decide what lands on screen. Most "the focus ring looks wrong" bugs are not
ring-styling bugs — they are _wrong-box_ bugs.

## The four inputs

1. **Which element is focused.** The ring is drawn around that element's **border box** — content +
   padding + border. `margin` is not part of it. Not the visual card, not the enlarged hit layer, not
   the wrapper.
2. **That element's own `border-radius`.** Modern browsers make `outline` follow `border-radius`
   automatically, and grow the radius with the offset so the ring stays concentric. It reads the
   _focused element's_ radius — never an ancestor's.
3. **`outline-width` + `outline-offset`.** The ring occupies the band
   `[border edge + offset, border edge + offset + width]`. The offset positions the ring's **inner**
   edge; the ring always grows outward from there. So `outline-3 outline-offset-0` sits fully outside,
   and only `outline-3 -outline-offset-3` sits fully inside.
4. **Every clip between that box and the screen.** Ancestor `overflow: hidden/clip/auto/scroll`
   (rounded or not), `clip-path`, and masks all cut the ring. The ring is painted last but it is not
   painted above the clip.

Decide input 1 first. Then 2-4 are mechanical.

## Rule 1 — Put focus on the element you want the ring around

The classic broken card: a rounded card clips its content, and the focusable thing is an inner box
that fills the card. The inner box has no radius, so its ring is a **sharp-cornered rectangle**, and
the parent's rounded clip removes exactly the four corner arcs. What survives is four straight
segments with gaps at the corners.

```tsx
// ❌ focus target is a square inner box inside a rounded clipper
<article className="relative overflow-hidden rounded-3xl">
  <button className="absolute inset-0 focus-visible:outline-2 focus-visible:-outline-offset-1" />
  {children}
</article>

// ✅ the focusable element IS the rounded card
<button className="overflow-hidden rounded-3xl focus-visible:outline-2 focus-visible:outline-offset-2">
  {children}
</button>

// ✅ or keep the real control inside and lift the ring to the card
<article className="overflow-hidden rounded-3xl has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2">
  <button className="focus-visible:outline-none">{children}</button>
</article>
```

An element's own `overflow: hidden` does **not** clip its own outline, so the card can clip content
and still draw a clean ring around itself. That is what makes the `:has(:focus-visible)` lift work.

When lifting, keep the semantics honest: the real interactive element stays a real `button`/`a`, only
the ring moves. Do not add `tabindex` to a wrapper to make the geometry easier.

## Rule 2 — The ring reads the focused element's own radius

```tsx
// ❌ square ring inside a rounded card
<div className="absolute inset-0 focus-visible:outline-2" />

// ✅ ring picks up the parent's curve
<div className="absolute inset-0 rounded-[inherit] focus-visible:outline-2 focus-visible:-outline-offset-2" />
```

`rounded-[inherit]` is the right default for any filling child that draws a ring, an inset stroke, or
a hover overlay. Do not hand-copy the parent's token (`rounded-3xl` on both) — it drifts the moment
the card's radius changes, and it is wrong anyway when the child is inset (see
`nested-corner-geometry` for the `r_inner = r_outer − inset` rule).

Do not hand-tune the ring's radius for the offset either. The browser already keeps the ring
concentric: a `rounded-3xl` (24px) card with `outline-offset-2` paints a 26px ring, with
`-outline-offset-8` paints a 16px ring.

## Rule 3 — Spend the offset with the clip in mind

Two directions, two different requirements:

| Intent            | Utilities                     | Requirement                                   |
| ----------------- | ----------------------------- | --------------------------------------------- |
| Ring outside      | `outline-2 outline-offset-2`  | 4px of unclipped space outside the border box |
| Ring flush inside | `outline-2 -outline-offset-2` | nothing — always safe inside a clipper        |
| Ring inset by 2px | `outline-2 -outline-offset-4` | nothing                                       |

Because the offset positions the ring's inner edge, a "slightly inset" ring like
`outline-3 -outline-offset-1` still puts 2 of its 3 pixels _outside_ the border box — inside a clipper
you get a 1px sliver and it reads as a thin, dim, broken line rather than a focus ring. Match the
numbers (`-outline-offset-N` with `outline-N`) whenever the ring must live inside a clip.

## Rule 4 — Symptom decoder for clipped rings

| What you see                                   | Cause                                                                                                                            |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Four straight segments, corners missing        | square-cornered ring + rounded ancestor clip (`overflow-hidden` + radius)                                                        |
| Ring missing on one edge only                  | scroll container edge — the ring is outside the scrollport on that side                                                          |
| Ring completely invisible                      | outset ring entirely outside the clip: `ring-*` (box-shadow) on a filling child, or a positive `outline-offset` inside a clipper |
| Ring invisible even with no ancestor clip      | `clip-path` on the focused element itself — it clips the element's own outline                                                   |
| Ring bigger / rounder than the visible control | wrong box: padding or a wrapper is carrying the focus, not the visual box                                                        |

Two of those deserve emphasis:

- **`clip-path` clips the element's own outline; `overflow: hidden` does not.** A `clip-path`-based
  rounded card silently kills its own focus ring. Use `border-radius` + `overflow: hidden` instead, or
  move the ring to an unclipped ancestor.
- **Tailwind's `ring-*` compiles to an outset `box-shadow`,** which lives entirely outside the border
  box. Inside a clipper it does not degrade into a sliver — it disappears completely. `outline` at
  least fails visibly, which is why it is the better default for focus.

### Scroll containers

The overflow clip edge is the **padding box**, so vertical padding on the scroller buys room for an
outward ring on the top/bottom edges — but a full-width row still loses its left/right sides. Either
inset the ring, or pad both axes.

```tsx
// ❌ first row's ring is clipped by the scrollport
<div className="h-40 overflow-auto">
  <button className="w-full focus-visible:outline-2 focus-visible:outline-offset-2" />
</div>

// ✅ inset ring — nothing to clip
<div className="h-40 overflow-auto">
  <button className="w-full rounded-md focus-visible:outline-2 focus-visible:-outline-offset-2" />
</div>

// ✅ or give the scrollport room on both axes and inset the rows
<div className="h-40 overflow-auto p-1.5">
  <button className="w-full rounded-md focus-visible:outline-2 focus-visible:outline-offset-2" />
</div>
```

If you genuinely need an outward ring inside a clipping (non-scrolling) box, `overflow: clip` plus
`overflow-clip-margin` extends the clip region without giving up the clip:

```tsx
<div className="overflow-clip rounded-3xl [overflow-clip-margin:6px]">…</div>;
```

This works only with `overflow: clip` — it has no effect on `hidden`, `auto`, or `scroll`.

## Rule 5 — The ring is sized by the focus box, not the hit box

Enlarging a control with padding enlarges the ring. Enlarging it with an absolutely positioned hit
layer does not — the focus box stays exactly the designed visual size.

```tsx
// ❌ 24px icon, 40px ring
<button className="size-6 p-2 focus-visible:outline-2" />

// ✅ 24px icon, 24px ring, 40px hit area
<button className="relative size-6 rounded-md focus-visible:outline-2 focus-visible:outline-offset-2">
  <span className="absolute -inset-2" />
  <Icon className="relative size-4" />
</button>
```

This is the geometric half of `seamless-hit-target` / `expanded-touch-target`: the visual box, the
focus box, and the hit box are three separate decisions, and only the focus box shapes the ring.

## Rule 6 — Inline elements fragment; block-level ones do not

A non-replaced inline element that wraps across lines is several boxes, and the ring is painted **per
fragment** — a wrapped link shows two separate rectangles, not one connected shape.
`box-decoration-break: clone` does not merge them (it governs border/padding/background, not outline).

This is correct, expected behaviour for prose links — leave it alone. Do not "fix" it with
`inline-block`, which stops the link from wrapping mid-phrase and rewrites the paragraph's line
breaks. Reach for `inline-flex` only for things that must never break in the first place:

```tsx
// ❌ turning a prose link into a block changes text flow to fix a cosmetic ring
<a className="inline-block focus-visible:outline-2">a long link inside a paragraph</a>

// ✅ prose link: accept per-fragment rings
<a className="focus-visible:outline-2 focus-visible:outline-offset-2">a long link inside a paragraph</a>

// ✅ chip / badge / tag: never wraps, so one ring by construction
<a className="inline-flex items-center rounded-full px-3 focus-visible:outline-2 focus-visible:outline-offset-2">
  <Icon /> label
</a>
```

## Rule 7 — Transforms scale the ring, including its stroke

The outline is painted in the focused element's local coordinate space, so `scale-150` renders a 2px
ring at 3px and pushes the offset out proportionally. If a control scales on hover/press, scale an
inner layer instead of the focusable element, so the ring keeps its designed weight:

```tsx
// ❌ ring thickness animates with the button
<button className="transition-transform hover:scale-105 focus-visible:outline-2" />

// ✅ visual layer scales, focus box is stable
<button className="group relative focus-visible:outline-2 focus-visible:outline-offset-2">
  <span className="block transition-transform group-hover:scale-105">{children}</span>
</button>
```

## Diagnostic recipe

1. Find the element that actually has focus — `document.activeElement`, or DevTools' `:focus-visible`
   force-state. Compare its box to the box you expected the ring around.
2. Read that element's `border-radius`. Square ring on a rounded component means you are on the wrong
   box or missing `rounded-[inherit]`.
3. Walk every ancestor up to the root looking for `overflow` other than `visible`, `clip-path`, or
   `mask`. Also check the element itself for `clip-path`.
4. Compare `outline-width` against `outline-offset`. If `offset > -width`, part of the ring is outside
   the border box and needs unclipped space.
5. Toggle to `-outline-offset-{width}` as a probe. If the ring becomes whole, it was a clipping
   problem; if it stays broken, it is a radius or wrong-box problem.

## Checklist

- The focusable element is the element whose shape you want the ring to have.
- Filling children that draw rings use `rounded-[inherit]`, not a copied radius token.
- Inside any clipper, ring width and negative offset match (`outline-2 -outline-offset-2`).
- Hit areas are expanded with an absolute layer, never with padding on the focus target.
- No `clip-path` on anything that needs to show a focus ring.
- Rows inside scroll containers use inset rings, or the scroller pads both axes.
- Scaling animations live on an inner layer, not on the focus target.
- `outline` is the default focus technique; `box-shadow`/`ring-*` only where an outset stroke is
  guaranteed unclipped space.

## Anti-patterns

- **Styling the ring before choosing the focus target** — tuning radius and offset on a box that was
  never the right box.
- **`focus-visible:outline-none` on the real control plus a decorative ring elsewhere with no
  `:has(:focus-visible)` link** — removes the indicator for keyboard users when the decorative layer
  is clipped or conditionally rendered.
- **Copying the parent's radius token onto an inset child** — drifts on redesign and ignores
  concentric geometry.
- **Slightly-negative offsets on thick rings** (`outline-4 -outline-offset-1`) inside a clipper —
  leaves a 1px sliver that reads as a rendering artifact.
- **`clip-path` for rounded corners on interactive surfaces** — kills the element's own outline.
- **Padding as a touch-target fix on a focusable element** — silently inflates the ring.
- **`inline-block` on prose links to unify a fragmented ring** — changes line breaking to fix
  something that was never broken.

## Verified behaviour

Measured in Chrome 153 (`outline: 3px`/`8px solid`, screenshots compared per case):

- Ring band is `[edge + offset, edge + offset + width]`: an 8px ring at `outline-offset: -2px` inside a
  clipping parent leaves a 2px sliver; at `-8px` all 8px survive, flush inside.
- Ring radius is `border-radius + outline-offset`: a `border-radius: 24px` box with
  `outline-offset: 8px` paints a path that coincides exactly with a reference box inset by -9px with
  `border-radius: 32px`.
- Square-cornered ring inside `overflow: hidden` + `border-radius: 24px` → four straight segments,
  four corner gaps. Removing the parent's `overflow` restores the full square ring; adding
  `border-radius: inherit` to the child restores the full rounded ring.
- Outward ring (`outline-offset: 2px`) on a child filling an `overflow: hidden` rounded parent →
  entirely invisible, even with `border-radius: inherit`. Same setup with
  `overflow: clip; overflow-clip-margin: 6px` → fully visible.
- Outset `box-shadow` ring on a filling child inside a rounded clipper → entirely invisible.
- `clip-path: inset(0 round 24px)` on the focused element → its own outline is clipped away.
  `overflow: hidden` on the focused element → its own outline is unaffected.
- Scroll container with unpadded rows: the first row's outward ring loses its top edge; vertical
  padding on the scroller restores top/bottom but not left/right for full-width rows.
- Wrapped inline link → two separate rectangles; unchanged by `box-decoration-break: clone`.
- `::after`-style hit layer at `inset: -8px` on a 24px button → ring stays 24px; `padding: 8px`
  instead → ring becomes 40px.
- `transform: scale(2)` on the focused element → ring geometry and stroke width both double.
