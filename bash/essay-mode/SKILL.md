---
name: essay-mode
description: "Essay Mode video-editing style for Claude: Video-essay explainer: paper textures, highlighter marks, serif headings, a chart or card every 8-10 s. Use for 16:9 explainers, analysis, history, news breakdowns, 'why X happened' videos. Turns a raw clip into a finished 16:9 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Essay Mode

Video-essay explainer: paper textures, highlighter marks, serif headings, a chart or card every 8-10 s.

- **Best for:** 16:9 explainers, analysis, history, news breakdowns, 'why X happened' videos
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-essay-mode --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-essay-mode/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-essay-mode/plan.json
python CORE/scripts/finish.py edit-essay-mode/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Cream paper cards with a serif heading and a yellow highlighter swipe. Charts are flat and labelled.
- One visual every 8-10 s: a paper card for each key idea, a counter or bar chart for each number, an image card for each place or person.
- Small lowercase captions at the bottom, optional. Film grade with grain.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Break the transcript into 3-6 sections; add a `titlecard` (class `paper-title`) at each section start.
- For each number, use `bars` when comparing things, `counter` for a single figure.
- For places, people or events, ask the user for images and add `card` elements with `image` and a one-line caption.
- Add `scribble` underlines or circles on cards to point at the key part.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Make this an essay-style explainer with charts."
- "Vox-style edit for my 8-minute video."
- "Add a chart every time I say a number."
