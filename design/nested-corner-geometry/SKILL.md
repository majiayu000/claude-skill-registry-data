---
name: nested-corner-geometry
description: Geometry rule for children placed near the inside edge or corner of a rounded container. Two constraints apply together — (1) the child's gap to each adjacent container edge should be equal (or match the container's content padding on each axis), and (2) when both child and parent are rounded, the child's corner radius should be concentric with the parent's via `r_inner = r_outer − inset_gap`, falling to 0 (square) when the difference is non-positive. Use when designing or reviewing cards / panels / sheets / modals whose interior holds buttons, pills, badges, icons, avatars, or smaller cards in or near a corner — even when the user only says "the button looks off" or "the corner feels weird" without naming geometry.
---

# Nested Corner Geometry

Two geometric rules that apply together whenever a child element sits in or near the corner of a rounded container.

## Rule 1 — Equal insets on adjacent edges

When a child approaches a corner of its parent, its distance to each of the two adjacent parent edges should be **the same value**, not whatever each `mb-*` / `mr-*` happened to be. The eye reads asymmetric insets as "the element is sliding off one side".

If the parent has different content paddings per axis (`px-6 py-4` is common in cards), the equal-inset rule applies to the **inner content frame**, not to the raw container edges. A CTA at the bottom-left should have its left edge aligned with where other text starts (i.e., the left content edge) **and** be the same distance from the bottom content edge as it is from that left content edge.

For a child near just one edge (no corner involvement), the simpler rule applies: the gap to that edge should equal the gap any sibling content has — i.e., match the container's content padding on that axis. Don't invent a new gap value.

## Rule 2 — Concentric corner radii (only when the child is inside the corner-arc region)

The parent's rounded corner is a quarter-circle that occupies a square of side `r_outer` in each corner. This rule only matters when the child sits **inside that quarter-circle's bounding square** — that is, when **both** of the child's insets to the adjacent parent edges are **less than `r_outer`**. Outside that region the parent's corner curve is "off-screen" relative to the child, and the two curves never appear side-by-side, so there is nothing to be concentric with.

Inside the corner-arc region, the child's radius should equal:

```
r_inner = r_outer − inset_gap
```

where `inset_gap` is the perpendicular distance from the child's edge to the nearest parent edge in the relevant axis. This produces visually parallel curves between the two rounded shapes — what the eye recognises as "tucked into the corner cleanly", the same principle that makes nested phone screen masks and OS window chrome feel right.

Edge cases for the math:

- **`r_outer − inset_gap` is small positive (≈ 1-4 px)** — two reasonable readings: pick the exact concentric value, or drop to 0 (square corners) if a barely-rounded curve looks worse than no curve. Don't pick something in between like `rounded-sm` just because it's a Tailwind token — that's the worst of both worlds.
- **`r_outer − inset_gap` ≤ 0, OR child sits outside the corner-arc region** — concentricity stops applying. The child uses the design system's normal radius for that component (typically `rounded-md` / `rounded-lg`), same as it would anywhere else in the app. Don't force square corners just because the math went negative; the math went negative because the rule doesn't apply.

For a circle / pill inside a rounded container, the inscribed circle's radius matters: when the pill's height plus 2×inset_gap exceeds 2×r_outer, the pill's outer arc bulges past the container's inner arc envelope and the corner looks pinched. Either reduce pill height, increase inset, or use a smaller parent radius.

## Pattern A — CTA tucked into a card corner

Card has `rounded-2xl` (`r_outer = 16px`) and `px-6 py-5` (content padding 24 / 20). A "Show more" link sits at the bottom-left, just inside the card.

```tsx
// ❌ Mismatched insets, hardcoded child radius
<article className="rounded-2xl px-6 py-5">
  <h2>News</h2>
  <ul>{items}</ul>
  <button className="mt-3 ml-0 mb-0 rounded-md px-3 py-2">Show one more →</button>
</article>

// ✅ Equal inset on bottom + left edges of content frame; child radius unset (parent's 16 − 12 inset = 4, or just leave square)
<article className="flex flex-col gap-3 rounded-2xl p-3 sm:p-4">
  <div className="px-3 py-2">
    <h2>News</h2>
    <ul>{items}</ul>
  </div>
  <button className="rounded-lg px-3 py-2 text-left">Show one more →</button>
</article>
```

The key shift: stop using the card as the direct positional context and let an inner flex layout carry the rhythm. The CTA's `px-3 py-2` matches the inner content block's padding so visual gaps line up.

## Pattern B — Pill inside a pill-shaped container

A status pill (`rounded-full`, height ~24 px) embedded into a card with `rounded-3xl` (24 px). Inset gap 12 px → `r_inner = 24 − 12 = 12 px`. Use `rounded-xl` (12 px) on the pill, not `rounded-full`, otherwise the pill's tight curve clashes optically with the card's gentler curve.

Exception: when the pill is small relative to the card and far from any corner (e.g., dead-centre), `rounded-full` is fine — concentricity only matters near the corner where the two curves are visible together.

## Pattern C — Avatar / circle near a card corner

A round avatar in the top-right of a card:

```
inset_gap = max(horizontal, vertical) = 16 px
r_outer = 16 px
r_inner-equivalent = 16 − 16 = 0
```

Since the avatar's centre lies further from the corner than the parent's radius, the avatar is fully outside the parent's corner curvature, so concentricity is moot — only Rule 1 (equal insets) applies. If the avatar's diameter is bigger than `2 × inset_gap`, parts of it would clip the parent's corner arc; check whether the avatar's outline ever crosses the rounded corner's curve and back off the inset if so.

## Diagnostic checklist

When something in a corner looks off but you can't pin it:

1. Measure the gap from the child's visible edge to each adjacent inner content edge of the parent. Are they equal?
2. Is the child actually inside the corner-arc region? — that's when both insets are `< r_outer`. If both insets ≥ `r_outer`, the child is in the straight-edge interior and Rule 2 doesn't apply; the child uses the design system's normal radius.
3. If yes (inside the corner-arc region): is `r_inner ≈ r_outer − inset_gap`? If the value is small positive (1-4 px), prefer either the exact value or **zero**, not an in-between Tailwind token.
4. Does the child's own padding match the rhythm of the parent's content padding? A `px-3 py-2` button next to a `px-6` heading creates a visible step the eye reads as misalignment.

## Anti-patterns

- **Mismatched margins at corners** — `mt-3 mb-1` or `ml-4 mr-2` for an element that visually sits near a corner. If the design wants asymmetric, set the asymmetry deliberately at the parent layout level, not via random child margins.
- **Hardcoded child radius when the child is inside the corner-arc region** — `rounded-md` on a button tucked 8 px from the corner of a `rounded-2xl` card. The concentric value would be 8 px (`rounded-lg`). When inside the corner region, scale with the parent.
- **Tiny non-zero child radius when concentric math gives 1-4 px** — snapping to `rounded-sm` because it's a Tailwind token, instead of either committing to the exact concentric value or dropping to zero.
- **Forcing square corners when the child is past the corner region** — if `inset_gap ≥ r_outer`, the rule doesn't apply; the child can keep its design system default. Don't override to square just because the formula "would have" gone negative.
- **`rounded-full` on a pill that's too tall** — if the pill's height ≥ `2 × inset_gap` near a corner, the pill's perfect circle on the cap clips the parent's rounded corner geometry. Use a smaller corner radius matching `r_outer − inset_gap`.

## When NOT to apply

- **Child in the middle of the container**, with no corner or edge nearby — concentricity is moot, equal-insets simplifies to "follow content rhythm".
- **Sharp-cornered (rectangular) containers** — Rule 2 doesn't apply; only Rule 1 (equal insets).
- **Visually distinct visual layer** (e.g., a floating overlay or a popover anchored to a corner with deliberate offset) — these are positioned by design, not by content rhythm.
