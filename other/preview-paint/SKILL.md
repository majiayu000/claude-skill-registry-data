---
name: preview-paint
description: Preview one specified wall or architectural surface in an exact paint color while preserving materials, lighting cues, furniture, and room design. Use for reversible paint-color visualization; do not use for full room restyling, object recoloring, material replacement, or structural renovation.
---
# Preview Paint

## Catalog

- Display name: Preview Paint
- Categories: Layout & Design
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: yellow
- Short description: Preview one specified wall or architectural surface in an exact paint color without redesigning the room.
## What this skill does

- Changes only declared paintable surfaces and respects trim, fixtures, openings and material boundaries.
- Simulates color under source lighting instead of replacing texture or flattening shadows.

## How to use

Provide a room photo, target surface, paint name or color value, finish and protected surfaces.

#### Example

```text
Change only the back wall to muted sage #9AA58D in eggshell; keep trim, ceiling, artwork and lighting unchanged.
```

## Workflow

1. Identify each paintable plane and protected edge; resolve ambiguous walls before editing.
2. Convert color and finish into material-aware instructions under source illumination.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Check edge containment, color family, shadow continuity and unchanged non-target surfaces.

## User-facing output

- Media type: One paint preview
- Default quantity: 1
- Content per image: The same space with only the selected surface recolored
- Default layout: Source-preserving or dimension-defined format
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Paint selection and renovation previews
