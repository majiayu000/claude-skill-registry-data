---
name: audio-scrape
description: Scrape podcast episodes, sermons, and audio sources — discovers via iTunes Search API, parses RSS feeds, downloads audio, transcribes via OpenAI Whisper, chunks for search, and upserts into the {{TABLE_NAME}} table.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Scrape audio sources: $ARGUMENTS

$ARGUMENTS should be one of:
- A person/topic name to search (e.g. `"Jane Smith"`) — discovers podcasts via iTunes
- `--rss https://feed.url/rss` to scrape a specific RSS feed
- `--episode-url https://example.com/episode.mp3 --title "Episode Title"` to scrape a single audio file
- `--refresh` to re-transcribe episodes that don't have transcripts yet
- Empty — ask the user for the search term

## Before Starting

1. Confirm `OPENAI_API_KEY` is set in `.env.local` — needed for Whisper transcription
2. Read `{{DB_SCHEMA}}` for the episodes and series table definitions
3. Read `{{SCRAPE_SCRIPT}}` to understand the existing scrape script
4. Optionally confirm `ffmpeg` is installed (`which ffmpeg`) — needed for splitting large audio files (>25MB)

## Pipeline Stages

### Stage 1 — Discover Podcasts

1. **iTunes Search API** (free, no key needed): Search `https://itunes.apple.com/search?term={query}&media=podcast`
2. **Multiple query variations**: `"{name}"`, `"{name} podcast"`, `"{name} interview"`, `"{name} sermon"`
3. **Deduplicate feeds**: Track by `feedUrl` to avoid duplicate processing
4. **Delta check**: Compare fetched episodes against existing `external_id` values in `{{TABLE_NAME}}`

### Stage 2 — Parse RSS Feeds

For each discovered feed:

1. Fetch the RSS/XML feed with a User-Agent header
2. Parse `<item>` elements extracting:
   - `<title>` → episode title
   - `<enclosure url="...">` → audio URL (required, skip items without it)
   - `<itunes:duration>` → duration in seconds
   - `<itunes:episode>`, `<itunes:season>` → numbering
   - `<pubDate>` → published date (convert to ISO 8601)
   - `<itunes:summary>` or `<description>` → episode description
   - `<itunes:image href="...">` → thumbnail
3. **Filter relevance**: Only keep episodes where the search term appears in title, description, or series name

### Stage 3 — Download & Transcribe

For each **new** episode (not already in DB with a transcript):

1. Download audio via `curl` to `{{AUDIO_CACHE_DIR}}/{external_id}.mp3` with caching
2. Transcribe via OpenAI Whisper API (`whisper-1` model):
   - Files <= 25MB: single API call
   - Files > 25MB: split into 20-minute chunks via `ffmpeg`, transcribe each, concatenate
3. If transcription fails, set transcript to `null` and continue

### Stage 4 — Chunk Transcripts for Search

Split each transcript into chunks for embedding/search:

- **Target**: 500 words per chunk
- **Overlap**: 75 words
- **Stride**: 425 words (500 - 75)
- Each chunk gets: `chunk_index`, `text`, `start_offset`
- Absorb tiny final chunks (< 75 words) into the previous chunk

### Stage 5 — Database Upsert

Upsert into `{{TABLE_NAME}}` and `{{SERIES_TABLE_NAME}}` tables.

## Database Mapping

Map RSS/audio fields to the episodes table:

| RSS Field | DB Column |
|---|---|
| `<title>` | `title` |
| title (slugified + external_id suffix) | `slug` |
| `<itunes:summary>` or `<description>` | `description` |
| `<enclosure url>` | `audio_url` |
| `<itunes:duration>` (parsed) | `duration_seconds` |
| `<itunes:episode>` | `episode_number` |
| `<itunes:season>` | `season_number` |
| `<pubDate>` (ISO 8601) | `published_at` |
| `<itunes:image>` or channel image | `thumbnail_url` |
| hash of audio_url | `external_id` |
| `<link>` | `external_url` |
| Whisper transcript | `transcript` |
| `'rss'` | `hosting_provider` |
| `'podcast'` / `'sermon'` / `'audio'` | `source_type` |
| `'published'` | `status` |

## Key Design Rules

- **Idempotent** — Use upserts keyed on `external_id` (hash of audio URL). Safe to re-run.
- **Resume-safe** — Skip audio download if file already exists in `{{AUDIO_CACHE_DIR}}/`
- **Incremental** — Only download/transcribe new episodes
- **Graceful degradation** — Per-episode failures don't crash the pipeline
- **All timestamps UTC** — ISO 8601 throughout
- **Pace API calls** — 1-second delay between Whisper calls, 200ms between RSS fetches

## Running

```bash
{{RUN_CMD}} audio:scrape -- --search "Search Term"
{{RUN_CMD}} audio:scrape -- --rss https://feed.example.com/rss
{{RUN_CMD}} audio:scrape -- --episode-url https://example.com/episode.mp3 --title "My Episode"
{{RUN_CMD}} audio:scrape -- --refresh
{{RUN_CMD}} audio:scrape -- --search "Search Term" --max 10
{{RUN_CMD}} audio:scrape -- --search "Search Term" --skip-transcribe
{{RUN_CMD}} audio:scrape -- --search "Search Term" --source-type sermon
```

## Output Format

```
## Audio Scrape Report

### Search: [query]
### Podcasts found: N feeds, M relevant episodes

### Stage 1 — Discovery: OK
- Feeds found: N
- Episodes parsed: M

### Stage 2 — Relevance filter: OK
- Relevant episodes: N

### Stage 3 — Transcripts: OK
- Transcribed: X
- Skipped (already exists): Y
- Failed: Z

### Stage 4 — Chunks: OK
- Total chunks: N across M episodes

### Stage 5 — Database:
- Series upserted: N
- Episodes inserted: X, updated: Y

### Warnings:
- [any non-blocking issues]
```

## Cost Notes

- iTunes Search API: Free, no key needed
- RSS feeds: Free, public
- OpenAI Whisper API: ~$0.006/minute of audio
  - A 1-hour episode costs ~$0.36
  - 100 episodes averaging 45 min each = ~$27
- Audio downloads: bandwidth only; files cached in `{{AUDIO_CACHE_DIR}}/`
- Large files (>25MB) require `ffmpeg` for splitting

## Error Handling

- Missing `OPENAI_API_KEY` → stop immediately with instructions
- Individual episode download failure → log warning, continue pipeline
- Whisper API error → log warning, set transcript null, continue
- RSS parse failure → log warning, skip feed, continue
- Large file without `ffmpeg` → attempt direct transcription (may fail for >25MB)
