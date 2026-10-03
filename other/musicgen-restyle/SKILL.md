---
name: musicgen-restyle
description: Change a song's style using Facebook AudioCraft MusicGen-Style + stem separation. Separates vocals from the original, generates new instrumental in the target style, then mixes vocals back. Use when the user wants to restyle a song with Audiocraft instead of ACE-Step.
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg, yt-dlp]
  paths: [~/src/audiocraft, ~/src/audio-separator]
metadata:
  hermes:
    tags: [music, restyle, style-transfer, audiocraft, musicgen, musicgen-style, audio, gpu, rocm]
    related_skills: [create-music, restyle-music]
---

# MusicGen-Style Restyle — change a song's style (AudioCraft MusicGen-Style)

Take an **existing audio file** + a **target style description** and re-render the instrumental in that style while keeping the original vocals, via Facebook's AudioCraft MusicGen-Style on the local AMD GPU (ROCm 7.2, gfx1151).

## When to use

- "Restyle this song in another style" / "change the genre of this song"
- "Convert this to lofi / orchestral / jazz / rock / and more"
- User wants to use **AudioCraft** specifically (not ACE-Step)

## Pipeline

```
Original Song
    │
    ├──► [Step 1] Separate → Vocals + Instrumental (UVR-MDX-NET, GPU)
    │
    ├──► [Step 2] Instrumental + Style Description ──► MusicGen-Style ──► New Instrumental
    │
    └──► [Step 3] Original Vocals + New Instrumental ──► Final Mix
```

1. **Separate** vocals and instrumental using `audio-separator` (UVR-MDX-NET, GPU via ROCm)
2. **Generate** new instrumental: pass the original instrumental as style reference to MusicGen-Style, with a text description of the target style
3. **Mix** original vocals back over the generated instrumental with gain control

## Building the `-s` caption — research the genre FIRST

Users usually give a **short genre name** ("和樂器 band", "city pop", "phonk", "Hardstyle"), not a full description. **Do not write the caption from memory** — first look the genre up.

**Workflow:**
1. **Take the user's requested style** (a genre name, an artist/band, a vibe).
2. **Web-search it** — e.g. `"<genre> instruments musical style"` — to find its **defining instruments, typical arrangement, tempo/mood, and what it deliberately avoids**.
3. **Compose the `-s` caption** from those findings.

### Caption format — how to write `-s` correctly

**The `-s` caption MUST be a descriptive paragraph.** Never just comma-separate tags.
Write it as a **descriptive paragraph** using this four-part structure:

```
[1. Big genre label] + [2. Specific instruments/arrangement] + [3. Mood/atmosphere/scene] + [4. Exclusions]
```

**Hard rules:**
- **Write the caption in English.** MusicGen's text encoder is English-centric.
- **Keep it under ~512 chars** (longer is truncated).
- **Describe an instrumental style** (no vocal descriptions) since we're keeping the original vocals.

### ✅ vs ❌ examples

```bash
# ❌ BAD — tag soup
-s "lofi jazz, chill, mellow, piano, beats, instrumental"

# ✅ GOOD — descriptive paragraph
-s "lofi jazz: mellow Rhodes electric piano over a relaxed hip-hop drum beat with brushed snare, upright bass walking the root notes, warm vinyl crackle texture, relaxed and contemplative mood for late-night study sessions. No heavy bass, no synth leads, no fast tempo."
```

## Quick start (one-shot)

```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i ./input_song.mp3 \
  -s "lofi jazz: mellow Rhodes electric piano over relaxed hip-hop drums with brushed snare and upright bass, warm and contemplative mood for late-night listening. No heavy bass, no synth leads." \
  -o ./restyled_ac.mp3
```

## Options

| Option | Flag | Default | Description |
|--------|------|---------|-------------|
| Input | `-i` | (required) | Audio file (mp3/wav/flac) or URL (YouTube etc.) |
| Style | `-s` | (required) | Target style description in English (see caption format above) |
| Output | `-o` | `./restyled_ac.mp3` | Output path |
| Duration | `-d` | `15` | Duration in seconds (max 30 — MusicGen-Style limit) |
| CFG | `-c` | `3.0` | CFG coefficient (higher = more adherence to text prompt) |
| Top-k | `-t` | `250` | Top-k sampling |
| Temperature | `-T` | `1.0` | Sampling temperature (higher = more creative/varied) |
| Excerpt | `-x` | `3.0` | Length of style reference excerpt (max 4.5s) |
| Vocal gain | `-V` | `1.0` | Vocal gain in final mix |
| Music gain | `-M` | `1.5` | Music/instrumental gain in final mix |
| Loudness | `-N` | `-13` | Target LUFS for final mix |
| Sep dir | `-s` | `~/src/audio-separator` | Audio-separator directory |
| Verbose | `-v` | off | Enable debug logging |

## Tuning guide

| If the user wants to… | Use | How |
|---|---|---|
| **Change the genre/instrumentation** | `-s "…"` | The core control. Write a full descriptive paragraph. |
| **More style change / "it still sounds like the original"** | `-c` ↓ | Lower CFG (e.g. `-c 2.0`) for more freedom |
| **Less style change / "it drifted too far"** | `-c` ↑ | Raise CFG (e.g. `-c 5.0`) for stronger text adherence |
| **More creative / varied generation** | `-T` ↑ | Higher temperature (e.g. `-T 1.5`) |
| **More deterministic / consistent** | `-T` ↓ | Lower temperature (e.g. `-T 0.7`) |
| **Longer output** | `-d` ↑ | Up to 30 seconds max (MusicGen-Style limit) |
| **Better style reference** | `-x` ↑ | Longer excerpt (up to 4.5s) captures more style info |
| **Louder instrumental** | `-M` ↑ | Higher music gain (e.g. `-M 2.0`) |
| **Louder vocals** | `-V` ↑ | Higher vocal gain (e.g. `-V 1.3`) |
| **Faster generation** | `-T` ↓ or `-t` ↓ | Lower temperature and top-k |
| **Lossless output** | `-o name.wav` | `.wav`/`.flac` = lossless (may exceed 25MB) |

## Performance & hardware

- Runs on AMD GPU (Radeon 8060S, 96GB GTT, ROCm 7.2)
- Model: `facebook/musicgen-style` (1.5B parameters)
- A ~15s song: model load ~30–60s + generation ~20–40s (depends on GPU utilization)
- VRAM usage: ~8GB for the model + ~2GB for stems separation = ~10GB total

## Notes / gotchas

- **Duration limit:** MusicGen-Style max is 30 seconds per generation. Use `-d 30` for full tracks, or `-d 15` for shorter clips.
- **Style reference length:** The `-x` excerpt should be 1.5–4.5 seconds. Too short loses style info; too long exceeds the model's training window.
- **Output sample rate:** Final mix is 48kHz stereo. Original model runs at 32kHz internally.
- **Vocals separation quality:** UVR-MDX-NET is generally good but imperfect — faint backing instrument leakage may remain in the vocal stem. This is normal.
- **Model loading:** The model downloads from HuggingFace on first run. Subsequent runs use cached models.
- **No `generate_with_style`:** This version uses `generate_with_chroma()` with the instrumental as the style reference (self_wav conditioner). This is the correct API for MusicGen-Style.
- **ROCm environment:** The script automatically sets `PYTORCH_HIP_ALLOC_CONF=expandable_segments:True` and `MIOPEN_FIND_MODE=FAST` for this box.
- **Language:** Always write the `-s` caption in English for best results. Native-script genre names in parentheses are fine (e.g., `(和樂器)`) but keep the description in English.

## Comparison with ACE-Step restyle (`restyle-music` skill)

| Feature | ACE-Step (restyle-music) | MusicGen-Style (musicgen-restyle) |
|---------|--------------------------|-----------------------------------|
| Style transfer quality | Good for obvious genre swaps | Better for nuanced style understanding |
| Duration | Full song (no hard limit) | Max 30s per generation |
| Vocal preservation | Via `-k` flag (same pipeline) | Always preserves original vocals |
| Model size | 0.6B + DiT turbo | 1.5B |
| GPU memory | ~21GB | ~10GB |
| Generation speed | ~65s (turbo) | ~20-40s (faster) |
| Best for | Long songs, aggressive style change | Shorter clips, nuanced style transfer |

Use `restyle-music` (ACE-Step) for full-length songs. Use `musicgen-restyle` (AudioCraft) when you want faster generation or better style understanding.

## Examples

### Lofi jazz
```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i song.mp3 \
  -s "lofi jazz: mellow Rhodes electric piano over relaxed hip-hop drums with brushed snare, warm vinyl crackle texture, chill and contemplative mood. No heavy bass, no synth leads." \
  -o lofi.mp3
```

### Traditional Japanese (和樂器)
```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i song.mp3 \
  -s "Traditional Japanese wagaku (和樂器) arrangement: plucked shamisen and koto, breathy shakuhachi bamboo flute, deep taiko drums, elegant ceremonial feel with pentatonic folk atmosphere, acoustic and organic. No electric guitar, no synthesizer." \
  -o wagaku.mp3
```

### City Pop
```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i song.mp3 \
  -s "80s Japanese city pop: bright electric guitar with clean chorus, syncopated bass line, tight drum machine with gated reverb snare, smooth Fender Rhodes keys, upbeat summer night drive vibe with neon city atmosphere. No heavy metal, no acoustic folk." \
  -o citypop.mp3
```

### Orchestral
```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i song.mp3 \
  -s "Cinematic orchestral arrangement: sweeping string sections with violins and cellos, French horn melodies, timpani rolls, grand brass fanfares, dramatic and emotional mood like a movie soundtrack. No electronic beats, no synthesizers." \
  -o orchestral.mp3
```

### From YouTube
```bash
~/.pi/agent/skills/media/musicgen-restyle/restyle_music_ac.sh \
  -i "https://youtu.be/XXXXXXXXXXX" \
  -s "lofi jazz: mellow Rhodes piano over relaxed hip-hop drums, warm and contemplative mood. No heavy bass." \
  -o restyled.mp3
```
