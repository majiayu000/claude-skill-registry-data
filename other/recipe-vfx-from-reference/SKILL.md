---
name: recipe-vfx-from-reference
description: "Recreate a reference effect (fire, a jet, smoke, sparks) from an image — intake, decomposition, the physical bake loop, sizing from the sidecar, judging in time with a numeric score, a stop condition."
---

# Vfx from reference (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/vfx-from-reference"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- recreate this fire / flame / flamethrower / smoke / explosion from a reference
- make the effect look like the reference image
- match a VFX reference
- bake a fire flipbook that looks like this
- judge an effect over time, not from one screenshot

## Ops it names

`editor.context`, `image.stats`, `vfx.bake_fire`, `vfx.bake_status`, `vfx.sheet_stats`, `vfx.capture`, `vfx.measure`, `vfx.score`, `vfx.sweep`, `vfx.sensitivity`, `vfx.effect`, `vfx.spawn`, `vfx.param`, `vfx.template`, `particle.set`, `volume.spawn`, `volume.stats`, `render.exposure`, `ui.follow_agent`, `scene.screenshot`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
