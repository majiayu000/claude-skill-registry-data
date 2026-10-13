---
name: recipe-play-step-verify
description: "Deterministic play-testing over MCP — pause-and-step exact tick windows, the input latch lag, spawn placement, 3D pickup radius, what serializes, and Play on a duplicated world (Stop drops it)."
---

# Play step verify (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "gameplay/play-step-verify"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- play testing a game deterministically over mcp
- stepping the simulation an exact number of ticks
- injected input seems ignored under game.step
- pawn or ai behaves oddly right after spawning
- verifying play mode left editor state untouched

## Ops it names

`game.play`, `game.pause`, `game.step`, `game.stop`, `input.action`, `game.spawn_ai`, `sim.verify_restore`, `sim.hash`, `game.ai_status`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
