---
name: sync-all-channels
description: Extract videos from all enabled YouTube channels in channels.yaml. Use for batch updating video lists before downloading transcripts overnight, when the user mentions "sync channels", "update video lists", "refresh channels", or before running download-all-transcripts.
---

# Sync All Channels

**Why?** Manually running extract-videos on each channel is tedious and error-prone. This skill automates batch extraction with rate limiting to respect YouTube's API.

## Quick Start

```bash
# 1. Ensure yq is installed
brew install yq

# 2. Run the sync
./scripts/sync_all_channels.sh
```

> [!TIP]
> Run this before `download-all-transcripts` to ensure video lists are current.

---

## Workflow

### 1. Verify Prerequisites

Check that `yq` is installed:

```bash
which yq || echo "Install with: brew install yq"
```

### 2. Review Channel Configuration

Open `data/channels.yaml` and verify:
- All desired channels have `enabled: true`
- Video counts are appropriate (20-100 typical)
- URLs point to channel video pages

```yaml
channels:
  - folder: OpenAI
    url: https://www.youtube.com/@OpenAI/videos
    count: 50
    enabled: true
```

> [!CAUTION]
> Setting `count` above 200 significantly increases sync time and may trigger rate limiting.

### 3. Execute the Sync

```bash
./scripts/sync_all_channels.sh
```

The script will:
1. Parse `data/channels.yaml`
2. Skip channels with `enabled: false`
3. Extract videos for each enabled channel
4. Wait 10 seconds between channels (rate limiting)
5. Report completion and next steps

### 4. Verify Results

After completion, check:
- Each channel folder exists in `data/`
- Each folder contains `videos.csv` with entries
- No persistent errors in output

```bash
# Quick verification
ls -la data/*/videos.csv | head -10
```

---

## Configuration

### Adding a New Channel

1. Add entry to `data/channels.yaml`:
   ```yaml
   - folder: new-channel-name
     url: https://www.youtube.com/@ChannelName/videos
     count: 50
     enabled: true
   ```

2. Run sync - folder is created automatically

> [!WARNING]
> Folder names should use lowercase with hyphens (e.g., `my-channel`). Avoid spaces or special characters.

### Disabling a Channel

Set `enabled: false` - the channel will be skipped during sync but data is preserved.

### Recommended Video Counts

| Channel Type | Recommended Count |
|-------------|-------------------|
| Infrequent posters (1-2/month) | 20 |
| Regular posters (weekly) | 50 |
| High-volume (daily) | 100 |
| Conference channels | 100-200 |

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `yq: command not found` | yq not installed | Run `brew install yq` |
| `Config file not found` | Running from wrong directory | Run from repo root: `./scripts/sync_all_channels.sh` |
| `Failed to sync [channel]` | Network issue or invalid URL | Check URL is accessible in browser, retry |
| Sync takes forever | Too many channels or high counts | Reduce counts or disable some channels |
| Empty videos.csv | Channel has no public videos or URL is wrong | Verify URL ends in `/videos` |
| Rate limit errors | Too many requests | Wait 1 hour and retry; reduce counts |

---

## Common Mistakes

1. **Wrong URL format** - Use `https://www.youtube.com/@ChannelName/videos` not `/channel/` or `/c/` URLs
2. **Running from wrong directory** - Must run from repo root, not from `scripts/`
3. **Forgetting to enable** - New channels default to `enabled: false` in templates
4. **Excessive counts** - Starting with `count: 500` causes long waits; start with 50
5. **Missing yq** - The script fails immediately without yq; install before first run

---

## Next Steps

After syncing channels:

```bash
# Download transcripts for all synced videos
./scripts/download_all_transcripts.sh
```

---

## Quality Checklist

Before running sync:
- [ ] `yq` is installed (`which yq`)
- [ ] Running from repository root
- [ ] `data/channels.yaml` exists and is valid YAML
- [ ] At least one channel has `enabled: true`

After sync completes:
- [ ] No persistent errors in output (warnings OK)
- [ ] Each enabled channel has `data/[folder]/videos.csv`
- [ ] CSV files contain video entries

---

## Rate Limiting Details

- **10 second delay** between channels (built into script)
- **Sequential processing** - one channel at a time
- **Graceful failure** - if one channel fails, others continue

> [!TIP]
> For overnight batch operations, run sync first, then download-all-transcripts. This sequence ensures video lists are current before downloading.
