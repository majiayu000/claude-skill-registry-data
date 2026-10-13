---
name: recipe-terrain-worldgraph
description: "Terrain and world-graph authoring — units are world metres, surface-chain routing and mask topology, cook settle polling, and cleaning up stale cooked meshes after a re-author."
---

# Terrain worldgraph (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/terrain-worldgraph"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- authoring terrain through the world graph
- surface layers or masks not showing on terrain
- waiting for a terrain cook to settle
- terrain came out flat after wiring field nodes
- old cooked mesh still visible after re-authoring

## Ops it names

`terrain.create`, `terrain.surface_add`, `terrain.surface_set_base`, `terrain.grass_type_create`, `terrain.grass_stats`, `qa.lint_scene`, `worldgraph.author`, `worldgraph.terrain_status`, `loom.cook_status`, `world.final_cook`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
