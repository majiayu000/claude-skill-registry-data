---
name: clip-miner-pro
description: "Professional clip-mining editor: finds the 5-15 strongest stand-alone moments in a long recording (podcast, interview, livestream, webinar, talk), checks each one makes sense without the episode, trims it to clean sentence boundaries, reframes 16:9 to 9:16 on the speaker's face, adds a hook title, captions and a CTA back to the full episode. Use when the user says: find the best moments, make shorts from my podcast, clip this livestream, repurpose this video, cut viral clips, extract highlights for Reels/TikTok/Shorts. Any Video Studio skin works (default clip-miner)."
license: MIT
---

# Clip Miner Pro

Mines a long recording for clips that stand on their own, then cuts each one like a short-form editor.

- **Best for:** podcasts, interviews, webinars, livestreams, keynotes, long YouTube videos
- **Inputs:** one long video (16:9 or 9:16), the episode title for the CTA
- **Default skin:** `clip-miner` · alternatives `halo-cut`, `pod-frame`, `hook-lab`
- **Formats:** 9:16 1080x1920 per clip (captioned + clean), `captions.srt` per clip
- **Duration target:** 20-60 s per clip (30-90 s for podcast stories); 5-15 clips; genre preset `clip-miner-pro`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre clip-miner-pro`.
- One work folder for the long file (`mine/`) and one per clip (`clip01/`, `clip02/`...).
- The `--genre` preset sets autocut's pause cut (0.35 s) and run.py respects it; pass `--max-gap` only to override.
- Ask for the episode/show name and where the full episode lives (for the CTA).

## How a pro cuts this

**What makes a clip:** it starts on a hook sentence (claim, number, question, contrast, story start), it has one idea, and it ends on a payoff line. Somebody who never saw the episode must understand it. Reject clips that need earlier context ("as I said", "that's why he...").

| beat | % | what happens |
| --- | --- | --- |
| hook | 0-10 | first spoken sentence is the hook; hook title on screen 0-2.5 s |
| context | 10-20 | only the minimum needed to follow |
| story / value | 20-85 | the moment itself, trimmed of tangents |
| payoff | 85-95 | the line that lands |
| CTA | last 2 s | "full episode: <title>" |

- **Pacing:** ASL 2-4 s; a punch-in or reframe change every 2.5-3 s on a single wide speaker; keep the speaker's rhythm (podcasts breathe more than reels).
- **Cut rules:** start and end on whole sentences only. Remove tangents inside the clip with `--cut` ranges, keep breaths. Never splice two unrelated sentences into a new claim (Frankenbite) - if you must join lines from different parts, tell the user and keep the meaning.
- **Two speakers:** `--reframe 9:16` follows the active speaker; for a conversation where both react, `track.py reframe --layout stack2` puts them top and bottom.
- **Transitions:** cut. Punch-ins hide jump cuts. No flashy transitions on serious topics.
- **Music/SFX:** usually none, or a very low bed (24 LU under). One pop on the hook title, nothing on every word.
- **Colour:** keep the episode's look; correct only. `clean-commercial` 0.5 if the source is flat.
- **Captions:** preset `hormozi` or `boxed`, 2-3 words, <= 17 cps, `dodgeFace: true`; name the speaker with a `lowerthird` the first time.
- **Client judges:** does each clip stand alone, hook strength, watch-through, clicks back to the episode.
- **Common mistakes:** clips that start mid-thought, inside jokes that need context, 90 s rambles, captions over the face, clips that all sound the same (vary topics and emotion).

## Make the edit

Mine the long file first:

```bash
python CORE/scripts/prep.py episode.mp4 --work mine
python CORE/scripts/transcribe.py --work mine --model small --prompt "Guest Name, Brand"
python CORE/scripts/clip_candidates.py --work mine --min 20 --max 60 --top 15
python CORE/scripts/story.py outline --work mine --genre clip-miner-pro      # quotable lines + hook scores
```

Read `candidates.json` and `outline.md`, read the transcript around each candidate, and pick the best N. Move each start to the hook sentence and each end to the payoff sentence. Show the user the list (times, hook, why) before cutting if they are around.

Cut each pick (source times S-E from the transcript):

```bash
python CORE/scripts/prep.py episode.mp4 --work clip01 --start 754.2 --end 801.9
python CORE/scripts/run.py clip01/source.mp4 --reframe 9:16 --style SKILLS/clip-miner --genre clip-miner-pro \
  --smart-cuts --retakes --cta "Full episode: SHOW TITLE" --work clip01-edit --stop-after plan
python CORE/scripts/editor.py review clip01-edit/plan.json --genre clip-miner-pro --fix
python CORE/scripts/render.py clip01-edit/plan.json --frames 0.5,3,10,20
python CORE/scripts/render.py clip01-edit/plan.json
python CORE/scripts/finish.py clip01-edit/plan.json --platform shorts
```

For a two-person shot that should stay stacked: `python CORE/scripts/track.py reframe clip01/source.mp4 --out clip01/stack.mp4 --format 9:16 --layout stack2` and use `clip01/stack.mp4` as the run.py input without `--reframe`.

## Refine the plan

- **Hook title:** a `text`/`headline` element 0.0-2.5 s, <= 7 words, written from what is actually said (no invented claims).
- **Captions:** `{"type": "captions", "preset": "hormozi", "dodgeFace": true, "keywords": ["..."]}`.
- **Speaker name:** `{"type": "lowerthird", "name": "Priya Rao", "role": "Founder, X", "start": 2.6, "end": 6}` (ask for spelling).
- **Pattern interrupts:** `speaker.zooms` every 2.5-3 s on key words (1.12x / 1.07x alternating).
- **Progress:** `{"type": "progress", "position": "top"}` helps long clips.
- **CTA:** the `--cta` text sits in the last 2 s; keep it, or use a `chip` "Full episode on YouTube".
- **Sound:** `"audio": {"voice": {"denoise": "light", "eq": "clear"}}`; music only if the show uses it.
- Name each work folder and output after its hook: `"outputFile": "clip01_why-we-fired-our-best-client.mp4"`.
- **Face-aimed punch-ins:** with `W/track.json` the zooms centre on the face instead of the frame centre: after `run.py ... --stop-after cut` (`--stop-after timeline` for a `--timeline` spec) run `python CORE/scripts/track.py analyze W/cut.mp4 --work W`, then `make_plan.py` (it copies the track into the plan). Per zoom, `"cx"`/`"cy"` (0-1) aim elsewhere; `"toFace": false` keeps centre.

## Deliver

```bash
python CORE/scripts/deliver.py clip01-edit/plan.json --to shorts,reels,tiktok --out-dir clip01-edit/deliver
python CORE/scripts/qc.py clip01-edit/deliver/clip01_why-we-fired-our-best-client_shorts.mp4 --plan clip01-edit/plan.json --platform shorts
```

- Each clip gets `captions.srt`, a cover thumbnail and a `post.md` draft (titles from the transcript only).
- Clean versions: copy the plan, remove `captions` and the hook title, new `outputFile`, render + finish.
- Keep a `clips.md` index: clip number, source in/out, hook, file names.

## Check before delivering

- Every clip makes sense to a stranger; starts on a hook sentence, ends on a payoff, no mid-word starts.
- Face stays in frame after the reframe (scrub the contact sheet at 4-5 points per clip).
- No constructed quotes; speaker names and titles correct.
- Captions inside the 9:16 safe zone and clear of the face; <= 17 cps.
- `qc.py` passes (-14 LUFS, -1 dBTP, length under the platform limit).
- Tell the user: each clip's source time range, hook, length and file path.

## Example requests

- "Find the 8 best moments in this 1-hour podcast and make Shorts with captions."
- "Clip-mine my livestream into reels - each one has to work on its own."
- "Give me 5 clips from this interview, follow whoever is talking, CTA to the full episode."
