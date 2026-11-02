---
name: game-modding
description: "Game mods & commands: Minecraft, Cities Skylines, ultrawide/32:9 gaming troubleshooting."
version: 1.0.0
author: Vesper (curator umbrella)
license: MIT
platforms: [linux, windows]
metadata:
  hermes:
    tags: [gaming, modding, minecraft, cities-skylines, commands, mods]
    category: gaming
---

# Game Modding & In-Game Commands

Umbrella for **modding and scripting the games Tyler actually plays** — which mods
to install, how each engine limits what's possible, and how to write in-game
commands that hit the right targets. Each game has its own reference file with
the full working knowledge; this page is the map.

**Trigger:** "which mods for <game>", "CS2-style roads in CS1", "write me a
command / command block that does X", group teleports, filtered targeting,
"why doesn't this in-game command work".

## Games covered

| Game | Reference | What's in it |
|---|---|---|
| **Minecraft (Java)** | `references/minecraft-commands.md` | Command / command-block authoring: target selectors, tags, group teleports, the homoglyph trap, dimension-scoped selectors. |
| **Cities: Skylines 1** | `references/cities-skylines-modding.md` | The mod stack for CS2-feel road building (NExt2, TM:PE, Network Anarchy, Move It) and the engine limits no mod can fix. |
| **Ultrawide / 32:9 gaming** | `references/ultrawide-32-9-gaming.md` | Forcing unsupported 32:9 (5120x1440) resolutions in games that don't natively support them. NVIDIA GPU scaling, borderless windowed, config edits, R6 Siege specifics. |

Project Zomboid (B42 Lua mods / NPC spawns) has its own deep skill — see
`pz-b42-modding` — because its API surface is large enough to live alone.

## Minecraft commands — the two failures that cost the most time

1. **Bare names in a selector resolve against ONLINE players only.** "No player
   was found" is usually "offline / never joined this world", not a typo. Tag
   with `/tag @a add <shorttag>` while the right people are standing there, then
   confirm with `/tag @a list` before building anything on the tag.
2. **The homoglyph trap.** In Minecraft's font, lowercase `l`, capital `I`, and
   lowercase `i` render near-identically. A tag containing them can be visibly on
   N entities and still be permanently unmatchable in a selector. Don't try to
   match it — add a NEW short tag and leave the original inert.
   Generalised rule: *when a string must match byte-for-byte and you cannot
   inspect the bytes, replace it with something you control.*

Full detail — tags are case-sensitive and per-world, selectors are
dimension-scoped (a Nether command block cannot see Overworld players), plus the
2026-10-11 teleport-button debug session: `references/minecraft-commands.md`,
`references/teleport-button-debug-2026-10-11.md`.

## Cities: Skylines — the mental model that saves hours

- **CS2 road-feel = lane *behaviour*, not road *types*.** CS1 has no "road with a
  turn lane"; turn lanes are TM:PE lane arrows.
- **Drawing a second road as a "turn lane" creates a dead-end street** — the
  classic beginner trap.
- **True CS2 lane-peels are impossible in CS1** (static per-type road meshes).
  Don't promise them.
- **Anarchy overlap fix = elevation** — step one elevation up (~15 m) while
  placing and the road bridges instead of clipping.

Mod stack, priorities, and what each mod actually does:
`references/cities-skylines-modding.md`.

## Notes

This umbrella absorbed the former standalone skills `minecraft-commands` and
`cities-skylines-modding`; their full bodies live in the reference files above.

Driving the game *window* (focus protocol, pixel-scan clicks, co-op input) is not
here — see the `windows-maintenance` umbrella (its
`references/game-co-op-patterns.md`) plus `computer-use` for the built-in driver.
