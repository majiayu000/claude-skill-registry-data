---
name: recipe-loom-kitbash-architecture
description: "Compose architecture — arches, towers, columns, plinths, stairs, crenellations — out of the existing world-graph SOPs and collapse the result into a reusable Loom def, instead of waiting for engine-shipped generators."
---

# Loom kitbash architecture (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/loom-kitbash-architecture"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- building architecture in the editor with no shipped generator for it
- need an arch, tower, column, plinth, stair or battlement
- asked for a castle, keep, fortress wall or cathedral silhouette
- want a parametric reusable building block instead of a one-off mesh
- turning a working node kitbash into a placeable asset

## Ops it names

`worldgraph.catalog`, `worldgraph.find`, `worldgraph.describe_node`, `worldgraph.author`, `worldgraph.add_node`, `worldgraph.connect`, `worldgraph.set_param`, `qa.lint_scene`, `material.apply_template`, `worldgraph.inspect_rows`, `graph.collapse_to_tool`, `loom.from_entities`, `mesh.bevel`, `scene.jitter_transforms`, `graph.expand_tool`, `worldgraph.script_api`, `graph.edit_tool_def`, `loom.wrap`, `loom.reconfigure`, `loom.list`, `loom.place`, `loom.nest`, `loom.set_param`, `world.final_cook`, `loom.cook_status`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
