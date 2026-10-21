---
name: bookmark-ninja
description: Converts browser bookmark HTML exports (Chrome, Firefox, Edge, Brave) into structured JSON or CSV indexes for agent consumption. Use whenever the user asks to parse, convert, organize, index, merge, deduplicate, or verify bookmarks, or when they want to turn a bookmark export into a queryable knowledge base. Supports incremental merging with conflict resolution and optional URL liveness checking.
license: MIT
compatibility: Requires python3. Optional dependency on the requests library for URL liveness checks.
metadata:
  author: Harold Mansfield
  version: 1.1.0
  homepage: https://github.com/SamaritanOC/Bookmark-Ninja
---

# Bookmark Ninja

This skill parses Netscape HTML bookmark exports (the universal format produced by Chrome, Firefox, Edge, and Brave) and produces structured JSON or CSV indexes ready for agent consumption. All processing is handled by `scripts/bookmark-parser.py`. The agent's role is to recognize when a bookmark task applies and invoke the script with the appropriate flags — no API keys, no external services, no configuration.

## When to Use This Skill

- **Convert browser bookmarks to agent-queryable format** — transform an exported HTML file into a structured JSON or CSV index
- **Build an incremental knowledge base** — merge periodic bookmark exports into a growing index without losing existing data
- **Organize accumulated research** — preserve full folder hierarchy as category breadcrumb paths (e.g., `Research > AI > Papers`)
- **Verify URL liveness** — identify dead links via HEAD request checks before querying
- **Merge multiple bookmark sources** — combine exports from different browsers or time periods with conflict resolution
- **Archive bookmarks before browser migration** — snapshot current bookmarks as a portable index before reorganizing

## How to Run the Script

The script lives at `scripts/bookmark-parser.py` relative to the skill folder. Use the path appropriate to the runtime environment.

**Basic parse** — reads an HTML export and writes `bookmarks-index.json`:
```bash
python3 scripts/bookmark-parser.py bookmarks.html
```

**Custom output path** — write the index to a specific location:
```bash
python3 scripts/bookmark-parser.py bookmarks.html -o ~/research/sources.json
```

**Merge with existing index** — add new bookmarks without overwriting; prompts interactively on conflicts:
```bash
python3 scripts/bookmark-parser.py new-bookmarks.html -o index.json --merge
```

**Auto-resolve merge conflicts** — skip interactive prompts by keeping old or new data:
```bash
# Keep the old entry on conflict
python3 scripts/bookmark-parser.py new-bookmarks.html -o index.json --merge --keep-old

# Keep the new entry on conflict
python3 scripts/bookmark-parser.py new-bookmarks.html -o index.json --merge --keep-new
```

**URL liveness check** — adds `"alive": true/false` to each entry (requires `requests`; note: slow on large collections):
```bash
python3 scripts/bookmark-parser.py bookmarks.html --check-alive -o verified.json
```

**Statistics only** — print a summary without writing any output file:
```bash
python3 scripts/bookmark-parser.py bookmarks.html --stats
```

**CSV output** — produce a CSV file instead of JSON:
```bash
python3 scripts/bookmark-parser.py bookmarks.html --format csv
```

**Both formats at once**:
```bash
python3 scripts/bookmark-parser.py bookmarks.html --format both
```

## Output Format

Each entry in the JSON array contains seven fields:

| Field | Description |
|---|---|
| `url` | The bookmark URL |
| `title` | Page title or user-defined name |
| `category` | Full folder hierarchy as breadcrumb (e.g., `Research > AI > Papers`) |
| `description` | Metadata attribute if present in the export |
| `date_added` | ISO 8601 timestamp converted from Unix ADD_DATE |
| `icon` | Favicon URL if present in the export |
| `alive` | `true` / `false` — only present when `--check-alive` was used |

Example entry:
```json
{
  "url": "https://dehashed.com/",
  "title": "DeHashed — #FreeThePassword",
  "category": "OSINT > Breach Data/Dumps",
  "description": "Searches breach, paste, or leak data for emails, usernames, and exposed records.",
  "date_added": "2026-03-14T09:20:00",
  "icon": "",
  "alive": true
}
```

For a multi-entry example, see `references/example-output.json`.

## Agent Query Patterns

```python
import json

with open("bookmarks-index.json") as f:
    bookmarks = json.load(f)

# Search by keyword (title or description)
keyword = "machine learning"
matches = [b for b in bookmarks if keyword.lower() in b["title"].lower()
           or keyword.lower() in b.get("description", "").lower()]

# Filter by category
email_tools = [b for b in bookmarks if "Email Search" in b["category"]]

# List all categories
categories = sorted(set(b["category"] for b in bookmarks))

# Find dead links (requires --check-alive run)
dead = [b for b in bookmarks if b.get("alive") == False]

# Recent bookmarks (last 30 days)
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=30)
recent = [b for b in bookmarks
          if b["date_added"] and datetime.fromisoformat(b["date_added"]) > cutoff]
```

## Command-Line Reference

```
usage: bookmark-parser.py [-h] [-o OUTPUT] [--format {json,csv,both}]
                          [--merge] [--keep-old] [--keep-new]
                          [--check-alive] [--stats]
                          input

Convert browser bookmarks to machine-readable index

positional arguments:
  input                 HTML bookmark file to parse

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (default: bookmarks-index.json)
  --format {json,csv,both}
                        Output format (default: json)
  --merge               Merge with existing index file
  --keep-old            On merge conflict, keep old entry (default: prompt)
  --keep-new            On merge conflict, keep new entry (default: prompt)
  --check-alive         Check URL liveness via HEAD request (adds latency)
  --stats               Print statistics only, don't save
```

## Workflow Example

1. **Initial import** — parse your first export:
   ```bash
   python3 scripts/bookmark-parser.py research-bookmarks.html -o research-library.json
   ```

2. **Monthly merges** — add each new export without losing history:
   ```bash
   python3 scripts/bookmark-parser.py bookmarks-june.html -o research-library.json --merge --keep-new
   ```

3. **Quarterly liveness check** — flag dead links before querying:
   ```bash
   python3 scripts/bookmark-parser.py bookmarks-current.html --check-alive -o research-library.json --merge --keep-new
   ```

4. **Agent queries the index** — load the JSON and filter programmatically using the patterns in the Agent Query Patterns section above.

## Troubleshooting

**"requests library not available" warning**
Liveness check requires `requests`. Install with `pip install requests`.

**Encoding errors on import**
The parser uses `errors="ignore"` for malformed HTML. If issues persist, re-export from the browser.

**Category hierarchy looks wrong**
Bookmark exports nest categories via `<DL>` tags. Ensure the export includes folder structure (not a flat list). In Chrome/Firefox, verify that folder structure is preserved during export.

**Merge conflicts on every entry**
Usually caused by date/time format changes between exports. Use `--keep-new` to auto-accept updated metadata without prompting.
