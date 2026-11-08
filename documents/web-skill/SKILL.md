---
name: web-skill
description: Local web search and page fetching for AI agents via SearXNG and Firecrawl. Use when you need to search the web, fetch page content as markdown, or gather information from URLs. No API keys required.
---

# Web Skill

Local web search (SearXNG) and page scraping (Firecrawl) — no external API keys needed.

**Ports**: search = `localhost:8899`, fetch = `localhost:8898`

## Search

```bash
web_search "query"                          # 5 results
web_search "query" -n 10                    # more results
web_search "query" --engines google,bing    # specific engines
```

## Fetch Page Content

```bash
web_fetch https://example.com                           # markdown output
web_fetch https://example.com --formats markdown,links  # include links
```

Install path via `link-dotfiles`: `~/.local/bin/web_search`, `~/.local/bin/web_fetch`
Source files: `tools/search.ts`, `tools/fetch.ts`

## Output Format

### Search
```
--- Result 1 ---
Title: Page Title
URL: https://example.com/page
Snippet: Description from search results
Engines: google, bing
```

### Fetch
```
# Page Title

Source: https://example.com
Status: 200

Markdown content of the page...
```

## One-Time Setup

Only needed if SearXNG/Firecrawl aren't already running on ports 8899/8898:

```bash
cd ~/Projects/dotfiles/skills/web-skill
podman compose ps
```

If services are missing or stopped, start them:

```bash
cd ~/Projects/dotfiles/skills/web-skill
podman compose up -d
```

Verify: `podman compose ps` — 7 containers should be running.

Teardown: `podman compose down` (add `-v` to remove data volumes).

## When to Use

- Searching for documentation, API references, or current information
- Fetching and reading content from specific URLs as clean markdown
- Gathering information from multiple sources in parallel
- Any task requiring web access without interactive browsing
