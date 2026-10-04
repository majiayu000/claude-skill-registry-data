---
name: openrouter-text2music
description: Generate atmospheric sound-design / SFX (NOT speech, NOT the front-of-blog BGM) via OpenRouter using Google Lyria 3 Pro.
---

# openrouter-text2music

Text → audio via OpenRouter. Default model: `google/lyria-3-pro-preview`.

**Role in Data2Story: atmospheric sound-design / SFX only — never the front BGM.** Use this for a sound the story needs that has NO findable real recording: an ambient bed (tension drone, texture, room tone) or best-effort sharp foley (e.g. a glass-shatter texture). Lyria's strength is ambient/textural beds, not crisp transients, so sharp foley is best-effort. The result is an opt-in, event/section-bound, reader-controlled element. **The front-of-blog BGM must be a SOURCED real track (sourced_bgm via the Scout) — never generated here.**

**⚠️ This is a generative audio model, not TTS.** It produces 48kHz stereo audio; for narration/voiceover use a dedicated TTS tool (e.g., OpenAI `tts-1`, ElevenLabs).

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

python3 TOOL_DIR/scripts/generate_music.py \
  --prompt "Low rumbling tension drone, sub-bass swell, no melody, slowly building unease" \
  --download PROJECT_DIR/assets/sfx_drone.wav
```

## SFX prompting

Describe a TEXTURE, not a song — no genre/BPM/lead/vocals. Examples:

- `"low rumbling tension drone, sub-bass swell, no melody"`
- `"sharp glass-shatter texture, brittle high transients"` (foley — best-effort)
- `"distant wind and creaking-ice ambience, cold and hollow"`

## Flags

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Text prompt — describe the atmospheric texture / SFX (mood, materials, motion); avoid song structure |
| `--download` | required | Output audio file path |
| `--model` | `google/lyria-3-pro-preview` | Alt: `google/lyria-3-clip-preview` (shorter clips) |

## Pricing

- `lyria-3-pro-preview`: $0.08 per call

## Notes

- Request uses `POST /api/v1/chat/completions` with `modalities: ["audio","text"]`.
- Response parsing handles several shapes: `message.audio`, a content part with `type=audio`, or a `data:audio/...` URL embedded in the text content.
- Output format is typically WAV (48kHz stereo); the script saves whatever bytes the API returns — choose the extension to match.
