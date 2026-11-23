---
name: micro-drama
description: "Vertical micro-drama series editor: cuts scripted footage into binge-able 60-120 s 9:16 episodes - a 3-5 s recap or cold conflict open, one escalation and one turn per episode, tight dialogue with J/L cuts and reaction shots, a cliffhanger in the last 3 s, episode cards and a consistent series template - plus a trailer cut. Use when the user says: micro drama, vertical drama series, short drama episodes, ReelShort/DramaBox-style series, cut my web series into episodes, cliffhanger episodes, vertical soap. Default skin cinematic-phone; any Video Studio skin works."
license: MIT
---

# Micro-Drama

Vertical episodes that end where the viewer can't stop: recap, conflict, turn, cliffhanger.

- **Best for:** vertical drama series, short web series, branded drama, story-driven creator series
- **Inputs:** scene footage shot vertical (or 16:9 to reframe), the script with episode breaks, series title, music cues
- **Default skin:** `cinematic-phone` · alternatives `minimal-mono`, `doc-real`, `vhs-tape` (flashbacks)
- **Formats:** 9:16 1080x1920 numbered episode set, dialogue subtitles (`captions.srt` per episode), a 30-60 s trailer
- **Duration target:** 60-120 s per episode; genre preset `micro-drama`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre micro-drama`.
- The genre preset tightens dialogue pauses to 0.6 s when autocut runs; use `--no-cut` on emotional scenes (pauses are acting).
- Get the episode breakdown from the script (which scenes/lines belong to which episode) and the series continuity notes (costume, props, time of day).

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| recap / cold conflict | 0-10 | 3-5 s of last episode's cliffhanger, or open mid-argument |
| escalation | 10-55 | the problem gets worse; no exposition scenes |
| turn | 55-85 | a reveal, a betrayal, a decision |
| cliffhanger | last 3-8 s | cut on the question (a look, a door, a phone screen), smash to the end card |

- **Pacing:** ASL 1.5-3.5 s in dialogue (tight coverage, close-ups: phones are small screens); hold 1-2 s on the key reaction.
- **Cut rules:** enter scenes late, leave early; cut exposition to the bone; best performance over cleanest take. Reactions are where the drama is.
- **J/L cuts:** 4-12 frames on dialogue; L-cut lines over the listener's face in confrontations.
- **Transitions:** cuts; a smash cut into the cliffhanger end card; `flash-white` for a flashback in/out (with `vhs-tape` style or `sepia` look for the flashback).
- **Music/SFX:** tension score 18-22 LU under dialogue; a `heartbeat` or `riser` into the cliffhanger, `boom` on the end card; silence on the reveal line.
- **Colour:** `fuji-eterna` or `moody` 0.6-0.8 for the series, consistent across all episodes.
- **Captions:** clean dialogue subtitles (preset `clean`), sentence case, inside 10-85 % height (many viewers watch muted).
- **Client judges:** binge-ability (episode-to-episode retention), cliffhanger strength, acting reads on a phone.
- **Common mistakes:** slow openings re-explaining the story, wide shots on a phone, every episode ending on a fade, inconsistent looks between episodes, subtitles covering mouths.

## Make the edit

Transcribe each scene take once (as in `scene-editor`), then write one timeline spec per episode (`ep01.json`) with the chosen takes, `jcut`/`lcut` on dialogue and the recap clip first:

```json
{"format": "9:16", "fps": 30,
 "clips": [
   {"src": "ep00_final_cliff.mp4", "in": 0, "out": 4.0},
   {"src": "sc14_cu_maya_t2.mp4", "in": 2.1, "out": 7.9, "reframe": "face"},
   {"src": "sc14_cu_dev_t1.mp4", "in": 5.0, "out": 8.2, "jcut": 0.2, "reframe": "face"},
   {"src": "sc15_phone_insert.mp4", "in": 0.5, "out": 3.0}]}
```

```bash
python CORE/scripts/run.py - --timeline ep01.json --style SKILLS/cinematic-phone --genre micro-drama --no-cut \
  --format 9:16 --model small --prompt "character names" --work ep01 --stop-after plan
python CORE/scripts/editor.py review ep01/plan.json --genre micro-drama --fix
python CORE/scripts/render.py ep01/plan.json --frames 1,20,50,85
python CORE/scripts/render.py ep01/plan.json
python CORE/scripts/finish.py ep01/plan.json --platform reels
```

`"reframe": "face"` crops 16:9 coverage to 9:16 on the face. Repeat per episode; copy the refined template elements (episode card, captions setup, end card) between plans.

## Refine the plan

- **Episode card:** `{"type": "chip", "text": "EP 3 · The Lie", "start": 4.0, "end": 6.5, "x": 540, "y": 230}` after the recap.
- **Captions:** `{"type": "captions", "preset": "clean", "dodgeFace": true, "cpsMax": 17}`.
- **Phone / message beats:** `chat` with the script's messages (`"messages": [{"text": "I know what you did", "side": "left", "at": 42.1}]`), `notification` for an incoming call.
- **Cliffhanger:** end the last clip on the look; then a `titlecard` end card ("Episode 4 →") 1.5 s; `"sfx": [{"t": 86.0, "kind": "riser", "gain": 0.4}, {"t": 87.2, "kind": "boom", "gain": 0.6}]`.
- **Flashbacks:** a `transition` overlay (`"kind": "flash-white", "at": 30.0`) in and out; the flashback clips get `"color": {"saturation": 0.6}` in the spec.
- **Look + sound:** `"color": {"look": "fuji-eterna", "intensity": 0.7}`, `"music": {"src": "tension.wav", "under": 20, "duck": "speech-aware"}`, `"roomTone": true`.

## Deliver

```bash
python CORE/scripts/deliver.py ep01/plan.json --to reels,tiktok,shorts --out-dir ep01/deliver
python CORE/scripts/qc.py ep01/deliver/final_reels.mp4 --plan ep01/plan.json --platform reels
```

- Name files `SERIES_S01E01_the-lie_9x16.mp4`; keep an `episodes.md` with length, cliffhanger and source scenes.
- Trailer: `trailer-teaser` skill with the best cliffhangers (no spoilers past episode 3).

## Check before delivering

- Each episode opens in conflict within 3 s and ends on an open question in the last 3 s.
- Continuity across episodes (costume, props, time of day); one look for the series.
- Subtitles match the dialogue and avoid mouths; names spelled consistently.
- `qc.py` passes per episode (-14 LUFS, length <= 3 min for Reels/Shorts).
- Tell the user: episode list with lengths and cliffhangers, files.

## Example requests

- "Cut these scenes into 10 vertical micro-drama episodes, each 90 seconds with a cliffhanger."
- "Episode 4 needs a recap of the slap at the start and a stronger ending."
- "Reframe our 16:9 web series to vertical episodes with subtitles."
