---
name: social-carousel
description: |
  A 3-card social-media carousel laid out as 1080×1080 squares.
  Connected headlines, cinematic gradients, drop-into-Instagram ready.
triggers:
  - "social carousel"
  - "carousel post"
  - "instagram carousel"
  - "linkedin carousel"
  - "x thread cards"
  - "social series"
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

# Social Carousel Skill

Produce a 3-panel social carousel on a single dark stage.

## Workflow
1. Read DESIGN.md. Pick loudest serif for headlines, mono for stamps.
2. Pick theme + 3 captions that read as one sentence:
   ("onwards." → "to the next one." → "looking ahead.")
3. **Stage**: full-bleed dark. Header strip with serif italic title
   + mono description + "SERIES · 01 → 03" badge.
4. **Cards**: 3 squares (`aspect-ratio: 1/1`), rounded 12px.
   - Background: layered radial+linear gradients (no images).
   - Top-left: brand wordmark + micro index "AI · 01/03".
   - Bottom-left: headline lockup, italic accent on one word.
   - Bottom-right: "1× LOOP" mono stamp.
5. **Self-check**:
   - Headlines form one sentence, feel cinematic.
   - Each panel's color story is distinct.
   - Mono only for index, stamp, captions.

## Output
Single `index.html`, inline CSS. Cards sized via `clamp(280px, 30vw, 380px)`.
