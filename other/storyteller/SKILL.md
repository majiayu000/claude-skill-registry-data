---
name: storyteller
description: "Use for any story, chapter, scene list, cast sheet or animator brief in a story game: bible, intimacy ladder, style presets, critic rubric, scene briefs."
---

# Storyteller: plan, write and brief a story game

The guide lives in `references/` (01 architecture, 02 archetypes, 03 ladder and pacing, 04 presets,
05 pipeline and rubric, 07 the Story team, 08 scene clips, player and sound, sources). Read `05` and the one file the task needs, never all.
Project specifics (the cast, the chapter plan, explicit text) live in the game's own private repo, never here
(this repo is public).

## Every time

1. **Content line**: every character is an adult fictional original or an adult version stated on page; no
   minors; explicit scenes are present-day adults only, flashbacks stay non-explicit. Explicit
   text lives only in the private game repo or behind the game's 18+ gate.
2. **Bible first**: cast sheets, relations, world, the preset. No bible yet: write it before chapter 1. Order and locks: `docs/preproduction-workflow.md`; sheet template `docs/templates/character-bible.md`.
3. **Ladder** (`03`): name each chapter's rung in the plan; escalate one rung per scene, never skip one; start
   early (first teasing beat by chapter 2 or 3) and keep a steady curve to the finale.
4. **Preset per chapter** (`04`), never mid-beat.
5. **The run** (`05`): plan (15 lines) → draft in the game's beat format → critic rubric, fail at ≤ 3 →
   continuity pass (who knows what, which flag is set, first kiss is first once, times and places) → lint →
   one chapter or one arc per PR.
6. **Models** (`07`): Planner and Director Opus, Writer Sonnet (Opus for the heat scenes and finales), Editor
   Sonnet, Continuity Haiku.
7. **One home**: one branch per story, merged when done; never leave chapters on side branches (2026-10-21:
   the spicier version sat unmerged on two branches and the owner saw the old one).

## Scene list and animator brief

Every animated or illustrated beat gets a row in one scene list (chapter, beat, slot name, type) and a brief
the animator can build from without asking. The brief template is in `docs/game-pipeline.md` (Scene brief).

## New story

Keep 01 to 05 and 07, write the new story's map (device, lead heroine, lineup with no two tells alike, endgame,
heat curve, PR order), then the bible, then chapter 1.
