---
name: character-factory
description: Full Character Factory pipeline — from the character the artist imagined to the character rigged, animated (idle, walk, attack, hit, death) and imported into Unity, with everything happening live in Blender. Use ALWAYS when the user asks for a new character ("create another character", "new character in the factory", "run the pipeline"), wants to resume a character, or asks for a step without saying which one. This skill decides the order and the gates of each stage, and hands off to the others (character-design, character-rig, character-clips, character-review, character-engine, character-show — characters acting together, summoner + summons, training target, round with health). Read it before any work in factory/. It also summarizes the 8 GAME principles (readability in the game camera, essence, style × scale, close-up, swarm variation, strike timing, simple rig, test bench with a Death Ray) and points to where each one is detailed.
---

# Character Factory — the pipeline

The artist describes a character; the factory delivers the character rigged, with five clips, measured and inside the
engine. Everything goes through the open Blender (the user **films** the screen), so every stage has to show up in the
viewport.

- Code and manual: `factory/README.md` (tool table + the `clip.json` contract), `factory/docs/TECHNIQUES.md`
  (each lesson with the number that proved it). Read the section for the stage you are in — not the whole file.
- One character = `factory/characters/<id>/` with `brief.md`, `refs/`, `model/`, `rig/landmarks.json`, `anim/*.clip.json`,
  `mocap/`, `review/`, `export/`, `state.json`. `<id>` in lowercase, `<NAME>` = the same in uppercase (object names).
- Complete examples to copy: `characters/brasa/` (dwarf, hammer), `characters/granizo/` (ogre, ice sledgehammer) and
  `characters/alvor/` (paladin: ONE-handed sword, held shield, healing aura, all clips hand-authored + Mixamo
  read as a reference),
  `characters/ocaso/` + `characters/ossinho/` (cloaked necromancer who is NOT a humanoid + the skeleton he summons:
  planted staff, unit that rises from the ground, spell with a projectile) and `characters/toco/` (training dummy: a prop
  that sways, dies by toppling over and respawns — not a character, no Rigify) and `characters/uivo/` (the first QUADRUPED: wolf, trimmed Rigify wolf rig, canter and dash timed to the user's video, gallop, pounce with a shake, sitting howl; `quad_build.sh`) and `characters/centelha/` (a short mage with a ONE-handed staff: living eyes on a single mesh, an AREA spell that falls from the sky and pins a pack from below, glass crystals, a Unity scene with two casts and edge cases; 15 rounds in a `/loop` until the user approved — `loop.json`; the original request is in `loop.json → user_request`, and this repo's `examples/centelha/PROMPT.md`).

## The order, and the exit gate of each stage

Only move on once the gate is measured. Almost all the rework on the first character came from discovering at stage 6 a
problem that stage 1 or 3 showed in seconds.

| # | Stage | Skill | Exit gate (a number, not an impression) |
|---|---|---|---|
| 1 | Brief + a design that fits the animation AND reads in the game | `character-design` | one-page brief with Essence (1–2 traits), Readability and Close-up; silhouette at 64 px checked; generation rules; left/right marker |
| 2 | T-pose concept (MOUTH OPEN) + 3D model + **Remesh (Smart Mesh P1.0 ALWAYS on, body 20k) → Smart UV → 4K Texture** in Tripo (the workspace, or the Agentic Canvas with retopology + bake + Smart UV in one node: §3b) + **the body in underwear ONLY and every garment its own object** (§3d; dressed in Blender: `character-rig` §4h) + separate props + the **paint pass** of the albedo in Blender (§3c) | `character-design` §3 6b–6c, §3a–§3d | real T-pose, empty hands, open jaw, props off the body; `model/<id>_hi.glb` + `model/<id>_game.glb` (clean UV); NEVER 8K (§3a); A/B original vs painted in `paint_look.py`; up to 5,000 Tripo credits per character |
| 3 | Import, game mesh, landmarks, **model gates** | `character-rig` | `model_gates.py`: `overhead`, `corridor` ≥ 1 (and `wrap` after the rig) |
| 4 | Rig (Rigify), weights, props, pose test | `character-rig` | `pose_test.py` + clean shoulder/wrist/hip close-ups; `fist_fit` read; with separate fingers, `hand_test.py` inspected up close |
| 5 | Base pose + attack | `character-clips` | attack closes without `twist_jumps`; `contact_probe` without penetration |
| 6 | Idle, walk, hit, death on top of the base pose | `character-clips` | five clips start in the same pose (≤ 1 mm); `./contacts.sh`: contact AND ground clean in all five |
| 7 | Evidence package + critics | `character-review` | weighted score and list of fixes; or the user's "it's good" |
| 8 | Export + Unity | `character-engine` | FBX round trip ≤ 0.05 cm; import `ok=True problems=[]`; transitions measured |
| 9 | (if any) characters together: summoning, target, round | `character-show` | show playing in the viewport; planted foot ≤ 0.1 cm/frame on a curve; target ≤ 5 mm on the ground; the same routine measured in Unity (`CFRoundProbe`) |
| 10 | Lab in Unity: the unit at game size and in the game camera, against the others | `character-show` §9d | `CFDuelLab` routine run: hit-stop frame = contact, clean 3-state death, on-screen height + 1:1 silhouette, Portrait; blends saved in `<NAME>.blend_tune.json` if they changed |

For a new painted collectible, or when a render looks plastic, use the [painted matte miniature workflow](../character-design/references/painted-miniatures.md).
It links the concept and bake to Blender material checks, game-size poses, and Unity Play Mode evidence.

The user's eye is the final gate: when they say the character is approved, stop iterating with critics and
record that in `state.json`. The critics' score is for finding defects, not for arguing with whoever approved it.

## The 8 GAME principles (what the player sees — they apply at every stage)

The gates above say the character is RIGHT; these say it WORKS in a mobile game seen from above at ~64 px.
They come from the user ("hyper important", 2026-11-14) and each one has a rule with a number in the stage's skill:

| # | Principle | The rule, short | Where it is detailed | How it is proven |
|---|---|---|---|---|
| 1 | **Readability first** | one glance = who it is + what it does; clear silhouette, exaggerated poses, broad movements; ALWAYS judge in the game camera at game size (1.4 m = 64 px, 1 px ≈ 2.2 cm), never in a Blender close-up | `character-design` §0a · `character-clips` §6b · `character-review` §0 | lab G + V (measured on-screen height, 1:1 silhouette); the critics' blind glance |
| 2 | **Amplified essence** | research who it is, reduce it to 1–2 traits (adjective + verb), push them until they read; one strong idea > many details | `character-design` §0b · `character-clips` §6b | Essence section + trait × clip table in the brief; a critic answers "does the trait show?" per clip |
| 3 | **Style at scale** | miniature action figure: simple, chunky shapes, bold proportions, 3–4 colors + 1 accent, nothing < 2 px (≈ 4–5 cm) carrying identity | `character-design` §0c | silhouette and values in the concept at 64 px before Tripo |
| 4 | **Close-up = personality** | unlock, victory, menu: the unit turns to the camera and leans ~7° up/back; big, unobstructed face; an expression per moment | `character-design` §0d · `character-clips` §6b (`victory`) · `character-show` §9c (Portrait take) | Portrait after a knockout (`env/duel/shots/lab/retrato_alvor_s.jpg`) |
| 5 | **Small variations** | a swarm does not walk in step: the engine varies pace ×0.92–1.08 and size ×0.95–1.05 per unit; the whole trick is 2–3 walks per swarm unit | `character-clips` §6b · `character-engine` §2e | lab: Summon 2–3× + Walk; different phases within 2 s |
| 6 | **Timing sells the strike** | short strike, clear contact frame, hold on the impact (clip 2–3 frames + engine 0.06 s / 0.13 s on death), spark + shake + FOV punch on the same frame | `character-clips` §6b · `character-engine` §2e | lab 1/10 + `+1 quadro`: the `[HIT-STOP]` frame is the contact pose |
| 7 | **Simple, mobile rig** | clean skeleton: base 30, fingers ≤ 8, ≤ 10 character bones (ear, tail, cape, beard, chain), deforming ≤ 50; a one-shot effect does not live in the skeleton | `character-rig` §0 | the manifest's `bones` key + the count in the Unity prefab |
| 8 | **Fast test bench** | a map with a "Death Ray" and buttons to spawn, attack, take damage and die; Animator blends tuned IN THE ENGINE and saved per character | `character-show` §9d (`CFDuelLab`) · `character-engine` §2e (`CFBlendTune`) | the lab's 8-step routine run, captures in the package |

New character: the brief already comes out with Essence, Readability and Close-up (stage 1); stage 10 below closes with
the lab. A character approved before these principles is not redone on your own initiative: whatever it does not meet
becomes an item in `state.json` (`game_principles`), reported to the user with the number (e.g. BRASA / GRANIZO hit
at 1.30 s, 23 frames from apex to contact; FERRUGEM carries 103 effect bones).

## Operating rules (they apply in all skills)

- **Always `cd factory` before a command** — the working directory drifts between calls.
- **Blender**: 4.5 LTS open with the *MCP for Blender* addon (socket 127.0.0.1:9876). Everything goes through
  `python3 cf/bl.py run blender/<script>.py --arg k=v` (or `bl.py code "<py>"`). If Blender crashes:
  `open -a ~/Applications/Blender-4.5.12-LTS.app <file.blend>`; the socket comes back on its own in ~3 s.
- **Never `raise SystemExit` in a script that runs in live Blender**: the addon only catches `Exception` and Blender
  closes in the middle of the recording. End with `cflib.out(...)` inside an `if/else`.
- **Show the stage**: `blender/board.py --arg title="..."` changes the title board; at the end of a block of work leave
  the result playing (`blender/play.py --arg name=<NAME> --arg action=<NAME>_<clip> --arg mode=play`, or the reel).
  Stop playback (`mode=stop`) before probes and renders.
- **Character facts come from the rest pose** (`mesh.vertices`), never from `bound_box` (that is the mesh posed at the
  current frame).
- **Look before you claim**: close-ups from several sides and several frames (`blender/closeup.py` + `cf/sheet.py`)
  before saying something is clean. The user complains about what they see in the viewport, not about what the
  metric says.
- **Secrets**: `RUNWARE_API_KEY` only in `.env` at the root (outside git). No user name, email or project in
  requests to external services. Do not commit unless asked.
- **zsh**: a glob with no match aborts the whole command (`rm -f a/*.x b/*.y` may run nothing at all).
- **Critic agents are read-only** (they do not run Blender or pipeline scripts): the session is being recorded and a
  second process touching the scene ruins the take.

## Switching characters in the live session (what has already gone wrong)

- **A destructive script has no dry run unless its header says so**: `reset_character.py --arg dry=true` (an invented
  flag) deleted the 99 objects in the scene. Read the header; use `--arg backup=<file>`.
- **Check `bpy.data.filepath` after the reset**: the session kept pointing at the previous character's `.blend`
  with the new one inside — a Ctrl+S would overwrite it. Right after the import: `save_as_mainfile(filepath=<new>, copy=False)`.
- **Opening another character's `.blend` in the live session** (without closing the Blender being filmed): save the
  current one and schedule `bpy.ops.wm.open_mainfile(filepath=…)` with `bpy.app.timers.register(fn, first_interval=1.0)`
  inside `temp_override(window=…)` — never directly in `bl.py code` (the socket reply dies with the context). The
  addon's server survives the load; poll `bpy.data.filepath` until it changes (< 4 s on the 450 MB files).
- **Characters together** (summoner + summons, target, round) go to their own `CF_Show` scene (skill `character-show`):
  while it is on screen no pipeline script runs (`--arg mode=off` returns to the character's scene);
  `--arg mode=remove` before saving the `.blend`; "they vanished from the screen" = `--arg mode=play` (turns the
  collections' eye back on).

## Factory state and memory

- **Loop until a score** (`/loop ... don't stop until score >= 9.5`): the rounds' state lives in
  `characters/<id>/loop.json` (plan, progress, scores per lens, what was measured); each round = measured fixes → pack
  → 3 critics → weighted score → `ScheduleWakeup`. A new user request in the middle (crystals "cleaner", "more
  translucent") becomes a round of its own, recorded and shown to the next critics. Stop when the user approves, even
  below the score.
- When you close a stage, update `characters/<id>/state.json` (`updated`, what was done, the gate numbers, `next`).
  That is how a new session resumes the work.
- A new lesson (something that took more than one attempt) goes into `docs/TECHNIQUES.md` with the **measured number**
  and the rule; if the lesson changes how the next character is designed, rigged or animated, also update the stage's
  skill.
- A parameter that lives in the base pose or in the rig (`rig/landmarks.json`: `weapon.grip`, `grip`, `keepclear`,
  proportions) propagates to ALL clips: if it changed, rebuild the five (attack first) and measure the five.

## How to report

Short status in the user's language after each block: what changed, the number that proves it, what is left. A limit that belongs to
the model (not to the animation) is stated as a limit, with the measurement — and becomes a design rule for the next
character.

## Second character onward

1. One `.blend` per character (`characters/<id>/<id>.blend`); the live scene holds only the character being worked on.
2. Brief → Tripo → `import_model.py` → `gameready.py` → **measure** (slices, colors, `look_at.py`) → `landmarks.json` →
   `model_gates.py` → `proportions.py` if needed → `./rebuild_rig.sh`.
3. `cf/port_clip.py` from an approved character → `limb_radii.py` → `./build.sh` / `./look.sh` / `./contacts.sh` per clip.
4. `reel.py` + `play.py` (the user films) → `lod.py` → `export.py` → `cf/to_unity.py` → the Unity importer.

The second character (GRANIZO, an ice ogre with a sledgehammer) went from brief to Unity with all five clips in one
session. Everything that got stuck became data in the landmarks or a script argument — no character name in the code.
If a script mentions `beard`, `backpack` or `BRASA` outside a comment, generalize before working around it.
