---
name: loop-ambient
description: "Loop Ambient video-editing style for Claude: Seamless looping visual: drifting gradient, morphing blob and moving bars behind a short quote or track title. Use for music posts, quotes, podcast audiograms, livestream backgrounds, website hero videos. Turns a raw clip into a finished 1:1 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Loop Ambient

Seamless looping visual: drifting gradient, morphing blob and moving bars behind a short quote or track title.

- **Best for:** music posts, quotes, podcast audiograms, livestream backgrounds, website hero videos
- **Category:** Product / app promo
- **Default format:** 1:1 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-loop-ambient --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-loop-ambient/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-loop-ambient/plan.json
python CORE/scripts/finish.py edit-loop-ambient/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Everything moves slowly and returns to its start so the video loops without a jump.
- One short line of text (or a track title and artist). Equalizer bars react while someone speaks.
- With audio, captions appear; without it, text holds.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Pass `--no-source --title "line" --duration 12` for a silent loop; add `music.src` for a track.
- For an audiogram of a podcast clip, run with the clip as input and set `speaker.mode` to `none` in the plan (keeps the audio and captions, hides the video).
- Check the loop: frame 0 and the last frame must look the same; keep durations that are multiples of 6 s.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Make a looping background for this quote."
- "Audiogram for my podcast clip."
- "Ambient loop visual for my track."
