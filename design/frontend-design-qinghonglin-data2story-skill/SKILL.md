---
name: frontend-design
description: "Reusable UI/visual-design system for building polished, distinctive, multimedia-rich self-contained HTML stories. A shared reference library that the Data2Story Designer and Programmer borrow from so every blog looks intentional and editorial rather than generic. Not a pipeline stage — a design source."
allowed-tools: Read
---

# Frontend Design

A shared design system for building **beautiful, distinctive, multimedia-rich** HTML stories. This is not a pipeline stage; it is a library the **Designer** reads to choose a visual language and the **Programmer** reads to implement it, so output looks like an editorial product, not a default template.

## When to use

- **Designer**: before writing `page_rhythm` and per-section visuals, pick a theme and component vocabulary from here. Borrow tokens, layout, and component recipes; record the chosen theme in `designer.json` `page_rhythm`.
- **Programmer**: implement the chosen theme's tokens as CSS `:root` variables and build each visual with the matching component recipe and motion/accessibility rules here.

## Core principles

1. **Editorial, not generic.** Avoid the default-AI look (bootstrap blue, purple gradient hero, everything centered, one system font, evenly-spaced soulless cards). Commit to one bold idea per story. See [`references/themes.json`](references/themes.json) → `anti_patterns`.
2. **Rich media by default.** A story should use multiple channels well — charts, images, video, audio, interactives/maps — each presented with craft, not dumped in. See [`references/media_presentation.json`](references/media_presentation.json).
3. **One system, themed per story.** All color/type/space/shadow flow from CSS `:root` tokens so the whole page is coherent and re-themeable. See [`references/design_tokens.json`](references/design_tokens.json).
4. **Structure carries the reading.** A clear content column, deliberate full-bleed moments, and consistent section rhythm. See [`references/layout.json`](references/layout.json).
5. **Motion and access are part of the design.** Subtle scroll reveals and transitions, always respecting `prefers-reduced-motion`, AA contrast, focus states, and "never autoplay sound." See [`references/interaction.json`](references/interaction.json).
6. **Self-contained.** Single HTML file; allowed CDNs only (Vega-Embed, Leaflet, optionally D3/PDF.js); inline data; works on `file://`.

## References

- **[`references/design_tokens.json`](references/design_tokens.json)** — color roles, data-color scales, fluid type scale, spacing/radius/shadow, themed via `:root`.
- **[`references/layout.json`](references/layout.json)** — content column, full-bleed breakout, section rhythm, responsive grid, sticky patterns.
- **[`references/components.json`](references/components.json)** — recipes: hero/teaser, stat callouts, card deck, pull quote, chart/map frames, audio players, scrollytelling, before/after, guess-reveal, data table, references footer.
- **[`references/media_presentation.json`](references/media_presentation.json)** — how to present each channel (image, video, audio, chart, map, instance) richly, and the "all five channels by default" doctrine.
- **[`references/themes.json`](references/themes.json)** — ready-made distinctive themes (token presets) and the anti-patterns to avoid.
- **[`references/interaction.json`](references/interaction.json)** — motion, scroll reveal, transitions, accessibility, reduced-motion, performance.

A story is well-designed when it commits to one clear visual identity, uses several media channels with craft, reads cleanly on mobile and desktop, and could not be mistaken for a default template.
