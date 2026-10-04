---
name: unique-cli-web-search
description: >-
  Search the public web and crawl URLs via the Unique AI Platform's
  `unique-cli web-search` command, with automatic per-turn citation
  tracking so cited web facts render as clickable external reference
  chips and `<sup>N</sup>` footnotes on the Unique platform. ALWAYS use
  this skill when the user asks to search the public web, research a
  topic online, look up news/articles/regulations, fetch the contents
  of one or more URLs, or perform any "two-phase" web research (search
  → review snippets → crawl selected URLs for full content). Routes
  through the Unique AI Platform's `/web-search-api` endpoints, so the
  engine (Google, Brave, Tavily, Jina, Firecrawl, …) and crawler are
  resolved server-side from the current environment — you never need
  to manage engine API keys yourself. Use this instead of fabricating
  answers from training data whenever fresh / source-cited information
  is needed. Do NOT use this skill for the internal knowledge base
  (`unique-cli search`) or for arbitrary tool execution (`unique-cli
  mcp`).
---

# Unique CLI -- Web Search & Crawl

Two-phase web research from the terminal, backed by the Unique AI Platform's public `/web-search-api`. Phase 1 (`search`) queries a search engine and returns URLs + snippets. Phase 2 (`crawl`) fetches the full page content for the URLs you actually want to read. The two-phase split lets you (or an LLM) review titles and snippets cheaply before paying the latency cost of full-page crawling. Every invocation annotates each result with a `sourceNumber` / `citation: "websourceN"` and records a per-turn citation manifest at `.unique/web-refs.jsonl`, so any fact you cite as `[websourceN]` is rendered with a footnote and a clickable external reference chip in the chat UI.

> **Server-side engine/crawler.** Unlike `unique-websearch`, this CLI does not instantiate engines locally — it just posts to the Unique platform, which resolves the engine and crawler from `ACTIVE_SEARCH_ENGINES` / `ACTIVE_INHOUSE_CRAWLERS` server-side. **You do not need any engine API keys** (Google, Brave, Tavily, etc.) on the client.

## Two-Phase Workflow (preferred for AI agents)

1. `unique-cli web-search search "<query>" --json` → candidate URLs with snippets and citation keys.
2. Review titles + snippets, pick the URLs that look relevant.
3. `unique-cli web-search crawl <selected-urls> --json` → full page content for those URLs, reusing citation keys for URLs returned by search.
4. Reason over the crawled content and cite web facts with `[websourceN]`.

This sequencing is much cheaper than crawling everything up-front and is the recommended pattern when an LLM is the consumer. In Swappable Intelligence, the CLI also writes `.unique/web-refs.jsonl`; the platform converts cited `[websourceN]` markers into external reference chips in the final answer.

```bash
unique-cli web-search search "EU AI Act enforcement timeline" --json \
  | jq -r '.results[].url' \
  | unique-cli web-search crawl --stdin
```

For convenience, search can also crawl in one shot via `--include-content` when the engine requires scraping (see below).

## Phase 1 — Search

```bash
# Basic search (uses server-side engine + default fetchSize)
unique-cli web-search search "quarterly earnings 2026"

# Limit the number of hits
unique-cli web-search search "AI regulation" -n 10

# JSON output (for piping or programmatic use)
unique-cli web-search search "python tutorial" --json

# Search AND populate result.content in one call (engine + crawler)
unique-cli web-search search "sustainability reports" --include-content --json
```

### Per-call engine override

Force a specific engine (or any engine-specific knob) without changing server config:

```bash
unique-cli web-search search "tax reform" \
  --engine-config '{"searchEngineName":"Google","fetchSize":3}'
```

The `--engine-config` value is a JSON object matching the server's
`searchEngineConfig` discriminated union (same shape `assistants-core`
expects). The discriminator key is `searchEngineName`.

## Phase 2 — Crawl

```bash
# Crawl one or more URLs explicitly
unique-cli web-search crawl https://example.com https://other.com

# Tune server-side concurrency
unique-cli web-search crawl --parallel 5 https://a.com https://b.com

# Read URLs from stdin (one per line) — composes nicely with `search --json`
echo "https://example.com" | unique-cli web-search crawl --stdin

# JSON output (preserves per-URL error info)
unique-cli web-search crawl https://example.com --json
```

### Per-call crawler override

```bash
unique-cli web-search crawl https://example.com \
  --crawler-config '{"crawlerType":"BasicCrawler"}'
```

The `--crawler-config` value is a JSON object matching the server's
`crawlerConfig` discriminated union (discriminator key: `crawlerType`).

## Config files (`~/.unique-websearch.json`)

For non-interactive workflows you can persist overrides in a JSON file
shape-compatible with the reference `unique-websearch` CLI. Resolution
order:

1. `--config / -c PATH` (subcommand value beats group value)
2. `$UNIQUE_WEBSEARCH_CONFIG`
3. `~/.unique-websearch.json` (used only if it exists)

Two file shapes are supported:

### A. Full platform config (camelCase or snake_case)

Includes a discriminator (`searchEngineName` / `crawlerType`) or the
top-level `webSearchActiveMode` key. The nested `searchEngineConfig` /
`crawlerConfig` blocks are forwarded verbatim to the API:

```json
{
  "searchEngineConfig": { "searchEngineName": "Google", "fetchSize": 5 },
  "crawlerConfig":      { "crawlerType": "BasicCrawler" }
}
```

### B. Simple overrides

No discriminator — the file just tunes well-known scalars. Only
`fetch_size` / `fetchSize` is currently honoured client-side; the rest
is ignored because the server can't apply scalar tweaks without a
discriminator:

```json
{ "search_engine_config": { "fetch_size": 50 } }
```

### Override precedence (highest first)

1. Inline `--fetch-size` / `--engine-config` / `--crawler-config` flags
2. Config file (`--config` / `$UNIQUE_WEBSEARCH_CONFIG` / `~/.unique-websearch.json`)
3. Server-side defaults (`ACTIVE_SEARCH_ENGINES`, etc.)

## Command Reference

### `unique-cli web-search search <query>`

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--fetch-size` | `-n` | server default | Override the engine's `fetchSize` |
| `--include-content` | `-i` | off | Populate `result.content` via the configured crawler |
| `--engine-config` | | none | Override `searchEngineConfig` (JSON object, must include `searchEngineName`) |
| `--crawler-config` | | none | Override `crawlerConfig` (JSON object) — only used with `--include-content` |
| `--config` | `-c` | none | Per-call override of the group's `--config` path |
| `--json` | | off | Emit `{engine, query, results: [...]}` JSON envelope |

### `unique-cli web-search crawl <url>...`

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--parallel` | `-p` | 10 | URLs the server crawls concurrently per batch (≥ 1) |
| `--stdin` | | off | Read URLs from stdin (one per line) — combines with positional URLs |
| `--crawler-config` | | none | Override `crawlerConfig` (JSON object, must include `crawlerType`) |
| `--config` | `-c` | none | Per-call override of the group's `--config` path |
| `--json` | | off | Emit `{crawler, results: [...]}` JSON envelope |

### Group options

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | `-c` | Config file path; falls back to `$UNIQUE_WEBSEARCH_CONFIG` and `~/.unique-websearch.json` |
| `--version` | | Show the CLI version |
| `--help` | | Show help |

## Output Format

### `search` (text)

```
engine: Google    query: 'quarterly earnings 2026'
Found 3 result(s):

  1. Example Page Title [websource1]
     https://example.com/article
     A short snippet describing the page content...

  2. Another Relevant Result [websource2]
     https://another.com/page
     [4523 chars of content]    # only when --include-content
```

### `search --json`

```json
{
  "engine": "Google",
  "query": "quarterly earnings 2026",
  "results": [
    {
      "url": "https://example.com/article",
      "title": "Example Page Title",
      "snippet": "A short snippet describing the page content...",
      "content": "",
      "sourceNumber": 1,
      "citation": "websource1"
    }
  ]
}
```

> The `--json` envelope (`engine`, `query`, `results`, plus per-result
> `content`) is richer than the reference `unique-websearch` CLI's flat
> array. To pipe URLs into `crawl`, address `.results[].url` (not
> `.[].url`):
>
> ```bash
> unique-cli web-search search "q" --json \
>   | jq -r '.results[].url' \
>   | unique-cli web-search crawl --stdin
> ```

### `crawl` (text)

```
crawler: BasicCrawler
Crawled 2 URL(s):

  1. https://example.com/article [websource1]
     [4523 chars]
     Full page content preview, truncated to ~500 characters...

  2. https://other.com/page [websource2]
     ERROR: HTTP 503 from upstream
```

### `crawl --json`

```json
{
  "crawler": "BasicCrawler",
  "results": [
    {
      "url": "https://example.com/article",
      "content": "Full page content as markdown...",
      "error": null,
      "sourceNumber": 1,
      "citation": "websource1"
    },
    {
      "url": "https://other.com/page",
      "content": "",
      "error": "HTTP 503 from upstream",
      "sourceNumber": 2,
      "citation": "websource2"
    }
  ]
}
```

## Exit Codes

In one-shot mode, the CLI exits **`0`** on success and **`1`** on
failures (config-file errors, invalid JSON overrides, API errors,
missing URLs for `crawl`, and citation-manifest I/O failures — e.g.
when `.unique/web-refs.jsonl` cannot be written or its parent
directory is unsafe). Error messages are prefixed with
`web-search:` or `web-crawl:` so they're easy to grep.

```bash
unique-cli web-search crawl  # no URLs → exits 1
# web-crawl: no URLs provided. Pass URLs as arguments or use --stdin.
```

## Workflow Examples

### Research a fast-moving topic and cite sources

User: "What did the EU just decide about general-purpose AI models?"

```bash
# 1. Find candidate sources
unique-cli web-search search "EU general-purpose AI model rules 2026" -n 10 --json \
  > /tmp/hits.json

# 2. Inspect the snippets, pick 3 promising URLs from /tmp/hits.json,
#    then crawl them for full content
jq -r '.results[0:3][].url' /tmp/hits.json \
  | unique-cli web-search crawl --stdin --json \
  > /tmp/pages.json

# 3. Reason over /tmp/pages.json and cite supported web facts as [websourceN].
```

### One-shot search-with-content (no manual selection)

When you trust the engine and just want full content for the top hits:

```bash
unique-cli web-search search "Swiss FINMA AI guidance" \
  --include-content --json -n 5
```

This populates `results[].content` server-side via the configured
crawler; no separate `crawl` call is needed.

### Force a specific engine for one call

```bash
unique-cli web-search search "OECD principles on AI" \
  --engine-config '{"searchEngineName":"Brave","fetchSize":5}'
```

### Persist defaults per environment

```bash
# Set once for the shell session
export UNIQUE_WEBSEARCH_CONFIG=~/configs/ws-google-fast.json

# Or pin per-invocation (sub-command --config wins over the group's)
unique-cli web-search --config ~/configs/ws-default.json \
  search --config ~/configs/ws-low-fetch.json "macro outlook 2026"
```

## SDK Usage (Python)

The CLI is a thin wrapper around `unique_sdk.WebSearch` and
`unique_sdk.WebCrawl`. Use these directly when scripting:

```python
import unique_sdk

unique_sdk.api_key = "ukey_..."
unique_sdk.app_id = "app_..."

# Phase 1 — search
hits = unique_sdk.WebSearch.search(
    user_id="user_123",
    company_id="company_456",
    query="EU AI Act enforcement",
    fetchSize=10,
    # Optional per-call overrides forwarded to the server's
    # WebSearchConfig.searchEngineConfig discriminated union:
    searchEngineConfig={"searchEngineName": "Google"},
)
urls = [r["url"] for r in hits.results]

# Phase 2 — crawl the URLs we want to read
pages = unique_sdk.WebCrawl.crawl(
    user_id="user_123",
    company_id="company_456",
    urls=urls[:5],
    parallel=5,
    crawlerConfig={"crawlerType": "BasicCrawler"},
)
for entry in pages.results:
    if entry["error"]:
        continue
    process(entry["url"], entry["content"])
```

Both classes have `*_async` variants (`WebSearch.search_async`,
`WebCrawl.crawl_async`) for async contexts.

## Citation Rules

Cite a fact from `unique-cli web-search` results with `[websourceN]`, where `N` matches the `sourceNumber` (also surfaced as the `citation: "websourceN"` field) the command emitted alongside the result. The Unique platform's Swappable Intelligence runner converts each `[websourceN]` marker in your final answer into a `<sup>N</sup>` footnote and a clickable external reference chip; without `unique-cli web-search`, web facts in your answer appear as plain text only, with no footnote and no chip — so this is the only way to make web citations render correctly on the platform.

```
The regulation enters into force in August 2026 [websource1],
with phased obligations through 2028 [websource2].
```

**Rules** (enforced by the platform's reference post-processor, which reads `.unique/web-refs.jsonl` rather than your prose):

1. **`[websourceN]` is for public web citations only.** Knowledge-base results from `unique-cli search` use `[sourceN]` instead — never mix the two namespaces, and never use `[sourceN]` for web results.
2. Only cite numbers you saw in the **current** turn's `unique-cli web-search` output. Numbers from previous turns are stale and will be silently dropped.
3. Write `websource` in singular form with the number in digits: `[websource1]`, `[websource2]` — not `[Websource 1]` or `[websource one]`.
4. The same URL keeps the same `[websourceN]` across `search` and `crawl` calls in a turn, so cite a fact from the crawled page with the marker the search snippet already advertised.
5. Do not invent source numbers for remembered or inferred facts.

## Prerequisites

```bash
UNIQUE_USER_ID    # User ID (required)
UNIQUE_COMPANY_ID # Company ID (required)
UNIQUE_API_KEY    # API key — optional on localhost / secured cluster
UNIQUE_APP_ID     # App ID — optional on localhost / secured cluster

# Optional — config file location
UNIQUE_WEBSEARCH_CONFIG   # Path to a JSON config (overrides default ~/.unique-websearch.json)
```

You **do not** need any engine-specific API keys (`GOOGLE_SEARCH_API_KEY`,
`BRAVE_SEARCH_API_KEY`, `TAVILY_API_KEY`, etc.) on the client — they live
on the server.

Install: `pip install unique-sdk`
