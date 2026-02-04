---
name: art-pipeline
description: Deterministic toon pipeline palettes, ramps, sprite baking, battle backgrounds
compatibility: opencode
---

# Skill: Art pipeline (deterministic)

## Objective

Create a pipeline that produces consistent visuals as the world expands.

## Outputs

- `art/palettes/...` palette json files
- `art/ramps/...` toon shading ramps
- `art/exports/...` baked outputs
- `game/assets/...` runtime imports

## Steps

1. Create versioned templates

- Blender toon material template
- Character rig + camera rigs for sprite baking
- Battle background diorama template

2. Use recipe files

- `art/recipes/<type>/<id>.yml` with tool versions, seeds, and source paths

3. Build validation scripts

- Validate naming, dimensions, palette compliance

## Acceptance checks

- Two assets generated from the same template look like the same "artist"
- Adding a new biome only requires adding a biome pack (palette + prop kit + backgrounds) without re-authoring the whole style
