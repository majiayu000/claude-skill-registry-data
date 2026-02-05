---
name: add-video-to-collection
description: Manually add individual YouTube URLs to a custom collection CSV. Use when adding one-off videos to folders like library-of-minds or random, not from a channel extraction.
---

# Add Video to Collection

**Why?** Curated collections contain videos from multiple sources—manually editing CSVs causes formatting bugs and duplicates. This skill uses the CLI to add videos safely.

## Quick Start

```bash
transcript-add <youtube-url> --csv data/<collection>/videos.csv
```

| Collection | CSV Path |
|------------|----------|
| library-of-minds | `data/library-of-minds/videos.csv` |
| random | `data/random/videos.csv` |

---

## Workflow

### 1. Identify the Target Collection

Determine which collection the video belongs to:

| If the video is... | Use collection |
|--------------------|----------------|
| Thought leader, interview, educational | `library-of-minds` |
| Miscellaneous, one-off interesting content | `random` |
| User specifies a collection | Use that collection |

### 2. Run the CLI Command

```bash
transcript-add <youtube-url> --csv data/<collection>/videos.csv
```

> [!CAUTION]
> **NEVER manually edit CSV files** to add videos. Always use `transcript-add` to ensure proper formatting and duplicate detection.

**Examples:**

```bash
# Add to library-of-minds
transcript-add https://www.youtube.com/watch?v=dQw4w9WgXcQ --csv data/library-of-minds/videos.csv

# Add to random collection
transcript-add https://www.youtube.com/watch?v=jNQXAC9IVRw --csv data/random/videos.csv

# Verbose output for debugging
transcript-add https://www.youtube.com/watch?v=9bZkp7q19f0 --csv data/random/videos.csv -v
```

### 3. Verify the Output

| Output | Meaning |
|--------|---------|
| `✓ Added video XXX to ...` | Success — video was added |
| `⊘ Video XXX already exists in ...` | Duplicate — no action needed |
| Error message | See Troubleshooting below |

### 4. Offer Transcript Download (Optional)

After adding, ask the user if they want to download the transcript:

```bash
transcript-download --csv data/<collection>/videos.csv --output-dir data/<collection>/transcripts
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `command not found: transcript-add` | CLI not installed | Run `pip install -e .` from project root |
| `Invalid YouTube URL` | Malformed URL | Use full URL: `https://www.youtube.com/watch?v=VIDEO_ID` |
| `Permission denied` | File permissions | Check write access to `data/` directory |
| `CSV file not found` | Collection doesn't exist | Create directory first: `mkdir -p data/<collection>` |
| Video not appearing in CSV | Silent failure | Run with `-v` flag to see debug output |

---

## Common Mistakes

1. **Editing CSV directly** — Causes newline corruption and duplicate entries. Always use CLI.
2. **Using short URLs** — `youtu.be/XXX` may not work. Use full `youtube.com/watch?v=XXX` format.
3. **Wrong collection** — Double-check the collection name matches an existing folder.
4. **Forgetting to download transcript** — Adding to CSV doesn't download content. Run `transcript-download` separately.

---

## Reference

**What the CLI handles automatically:**
- Duplicate detection (skips existing URLs)
- URL normalization to canonical format
- Proper CSV escaping and formatting
- Header creation for new CSV files

**Metadata populated during transcript download:**
- Video title
- Duration
- Upload date
- Channel name
