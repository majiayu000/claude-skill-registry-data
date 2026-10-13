---
name: recipe-loom-subassets
description: "Turn a working chunk of a graph — a script body, a kitbash, a repeated part — into a NAMED sub-asset with published parameters, then compose the model out of those instead of re-deriving shapes every time."
---

# Loom subassets (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "authoring/loom-subassets"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- a world.script node has grown past the point where a human could tune it
- the same part appears more than once in a model (a window, a wheel, a hull panel)
- the node graph shows one opaque box instead of describing the asset
- handing a model to someone who should not have to read the script that built it
- detail has to sit ON a sloped or curved surface (shingles, panels, rivets)

## Ops it names

`loom.promote_script`, `graph.collapse_to_tool`, `graph.expand_tool`, `graph.edit_tool_def`, `loom.defs`, `loom.reconfigure`, `loom.nest`, `loom.place`, `loom.set_param`, `loom.author`, `worldgraph.describe_node`, `worldgraph.inspect_rows`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
