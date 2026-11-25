---
name: raindrop
description: Manage bookmarks, collections, tags, and highlights in Raindrop.io using the REST API.
---

# Raindrop.io API Skill

## Purpose

This skill provides direct access to the Raindrop.io bookmark manager via its REST API. Use it to save, search, organize, and manage bookmarks (called "raindrops"), collections, tags, and highlights.

**Requires `RAINDROP_TOKEN` to be set in your environment.**

## Authentication

All requests use a Bearer token:

```bash
Authorization: Bearer $RAINDROP_TOKEN
```

Base URL: `https://api.raindrop.io/rest/v1`

Rate limit: **120 requests per minute** per authenticated user. HTTP 429 is returned when exceeded.

---

## Collections

Collections are folders/groups for bookmarks. System collections use special IDs:

| ID   | Name        |
|------|-------------|
| `0`  | All (except Trash) |
| `-1` | Unsorted    |
| `-99`| Trash       |

### Get all root collections

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/collections
```

### Get all child (nested) collections

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/collections/childrens
```

### Get a single collection

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/collection/{id}
```

### Create a collection

```bash
curl -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Collection", "public": false}' \
  https://api.raindrop.io/rest/v1/collection
```

**Body fields:**

| Field      | Type    | Description                                      |
|------------|---------|--------------------------------------------------|
| `title`    | string  | Collection name                                  |
| `public`   | boolean | Accessible without authentication?               |
| `view`     | string  | `list`, `simple`, `grid`, `masonry`              |
| `sort`     | number  | Sort order (descending)                          |
| `parent.$id` | integer | Parent collection ID (omit for root collections)|
| `cover`    | array   | Cover image URLs                                 |

### Update a collection

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Renamed Collection"}' \
  https://api.raindrop.io/rest/v1/collection/{id}
```

### Remove a collection

Moves the collection and its descendants to Trash. Raindrops move to Trash.

```bash
curl -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/collection/{id}
```

### Empty Trash

```bash
curl -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/collection/-99
```

### Get system collection counts

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/user/stats
```

---

## Raindrops (Bookmarks)

### Get a single raindrop

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

### Get multiple raindrops from a collection

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/{collectionId}?perpage=25&page=0"
```

**Query parameters:**

| Parameter    | Type    | Description                                                     |
|--------------|---------|-----------------------------------------------------------------|
| `sort`       | string  | `-created` (default), `created`, `score`, `-sort`, `title`, `-title`, `domain`, `-domain` |
| `perpage`    | integer | Results per page (max 50)                                       |
| `page`       | integer | Page number starting at 0                                       |
| `search`     | string  | Search query (see Search Operators below)                       |
| `nested`     | boolean | Include bookmarks from nested collections                       |

### Create a single raindrop

```bash
curl -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "link": "https://example.com",
    "title": "Example",
    "excerpt": "A description",
    "tags": ["tag1", "tag2"],
    "collection": {"$id": 12345},
    "important": false,
    "pleaseParse": {}
  }' \
  https://api.raindrop.io/rest/v1/raindrop
```

Set `"pleaseParse": {}` to auto-fetch title, cover, and description from the URL.

**Body fields:**

| Field         | Type    | Description                                 |
|---------------|---------|---------------------------------------------|
| `link`*       | string  | URL (required)                              |
| `title`       | string  | Title (max 1000 chars)                      |
| `excerpt`     | string  | Description (max 10000 chars)               |
| `note`        | string  | Personal note (max 10000 chars)             |
| `tags`        | array   | List of tag strings                         |
| `important`   | boolean | Mark as favourite                           |
| `collection`  | object  | `{"$id": collectionId}`                     |
| `pleaseParse` | object  | `{}` to auto-parse metadata from URL        |
| `order`       | number  | Sort position (0 = first)                   |
| `cover`       | string  | Cover image URL                             |
| `highlights`  | array   | Initial highlights                          |

### Update a single raindrop

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["newtag"], "important": true}' \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

### Remove a single raindrop

Moves to Trash. Remove from Trash to permanently delete.

```bash
curl -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

### Create many raindrops (bulk, max 100)

```bash
curl -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"link": "https://example.com", "title": "Example 1"},
      {"link": "https://another.com", "title": "Example 2"}
    ]
  }' \
  https://api.raindrop.io/rest/v1/raindrops
```

### Update many raindrops

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [111, 222], "tags": ["bulk-tag"]}' \
  https://api.raindrop.io/rest/v1/raindrops/{collectionId}
```

### Remove many raindrops

Moves to Trash. When `collectionId` is `-99`, permanently deletes.

```bash
curl -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [111, 222]}' \
  https://api.raindrop.io/rest/v1/raindrops/{collectionId}
```

### Suggest collection and tags for a URL

```bash
curl -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"link": "https://github.com/some/repo"}' \
  https://api.raindrop.io/rest/v1/raindrop/suggest
```

---

## Search Operators

Use these in the `search` query parameter:

| Operator             | Example                  | Description                          |
|----------------------|--------------------------|--------------------------------------|
| Plain text           | `javascript tutorial`    | Full-text search                     |
| `#tag`               | `#python`                | Filter by tag                        |
| `site:domain`        | `site:github.com`        | Filter by hostname                   |
| `type:value`         | `type:article`           | Type: `link`, `article`, `image`, `video`, `document`, `audio` |
| `important:true`     | `important:true`         | Favourited only                      |
| `created:>DATE`      | `created:>2024-01-01`    | Created after date (ISO 8601)        |
| `created:<DATE`      | `created:<2024-12-31`    | Created before date                  |

Combine operators: `#python site:github.com type:article`

---

## Tags

### Get all tags (optionally scoped to a collection)

```bash
# All tags
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/tags

# Tags in a specific collection
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/tags/{collectionId}
```

Response: `{"result": true, "items": [{"_id": "tagname", "count": 42}]}`

### Rename a tag

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["oldname"], "replace": "newname"}' \
  https://api.raindrop.io/rest/v1/tags
```

### Merge tags into one

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["js", "javascript", "ecmascript"], "replace": "javascript"}' \
  https://api.raindrop.io/rest/v1/tags
```

### Delete tag(s)

```bash
curl -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["obsolete-tag"]}' \
  https://api.raindrop.io/rest/v1/tags
```

---

## Highlights

A highlight is a text excerpt saved from within a bookmark. Colors: `blue`, `brown`, `cyan`, `gray`, `green`, `indigo`, `orange`, `pink`, `purple`, `red`, `teal`, `yellow` (default: `yellow`).

### Get all highlights (paginated)

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/highlights?perpage=25&page=0"
```

### Get highlights in a collection

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/highlights/{collectionId}
```

### Get highlights of a specific raindrop

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  https://api.raindrop.io/rest/v1/raindrop/{id}
# highlights[] array is inside the item object
```

### Add a highlight to a raindrop

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "highlights": [
      {"text": "Some quoted text", "color": "yellow", "note": "My note"}
    ]
  }' \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

### Update a highlight

Include the highlight `_id` and only the fields to change:

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"highlights": [{"_id": "62388e9e48b63606f41e44a6", "note": "Updated note"}]}' \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

### Remove a highlight

Set `text` to an empty string:

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"highlights": [{"_id": "62388e9e48b63606f41e44a6", "text": ""}]}' \
  https://api.raindrop.io/rest/v1/raindrop/{id}
```

---

## Raindrop Fields Reference

| Field          | Type    | Description                                                   |
|----------------|---------|---------------------------------------------------------------|
| `_id`          | integer | Unique identifier                                             |
| `link`         | string  | URL                                                           |
| `title`        | string  | Title (max 1000 chars)                                        |
| `excerpt`      | string  | Description (max 10000 chars)                                 |
| `note`         | string  | Personal note (max 10000 chars)                               |
| `type`         | string  | `link`, `article`, `image`, `video`, `document`, `audio`      |
| `tags`         | array   | List of tag strings                                           |
| `important`    | boolean | Marked as favourite                                           |
| `collection.$id` | integer | Collection ID                                               |
| `cover`        | string  | Cover image URL                                               |
| `domain`       | string  | Hostname (files always show `raindrop.io`)                    |
| `created`      | string  | ISO 8601 creation date                                        |
| `lastUpdate`   | string  | ISO 8601 last updated date                                    |
| `highlights`   | array   | List of highlight objects                                     |
| `broken`       | boolean | Original URL is unreachable                                   |

---

## Workflow Examples

### Save a new bookmark

```bash
curl -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "link": "https://example.com/article",
    "collection": {"$id": -1},
    "tags": ["reading"],
    "pleaseParse": {}
  }' \
  https://api.raindrop.io/rest/v1/raindrop
```

### Search bookmarks about TypeScript

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=typescript&perpage=20"
```

### List all bookmarks in a collection with pagination

```bash
curl -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/52644516?perpage=50&page=0&sort=-created"
```

### Move bookmarks to a different collection

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [111, 222], "collection": {"$id": 99999}}' \
  https://api.raindrop.io/rest/v1/raindrops/0
```

### Add tags to multiple bookmarks

```bash
curl -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [111, 222], "tags": ["new-tag"]}' \
  https://api.raindrop.io/rest/v1/raindrops/0
```

---

## Error Handling

- `result: true` → success
- `result: false` → failure; check `error` and `errorMessage` fields
- HTTP 429 → rate limit exceeded; retry after `X-RateLimit-Reset` timestamp
- HTTP 4xx → bad request, do not retry without changes
- HTTP 5xx → server error, safe to retry

## Best Practices

1. Use `pleaseParse: {}` when saving new bookmarks to auto-fetch metadata.
2. Use `search` with operators like `#tag site:domain` to filter precisely.
3. Use `perpage=50` (max) with `page` for efficient pagination.
4. Use bulk create (`POST /raindrops`) for importing multiple links at once (max 100 per request).
5. Collection ID `0` reads all bookmarks but cannot be used for bulk update/delete — use the specific collection ID instead.
6. Trash (`-99`) permanently deletes when you remove from it; use regular remove for soft-delete.
