---
name: logo-sting
description: "Logo Sting video style for Claude: A 3-6 second logo reveal with light rays, a ring burst and the brand name typing in underneath. Use for channel intros and outros, brand idents, video endings, app splash animations. Builds a finished 16:9 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Logo Sting

A 3-6 second logo reveal with light rays, a ring burst and the brand name typing in underneath.

- **Best for:** channel intros and outros, brand idents, video endings, app splash animations
- **Category:** Product / app promo
- **Default format:** 16:9 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
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
python CORE/scripts/run.py - --style STYLE --work edit-logo-sting --stop-after plan \
    --no-source --logo logo.png --title "Brand Name" --duration 5
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-logo-sting/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-logo-sting/plan.json
python CORE/scripts/finish.py edit-logo-sting/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Logo zooms in from small with a ring shock-wave, rays turn slowly behind it, the name types in below.
- Under 6 s. Brand colours from the logo. Boom on the reveal, ding on the name.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Pass `--no-source --logo logo.png --title "Brand Name" --duration 5` (input `-`).
- Set `--c-accent`/`--c-accent2` in `theme.vars` to the brand colours (sample them from the logo).
- Make 2-3 mood variants (dark, light, colour) if the user wants options; render each to its own file.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Make a logo sting from my logo."
- "5-second intro animation for my channel."
- "Animate my logo, gold on cream."
