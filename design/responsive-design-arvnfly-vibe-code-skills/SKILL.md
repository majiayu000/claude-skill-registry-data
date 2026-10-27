---
name: responsive-design
description: "Mobile-first responsive layouts, dynamic viewport units, fluid typography, and touch target accessibility."
---

# Responsive Design & Multi-Device Protocol

Deliver adaptive interfaces across mobile, tablet, desktop, and foldable screens.

---

## 1. Mobile-First Media Queries

1. Author base styles for mobile viewports (< 640px).
2. Layer layout expansions progressively using `min-width` breakpoints (`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`).

---

## 2. Touch Targets & Safe Areas

- Minimum touch target size: 44x44 CSS pixels for all interactive controls.
- Respect mobile device notches with `env(safe-area-inset-*)` padding.
