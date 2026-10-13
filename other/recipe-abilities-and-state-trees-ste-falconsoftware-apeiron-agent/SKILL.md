---
name: recipe-abilities-and-state-trees
description: "Per-ability logic graphs with latent tasks (montage, input, event, target data, delay) and StateTree AI with affordances — authoring them over MCP and proving they ran."
---

# Abilities and state trees (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "gameplay/abilities-and-state-trees"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- an ability needs logic beyond applying its effects (a combo, a montage hit window, a charge)
- waiting for an input press, a montage notify or a gameplay event inside an ability
- building enemy ai as states (patrol, chase, attack) instead of a behaviour tree
- ai that claims a seat, cover point or interaction spot
- an ability or a state tree does nothing and you need to see why

## Ops it names

`gas.grant`, `gas.query`, `gas.cast`, `gas.cancel`, `blueprint.grammar`, `game.door`, `ability.runs`, `ability.activate`, `ability.send_event`, `statetree.state`, `statetree.send_event`, `statetree.affordances`, `graph.new`, `game.play`, `game.step`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron-web:status`.
