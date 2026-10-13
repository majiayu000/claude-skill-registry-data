---
name: coze-voice-gen
description: Text-to-Speech (TTS) and Speech-to-Text (ASR) using coze-coding-dev-sdk. Returns results directly to stdout.
homepage: https://www.coze.com
metadata: { "openclaw": { "emoji": "🎙️", "requires": { "bins": ["npx"] } } }
---

# Coze Voice Generation

Text-to-Speech (TTS) and Automatic Speech Recognition (ASR) using coze-coding-dev-sdk.

## Text-to-Speech (TTS)

### Single Audio

```bash
npx ts-node {baseDir}/scripts/tts.ts --text "Hello, welcome to our service!"
```

### With Different Voice

```bash
npx ts-node {baseDir}/scripts/tts.ts \
  --text "This is a male voice" \
  --speaker zh_male_m191_uranus_bigtts
```

### Batch Generation

```bash
npx ts-node {baseDir}/scripts/tts.ts \
  --texts "Chapter 1: Introduction" "Chapter 2: Getting Started" "Chapter 3: Advanced Topics" \
  --speaker zh_female_xueayi_saturn_bigtts
```

### With Custom Parameters

```bash
npx ts-node {baseDir}/scripts/tts.ts \
  --text "Fast and loud announcement!" \
  --speech-rate 30 \
  --loudness-rate 20 \
  --format mp3 \
  --sample-rate 48000
```

## TTS Options

| Option               | Description                                        |
| -------------------- | -------------------------------------------------- |
| `--text <text>`      | Single text to synthesize                          |
| `--texts <texts...>` | Multiple texts for batch generation                |
| `--speaker <id>`     | Voice ID (default: zh_female_xiaohe_uranus_bigtts) |
| `--format <fmt>`     | mp3, pcm, ogg_opus (default: mp3)                  |
| `--sample-rate <hz>`  | 8000-48000 (default: 24000)                        |
| `--speech-rate <n>`   | -50 to 100 (default: 0)                            |
| `--loudness-rate <n>` | -50 to 100 (default: 0)                            |

## TTS Output

The script outputs audio URLs directly to stdout:

```
[1/1] Hello, welcome to our service!
  https://example.com/generated-audio.mp3
```

## Available Voices

**General Purpose:**

- `zh_female_xiaohe_uranus_bigtts` - Xiaohe (default)
- `zh_female_vv_uranus_bigtts` - Vivi (Chinese & English)
- `zh_male_m191_uranus_bigtts` - Yunzhou (male)
- `zh_male_taocheng_uranus_bigtts` - Xiaotian (male)

**Audiobook:**

- `zh_female_xueayi_saturn_bigtts` - Children's audiobook

**Video Dubbing:**

- `zh_male_dayi_saturn_bigtts` - Dayi (male)
- `zh_female_mizai_saturn_bigtts` - Mizai (female)
- `zh_female_jitangnv_saturn_bigtts` - Motivational female

**Role Playing:**

- `saturn_zh_female_keainvsheng_tob` - Cute girl
- `saturn_zh_male_shuanglangshaonian_tob` - Cheerful boy

## Speech-to-Text (ASR)

### From URL

```bash
npx ts-node {baseDir}/scripts/asr.ts --url "https://example.com/audio.mp3"
```

### From Local File

```bash
npx ts-node {baseDir}/scripts/asr.ts --file ./recording.mp3
```

## ASR Options

| Option          | Description           |
| --------------- | --------------------- |
| `--url <url>`   | Audio file URL        |
| `--file <path>` | Local audio file path |

## ASR Output

Transcription is printed directly to stdout:

```
============================================================
TRANSCRIPTION
============================================================
Hello, this is the transcribed text from the audio file...
============================================================

Duration: 1m 30s
Segments: 5
```

## ASR Requirements

- Duration: ≤ 2 hours
- File size: ≤ 100MB
- Formats: WAV, MP3, OGG OPUS, M4A

## Notes

- Audio URLs have valid expiration - use directly when possible
- Speech rate: negative = slower, positive = faster
- Loudness rate: negative = quieter, positive = louder
