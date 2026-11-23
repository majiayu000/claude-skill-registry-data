---
name: before-after
description: "Before After video-editing style for Claude: Transformation edit: a wipe slider reveals the 'after' over the 'before', with labels and a ding on the reveal. Use for fitness, design, renovation, editing, skin care, website redesigns, results. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Before After

Transformation edit: a wipe slider reveals the 'after' over the 'before', with labels and a ding on the reveal.

- **Best for:** fitness, design, renovation, editing, skin care, website redesigns, results
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-before-after --stop-after plan --image before.jpg --image2 after.jpg
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-before-after/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-before-after/plan.json
python CORE/scripts/finish.py edit-before-after/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- The comparison is the hero: large compare card in the top half, the speaker below or full frame behind.
- The wipe starts after a 0.8 s pause so the 'before' registers. Ding on the reveal.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Ask for before and after images (same framing). Add a `compare` element: `before`, `after`, x=W/2, y=H*0.3, w=W*0.9, h=H*0.42, start at the moment the speaker mentions the result.
- For video before/after, render each as an image sequence and use two `clip` elements side by side instead.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Before-after edit with my two photos."
- "Show my transformation with a slider."
- "Reveal the redesign with a wipe."
