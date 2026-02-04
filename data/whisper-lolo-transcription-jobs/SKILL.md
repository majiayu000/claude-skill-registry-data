---
name: whisper-lolo-transcription-jobs
description: Implement or adjust background transcription jobs for whisper-lolo. Use when wiring Inngest events, handling long-running jobs, chunking before transcription, persisting transcripts, or maintaining the TranscriptionProvider abstraction.
---

# Whisper Lolo Transcription Jobs

## Overview
Run transcription asynchronously with Inngest, storing results in Postgres, and keep a provider abstraction for Whisper now and Voxtral later.

## Job workflow
1) Emit `recording.uploaded` after successful Blob upload.
2) In Inngest, start `transcribeRecording` on that event.
3) Download audio from `blob_url`.
4) Chunk before transcription to fit provider limits.
5) Call the provider (Whisper now) and store text + segments.
6) Update statuses and handle errors with retries.

## Provider abstraction
- Maintain a `TranscriptionProvider` interface with `transcribe(audioUrl)`.
- Implement `WhisperProvider` now; leave `VoxtralProvider` stubbed.
- Avoid provider-specific logic in job orchestration.

## Status discipline
- `recordings.status`: uploaded -> transcribing -> done/error.
- `transcriptions.status`: pending -> done/error.
- Persist timestamps for observability where possible.

## Error handling
- Log failures with enough context to retry safely.
- Avoid duplicate transcription on retry (idempotency checks).

## References to consult
- `documentation/inngest-background-jobs.md`
- `documentation/inngest-demo-nextjs-full-stack.md`
- `documentation/openai-node-audio-example.md`
- `documentation/openai-speech-to-text.md`
- `documentation/openai-audio-api-reference.md`
