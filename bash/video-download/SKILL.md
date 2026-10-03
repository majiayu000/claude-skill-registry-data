---
name: video-download
description: >
  Downloads videos from YouTube, TikTok, Douyin, Bilibili, Instagram, XiaoHongShu and 1000+ platforms.
  Primary: yt-dlp. Fallback: agent-browser + GreenVideo for Douyin/TikTok when yt-dlp fails.
  Use when user says "download video", "save video", "grab video", "watermark-free download",
  or pastes a video URL. Do NOT use for AI video generation or video editing.
allowed-tools: Bash
metadata:
  author: renoise
  version: 0.3.0
  category: utility
  tags: [download, youtube, tiktok, douyin, yt-dlp, greenvideo]
---

# Video Download

Download videos from YouTube, TikTok, and other platforms to local MP4 files.
Handles format selection, platform-prefixed dedup, TikTok cookie fallback,
and Douyin/TikTok browser-based fallback automatically.

## Quick Start

```bash
# Download any video
bash ${CLAUDE_SKILL_DIR}/scripts/download-video.sh '<URL>'

# Download to a custom directory
bash ${CLAUDE_SKILL_DIR}/scripts/download-video.sh '<URL>' 'path/to/output'
```

## Prerequisites

```bash
yt-dlp --version   # Required. Install: brew install yt-dlp (macOS) or pip install yt-dlp
```

**Optional** (for Douyin/TikTok fallback):
- `agent-browser` installed globally (`npm install -g agent-browser`)
- Chrome for Testing installed (`agent-browser install`)

## Usage

### Single Video

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/download-video.sh '<URL>'
```

The script handles everything automatically:
- Extracts a platform-prefixed video ID (`yt-dQw4w9WgXcQ`, `tk-7571284267028729101`, `vid-aHR0cHM6Ly93d3`)
- Saves to `resources/references/<video_id>.mp4`
- Skips download if file already exists (dedup)
- Retries TikTok downloads with `--cookies-from-browser chrome` on failure
- Removes zero-byte leftovers from interrupted downloads

### Batch Download

```bash
for URL in '<URL1>' '<URL2>' '<URL3>'; do
  bash ${CLAUDE_SKILL_DIR}/scripts/download-video.sh "$URL"
done
```

### Script Output

| Output | Meaning |
|--------|---------|
| `ALREADY_EXISTS: <path>` | File already downloaded, skipped |
| `DOWNLOADED: <path>` | Download succeeded |
| `FAILED: <message>` | Download failed (exit code 1) |

## Post-Download Actions

After a successful download, the user may want to:

1. **Analyze the video** — extract script, style, or rhythm:
   ```bash
   renoise analyze <path> --target video --language <user-language> --json
   ```

2. **Add to Material Pool** — for use as reference material in video generation:
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/skills/renoise-cli/scripts/material-ingest.mjs <path>
   ```

Suggest these options to the user after download completes.

## Douyin/TikTok Fallback

When yt-dlp fails for Douyin or TikTok URLs (common with 403 errors or region-restricted content), use the one-step browser-based fallback:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/download-fallback.sh '<douyin-or-tiktok-url>' 'output-dir'
```

This script wraps the full agent-browser + GreenVideo flow into a single command (open → paste URL → parse → extract video URL → download → close).

### Manual Fallback Steps

If the fallback script is unavailable, follow these steps:

1. Open GreenVideo:
   ```bash
   agent-browser open "https://greenvideo.cc/en/"
   ```

2. Paste URL and parse:
   ```bash
   agent-browser snapshot
   agent-browser fill <input-ref> "<video-url>"
   agent-browser click <start-button-ref>
   ```

3. Wait 5 seconds, then extract video URL:
   ```bash
   agent-browser eval "
   (function() {
     const nuxtData = window.__NUXT__;
     if (!nuxtData) return 'ERROR: No Nuxt data found';
     const str = JSON.stringify(nuxtData);
     const mp4Match = str.match(/https?:[^\\\"]*(?:mp4|video|play|aweme|douyinvod|bilivideo)[^\\\"]{0,500}/g);
     if (mp4Match && mp4Match.length > 0) return mp4Match[0];
     return 'ERROR: No video URL found in Nuxt state';
   })()
   "
   ```

4. Download and cleanup:
   ```bash
   curl -L -o ~/Downloads/<filename>.mp4 "<extracted-video-url>"
   agent-browser close
   ```

## Video ID Logic

| Platform | Pattern | Example ID |
|----------|---------|------------|
| YouTube | `watch?v=`, `shorts/`, `embed/`, `youtu.be/` → 11-char ID | `yt-dQw4w9WgXcQ` |
| TikTok | 15+ digit numeric ID in URL | `tk-7571284267028729101` |
| Other | Base64url of URL, first 16 chars | `vid-aHR0cHM6Ly93d3` |

## Troubleshooting

| Error | Solution |
|-------|----------|
| `HTTP Error 403` (TikTok/Douyin) | Script auto-retries with cookies. If still failing, use fallback script |
| `--max-filesize` skipped | Video exceeds 200M limit. Download manually with `-f 'best[height<=720]'` |
| `is not a valid URL` | Ensure URL is wrapped in single quotes |
| `Requested formats are incompatible` | yt-dlp auto-transcodes, no action needed |
| Parse fails on GreenVideo | Check URL is valid and publicly accessible |
| No video URL in Nuxt state | Try clicking download button and check for `<video>` elements |
| Download fails (403) from GreenVideo | Video URLs expire quickly — extract and download immediately |
