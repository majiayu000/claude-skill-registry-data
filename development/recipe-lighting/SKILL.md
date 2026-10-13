---
name: recipe-lighting
description: "Light a scene — pin the clock, aim the sun through the clock and not its transform, fix the AMBIENT before the lamp's intensity, budget the local shadow atlas, and place and bake reflection probes."
---

# Lighting (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/lighting"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- light a scene, or relight one that reads flat
- a light you placed appears to do nothing
- shadows are blocky, missing, detached, or absent under one light
- moving the sun entity has no effect
- placing reflection probes, or GI looks inert
- a night scene still reads like an overcast afternoon
- sunrise or sunset looks flat, or lit from both sides

## Ops it names

`env.set_time`, `env.apply_look`, `env.set_ambient_tint`, `env.set_sky_ground`, `env.set_fog`, `env.set_sun_disk`, `env.set_hdri`, `env.set_hdri_rotation`, `env.day_night`, `place.actor`, `place.catalog`, `scene.inspect`, `scene.describe`, `scene.set_component_field`, `scene.fit_probe`, `bake.probe`, `render.exposure`, `lookdev.begin`, `lookdev.end`, `render.ab_capture`, `render.explain_pixel`, `render.histogram`, `render.gi_oracle`, `render.set_effect`, `render.shader_debug`, `qa.lint_scene`, `camera.register`, `camera.place`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
