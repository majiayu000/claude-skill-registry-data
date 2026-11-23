---
name: chaos-stack
description: "Chaos Stack video-editing style for Claude: Sensory-overload 'brainrot' edit: one huge word at a time, snap zooms every second, flashes and emoji bursts. Use for Gen-Z humour, hot takes, fast stories, meme commentary. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Chaos Stack

Sensory-overload 'brainrot' edit: one huge word at a time, snap zooms every second, flashes and emoji bursts.

- **Best for:** Gen-Z humour, hot takes, fast stories, meme commentary
- **Category:** Talking-head reel
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Text behind the speaker:** no

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-chaos-stack --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-chaos-stack/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-chaos-stack/plan.json
python CORE/scripts/finish.py edit-chaos-stack/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- One giant word at a time in the centre, bouncing in.
- Snap zoom (+25%) every 1-1.5 s, white flash on cuts, emoji bursts on key words.
- Optional stacked layout: speaker top half, gameplay or satisfying clip bottom half.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Stacked layout: set `speaker` to `{"mode":"panel","rect":[0,0,1080,960]}` and add a `clip` element (bottom half, x=540, y=1440, w=1080, h=960) with gameplay from the user.
- Map key words to fitting emoji in `burst.chars`.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Brainrot edit this."
- "Make it chaotic, fast and loud."
- "Chaos stack with Subway Surfers style gameplay under me."
