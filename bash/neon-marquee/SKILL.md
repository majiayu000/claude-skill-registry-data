---
name: neon-marquee
description: "Neon Marquee video-editing style for Claude: Your real shot cut into wide and tight shots per phrase (close-ups, an extreme close-up on the payoff), a huge glowing electric-blue marquee scrolling sideways at the top, compact caption chips with the key word in a blue italic box, a lime label bar, heavy blur transitions and a dark moody grade. Use for podcast clips, interviews, tech, news and bold opinion reels. Turns a raw talking clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Neon Marquee

Your real shot cut into wide and tight shots per phrase (close-ups, an extreme close-up on the payoff), a huge glowing electric-blue marquee scrolling sideways at the top, compact caption chips with the key word in a blue italic box, a lime label bar, heavy blur transitions and a dark moody grade.

- **Best for:** podcast clips, interviews, tech, news and bold opinion reels
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-neon-marquee --stop-after plan
python CORE/scripts/sequence.py edit-neon-marquee/plan.json --recipe eclipse   # the shot sequence (run.py does this; re-run after editing words)
# refine edit-neon-marquee/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-neon-marquee/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-neon-marquee/plan.json
python CORE/scripts/finish.py edit-neon-marquee/plan.json --platform reels
python CORE/scripts/qc.py edit-neon-marquee/final.mp4 --plan edit-neon-marquee/plan.json
```

Open `contact_sheet.png` and look at it before the full render. Pass `--title "..."` to `run.py` / `make_plan.py` for the title line.

## The look

The edit is cut by `sequence.py --recipe eclipse`: every phrase is one shot, and shots alternate (the last phrase is always tight):

- **Wide shot:** the full frame. The caption chip runs until the key word, then a lime label bar slides in from the left with the key phrase (key word to the end of the phrase, max 4 words).
- **Tight shot:** a close-up with your eye line on the upper third; on the key word it snaps to an extreme close-up (the last phrase holds it to the end) with an impact hit. The caption chip drops below the chin.
- **Every shot:** a giant glowing electric-blue marquee of the phrase's key words scrolls sideways at the top (direction alternates), over a dark top band. Captions: 2-3 white words in a small black chip; the key word sits in a blue box in italic serif.
- Shot changes get a heavy out-of-focus blur (`softCuts`) and a whoosh. Dark moody grade (`finish.grade` "moody") with grain and vignette.
- Key word = the longest of the phrase's last three words, skipping refrains (a word heard in 2+ phrases, like a shayari's "बरगी").
- Hindi/Devanagari falls back to Baloo 2 (marquee, label), Mukta (captions) and Rozha One (key word). Re-running `sequence.py` replaces only what it wrote.
- Punch-ins aim at the face from `track.json` (`python CORE/scripts/track.py analyze WORK/cut.mp4 --work WORK` before `make_plan.py`); without it they zoom on the frame centre.

## Refine the plan

- Read `words.json`, fix mis-heard words (keep their times) and rewrite the hook.
- Replace weak auto-picked key words and headlines with the words that carry the meaning.
- Marquee: the `nm-marq` headlines (`y` height, `keys.tx` speed). For a shot with headroom above the head, set their `"layer": "behind"` so the head eclipses the glow.
- Framing: the `_seq` zooms in `speaker.zooms` (`scale`, `cx`/`cy`); the chip and label `y` in `elements`.
- Use real names/claims for the lime labels only when they are said in the clip.
- Element types and fields: `CORE/references/plan-schema.md`, `CORE/references/motion.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing over the face, safe zones (10-85% of the height, clear of the right 12% in 9:16).
- Overlays land with the spoken word, not after it.
- `qc.py` with 0 FAIL. Tell the user what was cut, the look, and where the file is.

## Example requests

- "Podcast clip with big blue scrolling text behind the guest."
- "Neon headline behind my head, punchy captions."
