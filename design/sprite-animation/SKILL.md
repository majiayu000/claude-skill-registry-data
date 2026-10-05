---
name: sprite-animation
description: |
  CSS sprite-sheet animation with stepping keyframes. Character walk cycle,
  loading spinner, or UI micro-animation. Use for "sprite", "animation",
  "walk cycle", "loading animation".
triggers:
  - "sprite"
  - "sprite animation"
  - "walk cycle"
  - "loading animation"
  - "micro animation"
df:
  mode: prototype
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Sprite Animation Skill

Produce a CSS sprite-sheet animation.

## Structure
- **Stage**: centered container with background grid.
- **Sprite**: CSS `background-image` using an inline SVG sprite sheet
  (drawn as a row of frames).
- **Animation**: `steps(N)` keyframe animation cycling through frames.
- **Controls**: play/pause button (CSS-only toggle via checkbox hack or
  just auto-play).

## Rules
- 6–12 frames in the sprite sheet.
- Smooth loop (`animation-iteration-count: infinite`).
- Frame size consistent.
- `data-df-id` on stage and sprite.

## Output
Single `index.html`, inline CSS + inline SVG sprite sheet.
