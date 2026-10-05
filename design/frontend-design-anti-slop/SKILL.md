---
name: frontend-design-anti-slop
description: |
  Creates distinctive, production-grade frontend interfaces with exceptional
  design quality. Avoids generic AI aesthetics (Inter font, purple gradients,
  predictable card layouts). Use for any UI component, landing page, dashboard,
  or prototype styling.
triggers:
  - "anti-slop"
  - "distinctive design"
  - "high quality UI"
  - "craft"
  - "editorial UI"
df:
  mode: utility
  platform: any
  scenario: design
  design_system:
    requires: false
---

# Frontend Design Anti-Slop

Break the default "AI slop" pattern deliberately.

## Typography

Choose unexpected, characterful typefaces. Pair a distinctive display font
(Playfair Display, DM Serif Display, Syne, Bebas Neue, Instrument Serif)
with a refined body font.

**Never use as primary:** Inter, Roboto, Arial, system-ui, Space Grotesk.

## Color & Theme

Commit fully to one coherent aesthetic. Use CSS custom properties for every
color token.

**Try these palettes instead of purple-on-white:**
- Deep navy + warm amber
- Charcoal + acid green
- Cream + burgundy + gold
- Near-black + electric cyan

Use `oklch()` for perceptually uniform lightness steps and vivid gamut-P3 hues.

## Motion

CSS-only for HTML artifacts. One well-orchestrated page-load with staggered
`animation-delay` reveals beats scattered micro-interactions.

Gate all animations behind `@media (prefers-reduced-motion: reduce)`.

## Spatial Composition

Asymmetry. Overlap. Diagonal rhythm. Grid-breaking hero elements.
Resist center-aligning everything — left-aligned, offset, or edge-bleeding
layouts feel more crafted.

## Backgrounds

Never solid white or grey. Use:
- CSS gradients
- Noise/grain overlay (`opacity: 0.04`)
- Geometric SVG patterns
- Subtle radial glows

## Tone Commitment

Pick **one** tone and execute with full craft:
- Brutally minimal
- Maximalist chaos
- Retro-futuristic
- Organic warmth
- Luxury editorial
- Bold experimental

Do not hedge between styles — half-committed aesthetics look worse than any
single extreme.

## Hard Prohibitions

NEVER use:
- Inter/Roboto/Arial/Space Grotesk as primary typeface
- Purple gradients on white
- Symmetric 3-column card grids as the only layout
- Bootstrap-default drop shadows
- Grey placeholder rectangles as "images"
