---
name: web-scraping-tools
description: Web scraping templates, scripts, and patterns for documentation and content collection using Playwright, BeautifulSoup, and Scrapy. Includes rate limiting, error handling, and extraction patterns. Use when scraping documentation, collecting web content, extracting structured data, building RAG knowledge bases, harvesting articles, crawling websites, or when user mentions web scraping, documentation collection, content extraction, Playwright scraping, BeautifulSoup parsing, or Scrapy spiders.
allowed-tools: Bash, Read, Write, Edit, mcp__playwright
---

# web-scraping-tools

## Instructions

This skill provides production-ready web scraping tools, templates, and patterns for documentation collection and content extraction. It includes functional scripts with rate limiting, error handling, and multiple scraping frameworks (Playwright, BeautifulSoup, Scrapy).

### 1. Choose the Right Scraping Tool

**Decision Matrix:**

| Use Case | Tool | Reason |
|----------|------|--------|
| JavaScript-heavy sites | Playwright | Full browser rendering |
| Static HTML parsing | BeautifulSoup | Lightweight, fast parsing |
| Large-scale crawling | Scrapy | Built-in concurrency, pipelines |
| Authentication required | Playwright | Cookie/session handling |
| Simple data extraction | BeautifulSoup | Minimal dependencies |
| Complex crawling rules | Scrapy | Spider middleware, rules |

### 2. Setup Scraping Environment

Install required dependencies:

```bash
# Setup Playwright scraper (includes browser installation)
bash ./skills/web-scraping-tools/scripts/setup-playwright-scraper.sh

# Install for BeautifulSoup
pip install beautifulsoup4 requests lxml

# Install for Scrapy
pip install scrapy
```

**What the setup script does:**
- Installs Playwright with Python bindings
- Installs Chromium, Firefox, WebKit browsers
- Configures browser contexts
- Sets up rate limiting utilities
- Creates output directories

### 3. Use Functional Scraper Scripts

**Scrape Documentation Sites:**
```bash
# Scrape technical documentation with automatic rate limiting
python ./skills/web-scraping-tools/scripts/scrape-documentation.py \
  --url "https://docs.example.com" \
  --output-dir "./scraped-docs" \
  --max-depth 3 \
  --rate-limit 2

# Parameters:
# --url: Starting URL to scrape
# --output-dir: Where to save scraped content
# --max-depth: How many levels deep to crawl
# --rate-limit: Seconds to wait between requests
```

**Features:**
- Automatic rate limiting (respectful scraping)
- Error handling and retries
- Content deduplication
- Markdown conversion
- Metadata extraction (title, description, keywords)
- Progress tracking

**Scrape Articles and Blog Posts:**
```bash
# Extract article content with readability parsing
python ./skills/web-scraping-tools/scripts/scrape-articles.py \
  --urls urls.txt \
  --output-dir "./articles" \
  --format markdown

# Input file format (urls.txt):
# https://blog.example.com/post-1
# https://blog.example.com/post-2
```

**Features:**
- Article content extraction (removes nav, ads, footers)
- Author and date detection
- Tag/category extraction
- Image downloading (optional)
- Multiple output formats (markdown, json, html)

### 4. Customizable Templates

**Playwright Scraper Template:**
```bash
# Copy template for customization
cp ./skills/web-scraping-tools/templates/playwright-scraper-template.py my-scraper.py

# Edit for your needs:
# - Update selectors for target site
# - Customize extraction logic
# - Add specific data transformations
# - Configure authentication if needed
```

**Template Features:**
- Browser context setup
- Page navigation with retries
- Element waiting strategies
- Screenshot capture
- Cookie/localStorage handling
- Concurrent page processing

**Rate-Limited Scraper Template:**
```bash
# Copy rate-limited scraper for respectful crawling
cp ./skills/web-scraping-tools/templates/rate-limited-scraper.py my-crawler.py
```

**Template Features:**
- Configurable request delays
- Exponential backoff on errors
- Request queue management
- robots.txt respect
- User-agent rotation
- Request logging

### 5. Real-World Examples

**Example 1: Scrape GitHub Documentation**
```bash
# Run GitHub docs scraper
python ./skills/web-scraping-tools/examples/scrape-github-docs.py \
  --repo "microsoft/playwright" \
  --output "./github-docs"
```

**What it does:**
- Scrapes README, Wiki, Docs folder
- Extracts code examples
- Downloads images
- Creates structured markdown
- Builds navigation index

**Example 2: Scrape Blog Posts**
```bash
# Run blog post scraper
python ./skills/web-scraping-tools/examples/scrape-blog-posts.py \
  --blog-url "https://blog.example.com" \
  --category "tutorials" \
  --max-posts 50
```

**What it does:**
- Finds all blog posts in category
- Extracts article content
- Captures metadata (author, date, tags)
- Downloads featured images
- Generates index JSON

### 6. Best Practices for Ethical Scraping

**Always Implement:**
- Rate limiting (1-2 seconds between requests minimum)
- User-agent identification
- robots.txt compliance
- Error handling and retries
- Request caching to avoid redundant requests

**Never Do:**
- Scrape faster than a human would browse
- Ignore robots.txt
- Overwhelm small sites with requests
- Scrape copyrighted content without permission
- Bypass authentication to access private data

**Respect Website Resources:**
```python
# Good: Rate limited with retries
await asyncio.sleep(2)  # Wait between requests
if response.status == 429:  # Too Many Requests
    await asyncio.sleep(60)  # Back off
    retry()

# Bad: Rapid fire requests
for url in urls:  # No delays
    scrape(url)  # Hammers server
```

### 7. Data Extraction Patterns

**CSS Selectors (BeautifulSoup/Playwright):**
```python
# Article content
content = soup.select_one('article.main-content')

# All links in navigation
nav_links = soup.select('nav a[href]')

# Metadata
title = soup.select_one('meta[property="og:title"]')['content']
description = soup.select_one('meta[name="description"]')['content']
```

**XPath Selectors (Scrapy/Playwright):**
```python
# Article with specific class
article = page.locator('xpath=//article[@class="post"]')

# All headings
headings = response.xpath('//h1 | //h2 | //h3/text()').getall()
```

**Pagination Handling:**
```python
# Follow "Next" button
while next_button := page.locator('a.next'):
    await next_button.click()
    await page.wait_for_load_state('networkidle')
    extract_data(page)
```

### 8. Output Formats

**Markdown (for RAG/Documentation):**
```python
output = {
    'title': title,
    'url': url,
    'content': markdown_content,
    'metadata': {
        'author': author,
        'date': date,
        'tags': tags
    }
}
```

**JSON (for structured data):**
```python
{
    "url": "https://example.com/page",
    "title": "Page Title",
    "content": "Full text content...",
    "links": ["url1", "url2"],
    "images": ["img1.jpg", "img2.png"],
    "scraped_at": "2025-10-31T21:43:00Z"
}
```

**SQLite (for large datasets):**
```python
# Store in database for efficient querying
conn = sqlite3.connect('scraped_data.db')
cursor.execute('''
    INSERT INTO pages (url, title, content, scraped_at)
    VALUES (?, ?, ?, ?)
''', (url, title, content, datetime.now()))
```

## Requirements

**Python Dependencies:**
```
playwright>=1.40.0
beautifulsoup4>=4.12.0
requests>=2.31.0
lxml>=4.9.0
scrapy>=2.11.0
aiohttp>=3.9.0
markdownify>=0.11.0
```

**System Requirements:**
- Python 3.10+
- 500MB disk space for browsers (Playwright)
- Internet connection for scraping

**Installation:**
```bash
pip install playwright beautifulsoup4 requests lxml scrapy aiohttp markdownify
playwright install chromium
```

## Examples

### Example 1: Scrape Technical Documentation

**Use Case:** Build a RAG knowledge base from Python documentation

```bash
python ./skills/web-scraping-tools/examples/scrape-github-docs.py \
  --repo "python/cpython" \
  --docs-path "Doc" \
  --output "./python-docs" \
  --format markdown
```

**Result:**
- 500+ documentation pages as markdown
- Properly formatted code examples
- Navigation structure preserved
- Images downloaded locally
- Metadata JSON index

### Example 2: Scrape Tutorial Articles

**Use Case:** Collect programming tutorials for training data

```bash
python ./skills/web-scraping-tools/examples/scrape-blog-posts.py \
  --blog-url "https://realpython.com" \
  --category "tutorials" \
  --max-posts 100 \
  --output "./tutorials"
```

**Result:**
- 100 tutorial articles in markdown
- Author and publication date
- Code examples extracted
- Tags and categories
- Index of all articles

### Example 3: Monitor Competitor Content

**Use Case:** Track new posts on competitor blogs

```bash
# Setup scheduled scraper
python ./skills/web-scraping-tools/scripts/scrape-articles.py \
  --urls competitor-urls.txt \
  --output "./competitor-content" \
  --since-date "2025-10-01" \
  --notify-new
```

**Result:**
- Only new content since last run
- Email notification on new posts
- Diff from previous scrape
- Change tracking

## Troubleshooting

**Playwright browser installation fails:**
```bash
# Manual browser installation
playwright install chromium

# Or use system browser
PLAYWRIGHT_BROWSERS_PATH=/usr/bin playwright install
```

**Rate limiting / 429 errors:**
- Increase delay between requests (`--rate-limit 5`)
- Reduce concurrency (`--max-concurrent 1`)
- Add random jitter to delays
- Check robots.txt for crawl-delay directive

**JavaScript content not loading:**
- Use Playwright instead of BeautifulSoup
- Add explicit waits for elements
- Wait for network idle: `page.wait_for_load_state('networkidle')`

**Memory issues with large scrapes:**
- Process pages in batches
- Clear browser cache between pages
- Use Scrapy for better memory management
- Write to disk incrementally, don't hold in memory

**Blocked by anti-bot protection:**
- Rotate user agents
- Add realistic delays
- Use residential proxies (if legal and permitted)
- Respect robots.txt and Terms of Service

## Performance Optimization

**Concurrent Scraping:**
```python
# Use asyncio for parallel requests
import asyncio

async def scrape_all(urls):
    tasks = [scrape_page(url) for url in urls]
    return await asyncio.gather(*tasks)
```

**Caching:**
```python
# Cache responses to avoid re-scraping
import diskcache

cache = diskcache.Cache('./scrape-cache')

if url in cache:
    return cache[url]
else:
    content = scrape(url)
    cache[url] = content
    return content
```

**Incremental Updates:**
```python
# Track what's already scraped
scraped_urls = load_scraped_urls()
new_urls = [url for url in all_urls if url not in scraped_urls]
scrape_batch(new_urls)
```

---

**Plugin:** rag-pipeline
**Version:** 1.0.0
**Category:** Data Collection
**Skill Type:** Web Scraping & Content Extraction
