---
name: recipe-terrain-erosion
description: "Weather a terrain with real erosion — which of the four sims to pick, why pipe is the default, the knob to turn before adding iterations, and how to prove the relief actually changed instead of trusting the reply."
---

# Terrain erosion (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/terrain-erosion"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- making terrain look eroded or weathered
- adding rivers, valleys, gullies or talus to a landscape
- terrain looks like raw fractal noise and needs geology
- choosing between erode_pipe, erode_hydro, erode_fluvial and erode
- an erosion cook is slow, or the relief exploded

## Ops it names

`terrain.erode`, `terrain.describe`, `terrain.create`, `terrain.make_island`, `scene.screenshot`, `loom.cook_status`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
