---
name: recipe-lookdev
description: "Judge and drive a shot — value structure, silhouette read, palette and warm-cool balance, atmospheric depth ramp, composition — using the environment, grade and fog knobs plus numeric readback instead of eyeballing."
---

# Lookdev (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/lookdev"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- the render is technically correct but looks flat, muddy or amateur
- asked to make a scene look good, cinematic or hero-worthy
- choosing a time of day, fog, or colour grade for a shot
- judging whether a built scene matches an intended look
- preparing a presentable screenshot for a human to look at

## Ops it names

`env.apply_look`, `env.set_time`, `env.set_fog`, `env.set_fog_motion`, `env.set_ambient_tint`, `env.set_clouds`, `render.set_grade`, `render.exposure`, `render.histogram`, `render.region_stats`, `lookdev.begin`, `lookdev.end`, `lookdev.score`, `render.probe`, `render.set_aa`, `ui.overlays`, `scene.screenshot`, `camera.frame`, `camera.bookmark_set`, `camera.bookmark_recall`, `scene.set_component_field`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
