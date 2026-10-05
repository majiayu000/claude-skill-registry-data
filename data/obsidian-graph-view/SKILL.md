---
name: obsidian-graph-view
description: Render Obsidian-style weighted graph views from book JSON, keyword indexes, TOCs, card data, or node-link data. Use when the user asks for Obsidian graph view, graph view png, weighted graph, keyword graph, directory-keyword graph, spherical graph visualization, or high-weight nodes centered with clear Chinese labels.
---

# Obsidian Graph View

Create an Obsidian-like graph visualization from structured note/book data.

## Default Output

Produce three files when possible:

- `*.png` for direct viewing and sharing
- `*.svg` for editable vector output
- `*.html` for browser re-rendering

Prefer PNG dimensions around `1800 x 1300` unless the user asks otherwise.

## Visual Rules

- Put higher-weight nodes closer to the center.
- Push lower-weight nodes to outer rings.
- Use a spherical / ball-like node style with radial glow.
- Use different colors for different main Trails / note-sequence lines.
- If a node belongs to two Trails, render it as a two-color taiji-like sphere to show a note-sequence crossing point.
- Keep labels in Traditional Chinese readable: use large `PingFang TC` / `Heiti TC` / system CJK fonts, white text, dark translucent label boxes, and avoid placing labels directly on dark edges.
- Use a dark Obsidian-like background.
- Use node area, not radius, to represent weight. If the user says "放大兩倍面積", double the computed node area.
- Use semantic Trail colors rather than only node-type colors when main lines are available.
- Prefer undirected soft lines for Obsidian-style graph view; use arrows only if the user asks for directional semantics.
- Keep top-node count configurable. If the user corrects the count, update the graph and file names accordingly.

## Data Mapping

For EPUB/project-note JSON:

- `toc[]` becomes chapter or directory nodes.
- `index[]` becomes keyword nodes.
- `index[].links[]` becomes keyword-to-chapter edges.
- `toc[].cjk_count`, keyword `weight`, and index link weights contribute to node size.
- `chunks[].keyword_backlinks[]` can be used to enrich link weights.

For generic graph JSON:

- Accept `nodes[]` with `id`, `label`, `weight`, and optional `kind`.
- Accept `edges[]` with `source`, `target`, and optional `weight`.

## Workflow

1. Inspect the JSON schema and identify node candidates, weights, and links.
2. Select the top `N` nodes by descending weight; default to 15 if the user asks for a focused graph.
3. Lay out nodes with the largest weight at center, next largest on an inner ring, and lower weights on outer rings.
4. Render SVG and HTML first.
5. Use headless Chrome or another reliable renderer to export PNG.
6. Verify the PNG file dimensions and visually inspect if possible.

## Trail Color Semantics

When the data does not already provide Trail groups, infer them from repeated keywords, chapter labels, or user-provided concepts. For example:

- `危機演化線`: 馬爾薩斯、達爾文、危機、演化
- `夢想救援線`: TARS、Brand、Plan A、夢想、救援
- `檢查背叛線`: 曼恩、異常、數據、背叛、檢查
- `卡片系統線`: Agent、Skill、卡片盒、半人馬、五維空間

If a node matches two Trail groups, draw it as a two-color taiji sphere and keep the label explicit.

## Script

Use `scripts/render_obsidian_graph_view.py` as the starting point for JSON-to-SVG/HTML/PNG graph rendering. Patch the script for project-specific schemas rather than rewriting from scratch.
