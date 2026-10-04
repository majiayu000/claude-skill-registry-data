---
name: game-sprite-design
description: Design, generate, animate, export, and review game-ready 2D sprites and sprite pipelines. Use when Codex is asked about pixel art, 2D character sprites, enemy sprites, sprite sheets, animation frames, texture atlases, tile sets, autotiles, UI icons, item icons, VFX sprites, transparent backgrounds, frame grids, pivots/origins, hitboxes, Phaser sprites, Aseprite exports, Tiled tilesets, or HTML5 game-ready 2D assets.
license: MIT
---

# Game Sprite Design

## Core Workflow

1. Identify target engine/framework, art style, camera scale, tile/grid size, target resolution, animation needs, palette constraints, and export format.
2. Define the sprite's gameplay job before visual detail: player, enemy, pickup, projectile, hazard, tile, prop, UI icon, VFX, portrait, or cursor.
3. Establish readability at gameplay size: silhouette, value contrast, color grouping, facing direction, animation key poses, and separation from background.
4. Plan the asset structure: single PNG, frame sequence, uniform sprite sheet, trimmed atlas with JSON, tile sheet, or layered source file.
5. Generate or draw with consistency constraints: same view angle, lighting, outline style, palette, proportions, frame size, and transparent background.
6. Export with game-ready metadata: frame dimensions, tags/animation names, padding, optional edge extrusion, pivot/origin notes, hitbox guidance, and import instructions.
7. Verify inside the target engine at actual scale, with animation looping and neighboring frames/tiles checked for bleeding, jitter, and readability.

## Creative Priorities

- Silhouette: the sprite should read at final pixel size.
- Palette: use a controlled palette and intentional contrast; avoid noisy gradients for pixel art.
- Consistency: maintain perspective, line weight, lighting, proportions, and outline style across variants.
- Animation: start with key poses; add in-betweens only where they improve feel.
- Directionality: make facing, attack, damage, interaction, and movement states clear.
- Background separation: test against real game backgrounds, not only transparent or checkerboard previews.

## Production Priorities

- Use consistent frame dimensions unless the engine/importer expects trimmed atlas metadata.
- Add padding between frames and border padding around sheets to avoid texture bleeding.
- Use edge extrusion for atlases when filtering/scaling can sample neighboring pixels.
- Preserve source files separately from exported sheets.
- Use animation tags or clear naming for idle, walk, run, jump, attack, hit, death, interact, and special states.
- Define pivot/origin consistently, such as feet center for characters, center for projectiles, or top-left for tiles.
- Keep hitboxes/hurtboxes aligned to gameplay, not full visual bounds.
- For tilesets, define tile size, collision, terrain transitions, animated tiles, and autotile/terrain rules where relevant.

## Freshness Rule

Verify current tool and engine docs before giving version-sensitive export/import advice about Phaser, Aseprite, TexturePacker, Tiled, Unity, Godot, sprite atlas formats, filtering, or tilemap behavior.

## Deliverable Shape

For sprite work, provide:

- Sprite purpose and gameplay read
- Art style, palette, perspective, and scale
- Frame/tile dimensions and export format
- Animation list with frame counts/timing
- Sheet/atlas layout and metadata notes
- Pivot, collision, hitbox, and origin guidance
- Engine import and QA checklist

## References

- Read `references/sprite-production-checklist.md` when designing, generating, exporting, or reviewing sprites, sprite sheets, tile sets, or atlases.
