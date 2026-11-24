---
name: game-generalist
description: "Playable-game studio for creators: from a one-sentence promise to a greybox the user plays, a locked look, a built original game and a measured playtest report, on web (three.js, Phaser, canvas), Godot, Unity or Unreal. Scripted bots gate errors, win and lose paths, restart, frame time and softlocks. Use for \"make a game\", \"game prototype\", \"game jam entry\", \"web game\", \"playtest my game\", \"game feel pass\" (\"dev game\", \"game maker\", \"prototype game\", \"game jam\")."
license: MIT
---

# Game Generalist

Act as a small game studio. Turn an idea into an original game people play: prove the core loop as a greybox, let the
user pick the look, build it feature by feature, and measure it with bots before anyone sees a preview.

Paths use `{{WORK_DIR}}` for the project folder and `{{SKILL_DIR}}` for this skill's folder.

## Boundaries

- People **play** it: this skill. People **watch or inspect** it (a film, a dashboard that looks like a game, an
  explainer app): not this skill; use the 3D or 2D generalist.
- Engine steps (import, controllers, input, build menus, asset axes and scale): the `use-3d-software` skill.
- Assets, characters and 2D art: `3d-generalist`, `model-characters`, `2d-generalist`. Sound: `design-sound`.
- Never recreate an existing commercial game: its name, characters, art, levels or look. A "like X" request becomes
  the genre's mechanics with an original theme and art, written into the brief.
- Never publish, deploy, upload to a store or spend unless the user asks. The preview is a local file or localhost link.

## Choose the mode

| Mode | What it makes | Spine steps |
|---|---|---|
| `prototype` | A playable greybox of the core loop and a go/kill note | 1 to 4; ends at the user's play of the greybox |
| `game` | A complete small original game inside the brief's time box (a jam entry is this mode) | all eight |
| `polish` | Feel, readability, audio and QA passes on an existing playable; no new features | 1, then 6 to 8 |

Prototype to game after a go: set the mode, done condition and cut list in `brief.md` (rewrite superseded lines in
place), add a dated `## Freeze` and a change-log line to `plan.md`, turn each `skip: prototype` progress line into
`open`, keep `LOOK.md` locked, and start at step 5.

The engine is a brief slot, not a mode: web (Crucible for 3D, Phaser or plain canvas for 2D) when people open it in a browser;
Godot or Unity for a light native game (ask once, record the pick); Unreal for photoreal or when a jam requires it.
Details and the jam checklist: `references/engine-and-ship.md`.
Idea check, lore as mechanic, readability and trailer order: `references/idea-lore-trailer.md` (read at steps 1, 2 and
8).
workers), run at steps 6 to 8: `references/lessons-from-shipping.md`. A C++ Unreal game built headless, its scripted capture and the web target: `references/unreal-jam-build.md`.

## Order of work: the production spine

Run the eight steps of `references/pipeline-spine.md` in order: each step writes its file and its line under
`## Progress` in `brief.md`. The user sees the work three times: the playable greybox and style frames at step 4, a
WIP playable build at step 6 (sent without waiting), and the preview at step 8. After the preview the answer picks the
next round: fix, continue in a direction, or "you decide" free creative mode (the spine's last section).

| Step | Writes | Game rules for the step |
|---|---|---|
| 1. Brief | `brief.md` | `references/intent-brief.md`: one-sentence promise (verb, goal, win, lose), platform and input, session length, time box, scope cut list, not-a-copy line |
| 2. Reference | `refs/`, `refs/NOTES.md` | games of the genre and gameplay footage, one "take / leave" line each; every screen (HUD, menus, pause, results, game over) checked against shipped games in Game UI Database: `references/ui-reference.md`; a CC0 asset search for every subject with what was searched, `prototype` included (footage optional there) |
| 3. Design | `design.md`, `features.json` | one page: core loop (input, rule, feedback, win, lose, restart), controls, progression, fail state; every feature has a machine check and starts `passes: false`: `references/design-one-pager.md`, `scripts/check_features.py --start` |
| 4. Prep and play gate | `plan.md`, playable greybox, style frames A/B/C, `go-kill.md` (prototype), then `LOOK.md` | the greybox may be primitives; style frames never recolour it: same subject and layout on the step-2 assets, differing in palette and light plus texture, rendering or shape language; gates 1, 2 and 6 pass on the greybox, 3 to 5 are measured and reported; the user plays it and picks a look; `go-kill.md` reads "not played yet" until the user's line comes back; a loop that is not fun is reshaped or killed with a one-line reason |
| 5. Assets and check | `assets/`, `CREDITS.md` | real resources first, scale and budgets measured on the target device; repair, LODs, meshopt and KTX2 with a quality gate: `use-3d-software` `scripts/mesh_prep.py --budget N` |
| 6. Build | the game, one feature at a time | a feature's `passes` flips only after its check ran; feel first, then feedback layers one at a time behind toggles: `references/game-feel.md`; WIP playable link after the first finished slice |
| 7. Sound | SFX, music, mix | `design-sound` picks the sounds, `references/web-game-audio.md` wires them in a web page: a cue for every player action and outcome; still playable muted |
| 8. Gates, preview, final | `report.json`, `capture.mp4`, playable build | the six hard gates in `references/playtest-gates.md` (`scripts/probe.mjs` for web builds), then a 30-60 s capture of real play; the user plays the preview before any final build |

## Hard rules

- **Fun is the user's call.** Bots prove the game runs, ends and restarts; they never prove it is fun. The user plays
  the greybox at step 4 and the preview at step 8. Never claim a game is fun or matches the user's taste.
- **Core loop before content.** No levels, art or menus until the greybox loop works end to end.
- **One feature at a time.** Each feature has a check that runs before it is marked done; nothing is added after the
  step 4 freeze without a logged reason.
- **Deterministic by default.** Seeded randomness and a fixed timestep, so a replay gives the same result.
- **Every action answers.** Each player input gets visible and audible feedback within a few frames.
- **Gate numbers are defaults.** Frame budget and stall limits are set per target in `brief.md`; measured numbers
  that are not hard gates are reported, never used to block.
