---
name: arena-cli
description: >
  CLI tools for Are.na: export blocks, enrich with vision AI, generate views.
  Use when: (1) exporting Are.na blocks incrementally, (2) enriching images with
  AI-generated titles/tags/patterns, (3) generating browsable HTML views,
  (4) searching blocks by UI patterns or tags, (5) visual search results when
  terminal output is insufficient. Triggers: "export arena", "enrich arena",
  "sync arena", "arena view", "search arena for [pattern]", "show me [pattern]".
---

# arena-cli

CLI tools to export, enrich, and browse Are.na blocks locally.

## Setup

First-time setup requires:

```bash
# In your project directory
echo "ARENA_TOKEN=your_token_here" >> .env
echo "ARENA_USER_SLUG=your_username" >> .env
echo "GEMINI_API_KEY=your_key_here" >> .env
```

Get your Are.na token from: https://dev.are.na/oauth/applications

## Workflow

```
1. Export    →    2. Enrich    →    3. View/Search
   (blocks)       (vision AI)        (HTML + grep)
```

### 1. Export Blocks

```bash
# First run - exports all channels
npx ts-node scripts/export-blocks.ts

# Incremental update (only new blocks)
npx ts-node scripts/export-blocks.ts

# Specific channel
npx ts-node scripts/export-blocks.ts --channel=ui-ux-abc123

# With local image download
npx ts-node scripts/export-blocks.ts --images
```

Output: `arena-export/blocks/{id}.json`

### 2. Enrich with Vision AI

```bash
# Enrich all image blocks
npx ts-node scripts/enrich-blocks.ts

# Specific channel
npx ts-node scripts/enrich-blocks.ts --channel=ui-ux-abc123

# Preview without saving
npx ts-node scripts/enrich-blocks.ts --dry-run

# Re-enrich already processed
npx ts-node scripts/enrich-blocks.ts --force
```

Adds to each block:
- `vision.suggested_title` - Clean title
- `vision.description` - What's notable
- `vision.tags` - Searchable tags
- `vision.ui_patterns` - UI component patterns

### 3. Generate View

```bash
# Generate HTML
node scripts/gen-view.cjs

# Generate and open
node scripts/gen-view.cjs --open
```

Output: `arena-export/view.html`

### 4. Visual Search Results

When terminal output is insufficient (need to see actual images):

```bash
# Ad-hoc search - comma-separated patterns
node scripts/gen-search-view.cjs "dashboard,metric-cards" --open

# Multiple search groups
node scripts/gen-search-view.cjs "avatar,profile" "chart,graph" --open

# From config file
node scripts/gen-search-view.cjs --config=searches.json --open
```

Config file format (`searches.json`):
```json
[
  { "name": "Dashboards", "patterns": ["dashboard", "metric-cards", "kpi"] },
  { "name": "Charts", "patterns": ["chart", "graph", "visualization"] }
]
```

Output: `arena-export/search-results.html` with image grid, grouped by category.

## Searching

```bash
# Search by UI pattern
grep -l "inline-stats" arena-export/blocks/*.json

# Search by tag
grep -l '"dashboard"' arena-export/blocks/*.json

# Search with context
grep -B2 -A2 "leaderboard" arena-export/blocks/*.json
```

## Block Schema

```json
{
  "id": 12345,
  "title": "original-filename.png",
  "class": "Image",
  "image_url": "https://...",
  "channels": ["ui-ux-abc"],
  "vision": {
    "suggested_title": "Dark Trading Dashboard",
    "description": "Crypto dashboard with real-time charts",
    "tags": ["dashboard", "dark-mode", "trading"],
    "ui_patterns": ["metric-cards", "time-series-chart"]
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ARENA_TOKEN` | Yes | Are.na API token |
| `ARENA_USER_SLUG` | Yes | Your Are.na username |
| `GEMINI_API_KEY` | Yes | Google AI API key |
| `ARENA_EXPORT_DIR` | No | Export path (default: ./arena-export) |

## Customization

To customize the vision enrichment prompt, see [references/enrichment-prompt.md](references/enrichment-prompt.md).
