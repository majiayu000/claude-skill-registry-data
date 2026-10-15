---
name: Video Frames
description: Extract frames or the audio track from a local video file via ffmpeg. Pairs with openai-whisper for audio→text.
requires:
  bins:
    - ffmpeg
    - ffprobe
  env: []
---

# Video Frames

Use this skill whenever a local video file must become text (via audio +
Whisper) or selected JPG frames. The extension wraps `ffmpeg`/`ffprobe`
subprocesses with a path sandbox and per-call timeout.

## Use when

- "Transcribe this video"
- "Grab 12 frames from this clip"
- "What does this video say?" — chain through audio + whisper + summarize
- Prepare material from `bible_videos/` for agent kate to study

## Do not use when

- The file is not locally accessible (fetch first with `fetch_url` if
  allowed; operator decides the save path inside the sandbox)
- The clip is > 500 MB — split or downscale upstream
- You need real-time / streaming — this is batch only
- You need OCR on frames — that's a separate pipeline

## Tools

### `status`
No arguments. Returns ffmpeg + ffprobe versions, sandbox root, input and
frame limits.

### `probe`
- `path` (string, required) — local video file

Returns `{duration_secs, format, streams}` as JSON.

### `extract_frames`
- `path` (string, required)
- `output_dir` (string, required) — must lie under the sandbox root
- `count` (integer, optional, 1–1000, default 10) — evenly spaced over the whole clip
- `fps` (number, optional, 0.01–60) — overrides `count` with a fixed sample rate
- `width` (integer, optional, 16–4096) — resize keeping aspect ratio

Returns `{count_written, frames: [path, ...]}`.

### `extract_audio`
- `path` (string, required)
- `output_path` (string, required) — full path under the sandbox
- `codec` (string, optional, `mp3` default | `wav`)
- `mono` (boolean, optional, default true) — recommended for Whisper
- `sample_rate` (integer, optional, 8000–48000, default 16000) — matches Whisper

Returns `{output_path, bytes, codec, mono, sample_rate}`.

## Execution guidance

- For audio destined for `openai-whisper`, prefer **WAV mono 16 kHz** — this
  is the Whisper-native layout and avoids re-encoding downstream.
- Use `probe` first when the user's ask depends on duration (e.g.
  "every 30 seconds").
- Keep `count` modest (≤ 24 for most overview tasks). Thousand-frame dumps
  are rarely useful to an LLM.
- Error codes:
  - `-32030` ffmpeg missing → alert the operator
  - `-32032` ffmpeg failed → include the stderr preview in the reply so
    the user knows why (e.g. "no audio stream" for silent clips)
  - `-32033` timeout → suggest a shorter clip or a higher
    `VIDEO_FRAMES_TIMEOUT_SECS`
  - `-32034` io/sandbox → path was outside `VIDEO_FRAMES_OUTPUT_ROOT`;
    ask operator to use a sandboxed directory
- Wrap `extract_audio` → `transcribe_file` → `summarize_text` in a
  TaskFlow so a restart does not re-extract audio you already have.
