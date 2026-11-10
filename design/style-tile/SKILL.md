---
name: style-tile
zh_name: "风格样张"
en_name: "Style Tile"
emoji: "🎨"
description: "One compact board showing a color and type pairing — palette with contrast, type specimen and scale, core components, radius and spacing — built on the design-token contract so a chosen tile becomes a design system with no loss."
en_description: "One compact board showing a color and type pairing — palette with contrast, type specimen and scale, core components, radius and spacing — built on the design-token contract so a chosen tile becomes a design system with no loss."
category: design-system
scenario: design
tags: ["style tile", "color palette", "type pairing", "brand", "moodboard", "design tokens", "配色", "字体搭配"]
triggers:
  - "style tile"
  - "color and type"
  - "color palette"
  - "type pairing"
  - "font pairing"
  - "brand colors"
  - "visual direction"
  - "配色"
  - "字体搭配"
od:
  mode: design-system
  craft:
    requires:
      - color
      - typography
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Show me four color and type pairings for a calm, trustworthy fintech brand, as style tiles I can compare and then keep one as our design system."
---

# Style Tile

**Intent.** A style tile shows one visual direction (colors, type, the feel of components) on a single board, before anyone designs a page. People compare several side by side and pick one, so each tile must be quick to read and honest about how the system behaves.

Usually you make tiles inside a design exploration: `prepare_open_design_exploration` with this skill gives each tile its direction. A single tile works too.

## The token contract (required)

The tile's `:root` declares the design-token contract, and **everything on the tile is styled through those custom properties**. That is what lets `choose_open_design_direction` with `next: "save-design-system"` copy the tile into `tokens.css` exactly. Declare at least:

- **Identity:** `--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`, `--font-display`, `--font-body`.
- **Type scale:** `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--text-xl`, `--text-2xl`, `--text-3xl`, `--text-4xl`, `--leading-body`, `--leading-tight`, `--tracking-display`.
- **Layout:** `--container-max`, `--container-gutter-phone`, `--container-gutter-tablet`, `--container-gutter-desktop`, `--section-y-phone`, `--section-y-tablet`, `--section-y-desktop`.
- Recommended too: `--accent-on`, `--accent-hover`, `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-pill`, `--elev-raised`, `--font-mono`, `--success`, `--warn`, `--danger`.

Put `data-od-style-tile` on the tile's root element. `check_open_design_artifact` reports every missing required token as `token-missing`.

## What the tile shows

1. **Header:** the direction's name and one line on its mood ("Calm, precise, quietly confident").
2. **Palette:** a swatch per role (`bg`, `surface`, `fg`, `muted`, `border`, `accent`, plus status colors if declared). Each swatch shows its role, hex value, and the contrast ratio of the text that sits on it (for example `fg on bg 14.97:1`). Compute the ratios; don't estimate them. Body text pairs need 4.5:1.
3. **Type specimen:** the display face at `--text-4xl` with a short headline, the body face in a real paragraph at `--text-base`, and the scale from `--text-4xl` down to `--text-xs`, each labelled with its size. Name both families.
4. **Components:** a primary and a secondary button, an input with a label, a card with a title and a line of text, and a tag. All of them use the tokens.
5. **Shape and space:** the radius scale, a spacing ruler and the raised elevation, small.

Fonts come from Google Fonts. The tile is one screen on desktop (about 1200×900) and reflows to a single column on a phone.

## Make tiles different

In an exploration, every tile must differ from every other in at least two of: accent hue family, neutral temperature (warm or cool greys), display face classification (serif, sans, mono, display), and radius scale (sharp, soft, pill). Two blues with the same sans and the same radius aren't two directions.

## Then

When the user picks a tile, call `choose_open_design_direction` with `next: "save-design-system"`. Its instructions carry the tile's tokens verbatim for `tokens.css`; the agent writes `DESIGN.md` to describe them and registers the system, which becomes active.
