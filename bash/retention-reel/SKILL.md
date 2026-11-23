---
name: retention-reel
description: "Professional retention editor for talking-head Reels, TikToks and YouTube Shorts (15-60 s). Cuts a raw clip the way a top short-form editor does - hook on screen by 1.5 s, open loop, one idea per beat, a visual change every 1.5-3 s, payoff, then a CTA or a seamless loop back to the first frame - and delivers 9:16 burned-in, clean and SRT versions. Use when the user says: make this a reel, edit for retention, cut this for TikTok/Shorts, tighten my talking clip, make it go viral, hook + captions + zooms, short-form edit. Pick any Video Studio skin for the look (default halo-cut)."
license: MIT
---

# Retention Reel

Turns one raw talking clip into a short that holds the scroll: hook by 1.5 s, no dead air, payoff, loop or CTA.

- **Best for:** tips, opinions, stories, announcements, founder clips, one person talking to camera
- **Inputs:** one talking clip (any orientation; 16:9 gets a face-follow reframe), optional music, optional B-roll folder
- **Default skin:** `halo-cut` · alternatives `hook-lab`, `bold-bounce`, `depth-type` (text behind the head)
- **Formats:** 9:16 1080x1920 master, 4:5 feed, clean (no captions), `captions.srt`
- **Duration target:** 15-60 s (sweet spot 20-40 s); genre preset `retention-reel`

## Before you start

- Needs the **video-studio-core** skill in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder that holds both, so a skin is `SKILLS/halo-cut`.
- First time on a machine: `python CORE/scripts/check_env.py` and fix what it prints.
- Read the preset once: `python CORE/scripts/editor.py genre retention-reel`.
- Work in a new folder next to the footage (`edit-<name>/`), never inside a skill folder.
- The `--genre` preset sets autocut's pause cut (0.3 s) and run.py respects it; pass `--max-gap` only to override.

## How a pro cuts this

**Structure** (percent of the finished length):

| beat | % | what happens |
| --- | --- | --- |
| hook | 0-6 | the strongest line or visual, on screen as text (<= 7 words), lands by 1.5 s |
| open loop / setup | 6-18 | a number, question, contrast or stakes the end will pay off |
| value beats | 18-76 | one idea per beat, each 3-6 s, something changes every 1.5-3 s |
| payoff | 76-92 | close the loop; the line people will share |
| loop-back / CTA | last 2 s | a CTA, or the last line runs straight into the first frame |

- **Pacing:** ASL 1.5-3 s. Vary it: a 4 s hold on the emotional line, 1 s snaps in a list. Never uniform.
- **Cut rules:** cut at the end of a thought, in the quietest gap (`--smart-cuts`), keep 0.1 s of breath before a word. Jump cuts are allowed here, but alternate punch-in sizes (1.12x / 1.07x) so it doesn't feel like a metronome. Keep the last good take (`--retakes`).
- **Never open with** "hi guys", "welcome back", "in this video", a logo or > 0.3 s of silence. Start on the hook sentence even if it was said at 0:40 (`story.py reorder`).
- **J/L cuts:** rarely needed in a single-camera reel; use an L-cut only when B-roll runs over a statement.
- **Transitions:** cut. Zoom punch on key words, an occasional whip or flash on a topic change. One transition kind per reel.
- **Music/SFX:** optional bed 20-24 LU under the voice, ducked. SFX medium density (~10-15 per minute): pop on key words, swish on cuts, impact on the payoff. Drop the music 0.5 s before the payoff line.
- **Colour:** correct first, then `clean-commercial` or `punchy` at 0.6-0.8. Moody topics: `moody` 0.5.
- **Captions:** motion.md preset `hormozi` (or the skin's own), 1-3 words, <= 17 cps, inside 10-85 % height and clear of the right 12 %, `dodgeFace: true`.
- **Client judges:** 3-second hold, watch-through %, shares and saves, "does it look native".
- **Common mistakes:** slow open, every pause removed (breathless), 3+ overlays stacked, captions under the platform buttons, an outro after the payoff, a hook that the video never pays off.

## Make the edit

```bash
python CORE/scripts/run.py clip.mp4 --style SKILLS/halo-cut --genre retention-reel \
  --smart-cuts --retakes --work edit-reel --stop-after plan
#   16:9 source? add  --reframe 9:16   (face-follow crop before prep)
#   B-roll folder?    add  --broll broll/   (files named after what they show)
python CORE/scripts/story.py outline --work edit-reel --genre retention-reel   # read outline.md: ranked hooks
```

If the best hook is not the first sentence, build a cold open and re-run the plan on it:

```bash
python CORE/scripts/story.py reorder --work edit-reel --order "s5,s1-s4,s6-s9" --genre retention-reel --format 9:16
#  read story_flags.md (Frankenbite / back-reference warnings), then:
python CORE/scripts/run.py - --timeline edit-reel/story_timeline.json --style SKILLS/halo-cut --genre retention-reel \
  --smart-cuts --work edit-reel2 --stop-after plan
```

Then review, fix and look:

```bash
python CORE/scripts/editor.py review edit-reel/plan.json --genre retention-reel --fix   # read review.md
python CORE/scripts/render.py edit-reel/plan.json --frames 0.5,2,6,12,18               # LOOK at contact_sheet.png
python CORE/scripts/render.py edit-reel/plan.json
python CORE/scripts/finish.py edit-reel/plan.json --platform reels --formats 4:5
```

## Refine the plan

- **Hook text:** rewrite the hook element to <= 7 words that promise the payoff ("I lost $40k doing this"). Start 0.0 s, hold to ~2.4 s.
- **Captions:** `{"type": "captions", "preset": "hormozi", "keywords": ["40k", "never"], "dodgeFace": true, "cpsMax": 17}`.
- **Zooms:** `speaker.zooms` on 4-8 key words, start 0.05 s before the word, scale 1.12 then 1.07, never closer than 2.4 s apart.
- **Numbers:** a `counter` (`"from": 0, "to": 40000, "prefix": "$"`) for every number that matters.
- **Lists:** a `checklist` or `steps` element with `items[].at` = the second each item is said.
- **Open loop:** a `chip` or `progress` (`"position": "top"`) to show there is an end worth waiting for.
- **Loop ending:** trim the last line so its final word runs into the first word of the hook; no endcard. Or a CTA `text` in the last 2 s.
- **Sound:** `"sfx": [{"t": 0.0, "kind": "impact", "gain": 0.5}, {"t": 12.3, "kind": "whoosh-short", "gain": 0.45}]`; `"music": {"src": "bed.mp3", "under": 22, "duck": "speech-aware", "fitTo": "beats"}`.
- **Colour:** `"color": {"look": "clean-commercial", "intensity": 0.7}`; `"finish": {"grain": 4, "sharpen": 0.3}`.
- Re-run `editor.py review ... --fix` after every change and look at the frames again.
- **Face-aimed punch-ins:** with `W/track.json` the zooms centre on the face instead of the frame centre: after `run.py ... --stop-after cut` (`--stop-after timeline` for a `--timeline` spec) run `python CORE/scripts/track.py analyze W/cut.mp4 --work W`, then `make_plan.py` (it copies the track into the plan). Per zoom, `"cx"`/`"cy"` (0-1) aim elsewhere; `"toFace": false` keeps centre.

## Deliver

```bash
python CORE/scripts/deliver.py edit-reel/plan.json --to reels,tiktok,shorts --out-dir edit-reel/deliver
python CORE/scripts/qc.py edit-reel/deliver/final_reels.mp4 --plan edit-reel/plan.json --platform reels --strict
```

- `deliver.py` writes `captions.srt/.vtt`, a cover thumbnail and `post.md` (titles and hashtags from the transcript only).
- **Clean version:** copy `plan.json` to `plan_clean.json`, delete the `captions` and hook elements, set `"outputFile": "final_clean.mp4"`, then `render.py` + `finish.py` on it.
- Name files `client_project_v001_9x16_captions.mp4`; keep every version.

## Check before delivering

- Hook on screen and spoken by 1.5 s; first word <= 0.3 s; no greeting.
- `review.md` has no HIGH items; contact sheet: nothing over the face, nothing under the right rail, <= 2 overlays plus captions.
- Captions match the audio word for word; names and numbers spelled right.
- `qc.py`: -14 LUFS, -1 dBTP, no black or flash frames, 9:16 safe zone passes.
- It loops cleanly or ends on the CTA; nothing after the payoff.
- Tell the user: seconds removed, the hook you chose and why, the look, every file path.

## Example requests

- "Make this a reel that keeps people watching - hook, captions, zooms, under 40 seconds."
- "Edit my TikTok with bold-bounce, start with the line about losing 40k."
- "Retention edit for Shorts from this 16:9 clip, loop the ending back to the start."
