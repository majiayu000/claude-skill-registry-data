---
name: unity-build-2d-content
description: Author Unity sprites, atlases and Tilemaps while preserving sprite identities, explicit tile rules and content-loading ownership.
engines: [UNITY]
---

# Unity Build 2D Content

## When to use

Import or revise sprite sheets, pack atlases, author Tilemaps or RuleTiles, and configure pixel-perfect 2D presentation. Runtime HUD composition belongs to the UI owner; this skill owns its sprite content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-2d-content` before edits or tool launches. Require an effective `UNITY` engine and an eligible skill, honoring task override evidence and output scope. Selecting this skill never selects an engine.

Inspect the actual Editor version, package manifest/lock, sprite importer, Tilemap/Extras and Pixel Perfect availability, atlas mode, build target and selected content-delivery system. Packages and external art are explicit project dependencies; do not install or fetch them implicitly.

## Workflow

1. Record source rights, dimensions, pixels per unit, pivot/border policy, texture/compression budgets and animation/UI consumers. Inspect existing `.meta` and subasset references before changing imports.
2. Match retained sprite rectangles by stable authored identity. Preserve their `spriteID`, name-to-file-ID mapping and asset GUID; allocate new IDs only for genuinely new sprites. Verify prefab, animation and UI references after reimport. Read [sprite identity](references/sprite-identity.md) before automation.
3. Make atlas membership, variant settings, padding, filtering and platform overrides intentional. Separate Editor pack preview from built content. For deferred delivery, own every request callback, in-flight handle and retained atlas until consumers release it; read [atlas lifetime](references/atlas-lifetime.md).
4. Author tile topology from the intended world rules. A silhouette, filename, sprite-sheet order or neighbor-count heuristic is insufficient to infer RuleTile adjacency. Define match priority, transforms, empty cells and collider behavior, then test representative neighborhoods. Use [Tilemap and pixel presentation](references/tilemap-presentation.md).
5. Produce atlas/Addressables or bundle content for the selected platform before its dependent player build. Preserve an input/content hash relationship and check duplicate inclusion, missing catalogs and actual download/memory cost.

## Verification

Check retained GUID/local-file-ID references through import, save and reload. Exercise tile edges, corners, holes and rotated matches against declared expected tiles. Test multiple outstanding atlas requests, a failed load, scene teardown during loading and re-entry; validate sprites in an actual player, including a content update. Review pixel scrolling, camera movement and UI scaling on target displays.

## Output

Native-authored sprite/atlas/Tilemap assets, import and adjacency decisions, content-build ancestry, ownership rules and measured evidence. Record actual environment, expected/observed outcomes, and blocked/not-run checks. Editor packing or source inspection cannot certify player late binding, correct artistic topology or pixel stability.
