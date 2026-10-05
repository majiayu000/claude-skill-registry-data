---
name: exa
description: Search, extract content, and get AI-generated context using the Exa API. Use for web search, page content extraction, structured websets, and code-aware context retrieval.
---

Search and extract using the Exa AI API.

## Prerequisites

- `EXA_API_KEY` environment variable with a valid Exa API key

**Check before use:**

```bash
[ -z "$EXA_API_KEY" ] && echo "Error: EXA_API_KEY not set" || echo "OK: EXA_API_KEY is set"
```

**Note:** Never hardcode `EXA_API_KEY`. Always use the environment variable.

## Subcommands

| Command | Description |
| --- | --- |
| `exa search` | Neural search over the web |
| `exa contents` | Extract text, highlights, or summaries from URLs |
| `exa context` | Get AI-generated context for a query |
| `exa websets` | Manage Exa websets (create, get, list, items, delete, wait, cancel) |

## Output Modes

| Flag | Value | Output format | Use case |
| --- | --- | --- | --- |
| `--output` | `json` _(default)_ | JSON (pretty) | Programmatic use, saving to file |
| `--output` | `compact` | JSON (no whitespace) | Piping to `jaq` |
| `--output` | `text` | Human-readable formatted output | Quick review of results |

The `--output` flag accepts one of `json`, `compact`, or `text`.

## search

```bash
exa search [OPTIONS] QUERY
```

| Flag | API param | Description |
| --- | --- | --- |
| `--type` | `type` | `auto`, `fast`, `instant`, `deep-lite`, `deep`, `deep-reasoning` |
| `--num-results N` | `numResults` | Max results (default 10) |
| `--category` | `category` | Category filter (news, company, research paper, …) |
| `--include-domains DOMAIN` | `includeDomains` | Restrict to domain; repeatable |
| `--exclude-domains DOMAIN` | `excludeDomains` | Exclude domain; repeatable |
| `--start-published-date DATE` | `startPublishedDate` | YYYY-MM-DD or ISO 8601 |
| `--end-published-date DATE` | `endPublishedDate` | YYYY-MM-DD or ISO 8601 |
| `--moderation LEVEL` | `moderation` | Moderation level |
| `--highlights` | `contents.highlights` | Include key excerpts |
| `--summary` | `contents.summary` | Include LLM-generated summary |
| `--text` | `contents.text` | Include full page text |
| `--max-characters N` | `contents.text.maxCharacters` | Max characters per text result |
| `--max-age-hours H` | `contents.maxAgeHours` | Max age of cached content (0 = force livecrawl) |
| `--timeout SEC` | _(client)_ | Request timeout (default 60) |

**Important:** On `/search`, content params (`--highlights`, `--summary`, `--text`) are nested under `contents` in the API body. The CLI handles this automatically.

### Response (JSON)

```json
{
  "requestId": "...",
  "searchType": "auto",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "id": "https://example.com",
      "publishedDate": "2024-01-15T00:00:00.000Z",
      "text": "Full page content (if --text)...",
      "highlights": ["Key excerpt..."],
      "summary": "LLM-generated summary (if --summary)..."
    }
  ],
  "costDollars": { "total": 0.007 }
}
```

### Examples

```bash
# Basic search with highlights (recommended default)
exa search --highlights "recent breakthroughs in quantum computing"

# Domain-filtered news
exa search --highlights --category news \
  --include-domains reuters.com --include-domains bbc.com \
  --start-published-date 2025-01-01 \
  "AI regulation policy updates"

# Deep search with structured output via jaq
exa search --output=compact --type deep "compare latest frontier AI models" | jaq '.results[].title'

# Human-readable review
exa search --output=text --highlights --num-results 5 "python asyncio patterns"
```

## contents

```bash
exa contents [OPTIONS] URL [URL ...]
```

| Flag | API param | Description |
| --- | --- | --- |
| `--text` | `text` | Include full page text |
| `--highlights` | `highlights` | Include key excerpts |
| `--summary` | `summary` | Include LLM-generated summary |
| `--max-age-hours H` | `maxAgeHours` | Max age of cached content |
| `--livecrawl-timeout MS` | `livecrawlTimeout` | Livecrawl timeout in milliseconds |
| `--timeout SEC` | _(client)_ | Request timeout (default 60) |

**Important:** On `/contents`, content params (`--text`, `--highlights`, `--summary`) are **top-level** in the API body (NOT nested under `contents`). This differs from `/search`. The CLI handles this automatically.

### Examples

```bash
# Extract highlights from a URL
exa contents --highlights https://example.com/article

# Full text extraction
exa contents --text https://example.com/docs

# Multiple URLs at once
exa contents --highlights https://a.com https://b.com

# Compact JSON for piping
exa contents --output=compact --highlights https://example.com | jaq '.results[].highlights[]'
```

## context

```bash
exa context [OPTIONS] QUERY
```

| Flag | API param | Description |
| --- | --- | --- |
| `--tokens N` | `tokensNum` | Token budget: integer or `"dynamic"` (default: dynamic) |
| `--timeout SEC` | _(client)_ | Request timeout (default 60) |

### Examples

```bash
# Default (dynamic token budget)
exa context "react hooks useEffect cleanup"

# Fixed token budget
exa context --tokens 2000 "nix flake overlay pattern"

# Human-readable output
exa context --output=text "python dataclass vs pydantic model"
```

## websets

```bash
exa websets SUBCOMMAND [OPTIONS]
```

| Subcommand | Description                          |
| ---------- | ------------------------------------ |
| `create`   | Create a webset                      |
| `get`      | Get a webset by ID                   |
| `list`     | List all websets                     |
| `items`    | List items in a webset               |
| `delete`   | Delete a webset (requires `--force`) |
| `wait`     | Poll until webset status is `idle`   |
| `cancel`   | Cancel running webset operations     |

### create

```bash
exa websets create [PAYLOAD_JSON | --file FILE]
```

```bash
# Create from inline JSON
exa websets create '{"search":{"query":"AI companies in Europe","count":10}}'

# Create from file
exa websets create --file webset-config.json

# Create with enrichments
exa websets create '{
  "search": {"query": "AI startups Series A", "count": 20},
  "enrichments": [
    {"description": "CEO name", "format": "text"},
    {"description": "Funding amount", "format": "text"}
  ]
}'

# Create and wait until idle
exa websets create '...' && exa websets wait <ID>
```

### get

```bash
exa websets get [--expand items] ID
```

### list

```bash
exa websets list [--cursor CURSOR] [--limit N]
```

### items

```bash
exa websets items [--cursor CURSOR] [--limit N] WEBSET_ID
```

### delete

```bash
exa websets delete --force ID
```

### wait

```bash
exa websets wait [--timeout SEC] [--interval SEC] ID
```

Polls `GET /websets/{id}` until `status == "idle"`. Default: 300s timeout, 2s interval.

### cancel

```bash
exa websets cancel ID
```

## Error Handling

| HTTP Status | Meaning | Action |
| --- | --- | --- |
| `400` | Bad request — invalid parameters | Check flags and parameter types |
| `401` | Invalid or missing API key | Verify `EXA_API_KEY` is set and valid |
| `422` | Validation error | Check parameter types and constraints |
| `429` | Rate limit exceeded | Wait and retry with exponential backoff |
| `500` | Internal server error | Retry later |

Exit codes: `0` = success, `1` = error, `124` = timeout, `130` = interrupt.

## Best Practices

1. **Use `--highlights` over `--text` for agent workflows.** Highlights return 10x fewer tokens with the most relevant excerpts.

2. **`--type auto` is almost always the right search type.** Only use `fast`/`instant` when latency matters more than quality. Use `deep` variants for complex multi-step queries.

3. **`--max-age-hours 0` forces livecrawl.** This increases latency. Omit for the default (livecrawl only when no cache exists).

4. **Category filters disable some options.** `company` and `people` categories do not support `--exclude-domains` or date filters. Using them returns a 400 error.

5. **Websets are asynchronous.** Use `exa websets wait <ID>` after creating a webset to block until results are ready.

6. **Cache responses.** Search results for stable topics can be reused for the duration of a session.

7. **Pipe through `jaq` for custom filtering.** Use `--output=compact` for efficient JSON processing.

## Common Mistakes to Avoid

| Wrong | Correct |
| --- | --- |
| `useAutoprompt: true` | Remove it. Deprecated and does nothing. |
| `includeUrls` / `excludeUrls` | Use `--include-domains` / `--exclude-domains`. No URL-level filters exist. |
| `--text` nesting on `/contents` | The CLI handles nesting automatically. On `/search` content params nest under `contents`; on `/contents` they are top-level. |
| `--max-age-hours 0` always | Omit unless you specifically need fresh livecrawl results. |
