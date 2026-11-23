---
name: neon-orbit
description: "Neon Orbit video-editing style for Claude: A glowing cyan ring and orbiting lights behind the speaker's head, neon captions, night-time grade. Use for tech, crypto, gaming, nightlife, AI and futuristic topics. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Neon Orbit

A glowing cyan ring and orbiting lights behind the speaker's head, neon captions, night-time grade.

- **Best for:** tech, crypto, gaming, nightlife, AI and futuristic topics
- **Category:** Talking-head reel
- **Default format:** 9:16 (change with `--format 9:16 | 1:1 | 4:5 | 16:9`)
- **Needs camera footage:** yes, a raw talking clip
- **Text behind the speaker:** yes (uses the person cut-out)

## Before you start

This style runs on the **video-studio-core** skill, which must be installed in the same skills folder.

- `CORE` = the `video-studio-core` folder next to this one (e.g. `~/.claude/skills/video-studio-core`).
- `STYLE` = this skill's folder (it holds `theme.json` and `theme.css`).
- First time on a machine: `python CORE/scripts/check_env.py`, and fix anything it reports.
- If `CORE` is missing, tell the user to install `video-studio-core` from the same pack.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-neon-orbit --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-neon-orbit/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-neon-orbit/plan.json
python CORE/scripts/finish.py edit-neon-orbit/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Ring centred on the head (behind it), soft glow behind the ring, 3 light dots orbiting.
- Captions in white with a neon glow; key words in magenta.
- Ring pulses on key words (`pulseOn`). Neon grade and vignette.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Look at a still and set the ring, glow and orbit `x`/`y` to the centre of the head. Size the ring about 1.6x the head width.
- Copy the key-word times into the ring's `pulseOn` list.
- Needs the person matte so the ring passes behind the head.
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Neon-orbit edit for my AI tools video."
- "Glowing ring behind my head, futuristic vibe."
- "Make my crypto take look like a sci-fi trailer."
