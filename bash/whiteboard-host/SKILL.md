---
name: whiteboard-host
description: "Whiteboard Host video-editing style for Claude: Teacher layout: speaker in a panel on the left, notes appear in marker handwriting on a paper board on the right. Use for lessons, courses, coaching, exam prep, science and maths explainers. Turns a raw clip into a finished 16:9 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Whiteboard Host

Teacher layout: speaker in a panel on the left, notes appear in marker handwriting on a paper board on the right.

- **Best for:** lessons, courses, coaching, exam prep, science and maths explainers
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-whiteboard-host --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-whiteboard-host/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-whiteboard-host/plan.json
python CORE/scripts/finish.py edit-whiteboard-host/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- The board fills up as the speaker talks: key words in marker, underlined, numbered points.
- Speaker panel stays left; board on the right never has more than 4 lines.
- Clear the board at each new topic (end all notes at the same time).

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Rewrite auto notes into short board lines (2-5 words). Place them down the board: y = H*0.22, 0.38, 0.54, 0.70; x = W*0.72; `anchor: left` with x=W*0.5 for left aligned.
- Add `scribble` underlines under the most important line, and `circle` around answers.
- Use `counter` with class `wb-num` for numbers.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Whiteboard edit for my physics lesson."
- "Put my notes on a board next to me as I explain."
- "Teacher style video for my course."
