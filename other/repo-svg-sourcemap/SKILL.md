---
name: repo-svg-sourcemap
description: Generate zoomable, sourcemap-style SVG diagrams from Markdown or indented outlines (e.g., PROGRESS.md/ROADMAP.md/plan docs). Use when the user asks to "map this repo", "draw a repo diagram", "make an SVG sourcemap", or wants a large navigable visual artifact of a plan/spec.
---

# Repo Svg Sourcemap

## Workflow

### 1) Choose the source

- If the user provides a file path (commonly a `.md` plan/spec like `PROGRESS.md`): render it directly.
- If the user only provides a concept (“represent that”) in chat: first draft a dense outline (headings + nested bullets), then render.

### 2) Render the SVG

```bash
# From a file (great default for this repo: PROGRESS.md)
python3 ~/.codex/skills/repo-svg-sourcemap/scripts/generate_svg_sourcemap.py \
  --in PROGRESS.md \
  --out repo_map.svg \
  --title "Repo plan map" \
  --node-width 440 --h-gap 170 --v-gap 10 --grid-size 80

# From stdin (nice for quick iterations)
cat PROGRESS.md | python3 ~/.codex/skills/repo-svg-sourcemap/scripts/generate_svg_sourcemap.py \
  --in - \
  --out repo_map.svg \
  --title "Repo plan map"
```

The output SVG is standalone and embeds simple JS for wheel-zoom, drag-pan, and click-to-center.

### 3) Tune for “sourcemap” navigation

- Too tall: reduce whitespace via `--v-gap`, or cap depth via `--max-depth`.
- Too cramped: increase `--h-gap` or `--node-width`.
- Viewer can’t run scripts: re-render with `--no-js`.

## Bundled Scripts

### `scripts/generate_svg_sourcemap.py`
- Standard-library Python generator; reads `--in <path|-` and writes `--out <path>` atomically.

### `scripts/generate_svg_sourcemap.sh`
- Bash wrapper that calls `python3` on the Python generator.
