---
name: OpenAI Whisper
description: Transcribe audio files (≤25 MB) to text via OpenAI-compatible Whisper API.
requires:
  bins: []
  env:
    - WHISPER_OPENAI_API_KEY
---

# OpenAI Whisper

Use this skill to transcribe audio files into text. Backed by the
`openai-whisper` extension which calls any OpenAI-compatible
`/audio/transcriptions` endpoint (OpenAI, Groq, local whisper.cpp).

## Use when

- "Transcribe this audio"
- "Convert this voice note to text"
- "Get subtitles from this recording"
- User attaches `.mp3`, `.wav`, `.m4a`, `.webm`, `.ogg` and wants the text

## Do not use when

- Text-to-speech (TTS) — different skill / extension
- Real-time streaming transcription — this is batch only
- Speaker diarization with strict attribution — Whisper does not separate speakers reliably
- Audio > 25 MB — split or compress (downsample to 16 kHz mono) before calling

## Tools

### `status`
No arguments. Returns endpoint, default model, token presence, max file size.

### `transcribe_file`
- `file_path` (string, required) — absolute or relative path, ≤ 25 MB
- `model` (string, optional) — override default (`whisper-1`, `whisper-large-v3`, etc.)
- `language` (string, optional) — ISO 639-1 hint (`en`, `es`, `pt`); improves accuracy
- `prompt` (string, optional) — biases vocabulary/style; useful for technical terms or names
- `response_format` (string, optional) — `text` (default) | `json` | `verbose_json` (with segments+timestamps) | `srt` | `vtt`
- `temperature` (number, optional, 0..1) — 0 for deterministic

Returns `{file_path, bytes, model, language, response_format, transcript: {text, ...}}`.

## Execution guidance

- Default `response_format: "text"` for plain transcripts.
- Use `verbose_json` when the user needs timestamps or segment data (subtitles, alignment, search).
- Use `srt` / `vtt` when the user explicitly wants subtitle files.
- Always pass `language` if the audio language is known — accuracy improves significantly.
- Use `prompt` to feed proper nouns, jargon, or expected style ("Bible reading", "casual Spanish", "medical interview").
- If `-32014` (payload too large) → ask user to compress audio (`ffmpeg -i in.mp3 -ac 1 -ar 16000 out.mp3`).
- If `-32015` (unsupported media) → file format unsupported by provider; convert to `mp3`/`wav`.
- If `-32011` (unauthorized) → `WHISPER_OPENAI_API_KEY` missing or invalid.
