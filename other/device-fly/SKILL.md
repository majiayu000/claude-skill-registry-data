---
name: device-fly
description: "Device Fly video style for Claude: Your screen recording on a 3D phone (or laptop) that flies in over a moving gradient, with kinetic titles. Use for app and website promos, feature launches, product demos without a face on camera. Builds a finished 9:16 motion-graphics video (no camera footage needed) with the video-studio-core engine."
license: MIT
---

# Device Fly

Your screen recording on a 3D phone (or laptop) that flies in over a moving gradient, with kinetic titles.

- **Best for:** app and website promos, feature launches, product demos without a face on camera
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
python CORE/scripts/run.py - --style STYLE --work edit-device-fly --stop-after plan \
    --no-source --clip screen.mp4 --title "Your tagline" --cta "Download free"
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-device-fly/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-device-fly/plan.json
python CORE/scripts/finish.py edit-device-fly/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- One device, centred, flying in from depth then gently tilting. Title above, short feature chips appear one by one.
- Story: problem (2-3 s) -> the app in action (5-8 s) -> result -> call to action (2 s).
- Cut feature chips to the beat of the music if there is music.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Run make_plan with `--no-source --clip screen.mp4 --title "Your tagline" --cta "Download free"` (input to run.py can be `-`).
- Use `device: laptop` with w=W*0.86, h=W*0.55 for desktop recordings, `browser` for websites.
- Add 3-4 `chip` elements naming features, staggered 1.5 s apart, placed beside or under the device.
- Add music with `music.src` and sfx `whoosh` at the fly-in.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Put my app screen recording in a phone and make a 12-second promo."
- "Make a launch video for my website, laptop mockup."
- "Device-fly promo with the tagline 'Trade smarter'."
