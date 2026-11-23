---
name: glow-cutout
description: "Glow Cutout video-editing style for Claude: You, cut out with a soft golden glow, over a blurred and darkened copy of your own shot, with a gold-accent title and boxed karaoke captions. Use for interviews, podcasts clips, opinions, explainers and premium talking-head reels. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Glow Cutout

You, cut out with a soft golden glow, over a blurred and darkened copy of your own shot, with a gold-accent title and boxed karaoke captions.

- **Best for:** interviews, podcasts clips, opinions, explainers and premium talking-head reels
- **Category:** Talking-head reel
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Background replaced / cut-out:** yes (uses the person matte: `python CORE/scripts/matte.py --work WORK --input WORK/cut.mp4 --out WORK/matte.mp4` if `run.py` did not make it)

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-glow-cutout --stop-after plan
# run.py applies the skin's scene recipe; after editing words or the title in plan.json, re-run it:
python CORE/scripts/sequence.py edit-glow-cutout/plan.json --recipe aurora
# refine edit-glow-cutout/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-glow-cutout/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-glow-cutout/plan.json
python CORE/scripts/finish.py edit-glow-cutout/plan.json --platform reels
python CORE/scripts/qc.py edit-glow-cutout/final.mp4 --plan edit-glow-cutout/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

- The background is the same shot, heavily blurred and darkened; you sit sharp on top with a warm gold rim glow.
- A short title stays at the top: sans-serif with one word in gold italic serif (wrap it: `<i>word</i>`, element `html: true`).
- Captions: 2-3 words in a dark pill, uppercase, the spoken word turns gold.
- Key words pop as small glass cards top-left. Film grade, light grain.

## The scenes (aurora recipe)

`sequence.py PLAN --recipe aurora` turns the draft into alternating scenes, one per phrase (sentence, danda, or comma + pause):

- **Speaker scene** (phrase 1, 3, ...): you with the gold glow over the blurred shot, the caption chip (spoken word gold,
  the phrase's key word in gold italic serif) and a small dark-glass card top-left: tiny gold `01 / 04` + the key word,
  landing on that word.
- **Quote scene** (phrase 2, 4, ...): you are hidden; the same footage, blurred and darkened, fills the frame with a warm glow,
  the phrase as one big line (key word in gold italic serif) and a tiny gold `02 / 04` kicker. A phrase shorter than 1.2 s stays on you.
- The title stays on top the whole time. A plain title gets its key word in gold italic; write your own `<i>word</i>` to choose it.
- Scene changes get a soft blur and a whoosh. The key word is the longest of the last three words, skipping a refrain
  (a word heard in 2+ phrases). Fix the words in `plan.json` first if it picked the wrong one, then re-run the recipe.
- Re-running replaces everything the recipe wrote (`"_seq": true` elements, sfx, cutaways, blurs); hand-added items stay.
  It replaces the skin's auto key-word cards (`gc-card`) and captions with its own.

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Replace weak auto-picked key words and headlines with the words that carry the meaning.
- Set the title: `--title "Ten <i>years</i> of work"` style, then in plan.json set `"html": true` on that element.
- For a pull quote, add `{"type":"quote","text":"...","start":..,"end":..,"className":"gc-quote"}` and raise `speaker.backdropDim` to 0.7 for that moment if needed.
- Glow colour/size: `speaker.glow` `{color, size, strength}`. Blur/dim: `speaker.backdropBlur`, `speaker.backdropDim`.
- Framing: a tight selfie (head touching the top, shoulders filling the width) works best with `speaker.personDrop` 0.1-0.14 (cut-out slides down, top edge fades); a shot with headroom and space at the sides can use `speaker.personScale` 0.8-0.9 instead. Check a still.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Make it premium, me glowing over a blurred background."
- "Podcast clip with gold captions and a title on top."
