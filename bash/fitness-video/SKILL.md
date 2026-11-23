---
name: fitness-video
description: "Fitness and workout video editor for Claude: turns exercise footage into a 30-90 s vertical workout reel or a follow-along session with rep counters, interval timers, exercise name cards, right-vs-wrong form split screens and music cut to the BPM. Use when the user says 'edit my workout video', 'make a fitness reel', 'add a timer and rep counter', 'HIIT follow-along', 'gym tips short', 'show correct vs wrong form', or hands over training clips. Runs on video-studio-core (timeline, beats, captions, timers, split screens, deliver, QC)."
license: MIT
---

# Fitness Video

Clear form, honest timers, and energy that makes the viewer get up and do it.

- **Best for:** workout reels, exercise tutorials, HIIT/follow-along sessions, coach tips, yoga flows
- **Inputs:** exercise clips (one per move), optional talking-head tips, the workout plan (moves, reps, work/rest seconds), a track
- **Default skin:** `countdown-list` · alternatives `bold-bounce`, `data-story`, `before-after`
- **Formats:** 9:16 master, 4:5 and 1:1 feed; 16:9 for full follow-along sessions
- **Durations:** reel 30-90 s; follow-along = the real workout length
- **Genre preset:** `--genre fitness-video`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: move names, reps/sets, work and rest seconds, level (beginner/advanced), any safety cue the coach wants.
- **No medical claims** ("cures back pain", "burn 1000 calories"): keep text to what the coach can stand behind; add
  "consult a professional" when the workout is intense or targets an injury.
- Timers must match the real work/rest time when the video is a follow-along: viewers train to them.

## How a pro cuts this

**Structure (reel, % of length)**

| beat | % | what goes here |
| --- | --- | --- |
| result / hook | 10 | the hardest or most impressive rep, or the promise ("5 moves, no equipment") |
| exercise 1 | 25 | name card, 2-4 clean reps, one form cue |
| exercise 2 | 25 | same pattern |
| exercise 3 | 25 | same pattern |
| finisher + CTA | 15 | the burnout move, "save this workout" |

**Pacing.** ASL 1.5-3 s; visual change every 2.5 s. Cut on the rep (the bottom or top of the movement), on the beat
when you can. Follow-alongs hold one wide shot per move with the timer running: don't cut away from the form.

**Cut rules.**
- Show the full range of motion at least once per move, from an angle where the form is visible.
- Right vs wrong form side by side, same angle, wrong side clearly marked.
- Never speed up a demonstration rep (it misleads the tempo); speed up only transitions and setup.

**Transition grammar.** Cuts on the beat, whip between exercises, flash on the finisher. No dissolves.

**Music and sound.** BPM-matched bed ~-16 dB (cut on `downbeats`), ducked under the coach. SFX medium (~12/min):
`countdown-beep` before a work interval, `ding` at rest, `whoosh-short` between moves.

**Colour.** `punchy` or `gaming-vivid` for energy, `high-key` for yoga/wellness. Keep skin natural.

**Captions.** Word-pop 1-3 words, uppercase, <= 17 cps; move names and cues as `tile`s, not captions.

**What the client judges.** Clear form, timer accuracy, energy.

**Common mistakes.** Cutting mid-rep; timers that don't match the real interval; text over the body; music that
fights the coach; a wrong-form clip with no clear "wrong" mark; health claims.

## Make the edit

```bash
# moves in order with beat cuts (clips without speech)
python CORE/scripts/beats.py track.wav --out fv/beats.json
python CORE/scripts/timeline.py auto moves/ --work fv --mode montage --music track.wav --duration 45 --format 9:16 --beats-per-shot 4 --dry-run
#   edit fv/timeline_spec.json: hook rep first, moves in plan order, "freeze": [{"at": 2.1, "dur": 0.6}] on a form point
python CORE/scripts/run.py - --timeline fv/timeline_spec.json --style SKILLS/countdown-list --genre fitness-video --format 9:16 --no-cut --work fv --stop-after plan
python CORE/scripts/render.py fv/plan.json --frames 1,8,18,28,40
python CORE/scripts/render.py fv/plan.json
python CORE/scripts/finish.py fv/plan.json --platform reels
```

Coach talking to camera: `python CORE/scripts/run.py coach.mp4 --style SKILLS/bold-bounce --genre fitness-video --format 9:16 --smart-cuts --retakes --music track.wav --broll moves/ --work fv2 --stop-after broll`.
Follow-along session: `--format 16:9 --no-cut`, one clip per move at real length, timers matched to the plan.

## Refine the plan

- **Move cards:** `{"type": "tile", "text": "Reverse lunge x 12", "start": 4.0, "end": 9.5, "in": "pop", "y": 300}`.
- **Interval timer:** `{"type": "timer", "from": 40, "label": "work", "warnAt": 5, "start": 10, "end": 50, "w": 300, "h": 300}`
  (`from` = the real seconds; the element's window must be exactly that long).
- **Rep counter:** `{"type": "counter", "from": 0, "to": 12, "label": "reps", "countDur": 9.5, "start": 4, "end": 14}`
  timed to the real reps; or `checklist` items at each rep. Check make_plan's auto counters for junk.
- **Right vs wrong:** `{"type": "split", "layout": "h", "panes": [{"clip": "right", "label": "Right"}, {"clip": "wrong", "label": "Wrong"}]}`
  with both clips declared in `"clips": [{"id": "right", "src": "squat_good.mp4"}, {"id": "wrong", "src": "squat_bad.mp4"}]`;
  add a `scribble` `cross` on the wrong side.
- **Form cue:** `{"type": "callout", "point": [540, 1180], "x": 760, "y": 520, "title": "Knee over toes"}`.
- **Beat sync:** `"beats"` from `fv/beats.json` in the plan, `"pulseOn": "downbeats"` on the tile.
- **Captions:** delete the skin's `captions` element for music-only assemblies (and clear `words`).
- **Audio:** music-only: `"audio": {"platform": "reels", "voice": false}`; with coach voice:
  `"music": {"src": "track.wav", "under": 14, "duck": "speech-aware", "fitTo": "beats"}`.
- **SFX:** `{"t": 9.4, "kind": "countdown-beep", "gain": 0.4}` (3.7 s long: start it 3.7 s before work begins).
- **Colour:** `"color": {"look": "punchy", "intensity": 0.7}` (yoga: `high-key`).
- **Footage clean-up (video, before the spec):** handheld follow shots, dim gyms and fluorescent tubes: `python CORE/scripts/prep.py move04.mp4 --work fix/move04 --denoise light --deflicker`, then use `fix/move04/source.mp4` in the spec. `--stabilize` = vidstab (crops ~6% at the edges), `--denoise light|strong` = video noise, `--deflicker` = mains-light flicker. Only on clips that need it. Coach talking-head run: add `--deflicker` / `--denoise light` to `run.py` directly.

## Deliver

```bash
python CORE/scripts/deliver.py fv/plan.json --to reels,tiktok,shorts,facebook --out-dir fv/deliver
python CORE/scripts/qc.py fv/deliver/final_reels.mp4 --plan fv/plan.json --platform reels --strict
```

Follow-along: `--to youtube`. Hand over a clean (no captions) version and the cover still.

## Check before delivering

- Every timer and rep count matches the workout plan; no move cut mid-rep.
- Form visible in every demo; wrong-form shots clearly marked; no medical claims.
- `qc.py`: photosensitivity passes (flashes on the finisher can trip it), safe zones clear, -14 LUFS.

## Example requests

- "Make a 45-second leg workout reel from these clips with names and reps on screen."
- "Add a 40/20 interval timer to my follow-along HIIT video."
- "Show right vs wrong squat form side by side."
