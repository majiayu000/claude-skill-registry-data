---
name: glass-ribbon
description: "Glass Ribbon video-editing style for Claude: A glowing violet glass ribbon flows behind you (and across you) in a deep purple scene with soft light orbs; glass cards pop on key words and captions mix clean sans with italic serif. Use for tech, AI, product, coaching and premium short talking-head reels. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Glass Ribbon

A glowing violet glass ribbon flows behind you (and across you) in a deep purple scene with soft light orbs; glass cards pop on key words and captions mix clean sans with italic serif.

- **Best for:** tech, AI, product, coaching and premium short talking-head reels
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-glass-ribbon --stop-after plan
python CORE/scripts/sequence.py edit-glass-ribbon/plan.json --recipe ribbon   # the scene sequence (do not skip)
# refine edit-glass-ribbon/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-glass-ribbon/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-glass-ribbon/plan.json
python CORE/scripts/finish.py edit-glass-ribbon/plan.json --platform reels
python CORE/scripts/qc.py edit-glass-ribbon/final.mp4 --plan edit-glass-ribbon/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

The edit changes scene on every phrase (`sequence.py --recipe ribbon`):

- **Person scene:** you, cut out with a violet rim glow, on a dark dotted stage with a glossy ribbon wrapping behind you. A frosted card top-left (two words + the key word in italic serif) ticks off the words as you say them, glass icon buttons, a cream pill with the phrase. On the last phrase the payoff line lands in big italic serif.
- **Type scene (no person):** lighter violet with stars, big soft orbs and a glowing thread. The previous and current phrase stack as glass note cards, the phrase appears as big sans + italic serif type, and a search bar types the next phrase.
- Every scene change gets a soft full-frame blur (`softCuts`) and a whoosh; alternate person scenes punch in. Hindi/Devanagari falls back to Mukta and Rozha One automatically.
- `--split 0.55` sets where in each phrase the type scene takes over. Re-running `sequence.py` replaces only what it wrote.

- Your real background is replaced by a deep violet radial scene with drifting bokeh orbs.
- A thick glowing ribbon waves behind you; a thin one crosses in front at chest height.
- Captions: clean white sans, key words become large italic serif. Key words also pop as frosted glass cards.
- Optional typed search bar (`searchbar` element) on a question.

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Replace weak auto-picked key words and headlines with the words that carry the meaning.
- Move the front ribbon (`gr-ribbon-front`) so it never crosses the face; set its `y` below the chin.
- Add a `searchbar` element for a spoken question: `{"type":"searchbar","query":"...","className":"gr-search"}`.
- Change the palette in `theme.vars` (`--c-accent`, `--c-accent2`) and the ribbon `color`/`color2`.
- Framing: a tight selfie (head touching the top, shoulders filling the width) works best with `speaker.personDrop` 0.1-0.14 (cut-out slides down, top edge fades); a shot with headroom and space at the sides can use `speaker.personScale` 0.8-0.9 instead. Check a still.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Purple glass ribbon reel like a premium tech creator."
- "Replace my background with something futuristic."
