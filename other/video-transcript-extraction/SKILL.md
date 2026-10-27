---
name: video-transcript-extraction
description: >-
  How do I get the transcript of this video? Platform-aware extraction for any
  video source — YouTube, local files, or other platforms. Use when (1) need to
  transcribe a video for analysis, (2) user provides a video URL, (3) building
  a knowledge base from video content. Provides multiple methods with guided
  fallback chain (captions > Whisper > web services). Does NOT trigger for:
  watching videos, video editing, or non-transcript tasks.
---

# Video Transcript Extraction

**Seed question:** *How do I get the transcript of this video?*

Extract text transcripts from any video source. Platform-aware — detects what tools are available and guides to the best method.

## Setup Check

Before extracting, determine available tools:

| Tool | Check | Best For |
|------|-------|----------|
| `youtube-transcript-api` | `pip show youtube-transcript-api` | YouTube caption extraction (fastest) |
| MLX-Whisper MCP | Check `.mcp.json` for `mlx-whisper` | Apple Silicon local transcription (any video) |
| Whisper-cpp MCP | Check `.mcp.json` for `whisper-cpp` | Cross-platform local transcription |

Guide user to install what's missing for their platform if needed.

## Determine Source and Method

```
1. YouTube URL?
   → Method A: Caption extraction (youtube-transcript-api)
   → Fallback: Whisper if no captions available

2. Other video URL?
   → Check if platform provides captions
   → Fallback: Whisper transcription

3. Local video/audio file?
   → Method C: Whisper directly
   → Apple Silicon: MLX-Whisper (faster)
   → Other: Whisper-cpp
```

## Method A: YouTube Caption Extraction (Primary for YouTube)

### CLI
```bash
youtube_transcript_api VIDEO_ID
youtube_transcript_api VIDEO_ID --languages en es
youtube_transcript_api VIDEO_ID --json > transcript.json
```

### Python
```python
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript("VIDEO_ID")
text_only = " ".join([t['text'] for t in transcript])

# List available languages
transcript_list = YouTubeTranscriptApi.list_transcripts("VIDEO_ID")
```

### Bulk Processing
```bash
for vid in VIDEO_ID_1 VIDEO_ID_2 VIDEO_ID_3; do
  youtube_transcript_api "$vid" --json > "transcripts/${vid}.json"
  sleep 2
done
```

## Method B: Whisper Transcription (Any Video)

### MLX-Whisper (Apple Silicon)
```
mcp__mlx-whisper__transcribe_youtube(
  url="VIDEO_URL",
  language="en",
  task="transcribe",
  keep_file=true
)
```

### Whisper-cpp (Cross-platform)
```
mcp__whisper-cpp__transcribe(
  file_path="/path/to/video.mp4",
  language="en"
)
```

## Method C: Web Services (No Setup Required)

| Service | URL | Notes |
|---------|-----|-------|
| YouTubeToTranscript | youtubetotranscript.com | Manual, unlimited |
| YouTube-Transcript.io | youtube-transcript.io | 5 req/10s |
| YouTube built-in | Click "..." > "Show transcript" | Manual only |

## Extraction Workflow

```
1. CHECK: Does video have existing captions?
   → Try youtube-transcript-api first (fastest, zero compute)
   → Check language availability

2. IF NO CAPTIONS: Use Whisper
   → Apple Silicon: MLX-Whisper MCP
   → Other: Whisper-cpp MCP

3. IF TOOLS UNAVAILABLE: Web services
   → youtubetotranscript.com
   → Manual from YouTube UI

4. PROCESS: Clean transcript
   → Remove timestamps if not needed (saves tokens)
   → Save to file for downstream analysis
```

## Token Optimization

Transcripts can be long. Strategies:

- **Remove timestamps:** `" ".join([t['text'] for t in transcript])` — saves ~30% tokens
- **Chunk processing:** Split into 10K character chunks for analysis
- **Summarize first:** Quick summary pass before deep analysis
- **Consolidated output:** For 5+ videos, create `all_transcripts.md` with `---` separators

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Transcripts disabled" | Use Whisper transcription (Method B) |
| "Language not available" | Try auto-generated captions, or Whisper with `task="translate"` |
| "Rate limited" | Add delays between requests |
| "MCP not connected" | Restart Claude Code, check `.mcp.json` |
| "Long video truncation" | Use Whisper (no length limit) or chunk processing |

## Budget Mode

**Activation (any of these):**
1. Explicit flag: `--budget` or `-b`
2. Auto-detect: If `budget-mode` skill is active in session
3. Inherited: If calling skill passed budget context

**When active:**
- Prefer caption extraction over Whisper (lower compute cost)
- Skip timestamp inclusion by default
- Output text-only (no structured JSON)

**Note:** After context compaction, auto-detection may fail. Re-invoke `budget-mode` skill or pass `--budget` explicitly.

## Cross-References

- **Called by:** youtube-research (Phase 2)
- **Standalone:** Invoke directly for any video transcription need
- **Downstream:** Extracted transcripts feed into youtube-research analysis or DIP investigations requiring video source material

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
