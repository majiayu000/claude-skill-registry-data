---
name: download-transcripts
description: Download YouTube transcripts for videos tracked in a CSV file. Use when you need to download transcripts in bulk with progress tracking, fetching transcripts overnight, processing video libraries, or when the user mentions "get transcripts", "download captions", or "bulk transcript download".
---

# Download Transcripts from CSV

**Why?** Manually downloading transcripts one-by-one is tedious and error-prone. This skill automates bulk transcript downloads with rate limiting, progress tracking, and resume capability.

## Quick Start

```bash
# Standard usage (recommended)
ytscriber download --folder <channel-name> --delay 60

# Single video (adds to default collection and downloads)
ytscriber add "https://www.youtube.com/watch?v=VIDEO_ID" --folder random
```

---

## Workflow

### 1. Verify Prerequisites

Ensure you have a CSV file with video URLs:
- Created by `extract-videos` skill, OR
- Manually curated with `url` column

```bash
# Check CSV exists and has videos
head -5 ~/Documents/YTScriber/<channel-name>/videos.csv
```

> [!TIP]
> If you don't have a CSV yet, run `extract-videos` first to build your video list from a YouTube channel.

### 2. Run Download Command

```bash
ytscriber download --folder <folder-name> --delay 60
```

| Option | Description | Default | Notes |
|--------|-------------|---------|-------|
| `--folder` | Folder name containing videos.csv | Required | Uses platformdirs data path |
| `--delay` | Seconds between requests | 60 | Minimum 30, recommended 60+ |
| `--verbose, -v` | Enable verbose output | False | Shows download progress |

> [!CAUTION]
> **NEVER set `--delay` below 30 seconds.** YouTube will block your IP if you make requests too quickly. The default of 60 seconds exists for a reason. You WILL get banned and may wait hours before downloading again.

### 3. Validate Downloads

After the command completes:

```bash
# Check how many transcripts downloaded
ls -la ~/Documents/YTScriber/<folder-name>/transcripts/*.md | wc -l

# Verify CSV status updated
grep -c "success" ~/Documents/YTScriber/<folder-name>/videos.csv
```

The command automatically:
- Downloads transcripts as markdown with YAML frontmatter
- Updates CSV `transcript_downloaded` column with success/error/empty
- Skips already-downloaded videos on re-run

---

## Output Format

Transcripts are saved as markdown with YAML frontmatter:

```markdown
---
video_id: dQw4w9WgXcQ
video_url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
title: Building Resilient Microservices at Scale
author: Jane Smith
published_date: 2025-03-15
length_minutes: 42.5
views: 15234
description: "Video description..."
is_generated: True
---

[Transcript text as continuous paragraph]
```

---

## Examples

### Overnight Batch Processing
```bash
# Large channel - run overnight with safe delay
ytscriber download --folder aws-reinvent-2025 --delay 90 --verbose
```

### Conference Playlist
```bash
# Smaller collection - minimum safe delay
ytscriber download --folder pycon-2024 --delay 30
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "No transcript found" | Video lacks captions | Some videos have no captions available |
| IP blocked / 403 errors | Too many requests too quickly | Wait 30-60 minutes, then retry with `--delay 120` |
| Script interrupted mid-run | Network issue or Ctrl+C | Re-run the exact same command; it skips completed videos |
| Empty transcript files | Auto-captions unavailable or video is live | Check if video has captions on YouTube; skip if not |
| "Folder not found" | Wrong folder name | Verify folder with `ls ~/Documents/YTScriber/` |
| Slow downloads | Rate limiting working correctly | This is expected; 100 videos at 60s delay = ~2 hours |

---

## Common Mistakes

1. **Reducing delay to "speed up"** - Do not set delay below 30 seconds. You will get IP banned. Use overnight runs for large batches.

2. **Running without checking CSV first** - Always verify your CSV exists and has videos before running. Empty CSVs waste time.

3. **Not using resume capability** - If interrupted, don't start over. Re-run the same command to resume from where you left off.

---

## Quality Checklist

Before running:
- [ ] CSV file exists and has `url` column
- [ ] Folder name is correct
- [ ] Delay is 30+ seconds (60+ recommended)
- [ ] Sufficient time allocated (1 min per video minimum)

After running:
- [ ] Transcript count matches expected videos
- [ ] CSV `transcript_downloaded` column updated
- [ ] Spot-check 2-3 transcripts for valid content
- [ ] No empty or malformed markdown files
