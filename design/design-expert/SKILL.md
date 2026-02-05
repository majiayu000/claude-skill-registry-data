---
name: design-expert
description: Use for HTML/CSS layout, responsive behavior, and UI styling on the NestMind site; follow the Zed-inspired design system in css/styles.css and reuse existing patterns.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Design Expert

Use this skill when adjusting HTML/CSS, layout, or visual design in this repo. Keep the current editorial, light-theme aesthetic and reuse the design system.

## Project rules (must)
- Use tokens from `css/styles.css` (`:root`) for colors, spacing, typography, and motion.
- Keep typography pairing: `--font-serif` for headings, `--font-sans` for body.
- Default theme is light; add `.dark` overrides only when requested or already in use.
- Prefer existing classes/components before creating new ones.

## Responsive behavior
- Mobile-first; use existing breakpoints at 640px, 768px, and 1024px.
- Ensure tap targets are at least 44px and avoid horizontal overflow on small screens.
- Use flex/grid with wrapping; avoid fixed widths on mobile.

## Motion + performance
- Animate with `transform` and `opacity`; avoid layout thrash.
- Respect `prefers-reduced-motion`.

## Accessibility
- Use semantic HTML and visible focus states.
- Maintain text contrast at 4.5:1 or higher.

## File placement
- Global styles: `css/styles.css`
- Page-specific styles: `css/vision.css`, `css/docs.css`

## Reuse first
- Scan `css/styles.css` for existing patterns like `.container`, `.btn`, `.card`, `.hero`, `.nav`, `.feature-detail`, and `.phone-mockup`.
