---
name: lair-spawns
description: A legendary lair is also a wild spawn, and a legendary spawns only where its lairs stand. Applies whenever adding, moving or removing a lair, a legendary's biomes, or a legendary in a biome's spawn pool.
---

# A lair is a wild spawn

**Every biome that hosts a legendary lair stages each of that lair's residents in its own spawn pool.** A player who finds a lair in a biome can also meet its legendary walking that biome, and the dex lists both.

The lairs a biome hosts are `BIOME_LAIRS` in [`src/data/overworld/lair.ts`](../../../src/data/overworld/lair.ts). The pools are the files under [`src/data/biome/`](../../../src/data/biome/).

## What it takes

For each biome in a lair's host list, and each resident of that lair:

- the resident sits in the `special` band of one of that biome's pools at weight 10, in every period its `activeTimes` covers. The pool is the one its habitat fits (`spawn-surfaces`), so Kyogre stands in the beach's water pool,
- the resident's own `biomes` list names that biome, since a pool may only stage a species that says it lives there.

Adding a lair to a biome means adding those spawns in the same change. When a spawn is unwanted, take the lair out of that biome instead. Never leave one without the other.

## Mythicals are the exception

A mythical's lair is never hosted by a biome: a relic is the only way into one, and `getBiomeLairs` filters them out. A mythical still spawns in its home biome, through that biome's `mythical` band, with no lair involved.

## The test

The rule runs both ways: a legendary lives where its lairs stand and nowhere else. A roaming legendary is not an exception; if it should be met in a biome, that biome hosts one of its lairs.

Two tests in `test/data/spawns.test.ts` hold it:

- `stages a legendary wild wherever its lair stands` fails on a hosted lair's resident missing from the special band of the biome's pools.
- `stages a legendary nowhere its lairs do not stand` fails on a legendary whose `biomes` names a biome that hosts none of its lairs.
