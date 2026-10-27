---
name: tailwind-v4
description: "Tailwind CSS v4 engine, CSS-first configuration, arbitrary properties, and container query utilities."
---

# Tailwind CSS v4 Architecture Protocol

Build lightweight UI styling without CSS runtime overhead.

---

## 1. CSS-First Directives

1. In Tailwind v4, import using `@import "tailwindcss";` in CSS.
2. Define theme tokens with `@theme` blocks in CSS rather than `tailwind.config.js`.

---

## 2. Component Utility Composition

- Use component extraction or CVA (Class Variance Authority) for button and card variants.
- Avoid deeply duplicated utility strings across identical HTML templates.
