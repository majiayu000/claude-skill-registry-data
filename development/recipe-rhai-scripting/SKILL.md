---
name: recipe-rhai-scripting
description: "Attaching a Rhai script and proving it RAN — the snapshot-in/effects-out contract, what mem does and does not prove, the fuel limit that fails invisibly, and where the runtime error actually goes."
---

# Rhai scripting (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "gameplay/rhai-scripting"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- attaching a rhai script to an entity over mcp
- the script compiles and nothing happens
- verifying a gameplay script actually fired rather than merely installed
- a script's mem blackboard reads a plausible number that never changes
- writing code-like gameplay logic instead of a blueprint graph

## Ops it names

`script.compile_check`, `script.set`, `script.get`, `script.state`, `script.remove`, `game.play`, `game.pause`, `game.step`, `game.stop`, `ui.messages`, `tag.grant`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
