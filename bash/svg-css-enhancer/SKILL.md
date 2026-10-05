---
name: svg-css-enhancer
description: Enhance existing SVG files by injecting CSS (themes, hover highlighting, outlines, typography tweaks) and optional element normalization (ids/classes/titles) to make diagrams more informative and navigable. Use when a user provides an SVG and asks to restyle it, improve readability/contrast, add interactive hover emphasis, or generate a “debug/inspector” version without re-drawing the vector art.
---

# Svg Css Enhancer

## Overview

Turn a “plain” SVG into a more informative asset by adding a CSS preset (or your own CSS) and, optionally, adding ids/classes/titles so CSS can target elements reliably.

## Options (what the skill can do)

- **CSS injection only**: Insert a `<style>` block into the SVG (`<defs><style>...`) to theme colors, fonts, and add `:hover` highlighting.
- **CSS + normalization**: Add stable `id` values, append helpful classes (by tag/type), and add `<title>` tooltips so the SVG becomes inspectable and easy to style.
- **Background + framing**: Optionally insert a background `<rect>` (styling lives in CSS) so the SVG reads well on dark/light surfaces.
- **Presets**: Ship a few CSS presets (dark inspector, print-clean, neon/high-contrast), and allow custom CSS input.

## Quick start

Render an “inspector” version with hover highlighting:

```bash
python3 scripts/svg_css_enhance.py \
  --in diagram.svg \
  --out diagram.inspector.svg \
  --preset inspector-dark \
  --ensure-ids --add-classes --ensure-titles --add-background
```

Apply your own CSS file:

```bash
python3 scripts/svg_css_enhance.py \
  --in diagram.svg \
  --out diagram.styled.svg \
  --css my_styles.css
```

List what’s inside an SVG (ids/classes/tags) before deciding what CSS to write:

```bash
python3 scripts/svg_css_enhance.py --in diagram.svg --report
```

## Presets

- `inspector-dark`: dark background + hover highlight + crisp text defaults
- `print-clean`: minimal styling for export/print (no dark background)
- `neon-sourcemap`: high-contrast “sourcemap” look

Presets live in `assets/presets/`. You can copy/edit them or pass your own CSS via `--css`.

### scripts/
Contains the transformer CLI:
- `scripts/svg_css_enhance.py`

### assets/
CSS presets:
- `assets/presets/*.css`
