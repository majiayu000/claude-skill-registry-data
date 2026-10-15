---
name: web-ui-standards
description: Web UI standards covering Tailwind CSS, Radix UI, accessibility, animations, responsive layout, and pixel-perfect alignment. Use when building or reviewing web UI components, styling, animations, accessibility, dark mode, or when the user mentions UI standards or design system conventions.
---

# Web UI Standards

- Use **Tailwind CSS** v4 for styling; prefer utility classes over custom CSS.
- Use **Radix UI Primitives** as the headless component foundation (a11y + keyboard-first).
- Use **Motion** (formerly **Framer Motion**) for UI animations; respect `prefers-reduced-motion`, avoid layout-affecting animations unless necessary. Only animate when it serves UX purpose (feedback, orientation, continuity); keep transitions subtle and short — no decorative or showy effects.
- **Mobile-first** responsive layout; prefer clean modern composition with `flex` / `grid`, minimal compatibility workarounds.
- Enforce **accessibility**: correct semantics, proper ARIA attributes, `:focus-visible` focus styles, fully keyboard navigable interactions. Keep DOM nesting shallow — use Radix `asChild` to merge behavior onto existing elements instead of adding wrapper nodes.
- Minimize **layout shift (CLS)**: reserve space for async content, stable typography and sizing.
- Support **Dark / Light** via `prefers-color-scheme` only (CSS media query), no manual toggle or stored theme state.
- Consistent **typography & spacing**: use a defined type scale and spacing scale from the design system; no magic numbers.
- **Optimistic UI**: prefer optimistic updates for async mutations.
- **Keyboard shortcuts & Command Palette**: consider binding high-frequency actions to shortcuts; consider a `cmdk`-style command palette for power-user navigation when appropriate.
- **Micro-interactions & Feedback**: respond visually at the moment of interaction, not when the result arrives; provide clear state transitions and outcome feedback (success, error, validation). The user should never wonder "did that work?".
- **Pixel-perfect alignment**: treat 0.5px as 0.5px, not 0. Be aware that `border` occupies layout space while `outline` does not — choose deliberately. Consider `outline` with negative `outline-offset`, or an absolutely-positioned layer, for non-layout-affecting borders when alignment demands it. When drawing borders on rounded corners, maintain concentricity — inner and outer radii must share the same center (`inner-radius = outer-radius − border-width`); use `calc()` to derive the inner radius dynamically.
