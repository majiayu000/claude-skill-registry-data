---
name: grid-stage
description: "Grid Stage video-editing style for Claude: Dark studio stage: your background becomes a black grid with a soft spotlight and a slow-turning disc, one giant word sits behind your head each sentence, small uppercase captions and glass pills. Use for podcasts, interviews, founder and creator clips, business and tech talking heads. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Grid Stage

Dark studio stage: your background becomes a black grid with a soft spotlight and a slow-turning disc, one giant word sits behind your head each sentence, small uppercase captions and glass pills.

- **Best for:** podcasts, interviews, founder and creator clips, business and tech talking heads
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-grid-stage --stop-after plan
python CORE/scripts/sequence.py edit-grid-stage/plan.json --recipe layercut   # the scene sequence (do not skip)
# refine edit-grid-stage/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-grid-stage/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-grid-stage/plan.json
python CORE/scripts/finish.py edit-grid-stage/plan.json --platform reels
python CORE/scripts/qc.py edit-grid-stage/final.mp4 --plan edit-grid-stage/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

The edit changes scene on the phrases (`sequence.py --recipe layercut`):

- **Speaker scene:** you, cut out on the dark grid stage with a big dark vinyl disc turning behind you. One huge silver condensed word per scene sits behind your head (solid and outline alternate; your head covers its lower edge). Small uppercase captions on a dark chip under your chin. White audio-level bars (odd phrases) or a thin glowing wave line (even phrases) run behind you.
- **Panel scene (no speaker):** a 3D-tilted dark app panel flies in over a dotted stage: the phrase's key word is its title, the other words are slider and toggle rows.
- **Title-card scene (no speaker):** diagonal light beams, a small kicker with a glowing lime dot (the words before the key word), the key word in huge silver type, and the words after it appearing as they are said.
- The first and last phrases stay on you. A middle phrase opens on you and cuts to a panel (2nd, 4th...) or a title card (3rd, 5th...) exactly on its key word; a phrase too short for that stays on you. The last phrase ends with a glass pill (lime toggle + an italic script word) in the caption slot.
- Key word = the longest of the phrase's last three words, skipping refrains (a word heard in 2+ phrases). Scene changes get a soft blur (`softCuts`) and a whoosh. Re-running `sequence.py` replaces only what it wrote (and the skin's auto headlines, captions and key-word pills).
- Hindi/Devanagari falls back to Teko (condensed), Mukta and Rozha One automatically.

Without the recipe (draft plan only):

- Your real background is replaced by a near-black grid stage with a spotlight and a large slowly turning disc behind your head.
- One giant condensed word per sentence behind your head (silver, alternating with outline).
- Small uppercase captions under your chin; key words pop as glass pills with a lime dot.
- For chapter breaks, add a full-screen title card: a `background` (class `gs-card`) on the front layer plus a `headline` with `fx: gradientSweep`.

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Replace weak auto-picked key words and headlines with the words that carry the meaning.
- Set every headline `y` so the word sits at forehead height and the head covers its middle (recipe: `lc-head`, y 0.15 H).
- Recipe captions and the pill sit at 0.83 H, under the chin of a tight selfie at `personDrop` 0.14. With `personScale` or a lower `personDrop`, check a still and move the `lc-cap` / `lc-pill` `y` up so they stay under the chin.
- Chapter card example: `{"type":"background","layer":"front","className":"gs-card","start":8,"end":9.2}` + `{"type":"headline","text":"COMPOUNDING","className":"gs-cardtitle","fx":{"name":"gradientSweep","color":"#fff"},"start":8,"end":9.2}`.
- Put a `transition` (`whip-blur` or `zoom-blur`) on each chapter card.
- Framing: a tight selfie (head touching the top, shoulders filling the width) works best with `speaker.personDrop` 0.1-0.14 (cut-out slides down, top edge fades); a shot with headroom and space at the sides can use `speaker.personScale` 0.8-0.9 instead. Check a still.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Dark studio look with a big word behind my head."
- "Podcast clip on a black grid with title cards between sections."
