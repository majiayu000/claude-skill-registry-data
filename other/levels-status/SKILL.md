---
name: levels-status
description: Show one dashboard of every layer's current and target level, open gaps and pending actions, read from the project's LEVELS.md. Read-only and cheap. Use when the user runs /levels-status or asks where the project stands across the level skills.
summary: See every level and open gap in one table
argument-hint: "[layer]"
model: haiku
---

# Levels status

Arguments: `$ARGUMENTS`

Read-only. This skill changes no file, spawns no agent and starts no other skill.

1. Read `LEVELS.md` in the project root. If it does not exist, say so and list the level skills that can create it, one line each, then stop.
2. If the arguments name a layer, show that layer's section in full and stop.
3. Otherwise print, in this order:
   - A table from the levels block: layer, current level, target level, distance to target, open gaps, date last updated (the `Date:` line of the layer's section). Sort by distance to target, largest first.
   - **Waiting on you**: every pending live step, manual action or unanswered question recorded in any section, with the layer it belongs to.
   - **Accepted risks**: each one with its reason.
   - **Stale**: any layer not updated in over 30 days, or older than the last commit in the project.
   - **Not yet run**: level skills with no row in the block.
   - **Flow**: if the block has a `flow:` row, show it on its own line (current phase, skills left) and keep it out of the table. It is written by `levels` and is not a layer.
4. End with one line: the layer furthest from its target. Do not recommend an action. `levels-next` does that.

If the levels block and a section disagree, show both values and say they disagree. Do not guess which is right.

Report only what the file says. Never estimate a level that has not been recorded.
