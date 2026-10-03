---
name: firecrawl-setup
description: Setup and configure Firecrawl web scraping API — install SDK on hermes-agent, manage API key, handle new SDK v1+ quirks.
---

# Firecrawl Setup Guide

## Prerequisites

- `uv` must be installed on the system (available at `/home/chihmin/.local/bin/uv`)
- Hermes-agent venv uses `pip` binary is missing — use `uv pip install ... --python venv/bin/python`

## Step 1 — Install SDK

```bash
cd /home/chihmin/Desktop/hermes-agent
uv pip install firecrawl-py --python venv/bin/python
```

**Note:** Package name is `firecrawl-py` (not `firecrawl`). **Do NOT use `venv/bin/pip`** — `pip` binary does not exist in this venv. Use `uv` instead.

## Step 2 — Write API Key to .env

Append to `~/.hermes/.env`:

```bash
echo "FIRECRAWL_API_KEY=<your-key>" >> ~/.hermes/.env
```

**IMPORTANT: Verify for duplicates.** After writing, always run `grep FIRECRAWL_API_KEY ~/.hermes/.env` and deduplicate if multiple lines appear (a known issue when re-running the append).

## Step 3 — Test the connection

```python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key='<your-key>')
result = app.scrape(url='https://example.com', formats=['markdown'])
print(result.markdown)
```

**If this fails**, the API key in `.env` is not auto-loaded by the new SDK — you must pass it explicitly to `FirecrawlApp(api_key=...)`.

## Usage (SDK v1+ API)

The Firecrawl SDK API changed in v1+. Common gotchas:

| Old API | New API | Notes |
|---------|---------|-------|
| `app.scrape_url(url, formats)` | `app.scrape(url=url, formats=[...])` | Method renamed, uses `url=` positional arg |
| `result['markdown']` | `result.markdown` | Returns `Document` (Pydantic model), NOT subscriptable |
| `app.crawl_url(url)` | `app.crawl(url=url)` | Method renamed |

### Available methods after instantiation

```python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key='<key>')

# Scrape single page
doc = app.scrape(url='https://example.com', formats=['markdown'])
print(doc.markdown)  # attribute access, NOT ['markdown']

# Crawl entire site
crawl = app.crawl(url='https://example.com')

# Search
results = app.search('query')

# Map (discover links)
links = app.map(url='https://example.com')
```

## API Key not auto-loaded

The new Firecrawl SDK does **not** auto-read `FIRECRAWL_API_KEY` from environment variables. Always pass it explicitly:

```python
import os
from firecrawl import FirecrawlApp

# Option A: explicit
app = FirecrawlApp(api_key='fc-your-key-here')

# Option B: load from .env manually if needed
import dotenv
dotenv.load_dotenv('.env')
app = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])
```

## Deduplication recipe

If `grep FIRECRAWL_API_KEY ~/.hermes/.env` shows more than one line:

```bash
grep -v "FIRECRAWL_API_KEY" ~/.hermes/.env > /tmp/env-clean
echo "FIRECRAWL_API_KEY=<correct-key>" >> /tmp/env-clean
mv /tmp/env-clean ~/.hermes/.env
```

## Pitfalls

- Package name is `firecrawl-py`, not `firecrawl`
- Venv has no `pip` binary — use `uv pip install ... --python venv/bin/python`
- New SDK does not auto-read `FIRECRAWL_API_KEY` from `.env`
- SDK v1+ uses `app.scrape(url=…)` not `app.scrape_url(…)`
- Results are Pydantic `Document` objects — access via attribute (`result.markdown`), not subscript (`result['markdown']`)
- `echo >> ~/.hermes/.env` can create duplicates on repeated runs — always verify with `grep`
