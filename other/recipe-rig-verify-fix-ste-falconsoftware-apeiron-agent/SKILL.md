---
name: recipe-rig-verify-fix
description: "Judge a finished bind with numbers and repair what the numbers find — the five rig judges in the order they must run, what each one is structurally blind to, and which weight verb fixes which defect."
---

# Rig verify fix (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/rig-verify-fix"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- a bind is done and you need to know whether it is any good
- the skin tears, stretches, collapses or passes through itself
- a rendered frame looks wrong but the deform numbers look fine
- choosing between smooth_weights, paint_weights, set_skinning and a re-bind
- asked whether a pose is standable or anatomically possible

## Ops it names

`mesh.rig_readiness`, `rig.check_fit`, `rig.check_deform`, `rig.check_intersect`, `rig.balance`, `rig.check_limits`, `rig.deform_report`, `rig.bend_sheet`, `rig.plate`, `rig.smooth_weights`, `rig.paint_weights`, `rig.mirror_weights`, `rig.clean_weights`, `rig.set_skinning`, `rig.weights`, `rig.stack`, `scene.bind_skin`, `scene.screenshot_views`, `scene.screenshot_clip`, `scene.set_view`, `game.play`, `game.stop`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
