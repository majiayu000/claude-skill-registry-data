---
name: subtitle-burner
description: Burned-in subtitle (open caption) workflow for short-form video. Produces karaoke-style word-highlight captions for TikTok/Reels/Shorts. Uses Whisper for transcription + ffmpeg for styled caption burn. No Docker required.
---

# subtitle-burner

Burned-in styled captions for short-form video (TikTok, Instagram Reels, YouTube Shorts — 9:16 vertical).

## Note on Original Tool

The original `jurczykpawel/subtitle-burner` GitHub repo has been renamed and merged into `jurczykpawel/reelstack` — a full video pipeline app requiring Docker + Postgres + Redis + multiple API keys. That tool is too heavy for caption-only use.

**Our implementation** achieves the same karaoke-style caption output using two widely available tools: OpenAI Whisper (CLI) + ffmpeg. Neither requires Docker, Postgres, Redis, or API keys.

## Stack

- Transcription: `whisper` CLI (OpenAI Whisper). Detect the install with `command -v whisper` — the exact path varies by platform and package manager (Homebrew, pip, apt, etc.), so don't hardcode it. If `command -v whisper` returns nothing, install with `pip install -U openai-whisper` or `brew install openai-whisper`.
- Caption burn: `ffmpeg` with ASS subtitle filter for styled open captions. Any recent ffmpeg (4.x+) supports the `subtitles`/`ass` filters used below — no specific version is required.
- Alternative: `video-use` Whisper transcription for pipeline integration

## Short-Form Workflow (TikTok / Reels / Shorts — 9:16)

### Step 1: Transcribe to SRT

```bash
whisper input.mp4 \
  --model base \
  --output_format srt \
  --output_dir /tmp/captions/ \
  --language en
```

Output: `/tmp/captions/input.srt`

For better accuracy on AI/technical content:
```bash
whisper input.mp4 --model medium --output_format srt --output_dir /tmp/captions/
```

### Step 2: Burn Captions (short-form style)

**Standard short-form (bold white + black outline, bottom-third):**

```bash
ffmpeg -i input.mp4 \
  -vf "subtitles=/tmp/captions/input.srt:force_style='FontName=Arial,Bold=1,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=60'" \
  -c:v libx264 -crf 20 -c:a copy \
  output_captioned.mp4
```

**Karaoke-style (word highlight — requires ASS format):**

1. Convert SRT to ASS first:
```bash
ffmpeg -i /tmp/captions/input.srt /tmp/captions/input.ass
```

2. Edit the ASS file's `[Script Info]` style to add karaoke tags (each word highlighted in yellow):
```
Style: Default,Arial,18,&H00FFFF00,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,60,0
```

3. Burn:
```bash
ffmpeg -i input.mp4 \
  -vf "ass=/tmp/captions/input.ass" \
  -c:v libx264 -crf 20 -c:a copy \
  output_captioned_karaoke.mp4
```

### Caption Style Standards (Short-Form)

| Property | Value |
|---|---|
| Font | Arial Bold |
| Font size | 18-22 (ASS units, scales to ~6% of frame height) |
| Text color | White (#FFFFFF) |
| Outline | Black, 2px |
| Alignment | Bottom center (Alignment=2) |
| Margin V | 60px from bottom |
| Max chars/line | 42 |
| Max lines | 2 |

## Long-Form Workflow (YouTube — 16:9)

Long-form: use Whisper for transcription → export .srt → upload to YouTube as closed captions (do NOT burn in for horizontal video — YouTube's auto-CC is better for SEO).

```bash
whisper input.mp4 --model medium --output_format srt --output_dir ./captions/
# Upload ./captions/input.srt to YouTube Studio manually or via API
```

## Integration with Captioning Specialist Agent

The `vs-captioning-specialist.md` agent now defaults to this workflow. For short-form:
1. Whisper transcription (base model for speed, medium for quality)
2. Manual correction of proper nouns, brand names, technical terms
3. ffmpeg burn with short-form style above
4. Output: captioned MP4 + source .srt file

## When to Use vs. Alternatives

| Scenario | Tool | Reason |
|---|---|---|
| Short-form vertical 9:16 (TikTok/Reels) | This skill (Whisper + ffmpeg) | Fast, offline, no API cost |
| YouTube long-form | Whisper → .srt upload | Don't burn in, use YT's CC system |
| Live video / broadcast | Whisper real-time | Out of scope for this skill |
| Vietnamese content | video-use + vietnamese-language agent | Specialized pipeline |

## Follow-Up Needed (operator action)

The ReelStack hosted demo at `https://reelstack.techskills.academy` includes a karaoke mode. Worth checking once for comparison. No install required — just upload a video.
