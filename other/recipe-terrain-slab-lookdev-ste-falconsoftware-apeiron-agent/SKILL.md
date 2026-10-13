---
name: recipe-terrain-slab-lookdev
description: "Turn a heightfield into the finite BLOCK terrain tools present (extrude down an axis, never solidify), then shade it from the auto_mask layer bus — slope, cavity, flow, sediment, AO — and script masks the catalog lacks."
---

# Terrain slab lookdev (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/terrain-slab-lookdev"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- recreate a terrain reference image in the Loom graph
- make a heightfield a solid block with visible cut sides
- the terrain slab's sides render wrong
- colour terrain by slope / flow / sediment / cavity
- a mask I need does not exist as a node

## Ops it names



Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
