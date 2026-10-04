---
name: openrouter-text2music
description: Generate music (NOT speech) via OpenRouter using Google Lyria 3 Pro.
---

# openrouter-text2music

Text → music via OpenRouter. Default model: `google/lyria-3-pro-preview`.

**⚠️ This is a music-generation model, not TTS.** It produces 48kHz stereo audio with instrumentation, and can include vocals and timed lyrics based on the prompt. For narration/voiceover, use a dedicated TTS tool (e.g., OpenAI `tts-1`, ElevenLabs).

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

python3 TOOL_DIR/scripts/generate_music.py \
  --prompt "Driving synthwave, 120 BPM, nostalgic lead over a pulsing arpeggio, no vocals" \
  --download PROJECT_DIR/assets/bg_music.wav
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Text prompt (genre, mood, instruments, tempo, optional lyrics) |
| `--download` | required | Output audio file path |
| `--model` | `google/lyria-3-pro-preview` | Alt: `google/lyria-3-clip-preview` (shorter clips) |

## Pricing

- `lyria-3-pro-preview`: $0.08 per song

## Notes

- Request uses `POST /api/v1/chat/completions` with `modalities: ["audio","text"]`.
- Response parsing handles several shapes: `message.audio`, a content part with `type=audio`, or a `data:audio/...` URL embedded in the text content.
- Output format is typically WAV (48kHz stereo); the script saves whatever bytes the API returns — choose the extension to match.
