---
name: testimonial-card
description: "Testimonial Card video style for Claude: A real customer quote shown as a clean card: avatar, stars, the quote typing in word by word, name and role. Use for social proof posts, client reviews, case-study teasers (real reviews only). Builds a finished 4:5 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Testimonial Card

A real customer quote shown as a clean card: avatar, stars, the quote typing in word by word, name and role.

- **Best for:** social proof posts, client reviews, case-study teasers (real reviews only)
- **Category:** Product / app promo
- **Default format:** 4:5 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
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
python CORE/scripts/run.py - --style STYLE --work edit-testimonial-card --stop-after plan \
    --no-source --title "the exact review" --cta "Name, Role" --image avatar.jpg --duration 8
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-testimonial-card/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-testimonial-card/plan.json
python CORE/scripts/finish.py edit-testimonial-card/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- One card, centred, on a soft gradient. Stars pop first, then the quote words rise in, then the name.
- 6-10 s. Use the client's real words, unchanged, and only with their permission.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Pass `--no-source --title "the exact quote" --cta "Name, Role" --image avatar.jpg --duration 8`.
- Never write or edit a review for the user: ask for the real one. If they want an example, label it 'Sample review'.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Make a testimonial video from this client review."
- "Turn my 5-star review into a reel."
- "Social proof card for my agency."
