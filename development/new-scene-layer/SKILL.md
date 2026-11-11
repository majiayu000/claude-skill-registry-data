---
name: new-scene-layer
description: "Use when adding a new layer or per-tile dressing to the 3D scene (a new kind of object drawn from tile data: furniture, a vegetation kind, a structure, a data mark), or when moving one between the runtime and the baked terrain glTF."
---

# Adding a scene layer

Decisions behind this: ADR 0024 (tiles and their dressing), ADR 0027
(node materials), ADR 0030 (parts on the ground), ADR 0047 (memory).
Deep reference: the `city-walker` skill, "Node materials" and "Tiles".

## Decide where it is built

- **Depends only on baked data** (no look control, no time of day, no
  device)? Bake it into the fine terrain glTF as a named node in
  `scripts/bake-tiles.ts`; the layer file only gives it a material.
- **Otherwise** build it at runtime in the dressing plugin
  (`tile-stream.ts`), as a builder of steps run in slices
  (`lib/city/build-steps.ts`) if it can take more than a few ms on a phone.

## Checklist

1. **Data:** a baked per-tile file (`new-bake-step` skill), declared in
   `lib/city/tile.ts`; a missing optional file means "layer off".
2. **Frame:** positions in the Y-up frame, never inside the rotated `world`
   group; heights from the site's ground (`lib/city/ground.ts`).
3. **Material:** a node material; a `sceneMaterial` when it has no per-tile
   data. Fixed strengths are named constant nodes; anything that moves a
   shared uniform. Mind the eight vertex buffers and sixteen varyings.
4. **Instancing:** `Instances`, never `InstancedMesh`; chunk into cells so
   off-screen chunks cull; after writing matrices set `needsUpdate` and
   `computeBoundingSphere()`.
5. **Lifecycle:** build in `processTileModel`, compile before it shows
   (`PostStack.compile`), free in `disposeTile`. Add its bytes to
   `calculateBytesUsed`; add CPU arrays nothing reads later to the
   CPU-drop lists. A part built after its tile (on demand, or from a file
   of its own) is a `LatePart` adapter (`late-parts.ts`, beside
   `dressingPart` and `muralsPart`): the module builds, weighs, compiles,
   hangs and frees it; choose `hangAt` — `"wait"` only for what a level's
   hand-over waits on (the dressing), `"compile"` for everything else.
6. **Shadows:** casts only if static; call `invalidateShadows()` when it
   lands; sway casts through a rigid `castShadowPositionNode`.
7. **Ground:** feet and edges from `ground-join.ts`, joins tested
   (`JOIN_PARTS` or `checkJoins`); its doc comment says what happens where
   the ground beside it is higher and where it is lower.
8. **Night:** emissive or additive terms scale by `sceneNight`
   (`scene-environment.ts`); a part drawn only after dark wears
   `drawnAtNight` on its scene-wide material; a part whose instances
   follow the date `follow`s the environment at birth
   (`followEnvironment`) and lets go in `disposeDressing`.
9. **Styles:** tag what a picture style may dress (`userData.styleCrown`,
   `userData.styleLampHeads`); never read the style.
10. **Asking:** if a visitor may click it, a ray target from its data
    (`lib/city/ask-items.ts`), card lines and a heading in
    `lib/city/inquiry-features.ts`, a row in the kind table
    (`lib/city/inquiry.ts`), an arm in `lineage.ts` and a fixture in
    `inquiry-kinds.test.ts` (ADR 0042).
11. **Phone:** measure its bytes on the phone tier; the total must not grow
    (offset it elsewhere).
12. **Tests:** a unit test of the node setup and geometry; a scene-census
    line and an e2e assertion for presence.
13. **Visual check:** a real-GPU plate (`bun run shots`) from an oblique
    angle; snapshots in the PR (`pr-snapshots`).
14. **Docs:** `docs-upkeep` (ledger, the codebook in `docs/rendering.md`,
    the guide's layer table in both languages).
