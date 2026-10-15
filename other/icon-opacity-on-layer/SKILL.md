---
name: icon-opacity-on-layer
description: Apply opacity to the icon container layer, not to its strokes or fills via alpha-tinted currentColor. Use when rendering SVG icons that need to appear muted, disabled, or de-emphasized, especially icons with intersecting paths.
---

# Icon Opacity on Layer

## Rule

- SVG `stroke` / `fill` use a fully opaque `currentColor`.
- Apply transparency with `opacity` on the icon's container (the `<svg>` or its wrapper), not by giving the inherited color its own alpha channel (e.g. `text-black/40`).

## Why

If each stroke carries its own alpha, overlapping pixels composite alpha twice:

```
α_total = 1 − (1 − α)²   // e.g. α=0.4 → 0.64 at intersections
```

The overlap appears noticeably darker than the rest of the icon. Moving transparency up to the layer ensures the whole icon is flattened first, then the single layer alpha is applied — every pixel gets one alpha pass, so intersections match the rest.

## Pattern

```tsx
// ✗ alpha on currentColor → double-composite at path intersections
<svg className="text-black/40">
  <path stroke="currentColor" ... />
  <path stroke="currentColor" ... />
</svg>

// ✓ opaque color, opacity on the layer
<svg className="text-black opacity-40 dark:text-white">
  <path stroke="currentColor" ... />
  <path stroke="currentColor" ... />
</svg>
```
