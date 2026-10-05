---
name: svg-styled-sourcemap
description: Generate zoomable SVG “sourcemap” diagrams from Markdown/outlines and produce a styled (readable, semantic-colored, hover-highlighted) SVG variant. Use when users ask to create a repo/plan map from files like PROGRESS.md/ROADMAP.md/specs, to combine multiple Markdown docs into one SVG, or to improve the readability/style of an existing sourcemap-style SVG.
---

# Svg Styled Sourcemap

## Workflow

### 1) Generate a styled sourcemap (default path)

Use `scripts/generate_styled_sourcemap.py` (or `.sh`) to:
1) combine one-or-more Markdown inputs into a single outline,
2) render a zoomable SVG sourcemap,
3) inject a styling preset + element normalization (ids/classes/titles/background).

```bash
python3 scripts/generate_styled_sourcemap.py \
  --in PROGRESS.md \
  --out progress_map.styled.svg \
  --title "Repo plan map" \
  --max-depth 4
```

Combine multiple docs (each becomes its own “section” under a root node):

```bash
python3 scripts/generate_styled_sourcemap.py \
  --in PROGRESS.md \
  --in ai_docs/PREVIEW_CALL_ID_DEDUPE_DECISION.md \
  --out plan_plus_decision.styled.svg \
  --title "PROGRESS + Decision"
```

### 2) Tune layout + noise

- Reduce clutter: keep the default outline filter, or increase `--max-depth`.
- More detail: pass `--keep-all-lines` (includes non-bullet paragraphs as nodes).
- Too tall: increase `--max-depth`, increase `--node-width`, or reduce `--v-gap`.
- Too cramped: increase `--h-gap` or `--node-width`.

### 3) Choose a style preset (or custom CSS)

Presets live in `assets/presets/*.css` and are applied via `--style-preset`:

- `kimojo-sourcemap` (default): semantic colors for headings/items/text + stronger edges + hover.
- `inspector-dark`: darker inspector-style hover highlighting.
- `neon-sourcemap`: high-contrast neon accents.
- `print-clean`: white background + dark text for export/print.

Example:

```bash
python3 scripts/generate_styled_sourcemap.py \
  --in PROGRESS.md \
  --out progress_map.print.svg \
  --title "Repo plan map" \
  --style-preset print-clean
```

To add extra CSS on top of a preset, pass `--style-css path/to/extra.css`.

### 4) Advanced: restyle an existing SVG (no re-render)

If the SVG already exists and you only need styling/inspectability, run:

```bash
python3 scripts/svg_css_enhance.py \
  --in diagram.svg \
  --out diagram.styled.svg \
  --preset kimojo-sourcemap \
  --ensure-ids --add-classes --ensure-titles --add-background
```
