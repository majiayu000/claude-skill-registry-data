---
name: youtube
description: "Use when processing YouTube videos — fetch transcripts, generate summaries/threads/blogs from single videos, or batch-extract entire YouTube libraries (playlists, Liked Videos, Watch Later) via Phantom-MCP browser automation."
version: 1.0.0
author: Hermes Agent (consolidated from youtube-content + youtube-extraction)
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [youtube, video-content, transcript, summary, extraction, playlist, batch, phantom-mcp]
    triggers: [youtube, youtube-transcript, video-summary, youtube-content, video-transcription, youtube-download, video-notes, youtube-extraction, playlist-extract, saved-videos, youtube-playlist, video-archive, pim-ingestion, watch-later, pim]
    related_skills: [ocr-and-documents, gif-search, spotify]
---

# YouTube Skill — Single & Batch Video Processing

## Overview

Two modes for working with YouTube video content:

1. **Single Video** — Fetch a transcript for one URL, transform it into structured content (chapters, summaries, threads, blog posts).
2. **Batch Library Extraction** — Discover all playlists from YouTube Library via Phantom-MCP browser, extract video IDs, batch-fetch transcripts, run AI summarization, and persist to PIM DB / MemPalace.

Formerly two separate skills (`youtube-content` + `youtube-extraction`) — consolidated into one unified skill covering both single-video and batch workflows.

## When to Use

- User shares a YouTube URL and asks for a transcript or summary
- User wants a video turned into a blog post, Twitter thread, or bulleted notes
- User wants to archive their entire YouTube library (all playlists, Liked Videos, Watch Later)
- User asks about rate limits, transcript availability, or batch extraction

**Don't use for:** Extracting metadata only (video title, description, comments) — this skill focuses on transcripts and content transformation.

## Setup

```bash
pip install youtube-transcript-api
```

---

## Mode 1: Single Video — Transcript → Content Transformation

### 1. Fetch the Transcript

Use the helper script at `scripts/fetch_transcript.py`:

```bash
python scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text
python scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python scripts/fetch_transcript.py "URL" --language tr,en
```

### 2. Validate

Confirm output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, the video likely has captions disabled.

### 3. Chunk If Needed

If the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.

### 4. Transform

| Format | Description |
|--------|-------------|
| **Chapters** | Group by topic shifts, output timestamped chapter list |
| **Summary** | Concise 5-10 sentence overview |
| **Chapter summaries** | Chapters with a short paragraph |
| **Thread** | Twitter/X — numbered posts under 280 chars |
| **Blog post** | Full article with title, sections, takeaways |
| **Quotes** | Notable quotes with timestamps |
| **PIM Ingestion** | Folder of numbered `.md` files under `PIM/watch-later/{video-title}/` — see `references/pim-ingestion.md` |

See `references/output-formats.md` for examples of each format.

### 5. Verify

Re-read output for coherence, correct timestamps, completeness before presenting.

### Single Video Error Handling

| Error | Action |
|-------|--------|
| Transcript disabled | Tell user; suggest checking for subtitles on video page |
| Private/unavailable | Relay error, ask user to verify URL |
| No matching language | Retry without `--language` to fetch any available transcript |
| Dependency missing | Run `pip install youtube-transcript-api` and retry |

---

## Mode 2: yt-dlp Playlist Extraction (Simpler, Faster)

For extracting video IDs from authenticated playlists (Watch Later, Liked Videos, custom playlists), use **yt-dlp with browser cookies** instead of Phantom-MCP browser automation. This is faster, more reliable, and avoids the browser automation rate-limit issues.

### Prerequisites

```bash
pip install yt-dlp
# yt-dlp reads cookies from the user's running browser
```

### Auth Check (Run First)

Before extracting any playlist, verify that browser cookies are valid:

```python
def check_youtube_auth() -> bool:
    """Return True if YouTube cookies from browser are valid."""
    import json, subprocess
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--dump-single-json",
         "--ignore-errors", "--no-warnings", "--no-check-certificate",
         "--cookies-from-browser", "firefox",
         "https://www.youtube.com/playlist?list=WL"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0 and result.stdout.strip():
        data = json.loads(result.stdout)
        count = data.get("playlist_count", 0)
        print(f"Auth OK — Watch Later has {count} videos")
        return True
    else:
        print(f"Auth FAILED — {result.stderr[:200]}")
        return False
```

This catches the common case where Firefox is running but YouTube session cookies have expired. If auth fails, log into YouTube in Firefox first, then retry.

### Phase 1: Extract Playlist Videos

```bash
# Watch Later — uses Firefox cookies
yt-dlp --cookies-from-browser firefox \
  --flat-playlist --dump-single-json \
  --ignore-errors --no-warnings \
  "https://www.youtube.com/playlist?list=WL"
```

```python
import json, subprocess

def fetch_playlist_videos(playlist_url: str, label: str) -> list[dict]:
    """Fetch all video entries from an auth-required YouTube playlist."""
    cmd = ["yt-dlp", "--flat-playlist", "--dump-single-json",
           "--ignore-errors", "--no-warnings", "--no-check-certificate",
           "--cookies-from-browser", "firefox", playlist_url]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 or not result.stdout.strip():
        print(f"[WARN] Failed to fetch {label}: {result.stderr[:200]}")
        return []
    
    raw = json.loads(result.stdout)
    
    # ⚠️ CRITICAL: --dump-single-json returns a dict with 'entries' array,
    # NOT a flat list. You MUST access raw["entries"] to get the videos.
    if isinstance(raw, dict) and "entries" in raw:
        entries = raw["entries"]
    elif isinstance(raw, list):
        entries = raw
    else:
        entries = [raw]
    
    videos = []
    for entry in entries:
        if not entry or not isinstance(entry, dict):
            continue
        video_id = entry.get("id") or entry.get("video_id")
        if not video_id:
            continue
        if entry.get("title") in ("[Private video]", "[Deleted video]"):
            continue
        
        videos.append({
            "video_id": video_id,
            "title": (entry.get("title") or "").strip()[:500],
            "channel": (entry.get("channel") or entry.get("uploader") or "").strip()[:200],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "duration": entry.get("duration"),
        })
    
    return videos

# Usage
wl_videos = fetch_playlist_videos(
    "https://www.youtube.com/playlist?list=WL", "Watch Later"
)
ll_videos = fetch_playlist_videos(
    "https://www.youtube.com/playlist?list=LL", "Liked Videos"
)
```

### System playlists

| Playlist | URL ID | Typical Size |
|----------|--------|-------------|
| Watch Later | `WL` | 100-1000+ |
| Liked Videos | `LL` | 100-500+ |
| Favorites | `FL` | Varies |

### Phase 2: Dedup + Combine

```python
# Deduplicate by video_id across playlists
seen = set()
all_videos = []
for v in wl_videos + ll_videos:
    if v["video_id"] not in seen:
        seen.add(v["video_id"])
        all_videos.append(v)
```

### Phase 3: Batch-Fetch Transcripts (same as Mode 3 below)

Use `youtube-transcript-api` as described in Phase 3 below.

### When to Use Each Method

| Approach | When | Speedy? | Auth needed? |
|----------|------|---------|-------------|
| **Mode 2: yt-dlp + cookies** | Auth playlists, simple ID extraction | 🟢 Fast | Browser cookies |
| **Mode 3: Phantom-MCP browser** | Full extraction, rate-limited, or when cookies aren't available | 🔴 Slow | Manual login |
| **Third-party sites (Tactiq.io)** | IP-blocked from YouTube timedtext API | 🟡 Medium (browser req.) | None |
| **Description-only extraction** | ALL transcript endpoints blocked | 🟢 Instant | None |

For most cases, **prefer Mode 2** — it's 100x faster and doesn't trigger bot detection.
When Mode 2 AND Mode 3 fail with IP blocks, use **Tactiq.io** as the primary fallback (see Mode 4 below).

### Concrete Implementation

A full production-grade implementation of Mode 2 lives at:
**`${MY_REPOS}/Documents/github/git-mcp/services/personal-intelligence-mcp/app/connectors/yt_archive.py`**

This script wraps the entire batch extraction flow: auto-discovers ALL playlists (WL, LL, FL + custom), deduplicates, filters out music videos by channel/title keywords, fetches transcripts via `youtube-transcript-api` with yt-dlp fallback, and ingests into the PIM DB with full pipeline processing (summary + playbook). Runs as a cron job daily at 5AM ET.

Key features:
- Music filter: `is_music_video()` blocks VEVO, Topic, SoundCloud channels and songs/remix/cover/official-audio titles
- Dedup: `get_processed_ids()` queries PIM DB to skip already-ingested videos
- Pipeline integration: calls `process_item()` for summarization + playbook extraction
- Rate-limit-friendly: 0.5s delay between videos
- Dry-run mode: `--dry-run` flag to preview without writing

### Logging for Cron Jobs

When running playlist extraction as a cron job, always add persistent logging:

```python
import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path(__file__).parent / "yt_intelligence.log"
STATUS_FILE = Path(__file__).parent / "yt_last_status.json"

def log(msg: str, level: str = "INFO") -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line, flush=True)
    with open(str(LOG_FILE), "a") as f:
        f.write(line + "\n")

def save_status(status: dict) -> None:
    status["last_run_iso"] = datetime.now(timezone.utc).isoformat()
    with open(str(STATUS_FILE), "w") as f:
        json.dump(status, f, indent=2)
```

This ensures cron failures are visible in the log file even when stdout is discarded.

---

## Mode 3: Phantom-MCP Browser Extraction (Fallback)

For extracting when yt-dlp is blocked, rate-limited, or browser cookies aren't available, use Phantom-MCP browser automation with a real Firefox session.

### Phase 1: Discover Playlists

Navigate to `https://www.youtube.com/feed/library` via Phantom-MCP browser. Extract all playlist links using JavaScript:

```python
js = """(() => {
    const items = [];
    const links = document.querySelectorAll('a[href*="/playlist?list="]');
    const seen = new Set();
    links.forEach(a => {
        const href = a.href || '';
        const m = href.match(/[?&]list=([^&]+)/);
        const listId = m ? m[1] : '';
        if (listId && !seen.has(listId)) {
            seen.add(listId);
            items.push({listId, title: a.textContent.trim().substring(0,200), href});
        }
    });
    return JSON.stringify(items);
})()"""
```

**System playlists** (always available):
- Watch Later: `https://www.youtube.com/playlist?list=WL`
- Liked Videos: `https://www.youtube.com/playlist?list=LL`
- Favorites: `https://www.youtube.com/playlist?list=FL`

⚠️ **Covers ALL playlists** — Liked Videos (LL), Watch Later (WL), and every custom playlist.

### Phase 2: Extract Video IDs

Navigate to each playlist URL, scroll through up to 30 passes collecting video IDs, titles, channels:

```python
for scroll in range(30):
    await asyncio.sleep(1.5)
    
    js = """(() => {
        const videos = [];
        document.querySelectorAll('ytd-playlist-video-renderer, ytd-video-renderer').forEach(el => {
            const a = el.querySelector('a#video-title');
            if (!a) return;
            const m = (a.href || '').match(/watch\\?v=([^&]+)/);
            if (!m) return;
            const channel = el.querySelector('#channel-name a');
            videos.push({
                video_id: m[1],
                title: (a.textContent || '').trim().substring(0, 200),
                channel: channel ? channel.textContent.trim().substring(0, 100) : '',
                url: `https://www.youtube.com/watch?v=${m[1]}`,
            });
        });
        return JSON.stringify(videos);
    })()"""
    await browser.evaluate_script(ctx, "window.scrollBy(0, 600)")
```

Stop when 8+ consecutive scrolls yield no new video IDs.

### Phase 3: Batch-Fetch Transcripts

```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()  # v2: instantiate first
transcript = api.fetch(video_id)
segments = [{"text": seg.text, "start": seg.start, "duration": seg.duration}
            for seg in transcript]
```

Bulk: use `yt_transcripts.py` with ThreadPoolExecutor (10 workers, batches of 50).

### Phase 4: Browser Fallback for Rate-Limited Videos

If `IpBlocked` or `RequestBlocked`, use browser's authenticated InnerTube API:

```python
import requests as req
from youtube_transcript_api import YouTubeTranscriptApi
session = req.Session()
# Populate with YouTube cookies from headless Firefox
api = YouTubeTranscriptApi(http_client=session)
transcript = api.fetch(video_id)
```

See `references/innertube-api.md` for the full InnerTube endpoint and XML parsing.

### Phase 5: Save to PIM DB / MemPalace

Pipeline saves intermediate results to JSON, then ingests into the PIM database:

- `youtube_temp.json` — Full video metadata
- `youtube_transcripts.json` — Transcripts keyed by video_id

These are ingested by `pim_sync_mempalace.py` into **MemPalace** (personal-intelligence wing). The PIM DB table `saved_items` with `source_type='youtube'` is the centralized store:

```sql
SELECT * FROM saved_items WHERE source_type = 'youtube' ORDER BY created_at DESC;
```

### Phase 6: AI Summarization (Dual Provider)

After transcripts are fetched, run AI summarization. Google Gemini is primary; OpenRouter fallback when daily quota is exhausted.

**Script:** `${USER_HOME}/FireFox-Phantom-MCP/yt_summarize.py`

**Provider Chain (auto mode):**
1. Google Gemini — `gemini-2.5-flash-lite` (separate free quota pool, ~1,000 req/day)
2. OpenRouter — `nvidia/nemotron-3-nano-30b-a3b:free` (sequential to avoid rate limits)

```bash
python yt_summarize.py --provider auto
python yt_summarize.py --provider google
python yt_summarize.py --provider openrouter
```

See `references/gemini-summarization.md` and `references/google-api-key-setup.md` for quota management, model selection, and API key rotation.

---

## Fallback: Transcript API Blocked (HTTP 429)

When `youtube-transcript-api`, the InnerTube timedtext API, and third-party sites all return HTTP 429 (rate-limited), this means **YouTube has blocked the current IP** for automated caption requests. This is common on cloud-hosted or shared IPs. The block is per-IP and lasts 1-30+ minutes.

### What to try (in order):

1. **youtube-transcript-api** with browser cookies session — works if the browser itself has a different IP or cookie-based session
2. **Browser InnerTube API** — extract `window.ytInitialPlayerResponse` via browser evaluate, get the caption track URL, and fetch it from within the browser context (uses browser's own session)
3. **yt-dlp with `--cookies-from-browser firefox`** — uses Firefox's authenticated session; may bypass the IP block via cookie auth
4. **Third-party sites** — `youtubetranscript.com`, `downsub.com`, `subtitle.dog`, **`tactiq.io`** — these proxy through their own infrastructure

   **`tactiq.io/tools/youtube-transcript`** is the most reliable third-party option. Navigate there with a **Playwright/Phantom-MCP browser**, fill in the YouTube URL, and the page generates a full transcript with timestamps. Extract it with:
   ```javascript
   document.body.innerText
   ```
   The transcript appears after the "Learn more" section text, starting at `00:00:00.000`.
   
   **Note:** The "Download" button on Tactiq opens a blank popup — `innerText` is the reliable extraction method. The full text is ~100K+ chars for a 60-min video.
5. **Invidious API** — Some Invidious instances (`inv.nadeko.net`, `yewtu.be`) can list available captions via their REST API and may serve the content. But the upstream fetch from Invidious to YouTube will also fail if the IP is blocked — captions list may show but content comes back empty.
6. **Video description as data source** — when ALL transcript paths are blocked, use the video description + `ytInitialPlayerResponse` metadata as the primary content source

### When ALL transcript endpoints are blocked (fallback strategy):

```python
# Extract ytInitialPlayerResponse from the page HTML
import re, json
resp = requests.get(f"https://www.youtube.com/watch?v={video_id}", headers={...})
match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', resp.text, re.DOTALL)
data = json.loads(match.group(1))
# Extract videoDetails for metadata
details = data.get('videoDetails', {})
title = details.get('title')
description = details.get('shortDescription', '')
length = details.get('lengthSeconds')
# Extract captionTracks URLs (may also be blocked when fetched separately)
```

### Working with description-only source (full IP block):

When ALL endpoints return the Google "Sorry" page, the video description becomes the primary data source. The description often contains the **exact outline** the video follows, including bullet points for each topic covered.

**Process for description-only extraction:**

1. **Extract ytInitialPlayerResponse** from the page source (this always works since it's in the HTML, not fetched from an API):
   ```python
   import re, json, requests
   r = requests.get(f"https://www.youtube.com/watch?v={video_id}", headers=headers)
   match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', r.text, re.DOTALL)
   data = json.loads(match.group(1))
   vd = data['videoDetails']
   title = vd['title']
   description = vd['shortDescription']
   ```
2. **Parse the description** for structured content — bullet points (`*` items), numbered lists, section headers, and bolded text (`**...**`)
3. **Build the output files** (summary.md, playbook.md, and any specific extraction the user asked for) from the description's bullet points, enriched with channel/guest context and common knowledge about the topic
4. **Try to extract captionTracks URLs** from `data['captions']['playerCaptionsTracklistRenderer']['captionTracks']` — these URLs exist but will fail when fetched, proving the attempt was made
5. **Log which methods were tried** in `00-metadata.md` so the user knows the transcript wasn't verbatim

**Example output files for description-only extraction:**
- `01-summary.md` — overview, key themes, structured topic list, key numbers table
- `02-playbook.md` — phase-based framework built from the outline, with concrete steps
- `03-{user-requested-topic}.md` — the specific thing the user asked for (VA criteria, scripts, specific setup steps), synthesized from the topic outline around the relevant timestamp

**Limitations to note:**
- The description contains what the creator **intended to cover**, not what was **actually said** — nuance, examples, and digressions are lost
- Timestamps in the URL (e.g., `&t=1978s`) hint at which section the user cares about, but without the transcript you can't know exactly what's said there unless it's marked in chapters
- Clearly note in the output files that the content was compiled from the description outline, not a verbatim transcript

### Pitfalls

- The 429 block is **per-endpoint** — `video.google.com/timedtext` and `youtube.com/api/timedtext` are separate rate limit buckets
- The block applies to both Python requests AND browser `fetch()` calls from the same IP — even Playwright's fetch won't bypass it
- Using `youtube-transcript-api` with a `requests.Session` and custom headers does NOT bypass the block once the IP is flagged
- **Browser cookies do NOT bypass IP-level blocks** — the timedtext endpoint returns the Google "Sorry" page (429) even when fetched with `credentials: 'include'` from within an authenticated browser session. Cookie auth only helps with different rate-limit buckets like the InnerTube player API.
- **yt-dlp n-challenge also fails** when the IP is flagged — `yt-dlp` returns "n challenge solving failed: Some formats may be missing" and "Only images are available for download", not just on timedtext but across all format extraction. This means the block is at the **YouTube frontend/edge level**, not just the captions API.
- **Invidious upstream fetch fails too** — Invidious instances can list available captions via their REST API (`/api/v1/captions/{video_id}`), but the actual caption content fetch returns empty (0 bytes) because the Invidious server's upstream request to YouTube's timedtext API is also blocked from the same IP.
- **Auto-generated (ASR) captions are the only track for many videos** — these are more restricted than manual captions and may 404 on certain endpoints
- **Clean up browser sessions after use** — when using Playwright/Phantom-MCP to interact with YouTube, close the browser tab/context when done. Leaving a headless browser open with a video playing: (a) wastes system resources, (b) keeps the video audio playing if any, (c) maintains the rate-limit penalty against that IP. Call `browser_close()` or close the tab after extraction work is complete.
- A new IP (VPN, proxy, mobile tether, or waiting for the block to expire) resets the block instantly

| Error | Meaning | Solution |
|-------|---------|----------|
| `IpBlocked` | IP rate-limited | Use browser cookie auth or wait 10+ min |
| `RequestBlocked` | Request rejected | Same as IpBlocked |
| `TranscriptsDisabled` | Video has no captions | Skip permanently |
| `NoTranscriptFound` | No captions for requested language | Try without language param |

**Rate limits are STICKY:** Once blocked, it lasts 1-30+ minutes. Plan in two phases: first batch (up to ~400) via direct API, remainder via browser InnerTube fallback.

---

## Common Pitfalls

1. **Shorts/music videos rarely have transcripts** — ~60% of "Liked Videos" are Shorts/music with no captions.
2. **Duplicate video IDs across playlists** — Dedup by `video_id` when merging.
3. **Browser session must be logged in** — Navigate to YouTube first; check `document.cookie` for session tokens.
4. **Headless Firefox needs the real profile for YouTube cookies** — Use `-P "default-release-1"`, not the Hermes-MCP automation profile.
5. **Kill Firefox before relaunch** — `taskkill /F /IM firefox.exe`; orphaned instances may hold port 9223.
6. **youtube-transcript-api v2 uses instance methods** — `YouTubeTranscriptApi().fetch(video_id)`, not static `get_transcript`.
7. **Google API keys expire** — Check and renew at https://aistudio.google.com/apikey.
8. **Free tier daily quota can exhaust mid-batch** — 478 transcripts can exhaust 1,500 req/day. Switch to `gemini-2.5-flash-lite` (separate quota pool) or OpenRouter fallback.
9. **Browser InnerTube API key** — `AIzaSy<your-yt-api-key>` (use responsibly).
10. **🚨 `--dump-single-json` with playlists returns a DICT, not a list** — yt-dlp's `--dump-single-json` on a playlist URL returns a single JSON object with an `entries` array containing the video items. The outer dict has keys like `id`, `title`, `playlist_count`, and `entries`. You MUST access `data["entries"]` to get the actual video list.
11. **🚨 `--cookies-from-browser firefox` is the simplest auth solution on Windows** — On this Windows machine, Firefox is always running with the operator's YouTube login session. `yt-dlp --cookies-from-browser firefox` reads cookies directly from the running Firefox profile without needing a remote debugging port.
13. **Close Playwright/Phantom-MCP browser sessions after YouTube extraction** — Leaving a headless/Playwright browser open on a YouTube video page keeps the audio stream active (video playing silently) and consumes system resources. After extracting transcript data, click download or extract via `document.body.innerText`, then call `browser_close()` or close the tab immediately. The user can hear audio playing from a headless browser even though no window is visible.
14. **Always add persistent logging for cron jobs** — When running YouTube extraction as a cron job, write to a dedicated log file + save a status JSON after each run for offline debugging.

## Verification Checklist

- [ ] Single video: `python scripts/fetch_transcript.py <url>` returns valid JSON
- [ ] Single video: transcript transforms produce coherent chapters/summary/thread
- [ ] Batch: auth check passes (`check_youtube_auth()` returns True)
- [ ] Batch: playlist extraction returns expected number of videos
- [ ] Batch: entries parsed correctly (check `len(raw["entries"])`)
- [ ] Batch: transcript batching completes without rate limit errors
- [ ] Batch: AI summarization produces structured JSON output
- [ ] Batch: results persist to PIM DB / MemPalace
- [ ] Cron: log file created with timestamps
- [ ] Cron: status JSON file written with error list
- [ ] Old skills deleted: `youtube-content` + `youtube-extraction` removed

## Related Files

| File | Description |
|------|-------------|
| `scripts/fetch_transcript.py` | Single-video transcript fetcher (JSON/text/timestamped) |
| `templates/cron-status-check.py` | Reusable cron job health check script |
| `references/yt-dlp-cron-pattern.md` | Full yt-dlp + cookies auth extraction pattern with monitoring |
| `references/output-formats.md` | Examples for chapters, summary, thread, blog, quotes |
| `references/innertube-api.md` | InnerTube API endpoint and cookie-based auth bypass |
| `references/gemini-summarization.md` | Batch AI summarization via Gemini + OpenRouter fallback |
| `references/google-api-key-setup.md` | API key setup, free tier limits, key expiry/rotation |
| `references/pim-ingestion.md` | PIM Watch Later folder structure — numbered `.md` files under `PIM/watch-later/{video-title}/` |
| `yt_archive.py` (external) | Full production batch archive — auto-discovers playlists, filters music, fetches transcripts, ingests to PIM DB with playbook extraction. Path: `app/connectors/yt_archive.py` in the PIM MCP project. |
