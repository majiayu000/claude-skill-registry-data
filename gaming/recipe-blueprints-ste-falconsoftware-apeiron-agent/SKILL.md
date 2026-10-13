---
name: recipe-blueprints
description: "Building a Blueprint graph over MCP and proving it RAN — text authoring and its parenthesis rule, the tag nodes, plugin-crate nodes in the palette, and why \"BeginPlay HAS fired\" is not evidence."
---

# Blueprints (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "gameplay/blueprints"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- building or editing a blueprint graph over mcp
- the blueprint is attached and the entity does nothing
- verifying a blueprint actually executed rather than merely installed
- using a node a game or plugin crate exported into the palette
- granting or testing gameplay tags from a graph

## Ops it names

`blueprint.create`, `blueprint.from_text`, `blueprint.to_text`, `blueprint.add_node`, `blueprint.connect`, `blueprint.set_param`, `blueprint.list`, `blueprint.validate`, `blueprint.palette`, `blueprint.entities`, `blueprint.state`, `blueprint.trace`, `blueprint.vars`, `tag.query`, `tag.grant`, `game.play`, `game.step`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
