---
name: recipe-material-graph
description: "Build a surface in the material node graph — route slot-vs-template-vs-graph first, author the whole chain in one call, read the pin types before wiring, and check the G-buffer lanes rather than the beauty pixel."
---

# Material graph (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/material-graph"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- author a PBR material as a node graph on an entity
- the material renders flat near-white, or black, and nothing you wire changes it
- deciding between a slot material, a shipped template, and a hand-built graph
- a texture is bound but the surface still looks like plastic
- one material has to appear at several tints or roughnesses
- driving base colour / metallic / roughness / normal from procedural nodes

## Ops it names

`material.apply`, `material.apply_template`, `material.create_graph`, `material.author`, `material.compile`, `material.explain_surface`, `material.probe`, `material.explain_slots`, `material.list_nodes`, `material.set_param`, `material.snapshot`, `material.preview`, `material.new_instance`, `material.set_override`, `material.set_texture`, `material.fit_uv`, `material.dump_wgsl`, `material.validate_wgsl`, `material.set_graph_domain`, `mesh.uv_report`, `render.explain_pixel`, `render.histogram`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
