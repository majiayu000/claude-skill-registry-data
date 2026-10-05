---
name: global-clip-forge
description: Use when the user wants to turn a long YouTube interview, talk, or podcast into 5 to 8 short clips for a target audience language. This skill downloads the source video and any available subtitles, can transcribe videos that have no subtitles with an open-source Whisper model, lets the calling AI translate subtitles into a user-specified target language, analyzes the transcript, selects strong standalone moments, cuts clips under 3 minutes, prepares target-language packaging copy, and burns stacked bilingual subtitles into the exported videos.
---

# Global Clip Forge

## Overview

Use this skill to convert one long YouTube interview into multiple short hard-sub clips that are ready to review or post for a specific audience language. It bundles the download, transcript parsing, optional Whisper transcription fallback, AI-driven target-language subtitle translation, clip cutting, subtitle windowing, bilingual subtitle merge, and hard-sub burn-in helpers.

Key implementation points to keep in sync with the repository:
- The downloader can accept user-specified subtitle language priorities instead of being locked to English and Chinese.
- The source fetch path prefers Chrome cookies and uses the Android client route for a simpler MP4 download.
- The transcription helper supports both Whisper `transcribe` and `translate` tasks.
- When local transcription is needed, use the shared virtual environment under `work/.venv/` and install the standard `openai-whisper` package there instead of trying `mlx-whisper` first.
- For subtitle-free videos longer than 1 hour, prefer Whisper `base` to keep local transcription practical. For videos up to 1 hour, prefer `small` for better subtitle quality.
- Target-language translation is normally done by the calling AI so the workflow stays flexible across languages and environments.
- `translate_subtitles.py` remains available as an optional helper when you explicitly want a script-driven subtitle translation step.
- The hard-sub renderer uses transparent PNG overlays with `ffmpeg overlay`, so it does not depend on `libass` or `drawtext`.
- Subtitle-only export is the default. Only add a title card when the user explicitly asks for one, and keep title text in the target language only.
- Once the clip subtitle files are ready, the workflow should go straight to `clip.hardsub.mp4` export without asking for another confirmation step.

## When To Use

- The user gives a YouTube interview, talk, keynote, or podcast URL and wants multiple short clips.
- The user wants clips localized for a target audience language, with bilingual subtitles when helpful.
- The source video may not have platform subtitles, so the workflow needs a local transcription fallback.
- The user wants review-friendly candidate clip suggestions before export, or explicitly wants you to pick the best set yourself.

## Workflow

1. Confirm prerequisites.
Check `yt-dlp` and `ffmpeg` availability first. The helper scripts can use system `ffmpeg` or the `imageio-ffmpeg` binary fallback.

2. Create a work layout.
Use a layout like:

```text
work/<video-slug>/
  source/
  transcripts/
  analysis/
  clips/
```

3. Decide the localization plan up front.
Identify:
- the source language spoken in the video if known
- the target audience language requested by the user
- whether the export should be bilingual or target-language only
- whether title cards should be shown, and if so, keep them in the target language only

4. Download source assets.
Run [fetch_source.py](./scripts/fetch_source.py) with the YouTube URL and the `source/` directory. Pass `--subtitle-langs` in priority order when the user has a target language preference, for example `--subtitle-langs 'ja,ja-JP' --subtitle-langs 'en,en-US'`. This downloader prefers browser cookies and uses the more reliable Android client path for the MP4 download.

5. Inspect the downloaded files.
Identify:
- the source `.mp4`
- the subtitle `.srt`
- any sidecar files such as `.ytdl`

6. If the video has no usable subtitles, transcribe it locally.
Run [transcribe_subtitles.py](./scripts/transcribe_subtitles.py) against the downloaded video and save the generated SRT into `work/<video-slug>/transcripts/`. Use the default `transcribe` task to create source-language subtitles, or `translate` when you specifically need Whisper to emit English subtitles from non-English speech. Keep all original, translated, and merged subtitle artifacts in that `transcripts/` folder for unified management.
If Whisper is not already available, create and use `work/.venv/` as the shared local install location, then install the standard `openai-whisper` package there. Reuse that environment across subtitle-free tasks instead of reinstalling for each video. Do not try `mlx-whisper` first.
When you do not explicitly pass `--model`, let the helper auto-pick `small` for videos up to 1 hour and `base` for videos longer than 1 hour.

7. Create the target-language subtitle track.
If the target audience language differs from the source language, have the calling AI translate the subtitle text into the target language while preserving timestamps and write `source.<target>.srt` or `clip.<target>.srt`. Use the translated target-language file for packaging copy and for the title card text. If you explicitly want a script-driven translation step, [translate_subtitles.py](./scripts/translate_subtitles.py) can still be used as an optional helper.

8. Parse the working subtitle file into JSON.
Use [parse_subtitles.py](./scripts/parse_subtitles.py) and save the artifact into `analysis/transcript.json`.

9. Analyze before cutting.
Read [clip-schema.md](./references/clip-schema.md) and [analysis-prompt.md](./references/analysis-prompt.md). Generate a generous candidate list, then write `analysis/selected_clips.json` and `analysis/candidate-review.txt`.

10. Candidate rules.
- Target 5 to 8 exported clips unless the user asks for another count.
- Prefer clips between 20 and 180 seconds.
- Favor one clear idea per clip.
- Favor strong opening lines, complete endings, and minimal dependency on missing context.
- Reject filler, greetings, sponsor reads, and fragments that end mid-thought.

11. Export each chosen clip.
- Cut the video with [cut_clip.py](./scripts/cut_clip.py)
- Window both subtitle tracks with [trim_subtitles.py](./scripts/trim_subtitles.py) when you have separate source-language and target-language subtitle files
- If the target language differs from the source language, have the calling AI translate the local clip SRT into the target language while preserving timestamps
- If bilingual output is requested, merge the source-language and target-language subtitle files into one stacked bilingual SRT with [merge_bilingual_subtitles.py](./scripts/merge_bilingual_subtitles.py)
- Burn subtitles with [render_hardsubs.py](./scripts/render_hardsubs.py), and if a title card is requested pass the title in the target language only
- Do not stop for an extra approval round once subtitle assets are ready; export the final hard-sub video in the same run whenever feasible

12. Packaging copy.
For each exported clip, create:
- one short, sharp title in the target language
- one target-language description under 140 characters

Write per-clip metadata into each clip folder and also compile a combined `analysis/clip-packaging.txt`.

## File Layout

Use:

```text
work/<video-slug>/
  source/
    original.mp4
    original.<lang>.srt
  transcripts/
    source.<source-lang>.srt
    source.<target-lang>.srt
    source.bilingual.srt
  analysis/
    transcript.json
    selected_clips.json
    candidate-review.txt
    clip-packaging.txt
  clips/
    01-<slug>/
      clip.mp4
      clip.<source-lang>.srt
      clip.<target-lang>.srt
      clip.bilingual.srt
      clip.hardsub.mp4
      metadata.txt
```

## Script Notes

- Run the helper scripts from the skill root with `PYTHONPATH="$PWD"` when using `python3 -m scripts.<name>`.
- For local transcription tasks, keep Python packages isolated inside the shared `work/.venv/` instead of installing Whisper globally on the machine.
- Prefer the standard `openai-whisper` package inside that shared venv. Only deviate if the user explicitly asks for another runtime.
- Prefer a font that comfortably supports the target audience language. If no better font is available, let the script fall back to the system default.
- The hard-sub renderer now defaults to subtitle-only exports. Only pass `--title` when the user explicitly wants an opening title card.
- If a title card is used, keep it in the target language only instead of rendering bilingual title text.
- Subtitle parsing keeps line breaks intact so bilingual subtitles can stay stacked as `target language` plus `source language`.
- When `clip.<target-lang>.srt` or `clip.bilingual.srt` is already prepared, proceed directly to `clip.hardsub.mp4` creation instead of pausing for another user confirmation.
- The downloader uses Chrome cookies when available. If download fails because cookies are stale, refresh browser login state before changing the workflow.
- `ffmpeg` can come from either the system path or the `imageio-ffmpeg` fallback helper.
- `transcribe_subtitles.py` now auto-selects Whisper `base` for videos longer than 1 hour and `small` otherwise, unless the user explicitly overrides `--model`.

## Resources

- Scripts:
  [fetch_source.py](./scripts/fetch_source.py),
  [parse_subtitles.py](./scripts/parse_subtitles.py),
  [transcribe_subtitles.py](./scripts/transcribe_subtitles.py),
  [translate_subtitles.py](./scripts/translate_subtitles.py),
  [trim_subtitles.py](./scripts/trim_subtitles.py),
  [merge_bilingual_subtitles.py](./scripts/merge_bilingual_subtitles.py),
  [cut_clip.py](./scripts/cut_clip.py),
  [render_hardsubs.py](./scripts/render_hardsubs.py)
- References:
  [clip-schema.md](./references/clip-schema.md),
  [analysis-prompt.md](./references/analysis-prompt.md)

## Output Contract

Return:
- the source asset folder
- the candidate clip list with timestamps, duration, title, and two-sentence summaries
- the packaging text file path
- the final `clip.hardsub.mp4` path for each exported short

If the workflow cannot finish, report the exact blocker, such as stale cookies, failed download, missing `ffmpeg`, unavailable Whisper runtime, or unusable transcript quality.
