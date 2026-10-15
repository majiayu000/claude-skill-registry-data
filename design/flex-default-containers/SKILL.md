---
name: flex-default-containers
description: >-
  Fix wrapper elements whose default block layout puts inline children in an inline formatting
  context and leaks line-height leading into the box. Use when a card header, label strip, status row,
  or other wrapper around spans, badges, icons, or SVGs renders taller than padding plus font size;
  when an icon or label looks vertically off-center; or when someone changes a child to display block
  to compensate. Make the wrapper's flex or grid layout explicit even when the user does not mention
  baselines, leading, or inline formatting contexts.
---

# Flex-Default Containers

## Rule

Any element whose job is to **hold and arrange children** declares its `display` explicitly — `flex` for one-axis rows/columns, `grid` for two-axis layouts. Never let a layout wrapper fall back to the browser-default `block` value, because `block` leaves the wrapper in inline formatting mode for its children, which silently injects line-height leading around inline-level descendants (`<span>`, `<a>`, `<img>`, `<svg>`, inline-block buttons, etc.).

Inline primitives themselves (`<span>`, `<Badge>`, `<Eyebrow>`, `<Kbd>`, `<Dot>`) stay inline so they remain composable inside prose. The container is what changes.

## Why this matters

Three CSS facts compound to produce a confusing class of bugs:

1. **Inline-level elements live in an inline formatting context (IFC).** A `<span>` inside a default-block `<div>` participates in the parent's IFC.
2. **An IFC arranges children into line boxes, not into a content box.** Line box height is `line-height`, not `font-size`. With a page default `line-height: 1.5` and a `font-size: 9px` label, the line box is ~14px tall but the glyphs only paint ~9px. The remainder is **leading**, distributed above the cap-height and below the baseline.
3. **Leading is real height.** It pushes the parent's content box down. Visually this reads as "the title is too low" or "this strip has too much air on top", even though every padding value you wrote is honored.

Switching the parent to `display: flex`:

- The child becomes a **flex item**, not an inline-level box. It no longer participates in inline formatting.
- The flex container sizes itself to its items' margin-boxes, ignoring `line-height` on inline content.
- The leading collapses away. Visual height becomes exactly `font-size + padding`.
- You get `gap` for free, replacing margin-based spacing between siblings.

`align-items: center` (or the default `stretch`, when there is one row) then centers the child inside whatever vertical padding the container actually has, matching every designer's mental model.

### Why even the IFC workaround doesn't visually centre

Even if you shrink the strut (`leading-none` on the parent), uppercase ink doesn't land at the geometric centre. The cause isn't ascent/descent asymmetry per se — it's that **CSS sizes inline boxes by the font's design metrics (em + leading) but visible ink (cap-height, x-height) is positioned within that box wherever the font designer chose** — no mechanical relationship to the box's geometric centre.

For the macOS system font (`-apple-system` → SFNS.ttf), browser-used hhea metrics are:

- A ≈ `0.967 × font-size`
- D ≈ `0.211 × font-size`
- cap-height ≈ `0.705 × font-size`
- A + D ≈ `1.178 × font-size` (so `line-height: normal` actually computes to ~1.18; `leading-none` is ~18% tighter than the font's natural line-height)

Working through the geometry for any line-height L:

- Baseline within an inline box of height L = `A + (L − A − D)/2 = (A − D + L)/2 ≈ L/2 + 0.378`
- Cap centre = baseline − cap-height/2 = `(L − cap-height + A − D)/2`
- Offset of cap centre from box geometric centre = `(A − D − cap-height)/2 = (0.967 − 0.211 − 0.705)/2 ≈ +0.026 × font-size`

So in SFNS.ttf, **the cap sits ~0.026 × font-size BELOW the geometric centre of any inline box, regardless of `line-height`**. That residual is purely a property of where the font designer placed the cap inside the em — there is no CSS knob (short of `text-box-trim`) that removes it.

For 9px text the residual is 0.23 px (invisible). For 32px it's 0.83 px (visible if you're looking). For different fonts the constant differs entirely — a font with smaller A or larger cap-height could land the cap _above_ centre, or much further from it.

That mismatch is exactly what `text-box-trim: trim-both` (CSS Inline Layout L3) is designed to remove: it makes the inline box's height equal the **ink** height (cap-height or x-height, per `text-box-edge`), so geometric centring lines up with what you see. Support as of late 2026: **Chrome 133+, Safari 18.2+, no Firefox**.

Until `text-box-trim` is universally available, `display: flex` plus `align-items: center` plus `leading-none` on the inline child is the **closest practical approximation**:

- Flex centres the flex item's _margin box_ (geometric, not baseline-relative).
- `leading-none` on the child makes the child's content box equal `font-size` exactly.
- For UI fonts whose designer placed the cap near the em centre (SF Pro, Inter, Roboto, system-ui), this gives sub-pixel offset at normal sizes.
- For other fonts the residual will be larger — flex isn't a font-agnostic guarantee, just a useful approximation.

When the residual currently matters (large display text, monospace fonts, brand serifs), the pre-`text-box-trim` workarounds are `@font-face { ascent-override / descent-override / line-gap-override }` (Chrome 87+ / Safari 17+ / Firefox 89+), or `font-size-adjust` for cross-font x-height matching. Both target the metric calculations directly.

Matching the parent's font metrics to the child's (`text-[9px] leading-none` on the parent) does also work geometrically — it produces the same residual as flex — but hard-couples the wrapper to one child's font-size and breaks the moment any other content lands inside. Don't.

A subtle trap with "leading-none on the parent": **it's not enough on its own**. `leading-none` shrinks line-height from default (~1.5) to 1, but the strut height is still `parent-font-size × line-height`. If the parent's font-size is larger than the child's (the common case — a 14 px wrapper around a 9 px Eyebrow), the strut is still 14 px tall and dominates the 9 px child. You'd need `text-[9px] leading-none` on the parent — matching font-size and line-height — to actually collapse the line box to the child. See [references/sf-pro-metrics.md](references/sf-pro-metrics.md) for measured numbers showing leading-none-on-parent producing the exact same off-centre offset as the original default-block bug.

## Pattern A — Layout wrapper around an inline primitive

The shape that triggers the bug most often: a styled strip / pill / row with a single inline child.

```tsx
// ❌ Default-block wrapper — `<span>` is inline, line-height leading pads the strip
<div className="border-b bg-surface-3 px-4 py-2">
  <Eyebrow tone="subtle">Preview</Eyebrow>
</div>

// ✅ Wrapper declares flex — leading collapses, padding is honest
<div className="flex items-center border-b bg-surface-3 px-4 py-2">
  <Eyebrow tone="subtle">Preview</Eyebrow>
</div>
```

This applies even when there is only one child. The point isn't multi-child layout; it's exiting inline formatting.

## Pattern B — `leading-none` on the inline primitive (only useful inside flex/grid)

A common assumption is that adding `leading-none` to an inline primitive (`<Eyebrow>`, `<Badge>`, etc.) "collapses its line box to font-size" and so protects the primitive against a misauthored default-block wrapper. **This is wrong.** The line box's height is the maximum of:

1. The **strut** — a phantom inline derived from the IFC-establishing block's own `font-size × line-height`. The strut ignores the child's metrics entirely.
2. Each inline element's own contribution.

If the primitive lives in a default-block parent with `line-height: 1.5` (Tailwind preflight sets `html` to `1.5`), the strut is `parent-font-size × 1.5` — taller than a 9px Eyebrow no matter what its own `line-height` is. `leading-none` on the inline primitive doesn't shrink the strut, doesn't shrink the line box, and doesn't fix the gap.

What `leading-none` on the primitive _does_ protect against: **once the primitive lives in a flex or grid container**, there is no strut, and the flex item's cross-axis size is exactly its content box. Without `leading-none`, a 9px Eyebrow inheriting `line-height: 1.5` would have a 14px content box and re-introduce ~5px of unwanted height into the flex container. `leading-none` keeps the flex item exactly font-size tall.

So `leading-none` on the primitive is real defense in depth, but for a different threat than people usually think:

```tsx
// packages/ui/components/eyebrow.tsx
const eyebrowVariants = cva(
  // leading-none keeps Eyebrow's content box = font-size *when used inside
  // a flex/grid container*. It does NOT save Eyebrow from a default-block wrapper
  // — only the parent's display change does.
  "font-mono text-[9px] font-semibold uppercase tracking-wider leading-none",
);
```

There is no "fix it on the primitive alone" path. If the wrapper stays in IFC mode, the strut wins. The container change is non-negotiable.

If for some reason you cannot touch the wrapper (third-party code, CSS-in-JS layering you don't own), the only IFC-level escape hatches that work are on the wrapper itself: `leading-none` on the wrapper, or pairing `text-[X] leading-none` so its strut shrinks to match. Both couple the wrapper to a single child's font metrics — usually worse than just declaring `flex`.

## Pattern C — Row of inline children

Same rule, more obvious benefit: the moment you reach for `margin-right` between inline children, you've already lost. Flex + `gap` is shorter and survives reorder, conditional rendering, and last-child edge cases:

```tsx
// ❌ inline siblings, margin-based spacing, mysterious vertical drift
<div className="px-4 py-2">
  <Dot tone="ok" />
  <span className="ml-2">Online</span>
  <Badge className="ml-2">v2</Badge>
</div>

// ✅ flex row, gap-based spacing, no leading
<div className="flex items-center gap-2 px-4 py-2">
  <Dot tone="ok" />
  <span>Online</span>
  <Badge>v2</Badge>
</div>
```

## Diagnostic checklist

When something looks "a few pixels off" vertically and the padding values clearly add up to a smaller number than the rendered box:

1. Is the offending child inline-level? (`<span>`, `<a>`, `<img>`, `<svg>`, inline-block, an `<Eyebrow>`-style primitive.)
2. Is the parent a layout wrapper without an explicit `display`? (`<div className="px-4 py-2 …">` with no `flex`, `grid`, `block` is the default.)
3. Does the parent's computed `line-height` exceed the child's `font-size`?

If all three are yes, the strut is taller than the child and dominating the line box. The fix is `flex` (or any non-IFC display) on the parent — that's the only change that disposes of the strut. `leading-none` on the inline primitive is useful additionally (it keeps the primitive's intrinsic height tight once it lives in a flex/grid container) but it does **not** rescue the layout while the parent stays in IFC mode.

## Anti-patterns

- **`display: block` on the inline primitive** (`<Eyebrow className="block">`). This patches one site only and breaks composability the moment the primitive is reused inline in prose. The container is what should change.
- **Hard-coded negative margins on the wrapper** (`-mt-1`). Visually compensates the leading instead of removing it; drifts the moment font-size or line-height changes.
- **`vertical-align: top` on the inline child.** Works for `<img>` baseline gap, but doesn't address `line-height` leading on text-bearing inline primitives, and doesn't generalize.
- **`line-height: 0` on the wrapper.** Kills leading but also breaks any wrapped text the wrapper might ever hold. Too invasive.

## When NOT to apply this

- **Inline primitives sitting inside prose** (`<p>This is <Kbd>⌘K</Kbd> to open</p>`). The `<p>` is _meant_ to be a block of inline formatting — that's how prose flows. Keep the primitives inline; don't flex the paragraph.
- **Wrappers that legitimately host a block flow** of mixed paragraphs / headings (article body). Default block is correct there; that's what block-level content rendering means.

The rule targets **layout wrappers** — small structural boxes whose job is to position one or more children. Article bodies and prose containers are not layout wrappers.
