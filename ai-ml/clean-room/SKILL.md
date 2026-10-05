---
name: clean-room
description: Remove specified clutter from a room photograph with an AI-native contextual edit while preserving architecture, fixed furniture, perspective, materials, lighting, and the room's identity. Use for real-estate, hospitality, or interior cleanup, not redesign or restyling.
---
# Clean Room
## Catalog
- Display name: Clean Room
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: green
- Short description: Remove room clutter without redesigning the space.
- Similar skills: remove-object, restyle-room
## What this skill does
- Removes a declared clutter set as one coherent cleanup result.
- Reconstructs floors, walls, textiles, and surfaces while preserving architecture and fixed furnishings.
## How to use
Provide room photo and list removable clutter versus protected furniture and decor.
#### Clean a bedroom
```text
Remove clothes, cables, cups, and loose papers; keep all furniture, plants, art, bedding, and room layout.
```
## Workflow
1. Inventory removable clutter and protected structure, furniture, decor, textiles, windows, doors, and fixtures.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Request one spatially coherent cleanup; forbid redesign, new furniture, staging, material changes, or relighting.
4. Inspect perspective lines, floor/wall continuation, reflections, shadows, repeated textures, furniture count, and room proportions.
5. Reject missing protected items, added decor, warped architecture, floating furniture, or over-empty staged results.
## User-facing output
- Media type: One cleaned room image
- Default quantity: 1
- Content per image: Same room with specified clutter removed
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Real-estate, hospitality, and interior listings
