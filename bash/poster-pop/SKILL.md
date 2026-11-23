---
name: poster-pop
description: "Poster Pop video-editing style for Claude: Retro collage edit: the background behind you swaps to a new bold poster pattern (stripes, checkerboard, grid, sunburst, colour field) on every sentence, with a chunky slab headline, full-screen pattern interstitials and warm film grain. Use for stories, opinions, fun explainers, music and nostalgic or playful personal-brand reels. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Poster Pop

Retro collage edit: the background behind you swaps to a new bold poster pattern (stripes, checkerboard, grid, sunburst, colour field) on every sentence, with a chunky slab headline, full-screen pattern interstitials and warm film grain.

- **Best for:** stories, opinions, fun explainers, music and nostalgic or playful personal-brand reels
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-poster-pop --stop-after plan
python CORE/scripts/sequence.py edit-poster-pop/plan.json --recipe retro   # the scene sequence (do not skip)
# refine edit-poster-pop/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-poster-pop/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-poster-pop/plan.json
python CORE/scripts/finish.py edit-poster-pop/plan.json --platform reels
python CORE/scripts/qc.py edit-poster-pop/final.mp4 --plan edit-poster-pop/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

The edit changes scene on every phrase (`sequence.py --recipe retro`), with hard cuts:

- **Speaker scenes:** you, cut out, on a new poster backdrop each phrase, cycled: solid royal blue, green graph paper, black, cream paper, red glow, red/cream checkerboard, diagonal stripes. The phrase's key word lands as a chunky slab headline at the top, its foot tucked behind your hair (cream, orange or red by backdrop); a small italic tag on a cream label sits under it; small uppercase captions on a dark strip run at the bottom. Alternate scenes punch in a little.
- **Interstitials (no speaker):** every 2-3 phrases the end of the phrase, from its key word on, goes full screen: a loud pattern (stripes, sunburst, checkerboard) with the words being said stacked big on a cream poster panel (key word red) and the words said just before as an italic kicker. Never on the last phrase, so the edit ends on you.
- Every scene change gets a quick cream flash and a projector click; an interstitial lands with an impact. Warm high-contrast Kodachrome grade, heavy grain and a vignette (`finish`).
- Key word = the longest of the phrase's last three words, skipping refrains heard in every line (e.g. "बरगी"). Hindi/Devanagari falls back to Rozha One (headlines), Tiro Devanagari Hindi (italic) and Mukta (captions).
- Re-running `sequence.py` replaces only what it wrote (and drops the skin's per-sentence `pp-bg`/`pp-head` draft and captions).

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Replace weak auto-picked key words and headlines with the words that carry the meaning.
- After `sequence.py`: fix each scene's headline word (`pp-head` headline elements); keep it 1-2 words.
- Rewrite each speaker scene's italic tag (`pp-tag`, default "— 01 / 04 —") into a short line of your own, e.g. the English meaning of a Hindi line.
- Re-order the backdrops by changing a `background` element's `className` (`pp-blue pp-grid pp-black pp-paper pp-red pp-checker pp-stripes pp-sun`).
- An interstitial is the `front` `background` + `pp-tag` kicker + `pp-big` headline over the same window; keep it at least 0.8 s.
- Framing: a tight selfie (head touching the top, shoulders filling the width) works best with `speaker.personDrop` 0.1-0.14 (cut-out slides down, top edge fades); a shot with headroom and space at the sides can use `speaker.personScale` 0.8-0.9 instead. Check a still.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Retro poster edit, new background every line."
- "80s collage look with stripes and checkerboards behind me."
- "Retro edit with a pattern break every few lines, like a poster zine."
