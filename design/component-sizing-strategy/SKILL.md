---
name: component-sizing-strategy
description: Component sizing contract guidelines — intrinsic size vs layout contract, block-size owned by component, inline-size owned by container. Use when building reusable UI components, deciding width/height strategy, reviewing component sizing, or when a component's size behaves unexpectedly in different layout contexts.
---

# Component Sizing Strategy

Two layers determine every component's final size:

- **Intrinsic size** — how large the component naturally needs to be without external constraint.
- **Layout contract** — whether the parent expects it to hug, fill, or fit within a given range.

The core heuristic:

```
block-size  → component decides  (content, padding, line-height, min-height)
inline-size → container decides  (available space, grid/flex distribution)
```

This is a default priority, not an absolute rule. It reflects the fact that in normal flow, inline-size resolves from available space while block-size resolves from content.

Note that `auto` and `100%` are not interchangeable for inline-size. A block-level element with `width: auto` fills available space _minus_ its own margins — the browser resolves it. `width: 100%` forces the content box to exactly match the containing block's content width, which can cause overflow when the element has padding, border, or margin (unless `box-sizing: border-box` absorbs padding and border). In flex/grid contexts, `auto` means "use my content size" while `100%` means "use my containing block's size" — entirely different behaviors.

---

## Component Categories

### Leaf Components

`Button`, `Input`, `Tag`, `Badge`, `Avatar`, `IconButton`

- **block-size**: defined by the component via `padding-block`, `line-height`, `font-size`, `min-block-size`, and size variants (`sm` / `md` / `lg`).
- **inline-size**: default `auto` (hug content). Provide an explicit `fill` variant when full-width is needed — never default to `w-full`.
- Height tokens couple tightly with touch targets, text baselines, and icon size — do not let the parent stretch them arbitrarily. Flex containers default to `align-items: stretch`, which will override `min-block-size` and pull the component taller. Defend with an explicit `block-size` on the component root or `align-self: center`.

Typical height scale for controls:

| Variant | Height  | Use case                                   |
| ------- | ------- | ------------------------------------------ |
| `sm`    | 32px    | Dense UI, toolbars                         |
| `md`    | 36–40px | Default desktop                            |
| `lg`    | 44px    | Mobile touch target (Apple HIG / WCAG AAA) |

Width API pattern:

```ts
type Width = "auto" | "fill";
```

- `auto` → `inline-size: auto`
- `fill` → `inline-size: 100%`

### Container Components

`Card`, `List`, `Section`, `FormGroup`, `Panel`

- **inline-size**: default `100%` — fills the parent. The parent (or a page shell) controls `max-inline-size`. This assumes normal flow; inside a flex row, use `flex: 1` instead of `width: 100%` to fill available space.
- **block-size**: default `auto` — content determines height. Only constrain with `max-block-size` + `overflow: auto` when the container must scroll.

### Overlay / Strong-Layout Components

`Dialog`, `Drawer`, `Sidebar`, `Popover`, `Toast`

- Own their sizing contract as part of their API — default `min-inline-size`, `max-inline-size`, and sometimes explicit `block-size` are expected.
- These are the exception where a component legitimately ships fixed dimensional constraints.

---

## Sizing Contract: Who Owns What

### Component owns

- `padding`
- `gap`
- `line-height` / `font-size`
- `min-block-size`
- Optional `min-inline-size` / `max-inline-size` (for safety bounds, e.g. Button min-width, Input min-width, Popover max-width)
- Truncation / overflow behavior
- Icon size

### Parent / container owns

- Placement and available inline space
- Grid / flex distribution
- Page-level `max-inline-size`
- Section spacing
- Viewport adaptation

**Principle: the component defines "what it looks like and the minimum space it needs"; the container defines "how much space it gets in this context".**

---

## Flex Layout Pitfalls

Many sizing failures in practice are not about missing `width` — they are about flex/grid item defaults.

### `min-width: auto` on flex and grid items

By spec, flex items default to `min-width: auto`, which prevents them from shrinking below their content size when `overflow` is `visible` (the default). Long text or large children can blow out the layout. Grid items have the same automatic minimum size behavior.

Fix: apply `min-w-0` on items that should allow content to truncate. Setting `overflow: hidden` on the item also bypasses the automatic minimum, but `min-w-0` is the more surgical fix — it doesn't clip content on the cross axis.

### Trailing elements getting squeezed

Side elements (status indicator, action button) can shrink when the main content pushes against them.

Fix: apply `shrink-0` on elements that must maintain their intrinsic size.

Typical row pattern:

```tsx
<div className="flex items-center gap-3 px-4 py-3">
  <Icon className="shrink-0" />
  <span className="min-w-0 truncate">{label}</span>
  <StatusDot className="shrink-0" />
</div>;
```

---

## Storybook Verification

Storybook is a **verification tool**, not the sizing strategy itself. Use it to prove the component's sizing contract holds across contexts:

```tsx
export const NarrowContainer: Story = {
  decorators: [
    (Story) => (
      <div className="w-64">
        <Story />
      </div>
    ),
  ],
};

export const WideContainer: Story = {
  decorators: [
    (Story) => (
      <div className="w-[720px]">
        <Story />
      </div>
    ),
  ],
};

export const FlexRow: Story = {
  decorators: [
    (Story) => (
      <div className="flex gap-2">
        <Story />
        <Story />
      </div>
    ),
  ],
};
```

If a component only looks right inside one specific container width, its sizing contract is underspecified.

---

## Quick Reference

| Component type | `inline-size`                   | `block-size`                                |
| -------------- | ------------------------------- | ------------------------------------------- |
| Leaf           | `auto` (provide `fill` variant) | Component-defined via size token            |
| Container      | `100%`                          | `auto` (opt-in `max-block-size` + overflow) |
| Overlay        | Component-defined min/max       | Component-defined or `auto`                 |
| Page shell     | `100%` + `max-inline-size`      | Viewport-driven                             |
