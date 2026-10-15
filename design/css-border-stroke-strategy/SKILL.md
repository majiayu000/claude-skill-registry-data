---
name: css-border-stroke-strategy
description: Strategies for rendering borders, strokes, and outlines in CSS with explicit layout impact analysis. Use when adding borders, focus rings, decorative strokes, glass-effect inner shadows, or multi-layer stroke effects to components. Covers border, outline, box-shadow, and overlay techniques with trade-offs.
---

# CSS Border & Stroke Strategy

Choose the right technique based on whether the stroke should affect layout.

## Decision Table

| Technique                             | Layout impact                                  | Respects border-radius | Stackable | When to use                                             |
| ------------------------------------- | ---------------------------------------------- | ---------------------- | --------- | ------------------------------------------------------- |
| `border`                              | **Yes** — shrinks content area by border-width | Yes                    | No        | Structural borders that are part of the sizing model    |
| `outline` + `outline-offset`          | **No**                                         | Yes (modern browsers)  | No        | Focus rings, selection indicators                       |
| `box-shadow` (outset)                 | **No**                                         | Yes                    | Yes       | Decorative outer strokes, glow, elevation               |
| `box-shadow` (inset)                  | **No**                                         | Yes                    | Yes       | Inner strokes, glass highlight effects                  |
| Overlay `div` + `pointer-events-none` | **No**                                         | Yes                    | Yes       | Complex multi-layer strokes, independent radius control |

## `border`

Participates in the box model. Content area shrinks by `border-width`.

```css
border: 1px solid rgba(255, 255, 255, 0.6);
```

Use `box-sizing: border-box` (Tailwind default) so `width`/`height` include the border. When nesting rounded containers, maintain concentricity:

```
inner-radius = outer-radius - border-width
```

For a 24px outer radius with 2px border → inner content needs `rounded-[22px]`.

**Tailwind**: `border border-white/60`

## `outline` + `outline-offset`

Does not affect layout or box size. Draws outside (or inside with negative offset) the border edge.

```css
outline: 2px solid #0e6efc;
outline-offset: -2px; /* draw inside the element */
```

Ideal for focus-visible rings where adding layout shift would be disruptive.

**Tailwind**: `outline-2 outline-[#0E6EFC] -outline-offset-2`

**Caveat**: `outline` always follows the border-radius in modern browsers but does not support per-side control.

## `box-shadow` as Stroke

Zero-blur, zero-spread shadow simulates a border with no layout impact. Stackable via comma separation.

### Outer stroke

```css
box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.6);
```

**Tailwind**: `shadow-[0_0_0_1px_rgba(255,255,255,0.6)]`

### Inner stroke

```css
box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.6);
```

**Tailwind**: `shadow-[inset_0_0_0_1px_rgba(255,255,255,0.6)]`

### Glass inner highlight

Top-edge light reflection for glassmorphism:

```css
box-shadow: inset 0px 1px 1px rgba(255, 255, 255, 0.25);
```

**Tailwind**: `shadow-[inset_0px_1px_1px_rgba(255,255,255,0.25)]`

### Stacking multiple shadows

```css
box-shadow:
  inset 0px 1px 1px rgba(255, 255, 255, 0.25),
  /* glass highlight */ 0 0 0 1px rgba(255, 255, 255, 0.6),
  /* outer stroke */ 0px 8px 40px rgba(0, 0, 0, 0.12); /* elevation */
```

## Overlay Div

For effects that need independent border-radius, multiple layers, or animation:

```tsx
<div className="relative overflow-hidden rounded-3xl">
  {children}
  <div
    aria-hidden
    className={`
      pointer-events-none absolute inset-0
      shadow-[inset_0px_1px_1px_rgba(255,255,255,0.25)]
    `}
    style={{ borderRadius: "inherit" }}
  />
</div>;
```

Key attributes:

- `pointer-events-none` — click-through
- `absolute inset-0` — covers parent exactly
- `aria-hidden` — invisible to screen readers
- `borderRadius: 'inherit'` — matches parent's radius automatically

Stack multiple overlays for complex glass effects (e.g. doubled inner shadow for stronger highlight).

## Common Patterns

### Glass card

```tsx
<div
  className={`
  relative overflow-hidden rounded-[28px]
  border-[0.5px] border-white/80 bg-white/40 backdrop-blur-[20px]
  dark:border-white/20 dark:bg-white/10
`}
>
  {children}
  <div
    aria-hidden
    className={`
      pointer-events-none absolute inset-0
      shadow-[inset_0px_1px_1px_rgba(255,255,255,0.25)]
      dark:shadow-[inset_0px_1px_1px_rgba(255,255,255,0.08)]
    `}
    style={{ borderRadius: "inherit" }}
  />
</div>;
```

Here `border-[0.5px]` is acceptable because the 0.5px impact is negligible and `border` renders sharper than `box-shadow` at sub-pixel widths.

### Focus ring (no layout shift)

```tsx
className = "focus-visible:outline-2 focus-visible:outline-ring focus-visible:-outline-offset-2";
```

### Decorative outer glow

```tsx
className = "shadow-[0_0_0_1px_rgba(14,110,252,0.3),0_0_20px_rgba(14,110,252,0.15)]";
```

## Anti-Patterns

- **Using `border` for decorative strokes on glass elements** — the 1px layout shift causes content to jitter when borders toggle. Use `box-shadow` or overlay instead.
- **Forgetting `pointer-events-none` on overlay divs** — blocks clicks on content underneath.
- **Mixing `border` and `box-shadow` strokes without accounting for visual offset** — `box-shadow` renders outside the border edge, creating a visible gap.
- **Using `outline` for decorative strokes** — `outline` cannot be rounded per-side and doesn't support `inset`. Reserve for focus indicators.
