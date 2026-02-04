---
name: raindrop
description: Manage Raindrop.io bookmarks, collections, tags, and highlights via API. Use when user mentions raindrop, bookmarks, saving links, organizing URLs, bookmark collections, or web highlights.
---

# Raindrop.io API Skill

Manage bookmarks via Raindrop.io REST API.

## Prerequisites

User must have `RAINDROP_TOKEN` env var set. If not configured, instruct them to:
1. Create app at https://app.raindrop.io/settings/integrations
2. Generate test token
3. Add `export RAINDROP_TOKEN="..."` to `~/.zshrc.local`

## Authentication

All requests require:
```
Authorization: Bearer $RAINDROP_TOKEN
```

## Base URL

```
https://api.raindrop.io/rest/v1/
```

## Helper Script

Use `scripts/raindrop.sh` for API calls:
```bash
./scripts/raindrop.sh GET /collections
./scripts/raindrop.sh POST /raindrop '{"link":"https://example.com","pleaseParse":{}}'
./scripts/raindrop.sh PUT /raindrop/123 '{"tags":["new-tag"]}'
./scripts/raindrop.sh DELETE /raindrop/123
```

## Quick Reference

### Collections

| Action | Method | Endpoint |
|--------|--------|----------|
| List root | GET | `/collections` |
| List children | GET | `/collections/childrens` |
| Get one | GET | `/collection/{id}` |
| Create | POST | `/collection` |
| Update | PUT | `/collection/{id}` |
| Delete | DELETE | `/collection/{id}` |

### Raindrops (Bookmarks)

| Action | Method | Endpoint |
|--------|--------|----------|
| List | GET | `/raindrops/{collectionId}` |
| Get one | GET | `/raindrop/{id}` |
| Create | POST | `/raindrop` |
| Update | PUT | `/raindrop/{id}` |
| Delete | DELETE | `/raindrop/{id}` |
| Search | GET | `/raindrops/0?search=...` |

Special collection IDs: `0` = all, `-1` = unsorted, `-99` = trash

### Tags

| Action | Method | Endpoint |
|--------|--------|----------|
| List all | GET | `/tags` |
| List in collection | GET | `/tags/{collectionId}` |
| Rename | PUT | `/tags/{collectionId}` |
| Delete | DELETE | `/tags/{collectionId}` |

### Highlights

| Action | Method | Endpoint |
|--------|--------|----------|
| List all | GET | `/highlights` |
| In collection | GET | `/highlights/{collectionId}` |
| Add/Update/Remove | PUT | `/raindrop/{id}` |

Colors: blue, brown, cyan, gray, green, indigo, orange, pink, purple, red, teal, yellow

## Common Operations

### Create bookmark with auto-parse

```bash
./scripts/raindrop.sh POST /raindrop '{
  "link": "https://example.com",
  "collection": {"$id": 12345},
  "tags": ["tag1", "tag2"],
  "pleaseParse": {}
}'
```

### Search bookmarks

```bash
./scripts/raindrop.sh GET '/raindrops/0?search=keyword&sort=-created'
```

Search operators:
- `#tag` - by tag
- `type:article` - by type (link, article, image, video, document, audio)
- `domain:example.com` - by domain
- `created:>2024-01-01` - by date
- `important:true` - favorites only

### Create collection

```bash
./scripts/raindrop.sh POST /collection '{
  "title": "My Collection",
  "public": false
}'
```

### Add highlight to bookmark

```bash
./scripts/raindrop.sh PUT /raindrop/123 '{
  "highlights": [{"text": "highlighted text", "color": "yellow", "note": "my note"}]
}'
```

### Bulk tag bookmarks

```bash
./scripts/raindrop.sh PUT /raindrops/0 '{
  "ids": [1, 2, 3],
  "tags": ["new-tag"]
}'
```

### Export collection

```bash
curl -s "https://api.raindrop.io/rest/v1/raindrops/{collectionId}/export.csv" \
  -H "Authorization: Bearer $RAINDROP_TOKEN" > bookmarks.csv
```

Formats: csv, html, zip

## Rate Limits

120 requests/minute. Check headers: `X-RateLimit-Limit`, `RateLimit-Remaining`, `X-RateLimit-Reset`

## Detailed Reference

See [references/API-REFERENCE.md](references/API-REFERENCE.md) for complete endpoint documentation.
