---
name: svg-sourcemap
description: Generate detailed, zoomable, sourcemap-style SVG diagrams from Markdown or indented text outlines. Use when the user asks to "create an svg to represent that", wants a large navigable visual artifact they can zoom/pan deeply, or requests a "sourcemap" style map/diagram of a plan/spec/document (especially .md files) without requiring pretty styling.
---

# Svg Sourcemap

## Workflow

### 1) Choose the source

- If the user provides a file path (commonly a `.md` plan/spec): render it directly.
- If the user only provides a concept (“represent that”) in chat: first draft a dense outline (headings + nested bullets), then render.

### 2) Render the SVG

```bash
# From a file
./scripts/generate_svg_sourcemap.sh \
  --in PLAN.md \
  --out artifact.svg \
  --title "PLAN map"

# From stdin
cat outline.md | ./scripts/generate_svg_sourcemap.sh \
  --in - \
  --out artifact.svg \
  --title "Sourcemap"
```

The output SVG is standalone and embeds simple JS for wheel-zoom, drag-pan, and click-to-center.

### 3) Tune for “sourcemap” navigation

- Prefer *more nodes* over summarizing; keep each heading/bullet as its own node.
- If it’s too tall: reduce whitespace via `--v-gap`, or cap depth via `--max-depth`.
- If edges overlap too much: increase `--h-gap` or `--node-width`.
- If scripts aren’t allowed in the viewer: re-render with `--no-js` (still viewable; zoom depends on viewer UI).

## Bundled Scripts

### `scripts/generate_svg_sourcemap.py`
- Standard-library Python generator; reads `--in <path|-` and writes `--out <path>` atomically.

### `scripts/generate_svg_sourcemap.sh`
- Bash wrapper that calls `python3` on the Python generator.
