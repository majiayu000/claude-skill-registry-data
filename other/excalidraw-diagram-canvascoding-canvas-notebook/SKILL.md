---
name: excalidraw-diagram
description: Create or edit Canvas Notebook .excalidraw files for diagrams, flows, sketches, architecture maps, and visual explanations. Use when the user asks for an Excalidraw drawing, diagram, board, sketch, canvas, flowchart, architecture diagram, or when a file ending in .excalidraw should be generated. Output only the .excalidraw file unless the user explicitly asks for another artifact.
---

# Excalidraw Diagram

Create valid `.excalidraw` JSON files directly in the workspace. Canvas Notebook renders these files itself, so the deliverable is the file, not a PNG, SVG, markdown note, or separate explanation file.

## Output Contract

- Write exactly one `.excalidraw` file at the requested path or in the current/requested folder.
- Do not create a sidecar `.md`, `.png`, `.svg`, or README unless the user explicitly asks.
- If the user provides Mermaid syntax, use it only as source material and create the final `.excalidraw` file directly. Do not save a separate `.mmd` file unless explicitly requested.
- If a textual explanation is useful, put it in the chat response only.
- Set the root `source` to `canvas-notebook`.
- Prefer vector Excalidraw elements over embedded images. Use `files` only when image data is actually required and available.

## File Shape

Use this root structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "canvas-notebook",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

Canvas Notebook reads `elements`, `appState`, and `files` as Excalidraw `initialData`. Empty `elements` is valid, but a requested diagram should contain useful elements.

## Workflow

1. Determine the target `.excalidraw` path. If the user gave a folder, create a descriptive kebab-case filename ending in `.excalidraw`.
2. Understand what the diagram must communicate. For technical diagrams, inspect relevant files or docs first so names, APIs, and relationships are real.
3. If the source is Mermaid, translate its nodes, edges, labels, and diagram direction into Excalidraw elements; preserve the meaning but improve spacing and readability for Excalidraw.
4. Plan the visual structure before writing JSON. Use layout to show relationships, not just equal boxes with labels.
5. Write complete Excalidraw JSON. Use stable, descriptive IDs such as `api_gateway_rect` or `flow_to_worker`.
6. Validate the file:

```bash
python3 seed_skills/excalidraw-diagram/scripts/validate_excalidraw.py path/to/file.excalidraw
```

If the skill is installed elsewhere, run the same script from that skill folder.

7. Fix validation errors. If browser or Playwright verification is explicitly allowed, open the file in Canvas Notebook and visually check for overlaps, clipped text, and incorrect arrows.

## Diagram Quality

- Use visual patterns that match meaning: timelines for sequences, fan-out for one-to-many, convergence for aggregation, nested regions for ownership, and side-by-side layouts for comparisons.
- Avoid uniform card grids unless the concept is actually a collection of peers.
- Use arrows or lines for relationships that matter.
- Keep text short and readable. Use free-floating labels when a container adds no meaning.
- Make technical diagrams educational by including concrete examples: real endpoint names, event names, filenames, data shapes, or short code snippets where relevant.
- Keep everything within a coherent bounding box and leave generous margins.

## Element Rules

Every element should have these common fields:

- `id`, `type`, `x`, `y`, `width`, `height`
- `angle`, `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`
- `roughness`, `opacity`, `seed`, `version`, `versionNonce`, `isDeleted`
- `groupIds`, `boundElements`, `link`, `locked`

For text elements:

- Set both `text` and `originalText`.
- Use `fontSize`, `fontFamily`, `textAlign`, `verticalAlign`, and `lineHeight`.
- Useful font IDs: Excalifont `5`, Helvetica `2`, Cascadia `3`, Nunito `6`.
- For code or JSON snippets, use Cascadia `3`.

For arrows and lines:

- Set `points` with at least two `[x, y]` pairs.
- For arrows, set `startArrowhead` and `endArrowhead`.
- If using `startBinding` or `endBinding`, the referenced element IDs must exist.

For bound text:

- Shape `boundElements` should reference the text element.
- Text `containerId` should reference the shape.
- Keep text dimensions large enough that Canvas Notebook will not render clipped labels.

## Defaults

- Background: `#ffffff`
- Primary stroke: `#1f2937`
- Secondary stroke: `#475569`
- Muted stroke: `#94a3b8`
- Primary fill: `#e0f2fe`
- Success fill: `#dcfce7`
- Warning fill: `#fef3c7`
- Error fill: `#fee2e2`
- Neutral fill: `#f8fafc`
- Code fill: `#111827`
- Code text: `#e5e7eb`

Use color for meaning, not decoration.

## Editing Existing Files

When updating an existing `.excalidraw` file:

- Preserve unknown root fields and existing `files` entries unless replacing them is necessary.
- Preserve existing element IDs when modifying elements.
- Do not overwrite an invalid existing file unless the user asked to replace or initialize it.
