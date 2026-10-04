---
name: game-tilesets
description:
  "For GameGen projects, create and validate game tilesets, terrain transitions and tile metadata for square, isometric
  or hexagonal levels, including optional SpriteCook generation."
---

# Build terrain tilesets

Read [shared context](../../references/shared-context.md), ready preferences and the tileset provider route. Resolve
grid, projection, cell size, terrain layers and the actual adjacency method from the existing project or bootstrap. A
material texture and an autotile sheet have different contracts.

## Produce the required pieces

Use the accepted palette and lighting. For a terrain set include the required filled, empty, edge, outer-corner,
inner-corner and isolated cases for the selected algorithm. Match joins at native resolution and avoid an obvious
repeated stamp. Keep decorative props separate from terrain collision.

When using SpriteCook, read `spritecook-workflow-essentials` and `spritecook-generate-tilesets`. Query current tileset
options, preserve reference/edit/style ID semantics, use supported piece sets, and save the returned IDs, layout and
dimensions. A model stored in preferences is an explicit project choice; validate its support. Respect inherited
settings when a provider locks the size or layout for referenced assets.

For SpriteCook's 15-piece dual-grid set, read `spritecook-use-dual-grid-tilesets` before implementation. Do not feed its
indices directly into a different Godot terrain-mask convention. For square, isometric and hex layouts, derive
placement, adjacency and collision from the selected coordinate system.

## Verify in a map

1. Create a compact coverage map exercising every supported edge/corner and terrain transition, plus narrow passages and
   isolated cells.
2. Check gaps, seams, transparency, filtering, atlas bleed and the correct half-cell offsets where the algorithm uses
   them.
3. Separate logical occupancy, visual tiles, collision and navigation. Check transitions between chunks as well as
   inside a chunk.
4. Verify height layering, depth sorting and walkable entrances for isometric or elevated terrain. Keep visual
   projection and gameplay movement consistent.
5. Inspect at the intended zoom and device aspect ratio. Measure large-map costs through
   [game-optimization](../game-optimization/SKILL.md) before expanding the terrain library.

Store the piece-to-mask map, tile dimensions, collision/navigation layers, palette/reference revision and output hashes
with the asset. Handoff a playable test map and actual engine capture, not only a tileset PNG.
