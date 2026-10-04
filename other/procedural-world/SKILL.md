---
name: procedural-world
description: The seeded procedural endless city — deterministic generation, road network and block layout, chunk streaming and unloading, LOD, collision geometry, and designing generated space that produces good chases. Use when working on world generation, streaming, or when the city feels repetitive, disorienting, or bad to drive in.
---

# Procedural endless city

The world is generated from a seed and is effectively unbounded. Two things have to
be true at once: it must stream within a mobile memory budget, and it must be
_good to drive in_. The second is harder and is usually neglected.

## Determinism

World generation is pure and seeded, entirely in our own code — no dependence on
Havok, floats from physics, or wall-clock time.

- One root seed for a world. Each chunk derives its own seed from
  `hash(rootSeed, chunkX, chunkZ)` — **never** from a running generator, or chunks
  will differ depending on the order you drove through them.
- Generation must be a pure function: `generate(chunkX, chunkZ, rootSeed) -> ChunkData`.
  Same inputs, same output, forever, regardless of what else is loaded.
- This is a hard test: generate a chunk, drive away, come back, regenerate, assert
  identical. And generate the same chunk from two different visit orders.
- Seeded PRNG is explicit and passed in. Never `Math.random()` anywhere in generation.

Determinism here buys a lot: shareable seeds, tiny save files (seed + player state),
reproducible bug reports, and — later — a server and client that generate the same
city without shipping the city over the wire.

## Structure: roads first

Generate in this order. Each layer constrains the next.

1. **Road network** — the skeleton. Everything else is derived from it.
2. **Blocks** — the polygons enclosed by roads.
3. **Lots** — subdivisions of blocks.
4. **Buildings** — placed per lot, height and style by district.
5. **Props** — lights, signs, parked cars, barriers.

Do not generate buildings and then fit roads around them.

**Road network approach:** a grid with controlled irregularity is the right default —
deformed spacing, occasional missing links, arterial roads every N blocks, and a small
number of diagonals. Pure Voronoi or L-system cities look organic but produce
frustrating driving (dead ends, unpredictable junction angles). A grid is legible at
speed, which is what a chase needs.

## Make seams impossible rather than correct

Tiling chunks together is usually described as the hard part, and it is — but
only if a chunk generates its own contents and then has to agree with neighbours
it has never seen. Arrange it so that question never arises: make every feature a
pure function of a **global** index, not a chunk-local one.

- Road line `i` sits at `positionOf(rootSeed, axis, i)`.
- The segment between junctions `(i, j)` and `(i+1, j)` exists by a hash of
  `(i, j)`.

Neither takes a chunk argument, so two chunks meeting at a seam are evaluating
the same function on the same indices and cannot disagree. A chunk becomes a
_query_ — "which global features fall in this square" — which also means chunk
size becomes a free parameter that changes nothing about the world.

Then give each feature exactly one owner (the chunk containing its lower-index
endpoint) so nothing is emitted twice or missed. Segments will overhang chunk
bounds; that is correct. Splitting them at the boundary puts a joint down the
middle of a road.

**Repairs must only add, never remove.** Guaranteeing every junction at least two
exits by _deleting_ somewhere else makes the result depend on the order junctions
were visited — the exact bug determinism exists to prevent. Adding cannot reduce
another junction's degree, so each junction can be repaired in isolation, and two
chunks reach the same answer without communicating.

**Test the chunk output against the global functions**, not against itself. "Each
segment appears exactly once" passes even when ownership is shifted by an index,
or when a chunk computes positions chunk-relatively: the set is still
one-per-slot, just wrong.

## A local index is chunk-local even when the position it derives from is not

The rule above is easy to keep for positions and easy to lose for everything
else. Street lamps on #26 were keyed on `(segmentCentreX, segmentCentreZ, side)`
— two world coordinates and a `+1/-1` telling which kerb. That reads as global,
and two of the three parts are. `side` is not: it is signed relative to the
segment's own `a → b` direction, so describing the same road from the other end
flips it, and the same physical lamp gets a different roll for whether it is
dead.

Nothing reverses a road's winding today, so this was latent rather than live. It
would have surfaced as a strip of lamps changing which ones are burnt out at
exactly one chunk boundary — no crash, no assertion, and about as hard to trace
as anything in this codebase. The fix is to key on the thing that exists in the
world: the lamp post's own position, which is the same point whichever way the
segment is described.

The general form: **if a key mentions a direction, a side, a winding, an
ordering, or a loop counter, it is not global, however global the rest of the
key looks.** Ask what the key returns when the same feature is described from
the other end.

Worth a test of its own, because it is invisible otherwise:

```ts
const forward = lightsOnSegment(SEED, segment());
const backward = lightsOnSegment(SEED, segment({ ax: bx, az: bz, bx: ax, bz: az }));
expect(new Set(backward.map(key))).toEqual(new Set(forward.map(key)));
```

## Designing for chases

This is the main risk of procedural generation, and it needs deliberate work:

- **Legibility at speed.** The player must read a junction and commit to a turn in
  under a second. Consistent lane widths, generous corner radii, and clear sightlines
  matter more than visual variety.
- **Landmarks defeat samey-ness.** Inject rare, distinctive structures on a
  seeded schedule (a tower, a stadium, a bridge, a park) so the player can navigate
  by memory. Uniform blocks are the failure mode of every procedural city.
- **Districts, not noise.** Partition space into a handful of district types
  (downtown, industrial, suburbs, waterfront) with genuinely different block sizes,
  road density, and building heights. Variety should come from a few strongly
  distinct modes, not from randomising every parameter slightly.
- **Chase geography needs alternatives.** Long straights favour the faster car,
  tight grids favour the more agile one, and dead ends end chases abruptly. Constrain
  generation to guarantee route choice: assert at generation time that every junction
  has at least two exits, and cap dead-end frequency.
- **Authored set pieces are allowed.** Hand-built chunks (a bridge crossing, a
  multi-storey car park) placed procedurally give the best of both. Purity is not a
  goal; a good chase is.

## Districts must be keyed on a coarse region, not on the block

The difference between "districts" and "noise" is entirely the key you hash. Draw
a district type per block and every block differs from its neighbours: the map is
noise however strongly distinct the four types are, and the player can never
learn the city. Key it on `floor(i / N), floor(j / N)` instead and the same draw
produces contiguous regions you can navigate by.

Assert it rather than assuming: measure the fraction of adjacent blocks sharing a
district and require most of them to match. That test fails immediately if the
key is ever changed back.

Two things worth building in from the start:

- **An empty district.** Parks cost nothing to generate and buy sightlines,
  alternative lines through a chase, and relief from the grid. Open space is
  content.
- **Distinctness asserted on the parameters themselves.** Ranges that overlap
  heavily are the randomise-everything-slightly failure wearing a costume. A test
  that downtown's _minimum_ height clears industrial's _maximum_ keeps the modes
  actually distinct as they get tuned.

## Schedule landmarks; do not scatter and reject

Rarity plus minimum spacing is usually written as "place randomly, retry if too
close". Don't. Divide space into regions and give each region at most one
landmark at a seeded offset, with the offset range chosen so a footprint can
never cross into the neighbouring region. Spacing then falls out of the
arithmetic: two landmarks cannot overlap or crowd, no retry loop exists to get
subtly wrong, and "which landmark covers this block?" is answered by looking at
one region rather than searching neighbours.

Two consequences worth planning for:

- **Schedule the footprint before the kind.** The block generator needs to know
  which blocks a landmark occupies so it can leave them clear, and it must know
  that without consulting anything that depends on blocks — or the two modules
  import each other. Decide position and size from the seed alone; pick the kind
  later, from the district, in the caller that already holds the block.
- **Build only from the anchor block.** A 2×2 landmark is covered by four
  blocks. Building from each stacks four copies in the same place: invisible in
  a screenshot, and four times the instances.

## A landmark is a silhouette plus a light, and needs both

At night a dark tower against a dark sky is invisible however tall it is. The
first version here read as a single bright dot floating over the skyline,
because only its crown was lit — much weaker to steer by than a vertical line of
light. Lit bands at each setback fixed it, and are what a real tower looks like
anyway.

So test the property that matters, not the one that is easy: not "the landmark
has a light" but "the light is near the top of it". A glow at ground level sits
behind the surrounding blocks and does nothing, and passes the easy assertion.

Landmarks also need excusing from fog. Fog is what gives the city depth, and it
is also what would erase the one thing the player is meant to navigate by;
`material.fogEnabled = false` on the lit parts costs nothing and is the
difference between a tower being useful from three blocks away or from one.

Keeping landmarks to the same box primitives as ordinary buildings means they
ride the existing thin-instance path: a landmark costs a handful of instances
and **no extra draw call**. What separates it is silhouette and light, which is
all that reads at night anyway.

## Streaming

- Chunk size is a tunable, sized so that a chunk generates in well under one frame
  budget — or generation is chunked across frames / moved to a Worker. A visible hitch
  when crossing a chunk boundary is unacceptable and will be the most common bug here.
- Maintain a radius of loaded chunks around the player, in ring order, generating
  ahead along the direction of travel — at 150km/h the player crosses chunks fast, so
  prefetch must be velocity-aware, not just distance-based.
- Unload symmetrically and completely: meshes, materials not shared, textures, **and
  Havok bodies**. Orphaned physics bodies from unloaded chunks are the classic leak
  in this design.
- Hysteresis on load/unload radius — otherwise a player sitting on a boundary
  thrashes chunks continuously.
- Never block the render loop on generation. Generation is async and interruptible.

## The leak test has to bound residency, not just teardown

"Load and unload 1000 chunks, memory returns to baseline" is the right test and
it is easy to write a version that proves nothing. The first attempt here drove
1000 chunk loads through the real planner, called `clear()` at the end, and
asserted the body count was back to its starting value. It passed with a `sync()`
that **never dropped anything** — every chunk ever visited stayed resident and
the final teardown tidied them all away.

That is exactly the shape that kills an iOS tab: perfectly clean at exit, and
unbounded during play. So assert the peak _during_ the run:

- peak resident chunks equals the expected residency footprint, not more
- peak body count stays inside footprint × per-chunk budget
- and only then, that teardown returns to baseline

Verify by mutation, and include "drops nothing" among the mutations — it is the
one a teardown-only test cannot see.

## Freeing a physics body is three calls, not one

Removing a body from the world leaves the body and its shape allocated in the
WASM heap, where no JavaScript profiler will attribute them and nothing in JS
holds a reference to find them. All three are required:

    HP_World_RemoveBody(world, bodyId)
    HP_Body_Release(bodyId)
    HP_Shape_Release(shapeId)

Two related habits that make this safe rather than merely correct once:

- **Body handles must be map keys, not array indices.** Streaming removes bodies
  from the middle constantly, and an array whose indices shift silently repoints
  every handle held elsewhere — a save, a vehicle, a wheel raycast's ignore
  filter — at the wrong body. Never reuse a handle either: a stale one should be
  an error, not a hit on whatever occupies that slot now.
- **One object owns the chunk→handles mapping.** Handles scattered across call
  sites is how one gets missed on the unload path.

## One residency decision drives both halves

Meshes and collision bodies are disposed by different code on different sides of
the sim/engine boundary. Give them separate residency policies and they drift: a
chunk you can see but cannot crash into, or the reverse, which is worse than
either alone. Compute the plan once, in the pure layer, and have both follow it.

Two details that fall out of doing it that way:

- **Collision centres on the player; meshes centre on the look-ahead.** Bodies
  matter where the car is, geometry matters where it is looking. Centring
  collision on the look-ahead focus lets a fast car outrun its own collision.
- **Collision radius ≤ load radius < unload radius.** Assert all three
  relationships; they are easy to break while tuning one of them for a visual
  reason.

## Set the streaming radius from the fog, not by feel

The load radius, the far clip plane and the fog density are one decision. Fog at
density 0.0075 erases everything past ~400 m, so with 360 m chunks a radius of 1
already reaches beyond anything visible — radius 2 was generating, meshing and
holding collision for a ring of city the player could not see, and doubling the
worst-case resident set from 25 chunks to 49.

Whenever one of the three changes, re-derive the other two.

## LOD and collision

- Distant chunks render as merged, simplified geometry with no props and no collision.
- Collision geometry exists only within a small radius of the player and is built from
  simplified boxes, never from the visual mesh.
- Buildings collide as boxes. Nobody notices, and the saving is enormous.
- The road surface should be as close to a flat plane as possible under the physics —
  micro-geometry on roads causes suspension jitter at speed.

## Budgets

Every chunk has a stated budget, asserted in tests: max draw calls, max triangles,
max collision bodies, max generation time. A generator that exceeds budget fails CI
rather than being discovered on a phone.

## Testing

- Same chunk from different visit orders → identical.
- Every generated junction has >= 2 exits; dead-end rate below threshold.
- Road network is connected — no unreachable region within a chunk radius.
- Chunk generation stays within time and memory budget.
- Load/unload 1000 chunks in a loop → memory returns to baseline. This is the leak test.
