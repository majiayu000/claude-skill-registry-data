---
name: clip-miner
description: "Clip Miner video-editing style for Claude: Finds the best 20-60 s moments in a long video and turns each into a captioned vertical short. Use for podcasts, livestreams, webinars, interviews, long YouTube videos. Turns a raw clip into a finished 9:16 edit with the video-studio-core engine (transcribe, auto-cut, motion graphics, sound, grade)."
license: MIT
---

# Clip Miner

Finds the best 20-60 s moments in a long video and turns each into a captioned vertical short.

- **Best for:** podcasts, livestreams, webinars, interviews, long YouTube videos
- **Category:** Podcast / repurposing
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
python CORE/scripts/run.py clip.mp4 --style STYLE --work edit-clip-miner --stop-after plan
# refine edit-*/plan.json (see below), then check stills:
python CORE/scripts/render.py edit-clip-miner/plan.json --frames 1,3,6,9
python CORE/scripts/render.py edit-clip-miner/plan.json
python CORE/scripts/finish.py edit-clip-miner/plan.json
```

Open `contact_sheet.png` and look at it before the full render. The final video is `final.mp4` in the work folder.
Use `--formats 1:1,16:9` on `finish.py` for extra sizes. Add music with `"music": {"src": "track.mp3", "volume": 0.12}` in the plan.

## The look

- Each clip must start on a hook (a question, a bold claim, a number) and end on a payoff. Never start mid-thought.
- Vertical 9:16, face centred, big captions, a hook title for the first 2.5 s, progress bar.
- Name each output file after its hook.

## Refine the plan

The draft from `make_plan.py` is automatic. Make it good:

- Read `words.json` and rewrite the hook (first 2-3 s) into a short, specific promise.
- Replace weak auto-picked key words with the words that carry the meaning (numbers, results, names, contrasts).
- Fix any mis-heard words in the `words` array (keep their times).
- Workflow: `prep.py long.mp4 --work long` -> `transcribe.py --work long` -> `clip_candidates.py --work long --top 12`.
- Read the candidates and the transcript around them. Pick the best N, adjusting start/end to clean sentence boundaries. Show the user your picks with times and hooks before rendering if they are around.
- For each pick: `run.py long.mp4 --style CLIP_MINER_DIR --work clip01` after trimming with `prep.py long.mp4 --work clip01 --start S --end E` (run the rest of the steps on clip01).
- Any other style can be used for the clips: pass that style's folder instead.
- If the source is 16:9 with the speaker off-centre, set `speaker.focusX` (0 = left, 1 = right).
- Element types and fields: `CORE/references/plan-schema.md`.

## Check before delivering

- Contact sheet: text readable, nothing cut off, nothing covering the face unless intended, safe zones respected (9:16: keep text between 10% and 85% of the height).
- Watch for timing: overlays land with the spoken word, not after it.
- `ffprobe` the final file: right size, duration and audio.
- Tell the user what you cut (seconds removed), what the look adds, and where the file is.

## Change the look

Colours and fonts live in `theme.json` (`vars`, `fontsUrl`) and `theme.css`. For a one-off change, edit `plan.json` (`theme.vars`, element `style`) instead of the skill files.

## Example requests

- "Find the 8 best moments in this podcast and make shorts."
- "Clip-mine my 1-hour livestream into reels."
- "Give me 5 viral clips from this interview, score the hooks."
