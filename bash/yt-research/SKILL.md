---
name: yt-research
description: Search YouTube for videos on any topic and return structured metadata (titles, views, authors, duration, URLs). Use when the user asks to research, find, or search for YouTube videos on a topic.
allowed-tools: Bash Read
argument-hint: <topic to research>
---

## YouTube Research Skill

Search YouTube for videos on a topic and return structured metadata.

### CRITICAL: If no topic is provided in `$ARGUMENTS`, you MUST ask the user what topic they want to research before proceeding. Do NOT guess or assume a topic.

### Usage

1. Activate the virtual environment and run the search script:

```bash
cd /home/user/Sneha && source .venv/bin/activate && python .claude/skills/yt-research/scripts/yt_search.py --query "<TOPIC>" --max-results <N> --sort <relevance|date>
```

### Parameters

- `--query` / `-q`: The search topic (REQUIRED - ask user if not provided)
- `--max-results` / `-n`: Number of videos to return (default: 10)
- `--sort`: Sort order
  - `relevance` (default): Most relevant results
  - `date`: Most recent uploads (use when user says "latest", "trending", "newest", or "recent")

### Interpreting User Requests

- "Find 25 latest videos on X" → `--query "X" -n 25 --sort date`
- "Search for videos about X" → `--query "X"` (defaults are fine)
- "25 trending videos on X" → `--query "X" -n 25 --sort date`

### Output

The script outputs a JSON array to stdout. Parse it and present results as a formatted table with columns: #, Title, Author, Views, Duration, URL.

### Example Output

```json
[
  {
    "title": "Video Title",
    "url": "https://www.youtube.com/watch?v=...",
    "author": "Channel Name",
    "views": 123456,
    "duration": "12:34",
    "upload_date": "20250401"
  }
]
```

Format views with commas (e.g., 123,456) and upload_date as readable dates (e.g., "Apr 1, 2025").
