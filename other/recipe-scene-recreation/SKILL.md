---
name: recipe-scene-recreation
description: "Recreate a reference image as a 3D scene — intake, in-context decomposition, build-vs-buy routing, clean capture, numeric per-element compare, and the credit and termination guardrails."
---

# Scene recreation (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/scene-recreation"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- recreate a reference image or concept frame as a 3D scene
- handed a photo or screenshot and asked to build it in the editor
- deciding whether to author an element or generate it from an image
- scoring a built scene against a reference
- running an image-to-3D generation with a credit budget

## Ops it names

`editor.context`, `project.memory.append`, `render.region_stats`, `render.compare_shots`, `lookdev.begin`, `lookdev.end`, `lookdev.score`, `ui.overlays`, `scene.screenshot`, `scene.bounds`, `camera.frame`, `place.actor`, `pcg.scatter`, `loom.place`, `loom.from_entities`, `mesh.bevel`, `scene.jitter_transforms`, `graph.collapse_to_tool`, `worldgraph.author`, `level.save`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
