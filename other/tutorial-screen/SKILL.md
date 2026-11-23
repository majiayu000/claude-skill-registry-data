---
name: tutorial-screen
description: "Screen-tutorial editor for software how-tos, coding walkthroughs and course demos: promise, prerequisites, numbered steps, recap; cuts the waiting, typing and loading, punches in on the area being clicked, adds step chips, keyboard-shortcut and callout overlays, blurs private data, and delivers a 16:9 video with YouTube chapters and captions. Use when the user says: edit my screen recording, tutorial video, how-to video, coding tutorial, software walkthrough, cut the loading screens, zoom on my cursor, add step numbers, make my Loom look professional. Default skin chapter-pro; any Video Studio skin works."
license: MIT
---

# Tutorial Screen

A screen recording a viewer can follow without pausing: no waiting, the right thing magnified, every step labelled.

- **Best for:** software tutorials, coding walkthroughs, SaaS how-tos, course demos, bug-fix videos
- **Inputs:** a screen recording with your narration (best), or a screen recording + a facecam recorded at the same time; optional final project link
- **Default skin:** `chapter-pro` · alternatives `tutorial-steps` (facecam circle + step chips), `terminal-tech`, `highlighter-study`
- **Formats:** 16:9 1920x1080 master, chapters, `captions.srt`; optional 9:16 tip clips
- **Duration target:** 5-15 min (one task per video); tips 30-60 s; genre preset `tutorial-screen`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre tutorial-screen`.
- The `--genre` preset sets autocut's pause cut (0.45 s) and run.py respects it; pass `--max-gap` only to override.
- Ask what is private on screen (emails, API keys, customer names, tokens). It must be blurred **before** anything is published.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| promise | 0-5 | show the finished result first (5-10 s), then say what you'll build |
| prerequisites | 5-10 | versions, accounts, files needed (a checklist card) |
| numbered steps | 10-90 | one step = one chapter; say it, do it, show the result |
| recap | 90-97 | the steps again in 15 s |
| next / CTA | 97-100 | link, next video |

- **Pacing:** ASL 3-8 s; cut every wait (loading, installs, typing long strings - show a 1 s speed-up or skip to the result). Something changes every 4-6 s: a zoom, a chip, a callout.
- **Cut rules:** never cut away the click that matters; keep the result on screen >= 1 s after each action. Don't cut mid-sentence of an explanation.
- **Zoom:** zoom in when the UI text is small or the action is in one corner (1.6-2.5x on the area), zoom out before the cursor travels across the screen. Smooth 0.4-0.6 s moves, not jumps.
- **Transitions:** cuts; a step-chip change marks a new step. No whooshes on every click.
- **Music/SFX:** quiet bed (28 LU under) or none; soft `click`/`ui-tap` only on the key clicks.
- **Colour:** none - accurate UI colours (`"color": {"auto": false}`).
- **Captions:** sidecar SRT (YouTube) or `clean` preset low on screen; keyboard shortcuts as their own chips.
- **Client judges:** can a viewer follow every step without pausing or hunting for the cursor.
- **Common mistakes:** 4K UI shown full-frame (unreadable), cursor lost, leaked secrets, dead air while something installs, steps not labelled, music louder than the narration.

## Make the edit

**A. Narration recorded with the screen (one file):**

```bash
python CORE/scripts/run.py screen.mp4 --style SKILLS/chapter-pro --genre tutorial-screen \
  --smart-cuts --retakes --no-matte --model small --prompt "product names, commands" --work tut --stop-after plan
```

**B. Screen + separate facecam recorded together:** combine them into one picture-in-picture source first, so every cut removes the same moment from both (otherwise autocut desyncs the face from the screen):

```bash
ffmpeg -i screen.mp4 -i face.mp4 -filter_complex "[1:v]scale=360:-2[f];[0:v]scale=1920:-2[s];[s][f]overlay=W-w-40:H-h-40" \
  -map 1:a -c:v libx264 -crf 18 -c:a aac -shortest tut_src.mp4
python CORE/scripts/run.py tut_src.mp4 --style SKILLS/chapter-pro --genre tutorial-screen --smart-cuts \
  --retakes --model small --work tut --stop-after plan
```

(With `tutorial-steps` instead: `run.py face.mp4 --clip screen.mp4 --no-cut ...` shows the screen full-frame with the face in a circle, but only stays in sync without autocut.)

Then:

```bash
python CORE/scripts/scenes.py tut/cut.mp4 --work tut --threshold 0.15     # big screen changes = step boundaries
python CORE/scripts/editor.py review tut/plan.json --genre tutorial-screen --fix
python CORE/scripts/render.py tut/plan.json --frames 2,20,60,120          # LOOK: UI text readable?
python CORE/scripts/render.py tut/plan.json
python CORE/scripts/finish.py tut/plan.json --platform youtube
```

**Blur private data** with the plan's `blurs` list (box in output pixels, top-left corner; read the position off a
`--frames` still): `"blurs": [{"x": 880, "y": 96, "w": 420, "h": 40, "start": 0, "end": 95.0}]`, or `"pixelate": true`
for a mosaic. It blurs the recording under the graphics, so chips and captions stay sharp. A secret that moves (scrolling,
a zoom) needs one box per time range; the engine has no tracking blur. See `CORE/references/plan-schema.md`.

## Refine the plan

- **Zoom on the action:** `speaker.focusX`/`focusY` set where a zoom aims for the whole video; per-moment zooms are `speaker.zooms` (`{"start": 42.1, "end": 47.0, "scale": 1.8, "cx": 0.78, "cy": 0.08}`: `cx`/`cy` = the clicked spot, 0-1 of the source frame; the engine does not follow the cursor by itself). When different zooms need different areas, put the screen in a `clip` element and animate it with keys: `"keys": {"s": [[0, 1], [0.5, 2.0, "inOut"], [4.5, 2.0], [5, 1, "inOut"]], "tx": [[0, 0], [0.5, -420]], "ty": [[0, 0], [0.5, 260]]}`.
- **Step chips:** `{"type": "chip", "text": "Step 2 · Add the API key", "start": 61.0, "end": 140.0, "x": 50, "y": 60, "anchor": "top-left"}` and top-level `"chapters": [{"start": 0, "title": "Result"}, {"start": 61.0, "title": "Add the API key"}]`.
- **Prerequisites:** `{"type": "checklist", "title": "You need", "items": [{"text": "Node 20", "at": 22.4}, {"text": "A free account", "at": 24.0}]}`.
- **Shortcuts:** `{"type": "tile", "text": "Ctrl + Shift + P", "start": 80.2, "end": 82.4, "x": 960, "y": 960}`.
- **Callouts / pointer:** `{"type": "callout", "point": [1510, 88], "x": 1200, "y": 300, "title": "Deploy button"}`, `{"type": "pointer", "kind": "arrow", "x": 1510, "y": 88, "from": [1300, 400]}`.
- **Code:** `{"type": "codeblock", "title": "app.js", "code": "...", "diff": true}` to restate code the viewer must copy (exact text from the recording).
- **Speed-up the wait:** remove it with `--cut "start-end"` (source seconds) on run.py, or keep 1 s with a `chip` "2 minutes later".
- **Auto elements:** the skin may add counters (labels built from nearby words, e.g. "% faster Follow") and a `subscribe` button that can collide with captions near the end. Fix the label text or delete them.
- **Sound:** `"audio": {"voice": {"denoise": "light", "eq": "clear"}}`, `"sfx": [{"t": 81.0, "kind": "click", "gain": 0.3}]`.
- **Colour:** `"color": {"auto": false}`, `"finish": {"grain": 0, "vignette": false, "sharpen": 0.3}`.

## Deliver

```bash
python CORE/scripts/deliver.py tut/plan.json --to youtube --out-dir tut/deliver
python CORE/scripts/qc.py tut/deliver/final_youtube.mp4 --plan tut/plan.json --platform youtube
```

- Upload `captions.srt`; paste `chapters.txt` (one chapter per step) into the description with the links.
- Tips for Shorts: cut single steps with `retention-reel` (`--reframe` will not help on UI; render a 9:16 plan with the screen in a `clip` element zoomed on the area instead).

## Check before delivering

- Watch every step at 1x: could you follow it without pausing? UI text >= ~24 px tall at 1080p when it matters.
- No secrets anywhere (scrub the contact sheet and the full video; also thumbnails).
- Results stay on screen >= 1 s after each action; no cursor-lost moments.
- Chapters match the steps; `qc.py` passes (-14 LUFS, -1 dBTP).
- Tell the user: seconds removed, steps and chapter times, what was blurred, file paths.

## Example requests

- "Edit my 25-minute screen recording into a clean tutorial, cut all the loading and zoom on the clicks."
- "Coding tutorial: add step numbers, chapters and show my shortcuts on screen."
- "My Loom with facecam - make it look professional and blur my API key."
