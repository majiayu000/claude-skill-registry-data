---
name: hole-content
description: Add content to Hole Island - a new edible item (catalog row + procedural builder + tests + lineup check) or a whole new map (bounds, zones, point budget, registry entry, per-map scores version). Use for any request about Hole Island items, plush, toys, buildings, maps, the toy store (Toy Emporium) or the City Island generator.
---

# Hole Island content workflow

Read first: `src/games/hole/DETAILS.md` (rules, level / tier tables, catalog, art style) and, for the toy store,
`src/games/hole/TOY-STORE.md`, for Animal Island `src/games/hole/ANIMAL-ISLAND.md`, for Construction Site `src/games/hole/CONSTRUCTION-SITE.md`. Points, tier and unlock level are **derived from the item size**
(`size = max(w, d, h x 0.25)`, see `sim/progression.ts`): never hand-pick them. Changing an item size changes its points,
so bump that map's scoring version (below).

## Add an item

1. **Catalog row.**
   - City Island: `items/catalog.ts` (`def(...)`, keep the list ordered by size).
   - Toy Emporium: `items/catalog-toy.ts` (generated from the roster in `TOY-STORE.md` 4.1; keep the department in
     `where` as `"<Department> - <note>"`, the generator homes items by that department; give it a priority).
   - `paints` = per-instance colours, only if the builder has `paint: true` parts (the test checks both ways).
2. **Builder.** City: `build-small.ts` / `build-vehicles.ts` / `build-buildings.ts`. Toy: `build-toys.ts` (bricks,
   figures, toys, games, dolls, store), `build-toyveh.ts` (vehicles, rides, robots, rockets, outdoor, trucks),
   `build-plush.ts` (plush rig: add a family to `PLUSH` and an id `plush_<family>_<size>`), `build-landmarks.ts`.
   - Toy recipes use `F(m, w, d, h)` from `kit-toy.ts` and **fractions** of the catalog size, so the built size equals the
     catalog size. Vehicles run along X, plush / shelves / people face +Z, pivot at the ground centre.
   - Toy builders run with `Mesher.decoplanar` (faces that share a plane are pulled apart by 5.8 mm). Cylinders and
     tapered boxes are **not** handled: keep their tops / sides off other parts' planes by hand.
   - Proud details (eyes, doors, decals) stick out 1-3 cm (use at least `0.012 / d` as a fraction on small items).
   - Register in the builder map of that file (`TOY_BUILDERS`, `TOYVEH_BUILDERS`, `LANDMARK_BUILDERS`, ...); `builders.ts`
     merges them. Plush ids are resolved from the family name automatically.
3. **Tests.** `npx rstest run tests/hole` - City: `items`, `clip`; Toy: `toy-items` (size within 15 % footprint / 10 %
   height, on the ground, paint list, triangle budget per group), `toy-clip` (z-fighting, mostly-buried parts; the
   failure names the builder `file:line`), `toy-map`. Every size tier 1-25 and hole level 1-15 needs >= 2 types per
   catalog: **protect the thin tiers** (toy: 17, 20, 21, 23).
4. **Look at it.** `item-viewer.html?map=toy&mode=lineup&family=plush_panda&gamecam=1` (and `mode=compare` for the tier
   boundary). It has to read at game-camera distance at the item's first hole level, not just in the viewer.
5. **Place it.** City: add its `SPAWN` row in `map/spawn.ts` (zones its centre may be in; only vehicles may list `road`, see
   DETAILS.md "Map generation rules") and a placement in `map/generate.ts` through `tryPut` / `spotFor`. Toy: it is picked up automatically by the zone of its department
   (`homeOf` in `map/toy/generate.ts`); anything with size > 14.5 m homes in the atrium. Check `map-viewer.html?map=toy`.
6. **Docs + scores.** Update the DETAILS.md / `TOY-STORE.md` roster row (one row, no prose). Bump the scoring version of the map (below).

## Add an animal / scenery item (Animal Island)

1. Row in `items/catalog-animal.ts` (`def(id, name, group, w, d, h, note, priority, biomes, motion, { paints, variants })`):
   biomes = where it may be placed, motion = `wander | herd | hop | crawl | skitter | flutter | swim | trail | patrol | roam | -`.
   Check tier / level coverage with `npx rstest run tests/hole/animal-items`.
2. Builder: a family row in `build-animals.ts` (`QUADS`, `HOPS`, `BIRDS`, `SIMPLE`; `<family>_big` / `<family>_giant` reuse the
   rig with a glowing collar), or a recipe in `build-nature.ts` / `build-zoo.ts`. Recipes run in `Mesher.fitted`, so design by
   proportion; use `ball()` for round parts. Parts closer than 4 mm to a neighbour's face fail the clip test.
3. The generator places it by itself from its biomes and priority (`planCounts`); giants and compound items are listed in
   `GIANTS` and `buildCompound` of `map/animal/generate.ts`. Bump `MAP_SCORING_VERSIONS.animal` once the map is released.
4. Look: `item-viewer.html?map=animal&mode=lineup&family=<id part>`; pace: `tests/hole/animal-map.test.ts` bands.

## Add a map

1. A generator `map/<id>/generate.ts` returning `MapData` (`map/types.ts`): `placements`, `rects` (flat floor patches),
   `start`, and either `coast` (island) or `bounds` (`hx`, `hz`, `inset`, `door`) for a closed rectangle. Deterministic
   (`src/shared/rng.ts`), DOM-free.
2. **Exact point total** per map (City Island 30 000, Toy Emporium 22 000): fill, then trim small items / top up with 1-point fillers
   (`balancePoints` in `map/generate.ts` and `map/toy/generate.ts`). Every tier 1-25 and level 1-15 has >= 2 types placed,
   every type up to tier 20 is placed, the start has > 15 tier 1-3 items within 25 m, total >= 2 x `cumulativeXp(15)`.
3. **Pace it with the bot** (`sim/bot.ts`, `balance.html?map=<id>`): good bot, Hard 120 s reaches level >= 10, Medium
   240 s level 15, Easy 480 s clears > 95 %. Density (points per m2) decides the pace: the toy store needed a 600 x 400 m
   floor. Tune floor size and clustering, **not** the XP curve.
4. **Ground + mood.** A ground builder in `render/` (use the stencil-cut `createGroundMaterial()` for everything the hole
   cuts) and wire it in `render/map-ground.ts`; walls use `getItemMaterials().prop` so the building fade dithers them.
5. **Register** a `MapDef` in `map/registry.ts` (name, blurb, noun for the HUD, points, mood colours, menu camera) and
   add the id to `MAP_SCORING_VERSIONS` in `game/scores.ts` (start at 1). A new map goes into `MAPS_LIST` with `hideInProd: true` in
   `src/games/hole/release.ts` first (dev server and `build:test` only); remove the flag when Deni says ship.
   Add a menu card picture `screenshots/menu-<id>.jpg` (640 x 360) in `game/menu.ts`.
6. Tests like `tests/hole/toy-map.test.ts` (determinism, exact points, coverage, items inside bounds, reachability from
   the clamped hole centre, balance bands). Viewers: `map-viewer.html?map=<id>`, `balance.html?map=<id>`.

## Testing in the browser

Open the game with `mute=1` (`/games/hole/?map=toy&mute=1`): no sound while creating / editing (AGENTS.md "Sound while testing"). Drop it only when the task is a sound fix in `game/audio.ts`.

## Scoring version rule

`MAP_SCORING_VERSIONS` in `game/scores.ts` is per map. Bump the version of every map whose item dimensions / points,
point total, clear bonus, difficulty times or map content changed (shared rules in `sim/` bump all). The history lives in
the comment above it.
