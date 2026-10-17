---
name: audio-transcription
description: Transcribe inbound audio clips to text using local Whisper (faster-whisper). Use when the user sends voice notes/audio files and asks what was said, asks for transcript/summary/action items, or asks to process audio privately on-host. Default model is small.en for better English accuracy on constrained hosts.
---

# Audio Transcription (Local, small.en)

Use local transcription by default with `small.en`.

## Default command

```bash
python3 skills/audio-transcription/scripts/transcribe_local.py \
  --input "<audio-path>" \
  --model small.en
```

## Fast/lower-resource fallback

```bash
python3 skills/audio-transcription/scripts/transcribe_local.py \
  --input "<audio-path>" \
  --model base.en
```

## What to return to user

1. Transcript (verbatim best-effort)
2. Short summary (2-4 bullets)
3. Action items/questions extracted from transcript
4. If confidence seems low, say so clearly

## Notes

- First run downloads model weights (~500MB for `small.en`).
- Keep transcripts concise in chat; offer full dump on request.
- Treat audio content as sensitive by default; do not share externally.
