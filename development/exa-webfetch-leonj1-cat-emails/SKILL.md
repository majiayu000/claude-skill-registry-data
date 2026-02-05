---
name: exa-webfetch
description: Uses Exa API for intelligent web searches instead of default WebFetch. Provides up-to-date information with semantic search capabilities.
---

# Exa WebFetch Skill

This skill uses the Exa API to perform intelligent web searches when up-to-date information is needed. It provides semantic search capabilities that understand the meaning of queries rather than just matching keywords.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **Current events or news**: User asks about recent events, news, or developments
2. **Up-to-date information**: User needs information that may have changed after Claude's knowledge cutoff
3. **Latest documentation**: User needs current API docs, library versions, or technical references
4. **Research queries**: User asks for comprehensive research on a topic
5. **Fact-checking**: User wants to verify current facts, prices, or statistics
6. **Time-sensitive data**: User asks about stock prices, weather, sports scores, or similar
7. **Finding similar content**: User wants to find pages similar to a given URL

## Prerequisites

Ensure the `EXA_API_TOKEN` environment variable is set with a valid Exa API key.

```bash
# Verify the token is available
[ -n "$EXA_API_TOKEN" ] && echo "Exa API token is configured" || echo "ERROR: EXA_API_TOKEN not set"
```

## Exa API Endpoints

### 1. Search (`POST https://api.exa.ai/search`)

The primary endpoint for web searches. Use this for most queries.

**Example:**
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "YOUR_SEARCH_QUERY",
    "type": "auto",
    "numResults": 10,
    "contents": {
      "text": true,
      "highlights": {
        "numSentences": 3
      }
    }
  }'
```

**Key Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | required | The search query |
| type | enum | "auto" | Search type: "neural", "fast", "auto", "deep" |
| numResults | integer | 10 | Number of results (max 100) |
| category | enum | - | Filter: "company", "research paper", "news", "pdf", "github" |
| includeDomains | array | - | Limit to specific domains |
| excludeDomains | array | - | Exclude specific domains |
| startPublishedDate | string | - | Filter by publish date (ISO 8601) |
| endPublishedDate | string | - | Filter by publish date (ISO 8601) |
| contents.text | boolean | false | Return full page text |
| contents.highlights | object | - | Extract relevant snippets |
| contents.summary | object | - | Generate summaries |

### 2. Get Contents (`POST https://api.exa.ai/contents`)

Retrieve full content from specific URLs.

**Example:**
```bash
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "ids": ["url1", "url2"],
    "text": true
  }'
```

### 3. Find Similar (`POST https://api.exa.ai/findSimilar`)

Find pages similar to a given URL.

**Example:**
```bash
curl -X POST 'https://api.exa.ai/findSimilar' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://example.com/article",
    "numResults": 10
  }'
```

### 4. Answer (`POST https://api.exa.ai/answer`)

Get direct answers to questions with citations.

**Example:**
```bash
curl -X POST 'https://api.exa.ai/answer' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "What is the latest version of Python?",
    "text": true
  }'
```

## Usage Patterns

### For News/Current Events
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "YOUR_NEWS_QUERY",
    "type": "auto",
    "category": "news",
    "numResults": 10,
    "startPublishedDate": "2025-01-01T00:00:00Z",
    "contents": {
      "text": true,
      "highlights": {"numSentences": 3}
    }
  }'
```

### For Technical Documentation
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "YOUR_TECH_QUERY documentation",
    "type": "auto",
    "numResults": 5,
    "includeDomains": ["docs.example.com", "github.com"],
    "contents": {
      "text": true
    }
  }'
```

### For Research Papers
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "YOUR_RESEARCH_QUERY",
    "type": "neural",
    "category": "research paper",
    "numResults": 10,
    "contents": {
      "text": true,
      "summary": {"query": "Summarize the key findings"}
    }
  }'
```

### For GitHub Repositories
```bash
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "YOUR_REPO_QUERY",
    "type": "auto",
    "category": "github",
    "numResults": 10,
    "contents": {
      "text": true
    }
  }'
```

## Response Format

The API returns JSON with this structure:

```json
{
  "requestId": "unique-id",
  "resolvedSearchType": "neural",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "publishedDate": "2025-01-15",
      "author": "Author Name",
      "text": "Full page content...",
      "highlights": ["Relevant snippet 1", "Relevant snippet 2"],
      "summary": "AI-generated summary..."
    }
  ],
  "costDollars": {
    "total": 0.001
  }
}
```

## Best Practices

1. **Use appropriate search type:**
   - `auto` - Let Exa decide (recommended for most cases)
   - `neural` - Semantic search for conceptual queries
   - `fast` - Keyword-based for specific terms
   - `deep` - Comprehensive search for complex queries

2. **Filter by category** when searching for specific content types (news, papers, github)

3. **Use date filters** for time-sensitive queries to get recent results

4. **Request highlights** for quick scanning without full text

5. **Use domain filters** when you know authoritative sources

## Error Handling

Check for these common issues:

- **401 Unauthorized**: Invalid or missing `EXA_API_TOKEN`
- **429 Rate Limited**: Too many requests, implement backoff
- **400 Bad Request**: Invalid query parameters

## Do NOT Invoke When

- User is asking about Claude's capabilities or identity
- User is asking about static code in the current project
- The information is already in the conversation context
- User explicitly requests using the default WebFetch tool
- The query is about private/internal systems not on the web
