---
name: split-proof
description: "Split Proof video-editing style for Claude: Speaker in the bottom half, proof in the top half: a new card, number, image or clip for every claim. Use for claims that need evidence: results, reviews, comparisons, news reactions, tutorials. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Split Proof

Speaker in the bottom half, proof in the top half: a new card, number, image or clip for every claim.

- **Best for:** claims that need evidence: results, reviews, comparisons, news reactions, tutorials
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-split-proof --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-split-proof/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-split-proof/plan.json
python CORE/scripts/finish.py edit-split-proof/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Top half = the visual, swapping every 4-6 s. Bottom half = the speaker. Captions sit on the seam in a dark pill.
- Every claim gets proof: a screenshot (`image`), a clip, a counter for numbers, or a card with the claim in 3-6 words.
- Dark dotted background behind the top half so cards pop.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Ask the user for screenshots or clips that prove their claims. Add each as an `image` or `clip` element in the top half: x=W/2, y=H*0.25, w=W*0.9, h=H*0.42.
- Without proof media, use `tile` cards with the claim in 3-6 words, or `counter` / `bars` for numbers.
- Never leave the top half empty for more than 2 s.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Split-proof this, I'll send screenshots of my results."
- "Me at the bottom, proof at the top for every point."
- "Turn my reaction video into a split screen."
