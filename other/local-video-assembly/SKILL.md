---
name: local-video-assembly
description: Plan, assemble, and validate local video exports with FFMPEG and ffprobe. Use when Codex is asked to create render manifests, assemble narrated explainers, combine stills/slides/audio/captions, burn in subtitles, normalize audio, export MP4 files, or verify local video packages before human-reviewed publishing.
license: MIT
---

# Local Video Assembly

## Core Workflow

1. Identify the target output: platform, aspect ratio, resolution, frame rate,
   target length, source assets, voiceover, captions, review owner, and whether
   captions should be sidecar, burned in, or both.
2. Inspect local inputs before planning commands: image dimensions, audio
   duration, sample rate, caption timing, missing files, rights/provenance
   notes, and any render constraints from the surrounding production brief.
3. Create or update a render manifest with scene order, file paths, durations,
   visual treatment, voiceover segments, caption references, overlays, output
   profile, and acceptance checks.
4. Plan FFMPEG assembly with deterministic local steps: normalize source media,
   compose still or slide scenes, sync narration, add simple motion or fades,
   apply captions, normalize loudness, and export a review MP4.
5. Validate the export with `ffprobe` and visual/audio spot checks: confirm
   video stream, audio stream, resolution, duration, frame rate, sample rate,
   caption readability, audio sync, and no missing or placeholder assets.
6. Return a human-review package with the final file path, validation summary,
   known issues, disclosure/provenance notes, and a clear `go`, `revise`, or
   `hold` recommendation for the next publishing checklist.

## MVP Defaults

- Use a 16:9 narrated explainer profile unless the user requests another
  format: 1920x1080, 30 fps, MP4 container, H.264 video, AAC stereo audio at
  48 kHz, progressive scan, `yuv420p`, and fast-start metadata.
- Prefer still, slide, screenshot, or generated-image scenes with restrained
  pans, zooms, fades, and text overlays. Do not assume a synthetic on-camera
  host unless the production brief explicitly includes one.
- Keep critical visual content and captions out of platform UI safe areas.
  Create both sidecar captions and burned-in review captions when practical.
- Treat local TTS, generated visuals, stock assets, screen captures, and
  third-party media as provenance-sensitive inputs that need review.
- Verify current platform upload, disclosure, or encoding guidance from
  official sources when exact tactical requirements matter.

## Manifest Fields

Use a structured manifest when possible. Include:

- `episode_id`, `topic`, `audience`, `promise`, `target_length`, and
  `review_owner`
- `output_profile`: aspect ratio, resolution, frame rate, video codec, audio
  codec, caption mode, and destination path
- `assets`: source file, purpose, rights/provenance status, and missing-asset
  notes
- `scenes`: order, duration, visual asset, motion, voiceover segment, caption
  range, overlay text, and transition
- `audio`: narration file, music/SFX files, loudness target, ducking notes, and
  sync checks
- `validation`: expected streams, duration tolerance, caption checks, review
  result, and unresolved blockers

## Safety Rules

- Do not upload, publish, schedule, or mark a video approved. Hand off to
  `publishing-checklist` for pre-publish QA and keep final approval human-led.
- Do not fabricate source assets, rights, provenance, captions, transcripts,
  claims, sponsor approval, AI disclosure, or platform compliance.
- Hold the package when a source asset is missing, an audio or caption sync
  problem remains, a claim lacks review, or rights/provenance is unclear.
- Do not use private likenesses, distinctive voices, protected characters,
  copyrighted logos, or confidential source assets without explicit rights and
  review.

## Deliverable Shape

For local video assembly work, provide:

- Render manifest or manifest changes
- FFMPEG command plan or executed command summary
- Output files and paths, including `final.mp4` or a clearly named draft
- Caption files and burn-in status
- `ffprobe` validation summary
- Missing assets, sync issues, quality issues, and provenance notes
- `go`, `revise`, or `hold` recommendation for human review

## References

- Read `references/local-video-assembly-checklist.md` when creating a render
  manifest, planning FFMPEG commands, validating an export, or packaging a
  local narrated explainer for review.
