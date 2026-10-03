---
name: video-shorts-localized
description: Create short clips from a YouTube URL or local long-form video with subtitles in one or more requested languages. Use when Codex needs to analyze a transcript, select strong short-form moments, translate or localize subtitles, write per-language packaging copy, and export hard-subbed shorts from interviews, talks, podcasts, explainers, streams, or similar videos.
---

# Video Shorts Localized

## Overview

Turn one long-form video into several review-ready short clips with subtitles and packaging in the languages the user requests.

## Workflow

1. Confirm prerequisites.
Check `yt-dlp` and `ffmpeg` first.
If you are touching subtitle localization or using the skill on a new machine, run [smoke_test.py](./scripts/smoke_test.py) once to validate UTF-8 writes and Chinese hard-sub rendering.

2. Capture the localization requirements.
Determine:
- target clip count
- target language or languages
- whether the source is a YouTube URL or a local video file

3. Create the work layout.

```text
work/<video-slug>/
  source/
  analysis/
  clips/
```

4. Ingest the source.
- For YouTube URLs, run [download_youtube.py](./scripts/download_youtube.py)
- For local source videos, copy the source into `source/original.<ext>` and obtain or generate the best subtitle file you can
- The downloader now fetches the video once, then walks subtitle language preferences one by one so a failure or `429` on one subtitle locale does not kill the entire ingest step

5. Parse the source subtitle file.
Use [srt_to_json.py](./scripts/srt_to_json.py) and save `analysis/transcript.json`.

6. Select candidate clips.
Read [clip-schema.md](./references/clip-schema.md) and [analysis-prompt.md](./references/analysis-prompt.md). Write:
- `analysis/selected_clips.json`
- `analysis/candidate-review.txt`

7. Apply clip rules.
- Default to 3 to 10 clips unless the user asks for another count
- Prefer 15 to 180 seconds per clip
- Favor one clear idea per clip
- Favor strong openings, complete endings, and context-light moments
- Reject filler, greetings, sponsor reads, and fragments that end mid-thought

8. Export the raw clip windows.
- Cut the source video with [clip_video.py](./scripts/clip_video.py)
- Window the subtitle file with [window_srt.py](./scripts/window_srt.py)
- Keep `clip.<source-lang>.srt` for review whenever possible so translation issues can be checked against source phrasing

9. Produce one localization set per requested language.
For each target language:
- translate or clean the local clip subtitle into natural spoken output for that language
- write a short title and a short description in that language
- burn subtitles and a first-second title with [burn_subtitles.py](./scripts/burn_subtitles.py)
- Prefer the script defaults for font selection; it now chooses common CJK-capable fonts per platform when available

10. Write all localized files safely.
Never write non-ASCII subtitle or metadata files via raw shell heredocs or shell redirection.

Instead:
- build a JSON payload of files to create
- serialize the payload with `json.dumps(..., ensure_ascii=True, indent=2)`
- run [write_localized_assets.py](./scripts/write_localized_assets.py) with that payload

Use one payload for all requested languages if convenient.

11. Verify artifacts before returning.
- Confirm the expected files exist for every clip and language
- If terminal output shows `???`, do not assume corruption; verify bytes or inspect with Python using `unicode_escape`
- Treat missing subtitle files, empty subtitle files, or zero-byte exports as blockers and report them explicitly

## File Layout

```text
work/<video-slug>/
  source/
    original.mp4
    original.<lang>.srt
  analysis/
    transcript.json
    selected_clips.json
    candidate-review.txt
    clip-packaging.<lang>.txt
  clips/
    01-<slug>/
      clip.mp4
      clip.<source-lang>.srt
      clip.<lang>.srt
      clip.hardsub.<lang>.mp4
      metadata.<lang>.txt
```

Use language suffixes consistently, even when the user asks for only one target language.

## Resources

- Scripts:
  [download_youtube.py](./scripts/download_youtube.py),
  [srt_to_json.py](./scripts/srt_to_json.py),
  [window_srt.py](./scripts/window_srt.py),
  [clip_video.py](./scripts/clip_video.py),
  [burn_subtitles.py](./scripts/burn_subtitles.py),
  [write_localized_assets.py](./scripts/write_localized_assets.py),
  [smoke_test.py](./scripts/smoke_test.py)
- References:
  [clip-schema.md](./references/clip-schema.md),
  [analysis-prompt.md](./references/analysis-prompt.md)

## Output Contract

Return:
- the source asset folder
- the selected clip list with timestamps, duration, title, and summary
- the packaging file path for each requested language
- the final `clip.hardsub.<lang>.mp4` path for each exported short and language

If the workflow cannot finish, report the exact blocker.
