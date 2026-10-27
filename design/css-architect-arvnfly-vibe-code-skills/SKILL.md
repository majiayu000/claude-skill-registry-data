---
name: css-architect
description: "Maintainable CSS architectures, container queries, fluid spacing tokens, CSS variable cascades, and layout shift prevention."
---

# CSS Architecture & Layout Hygiene Protocol

When authoring stylesheets, utility tokens, or component styles, maintain strict modular hygiene.

---

## 1. Token Cascades & Custom Properties

1. Define global design tokens exclusively on :root using semantic variables:
   --color-bg-primary, --color-text-main, --space-md.
2. Component styles should consume semantic tokens, never raw hex colors or fixed pixel dimensions.
3. Media queries for dark mode should simply rebind CSS custom properties, avoiding duplicated selector rules.

---

## 2. Layout Shift (CLS) Prevention

1. Always specify aspect-ratio or explicit width and height on media items (images, videos, embeds).
2. Avoid animating layout properties (width, height, margin, top). Animate composite-only properties (transform, opacity).
3. Use font-display: swap with matched fallback metrics to prevent layout shifts during web font loading.

---

## 3. Modern Responsive Layouts

- Prefer CSS Grid and Flexbox over float/inline-block hacks.
- Use CSS Container Queries (@container) for modular components that adapt to parent container width rather than viewport width.
