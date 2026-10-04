---
name: media-toolkit
description: Process audio and video with clipping, conversion, analysis, captions, thumbnails, GIFs, and batch utilities. Use for practical media manipulation workflows.
---

# Media Toolkit

Use this suite for practical audio and video operations that were previously spread across many narrow skills.

## Included Tools

- Audio: `audio_analyzer.py`, `audio_converter.py`, `audio_normalizer.py`, `audio_trimmer.py`, `podcast_splitter.py`, `sfx_generator.py`
- Video: `video_captioner.py`, `video_clipper.py`, `video_metadata_inspector.py`, `video_thumbnail_extractor.py`, `gif_workshop.py`, `thumbnail_gen.py`, `timelapse_creator.py`

## Workflow

1. Identify the medium, input format, and target output.
2. Pick the narrowest script that completes the job.
3. Keep transformations explicit: clip times, output codec, target size, caption source, or thumbnail cadence.
4. Verify output duration, dimensions, and bitrate-sensitive settings when the request depends on platform limits.

## Guardrails

- Avoid recompression churn when a simple trim or extract is enough.
- Call out when generated captions or “best frame” choices are heuristic.
