---
name: safari-tabs
description: Interact with Safari browser tabs, reading list, bookmarks, and history via AppleScript. Use when the user asks to analyze, organize, summarize, deduplicate, close, export, or manage their Safari tabs. Also handles reading list, bookmarks, and history searches. Triggers include "my tabs", "open tabs", "Safari tabs", "clean up my browser", "what tabs do I have open", "organize my tabs", "too many tabs", "reading list", "bookmarks", "browser history", "export tabs". Requires macOS with Safari.
---

# Safari Tabs

Safari browser management via AppleScript.

## Key Scripts

| Script | Purpose |
|--------|---------|
| `get_tabs.sh` | Get tabs with optional window filtering (TSV/markdown/JSON) |
| `close_by_pattern.sh` | **RECOMMENDED**: Close tabs matching URL pattern |
| `close_tabs.sh` | Close by window,tab index (advanced) |
| `find_duplicates.sh` | Find/close duplicate tabs |
| `domain_stats.sh` | Analyze tabs by domain |
| `export_tabs_*.sh` | Export as JSON/CSV/markdown/HTML |
| `get_reading_list.sh` | Export Reading List |
| `get_bookmarks.sh` | Export bookmarks |
| `search_history.sh` | Search history |
| `open_urls.sh` | Open URLs from file/stdin |

## Getting Tabs

```bash
get_tabs.sh                    # All tabs as TSV
get_tabs.sh markdown           # All tabs as markdown
get_tabs.sh -w 1 markdown      # Window 1 only
get_tabs.sh -m "term" markdown # Window containing "term"
```

## Closing Tabs

**Always use `close_by_pattern.sh`** (finds tabs by URL regardless of position):

```bash
close_by_pattern.sh "unique-url-substring"

# Examples
close_by_pattern.sh "adrianroselli.com"
close_by_pattern.sh "/article/css-has-guide"
```

Closes ALL matching tabs across all windows. Use unique substring.

**Alternative: close by position** (error-prone, avoid unless necessary):
```bash
close_tabs.sh "1,5" "2,3"  # Window,tab pairs (1-indexed)
```

## Analysis Workflow

1. Fetch: `get_tabs.sh markdown`
2. Analyze: group by domain, identify duplicates/clusters, flag stale content
3. Report: stats, categorized list, suggestions
4. Act: close with `close_by_pattern.sh "url-substring"`

**Process-and-close pattern:**
1. Fetch tab
2. Process it
3. Close: `close_by_pattern.sh "unique-url-part"`
4. Next tab

## Export Formats

```bash
export_tabs_markdown.sh [list|table|checklist|grouped]
export_tabs_json.sh
export_tabs_csv.sh
export_tabs_html.sh > bookmarks.html  # Importable format
```

## Other Features

**Duplicates**: `find_duplicates.sh [--close]`
**Domain stats**: `domain_stats.sh`
**Reading list**: `get_reading_list.sh [tsv|markdown|json]`
**Bookmarks**: `get_bookmarks.sh [tree|flat|json]`
**History**: `search_history.sh [term] [--days N]`
**Open URLs**: `open_urls.sh urls.txt` or pipe stdin

**Privacy**: Tab data stays local. Page content not accessed unless explicitly requested.
