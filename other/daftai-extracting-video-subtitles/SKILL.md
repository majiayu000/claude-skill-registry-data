---
name: daftai-extracting-video-subtitles
description: >
  Extracts timed subtitles from local video/audio files using Whisper.
  Outputs SRT format with accurate timestamps. Handles complex filenames automatically.
  Use when user asks to "extract subtitles", "get subtitles", "transcribe video",
  "识别字幕", "提取字幕", or "获取字幕".
---

# Video Subtitle Extractor

Extract timed subtitles (SRT) from local video/audio files using OpenAI Whisper.

> **Scripts**: All scripts are in `scripts/` relative to this SKILL.md.

## Workflow

```
- [ ] Step 1: Environment check (Whisper + FFmpeg)
- [ ] Step 2: Input validation (file exists, has audio stream)
- [ ] Step 3: Detect language (auto or user-specified)
- [ ] Step 4: Run extraction script
- [ ] Step 5: Verify output and report
```

---

### Step 1: Environment Check

```bash
which whisper
which ffprobe
```

| Result | Action |
|--------|--------|
| whisper found | Continue |
| whisper missing | `brew install openai-whisper` (macOS) or `pip install openai-whisper` |
| ffprobe missing | `brew install ffmpeg` |

---

### Step 2: Input Validation

1. Confirm video/audio file exists
2. Get duration and confirm audio stream present — handled by script automatically

---

### Step 3: Language Detection

- If user specifies language → use it
- If unclear → ask user, suggest `en` or `zh` as common options
- Whisper `--language` flag values: `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`, etc.

---

### Step 4: Run Extraction

```bash
bun scripts/extract_subtitles.ts "<video_path>" [language] [model]
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| video_path | (required) | Input video/audio file |
| language | `en` | Language code |
| model | auto by duration | Whisper model |

**Model auto-selection (by duration):**

| Video duration | Model | Approx. speed (CPU) |
|---------------|-------|---------------------|
| < 2 min | medium | ~2-3 min |
| 2-30 min | turbo | ~1x duration |
| > 30 min | base | fastest |

**The script automatically handles:**
- Complex filenames (copies to temp dir)
- Audio stream validation
- Duration detection and model selection
- Temp file cleanup

**Known issues:**

| Issue | Solution |
|-------|----------|
| `FP16 not supported on CPU` warning | Normal on Mac CPU, auto falls back to FP32 |
| MPS NaN errors | Do NOT use `--device mps`, script uses CPU |

---

### Step 5: Verify & Report

Script automatically reports:
- Output SRT file path
- Number of subtitle entries
- Processing time

---

## Examples

**Basic extraction:**
```
User: 帮我提取这个视频的字幕
→ bun scripts/extract_subtitles.ts "video.mp4" en
```

**With language specified:**
```
User: Extract English subtitles from this video
→ bun scripts/extract_subtitles.ts "video.mp4" en
```

**Chinese video:**
```
User: 提取中文字幕
→ bun scripts/extract_subtitles.ts "video.mp4" zh
```

**Long video with specific model:**
```
User: 提取这个一小时视频的字幕
→ bun scripts/extract_subtitles.ts "video.mp4" en base
```
