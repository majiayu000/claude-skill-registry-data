---
name: crawl4ai
description: Crawl and extract web content for AI with Crawl4AI — async browser-based crawling with clean Markdown output, CSS/XPath/LLM extraction strategies, chunking, screenshot capture, session reuse for SPAs, and Docker deployment.
triggers:
  - "crawl4ai"
  - "crawl 4 ai"
  - "crawl4ai extract"
  - "async web crawler ai"
  - "crawl4ai markdown"
  - "crawl4ai css extraction"
  - "crawl4ai llm extraction"
  - "crawl4ai screenshot"
  - "crawl4ai session"
  - "browser crawling python"
  - "playwright crawler ai"
  - "web data extraction ai"
do_not_use_for:
  - Managed API scraping — use firecrawl instead
  - Browser automation (clicks/forms) — use browser-use instead
  - Simple HTTP scraping — use requests + BeautifulSoup instead
see_also:
  - firecrawl
  - browser-use
---

# Crawl4AI — Async Web Crawling for AI

**Source:** unclecode/crawl4ai (Apache 2.0) — fast async crawler with LLM-ready output

## Why Crawl4AI

- **Free & open source** — runs fully locally, no API key needed for basic crawling
- **Async-first**: concurrent crawling with asyncio
- **LLM-ready**: cleans HTML → Markdown automatically
- **Multiple extraction modes**: CSS selectors, XPath, LLM schema, cosine similarity
- **Session reuse**: handle SPAs with persistent browser sessions

## Install

```bash
pip install crawl4ai
crawl4ai-setup          # installs Playwright browsers
# or: python -m crawl4ai.async_webcrawler  (no setup needed)
```

## Basic Scrape

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://example.com")

        print(result.success)          # True/False
        print(result.markdown)         # clean Markdown
        print(result.cleaned_html)     # stripped HTML
        print(result.links)            # {"internal": [...], "external": [...]}
        print(result.media)            # images, videos, audio
        print(result.metadata)         # title, description, etc.

asyncio.run(main())
```

## Concurrent Crawling

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

urls = [
    "https://docs.example.com/page1",
    "https://docs.example.com/page2",
    "https://docs.example.com/page3",
]

async def crawl_many():
    config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=config,
            max_concurrent=5,    # parallel workers
        )

    for r in results:
        if r.success:
            print(r.url, len(r.markdown))

asyncio.run(crawl_many())
```

## CSS Extraction Strategy

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

schema = {
    "name": "Product Listings",
    "baseSelector": ".product-card",
    "fields": [
        {"name": "title",  "selector": "h2.title",         "type": "text"},
        {"name": "price",  "selector": ".price",           "type": "text"},
        {"name": "rating", "selector": ".stars",           "type": "attribute", "attribute": "data-rating"},
        {"name": "url",    "selector": "a",                "type": "attribute", "attribute": "href"},
        {"name": "image",  "selector": "img",              "type": "attribute", "attribute": "src"},
    ],
}

async def main():
    strategy = JsonCssExtractionStrategy(schema, verbose=True)
    config = CrawlerRunConfig(extraction_strategy=strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://shop.example.com/products",
            config=config,
        )

    products = json.loads(result.extracted_content)
    for p in products[:3]:
        print(p["title"], p["price"])

asyncio.run(main())
```

## LLM Extraction Strategy

```python
import asyncio
import json
from pydantic import BaseModel
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

class Article(BaseModel):
    title: str
    author: str
    published_date: str
    summary: str
    key_points: list[str]

async def main():
    strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="anthropic/claude-sonnet-4-5",
            api_token="your-anthropic-key",
        ),
        schema=Article.model_json_schema(),
        extraction_type="schema",
        instruction="Extract the article information precisely.",
    )

    config = CrawlerRunConfig(extraction_strategy=strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://blog.example.com/article-slug",
            config=config,
        )

    article = Article(**json.loads(result.extracted_content))
    print(article.title, article.author)

asyncio.run(main())
```

## Markdown Generation with Content Filter

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter

async def main():
    # Prune irrelevant content (nav, ads, sidebars)
    content_filter = PruningContentFilter(
        threshold=0.48,
        threshold_type="fixed",
        min_word_threshold=0,
    )

    # Or filter by relevance to a query
    bm25_filter = BM25ContentFilter(
        user_query="machine learning deployment",
        bm25_threshold=1.2,
    )

    md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
    config = CrawlerRunConfig(markdown_generator=md_generator)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://docs.example.com/ml-ops",
            config=config,
        )

    print(result.markdown.fit_markdown)    # filtered, relevant content
    print(result.markdown.raw_markdown)    # all content

asyncio.run(main())
```

## Session Reuse (SPA / Login)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

async def scrape_authenticated():
    browser_config = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Step 1: Login (reuse session)
        session_id = "my-session"

        login_result = await crawler.arun(
            url="https://app.example.com/login",
            config=CrawlerRunConfig(session_id=session_id),
            js_code="""
                document.querySelector('#email').value = 'user@example.com';
                document.querySelector('#password').value = 'password';
                document.querySelector('#login-btn').click();
                await new Promise(r => setTimeout(r, 2000));
            """,
        )

        # Step 2: Access protected pages with same session
        result = await crawler.arun(
            url="https://app.example.com/dashboard",
            config=CrawlerRunConfig(session_id=session_id),
        )
        print(result.markdown)

asyncio.run(scrape_authenticated())
```

## Screenshot & PDF

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
import base64

async def main():
    config = CrawlerRunConfig(
        screenshot=True,
        pdf=True,
        screenshot_wait_for=".content-loaded",  # CSS selector to wait for
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com", config=config)

    # Save screenshot
    if result.screenshot:
        with open("screenshot.png", "wb") as f:
            f.write(base64.b64decode(result.screenshot))

    # Save PDF
    if result.pdf:
        with open("page.pdf", "wb") as f:
            f.write(base64.b64decode(result.pdf))

asyncio.run(main())
```

## Deep Crawl (Multi-page)

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepGraphCrawlStrategy

async def main():
    strategy = BFSDeepGraphCrawlStrategy(
        max_depth=3,
        max_pages=50,
        include_patterns=["*/docs/*"],
        exclude_patterns=["*/blog/*", "*/changelog/*"],
        score_threshold=0.3,
    )

    config = CrawlerRunConfig(deep_crawl_strategy=strategy)

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(
            url="https://docs.example.com",
            config=config,
        )

    for result in results:
        if result.success:
            print(result.url, result.depth)

asyncio.run(main())
```

## Anti-Fake-Pass Checks

- [ ] `result.markdown` is a `MarkdownGenerationResult` object — access `.raw_markdown` or `.fit_markdown`
- [ ] `arun_many()` for concurrent crawling — not a loop of `arun()` calls
- [ ] CSS extraction `type: "attribute"` requires `attribute` field — without it returns empty
- [ ] LLM extraction costs API tokens per page — use CSS extraction when schema is static
- [ ] `session_id` must be the same string across calls to reuse browser context
- [ ] `crawl4ai-setup` must be run once to install Playwright browsers before first use
- [ ] `result.success` check before accessing content — failed crawls have empty markdown
