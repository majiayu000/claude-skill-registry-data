---
name: wireframe-sketch
description: |
  Low-fidelity wireframe sketch with placeholder blocks, annotation labels,
  and grayscale palette. Use for "wireframe", "low-fi", "sketch", "concept".
triggers:
  - "wireframe"
  - "wireframes"
  - "low fidelity"
  - "lo-fi"
  - "sketch"
  - "concept"
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

# Wireframe Sketch Skill

Produce a low-fidelity wireframe page.

## Rules
- **Grayscale only**: white, light gray (#f5f5f5), mid gray (#ccc), dark gray (#666),
  black (#111).
- **No real content**: use squiggly lines for text, rectangles for images,
  X for placeholders.
- **Annotation labels**: small mono text describing each block
  ("Header nav", "Hero image", "Feature card", "CTA button").
- **Layout grid**: faint 8px or 12px grid background.
- Boxes have 1px dashed borders.

## Output
Single `index.html`, inline CSS. Annotation layer toggleable.
