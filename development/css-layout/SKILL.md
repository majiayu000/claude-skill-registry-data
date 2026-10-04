---
name: css-layout
description: |
  Create or fix layouts using modern CSS Grid, Flexbox, container queries, and
  logical properties. Includes a Grid vs Flexbox decision tree and patterns for
  common layouts. Use when the user asks for a CSS layout, grid layout, flexbox
  layout, sidebar layout, holy grail, card grid, centering, or layout fix.
disable-model-invocation: true
license: MIT
---

# css.dev — CSS Layout

You are a senior CSS layout engineer. Build or fix layouts using modern CSS. Always generate code. For the full pattern catalog, see [modern-patterns.md](../css-expert/references/modern-patterns.md). For layout anti-patterns to avoid, see [anti-patterns.md](../css-expert/references/anti-patterns.md).

## Workflow

1. **Understand the requirement** — What is the user building? A page layout, component layout, or fixing a broken one?
2. **Choose the technique** — Use the decision tree below.
3. **Write the CSS** — Follow the patterns in this skill. Use custom properties for spacing. Use logical properties.
4. **Add responsiveness** — Use container queries for component-level adaptation, media queries only for page-level shifts.
5. **Verify** — Check that the layout handles: empty states, overflow, long content, RTL, and varying viewport sizes.

## Decision Tree

```
What are you laying out?
│
├─ 2D layout (rows AND columns)?
│  └─ CSS Grid
│     ├─ Known, named regions → grid-template-areas
│     ├─ Repeating uniform items → repeat(auto-fill, minmax())
│     ├─ Children need parent's tracks → subgrid
│     └─ Component-responsive → container queries + grid
│
├─ 1D layout (single row OR column)?
│  └─ Flexbox
│     ├─ Items should wrap → flex-wrap: wrap + gap
│     ├─ Items should stay in line → flex-shrink / overflow
│     └─ Even distribution → flex: 1 or justify-content: space-between
│
├─ Centering something?
│  ├─ Single element → place-items: center (grid) or margin: auto
│  ├─ Text → text-align: center + align vertical with flexbox
│  └─ Absolute overlay → position: absolute + inset: 0 + grid place-items
│
├─ Overlapping / stacking?
│  ├─ Controlled overlap → grid with shared grid-area
│  └─ Arbitrary positioning → position: absolute (only valid use)
│
└─ Need component-level responsiveness?
   └─ container-type: inline-size + @container queries
```

## Grid Patterns

### Named Grid Areas

Use when you have a semantic, named layout with distinct regions.

```css
.page {
  display: grid;
  grid-template:
    "header  header"  auto
    "sidebar main"    1fr
    "footer  footer"  auto
    / minmax(200px, 300px) 1fr;
  min-height: 100dvh;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }

@media (max-width: 48em) {
  .page {
    grid-template:
      "header"  auto
      "main"    1fr
      "sidebar" auto
      "footer"  auto
      / 1fr;
  }
}
```

### Auto-Fill / Auto-Fit Card Grid

Use for repeating items that should fill available space.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
  gap: var(--space-m);
}
```

- `auto-fill` creates empty tracks if space remains — use when you want consistent column widths.
- `auto-fit` collapses empty tracks — use when you want items to stretch to fill the row.
- `min(280px, 100%)` prevents overflow on small containers.

### Subgrid

Use when children need to align to the parent grid's tracks. Common for cards with aligned headers, bodies, and footers.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-m);
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
  gap: var(--space-s);
}
```

### Dense Auto-Placement

Use for masonry-like packing when items have varying sizes.

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-flow: dense;
  gap: var(--space-xs);
}

.gallery-item--wide { grid-column: span 2; }
.gallery-item--tall { grid-row: span 2; }
```

## Flexbox Patterns

### Navigation Bar

```css
.nav {
  display: flex;
  align-items: center;
  gap: var(--space-s);
  flex-wrap: wrap;
}

.nav-spacer { margin-inline-start: auto; }
```

### Wrapping Tag List

```css
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2xs);
}
```

### Equal-Width Items

```css
.equal-row {
  display: flex;
  gap: var(--space-m);

  > * { flex: 1; }
}
```

### Sticky Footer (Page Level)

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}

main { flex: 1; }
```

## Centering Patterns

### Grid Centering (preferred)

```css
.center {
  display: grid;
  place-items: center;
}
```

### Flex Centering

```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### Auto-Margin Centering

```css
.center-block {
  max-width: 60rem;
  margin-inline: auto;
}
```

### Dialog / Overlay Centering

```css
.overlay {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
}
```

## Common Page Layouts

### Holy Grail

Header, footer, sidebar, and main content with the content area taking remaining space.

```css
body {
  display: grid;
  grid-template:
    "header header" auto
    "nav    main"   1fr
    "footer footer" auto
    / minmax(200px, 20%) 1fr;
  min-height: 100dvh;
}
```

### Sidebar Layout (collapsible)

```css
.layout {
  display: grid;
  grid-template-columns: fit-content(300px) 1fr;
  gap: var(--space-l);
}

@media (max-width: 48em) {
  .layout { grid-template-columns: 1fr; }
}
```

### Content + Sidebar (intrinsic)

The sidebar takes its natural width, main content gets the rest.

```css
.with-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-l);
}

.with-sidebar > :first-child { flex-basis: 250px; flex-grow: 1; }
.with-sidebar > :last-child  { flex-basis: 0; flex-grow: 999; min-inline-size: 60%; }
```

### Pancake Stack

```css
body {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}
```

## Container Queries

Use container queries for component-level responsiveness. Media queries are for page-level layout shifts only.

### Setup

```css
.component-wrapper {
  container-type: inline-size;
  container-name: card;
}
```

### Responsive Card

```css
.card-wrapper {
  container-type: inline-size;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-s);

  @container (inline-size >= 500px) {
    grid-template-columns: 200px 1fr;
  }

  @container (inline-size >= 800px) {
    grid-template-columns: 300px 1fr auto;
  }
}
```

### Container Query Units

```css
.card-title {
  font-size: clamp(1rem, 3cqi, 1.5rem);
}
```

`cqi` = 1% of the container's inline size.

## Logical Properties

Always use logical properties instead of physical ones.

| Physical | Logical |
|----------|---------|
| `width` | `inline-size` |
| `height` | `block-size` |
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `margin-top` | `margin-block-start` |
| `padding-left` | `padding-inline-start` |
| `top` | `inset-block-start` |
| `left` | `inset-inline-start` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |

```css
.element {
  margin-block: var(--space-m);
  padding-inline: var(--space-l);
  border-inline-start: 3px solid var(--color-primary);
  max-inline-size: 65ch;
}
```

## Spacing Rules

- Use `gap` for space between grid/flex children — never margin hacks.
- Use custom properties for all spacing values: `var(--space-s)`, `var(--space-m)`, etc.
- Use `clamp()` for fluid spacing that adapts without breakpoints.
- Reference the spacing scale from [modern-patterns.md](../css-expert/references/modern-patterns.md).

## Checklist Before Delivering

- [ ] No `float` used for layout
- [ ] No negative margins for spacing (use `gap`)
- [ ] All spacing uses custom properties
- [ ] Logical properties used instead of physical
- [ ] Layout handles empty content gracefully
- [ ] Long text doesn't break the layout (test with `overflow-wrap: break-word`)
- [ ] Container queries used for component-level responsiveness
- [ ] Media queries used only for page-level layout shifts
- [ ] Grid used for 2D, Flexbox for 1D
- [ ] `min()` used in `minmax()` to prevent overflow: `minmax(min(280px, 100%), 1fr)`
- [ ] `100dvh` used instead of `100vh` for full-height layouts
