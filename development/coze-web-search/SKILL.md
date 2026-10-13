---
name: coze-web-search
description: Search the web using coze-coding-dev-sdk. Supports web search, image search, AI summaries, time filters, and site restrictions.
homepage: https://www.coze.com
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["npx"] } } }
---

# Coze Web Search

Search the web using coze-coding-dev-sdk. Returns structured results with URLs, snippets, and AI summaries.

## Quick Start

### Basic Search

```bash
npx ts-node {baseDir}/scripts/search.ts -q "Python programming"
```

### With Time Filter

```bash
npx ts-node {baseDir}/scripts/search.ts \
  -q "AI news" \
  --time-range 1w \
  --count 15
```

### Site-Specific Search

```bash
npx ts-node {baseDir}/scripts/search.ts \
  -q "Python tutorials" \
  --sites "python.org,github.com,stackoverflow.com"
```

### Image Search

```bash
npx ts-node {baseDir}/scripts/search.ts \
  -q "mountain landscape" \
  --type image \
  --count 20
```

### Output as Markdown

```bash
npx ts-node {baseDir}/scripts/search.ts \
  -q "machine learning" \
  --format markdown
```

## Script Options

| Option                    | Description                                |
| ------------------------- | ------------------------------------------ |
| `-q, --query <text>`      | Search query (required)                    |
| `--type <type>`           | `web` or `image` (default: web)            |
| `--count <n>`             | Number of results (default: 10)            |
| `--time-range <range>`    | `1d`, `1w`, `1m` (web only)                |
| `--sites <domains>`       | Comma-separated domains to include         |
| `--block-hosts <domains>` | Comma-separated domains to exclude         |
| `--no-summary`            | Disable AI summary                         |
| `--need-content`          | Include full page content                  |
| `--format <fmt>`          | `json`, `text`, `markdown` (default: text) |

## Time Range

| Value | Description   |
| ----- | ------------- |
| `1d`  | Last 24 hours |
| `1w`  | Last week     |
| `1m`  | Last month    |

## Output Formats

### Text (default)

```
============================================================
AI SUMMARY
============================================================
Python is a high-level programming language...

============================================================
SEARCH RESULTS (10 items)
============================================================

[1] Python.org
    URL: https://www.python.org
    Source: Python Software Foundation
    The official home of the Python Programming Language...
```

### Markdown

Formatted with headers, links, and collapsible content sections.

### JSON

Raw API response.

## Notes

- Use `--time-range` for recent content
- Use `--sites` to limit to trusted sources
- Use `--need-content` sparingly (increases response size)
