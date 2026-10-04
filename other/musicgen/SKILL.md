---
name: musicgen
description: "CLI wrapper for MusicGPT (AudioCraft MusicGen backend) — generates AI music from text prompts. Use for BGM generation in video production. Default model: small (fast, ~1 min for 10s clip on Apple Silicon)."
---

# musicgen

AI music generation from text prompts via MusicGPT. Backend uses Meta's AudioCraft MusicGen models, running fully locally (no API key needed, no network after first model download).

## Binary

```
~/.claude/tools/musicgpt/musicgpt
```

Version: 0.3.28
Model cache: `~/.local/share/musicgpt/` (auto-managed, downloaded on first run per model)

## Core Command

```bash
~/.claude/tools/musicgpt/musicgpt \
  "{prompt}" \
  --model small \
  --secs {duration} \
  --output {path}.wav \
  --no-playback \
  --no-interactive
```

## Prompt Template

Default BGM prompt for video production:

```
{mood} {genre} instrumental, {bpm} bpm, no vocals
```

Examples:
- `"calm ambient electronic instrumental, 90 bpm, no vocals"`
- `"upbeat corporate pop instrumental, 120 bpm, no vocals"`
- `"dark cinematic orchestral instrumental, 80 bpm, no vocals"`
- `"energetic hip-hop beat, 140 bpm, no vocals"`
- `"lo-fi chill background music, 75 bpm, no vocals"`

## Model Options

| Model | Size | RAM | Speed (10s clip on M-series) | Quality |
|---|---|---|---|---|
| small | ~300M params | ~2GB | ~60s | Good — default |
| medium | ~1.5B params | ~6GB | ~4 min | Better |
| large | ~3.3B params | ~12GB | ~15 min | Best |

Default: `small`. Use `medium` for final master tracks. Avoid `large` unless you have 16GB+ free RAM.

Note: `small-fp16`, `medium-fp16` are available but untested on Apple Silicon — default float32 is recommended.

## Duration Guidelines

| Use case | Duration | Notes |
|---|---|---|
| Short-form intro/outro | 5-15s | Loop if needed |
| Full video BGM | 30-90s | Generate full length, no seamless loop yet |
| YT long-form background | 60-120s | Use medium model for quality |

## Integration with Video Pipeline

**Default BGM source for any video needing original music:**
1. Generate with musicgpt using prompt template above
2. Normalize audio: `ffmpeg-normalize input.wav -o output.wav -c:a aac -b:a 192k --target-level -14`
3. Mix under VO using ffmpeg: `ffmpeg -i video.mp4 -i bgm.wav -filter_complex "[1:a]volume=0.15[bgm];[0:a][bgm]amix=inputs=2:duration=first" -c:v copy output.mp4`

**MoneyPrinterTurbo BGM replacement:**
Replace MPT's default BGM by generating a musicgpt track first, then passing the path to MPT's audio_file parameter. See colorist-audio-engineer agent for the full mastering chain.

## First Run

First run downloads:
1. ONNX runtime libraries (~25MB from GitHub)
2. Model weights (small: ~300MB, medium: ~1.5GB, large: ~3.3GB)

Subsequent runs use cached models — no network needed.

## Output

Always generates WAV (32000 Hz, mono). Convert to AAC/MP3 for embedding:

```bash
ffmpeg -i musicgpt-generated.wav -c:a aac -b:a 192k output.aac
```

## Known Limitations

- No seamless loop generation (use 30s+ clips for background music)
- Mono output (fine for BGM; stereo enhancement possible via ffmpeg `extrastereo` filter)
- Prompt adherence varies — iterate if first result doesn't match mood
- AudioCraft pip package fails on Python 3.14 (blis/spacy build issue) — MusicGPT binary is the correct install path
