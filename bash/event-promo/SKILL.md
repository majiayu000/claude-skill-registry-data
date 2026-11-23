---
name: event-promo
description: "Event Promo video style for Claude: Announcement promo: event name in kinetic type, date and place chips, countdown-style energy, ticket CTA. Use for events, webinars, launches, sales, workshops, live streams. Builds a finished 9:16 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Event Promo

Announcement promo: event name in kinetic type, date and place chips, countdown-style energy, ticket CTA.

- **Best for:** events, webinars, launches, sales, workshops, live streams
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
python CORE/scripts/run.py - --style STYLE --work edit-event-promo --stop-after plan \
    --no-source --title "EVENT NAME" --cta "Register now" --duration 10
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-event-promo/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-event-promo/plan.json
python CORE/scripts/finish.py edit-event-promo/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Name slams in letter by letter, then date chip, place chip, then one line on why to come, then CTA.
- Each beat 1-1.5 s. Riser into the name, boom on the date.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Pass `--no-source --title "EVENT NAME" --cta "Register now" --duration 10`.
- Add `chip` elements (class `ep-chip`) for date, time, place and price exactly as the user gives them, staggered from ~2.5 s.
- With a speaker clip instead, run with a source and keep the chips.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Event promo for my webinar on Saturday 7 pm."
- "Announce my workshop with kinetic text."
- "10-second hype video for our sale."
