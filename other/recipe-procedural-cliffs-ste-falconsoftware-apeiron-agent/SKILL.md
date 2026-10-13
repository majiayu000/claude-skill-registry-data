---
name: recipe-procedural-cliffs
description: "Turn a terrain mask into real cliff geometry — slope minus erosion into a mask, the mask into a labelled mesh, the mesh extruded by the mask's own strength, then roughened into rock that survives the next terrain edit."
---

# Procedural cliffs (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/procedural-cliffs"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- making cliffs, rock faces or escarpments from a terrain
- converting a terrain mask into geometry instead of a splat texture
- a cliff outline looks stair-stepped or grid-aligned
- every cliff is the same height and should vary with the mask
- editing one rock changed rocks elsewhere in the level
- building riverbanks, road cuts or mesa caps from a heightfield

## Ops it names

`worldgraph.add_node`, `worldgraph.set_param`, `worldgraph.connect`, `worldgraph.catalog`, `worldgraph.describe_node`, `worldgraph.inspect`, `worldgraph.dryrun`, `loom.node_stats`, `loom.cook_report`, `loom.field_probe`, `loom.field_stats`, `terrain.erode`, `terrain.describe`, `qa.lint_scene`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
