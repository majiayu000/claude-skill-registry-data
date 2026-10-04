---
name: youtube-scrape
description: Scrape a YouTube channel or video — fetches all video metadata via YouTube Data API, downloads transcripts with yt-dlp, chunks for search, and upserts into the videos table. Use when scraping a channel handle, refreshing stats, or ingesting a single video.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Scrape YouTube videos: $ARGUMENTS

$ARGUMENTS should be one of:
- A YouTube channel handle (e.g. `@AlanHirsch`) or channel ID (e.g. `UCxVxcTULO9cFU6SB9qVaisQ`)
- `--video VIDEO_ID` to scrape a single video
- `--refresh` to re-fetch stats for all existing videos without re-downloading transcripts
- Empty — ask the user for the channel handle

## Before Starting

1. Confirm `YOUTUBE_API_KEY` is set in `.env.local` — if not, tell the user to add it
2. Confirm `yt-dlp` is installed (`which yt-dlp`) — if not, tell the user to install it (`pip install yt-dlp`)
3. Read `{{SCHEMA_PATH}}` for the `videos`, `videoSeries` table definitions
4. Read `{{SCRIPTS_DIR}}/youtube-scrape.ts` to understand the existing scrape script

## Pipeline Stages

### Stage 1 — Fetch All Videos from Channel

1. **Resolve channel ID**: If given a handle (`@Name`), call the YouTube Data API v3 `channels?part=id&forHandle=@Name` to get the `UC...` channel ID
2. **Derive uploads playlist**: Replace `UC` prefix with `UU` to get the uploads playlist ID
3. **Paginate playlist**: Call `playlistItems.list` with `maxResults=50`, following `nextPageToken` until exhausted
4. **Enrich with details**: Call `videos.list` in batches of 50 (`part=snippet,contentDetails,statistics`) to get full metadata
5. **Delta check**: Compare fetched `video_id` list against existing `external_id` values in the `videos` table — only download transcripts for new videos

### Stage 2 — Download & Parse Transcripts

For each **new** video (not already in DB with a transcript):

1. Run `yt-dlp --write-auto-subs --sub-lang en --skip-download -o "data/vtt/%(id)s" "https://youtube.com/watch?v=VIDEO_ID"` with a 60-second timeout
2. Parse the resulting `.en.vtt` file:
   - Strip VTT headers, cue IDs, positioning metadata
   - Deduplicate repeated lines (auto-subs repeat heavily)
   - Extract `{ start, end, text }` segments
   - Concatenate into `fullText`
3. If no VTT file produced, set transcript to `null` and continue

### Stage 3 — Chunk Transcripts for Search

Split each transcript into chunks for embedding/search:

- **Target**: 500 words per chunk
- **Overlap**: 75 words
- **Stride**: 425 words (500 - 75)
- Each chunk gets: `chunk_index`, `text`, `start_time`, `end_time`, `timestamp_url` (deep-link to that point in the video)
- Absorb tiny final chunks (< 75 words) into the previous chunk

Store chunks in a JSON field or separate table as appropriate.

### Stage 4 — Fetch Comments (Optional)

Call `commentThreads.list` with `maxResults=100&order=relevance`, paginating with `nextPageToken`:

- Handle 403 gracefully (comments disabled) — return `[]`
- Extract: `comment_id`, `author`, `text`, `like_count`, `published_at`
- Per-video errors should not crash the pipeline

## Database Mapping

Map YouTube fields to the existing `videos` table:

| YouTube Field | DB Column |
|---|---|
| `item.id` | `external_id` |
| `item.snippet.title` | `title` |
| `item.snippet.title` (slugified) | `slug` |
| `item.snippet.description` | `description` |
| `https://youtube.com/watch?v={id}` | `video_url` |
| `item.snippet.thumbnails.maxres?.url` | `thumbnail_url` |
| `item.contentDetails.duration` (parsed) | `duration_seconds` |
| `item.statistics.viewCount` | `view_count` |
| `item.statistics.likeCount` | `like_count` |
| `item.statistics.commentCount` | `comment_count` |
| `item.snippet.tags` | `tags` (jsonb) |
| `item.snippet.publishedAt` | `published_at` |
| Parsed transcript fullText | `transcript` |
| `'youtube'` | `hosting_provider` |
| `<iframe>` embed string | `embed_code` |
| `'published'` | `status` |

## Key Design Rules

- **Idempotent** — Use upserts keyed on `external_id`. Safe to re-run.
- **Resume-safe** — Skip transcript download if VTT file already exists in `data/vtt/`
- **Incremental** — Only download transcripts for new videos. Always refresh stats.
- **Graceful degradation** — 403 returns `[]`; per-video errors don't crash the pipeline
- **All timestamps UTC** — ISO 8601 throughout
- **Batch operations** — 50 per YouTube API call; small delays between yt-dlp downloads

## Running

```bash
pnpm youtube:scrape -- --channel @AlanHirsch
pnpm youtube:scrape -- --video dQw4w9WgXcQ
pnpm youtube:scrape -- --refresh
```

## Output Format

```
## YouTube Scrape Report

### Channel: [name] ([handle])
### Videos found: N total, M new

### Stage 1 — Metadata: OK
- Fetched: N videos
- New (not in DB): M

### Stage 2 — Transcripts: OK
- Downloaded: X
- Skipped (already exists): Y
- Failed (no subs): Z

### Stage 3 — Chunks: OK
- Total chunks: N across M videos

### Stage 4 — Comments: OK / SKIPPED
- Fetched: N comments across M videos

### Database:
- Upserted: N videos
- Stats refreshed: M videos

### Warnings:
- [any non-blocking issues]
```

## Quota Notes

- YouTube Data API v3 free tier: 10,000 units/day
- `playlistItems.list` = 1 unit, `videos.list` = 1 unit, `commentThreads.list` = 1 unit
- A channel with 100 videos uses ~104 units per full run
- yt-dlp has no official rate limit but add small delays between downloads

## Error Handling

- Missing `YOUTUBE_API_KEY` → stop immediately with instructions
- Missing `yt-dlp` → stop immediately with install instructions
- Individual video transcript failure → log warning, continue pipeline
- Comments disabled (403) → return empty array, continue
- API quota exceeded (403 with reason `quotaExceeded`) → stop and report progress so far
