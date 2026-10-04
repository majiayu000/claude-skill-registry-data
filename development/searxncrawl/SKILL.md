---
name: searxncrawl
description: "Web crawling and SearXNG search via CLI, MCP server, and Python API. Use when user mentions `crawl`, `search`, `SearXNG`, `MCP server`, `site crawl`, or `crawl-capture`."
---

# searxNcrawl

MCP server and CLI toolkit for web search and crawling, built on Crawl4AI + SearXNG. Returns model-friendly Markdown or JSON.

## Quick start

```bash
# Docker (everything included — SearXNG + Playwright + MCP server)
cp .env.example .env && docker compose up --build
# MCP endpoint: http://localhost:9555/mcp

# pip (standalone)
python -m venv .venv && source .venv/bin/activate
pip install -e . && playwright install chromium

# uv (standalone)
uv sync && uv run playwright install chromium
```

## Workflows

### Crawl a page

```bash
crawl https://docs.example.com                    # markdown to stdout
crawl https://docs.example.com --json              # JSON with metadata + dedup stats
crawl https://example.com --remove-links           # strip URLs from output
crawl https://example.com -o output.md             # save to file
crawl https://a.com https://b.com --concurrency 5  # batch crawl
```

### Crawl an entire site

```bash
crawl https://docs.example.com --site --max-depth 2 --max-pages 10 -o docs/
crawl https://docs.example.com --site --include-subdomains --json
```

Site crawl uses BFS strategy. One URL only (no batch). Output aggregates all pages.

### Search via SearXNG

```bash
search "python tutorials"
search "Rezepte" --language de --max-results 5
search "AI news" --time-range week --categories news
search "rust async" --engines google,duckduckgo --safesearch 2
```

Requires a running SearXNG instance with JSON output enabled. Docker Compose includes one automatically.

### Authenticated crawling (crawl-capture)

```bash
# Method A: Playwright login flow
crawl-capture --start-url https://example.com/login \
    --completion-url 'https://example.com/dashboard.*' \
    --output ./state.json

# Method B: Export from running Chrome via CDP
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-cdp"
# Log in manually, then:
crawl-capture --cdp-url http://127.0.0.1:9222 --list-sessions
crawl-capture --cdp-url http://127.0.0.1:9222 --cdp-session 2 --output ./state.json

# Use captured state
crawl https://example.com/private --storage-state ./state.json
```

Exit codes: `0` success, `2` timeout, `130` browser closed before completion.

## Examples

### Research a topic — search then crawl top results

```bash
search "FastAPI websockets" --max-results 5
# Pick the most relevant URLs from results, then:
crawl https://fastapi.tiangolo.com/advanced/websockets/ \
      https://websockets.readthedocs.io/en/stable/ \
      --remove-links -o research.md
```

### Mirror a docs site for offline context

```bash
crawl https://docs.pydantic.dev/latest/ --site \
      --max-depth 3 --max-pages 50 -o pydantic-docs/
# Each page saved as a separate file in pydantic-docs/
```

### Give Claude Code web search + crawl

Start the Docker stack, then add to your MCP config:

```json
{
  "mcpServers": {
    "crawler": { "url": "http://localhost:9555/mcp" }
  }
}
```

Claude Code now has `crawl`, `crawl_site`, and `search` tools — no API keys needed.

### Crawl a JS-heavy SPA

```bash
# Crawl4AI uses Playwright/Chromium — JS renders automatically
crawl https://app.example.com/dashboard --json --timeout 60
```

### Search in a specific language

```bash
search "Maschinelles Lernen Einführung" --language de --max-results 10
search "料理 レシピ 簡単" --language ja --categories general
```

### Extract structured data from a page

```bash
crawl https://example.com/pricing --json
# Returns: markdown content + extracted links as references[] + dedup metadata
```

### MCP server setup

```bash
# STDIO transport (for Claude Code, Zed, VS Code, etc.)
python -m crawler.mcp_server

# HTTP transport
python -m crawler.mcp_server --transport http --port 8000

# HTTP with CORS
python -m crawler.mcp_server --transport http --cors-origins "http://localhost:3000"

# Docker
docker compose up --build   # HTTP at http://localhost:9555/mcp
```

**Client config (STDIO):**
```json
{
  "mcpServers": {
    "crawler": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/searxNcrawl", "python", "-m", "crawler.mcp_server"],
      "env": { "SEARXNG_URL": "http://your-searxng:8888" }
    }
  }
}
```

**Client config (HTTP/Docker):**
```json
{
  "mcpServers": {
    "crawler": { "url": "http://localhost:9555/mcp" }
  }
}
```

## Reference

### MCP tools

| Tool | Key params | Notes |
|------|-----------|-------|
| `crawl` | `urls[]`, `output_format`, `concurrency`, `timeout`, `remove_links`, `dedup_mode`, `storage_state` | Batch crawl; returns markdown or JSON |
| `crawl_site` | `url`, `max_depth` (2), `max_pages` (25), `include_subdomains`, `timeout` (120) | BFS site crawl from seed URL |
| `search` | `query`, `language` (en), `time_range`, `categories`, `engines`, `safesearch` (1), `max_results` (10) | SearXNG metasearch; results capped at 50 |

### Python API

```python
from crawler import crawl_page_async, crawl_pages_async, crawl_site_async

doc = await crawl_page_async("https://docs.example.com", dedup_mode="exact")
docs = await crawl_pages_async(["https://a.com", "https://b.com"], concurrency=3)
result = await crawl_site_async("https://docs.example.com", max_depth=2, max_pages=10)
# result.documents, result.stats
```

Sync wrappers: `crawl_page()`, `crawl_pages()`, `crawl_site()`.

### CrawledDocument fields

`request_url`, `final_url`, `status` ("success"/"failed"/"redirected"), `markdown`, `html`, `headers`, `references` (extracted links), `metadata` (title, status_code, dedup metrics, guardrail signals), `error_message`.

### Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `SEARXNG_URL` | `http://localhost:8888` | SearXNG instance URL |
| `SEARXNG_USERNAME` | _(none)_ | Optional basic auth |
| `SEARXNG_PASSWORD` | _(none)_ | Optional basic auth |
| `MCP_PORT` | `9555` | Docker HTTP port |

Config file search order: `./.env` → `~/.config/searxncrawl/.env` → auto-copy from `.env.example`.

### Dedup modes

- `exact` (default) — removes repeated markdown blocks; guardrail triggers if >60% sections removed
- `off` — no deduplication
