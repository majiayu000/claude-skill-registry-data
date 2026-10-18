---
name: photo-poster-stylist
description: 当使用者说"把照片做成极简海报"、"做一张几何风格的海报"、"把这张照片抽象成海报"时使用。Turn a photographer-provided description of an existing photo into a minimal, geometric SVG poster with an explicit visual abstraction, restrained palette, grid, typography, bleed, and deterministic validation. Use when the user wants to reinterpret one of their photos as a stylized poster rather than retouch or reproduce the photo.
category: photography
version: 0.1.1
status: draft
priority: P2
compatible_agents:
  - claude-code
  - openclaw
  - cursor
  - codebuddy
  - generic-llm-agent
---

# Photo Poster Stylist

Create a minimal poster from an **existing photo plus the photographer's account of it**. Translate; do not pretend to infer intent that was not supplied.

## Use this skill when

- The user wants a geometric, minimal poster based on one photographed scene.
- The desired deliverable is editable SVG, optionally converted to PNG/PDF by a renderer available in the host environment.
- Human judgment can confirm whether the abstraction still represents the source image.

## Do not use it for

- Photo retouching, compositing, restoration, or faithful vector tracing.
- Inventing a photographer's emotions, symbolism, location, identity, or story.
- A multi-photo layout: use `photo-series-layout` for 3–9 photos on one page, or `photo-spread-composer` for a publication-style spread with bands and credits.
- Work where the user has no right to use the source image or requested branding assets.

## Required inputs

Ask only for missing decisions that change the output:

1. Source: the photo if the environment can inspect images; otherwise a factual description from the photographer.
2. Visual anchors: subject silhouette, dominant light/dark masses, and one detail that must survive abstraction.
3. Output: trim width/height, orientation, and intended medium (screen or print).
4. Copy: title/subtitle/credit exactly as supplied, or confirmation that the poster has no text.
5. Constraints: preferred/forbidden colors, typeface availability, and required bleed.

If image inspection is unavailable, say so and request the three visual anchors. Never fill them in from stereotypes.

## Workflow

### 1. Build an evidence-bound visual brief

Separate inputs into:

- **Observed/provided facts** — objects, approximate positions, colors, light direction, text.
- **Interpretive choices** — crop, geometric simplification, hierarchy, palette reduction.
- **Unknowns** — anything requiring photographer confirmation.

Write one sentence for the concept: “Preserve **X**, reduce **Y** to **Z**, and use **W** as the focal contrast.” Get confirmation when a mistaken anchor would invalidate the design.

### 2. Reduce the image

Make a mass map before drawing details:

1. Choose one dominant silhouette or negative-space shape.
2. Reduce remaining tonal structure to 2–5 supporting masses.
3. Preserve at most one identifying detail.
4. Remove texture that does not affect recognition or rhythm.

Prefer subtraction. Do not reproduce faces or logos as detailed vectors unless explicitly required and authorized.

### 3. Choose the system

Use [references/layout-rules.md](references/layout-rules.md). Default limits:

- no more than 3 visible colors;
- no more than 24 graphic elements, excluding metadata;
- one focal area;
- at most 2 type sizes and 2 font weights;
- all intentional alignments land on the declared grid.

For ordinary text, target contrast ratio 4.5:1; for large text, 3:1. Treat these as accessibility checks, not guarantees of legibility in every print process.

### 4. Produce a poster specification

Create a UTF-8 JSON file accepted by the deterministic renderer:

```json
{
  "width": 1080,
  "height": 1350,
  "bleed": 0,
  "palette": {"background": "#F3EFE6", "foreground": "#151515", "accent": "#D95336"},
  "title": "NORTH WINDOW",
  "subtitle": "Shanghai · 2026",
  "credit": "Photograph: supplied by user",
  "shapes": [
    {"type": "circle", "cx": 760, "cy": 410, "r": 210, "fill": "accent"},
    {"type": "rect", "x": 90, "y": 620, "width": 900, "height": 360, "fill": "foreground"}
  ]
}
```

Allowed shape types are `rect`, `circle`, `ellipse`, `polygon`, and `path`. Colors in shapes may use palette role names or six-digit hex values already present in the palette. Keep paths simple; every shape counts as one element.

### 5. Render and validate

From this skill directory:

```sh
python3 scripts/poster_tool.py render poster.json poster.svg
python3 scripts/poster_tool.py validate poster.svg
```

The script uses only the Python standard library. It checks parseability, dimensions, color count, graphic-element count, text hierarchy, bounds, and foreground/background text contrast. A zero exit status means the deterministic checks passed, not that the design is aesthetically successful.

Bounds are checked in the SVG's viewBox coordinates, so with bleed the canvas runs from `-bleed` to `trim + bleed`: a shape may fill the bleed, but not go past it. Paths are measured by their exact outline (`M L H V C S Q T A Z`, absolute and relative), curves by their extremes rather than their control points. Text is checked with an estimated box (full-width CJK characters 1 em, spaces 0.3 em, other characters 0.6 em): its anchor must be on the canvas and the box inside the trim. Warnings, which do not fail the check, cover text reaching into the 5% side margins of the safe area and, with bleed, a shape that crosses the trim edge but stops short of the bleed edge. The validator rejects `transform`, `style`, and `stroke` attributes, and any element other than `rect`, `circle`, `ellipse`, `polygon`, `path`, `text`, `g`, `title`, `desc`, and `metadata`, because these checks cannot follow them; hand-edited SVG must stay within the renderer's subset. Run `python3 scripts/poster_tool.py --selftest` after changing the script.

If another renderer is available, PNG/PDF conversion is optional. Do not claim those formats were produced unless the conversion was actually run and inspected.

### 6. Human review

Show the SVG and ask the photographer to verify:

- Does the silhouette still identify the intended subject?
- Was the must-keep detail preserved?
- Does any interpretation imply a story not provided?
- Is small text legible at final size?
- For print, are bleed, safe area, color handling, and printer requirements confirmed?

Revise the brief before adding detail. Extra decoration is not the default fix.

## Deliverables

Return:

1. the confirmed one-sentence concept;
2. the editable JSON specification;
3. the SVG poster;
4. the validator result and any unresolved warnings;
5. a short record of factual inputs versus design choices.

## Failure handling

- **No usable visual description:** stop after a neutral input checklist; do not invent the scene.
- **More than three essential colors:** ask which hierarchy matters, or offer two separate three-color directions.
- **Validator failure:** fix the specification and rerender; do not hand-edit around the checker without explaining why.
- **Unsupported SVG feature:** simplify it to supported geometry or validate the external SVG separately.
- **Aesthetic disagreement:** present at most two materially different abstractions and state the tradeoff.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | validate 改按 viewBox 坐标查边界（有出血时满出血形状不再误报、越出出血边的形状不再放过），补 path 精确外框（M/L/H/V/C/S/Q/T/A/Z，含相对命令）和文字估算框检查，transform/style/stroke 等查不了的写法直接报错；加 --selftest；多图排版改点名 photo-series-layout / photo-spread-composer，description 前加中文触发语；目录内测试副本并入 tests/cases 后删除 | patch |
| 0.1.0 | 2026-09-09 | 初始版本 | minor |
