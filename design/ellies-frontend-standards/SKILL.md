---
name: ellies-frontend-standards
description: Frontend development standards for Ellie's projects. Use when building frontend interfaces, components, pages, or applications. Enforces tech stack preferences (Leptos > HTMX/SolidJS > React, modern vanilla CSS, no Tailwind) and accessibility-first development. Always apply these standards unless they conflict with an existing project's established patterns.
---

# Ellie's Frontend Standards

## Core Principles

**Consistency trumps these guidelines.** If working in an existing project with established patterns, follow those patterns even if they contradict the preferences below.

## Tech Stack

### Frameworks (in order of preference)

1. **Leptos** (Rust) - Preferred when Rust is an option
2. **HTMX** or **SolidJS** - Preferred for JS-based projects
3. **React** - Only when required by existing project or explicit request

### CSS

**Use modern vanilla CSS.** Take advantage of:
- CSS custom properties (variables)
- Native CSS nesting
- Container queries
- `:has()`, `:is()`, `:where()` selectors
- CSS Grid and Flexbox
- `clamp()` for fluid typography and spacing

**Never use Tailwind.** No exceptions.

### Aesthetics

Defer to the `frontend-design` skill for visual design guidance (typography, color, motion, layout aesthetics).

## Accessibility

Accessibility is a priority, not an afterthought:

- **Semantic HTML first** - Use the right element for the job (`<button>`, `<nav>`, `<main>`, `<article>`, etc.)
- **Keyboard navigation** - All interactive elements must be keyboard accessible
- **Focus management** - Visible focus indicators, logical focus order, focus trapping in modals
- **ARIA when needed** - Only when semantic HTML isn't sufficient; prefer native elements
- **Color contrast** - Meet WCAG AA minimum (4.5:1 for text, 3:1 for large text/UI)
- **Motion** - Respect `prefers-reduced-motion`
- **Screen reader testing** - Consider how content reads linearly
