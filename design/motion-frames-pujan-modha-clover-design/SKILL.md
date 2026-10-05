---
name: motion-frames
description: |
  Single-frame motion-design composition with looping CSS animations.
  Rotating type ring, animated globe, ticking timer, parallax labels.
  Ready for frame-grabber export.
triggers:
  - "motion design"
  - "animated hero"
  - "loop animation"
  - "video poster"
  - "title card"
  - "kinetic typography"
df:
  mode: prototype
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Motion Frames Skill

Produce a single full-bleed motion composition. CSS animations only.

## Layers (back to front)
1. **Stage** — full-bleed `<main>`. Subtle dotted grid texture.
2. **Concentric rings** — 2–3 SVG circles, ultra-thin strokes, rotate at
   different speeds (60s, 90s, 180s).
3. **Focal mark** — wireframe globe or typographic monogram, ~28% canvas width.
4. **Ring labels** — short words around a ring, counter-rotated to stay upright.
5. **Headline** — bottom-left or center-bottom. Display serif, italic accent.
   `letterSpacing` + opacity reveal animation.
6. **Frame chrome** — corner stamps, thin baseline rule. Static.

## Animations (CSS `@keyframes` only)
- `rotate-slow/med/fast` for rings.
- `globe-spin` for focal mark.
- `pulse` for focal dot.
- `marquee-fade` for headline reveal.

## Rules
- Still reads as a poster at frame 0.
- ≥3 layers move at different speeds.
- Accent appears once (italic word in headline).
- `data-df-id` on stage, focal, ring, headline.

## Output
Single `index.html`. No JS — deterministic for frame grabbers.
