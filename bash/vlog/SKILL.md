---
name: vlog
description: "YouTube vlog editor: turns a day of handheld A-roll, B-roll and phone clips into a chronological story - cold open on the best moment, title, story beats with jump cuts, J/L cuts and B-roll, music that changes per segment, locator/map graphics, end screen - plus Shorts cutdowns and thumbnail stills. Use when the user says: edit my vlog, day in my life, travel vlog, cut my footage into a YouTube video, weekly vlog, behind the scenes video, make my vlog feel like Casey/creator-style. Default skin cinematic-phone; any Video Studio skin works."
license: MIT
---

# Vlog

A day of footage becomes a story with a cold open, a shape and a personality.

- **Best for:** daily / weekly vlogs, travel days, behind-the-scenes, events from the creator's point of view
- **Inputs:** many clips in shooting order (talking A-roll + B-roll), optional music tracks (licensed), a B-roll folder
- **Default skin:** `cinematic-phone` · alternatives `vhs-tape`, `chapter-pro`, `minimal-mono`
- **Formats:** 16:9 1920x1080 (or 4K source) master, 9:16 Shorts cutdowns, 3 thumbnail stills
- **Duration target:** 8-20 min (any length that holds); Shorts 30-60 s; genre preset `vlog`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre vlog`.
- Name or number clips in shooting order (`001.mp4`...). Put pure B-roll in `broll/`, named after what it shows.
- The `--genre` preset sets autocut's pause cut (0.4 s) and run.py respects it; pass `--max-gap` only to override.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| cold open | 0-5 | the best / funniest / highest-stakes moment of the day, 5-15 s |
| title / promise | 5-8 | title card or spoken promise of what today is |
| story beats | 8-90 | chronological; each beat = A-roll line + 2-4 B-roll shots + a music change |
| re-engagement | ~every 3 min | a reveal, a twist, a new place |
| resolution + outro | 90-100 | how it ended, one CTA, end screen space (last 10-20 s) |

- **Pacing:** ASL 3-6 s; a visual change every 4-5 s, faster in the first minute. Hold on real emotion.
- **Cut rules:** jump cuts in talking bits are fine; B-roll covers the boring ones. Top and tail every clip (enter late, leave early). Keep the moments with personality over the "clean" ones.
- **J/L cuts:** bring the next place's ambience in 0.5-1 s before its picture (J); let a line run over B-roll (L).
- **Transitions:** cuts; whip or zoom between locations (matching motion) with a whoosh; dip to black only for a day change.
- **Music:** a different track per segment, cut on a downbeat at the segment change; 20-24 LU under talking, up to full in montages. Room tone / ambience under montages so places feel real.
- **Colour:** one look across phone + camera: correct each clip, then `portra` or `kodachrome` 0.6-0.8 (travel `ektachrome`).
- **Captions:** subtitles as sidecar SRT for YouTube; burned `clean` preset only on Shorts.
- **Client judges:** retention graph, authentic personality, no dead air.
- **Common mistakes:** 60 s of "good morning" before anything happens, music too loud under speech, every clip at the same length, no ambience, ending three times.

## Make the edit

Assemble the day in story order (speech regions kept, B-roll-only clips get a 3 s middle section):

```bash
python CORE/scripts/run.py - --clips footage/*.mp4 --auto story --style SKILLS/cinematic-phone --genre vlog \
  --smart-cuts --retakes --broll broll/ --format 16:9 --model small --work vlog --stop-after plan
python CORE/scripts/story.py outline --work vlog --genre vlog        # pick the cold open from the ranked hooks
```

For full control write the spec yourself (`timeline.md`): cold open first, `jcut`/`lcut` between locations, `transition: "whip"` on location changes, `speedRamp` on travel shots, then:

```bash
python CORE/scripts/run.py - --timeline vlog_spec.json --style SKILLS/cinematic-phone --genre vlog \
  --smart-cuts --format 16:9 --work vlog --stop-after plan
python CORE/scripts/broll.py --work vlog --library broll/ --frequency med --merge vlog/plan.json
python CORE/scripts/editor.py review vlog/plan.json --genre vlog --fix
python CORE/scripts/render.py vlog/plan.json --frames 3,30,90,180
python CORE/scripts/render.py vlog/plan.json
python CORE/scripts/finish.py vlog/plan.json --platform youtube
```

Per-segment music: cut each track to the segment length on bars - `python CORE/scripts/music_fit.py track2.mp3 --duration 74.5 --out vlog/seg2.wav` - and add them as timeline clips' music, or premix them into one bed and use it as the plan `music`.

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Cold open:** move the best moment first (`story.py reorder --order "s40-s43,s1-s39,s44-..."`) and add a `titlecard` after it (`"kicker": "DAY 12", "title": "Lisbon in 24 hours"`).
- **Locators:** `{"type": "map", "pins": [{"x": 0.3, "y": 0.5, "label": "Porto"}, {"x": 0.35, "y": 0.62, "label": "Lisbon"}]}` (stylised dot map, not accurate geography) or a `chip` "LISBON · 9:40 AM".
- **Chapters:** top-level `"chapters": [{"start": 0, "title": "Cold open"}, ...]` (>= 3, each >= 10 s).
- **Sound:** `"sfx"` whooshes 0.4 s before whip cuts; `"roomTone": true`; `"music": {"src": "bed.wav", "under": 22, "duck": "speech-aware"}`.
- **Look:** `"color": {"look": "portra", "intensity": 0.7}`, `"finish": {"grain": 6, "halation": 0.2}`.
- **End screen:** keep the last 15 s visually calm (no captions/elements) for YouTube end-screen cards.
- **Footage clean-up (video, before the spec):** shaky walking or low-light phone clips: `python CORE/scripts/prep.py walk.mp4 --work fix/walk --stabilize --denoise light`, then use `fix/walk/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. Keep deliberate handheld energy. A single-file vlog: add the same flags to `run.py`.
- **Face-aimed punch-ins:** with `W/track.json` the zooms centre on the face instead of the frame centre: after `run.py ... --stop-after cut` (`--stop-after timeline` for a `--timeline` spec) run `python CORE/scripts/track.py analyze W/cut.mp4 --work W`, then `make_plan.py` (it copies the track into the plan). Per zoom, `"cx"`/`"cy"` (0-1) aim elsewhere; `"toFace": false` keeps centre.

## Deliver

```bash
python CORE/scripts/deliver.py vlog/plan.json --to youtube --out-dir vlog/deliver
python CORE/scripts/qc.py vlog/deliver/final_youtube.mp4 --plan vlog/plan.json --platform youtube
```

- Shorts: cut 2-3 moments with the `retention-reel` or `clip-miner-pro` skill from `vlog/final.mp4`.
- Thumbnails: `thumb_*.png` - pick the most expressive face; upload `captions.srt` and `chapters.txt`.

## Check before delivering

- Something happens in the first 10 s; the title promise is paid off.
- Music changes land on bars and never fight speech; ambience under montages; no digital-silence holes.
- One consistent look across cameras; faces natural.
- `qc.py` passes (-14 LUFS, -1 dBTP, no black frames); end-screen space kept.
- Tell the user: runtime, structure (beats with times), music used (licences), files.

## Example requests

- "Edit my Lisbon travel vlog - start with the cliff jump, then the day in order."
- "Cut these 40 clips into a 12-minute day-in-the-life vlog with music and B-roll."
- "Make my weekly vlog plus two Shorts from it."
