---
name: dual-subs
description: "Dual Subs video-editing style for Claude: Two-language captions: the original word-by-word on top, a translated line underneath, both readable. Use for reaching a second audience: Hindi + English, Spanish + English, any pair. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Dual Subs

Two-language captions: the original word-by-word on top, a translated line underneath, both readable.

- **Best for:** reaching a second audience: Hindi + English, Spanish + English, any pair
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-dual-subs --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-dual-subs/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-dual-subs/plan.json
python CORE/scripts/finish.py edit-dual-subs/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Original captions karaoke-style at 66% height; translation in a smaller, lighter line under it.
- Translation follows sentences, not words, so it reads naturally. Never machine-literal: translate the meaning.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- make_plan puts each sentence's original text into the second caption track (`lines`). Replace every `lines[].text` with your translation into the target language, keeping start and end.
- For Hindi use Devanagari unless the user wants Hinglish (Roman script). Add a Noto Sans font for the script: e.g. add `Noto+Sans+Devanagari` to `theme.fontsUrl`.
- Optionally swap: translation as the main track for a foreign audience.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Add Hindi subtitles under my English captions."
- "Dual subs English and Spanish."
- "Make Hinglish + English captions."
