---
name: firecrawl
description: Scrape and crawl websites for AI with Firecrawl — scrape single URLs to clean Markdown/HTML, crawl entire sites with depth/path filters, extract structured data with LLM schema, use map to discover all URLs, and batch scrape multiple pages in parallel.
triggers:
  - "firecrawl"
  - "fire crawl"
  - "firecrawl scrape"
  - "firecrawl crawl"
  - "firecrawl extract"
  - "web scraping ai"
  - "scrape to markdown"
  - "crawl website ai"
  - "firecrawl map"
  - "firecrawl batch"
  - "structured data extraction web"
  - "web scraping llm"
do_not_use_for:
  - General web crawling without AI parsing — use Playwright or Puppeteer instead
  - Web automation (clicking, forms) — use browser-use instead
  - Simple fetch/parse — use BeautifulSoup + requests instead
see_also:
  - crawl4ai
  - browser-use
---

# Firecrawl — Web Scraping for AI

**Source:** mendableai/firecrawl (AGPL-3.0) — turn websites into LLM-ready data

## Why Firecrawl

- Returns clean **Markdown** (not raw HTML) — ready for LLM context
- Handles JavaScript-rendered pages (headless browser under the hood)
- Built-in LLM extraction with Pydantic schema
- **Crawl** entire sites, **map** all URLs, **batch** scrape in parallel
- Managed API or self-hosted Docker

## Install

```bash
pip install firecrawl-py
# or
npm install @mendable/firecrawl-js
```

## Scrape a Single URL

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your-api-key")

# Basic scrape — returns Markdown
result = app.scrape_url(
    "https://docs.anthropic.com/en/docs/about-claude/models",
    params={"formats": ["markdown"]},
)
print(result["markdown"])  # clean markdown content
print(result["metadata"]["title"])
print(result["metadata"]["description"])

# Get both markdown + raw HTML
result = app.scrape_url(
    "https://example.com",
    params={"formats": ["markdown", "html"]},
)
```

## Crawl an Entire Website

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your-api-key")

# Async crawl (recommended for large sites)
crawl_job = app.async_crawl_url(
    "https://docs.example.com",
    params={
        "limit": 100,                      # max pages
        "maxDepth": 3,                     # crawl depth
        "includePaths": ["/docs/.*"],      # regex: only docs pages
        "excludePaths": ["/blog/.*"],      # regex: skip blog
        "formats": ["markdown"],
        "onlyMainContent": True,           # strip nav/footer/ads
    },
)

job_id = crawl_job["id"]

# Poll until done (or use webhook)
import time
while True:
    status = app.check_crawl_status(job_id)
    if status["status"] == "completed":
        break
    print(f"Crawled: {status['completed']}/{status['total']}")
    time.sleep(5)

# Get results
pages = status["data"]  # list of scraped pages
for page in pages:
    print(page["url"], len(page["markdown"]))
```

## Structured Data Extraction (LLM-powered)

```python
from firecrawl import FirecrawlApp
from pydantic import BaseModel

app = FirecrawlApp(api_key="fc-your-api-key")

class ProductInfo(BaseModel):
    name: str
    price: float
    rating: float
    reviews_count: int
    in_stock: bool
    features: list[str]

result = app.scrape_url(
    "https://www.amazon.com/dp/B08N5WRWNW",
    params={
        "formats": ["extract"],
        "extract": {
            "schema": ProductInfo.model_json_schema(),
            "systemPrompt": "Extract product information accurately.",
        },
    },
)

product = ProductInfo(**result["extract"])
print(product.name, product.price, product.rating)
```

## Map — Discover All URLs

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your-api-key")

# Get all URLs from a site without scraping content
map_result = app.map_url(
    "https://docs.example.com",
    params={
        "search": "authentication",    # filter URLs by keyword
        "limit": 500,
    },
)

urls = map_result["links"]
print(f"Found {len(urls)} URLs")
for url in urls[:10]:
    print(url)
```

## Batch Scrape (Multiple URLs in Parallel)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your-api-key")

urls = [
    "https://docs.example.com/page-1",
    "https://docs.example.com/page-2",
    "https://docs.example.com/page-3",
]

# Async batch scrape
batch_job = app.async_batch_scrape_urls(
    urls,
    params={"formats": ["markdown"], "onlyMainContent": True},
)

# Poll for completion
status = app.check_batch_scrape_status(batch_job["id"])
results = status["data"]
```

## Webhook (Push Results)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-your-api-key")

# Crawl with webhook — no polling needed
crawl_job = app.async_crawl_url(
    "https://docs.example.com",
    params={
        "limit": 200,
        "webhook": {
            "url": "https://your-server.com/webhook/firecrawl",
            "headers": {"Authorization": "Bearer your-token"},
            "events": ["completed", "page"],  # page = per-page results
        },
    },
)
```

## With LangChain

```python
from langchain_community.document_loaders import FireCrawlLoader

loader = FireCrawlLoader(
    api_key="fc-your-api-key",
    url="https://docs.example.com",
    mode="crawl",       # "scrape" | "crawl"
    params={"limit": 50, "formats": ["markdown"]},
)

docs = loader.load()
# Each doc is a LangChain Document with page_content + metadata
for doc in docs[:3]:
    print(doc.metadata["url"])
    print(doc.page_content[:200])
```

## Self-Hosted (Docker)

```bash
git clone https://github.com/mendableai/firecrawl
cd firecrawl

# Copy env file and configure
cp apps/api/.env.example apps/api/.env
# Edit .env: set OPENAI_API_KEY (for LLM extraction)

# Start all services
docker compose up -d

# Use with local endpoint
app = FirecrawlApp(api_key="test", api_url="http://localhost:3002")
```

## JavaScript (Node.js)

```typescript
import FirecrawlApp from "@mendable/firecrawl-js";
import { z } from "zod";

const app = new FirecrawlApp({ apiKey: "fc-your-api-key" });

// Scrape
const scrapeResult = await app.scrapeUrl("https://example.com", {
  formats: ["markdown"],
});
console.log(scrapeResult.markdown);

// Extract with Zod schema
const schema = z.object({
  company_mission: z.string(),
  founding_year: z.number(),
  team_size: z.number(),
});

const extractResult = await app.scrapeUrl("https://example.com/about", {
  formats: ["extract"],
  extract: { schema },
});
console.log(extractResult.extract);
```

## Anti-Fake-Pass Checks

- [ ] `result["markdown"]` — not `result.content` or `result.text`
- [ ] Async crawl needs `check_crawl_status(job_id)` polling — `async_crawl_url` only starts the job
- [ ] `onlyMainContent: true` strips nav/footer — important for clean LLM context
- [ ] `extract` format requires LLM API key configured in Firecrawl (cloud or self-hosted)
- [ ] `map_url` returns URLs only — no content; use `batch_scrape` to get content for those URLs
- [ ] Rate limits on free tier: 500 pages/month, 10 pages/min — use async + webhook for large crawls
