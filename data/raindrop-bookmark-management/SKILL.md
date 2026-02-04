---
name: Raindrop Bookmark Management
description: Manage bookmarks with Raindrop.io MCP server. Use when saving URLs, organizing bookmarks into collections, tagging content, searching saved links, or managing highlights. Covers bookmark CRUD, collection organization, tag management, and URL parsing.
keywords: [raindrop, bookmarks, collections, tags, highlights, save, organize, search]
topics: [knowledge-management, bookmarks, research, web-clipping]
---

# Raindrop Bookmark Management

Guide for using the Raindrop.io MCP server to manage bookmarks effectively.

## Available MCP Tools

### Bookmark Operations

| Tool | Purpose |
|------|---------|
| `create-raindrop` | Save a new bookmark with optional metadata |
| `create-raindrops-bulk` | Batch save multiple bookmarks (up to 50) |
| `get-raindrop` | Get details of a specific bookmark |
| `list-raindrops` | List bookmarks from a collection |
| `update-raindrop` | Modify bookmark properties |
| `delete-raindrop` | Move to trash or permanently delete |
| `search-raindrops` | Full-text and operator search |

### Collection Operations

| Tool | Purpose |
|------|---------|
| `list-collections` | Get all collections (folders) |
| `get-collection` | Get specific collection details |
| `create-collection` | Create new collection |
| `update-collection` | Modify collection properties |
| `delete-collection` | Remove collection (bookmarks go to trash) |

### Tag Operations

| Tool | Purpose |
|------|---------|
| `list-tags` | Get all tags with counts |
| `merge-tags` | Rename or consolidate tags |
| `delete-tags` | Remove tags from bookmarks |

### Other Tools

| Tool | Purpose |
|------|---------|
| `list-highlights` | Get text highlights from articles |
| `parse-url` | Preview URL metadata before saving |
| `check-url-exists` | Check for duplicate bookmarks |

## Special Collection IDs

- `0` - All bookmarks across collections
- `-1` - Unsorted (default for new bookmarks)
- `-99` - Trash

## Search Operators

```text
#tag              Search by tag
site:example.com  Filter by domain
type:article      Filter by type (article/image/video/document/audio)
important:true    Favorites only
created:YYYY-MM-DD  Date filter
```

## Field Presets

Optimize response size with presets:

| Preset | Fields Included |
|--------|-----------------|
| `minimal` | _id, link, title |
| `basic` | + excerpt, tags, created, domain |
| `standard` | + note, type, cover, lastUpdate, important |
| `media` | _id, link, title, cover, media, type, file |
| `organization` | _id, title, tags, collection, collectionId, sort, removed |
| `metadata` | _id, created, lastUpdate, creatorRef, user, broken, cache |

## Common Workflows

### Save URL with Tags

```text
Use create-raindrop with:
- link: "https://example.com/article"
- tags: ["research", "ai"]
- collectionId: 12345 (or omit for Unsorted)
- pleaseParse: true (auto-extract metadata)
```

### Organize Bookmarks

```text
1. list-collections to see available folders
2. create-collection for new category
3. update-raindrop with collectionId to move items
```

### Clean Up Tags

```text
1. list-tags to see all tags with counts
2. merge-tags to consolidate similar tags
3. delete-tags to remove unused ones
```

### Research Workflow

```text
1. parse-url to preview before saving
2. check-url-exists to avoid duplicates
3. create-raindrop to save with notes
4. search-raindrops later to find content
```

## Environment Setup

Requires `RAINDROP_TOKEN` environment variable. Get your token from:
https://app.raindrop.io/settings/integrations

Set in `~/.dotfiles/local/.env`:
```bash
export RAINDROP_TOKEN="your-token-here"
```
