---
name: graphthulhu
description: Knowledge graph MCP server for Logseq and Obsidian. 37 tools for reading, writing, searching, and analyzing your second brain.
metadata:
  openclaw:
    requires:
      bins:
        - graphthulhu
---

# graphthulhu

MCP server that gives you full access to a Logseq or Obsidian knowledge graph. 37 tools across 9 categories: navigate, search, analyze, write, decisions, journals, flashcards, whiteboards, and health.

## Install

Download the binary for your platform from [GitHub Releases](https://github.com/skridlevsky/graphthulhu/releases) and put it on your PATH.

Or: `go install github.com/skridlevsky/graphthulhu@latest`

## Configure

### Obsidian

Add to your MCP settings:

```json
{
  "mcpServers": {
    "graphthulhu": {
      "command": "graphthulhu",
      "args": ["--backend", "obsidian", "--vault", "/path/to/your/vault"]
    }
  }
}
```

No plugins required. Reads `.md` files directly. Full read-write support.

### Logseq

Enable the HTTP API server in Logseq (Settings > Features > HTTP APIs server), start it, and create a token.

```json
{
  "mcpServers": {
    "graphthulhu": {
      "command": "graphthulhu",
      "env": {
        "LOGSEQ_API_URL": "http://127.0.0.1:12315",
        "LOGSEQ_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

## What you can do

- **Navigate** — get pages with full block trees, traverse the link graph, list pages by namespace/tag/property
- **Search** — full-text search with context, property queries, tag hierarchy search, raw Datalog (Logseq)
- **Analyze** — graph overview, find connections between pages, detect knowledge gaps and orphans, discover topic clusters
- **Write** — create pages, append/upsert blocks with nested children, update/delete/move blocks, link pages bidirectionally, rename pages with link updates, bulk update properties
- **Decisions** — create decisions with deadlines, check status, resolve or defer with tracking
- **Journals** — read entries by date range, search within journals
- **Flashcards** — SRS stats, due cards, create new cards (Logseq)
- **Whiteboards** — list and inspect spatial canvases (Logseq)

## Links

- [GitHub](https://github.com/skridlevsky/graphthulhu)
- [Full tool reference](https://github.com/skridlevsky/graphthulhu#tools)
