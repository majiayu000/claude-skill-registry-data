---
name: card-grass
description: Use when a large terrain needs ground cover (meadow, hill grass, snow tufts) that reads well from a road or a walking camera at a low triangle and fill cost. ATS/ETS2-style card grass on WebGPU with TSL - one fixed-yaw textured quad per clump from a 4x4 cutout atlas, instanced per terrain tile, on a jittered grid gated by a density field; ships `card-grass.tsl.js` and `make-atlas.md`.
---

# Card Grass

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

The companion file `scripts/card-grass.tsl.js` is the material, the placement and the tile meshes. Copy it into the project; it imports only from `three/webgpu` and `three/tsl`. `references/make-atlas.md` builds the atlas it samples.

## What it is

Ground cover the way the truck simulators do it: each clump is ONE textured quad standing upright at a fixed random yaw (it never turns to the camera), cut from a 4 x 4 atlas of cutout plant photos. Cards sit on a jittered grid (density from the spacing, not a count), thinned by a two-octave noise field so patches are dense and the ground between is thin. The CPU picks each card's atlas cell (by climate, altitude, wetness: the caller's rule) and its height. The shader lights every card as flat ground, alpha-tests it, sways its top, tints it toward the ground colour, turns it into snow-covered tufts in winter, and sinks it underground past a fade band. Cards never cast shadows and receive one shadow sample at the root.

## When to use it

- open terrain seen from 1-3 m up, at speed or walking: roadsides, fields, hills, moorland, snowfields
- terrain streamed in tiles (64-512 m) with a draw distance for vegetation of 150-400 m
- fill-bound scenes where blade geometry or crossed billboards cost too much

Not for: lawns seen from above (cards read as flat sticks top-down), close-up hero grass you walk through (use blade geometry with bending), or anything past ~400 m (let the terrain texture carry it).

## Companion file API

`createCardGrassMaterial(options)` returns a `MeshLambertNodeMaterial` (DoubleSide). Options, from `CARD_GRASS_DEFAULTS`:

- `atlas` (required): the atlas texture; sRGB, ClampToEdge, mipmapped
- `grid` (4): cells per atlas row; `inset` (0.005): cell fraction kept clear at each edge
- `fade` ([214, 306]): m from the view camera where cards start to sink / are fully under; or a `Vector2` uniform you share
- `sink` (2.4): m a faded card drops
- `viewXZ` (null): a `Vector2` uniform holding the VIEW camera's xz; created if null. Write it each frame with `updateGrassView(material, camera)`
- `gain` (1.0): brightness; leave at 1 with a normalised atlas
- `rootShade` (0.72): colour at the root, rising to 1 at 45 % of the card height (a cheap fake AO)
- `clumpJitter` (0.26): per-instance brightness spread
- `patch` ({ scale 0.11, amount 0.24 }): ~9 m brightness patches; `macro` ({ scale 0.011, amount 0.16 }): ~90 m tone drift
- `tintAt` (null): `(positionWorld) => vec3`, the ground colour under the card; `tintAmount` (0.65): share of the card's chroma replaced by it
- `winter` (0): global snow amount, uniform; `winterAt` (null): `(positionWorld) => float`, combined by max
- `palette` ({ lo 0xccd5db, tip 0xf1f6f9 }): winter root and tip colours
- `wind` ({ amount 0.035, speed 1.15, ripple 0.28, rippleSpeed 2.33, side 0.35 }): metres of sway at the top
- `maskAt` (null): `(positionWorld) => float` multiplied into alpha, for holes (inside a vehicle, under a building)
- `alphaTest` (0.5); `rootLift` (0.06): m above the root where the shadow is sampled

Live uniforms: `material.userData.grass` = `{ uFade, uView, uGain, uWinter, uSink }`.

`createCardGeometry()`: a unit `PlaneGeometry`, base at y = 0. One per session; tiles clone it.

`placeGrass({ originX, originZ, size, spacing = 1.03, seed = 0, heightAt, accept, density, clump, scale })` returns a `Float64Array` of `[x, y, z, scale, ...]` in world space:
- `heightAt(x, z)` (required): terrain height
- `accept(x, y, z)`: false rejects the cell (slope, water, road surface, buildings, bare rock)
- `density`: an object over `DENSITY_DEFAULTS` ({ base 0.6, a 0.55, scaleA 38, b 0.35, scaleB 9, min 0.2, max 1 }: keep share = base + a * noise(38 m) + b * noise(9 m), clamped), or `(x, z) => 0..1`, or `false` for every cell
- `clump`: null, or an object over `CLUMP_DEFAULTS` ({ where null, scale 8, lo 0.5, hi 0.65, keep 1, extra 3 }); where `where(x, y, z)` is true, cells survive only inside 8 m noise blobs and each survivor gets `extra` more cards jittered in its cell. For snowfields: bare snow between dense tufts
- `scale` ([0.22, 0.6]): placement scale range, or `(x, y, z, r) => scale` (e.g. 0.65-1.1 near trees)

`hash2(x, z, seed)` (integer hash to [0, 1], `Math.imul`, exact at any integer) and `noise2(x, z, scale, seed)` (value noise in [-1, 1]) are exported for the caller's own rules.

`createGrassTile(geometry, material, capacity = 32000)`: an empty `InstancedMesh` (count 1, zero matrix), `castShadow` false, `receiveShadow` true, with its own cloned geometry carrying the `aCard` instance attribute (atlas cell, card height m).

`writeGrassTile(mesh, placements, origin, pickCard, options)`: moves the mesh to `origin` ({ x, z }), writes tile-local matrices and `aCard`, sets `count`, the upload ranges and the bounding sphere. `pickCard(x, y, z, scale, h)` returns the atlas cell; `h` is a 0..1 hash of the position. Options from `TILE_DEFAULTS`: `height` ({ base 0.35, perScale 1.5, min 0.45, max 1.4 }: card height m = base + perScale x scale, so 0.68-1.25 m for the default scale range), `width` ([0.85, 1.15] x height), `lean` (0.24 rad full range, +-7 deg), `rootDepth` (0.05 m under the ground), `boundsPad` (2.5 m), `seed` (7000).

`parkGrassTile(mesh)` and `createGrassPool(geometry, material, capacity)` (`prewarm(n)`, `acquire(placements, origin, pickCard, options)`, `release(mesh)`, `parked`): the pooling pattern below.

## How it works

- **Fixed yaw, not camera-facing.** A camera-facing billboard swims as the camera turns and every card shows its full face; fixed cards give parallax and depth like real clumps. Yaw = `hash2` of the rounded world position. A linear yaw (`0.73 x + z`) is constant along diagonals 6.3 m apart; cards facing the camera edge-on vanish together along those lines and the field shows a grid from some angles.
- **Jittered grid.** One cell per `spacing` m, the card jittered over the WHOLE cell. A 0.1-0.9 jitter left the lattice visible. Cells are indexed globally (`floor(world / spacing)`), so tiles of any size join without seams and a tile always gets the same cards.
- **Density field.** Two octaves (38 m and 9 m) of keep share between 20 and 100 %, ~60 % mean: dense patches, thin ground between. Without it the even cover reads as a carpet.
- **Atlas cell on the CPU.** `pickCard` runs once per card when the tile is written; the GPU only reads `aCard.x`. Typical rule: dry share from altitude or climate (`h < dry` picks the dry set), then 2.5 % flowers, 2 % plumes, the rest green.
- **Flat up normal.** `normalNode` = the up vector in view space: a card is lit exactly like the ground it stands on (SCS's grass shader does the same). Real card normals make half the field black against the sun and flicker as the yaw changes.
- **Shadow received once at the root.** `receivedShadowPositionNode` = the root position as a FLAT varying. A card is in shade or in sun as a whole; per-fragment lookups put stripes of the cascade's texels across a 1 m card.
- **No cast shadow.** `castShadow = false` keeps every grass tile out of the shadow depth pass, which is where alpha-tested cards cost most (no early-Z).
- **Wind.** Gust (1.15 rad/s) plus a 0.28 ripple (2.33 rad/s), phased per instance, scaled by `uv.y^2` so the root stays planted: 3.5 cm at the tip, x and 0.35 x on z.
- **Distance sink.** Past `fade.x` cards slide down to `sink` m under the ground by `fade.y`, measured from `viewXZ`. Sinking instead of alpha-fading keeps the alpha test binary (no sorting, no dithering pattern) and the ring of growing cards is hidden by perspective.
- **Ground tint.** `tintAt` gives the ground colour; its unit-luminance hue times the card's own luminance replaces 65 % of the card's colour. The card keeps its shading and detail and stops looking green-on-brown. Use the same band colours the terrain shader uses (by altitude, slope ignored: cards never stand on rock) plus the terrain's dry-patch field.
- **Winter.** No winter cards exist in any pack worth using. Snow = `palette` from root to tip times `min(1, 0.15 + 2.6 x card luminance)`: pale tufts that keep the card's structure.

## Integration

```js
import * as THREE from 'three/webgpu';
import { createCardGrassMaterial, createCardGeometry, createGrassPool, placeGrass, updateGrassView } from './card-grass.tsl.js';

const atlas = new THREE.Texture(Object.assign(document.createElement('canvas'), { width: 1, height: 1 }));
atlas.colorSpace = THREE.SRGBColorSpace; atlas.anisotropy = 8; atlas.needsUpdate = true;
new THREE.ImageLoader().loadAsync('textures/grass-cards.webp').then((img) => { atlas.image = img; atlas.needsUpdate = true; });

const SETS = { green: [0, 1, 2, 3, 4, 5, 6, 7], dry: [8, 9, 10, 11, 12, 13], flower: 14, plume: 15 };
const pickCard = (x, y, z, s, h) => {
  const dry = THREE.MathUtils.smoothstep(y, 40, 120);            // the caller's climate rule
  if (h < dry) return SETS.dry[(h / Math.max(dry, 1e-6) * SETS.dry.length) | 0];
  const g = (h - dry) / (1 - dry);
  if (g < 0.025) return SETS.flower;
  if (g < 0.045) return SETS.plume;
  return SETS.green[((g - 0.045) / 0.955 * SETS.green.length) | 0];
};

const material = createCardGrassMaterial({ atlas, tintAt: (p) => terrainBandColour(p) }); // a TSL fn of yours
const pool = createGrassPool(createCardGeometry(), material, 32000);
pool.prewarm(25);                                                 // peak tile count, at load

function fillTile(tile) {                                         // from the streamer, in a worker if you can
  const values = placeGrass({ originX: tile.x, originZ: tile.z, size: 256, seed: 1, heightAt,
    accept: (x, y, z) => slopeAt(x, z) < 0.8 && !onRoad(x, z, 2) && !inWater(x, z) });
  tile.grass = pool.acquire(values, { x: tile.x, z: tile.z }, pickCard);
  tile.group.add(tile.grass);
}
function emptyTile(tile) { pool.release(tile.grass); tile.grass = null; }

renderer.setAnimationLoop(() => { updateGrassView(material, camera); renderer.render(scene, camera); });
```

Steps:
1. Build the atlas (`references/make-atlas.md`); write down which cells form which set.
2. One material and one geometry for the session; share `fade` with any other fading vegetation.
3. Placement runs per tile, ideally in the worker that builds the tile's heights (pure JS, no three). Return the `Float64Array` as a transferable.
4. Fill tiles within the fade radius only, with hysteresis: fill when the camera is within `fade.y + ~35 m` of the tile's square (distance to the square, not its centre), release past `fade.y + ~95 m`, and cap by tile ring (Chebyshev 2 for 256 m tiles at a 306 m fade = at most 25 tiles). Re-check every ~20 frames, not every frame.
5. Call `updateGrassView` every frame with the eye camera before rendering.

## Pooling

- **One `InstancedMesh` per tile**, not one ring for the world: each tile gets its own frustum culling in the main pass, and a write touches only its own buffers.
- **Per-mesh geometry.** `aCard` is an `InstancedBufferAttribute`; it cannot live on a geometry shared by meshes with different contents, so each tile clones the quad (4 vertices: nothing).
- **Parked, never disposed.** Destroying an instance buffer that a queued command buffer still uses is a WebGPU error ("used in submit while destroyed"). Release = detach, count 1, zero matrix, upload one matrix (`parkGrassTile`).
- **Prewarm the peak count at load.** A new `InstancedMesh` mid-session costs a render-object setup (bind groups) in every render context the grass appears in, though since r187 the node build itself is shared by attachment state and one `InstancedMesh` per material compiles for all; reused meshes cost a buffer upload only.
- **Upload ranges.** Only the written prefix: `addUpdateRange(0, count * 16)` on the matrices, `count * 2` on `aCard`. A full 32k-slot upload is 2 MB per tile.
- **Bounds by hand.** `computeBoundingSphere()` includes the unused slots at the tile origin; the min/max of the written cards plus 2.5 m (card size + sway) is exact.
- **Cap per tile.** At spacing 1.03 m the grid holds 0.94 cells/m^2 and the default density keeps ~0.64/m^2 before `accept`: 41.7k on a bare 256 m tile, ~27k measured max with real rejection rules (roads, water, slope, rock). Cap 32000 x 64 B = 2 MB of matrices per tile, 51 MB over 25 tiles. Overflow warns and drops the tail.

## Do not

- **No roadside-only grass** (discs at pole feet, strips along guardrails): tried and removed. Every pole gets the same disc and every rail a straight line; it reads as artificial. Let the grid run to a ~2 m road margin instead.
- **No camera-facing cards**, no crossed quads (twice the fill for no gain at road speed).
- **No `cameraPosition` in the fade.** In a shadow pass it is the light camera: cards sink relative to the sun and the fade ring is wrong in every pass but the eye.
- **No per-card normals** and **no cast shadow** (above).
- **No fixed jitter range smaller than the cell**, no linear yaw formula (both show the grid).
- **No shader brightness fix for a dark card.** Normalise in the atlas; a global gain brightens the good cards too.

## Pitfalls

- The tile mesh must be translated only: the sink and sway are added in tile-local space, and `writeGrassTile` puts instance translations relative to `origin`. Keep the origin per tile: world-space float32 positions jitter visibly past ~10 km.
- The TSL noise in the material uses a sin hash; it loses precision a few km from the origin. With a floating origin this does not matter; otherwise feed it a tile-relative position or swap in an integer hash.
- Atlas row 0 is the TOP of the image; the material flips v. A card whose base is not on the cell's bottom edge floats.
- Alpha test turns tiny mips into noise: keep `anisotropy` 8 and the 0.5 % inset; do not lower `alphaTest` below 0.4 (cards fatten into blobs at distance).
- Snow chunks and dense fields multiply: four cards per kept clump cell in snow is right only because the gate keeps ~15 % of the cells.
- `aCard.y` (card height) feeds the root shadow position; if you scale instances some other way, write the real height there.
- Rain splash or particle sprites spawned on the ground around the camera read as snowflakes on top of grass; spawn them on hard surfaces only, or tint them by the ground.

## Performance

Measured on one terrain (256 m tiles, 3 x 3 tiles around the camera) when blade clumps were replaced by cards:
- triangles in grass 2.1 M -> 0.32 M
- grass GPU row 2.1-3.2 ms -> 1.5 ms; draw count unchanged (one per tile)
- placement in the worker: tile generation 40 -> 50-65 ms (off the main thread)
- 10-16k cards on a green 256 m tile, ~7k on a snowfield tile with the clump gate

Cost is fill, not vertices: every card is alpha-tested with no early-Z, so the knobs are `spacing` (count goes as 1/spacing^2: 1.1 -> 1.03 m is +15 %), the density field and the fade distance (doubling the fade from 153 to 306 m took the tiles in range from 9 to up to 25). Keep the grass out of reflection passes (a layer the mirror cameras do not enable) and out of the shadow depth pass (`castShadow` false).
