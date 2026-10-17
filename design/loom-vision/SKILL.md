---
name: loom-vision
description: Process a Loom share URL into multimodal context - downloaded video, sampled frames at one frame per 5 seconds, and the auto-generated transcript. Triggers when the user shares a Loom URL, asks "what is happening in this Loom video", or wants visual context beyond the transcript.
plugin: behalfbot-loom-vision
enabled_when: "chassis.config.yaml modules.loom-vision.enabled == true"
metadata: { "openclaw": { "emoji": "🎥", "homepage": "https://behalf.bot", "requires": { "bins": ["node", "loom-dl", "ffmpeg"] }, "install": [ { "id": "node-loom-dl", "kind": "node", "package": "loom-dl@1.1.1", "bins": ["loom-dl"], "label": "Install loom-dl (npm, pinned)" } ] } }
---

# Loom Vision

Use this skill whenever:

- The user pastes a Loom share URL (`https://www.loom.com/share/<32-hex-id>` or similar).
- The user asks you to "watch", "review", "summarize", or "explain" a Loom video.
- The user references a Loom video they recorded and asks a question that needs visual context (e.g. "what was the error on screen at minute 3", "did I click the right button", "what's the diff in that PR walkthrough").

The skill exists because Loom's auto-transcript captures only what was said aloud - not what was on screen. For code walkthroughs, design reviews, and bug repros, the screen contents are often more important than the audio.

## How to invoke

Run the processor script with the Loom share URL. It downloads the mp4, samples frames, and prints the output directory path.

```bash
bash {baseDir}/process-loom.sh "<loom-share-url>"
```

`{baseDir}` expands to the directory containing this `SKILL.md` at runtime - both `process-loom.sh` and `SKILL.md` ship in the same bundle so the script is always co-located with the skill.

The script prints the output directory path to stdout. Inside that directory:

- `video.mp4` - the original video (kept in case you want to re-process at a different frame interval)
- `transcript.vtt` - Loom's auto-transcript as WebVTT with timestamps (read this one)
- `transcript.txt` - the same transcript as plaintext, no timestamps
- `transcript.json` - the raw loom-dl transcript JSON, kept verbatim
- `frame_001.jpg`, `frame_002.jpg`, ... - sampled frames at 1 frame per N seconds (default 5)

Note: loom-dl writes its transcript as `<basename>.transcript.json`, not VTT. The
script converts that JSON into `transcript.vtt` + `transcript.txt` for you, so the
"read the transcript" step below always has a file to read.

## What to do with the output

Read the transcript first to anchor timing, then browse the frames that fall in the relevant time window. For a 10-minute video at 5-second sampling that's 120 frames - review them in batches or jump to the specific window the user asked about.

Frame N corresponds to timestamp `(N - 1) * frame_interval_seconds` from the start of the video. Default interval is 5 seconds, so frame_007.jpg is at the 30-second mark.

## Working with the output

Common patterns:

- **Summarize the whole video.** Read the full transcript, then sample every 6th frame (one per 30 seconds) for the visual narrative. Combine.
- **Answer a specific question.** Search the transcript for the relevant keyword, find the timestamp, look at the frame(s) within plus or minus 10 seconds.
- **Spot what's missing from the transcript.** Errors, popup dialogs, UI states, and on-screen code rarely make it into the spoken audio - go directly to the frames.

## Configuration

The plugin manifest's `configSchema` controls:

- `frame_interval_seconds` - default 5. Lower for densely visual content (animations, fast UI changes), higher for slow walkthroughs. For fast bug repros where you need to catch a transient error, 2-3 seconds is a good tighter setting.
- `frame_max_width_px` - default 1280. Bump up for tiny-font code review videos.
- `frame_quality` - default 3 (ffmpeg `-q:v` scale, 1-31, lower = better).
- `output_root` - default `${CHASSIS_HOME}/temp/`.

These are read at run time from chassis.config.yaml (chassis installs) or set via environment variables before invoking the script (standalone installs). See `{baseDir}/process-loom.sh` for the env var contract.

## Dependencies

Three system CLIs are required (installed by `setup.sh`, idempotent):

- `node` - runs the transcript JSON to VTT conversion. Also required by loom-dl (an npm CLI), so a working loom-dl implies node is present. Install via your platform's package manager.
- `loom-dl` - `npm install -g loom-dl@1.1.1` (pinned; see setup.sh)
- `ffmpeg` - via your platform's package manager (Debian: `apt-get install ffmpeg`). Supplies `ffprobe`, used to bound the final transcript cue.

If you install ffmpeg from something other than a full package - notably the `ffmpeg-static` npm module - you may get the `ffmpeg` binary without `ffprobe`. That is not fatal: the script detects the missing `ffprobe` and degrades gracefully, estimating the end time of the last transcript cue instead of reading the true video duration. Frames, transcript text, and all earlier cue timings are unaffected. To get exact bounding, install ffmpeg via your package manager or the official static builds from ffmpeg.org, which bundle `ffprobe`.

## Why this exists

Most Loom-style integrations treat the video as audio-with-pictures: they ingest the transcript and stop. That loses the entire visual half of a walkthrough - IDE state, error popups, on-screen code, design mockups, the actual change in a PR review.

Sampling at 1 frame per 5 seconds is the sweet spot for code/UI content: dense enough to catch transient errors and UI transitions, sparse enough that a 10-minute video yields 120 frames (manageable batch size for multimodal review). The transcript provides the audio narrative; the frames provide everything else.
