---
name: sap-tutorials-content
description: Read SAP developer tutorial content from the public developers.sap.com API — catalog, navigation, tutorial HTML/JSON, and full-text search. Use when an agent needs to discover, fetch, or search official SAP tutorials, missions, groups, or concepts without authentication.
---

# SAP tutorials — read-only content access

Fetch official SAP developer tutorial content directly from the public
production API. Everything here is **anonymous and read-only** — no login, no
token, no API key. It is the same content served at
[developers.sap.com](https://developers.sap.com).

Use this when you need to:
- discover what tutorials/missions/groups exist,
- pull the rendered HTML or structured JSON of a specific tutorial,
- search the catalog by keyword, tag, or facet,
- or wire the content into an agent via the ready-made public MCP endpoint.

## Base URL

```
https://developers.sap.com
```

All paths below are relative to that host. Responses set `ETag` /
`Cache-Control`; honor them and avoid hammering — this is a shared public
service. Endpoints verified reachable and anonymous as of 2026-08-18.

## Fastest starting points

- **`GET /llms.txt`** — a compact, LLM-oriented site map (plain text, ~4 KB).
  Read this first to orient. `GET /llms-full.txt` is the expanded version.
- **`GET /build/catalog`** — the full catalog as JSON: missions, groups, and
  tutorials with slugs, titles, and relationships. (~700 KB.)

## Discover: catalog, navigation, mappings (JSON)

| Endpoint | Returns |
|---|---|
| `GET /build/catalog` | Full missions/groups/tutorials catalog |
| `GET /build/navigator` | Missions, groups, tutorial→mission/group mappings, checkpoints |
| `GET /build/slug-mapping` | slug → internal ID map |
| `GET /build/mission/{slug}` | One mission's structure |
| `GET /build/topics-gallery` | Topic gallery grouping |
| `GET /build/concepts` | Published knowledge-graph concepts |
| `GET /tutorials/_nav.json` | Navigation metadata for all published tutorials |

## Read a specific tutorial

Tutorial slugs are **lowercase canonical** (mixed-case requests 301-redirect).

| Endpoint | Returns |
|---|---|
| `GET /tutorials/{slug}` | Rendered tutorial **HTML** |
| `GET /tutorials/{slug}.model.json` | Structured **JSON** (legacy AEM `model.json` shape) |
| `GET /content/tutorials/{slug}` | Same HTML as `/tutorials/{slug}` (direct content prefix) |

Prefer `.model.json` when you want to parse steps/structure; prefer the HTML
route when you want the page as a human sees it. If you don't know a slug, get
it from `/build/catalog` or via search below.

## Concepts & content pages (HTML)

| Endpoint | Returns |
|---|---|
| `GET /concepts/` | Knowledge-graph concepts index |
| `GET /concepts/{slug}` | A single concept landing page (404 if not published) |
| `GET /content/pages/{name}` | Content pages (e.g. browse/topics/verb landing pages) |
| `GET /sitemap.xml` | Sitemap |

## Search (OData v4, anonymous)

The search service is anonymous and rate-limited by IP. OData base: `/search`.

| Endpoint | Returns |
|---|---|
| `GET /search/SearchableItems?$search=<q>&$top=20` | Ranked items (slug, title, description, tags, searchScore) |
| `GET /search/SearchableItems?$filter=<expr>` | Filtered items |
| `GET /search/Tags` | Available tags |
| `GET /search/$metadata` | **EDMX** service metadata (the schema for everything above) |

Typed OData **functions** (return structured shapes):

- `GET /search/search_tutorials(query='cap',top=10)`
- `GET /search/list_missions(top=20)`
- `GET /search/get_mission(slug='...')`
- `GET /search/get_tutorial(slug='...')`
- `GET /search/getFacets(...)`

There is also a public GraphQL surface at `POST /graphql/public`.

Read `/search/$metadata` to confirm exact function parameter names and entity
shapes before constructing queries — do not guess field names.

## MCP endpoint (ready-made, anonymous)

The platform exposes a **public MCP server** over Streamable HTTP — no auth. This
is the easiest way to give any MCP-capable agent live tutorial search:

```
https://developers.sap.com/mcp/search    # search tools: search_tutorials, list_missions, get_mission, get_tutorial
https://developers.sap.com/mcp/graph      # knowledge-graph tools
```

Add to **Claude Code**:

```bash
claude mcp add --transport http sap-tutorials https://developers.sap.com/mcp/search
```

Or in **Claude Desktop** / any MCP client config:

```json
{
  "mcpServers": {
    "sap-tutorials": {
      "type": "http",
      "url": "https://developers.sap.com/mcp/search"
    }
  }
}
```

Quick reachability check (expect an SSE `text/event-stream` response):

```bash
curl -sS -X POST https://developers.sap.com/mcp/search \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Conventions & etiquette

- **Read-only.** Nothing here mutates state. Do not attempt `POST`/`PUT` against
  content routes — the write/ops endpoints (`/content/publish`, `/content/rollback`,
  image ingest, admin/QA surfaces) require credentials and are not part of this
  public read surface.
- **Cache-friendly.** Respect `ETag`/`Cache-Control`; send `If-None-Match` on
  repeat fetches. Batch discovery via `/build/catalog` once rather than crawling
  every tutorial.
- **Lowercase slugs.** Always lowercase a slug before requesting it.
- **Degrade gracefully.** A 404 means "not published"; a 429 means you're being
  rate-limited — back off. Don't retry aggressively.
- **Machine discovery.** ORD documents are published under `/ord/*` and an agent
  card at `/.well-known/agent-card.json` for automated capability discovery.
