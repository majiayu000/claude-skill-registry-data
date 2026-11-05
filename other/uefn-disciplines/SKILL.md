---
name: uefn-disciplines
description: Index that says which kit skill or recipe to read for a design concept. Use when the owner names a concept (feedback, layout, pacing, camera, music, enemies, waves, loot, shop, levels, hunger, quests, checkpoints, saving progress, economy, UI, effects) or a genre (tower defense, shooter, deathrun, adventure, tycoon, survival, roguelike) and you are not sure what to load.
kind: discipline
last_reviewed: 2026-10-30
sources: [original]
---

# Which skill for which concept

Load only the row that matches, read its entry point, and open its references only when needed.

## When to use
- The request is about how a game should work or feel, not about a specific device or error.

**When not to use:** a Verse compile error or a device that misbehaves (use `uefn-verse-build` or `uefn-device-gotchas`), a console or documents question.

| The owner says | Read |
|---|---|
| feedback, juice, punchy, hit marker, reward cue | `game-feel-uefn` |
| layout, blockout, pacing, spawn area, arena size, soft-lock | `level-design-uefn` |
| camera, music, ambience, volume, sound | `camera-audio-uefn` |
| enemies, guards, creatures, patrol, aggro | `game-ai-uefn` |
| quest, mission, objective, collect N, tracked goal, quest reward | `uefn-quests` |
| waves, loot box, shop, money, XP, levels, hunger, quest steps, checkpoints | recipe in the `mechanics` skill: `python Claude/hooks/skills_lib.py recipes mechanics <word>` |
| prices, income, payback, rebirth | `economy-sim` |
| saving progress, persistable data, Verse structure | `verse-patterns`, `uefn-lessons` |
| HUD, menus, widgets | `uefn-ui-widgets`, `game-ui-designer` |
| particles, effects, materials | `uefn-vfx-niagara`, `uefn-materials` |
| memory, many actors, lag | `performance-uefn-checklist`; to measure with the profiler: `uefn-profiling` |
| placing devices and folders | `uefn-level-devices` |
| a new UEFN version, 43.00, update, upgrade, build broke after updating, experimental, before publishing from an older project | `uefn-version-upgrade` |
| a forest, a rock field, many props, scatter, procedural placement | `uefn-pcg` |
| PCG, cinematics, Sequencer, MetaSound, lighting, generated media (Epic's editor skills) | `uefn-epic-skills` |
| a whole genre (tower defense, shooter, deathrun, adventure, tycoon, survival, roguelike, party, sports) | the genre skill named in `Claude/docs/.genre`; its reference items come first, learned items outrank them |

Order when several apply: the genre, then the concept, then the recipe, then the device details.
