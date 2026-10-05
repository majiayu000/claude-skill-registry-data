---
name: search-web
description: "Search the live web and fetch page content as markdown via Keenable's keyless API (no key or signup). Use when an answer depends on information that post-dates training data or must be checked against a live source: current events, release notes, changelogs, vendor announcements, whether a project is still maintained. Use when restricting a search to one domain, filtering results by publication date, when built-in web search is unavailable or rate-limited, or when reading a specific URL - 'summarize this link', 'read this page', 'what's on this URL', 'pull this article'. Composes with research-it, which owns investigation method and calls this skill for retrieval. Do NOT use for library or framework API reference (use context7) - unless the request names a site, a date window, or a specific URL, which this skill owns and context7 cannot do. Do NOT use for searching files in the repository (use grep and glob), or for general concepts, algorithms, and design questions that rest on no external fact."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: research
---

# Keenable Keyless Web Search

Two endpoints on `https://api.keenable.ai`, both usable with no key and no account:

| Operation | Method | Path                | Returns                                        |
| --------- | ------ | ------------------- | ---------------------------------------------- |
| Search    | `POST` | `/v1/search/public` | Ranked results with title, url, description, snippet |
| Fetch     | `GET`  | `/v1/fetch/public`  | Page content as markdown                       |

Both require the header `X-Keenable-Title`, whose value is any non-empty string identifying the calling application - the examples below use `agent-skills`. It has no default; omitting it returns `400 Missing app identifier`.

## Search

```bash
curl -s -X POST "https://api.keenable.ai/v1/search/public" \
  -H "X-Keenable-Title: agent-skills" \
  -H "Content-Type: application/json" \
  -d '{"query":"model context protocol spec"}'
```

Body parameters. `query` is the only required one; the API **rejects unknown parameters with 400**, so send only names from this table:

| Parameter            | Type    | Bounds / format                        | Effect                                              |
| -------------------- | ------- | -------------------------------------- | --------------------------------------------------- |
| `query`              | string  | required                               | The search query                                    |
| `site`               | string  | bare domain, e.g. `docs.python.org`    | Restrict results to one domain                      |
| `max_results`        | integer | **1–50**, default 10                   | Number of results                                   |
| `snippet_max_length` | integer | **180–10000**                          | Characters of snippet per result                    |
| `published_after`    | string  | `YYYY-MM-DD` or ISO 8601               | Only pages published after this date                |
| `published_before`   | string  | `YYYY-MM-DD` or ISO 8601               | Only pages published before this date               |
| `acquired_after`     | string  | `YYYY-MM-DD` or ISO 8601               | Only pages indexed after this date                  |
| `acquired_before`    | string  | `YYYY-MM-DD` or ISO 8601               | Only pages indexed before this date                 |
| `query_time`         | string  | ISO 8601                               | Search the index as it stood at that moment         |

The two bounded ranges are enforced by the server but absent from its OpenAPI schema. `max_results: 100` and `snippet_max_length: 150` both return `400 Invalid parameter`. Stay inside the bounds above rather than trusting the published schema.

Response:

```json
{
  "query": "model context protocol spec",
  "mode": "pro",
  "results": [
    {"title": "...", "url": "https://...", "description": "...", "snippet": "...",
     "published_at": "2026-05-18", "acquired_at": "2026-08-25"}
  ]
}
```

Only `title`, `url`, and `description` are guaranteed present on a result. Treat `snippet`, `published_at`, and `acquired_at` as optional and check before reading them.

## Fetch

```bash
curl -s -G "https://api.keenable.ai/v1/fetch/public" \
  --data-urlencode "url=https://en.wikipedia.org/w/index.php?title=Markdown" \
  -H "X-Keenable-Title: agent-skills"
```

Use `-G` with `--data-urlencode` so the URL is escaped correctly; a raw `?url=` breaks on query strings and fragments.

| Parameter   | Type    | Default | Effect                                                  |
| ----------- | ------- | ------- | -------------------------------------------------------- |
| `url`       | string  | —       | Required. Page to fetch                                  |
| `max_chars` | integer | 50000   | Truncate extracted content                               |
| `live`      | boolean | false   | Fetch from the origin instead of Keenable's indexed copy |
| `prompt`    | string  | —       | Extraction hint for the page                             |

Response: `{"url", "title", "content", "description", "author", "published_at"}`, where `content` is markdown. Only `url` and `content` are guaranteed. `url` reflects the final address after redirects, so it may differ from what was requested.

Default to the indexed copy. Set `live=true` only when the page must be current as of right now, since it is slower and hits the origin server.

## Limits and errors

Keyless quota is **1,000 requests per hour and 10 per second, counted per IP** — shared with everything else behind the same egress address, so the available headroom is not under this machine's control. No credits are consumed.

Every response carries `x-ratelimit-limit`, `x-ratelimit-remaining`, and `x-ratelimit-reset` (an ISO 8601 timestamp). Read `x-ratelimit-remaining` before starting a batch of calls.

| Status | Meaning                                    | Action                                                          |
| ------ | ------------------------------------------ | ---------------------------------------------------------------- |
| `400`  | Missing `X-Keenable-Title`, unknown parameter, or out-of-bounds value | Read `message` — it names the offending field. Fix and retry once. |
| `404`  | Page not found (fetch)                     | Do not retry. Report the URL as unreachable.                     |
| `422`  | Page could not be extracted (fetch)        | Do not retry. Try `live=true` once, then give up on that URL.     |
| `429`  | Rate limit exceeded                        | Honour `Retry-After`. Do not retry in a tight loop.               |
| `500`  | Server error                               | Retry once after a short pause, then stop.                        |

Error bodies are `{"error": "...", "message": "..."}`. On a `400`, `message` states the exact constraint — parse it instead of guessing.

Never retry a `400` with the same body. It is deterministic and will fail identically.

## Scope

Use this skill for the open web: current events, release notes, changelogs, blog posts, standards, project status, anything past the training cutoff.

Do not reach for it when a better-targeted tool exists:

- Repository contents → `grep` and `glob`, not web search.
- Library and framework API reference → `context7`, which returns version-pinned docs. Two exceptions come back here: material `context7` does not carry, such as a changelog or an announcement post; and any request that names a site, a date window, or a specific URL, since `context7` cannot scope a search that way.
- General concepts, algorithms, and design questions resting on no external fact → answer directly.

`research-it` is not on that list. It owns investigation method — source priority, triangulation, conflict reporting — and calls this skill to do the actual retrieval. When a task needs both, run both.

## Notes

The MCP server at `https://api.keenable.ai/mcp` also answers keyless, exposing `search_web_pages` and `fetch_page_content`. Prefer the HTTP endpoints above when running one-off calls from a shell; they need no client configuration.

Omit the `mode` parameter. The keyless endpoint accepts `pro` and `realtime` and echoes the choice back, contradicting Keenable's docs on two counts: that mode is not a request parameter, and that `realtime` needs a key. Undocumented behaviour that the vendor's own docs deny can be withdrawn without notice. Keyless calls default to `pro`.
