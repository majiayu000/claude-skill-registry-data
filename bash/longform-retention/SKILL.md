---
name: longform-retention
description: "High-retention YouTube long-form editor (MrBeast-memo style structure, widely reported but leaked/unofficial): pays off the title and thumbnail in the first minute, cold-opens on the best moment, re-engages around 3:00 and 6:00 and then every ~3 minutes, stair-steps the stakes, keeps constant visual change (zooms, counters, timers, SFX, captions) and ends abruptly after the payoff. Use when the user says: edit for retention, YouTube video editing, MrBeast style, challenge video, make my long video hold attention, fix my retention graph, fast-paced YouTube edit. Default skin chapter-pro; any Video Studio skin works."
license: MIT
---

# Long-form Retention

A 8-20 minute YouTube video edited so the retention graph stays flat: promise early, escalate, end on the payoff.

- **Best for:** challenges, experiments, story videos, entertainment talking-head videos, list videos
- **Inputs:** A-roll (one or many clips), B-roll, the title and thumbnail idea (the promise the first minute must pay off)
- **Default skin:** `chapter-pro` · alternatives `bold-bounce`, `news-desk`, `essay-mode` (calmer topics)
- **Formats:** 16:9 1920x1080 master, chapters, thumbnails, 9:16 cutdowns
- **Duration target:** 8-20 min; genre preset `longform-retention`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre longform-retention`.
- The `--genre` preset sets autocut's pause cut (0.45 s) and run.py respects it; pass `--max-gap` only to override.
- Ask for the **title and thumbnail**. The first 60 s must deliver that promise. Match intensity to the topic: the fast style can hurt calm educational content (use `video-essay` or `tutorial-screen` there).

## How a pro cuts this

| time | what happens |
| --- | --- |
| 0:00-0:15 | cold open: the title promise, shown not told; the best visual moment |
| 0:15-1:00 | stakes and rules; prove the thumbnail; no channel intro, no "subscribe" |
| 1:00-3:00 | stop telling, start showing; compress time; quick scene changes |
| ~3:00 | re-engagement: a spectacle, twist, reveal or new stake |
| 3:00-6:00 | attach the viewer to people; escalate |
| ~6:00, then every ~3 min | re-engagement beats; stakes stair-step up |
| back half | energy can dip but never sags; no "in conclusion" |
| payoff | the moment the title promised; end within 1-2 s after it, then end screen (5-20 s) |

- **Pacing:** ASL 3-6 s, 2-5 s in minute one. A visual change at least every 5 s (counter, zoom, B-roll, SFX, angle). Vary shot length.
- **Cut rules:** cut every "um", restart and dead moment; keep reactions that carry emotion. Time compression: show 3 seconds of a 30-minute task with a `timer`/clock chip.
- **J/L cuts:** reactions as L-cuts over the next action; J-cut the next scene's sound to pull forward.
- **Transitions:** cuts, zoom punches, whips with whooshes between scenes; one transition language.
- **Music/SFX:** music changes per section (tension under stakes, release after wins), 18-24 LU under speech; SFX 3-6/min (whoosh on moves, ding on counts, riser into reveals, silence 0.5 s before the payoff).
- **Colour:** `punchy` / `gaming-vivid` 0.6-0.7 for entertainment; skin natural.
- **Captions:** sidecar SRT; on-screen text for numbers, stakes, rules, time ("DAY 3").
- **Client judges:** first-day AVD/AVP, CTR, the second-by-second retention graph, the first-minute drop.
- **Common mistakes:** channel intro before the hook, the promise delivered at minute 8, signalling the end early, flat stakes, uniform pacing, an outro after the payoff.

## Make the edit

```bash
python CORE/scripts/run.py - --clips footage/*.mp4 --auto story --style SKILLS/chapter-pro --genre longform-retention \
  --smart-cuts --retakes --broll broll/ --model small --work yt --stop-after plan
python CORE/scripts/story.py outline --work yt --genre longform-retention    # hooks + beat map vs structure
python CORE/scripts/story.py reorder --work yt --order "s88-s90,s1-s87,s91-s140" --genre longform-retention --format 16:9
python CORE/scripts/run.py - --timeline yt/story_timeline.json --style SKILLS/chapter-pro --genre longform-retention \
  --smart-cuts --work yt2 --stop-after plan
python CORE/scripts/editor.py review yt2/plan.json --genre longform-retention --fix   # retention score, interrupts
python CORE/scripts/render.py yt2/plan.json --frames 5,60,180,360
python CORE/scripts/render.py yt2/plan.json
python CORE/scripts/finish.py yt2/plan.json --platform youtube
```

Read `story_flags.md` after a reorder; reorder only whole sentences for a cold open.

## Refine the plan

- **Re-engagement marks:** list the times near 3:00, 6:00, 9:00... and put a reveal there: `titlecard` ("ROUND 2"), a `counter` of money/stakes, a `timer`, a new location chip, a `riser` -> `impact` SFX pair (`riser` at hit - 1.2 s).
- **Stakes on screen:** `{"type": "counter", "from": 0, "to": 10000, "prefix": "$", "label": "prize pool"}`; `{"type": "timer", "from": 10, "label": "seconds left"}`; `poll` for "who wins?".
- **Pattern interrupts:** `speaker.zooms` alternating 1.12/1.07 where review.md reports stretches over 5 s.
- **Chapters:** top-level `"chapters"` (first at 0, >= 3, each >= 10 s), named as hooks ("The $10,000 mistake").
- **End:** delete anything after the payoff except 5-20 s of end-screen space; no "thanks for watching" over it.
- **Sound:** `"music": {"src": "act1.wav", "under": 20, "duck": "speech-aware", "fitTo": "beats"}`, music premixed per section if it changes; `"roomTone": true`.
- **Look:** `"color": {"look": "punchy", "intensity": 0.6}`.
- **Face-aimed punch-ins:** with `W/track.json` the zooms centre on the face instead of the frame centre: after `run.py ... --stop-after cut` (`--stop-after timeline` for a `--timeline` spec) run `python CORE/scripts/track.py analyze W/cut.mp4 --work W`, then `make_plan.py` (it copies the track into the plan). Per zoom, `"cx"`/`"cy"` (0-1) aim elsewhere; `"toFace": false` keeps centre.

## Deliver

```bash
python CORE/scripts/deliver.py yt2/plan.json --to youtube --out-dir yt2/deliver
python CORE/scripts/qc.py yt2/deliver/final_youtube.mp4 --plan yt2/plan.json --platform youtube
```

- Look at `thumb_*.png`; the thumbnail moment must appear in the first minute.
- Cutdowns: `clip-miner-pro` on `yt2/final.mp4` for 3-5 Shorts.

## Check before delivering

- Title/thumbnail promise visible in the first 60 s; nothing before the hook.
- Re-engagement beat near 3:00, 6:00 and every ~3 min after; stakes rise.
- No 5+ s stretch without a visual change (`review.md`); pacing varies.
- Ends within 2 s of the payoff; `qc.py` passes.
- Tell the user: where each re-engagement is, chapter list, files.

## Example requests

- "Edit my challenge video MrBeast-style - hook in the first 10 seconds, re-engage every 3 minutes."
- "My retention drops at 0:40, recut the first minute so it pays off the thumbnail."
- "Fast-paced 12-minute YouTube edit with counters, timers and SFX."
