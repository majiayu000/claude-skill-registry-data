---
name: museum-search
description: Search the Met Museum Open Access Paintings collection using semantic search, find similar artworks, and search by image. Use this when users ask about art, paintings, museum collections, or want to find artworks by description, visual similarity, or artist.
---

# Met Museum Paintings Semantic Search

Search ~2,300 paintings from the Met Museum Open Access collection using AI-powered semantic search.

**Keywords**: art search, museum, paintings, Met Museum, semantic search, artwork discovery, visual similarity, art history

## When to Use This Skill

Use this skill when users:
- Ask to find artworks by description ("find paintings of people on bridges")
- Want to explore museum collections
- Ask about specific artworks or artists at the Met
- Want to find visually similar artworks
- Upload an image to find matching paintings

## API Base URL

```
https://museum-semantic-search.vercel.app/api/mcp
```

## API Endpoints

### POST /search - Search Artworks

Search the collection using text queries with optional filters.

```bash
curl -X POST https://museum-semantic-search.vercel.app/api/mcp/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "person with a dog",
    "mode": "semantic",
    "limit": 10
  }'
```

**Request body:**
```json
{
  "query": "string (required)",
  "mode": "hybrid | semantic | keyword",
  "detail": "minimal | standard | full",
  "filters": {
    "artistName": "string (fuzzy matched)",
    "yearStart": 1800,
    "yearEnd": 1900,
    "department": "string (exact match)",
    "culture": "string (exact match)",
    "classification": "string (exact match)",
    "tags": ["string (exact match)"],
    "medium": "string (fuzzy matched)",
    "country": "string (exact match)",
    "onView": true,
    "isPublicDomain": true
  },
  "limit": 10,
  "offset": 0
}
```

**Mode selection:**
- **"hybrid"** (default, recommended): Combines keyword + semantic search. Best for most queries.
- **"semantic"**: For purely conceptual/descriptive queries like "lonely figure in nature", "woman looking in mirror", "stormy seascape"
- **"keyword"**: For exact matches like artist names or specific titles

**Detail levels:**
- **"minimal"**: Just id, score, title, artist, date (fastest)
- **"standard"** (default): + medium, classification, department, tags, culture, image_url, source_url, alt_text (concise AI description)
- **"full"**: + long_description (detailed AI description), similar_artworks, dimensions, etc. Use when you need to verify semantic content.

**Response:**
```json
{
  "meta": {
    "query": "person with a dog",
    "mode": "hybrid",
    "total": 150,
    "returned": 10,
    "offset": 0,
    "limit": 10,
    "has_more": true,
    "filters_applied": {},
    "processing_time_ms": 234
  },
  "results": [
    {
      "id": "met_436524",
      "score": 0.85,
      "title": "A Boy with a Flying Squirrel",
      "artist": "John Singleton Copley",
      "date": "1765",
      "medium": "Oil on canvas",
      "classification": "Paintings",
      "department": "American Wing",
      "image_url": "https://images.metmuseum.org/...",
      "thumbnail_url": "https://images.metmuseum.org/.../small/...",
      "tags": ["Boys", "Portraits", "Squirrels"],
      "culture": "American",
      "source_url": "https://www.metmuseum.org/art/collection/search/436524",
      "alt_text": "Portrait of a young boy in blue satin holding a gold chain attached to a pet flying squirrel on a polished table"
    }
  ]
}
```

### GET /artwork/{id} - Get Artwork Details

Get complete details for a specific artwork.

```bash
curl https://museum-semantic-search.vercel.app/api/mcp/artwork/met_436524
```

**Response includes:**
- Basic info: title, titles (alternate), artist, artists (with roles, bio, dates)
- Dates: date, date_start, date_end
- Physical: medium, dimensions
- Classification: classification, department, object_name
- Context: culture, period, dynasty, country, region
- Collection: collection, collection_id, credit_line, accession_year
- Status: is_public_domain, is_highlight, on_view, gallery_number
- Image: url, thumbnail_url, width, height
- AI description: alt_text, long_description, emoji_summary
- Tags: array of keywords
- Similar artworks: id, similarity_type, confidence, explanation
- Links: source_url (Met Museum page)

### GET /similar/{id} - Find Similar Artworks

Find artworks similar to a given artwork using different methods.

```bash
# Precomputed (LLM-curated, recommended - includes explanations)
curl "https://museum-semantic-search.vercel.app/api/mcp/similar/met_436524?method=precomputed&limit=10"

# Embedding-based visual similarity (CLIP)
curl "https://museum-semantic-search.vercel.app/api/mcp/similar/met_436524?method=embedding&model=jina_clip&limit=10"

# Embedding-based conceptual similarity (text)
curl "https://museum-semantic-search.vercel.app/api/mcp/similar/met_436524?method=embedding&model=jina_text&limit=10"

# Metadata-based (same artist, period, culture, etc.)
curl "https://museum-semantic-search.vercel.app/api/mcp/similar/met_436524?method=metadata&limit=10"

# Combined (fuses metadata + text + image embeddings)
curl "https://museum-semantic-search.vercel.app/api/mcp/similar/met_436524?method=combined&limit=10"
```

**Query parameters:**
- `method`: "precomputed" (default) or "embedding"
- `model`: "jina_clip" (visual) or "jina_text" (conceptual) - only for embedding method
- `limit`: 1-50 (default 10)

**Response:**
```json
{
  "meta": {
    "source_artwork": {
      "id": "met_436524",
      "title": "...",
      "artist": "..."
    },
    "method": "precomputed",
    "model": null,
    "total": 10,
    "returned": 10,
    "processing_time_ms": 45
  },
  "results": [
    {
      "id": "met_437234",
      "score": 0.92,
      "title": "...",
      "artist": "...",
      "similarity_type": "compositional",
      "similarity_explanation": "Both feature a central figure with a dog..."
    }
  ]
}
```

### POST /image-search - Search by Image

Find visually similar artworks by uploading an image.

```bash
curl -X POST https://museum-semantic-search.vercel.app/api/mcp/image-search \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQ...",
    "limit": 10
  }'
```

**Request body:**
```json
{
  "image": "base64-encoded image (with or without data URL prefix)",
  "mimeType": "image/jpeg",
  "filters": { },
  "limit": 10,
  "detail": "standard"
}
```

**Response:** Same format as /search but includes `embedding_time_ms` in meta.

### GET /filters - Get Filter Options

Get available filter values for the collection. Supports search mode to find specific filter values.

```bash
# Get all top filter values
curl https://museum-semantic-search.vercel.app/api/mcp/filters

# Search for specific filter values (case-insensitive)
curl "https://museum-semantic-search.vercel.app/api/mcp/filters?search=japan"
curl "https://museum-semantic-search.vercel.app/api/mcp/filters?search=oil&field=mediums"
```

**Query parameters (for search mode):**
- `search`: Case-insensitive search string (e.g., "japan", "portrait", "oil")
- `field`: Limit to specific field: `departments`, `classifications`, `cultures`, `mediums`, `tags`, `countries`, `periods`
- `limit`: Max results per field (1-100, default 20)

**Response (default mode):**
```json
{
  "departments": [{ "value": "European Paintings", "count": 1500 }, ...],
  "classifications": [{ "value": "Paintings", "count": 2300 }, ...],
  "cultures": [{ "value": "French", "count": 450 }, ...],
  "mediums": [{ "value": "Oil on canvas", "count": 1800 }, ...],
  "tags": [{ "value": "Portraits", "count": 800 }, ...],
  "date_range": { "min": 1250, "max": 1950 },
  "schema": {
    "artistName": { "type": "string", "description": "...", "examples": [...] },
    "medium": { "type": "string", "description": "...", "examples": [...] },
    "yearStart": { "type": "number", "description": "...", "min": 1250, "max": 1950 },
    ...
  }
}
```

**Response (search mode):**
```json
{
  "search_query": "japan",
  "field_filter": "all",
  "results": {
    "cultures": [
      { "value": "Japan", "count": 45 },
      { "value": "probably Japan", "count": 12 }
    ]
  }
}
```

## Workflow

### Step 1: Discover the Collection
Call `GET /filters` first to see available departments, cultures, mediums, tags, and date ranges. Use search mode to find specific filter values.

### Step 2: Search
Use `POST /search` - hybrid mode (default) works well for most queries.

### Step 3: Get Details
Call `GET /artwork/{id}` on interesting results, or use `detail: "full"` in search to get complete details inline.

### Step 4: Explore
Use `GET /similar/{id}` to discover related works.

## Example Queries

| Query | Recommended Mode | Why |
|-------|------------------|-----|
| "person with a dog" | hybrid (default) | Works well for most queries |
| "woman looking in mirror" | semantic | Purely conceptual description |
| "stormy seascape" | hybrid | Mood-based but may match titles |
| "Madonna and child" | hybrid | Common in artwork titles |
| "Rembrandt self portrait" | hybrid | Artist name + description |
| "paintings from 1880s" | hybrid + filters | Use yearStart/yearEnd filters |

## Tips

- The collection is primarily European and American paintings from the Met Museum
- AI-generated descriptions enable finding artworks by what's depicted, not just metadata
- Use `source_url` to link users to the official Met Museum page
- Pagination: when `has_more` is true, increase `offset` to get more results
- For similar artworks: "precomputed" gives the best quality with explanations; "embedding" is faster
- No authentication required - the API is publicly accessible
