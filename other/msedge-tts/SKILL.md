---
name: Microsoft Edge TTS
description: Synthesize text to speech using Microsoft Edge Read Aloud voices (no API key).
requires:
  bins: []
  env: []
---

# Microsoft Edge TTS

Use this skill to convert text into spoken audio. Backed by the `msedge-tts`
extension which uses the free Microsoft Edge Read Aloud backend via the
`msedge_tts` crate — no API key required.

## Use when

- "Read this aloud" / "say this out loud"
- "Generate audio from this text"
- "Make a voice note that says ..."
- User wants an MP3/WAV of spoken text

## Do not use when

- Speech-to-text (transcription) — use `openai-whisper`
- Real-time streaming TTS with low latency — this writes a file after full synthesis
- Cloned / custom voices — only the public Edge voice catalog is available

## Tools

- `status` — returns defaults (voice, audio format, output dir)
- `list_voices` — list Edge voices; supports `query` substring filter and `limit`
- `synthesize` — write an audio file from `text`; optional `voice`, `audio_format`,
  `rate`, `pitch`, `volume`, `output_path`

Default voice: `en-US-EmmaMultilingualNeural`.
Default format: `audio-24khz-48kbitrate-mono-mp3`.
Default output dir: `$TMPDIR/agent-msedge-tts/speech-<timestamp>.mp3`.

## Typical flow

1. `list_voices` with a language query (e.g. `"es-"`, `"en-US"`, `"multilingual"`)
   to pick a voice.
2. `synthesize` with `text` and the chosen `voice`. Grab `output_path` from the
   response to send or play the audio.

## Notes

- `rate`, `pitch`, `volume` are provider-native integer adjustments (0 = neutral).
- File extension is inferred from `audio_format` (mp3 / wav / webm / ogg / opus / amr).
- Empty `text` is rejected.
