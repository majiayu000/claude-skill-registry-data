---
name: standalone-divider-spacer
description: Render dividers (rules between rows/sections) and spacers (fixed gaps between elements) as their own standalone elements, with the surrounding gap owned by the layout — never as a `border-t`/`border-b` plus `py-*`, or an `mt-*`/`mb-*`, glued onto a content element. Use when adding a divider between list rows or panel sections, inserting fixed space between elements, reviewing layout code that fakes spacing with padding/margin on bordered blocks, or when you catch yourself debating whether a margin belongs to the element above or below.
---

# Standalone Divider & Spacer

## Rule

A divider (the visible rule between rows/sections) and a spacer (deliberate empty space between elements) are **layout concerns, not properties of the content**. Express each as its own element — or, better, as the parent's `gap` — instead of welding a border + padding, or a margin, onto a content box.

```tsx
// ❌ divider welded to the row: padding fakes the gap, `first:` undoes the edge
<div className="border-t border-dashed border-border py-1 first:border-t-0">{row}</div>

// ❌ margin on a bordered block: whose space is mt-1.5 / mb-3 — the block's, or its neighbour's?
<div className="mt-1.5 mb-3 border-y border-border">{editor}</div>
```

```tsx
// ✅ rows stay pure; the rule lives in the gap as its own element
<div className="flex flex-col gap-1">
  {Children.toArray(children).map((child, i) => (
    <Fragment key={i}>
      {i > 0 && <Divider />}
      {child}
    </Fragment>
  ))}
</div>;
```

## Why

- **No ownership question.** A standalone gap belongs to nobody. You never have to decide whether the space is `mb` on the element above or `mt` on the element below — the philosophical coin-flip that makes margins drift and double up.
- **The content element stays untouched.** A row/card keeps its own box model. Move it, reorder it, reuse it elsewhere — it drags no divider state, no `first:`/`last:` overrides, no neighbour-specific margin with it.
- **Symmetric by construction.** A divider sitting inside a parent `gap` gets equal breathing room above and below automatically. No `py` to balance against the next item's `py`.
- **Composable.** In a mapped/reorderable list, interleaving `<Divider>` between children means removing an item re-balances the rules with zero `first-child`/`last-child` edge cases.
- **No margin-collapse surprises.** An element in flow can't collapse against its neighbours the way adjacent/parent margins do.

## Divider primitive

A dedicated 1px element. `dashed` picks the lighter inter-row rule; default is the solid section rule.

```tsx
export const Divider: FC<{ dashed?: boolean; className?: string; }> = ({ dashed, className }) => (
  <div
    aria-hidden
    className={(dashed ? "border-t border-dashed border-border" : "h-px bg-border")
      + " w-full shrink-0"
      + (className ? " " + className : "")}
  />
);
```

The line width and the space around it are now independent: the line is the element, the space is the parent's `gap`. Tune them separately without `first:border-t-0` hacks.

## Spacer: prefer `gap`, then a real element

The cleanest spacer is the parent's `gap` / `space-y-*` — reach for an explicit element only when the layout genuinely can't express the gap:

```tsx
// Fixed empty space the parent gap can't express (e.g. one larger break in a list)
const Spacer: FC<{ size: number }> = ({ size }) => (
  <div aria-hidden className="shrink-0" style={{ height: size }} />
)

// Flexible push (shove trailing content to the far edge) — a flex spacer, not margin-auto soup
<div className="flex items-center">
  <Brand />
  <div className="flex-1" />
  <Actions />
</div>
```

## When NOT to use

- **A genuine region edge** — a panel header's bottom rule, a card's outline, an input's border — is an edge **of that element**, not an inter-element divider. Leaving it as `border-b` / `border` on the element is correct; it isn't faking a gap with padding.
- **A single fixed gap a parent `gap` already covers** — don't insert a `<Spacer>` where `gap-*` / `space-y-*` on the container does the job. The element-spacer is for the cases `gap` can't express (uneven gaps, a flexible push).
