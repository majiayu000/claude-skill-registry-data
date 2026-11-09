---
name: create-game-art-sheets
description: Plan and specify production-ready game art sheets, including environment tilesets, biome/terrain sets, autotile sets, prop atlases, and directional character animation sheets with 4, 6, 8, 16, or custom facing counts. Use when art roles need to create tilesets or sprite animation sets before implementation handoff.
engines: [AGNOSTIC]
---

## When to use
Use when creating or reviewing tilesets, environment sets, prop sheets, character sprite sheets, creature animation sheets, equipment overlays, directional attack sets, or isometric movement/animation sheets.

## Workflow
1. Read `../STYLE.md` and the relevant `.styles` templates before planning the sheet.
2. Decide whether the deliverable is a tileset, prop/object atlas, directional animation sheet, VFX sheet, or mixed package.
3. For tilesets, define tile dimensions, grid orientation, terrain families, transitions, variants, collision/walkability metadata, elevation rules, and atlas grouping.
4. For animation sheets, choose between one-action-per-file sheets, one combined character atlas, equipment overlay sheets, or engine-native atlas packing.
5. For animation sheets, define direction count, facing names, frame size, anchor/contact point, direction rows, frame columns, action file names, loop rules, timing, and gameplay events.
6. When a local sample exists, inspect it and follow its reusable layout conventions unless the user asks to change them.
7. For isometric sheets, include projection, tile footprint, elevation unit, stable foot anchors, draw-order expectations, contact shadows, and readable facings.
8. Produce a manifest-ready contract before final art creation so engineering, design, QA, and documentation can validate the same assumptions.
9. Pair this skill with `prepare-game-art-handoff` when the sheet is ready for runtime integration.

For reference-derived sets, use `plan-hybrid-game-assets` to declare reference contributions and invariant features. Before handoff, read [content review](references/content-review.md) for frame-specific evidence, actual transparency, semantic anchors, loop playback and assembled tile/parallax checks.

## Sample-Driven Sheet Profile
When the host repository contains a sample like `assets/sky-knight`, use it as a local style/layout reference after inspection:

- one action per PNG file
- kebab-case action names such as `idle.png`, `run.png`, `cast-spell.png`, `take-damage.png`, and `shield-block-start.png`
- 8 direction rows
- 15 frame columns per action
- 128x128 frame cells
- 1920x1024 total sheet dimensions
- transparent PNG background
- stable anchor/contact point across all actions and facings

Do not hard-code this profile for every project. Treat it as the preferred local convention only when the user provides or selects it.

## Direction Sets
- 4-direction: north, east, south, west; use for simple top-down or grid movement.
- 6-direction: useful for hex grids, stylized tactical games, or constrained facings; document exact facing angles.
- 8-direction: common for top-down/isometric movement; include cardinal and diagonal facings.
- 16-direction: use only when rotation fidelity, aiming, vehicles, bosses, or high-resolution facings justify the asset cost.
- Custom direction counts must document angle degrees, row order, mirrored frames, and whether mirroring is allowed.

## Tileset Contract
- tile size and orientation
- base terrain tiles
- edge, corner, inner-corner, diagonal, cliff, shoreline, road, stair, wall, roof, and water transitions
- biome variants and decoration frequency
- walkable, blocker, hazard, cover, interactable, objective, and spawn metadata
- atlas padding, naming, tile IDs, and source/runtime paths
- seam stress-test layouts

## Animation Contract
- entity scale, frame size, transparent padding, and anchor point
- direction count and row order
- sheet packaging: one action per file or combined atlas
- action filename list and kebab-case naming
- action states such as idle, walk, run, attack, cast, hit, death, interact, emote, mount, swim, or fly
- frames per action, frame duration, loop mode, cancel/event markers, and hit/contact frames
- equipment, shadow, VFX, and attachment layers
- collision/hitbox assumptions and runtime animation names

## Output
- selected sheet type and active style templates
- tile or frame dimensions
- row/column layout and naming convention
- direction/facing list when applicable
- required variants and action states
- atlas and metadata fields
- validation checks for seams, anchors, sorting, readability, animation timing, and licensing

## Commands
- `./commands/print-tileset-sheet-template.sh [tileset-name] [orientation]`
- `./commands/print-directional-animation-sheet-template.sh [character-name] [direction-count] [frames-per-action] [cell-size]`
- `./commands/inspect-animation-sheet-folder.sh [folder] [cell-size]`
- `./commands/print-game-art-handoff-template.sh [asset-type] [engine]`
- `./commands/print-isometric-production-checklist.sh [asset-type]`
