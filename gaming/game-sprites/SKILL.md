---
name: game-sprites
description:
  "For GameGen projects, produce and integrate pixel, painted, cutout or Blender-rendered game sprites with consistent
  identity, directions, pivots, alpha and atlas metadata."
---

# Produce game sprites

Read [shared context](../../references/shared-context.md), ready preferences and
[provider routing](../../references/providers.md). Inspect the accepted identity and select the sprite mode from
presentation settings. Use game-tilesets for terrain adjacency rather than treating terrain as unrelated decorative
sprites.

## Choose the appropriate source

- Pixel art: preserve intentional pixel clusters, palette, consistent pixel density and nearest-neighbor presentation.
  Inspect at native resolution as well as enlarged.
- Painted or HD sprites: preserve edge quality, transparent margins and the selected texture filtering. Do not assume
  every 2D game should use pixel filtering.
- Cutout characters: retain editable layers, clear joint overlaps and stable attachment/pivot positions for the rig.
- Blender-rendered sprites: use one consistent source model and a rig when the animation needs one, following
  [blender-game-assets](../blender-game-assets/SKILL.md). Keep camera/projection/light fixed and share render bounds
  across directions and actions. Render local `bpy` batches using the
  [Blender execution workflow](../../references/blender-cli.md). Bake any stateful simulations before rendering
  independent frame ranges, and preserve real alpha in the output sequence.

Use the configured route. For SpriteCook, read `spritecook-workflow-essentials` plus `spritecook-generate-sprites`,
`spritecook-upload-assets` and `spritecook-use-assets-in-godot` as applicable. Use the canonical approved source asset
for edits and animations; persist provider IDs. Use actual output dimensions rather than the requested dimensions when
slicing.

## Build a coherent sprite set

1. Set canvas and frame dimensions, grounded pivot, viewing directions, palette and lighting from preferences or the
   asset contract. Account for asymmetric details before mirroring.
2. Generate or draw one representative sprite and inspect it in the intended camera and background before a batch.
   Preserve identity across directions.
3. Verify real alpha, edge halos on light/dark backgrounds, consistent scale and sufficient padding for motion. A
   checkerboard baked into an image is not transparency.
4. Pack frames with explicit layout, columns, count, dimensions and padding/extrusion. Preserve untrimmed frames or trim
   offsets so animations do not jitter. Keep source masters outside runtime assets.
5. For animation, use game-animation and record fps/looping per clip. Never infer all animation timings from the
   sprite-sheet dimensions.
6. Import into Godot with SpriteFrames/AnimatedSprite2D, AnimatedSprite3D, a cutout rig or a suitable custom component.
   Use the actual frame metadata; do not assume every sheet is one horizontal row.

Use `scripts/asset_audit.py` to check PNG dimensions and declared frame layout. Inspect actual playback and collisions
separately. Provide both the editable source/manifest and an engine capture at native gameplay scale.
