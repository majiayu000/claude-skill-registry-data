---
name: make-silhouette
description: Convert one named subject into a clean solid silhouette while preserving its recognizable outer contour and requested background or transparency. Use for people, animals, products, icons, or cut-paper profile shapes.
---
# Make Silhouette
## Catalog
- Display name: Make Silhouette
- Categories: Social Media, Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: slate
- Short description: Turn a subject into a recognizable silhouette.
## What this skill does
- Isolates one target and converts its interior to a uniform fill.
- Preserves gesture-defining contour details and optional negative spaces.
## How to use
Provide source, target, fill color, background, and internal cutout rule.
#### Make a silhouette
```text
Turn only the cyclist into solid black on the sunset; retain bicycle spoke gaps.
```
## Workflow
1. Define target contour, important negative spaces, ground contact, and background.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Fill target uniformly; do not darken the whole image.
4. Inspect edge continuity, accessories, negative spaces, halos, holes, and recognizable pose.
5. Hand off to `$remove-background` when transparent alpha is requested.
## User-facing output
- Media type: One silhouette image
- Default quantity: 1
- Content per image: One target silhouette
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Icons, posters, and profile graphics
