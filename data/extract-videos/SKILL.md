---
name: extract-videos
description: Extract video metadata from a YouTube channel and save to CSV for tracking. Use when adding a new channel, extracting conference videos, populating video lists, or when the user mentions "extract videos", "get videos from channel", "add channel", or "video metadata".
---

# Extract Videos from YouTube Channel

**Why?** Manually tracking YouTube videos is tedious and error-prone. This skill automates extracting video metadata (titles, durations, URLs) into a CSV for systematic transcript downloading and analysis.

## Quick Start

```bash
# Recurring channel (adds to channels.yaml for future syncs)
mkdir -p data/<channel-name>
transcript-extract https://www.youtube.com/@ChannelName/videos \
  --count 50 \
  --append-csv data/<channel-name>/videos.csv \
  --register-channel

# One-time extraction (conferences, playlists)
mkdir -p data/<name>
transcript-extract <youtube_url> --count 100 --append-csv data/<name>/videos.csv
```

---

## Workflow

### 1. Determine Extraction Type

| Scenario | Use `--register-channel`? | Typical Count |
|----------|---------------------------|---------------|
| New channel for ongoing tracking | Yes | 50-200 initial, then 20-50 for syncs |
| Conference talks (one-time) | No | 50-500 |
| Specific playlist/topic | No | As needed |
| Testing/exploration | No | 5-10 |

> [!TIP]
> Use `--register-channel` only for channels you want to sync regularly. It adds the channel to `data/channels.yaml` for the `sync-all-channels` skill.

### 2. Create Directory Structure

```bash
mkdir -p data/<channel-name>
```

**Naming conventions:**
- Use lowercase with hyphens: `aws-reinvent-2025`, `veritasium`, `lexfridman`
- Match the YouTube handle when possible: `@veritasium` becomes `veritasium`
- For conferences, include year: `pycon-2025`, `kubecon-eu-2024`

### 3. Run Extraction Command

```bash
transcript-extract <channel_url> \
  --count <N> \
  --append-csv data/<channel-name>/videos.csv \
  [--register-channel]
```

**Parameters:**

| Option | Description | Default | When to Use |
|--------|-------------|---------|-------------|
| `--count, -n` | Number of latest videos | 10 | Always specify explicitly |
| `--append-csv` | CSV file path | Required | Always use for tracking |
| `--register-channel` | Add to `channels.yaml` | False | Recurring channels only |
| `--output, -o` | Save video IDs to text file | - | Rarely needed |
| `--verbose, -v` | Enable verbose output | False | Debugging |

> [!CAUTION]
> The `--count` in the command sets the INITIAL extraction count. The `count` in `channels.yaml` (set by `--register-channel`) controls FUTURE sync counts. These are independent values.

### 4. Verify Extraction

```bash
# Check CSV was created with expected columns
head -3 data/<channel-name>/videos.csv

# Count extracted videos
wc -l data/<channel-name>/videos.csv
```

**Expected CSV columns:**
- `url` - Full YouTube video URL
- `title` - Video title
- `duration_minutes` - Video length
- `view_count` - Number of views
- `description` - Video description
- `transcript_downloaded` - Tracking field (initially empty)
- `summary_done` - Tracking field (initially empty)

---

## Examples

### Adding a New Channel for Regular Syncing

```bash
# 1. Create directory
mkdir -p data/veritasium

# 2. Extract initial batch with registration
transcript-extract https://www.youtube.com/@veritasium/videos \
  --count 100 \
  --append-csv data/veritasium/videos.csv \
  --register-channel

# Result: 100 videos extracted, channel added to channels.yaml with count: 100
```

### One-Time Conference Extraction

```bash
# Extract AWS re:Invent talks (won't be synced later)
mkdir -p data/aws-reinvent-2025
transcript-extract https://www.youtube.com/@AWSEventsChannel/videos \
  --count 200 \
  --append-csv data/aws-reinvent-2025/videos.csv

# No --register-channel = not added to channels.yaml
```

### Re-running on Existing CSV (Incremental Update)

```bash
# Running again only adds NEW videos (duplicates auto-skipped)
transcript-extract https://www.youtube.com/@veritasium/videos \
  --count 20 \
  --append-csv data/veritasium/videos.csv

# Safe to run multiple times - existing videos preserved
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "No videos found" | Wrong URL format | Use `https://www.youtube.com/@ChannelName/videos` (include `/videos`) |
| CSV not created | Directory doesn't exist | Run `mkdir -p data/<name>` first |
| Duplicate videos appearing | Running with different URL variants | Always use canonical `@handle/videos` format |
| Channel not in `channels.yaml` | Forgot `--register-channel` | Re-run with flag, or manually add to YAML |
| Wrong video count in `channels.yaml` | Flag uses command's `--count` value | Edit `channels.yaml` manually to adjust future sync count |
| Permission denied | File locked or read-only | Close any apps using the CSV |

---

## Common Mistakes

1. **Forgetting `/videos` in URL**
   - Wrong: `https://www.youtube.com/@veritasium`
   - Right: `https://www.youtube.com/@veritasium/videos`

2. **Using `--register-channel` for one-time extractions**
   - This pollutes `channels.yaml` with channels you won't sync
   - Only use for channels you want in the regular sync rotation

3. **Expecting transcripts to download**
   - This skill ONLY extracts video metadata to CSV
   - Use `download-transcripts` skill to actually fetch transcripts

4. **Not creating directory first**
   - The `--append-csv` path requires parent directory to exist
   - Always run `mkdir -p data/<name>` before extraction

5. **Confusing command `--count` with `channels.yaml` count**
   - Command `--count`: How many videos to extract NOW
   - `channels.yaml` `count`: How many videos for FUTURE syncs
   - Initial extraction might be 200, but sync count might be 30

---

## Quality Checklist

Before considering extraction complete:

- [ ] Directory created in `data/` with proper naming
- [ ] CSV exists with expected video count
- [ ] CSV has all required columns (url, title, duration_minutes, etc.)
- [ ] If recurring channel: entry exists in `channels.yaml`
- [ ] If recurring channel: `channels.yaml` count is set appropriately for future syncs

---

## Next Steps

After extracting videos:

1. **Download transcripts**: Use the `download-transcripts` skill
2. **Sync channels later**: Use `sync-all-channels` for registered channels
3. **Add summaries**: Use `summarize-transcripts` after downloading
