---
name: frontend-design
description: Production-grade frontend design skill. Creates distinctive, polished interfaces that avoid generic AI aesthetics. Use when building any web page, component, or UI.
license: Adapted from Anthropic's official frontend-design skill (MIT)
---

Create distinctive, production-grade frontend interfaces. No generic AI slop.

## Before Coding: Choose a Direction

Every design starts with a deliberate aesthetic choice:
- **Purpose** — What problem does this solve? Who uses it?
- **Tone** — Pick one: brutally minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, soft/pastel, industrial. Commit fully.
- **Differentiation** — What's the one thing someone will remember about this design?

## Typography

- Choose fonts that are **distinctive**, not default. Never use Arial, Inter, or Roboto as your primary display font without a specific reason.
- Pair a display font (headlines) with a body font (text). They should contrast but complement.
- Load from Google Fonts, Fontshare, or similar CDN — always include the `<link>` tag.

## Colour

- Commit to a **cohesive palette**. 2-3 colours max, used consistently.
- Use CSS custom properties (`--color-primary`, etc.) for every colour.
- One dominant colour + one sharp accent outperforms an evenly-distributed palette.
- Dark themes: true dark backgrounds (#060610-#111) read as "premium tech." Light themes: generous whitespace reads as "editorial."

## Layout

- Break the grid sometimes. Asymmetry, overlap, and unexpected spacing create visual interest.
- Generous negative space is a design choice, not laziness.
- Every section should have a clear visual hierarchy: what do you see first, second, third?

## Motion

- One well-orchestrated page load (staggered reveals) creates more delight than scattered micro-interactions.
- CSS-only animations for HTML. Use animation libraries for React.
- `prefers-reduced-motion` media query on ALL animations — non-negotiable.

## Self-Contained Output

- All CSS must be inline or in a `<style>` block — no external stylesheet references.
- All fonts loaded via CDN `<link>` tags.
- No placeholder images — generate them first or use CSS gradients/patterns.
- The HTML file must work when opened directly in a browser.

## What NOT to Do

- Purple gradient on white background
- Cookie-cutter card layouts
- "Hero section with stock photo"
- Same font for everything
- Buttons that all look the same
- Missing accessibility (focus states, contrast, alt text)
