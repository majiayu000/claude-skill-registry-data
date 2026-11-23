---
name: kinetic-launch
description: "Kinetic Launch video style for Claude: Type-only motion piece: bold words slam in one after another in sync with the beat or voiceover. Use for launch teasers, announcements, quotes, manifesto videos, intros, ads without footage. Builds a finished 9:16 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Kinetic Launch

Type-only motion piece: bold words slam in one after another in sync with the beat or voiceover.

- **Best for:** launch teasers, announcements, quotes, manifesto videos, intros, ads without footage
- **Category:** Product / app promo
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** no
- **Text behind the speaker:** no

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py - --style STYLE --work edit-kinetic-launch --stop-after plan \
    --no-source --title "Your final line" --cta "Out now" --duration 8
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-kinetic-launch/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-kinetic-launch/plan.json
python CORE/scripts/finish.py edit-kinetic-launch/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- One idea per beat: 1-4 words on screen, each held 0.6-1.2 s. Huge type, high contrast, one accent colour.
- Vary scale and motion: slam (stamp), rise, wipe. Hold the final line longer.
- Use music; time each word to a beat. Loop cleanly if asked (first frame = last frame).

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- With a voiceover, run normally: each sentence becomes a kinetic headline.
- Without one, write the script into a sequence of `text` elements with `split: "words"` or `"chars"`, each 0.6-1.2 s, centred, `fit: true`, alternating `className` `kl-a` / `kl-b`.
- Use `--no-source --title "Final line" --cta "..."` and set `--duration`.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Kinetic type promo for my launch: 'Trading. Rebuilt. For you.'"
- "Make a 10-second type-only teaser, loopable."
- "Animate my voiceover as big words."
