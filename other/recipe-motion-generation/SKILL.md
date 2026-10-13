---
name: recipe-motion-generation
description: "Generate a character animation from a text prompt or author one by hand, then clean the raw clip into a game-ready loop — crop the gait cycle, gate the contacts, bake the planting, close the seam, measuring every step."
---

# Motion generation (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/motion-generation"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- asked to generate, invent or author an animation from a description
- the clip library lacks a move (strafe, backpedal, turn, idle variant) and nobody is buying content
- a generated or imported clip pops once per cycle, or its feet skate
- asked to turn a raw motion clip into a locomotion loop for a blend space
- hand-authoring a clip's keyframes, or a hand-authored clip looks almost right
- setting up the local motion runtime for the first time

## Ops it names

`scene.create_clip`, `control.derive`, `control.list`, `control.set`, `control.reset`, `scene.set_clip_channel`, `scene.rig_query`, `scene.set_anim_time`, `plugin.enable`, `plugin.motion-gen.status`, `plugin.motion-gen.generate`, `plugin.motion-gen.jobs`, `plugin.motion-gen.keep`, `anim.detect_sync_markers`, `anim.synthesize_clip`, `anim.set_clip_curve`, `anim.list_clips`, `anim.measure_foot_slide`, `scene.set_anim_clip`, `scene.screenshot_clip`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
