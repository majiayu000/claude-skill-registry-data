---
name: chapter-pro
description: "Chapter Pro video-editing style for Claude: Long-form YouTube polish: chapter title cards, lower thirds, subtle captions, list cards and an end screen. Use for long YouTube videos, vlogs, courses, reviews, interviews (5-60 min). Turns a raw clip into a finished 16:9 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Chapter Pro

Long-form YouTube polish: chapter title cards, lower thirds, subtle captions, list cards and an end screen.

- **Best for:** long YouTube videos, vlogs, courses, reviews, interviews (5-60 min)
- **Category:** YouTube explainer
- **Default format:** 16:9 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-chapter-pro --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-chapter-pro/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-chapter-pro/plan.json
python CORE/scripts/finish.py edit-chapter-pro/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Chapter card every major topic change (2.5 s, then cut back).
- Captions small and quiet at the bottom. Lower third for the host in the first 10 s.
- Last 10 s: end screen with subscribe chip and space for YouTube end cards.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Read the transcript and split it into 4-10 chapters; add a `titlecard` (kicker 'Chapter N', title 2-5 words) at each start.
- Also write `chapters.txt` with YouTube timestamps (0:00 Intro, ...) for the description and give it to the user.
- Add a `lowerthird` with the host's name at ~3 s.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Polish my YouTube video with chapters."
- "Add chapter cards and give me timestamps for the description."
- "Make my 20-minute video look professional."
