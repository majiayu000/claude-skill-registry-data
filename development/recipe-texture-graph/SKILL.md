---
name: recipe-texture-graph
description: "Author a procedural material from a reference image — one-call graph spec, contact-sheet debugging to find the stage where the signal died, port polarity and wiring rules, and a numeric stop condition, not eyeballing."
---

# Texture graph (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/texture-graph"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- author a procedural texture or material from a reference photograph
- build a tiling surface — stone, brick, cobble, plaster, wood, metal — in the texture graph
- a texture graph cooks but the map comes out flat, black or inverted
- matching a texture to a reference without a human to look at it
- deciding when a procedural material is DONE

## Ops it names

`texture_graph.author`, `texture_graph.contact_sheet`, `texture_graph.preview`, `texture_graph.score`, `texture_graph.match_reference`, `texture_graph.region_stats`, `texture_graph.inspect`, `texture_graph.script_api`, `texture_graph.templates`, `texture_graph.set_param`, `texture_graph.sweep`, `texture_graph.profile`, `texture_graph.cook`, `texture_graph.apply_to_material`, `loom.place`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
