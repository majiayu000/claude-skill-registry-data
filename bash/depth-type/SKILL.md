---
name: depth-type
description: "Depth Type video-editing style for Claude: A giant one-word headline sits behind the speaker's head and changes with every sentence. Use for statements, opinions, motivational and personal-brand reels where one word sums up each sentence. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Depth Type

A giant one-word headline sits behind the speaker's head and changes with every sentence.

- **Best for:** statements, opinions, motivational and personal-brand reels where one word sums up each sentence
- **Category:** Talking-head reel
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Text behind the speaker:** yes (uses the person cut-out)

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-depth-type --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-depth-type/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-depth-type/plan.json
python CORE/scripts/finish.py edit-depth-type/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- One word per sentence, condensed display type (Anton), cream and amber alternating, behind the head.
- The word must be readable around the head: set its `y` so it sits at forehead height. Check a still first.
- Small, calm captions low in the frame; spoken word bright, the rest dimmed.
- Film grade with light grain and vignette.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Look at a still (`render.py --preview 1`) and move every headline's `y` to the head's top edge.
- Replace auto headline words with the single word that best sums up each sentence (a verb or a noun, not 'the').
- Needs the person matte. With a busy background, try `matte.py --backend rembg`.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Depth-type edit, big words behind my head."
- "Put one word behind me for each sentence, cinematic."
- "Make it like a poster that moves."
