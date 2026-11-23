---
name: scene-editor
description: "Narrative scene editor for scripted coverage (wide, mediums, overs, close-ups, inserts): builds line strings of every take, picks the best performance per line (emotion over continuity, Murch's Rule of Six), assembles the scene with J/L cuts and real reactions, times cuts to the end of thoughts and before blinks, checks the 180-degree and 30-degree rules, and hands over an EDL/FCPXML/OTIO turnover. Use when the user says: edit this scene, cut my short film scene, assemble my coverage, choose the best takes, dialogue scene edit, rough cut of a scene, cut on action, L-cuts for reactions. Default skin minimal-mono (no graphics)."
license: MIT
---

# Scene Editor

Coverage in, a scene that plays out: the best reading of every line, reactions that mean something, invisible cuts.

- **Best for:** short films, web series, sketches, music-video narrative scenes, branded drama
- **Inputs:** every take of every setup for one scene (`A_wide_t1.mp4`, `B_cu_anna_t3.mp4`...), the script page, script-supervisor notes if any (circled takes)
- **Default skin:** `minimal-mono` (graphics off) · alternatives `cinematic-phone`, `doc-real`, `essay-mode` (only for titles)
- **Formats:** 16:9 (or the project ratio, e.g. 2.39 letterbox) reference cut + EDL / FCPXML / OTIO turnover
- **Duration target:** the scene's natural length (rule of thumb ~1 min per script page); genre preset `scene-editor`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre scene-editor`.
- Never autocut drama: always `--no-cut` (pauses are performance). run.py's default pause cutting would destroy it.
- Ask: which takes the director circled, the intended tone, and the project aspect ratio.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| establish | 0-10 | where we are and who is there (wide or a telling detail); skip it if the previous scene already did |
| build | 10-70 | dialogue and action; coverage tightens as tension rises (wide -> medium -> close) |
| turn | 70-90 | the moment the scene is about: closest shot, longest hold, best reading |
| button / exit | 90-100 | a reaction, a look, a line; leave the scene early |

- **Choose by Rule of Six:** emotion 51 %, story 23 %, rhythm 10 %, eye-trace 7 %, 2D plane 5 %, 3D space 4 %. Never trade emotion or story for a continuity match.
- **Line strings:** for each line, watch every take of it back to back and mark the best reading. The last complete take is often the keeper, but performance beats polish.
- **Cut points:** at the end of a thought, 1-2 frames before a blink; cut on action about a third into the move; enter late, leave early.
- **J/L cuts:** dialogue split edits 4-12 frames; hold on the listener (L) when the reaction matters more than the speaker's face; bring the next scene's sound 1-2 s early.
- **Avoid "Dragnet" tennis** (every line its own straight cut). Reactions are story choices (Kuleshov): pick the one that tells the truth of the moment.
- **Continuity checks:** 180-degree line kept, >= 30 degrees or >= 1.2x size change between shots of the same person, eyelines matching, props/hands in the same place across the cut (but emotion wins).
- **Pacing:** ASL 3-8 s; let the turn breathe 1-3 s after the line lands.
- **Transitions:** cuts. Dissolve only for time passing; dip to black only at act ends.
- **Music/SFX:** temp score only if asked; room tone under every edit; ambience continuous across cuts.
- **Colour:** reference only (`documentary-natural` 0.3); the real grade comes after lock (`short-film-finisher`).
- **Client (director) judges:** performance choices, invisible cutting, rhythm.
- **Common mistakes:** keeping the clean take over the true one, cutting every line, holding the wide too long, crossing the line by accident, cutting on a blink-less stare mid-thought.

## Make the edit

Transcribe each take once (fast, for line matching):

```bash
python CORE/scripts/prep.py A_wide_t2.mp4 --work takes/A_wide_t2 && python CORE/scripts/transcribe.py --work takes/A_wide_t2 --model small
# repeat per take; a loop:  for f in takes_src/*.mp4; do n=$(basename $f .mp4); python CORE/scripts/prep.py $f --work takes/$n && python CORE/scripts/transcribe.py --work takes/$n --model small; done
python CORE/scripts/selects.py --work takes/B_cu_anna_t3      # per-take sentences and retake groups (paper_edit.md)
```

Build the line strings by reading every take's `transcript.json` line by line; write the chosen cut as a timeline spec `scene.json` (times in each take's source seconds, `words` so the transcript is re-timed):

```json
{"format": "16:9", "fps": 30,
 "clips": [
   {"src": "A_wide_t2.mp4", "in": 3.10, "out": 9.40, "words": "takes/A_wide_t2/transcript.json"},
   {"src": "B_cu_anna_t3.mp4", "in": 12.05, "out": 16.80, "jcut": 0.27, "words": "takes/B_cu_anna_t3/transcript.json"},
   {"src": "C_cu_ben_t1.mp4", "in": 20.30, "out": 24.10, "lcut": 0.4, "words": "takes/C_cu_ben_t1/transcript.json"},
   {"src": "B_cu_anna_t5.mp4", "in": 31.00, "out": 38.60, "words": "takes/B_cu_anna_t5/transcript.json"}]}
```

Assemble, review and look:

```bash
python CORE/scripts/run.py - --timeline scene.json --style SKILLS/minimal-mono --genre scene-editor --no-cut \
  --format 16:9 --work sc --stop-after plan
python CORE/scripts/editor.py review sc/plan.json --genre scene-editor          # cut scores per join, read review.md
python CORE/scripts/render.py sc/plan.json --frames 2,8,15,25
python CORE/scripts/render.py sc/plan.json && python CORE/scripts/finish.py sc/plan.json --platform youtube
python CORE/scripts/export_edl.py sc --out-dir sc/handoff --title "SC12"
```

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Graphics off:** delete every element the skin adds (`"elements": []`) except a slate `titlecard` if the director wants one ("SC 12 · v002").
- **Aspect:** `"finish": {"letterbox": 2.39}` for a scope reference; framing stays the camera's.
- **Room tone:** `"roomTone": true`; ambience bed as `"music": {"src": "amb_room.wav", "volume": 0.3, "duck": false}` if the location had one.
- **Colour:** `"color": {"look": "documentary-natural", "intensity": 0.3}` for review only.
- **Notes:** after each director note, change only the spec clip(s) involved, rebuild into a new work folder (`sc_v003`), keep every version.

## Deliver

```bash
python CORE/scripts/deliver.py sc/plan.json --to youtube --out-dir sc/deliver --no-post --no-thumbs     # review copy
python CORE/scripts/qc.py sc/final.mp4 --plan sc/plan.json --platform none
```

- **Turnover:** `sc/handoff/*.edl`, `.fcpxml`, `.otio`. Known limit: for a timeline-assembled scene the hand-off references the assembled `sc/source.mp4`, not each camera original; give the editor/colourist the spec (`sc/timeline.json` lists every source file and in/out) alongside it.
- Then lock picture and finish with `short-film-finisher`.

## Check before delivering

- Every line's chosen take noted (`takes_used.md`: line, take, why); circled takes respected or the choice explained.
- No accidental line crossing, no jump cuts between near-identical framings, eyelines match.
- Room tone under every edit; no audio pops at J/L points.
- Reactions are real reactions from the same scene (no stolen reactions in documentary-style pieces).
- Tell the user: scene length, takes used, which notes were addressed, version number, files.

## Example requests

- "Cut scene 12 from these 14 takes - best performances, L-cut on Ben's reaction."
- "Assemble my short film's dialogue scene, check the 180 rule, give me an EDL for Resolve."
- "Recut the argument scene so it builds; hold longer on the turn."
