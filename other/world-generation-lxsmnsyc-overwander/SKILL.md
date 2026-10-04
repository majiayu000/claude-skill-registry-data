---
name: world-generation
description: The world has two generations, the live one is frozen, and every roll that places something on the ground goes through `world.draws(key)` with a name. Applies whenever changing terrain, biomes, scenery, landmark placement, towns, portals, cave mouths or start positions, or any table that stores something placed on the ground.
---

# The world has generations

A world is read with one `Generation` (`src/overworld/world.ts`), set when it is built and carried to its cave layer.

- **First** is the live world. Every map a player has seen is its output, so its output never changes. `test/overworld/generation-fingerprint.test.ts` pins it, and a change that moves that fingerprint moves every player's towns, gym seats and catch origins.
- **Second** reads hashed simplex fields (`src/core/simplex.ts`) and keyed rolls. Its fields never repeat, and a roll added to it moves nothing already rolled. It is pinned too, so changing it is a decision rather than an accident.

`VITE_WORLD_GENERATION=2` builds the shared world on the second.

## Rows tied to the ground carry their generation

Positions, towns, gym seats and challenges, raids, stops, snapshots, encounters, fled keys and every claim table have a `generation` column with no default. A build reads and writes only `WORLD_GENERATION` (`src/overworld/current.ts`), so switching generations hides the other world's rows instead of deleting them.

- Every query on those tables filters on `generation`, and every insert writes it. A forgotten insert fails on the missing column; a forgotten filter does not, so check reads by hand.
- The generation is part of each key, since ids built from chunk seeds read the same in both worlds. Raids are the exception: their `id` stays the key, and a later generation's raid id starts with `#<generation>`.
- A new table holding anything placed by the world gets the column and the key the same way.

## Placing something: name the roll

Anything that decides where a thing stands takes its rolls from `world.draws(key)`, never from a fresh `AleaRNG`:

```ts
const draws = world.draws(`${chunk.seed}landmarks`);
const count = MIN + Math.floor(draws.random('count') * SPREAD);
const order = shuffled(sourceOf(draws, 'order'), cells);
```

- The first generation ignores the name and reads the stream in call order, so **never reorder the calls** in an existing roll: that alone changes the live world.
- The second keys each roll on its name and how many of that name came before. A new decision gets a **new name** rather than an extra call under an old one.
- A helper that wants a plain source (a shuffle, `pickFreeCell`) takes `sourceOf(draws, name)`.

Content that turns over with the clock (spawns, raids, NPCs, caches, nests) keeps its own `AleaRNG` seeds, because the server re-derives and stores them. So does the battle engine.

## Fields

A field is a `Noise2D`. On the second generation it is `new SimplexNoise(hashString(seed), salt, octaves)`, with a salt of its own in `FieldSalt`. Its values are mapped onto the first generation's Perlin spread, so every threshold in `src/overworld/fields.ts` cuts the world in the same proportions on both. A new octave count needs its own measured knot table in `simplex.ts`; the noise test checks the proportions.

A cell's climate is read through `world.getCellBiome`, `getCellClimate` or `getCellElevation`, which remember each chunk's values; never sample the climate or warp fields directly, and never put a second memo in front of those calls. Second-generation fields read at one shared point go through a `SimplexStack`, which pays for the lattice once.
