---
name: hyperframes
description: |
  Multi-frame animated composition with CSS keyframes — scroll-driven or
  auto-playing frames for storytelling. Use with "hyperframes", "scroll story",
  "animated narrative".
triggers:
  - "hyperframes"
  - "scroll story"
  - "animated narrative"
  - "frame animation"
  - "scroll animation"
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

# HyperFrames Skill

Produce a multi-frame scroll-driven or auto-playing composition.

## Structure
- **Container**: 100vh frames stacked vertically.
- **Each frame**: full-bleed scene with layered elements.
- **Transitions**: CSS `position: sticky` + opacity/scale transforms.
- **Auto-play mode**: `setInterval` or CSS animation delays to cycle frames.

## Rules
- Each frame tells one micro-story.
- Text minimal — 1 headline + 1 sentence max per frame.
- Motion: subtle parallax between background, midground, foreground.
- No JS frameworks — vanilla CSS + minimal JS for scroll detection.
- `data-df-id` on each frame.

## Output
Single `index.html`, inline CSS/JS.
