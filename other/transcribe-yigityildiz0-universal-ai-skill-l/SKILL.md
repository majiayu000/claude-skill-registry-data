---
name: transcribe
description: Transcribe audio or video with an already configured local or approved speech-to-text capability, selecting current supported options from evidence at run.
license: MIT
---

# Transcription

## Inspect and scope

Record file type, duration, channels, sample rate, language(s), speaker count, noise/music, privacy, desired timestamps, diarization, speaker names, verbatim versus cleaned style, and output format. Preserve the original.

## Choose an available path

Use an installed local engine or an already approved/configured API. Verify current supported model IDs, size/duration limits, diarization, prompting, timestamp, and language behavior from installed/current official documentation. Do not hard-code a model, silently upload audio, install dependencies, or spend credits.

For sensitive recordings, prefer local processing. Named-speaker references require consent and must be stored/removed intentionally. Do not infer speaker identity from voice alone.

## Process

- Normalize/convert audio losslessly enough for speech recognition and keep channel information when it helps speaker separation.
- Chunk long files on silence/overlap boundaries and retain source offsets.
- Preserve uncertainty with markers rather than inventing words.
- Use a glossary for verified names/terms; do not let a prompt override the audio.
- Keep raw, timestamped, and cleaned transcripts separate. Cleaning may fix punctuation/fillers but must not alter facts.

## Validate

Spot-check the start, middle, end, speaker transitions, low-confidence segments, names, numbers, dates, negations, and domain terms against audio. Check caption timing/line length when producing SRT/VTT. For important work, report word/error uncertainty or a reviewed-segment list.

## Deliverable

Return output paths, engine/provider and configuration source, language, timestamps/diarization choices, coverage, low-confidence markers, whether audio left the device, and deletion/retention status of temporary files.
