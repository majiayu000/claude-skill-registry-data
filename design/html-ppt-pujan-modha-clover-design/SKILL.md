---
name: html-ppt
description: |
  HTML Presentation Studio — author slide decks as static HTML files with
  keyboard navigation, themes, animations, and presenter mode. Use for
  "presentation", "ppt", "slides", "deck", "keynote", "pitch deck".
triggers:
  - "ppt"
  - "deck"
  - "slides"
  - "presentation"
  - "keynote"
  - "reveal"
  - "slideshow"
  - "pitch deck"
  - "tech sharing"
  - "technical presentation"
df:
  mode: deck
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# HTML-PPT Skill

Author professional HTML presentations as static files.

## Before you start — confirm 3 things
1. **Content & audience** — topic, slide count, who's watching.
2. **Style / theme** — recommend 2–3 from:
   - Business: corporate-clean, swiss-grid
   - Tech: tokyo-night, dracula, terminal-green
   - Creative: cyberpunk-neon, vaporwave, neo-brutalism
3. **Starting point** — pitch-deck, tech-sharing, weekly-report, product-launch.

## Structure
- One `.slide` per logical page. `is-active` class toggles visibility.
- Wrap speaker notes in `<div class="notes">...</div>` inside each slide.
- Never put presenter-only text on the slide itself.

## Keyboard shortcuts
- ← → Space: navigate
- F: fullscreen
- T: cycle theme
- S: presenter mode (current/next/script/timer)

## Output
Single `index.html` with inline CSS/JS. No build step.
