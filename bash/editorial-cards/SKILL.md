---
name: editorial-cards
description: "Editorial Cards video-editing style for Claude: Editorial explainer on a warm paper page: your footage sits in a tilted rounded card that moves to a new spot every sentence, big black words land as you say them, and key words get hand-drawn circles and underlines. Use for explainers, essays, interviews, education, opinions and thought-leadership clips. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Editorial Cards

Editorial explainer on a warm paper page: your footage sits in a tilted rounded card that moves to a new spot every sentence, big black words land as you say them, and key words get hand-drawn circles and underlines.

- **Best for:** explainers, essays, interviews, education, opinions and thought-leadership clips
- **Category:** Explainer
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Person cut-out:** not needed

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-editorial-cards --stop-after plan
# run.py already applies the scene recipe; re-run it after fixing words or key words:
python CORE/scripts/sequence.py edit-editorial-cards/plan.json --recipe explainer
# refine edit-editorial-cards/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-editorial-cards/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-editorial-cards/plan.json
python CORE/scripts/finish.py edit-editorial-cards/plan.json --platform reels
python CORE/scripts/qc.py edit-editorial-cards/final.mp4 --plan edit-editorial-cards/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

Cream paper page, calm soft cuts, one scene per phrase (the `explainer` recipe in `sequence.py`), cycling:

1. **Card low** - small grey kicker (`01 / 04`), big black headline whose words write on as they are spoken, the key
   word in coral italic serif with a hand-drawn underline; your footage below in a tilted, white-framed rounded card.
2. **Type only** - no footage: bigger type mid-page, a coral circle draws round the key word as it is said (a phrase
   shorter than 1.2 s stays on a card instead).
3. **Card + blank** - the card top-right; the phrase below in light grey, darkening as it is read, the key word a
   `_ _ _` blank that is written in coral when it is said.
4. **Card + highlighter** - headline on top, a yellow highlighter swipes the key word, the card lower-left with a coral
   arrow and a punch-in on the key word.

Hindi / Haryanvi set in Mukta (bold sans) and Tiro Devanagari Hindi (true italic serif). No colour look, light grain.

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Key word per phrase: the recipe takes the longest of the last three words, skipping refrains (words heard in 2+
  phrases). To change one, edit that scene's captions `keywords` (one word). Kicker text: the `ed-kick` elements.
- Card positions live in `speaker.layouts` (`rect` px, `radius`, `rot` degrees, `start`/`end`); a type scene's card is
  parked off-frame (x beyond the width). Re-running the recipe rewrites the layouts and everything marked `_seq`.
- Hand-drawn marks are `scribble` elements (`kind` circle, underline, arrow, box, check, highlight); move them to the word they mark.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Editorial explainer with my clip in cards and big words."
- "Make it look like a magazine page with hand-drawn circles."
