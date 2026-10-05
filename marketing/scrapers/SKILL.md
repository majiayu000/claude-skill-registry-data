---
name: scrapers
description: Use when data extraction hub — content monitoring, price tracking, web
  scraping, and social listening for competitive intelligence, market research, and
  automated revenue generation.
domain: automation
author: oyi77
license: Apache-2.0
subdomain: web-scraping
tags:
- automation
- scrapers
- content-monitor
- price-tracker
- smart-scraper
- social-listener
- data
- intelligence
version: 1.0.0
category: automation
---
## Overview

This skill is the data extraction hub covering content monitoring, price tracking, web scraping, and social listening. Load it when you need structured data pulled from external sites on a schedule. It covers scraper design, anti-blocking, and feeding results into competitive or market intelligence pipelines.


# Scrapers — Data Extraction Hub

## Money-Making Overview

| Tool | Data You Extract | Monthly Revenue Potential | Effort |
|---|---|---|---|
| **Content Monitor** | Competitor article/blog updates, regulatory changes, job postings | $500-$3,000/mo | Low |
| **Price Tracker** | E-commerce pricing, competitor discounts, restock alerts | $1,000-$5,000/mo | Medium |
| **Smart Scraper** | Custom web scraping — product catalogs, reviews, directories, leads | $2,000-$8,000/mo | Medium-High |
| **Social Listener** | Brand mentions, sentiment analysis, trend detection, influencer discovery | $1,000-$4,000/mo | Medium |
| **All Four Combined** | Full competitive intelligence + market monitoring package | $3,000-$15,000/mo | Managed |

**Combined Revenue Potential: $3,000-$15,000/mo** as a productized data-as-a-service (DaaS) offering.

---

## Combined Capabilities Table

| Capability | Content Monitor | Price Tracker | Smart Scraper | Social Listener |
|---|---|---|---|---|
| Data type | Articles, blog posts, docs | Product prices, inventory | Any web page | Social posts, comments, mentions |
| Trigger | Schedule + change detection | Schedule + price drop threshold | Schedule + event | Keyword + schedule |
| Output | Diff reports, summaries | Price history, alerts | Structured JSON/CSV | Sentiment trends, alerts |
| Anti-blocking | Respect robots.txt, user-agent rotation | Proxy rotation, request throttling | Headless browser, captcha solving | Platform API (official) |
| Storage | Git-like version history | Timeseries DB (SQLite/Influx) | File/DB | Elasticsearch/Postgres |
| Monetization | Alert subscriptions | Deal alerts + affiliate | Lead gen, market research | Brand monitoring, crisis alerts |

---

## 1. Content Monitor

### Overview

Content monitoring watches websites, blogs, docs, and RSS feeds for changes. When new content appears, it extracts the diff, summarizes, and alerts via Telegram/Slack/email. Essential for competitive intelligence and regulatory monitoring.

### Quick Start — Python Watchdog

```python
import requests
import hashlib
import time
from difflib import unified_diff
import smtplib

MONITOR_SITES = [
    {"url": "https://competitor.com/blog", "name": "Competitor Blog"},
    {"url": "https://docs.example.com/changelog", "name": "Changelog"},
]

# Local hash cache — in production use Redis/DB
hash_cache = {}

def check_site(entry):
    url = entry["url"]
    name = entry["name"]

    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    content = resp.text
    content_hash = hashlib.sha256(content.encode()).hexdigest()

    previous = hash_cache.get(url)
    if previous and previous != content_hash:
        # Content changed — extract diff
        lines_old = previous.get("lines", [""])
        lines_new = content.splitlines()
        diff = "\n".join(unified_diff(lines_old, lines_new, lineterm=""))

        # Alert
        alert = f"[{name}] Content changed!\n{diff[:1000]}"
        print(alert)  # Replace with Telegram/Slack webhook

    # Update cache
    hash_cache[url] = {
        "hash": content_hash,
        "lines": content.splitlines()[:50],  # store first 50 lines
        "checked_at": time.time()
    }

# Run every hour
while True:
    for site in MONITOR_SITES:
        try:
            check_site(site)
        except Exception as e:
            print(f"Error checking {site['name']}: {e}")
    time.sleep(3600)
```

### RSS-Based Monitoring (Zero-Block)

```python
import feedparser
from datetime import datetime, timezone

FEEDS = [
    "https://medium.com/feed/@competitor",
    "https://news.ycombinator.com/rss",
    "https://aws.amazon.com/new/feed/"
]

seen_ids = set()

def check_feeds():
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            if entry.id not in seen_ids:
                seen_ids.add(entry.id)
                print(f"NEW: {entry.title}")
                print(f"     {entry.link}")
                # Alert via webhook

while True:
    check_feeds()
    time.sleep(900)  # 15 min
```

### Money-Making Workflows

1. **Competitive Intelligence Alerts** — Monitor competitor blog, pricing page, job listings; $100-$300/mo per client
2. **Regulatory Change Monitor** — Watch government/regulator websites for rule changes; $200-$500/mo (high-value for compliance teams)
3. **Job Posting Monitor** — Track competitor hiring to detect strategy shifts; $100-$200/mo
4. **Content Aggregator** — Curate industry news for a newsletter; monetize through sponsorship
5. **Documentation Drift** — Monitor API docs for breaking changes; $100-$200/mo per product

---

## 2. Price Tracker

### Overview

Price trackers automatically check e-commerce product prices at regular intervals, log the history, and alert when prices drop below a target threshold. This is a proven affiliate revenue machine.

### Quick Start — Python Price Tracker

```python
import requests
import json
import sqlite3
import smtplib
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCTS = [
    {
        "url": "https://shopee.co.id/product/123456789",
        "name": "Gadget X",
        "target_price": 500000,
        "affiliate_link": "https://lynk.id/gadget-x-deal"
    },
    {
        "url": "https://tokopedia.com/product/987654321",
        "name": "Headphone Y",
        "target_price": 250000,
        "affiliate_link": "https://lynk.id/headphone-y-deal"
    }
]

def init_db():
    conn = sqlite3.connect("prices.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            product TEXT, price INTEGER, currency TEXT,
            timestamp TEXT, url TEXT
        )
    """)
    return conn

def check_price(product):
    resp = requests.get(product["url"], headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
    soup = BeautifulSoup(resp.text, "html.parser")

    # Platform-specific selectors — adjust per site
    price_el = soup.select_one("[data-testid='product-price']")
    if not price_el:
        price_el = soup.select_one(".price")

    if price_el:
        price_text = price_el.text.strip().replace("Rp", "").replace(".", "").replace(",", "")
        current_price = int(price_text)
        return current_price
    return None

def monitor_loop():
    conn = init_db()

    while True:
        for product in PRODUCTS:
            price = check_price(product)
            if price is None:
                print(f"Could not parse price for {product['name']}")
                continue

            # Log to DB
            conn.execute(
                "INSERT INTO price_history VALUES (?, ?, ?, ?, ?)",
                (product["name"], price, "IDR", datetime.now().isoformat(), product["url"])
            )
            conn.commit()

            # Check threshold
            if price <= product["target_price"]:
                alert = f"🔥 PRICE DROP: {product['name']} now Rp{price:,}!\n"
                alert += f"Buy: {product['affiliate_link']}"
                print(alert)
                # Send alert via Telegram/Slack/email

            print(f"{product['name']}: Rp{price:,} (target: Rp{product['target_price']:,})")

        time.sleep(3600)  # Check hourly

monitor_loop()
```

### Anti-Detection Tips

```python
# Rotate user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
]

# Use proxies for high-volume scraping
proxies = {
    "http": "http://user:pass@proxy:8080",
    "https": "http://user:pass@proxy:8080",
}

# Add random delays
import random
import time
time.sleep(random.uniform(2, 5))

# Use headless browser for JS-rendered pages
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(url)
price = driver.find_element("css selector", ".price").text
driver.quit()
```

### Money-Making Workflows

1. **Deal Alert Affiliate Bot** — Track prices on Shopee/Tokopedia/Amazon; alert subscribers with affiliate link; earn 5-30% commission
2. **Competitor Pricing Monitor** — Track competitor price changes hourly; $200-$500/mo per client
3. **Restock Notifier** — Monitor "out of stock" → "in stock" for hot items; sell alerts
4. **Price History API** — Expose historical pricing via API; $50-$200/mo subscription
5. **Arbitrage Finder** — Compare prices across platforms; alert on profitable differences

---

## 3. Smart Scraper

### Overview

Smart scraping extracts structured data from any website — directories, reviews, product catalogs, real estate listings, job boards. Use Playwright/Selenium for JS-rendered pages, or `requests + BeautifulSoup` for static HTML.

### Quick Start — Playwright Scraper

```python
import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_listing(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Extract structured data
        data = await page.evaluate("""
            () => ({
                title: document.querySelector('h1')?.innerText,
                price: document.querySelector('.price')?.innerText,
                description: document.querySelector('.description')?.innerText,
                images: Array.from(document.querySelectorAll('.gallery img')).map(i => i.src),
                specs: Array.from(document.querySelectorAll('.specs tr')).map(row => ({
                    key: row.cells[0]?.innerText,
                    value: row.cells[1]?.innerText
                }))
            })
        """)

        await browser.close()
        return data

# Run
result = asyncio.run(scrape_listing("https://example.com/product/123"))
print(json.dumps(result, indent=2))
```

### Scraper Pipeline Architecture

```python
# pipeline.py — production scraper architecture
import json
import sqlite3
from datetime import datetime

class ScraperPipeline:
    def __init__(self, name, extract_fn):
        self.name = name
        self.extract_fn = extract_fn
        self.conn = sqlite3.connect(f"{name}_data.db")

    def init_storage(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data JSON, url TEXT UNIQUE,
                scraped_at TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS scrape_log (
                url TEXT, status TEXT, items INTEGER,
                error TEXT, scraped_at TEXT
            )
        """)
        self.conn.commit()

    def scrape_url(self, url):
        try:
            data = self.extract_fn(url)
            self.conn.execute(
                "INSERT OR REPLACE INTO scraped_data (data, url, scraped_at) VALUES (?, ?, ?)",
                (json.dumps(data), url, datetime.now().isoformat())
            )
            self.conn.execute(
                "INSERT INTO scrape_log (url, status, items, scraped_at) VALUES (?, 'success', ?, ?)",
                (url, len(data) if isinstance(data, list) else 1, datetime.now().isoformat())
            )
            self.conn.commit()
            return data
        except Exception as e:
            self.conn.execute(
                "INSERT INTO scrape_log (url, status, error, scraped_at) VALUES (?, 'failed', ?, ?)",
                (url, str(e), datetime.now().isoformat())
            )
            self.conn.commit()
            raise

    def export_csv(self, output_path):
        import csv
        rows = self.conn.execute("SELECT data, url, scraped_at FROM scraped_data")
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'data', 'scraped_at'])
            for row in rows:
                writer.writerow(row)

# Usage
def extract_products(url):
    # Playwright/Selenium logic here
    return {"title": "Product", "price": 100, "reviews": 42}

pipeline = ScraperPipeline("products", extract_products)
pipeline.init_storage()
data = pipeline.scrape_url("https://example.com/products")
pipeline.export_csv("products_export.csv")
```

### Anti-Blocking Strategy

| Technique | When to Use | Implementation |
|---|---|---|
| Rotate user agents | Always | Random pick from pool of 10+ |
| Rotate proxies | High-volume | Residential proxy service ($30-$100/mo) |
| Random delays | Low-volume | `time.sleep(random.uniform(1, 5))` |
| Headless browser | JS-rendered sites | Playwright/Selenium |
| Respect robots.txt | Legitimate use | `robotparser` module |
| CAPTCHA solving | Occasional blocks | 2Captcha, Anti-Captcha (~$2/1K solves) |
| Cookie/session persistence | Login-required | Playwright storage state |

### Money-Making Workflows

1. **Lead Generation as a Service** — Scrape directories (Yellow Pages, Google Maps, LinkedIn) for leads: $500-$2,000/mo
2. **Product Catalog Dropshipping** — Scrape supplier catalogs, auto-update your store; $1,000-$5,000/mo
3. **Review Monitoring** — Scrape reviews across platforms for brand monitoring; $200-$500/mo
4. **Real Estate Data Feed** — Scrape listings; sell as structured data to investors; $500-$2,000/mo
5. **Job Board Aggregator** — Scrape job listings; sell as recruiting feed; $1,000-$4,000/mo
6. **White-Label Data API** — Collect data from 5+ sources, expose as REST API: $200-$1,000/mo

---

## 4. Social Listener

### Overview

Social listening monitors brand mentions, keywords, sentiment, and trends across Twitter/X, Reddit, Instagram, TikTok, and news. Combined with sentiment analysis, it provides real-time brand intelligence.

### Quick Start — Multi-Platform Listener

```python
import requests
import json
from datetime import datetime, timedelta
import re
import sqlite3

KW_MONITORS = [
    {"keywords": ["yourbrand", "your product name"], "platform": "all"},
    {"keywords": ["competitor name"], "platform": "twitter"},
    {"keywords": ["industry trend"], "platform": "reddit"},
]

class SocialListener:
    def __init__(self):
        self.conn = sqlite3.connect("mentions.db")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS mentions (
                id TEXT PRIMARY KEY,
                platform TEXT, author TEXT, content TEXT,
                sentiment REAL, url TEXT,
                mentioned_at TEXT, captured_at TEXT
            )
        """)

    def analyze_sentiment(self, text):
        """Simple lexicon-based sentiment scoring."""
        positive = {"good", "great", "amazing", "love", "excellent", "awesome", "best"}
        negative = {"bad", "terrible", "awful", "hate", "worst", "poor", "horrible"}
        words = set(re.findall(r'\w+', text.lower()))
        score = (len(words & positive) - len(words & negative)) / max(len(words), 1)
        return round(score, 3)

    def check_twitter(self, keyword):
        """Search Twitter via agent-reach or API."""
        import subprocess
        result = subprocess.run(
            ["agent-reach", "twitter", "search", keyword, "--limit", "20", "--format", "json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return []

    def check_reddit(self, keyword):
        """Search Reddit."""
        resp = requests.get(
            f"https://www.reddit.com/search.json?q={keyword}&limit=20&sort=new",
            headers={"User-Agent": "brand-monitor/1.0"}
        )
        if resp.status_code == 200:
            data = resp.json()
            return [{
                "id": post["data"]["id"],
                "author": post["data"]["author"],
                "content": post["data"]["title"] + " " + post["data"].get("selftext", ""),
                "url": f"https://reddit.com{post['data']['permalink']}",
                "created_utc": post["data"]["created_utc"]
            } for post in data["data"]["children"]
            if not post["data"].get("stickied")]
        return []

    def store_mention(self, mention):
        mention["sentiment"] = self.analyze_sentiment(mention["content"])
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO mentions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (mention["id"], mention["platform"], mention["author"],
                 mention["content"], mention["sentiment"], mention["url"],
                 mention["created_utc"], datetime.now().isoformat())
            )
            self.conn.commit()
        except Exception as e:
            print(f"Store error: {e}")

    def run_check(self):
        for monitor in KW_MONITORS:
            kw = monitor["keywords"][0]  # primary keyword
            platform = monitor["platform"]

            if platform in ("all", "twitter"):
                for mention in self.check_twitter(kw):
                    self.store_mention(mention)

            if platform in ("all", "reddit"):
                for mention in self.check_reddit(kw):
                    self.store_mention(mention)

    def generate_report(self, hours=24):
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        rows = self.conn.execute(
            "SELECT platform, COUNT(*) as count, AVG(sentiment) as avg_sentiment "
            "FROM mentions WHERE captured_at > ? GROUP BY platform",
            (cutoff,)
        )
        report = {}
        for platform, count, sentiment in rows:
            report[platform] = {
                "mentions": count,
                "avg_sentiment": round(sentiment, 3) if sentiment else 0,
                "alert": sentiment is not None and sentiment < -0.3
            }
        return report

listener = SocialListener()
listener.run_check()
report = listener.generate_report(24)
print(json.dumps(report, indent=2))
```

### Sentiment Alerting

```python
# Alert on negative sentiment spike
def check_alerts():
    report = listener.generate_report(1)  # last hour
    for platform, stats in report.items():
        if stats.get("alert"):
            send_slack_alert(
                f"⚠️ Negative sentiment spike on {platform}!\n"
                f"Mentions: {stats['mentions']} | Sentiment: {stats['avg_sentiment']}"
            )
```

### Money-Making Workflows

1. **Brand Sentiment Monitoring** — Monthly report + real-time alerts; $200-$500/mo per brand
2. **Crisis Detection** — Alert within minutes of negative virality; $300-$800/mo
3. **Competitor Intel** — Track competitor campaigns, launches, sentiment; $200-$400/mo
4. **Trend Detection** — Identify emerging trends before they go mainstream; sell to content creators/marketers
5. **Influencer Discovery** — Find high-engagement accounts mentioning your keywords; $200-$500/mo
6. **Product Feedback Mining** — Extract feature requests and complaints from social mentions; $300-$600/mo

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Scraping is illegal/shady" | Scraping public data is legal; respect robots.txt, rate limits, and ToS |
| "I can just use Google Alerts" | Google Alerts is delayed by hours/days; misses 80% of mentions |
| "Websites will block me" | Rotate user agents + proxies + delays = 99%+ success rate |
| "Social listening needs expensive tools" | Python + free tier APIs = $0; upgrade when revenue justifies |
| "I don't know what to scrape" | Start with competitor prices + brand mentions = proven demand |
| "Price tracking is saturated" | Most price trackers are region-specific; dominate your local market |
| "AI will replace scraping" | AI generates text; scraping extracts REAL data (prices, inventory, reviews) |

---

## First Action in 60 Minutes

1. **Set up Price Tracker** — Track 3 products from Shopee/Tokopedia; log to SQLite (10 min)
2. **Deploy Content Monitor** — Watch competitor blog + one RSS feed; alert via Telegram (10 min)
3. **Build Social Listener** — Monitor your brand on Twitter + Reddit; store mentions (15 min)
4. **Scrape one lead source** — Directory/review page → CSV (10 min)
5. **Create alert pipeline** — Webhook → Telegram/Slack for price drops + negative sentiment (10 min)
6. **Document your stack** — Tweet: "I built a price tracker in 30 min" (5 min)
7. **Day 2** — Add affiliate links to price alerts; first commission tracks
8. **Week 2** — Productize one scraper as a $200/mo service for a client
9. **Month 1** — 3 clients on brand monitoring + price tracking = $1,000-1,500/mo MRR

---

## Verification

- [ ] Price tracker successfully extracts prices from target e-commerce sites
- [ ] Content monitor detects changes and generates accurate diffs
- [ ] Smart scraper handles JS-rendered pages (Playwright test)
- [ ] Social listener captures mentions across at least 2 platforms
- [ ] Sentiment analysis produces reasonable scores (test with known-positive/negative text)
- [ ] Alerts fire correctly on price drops and negative sentiment
- [ ] Rate limits respected (no IP blocks during testing)
- [ ] All scraped data stores to structured storage (SQLite/CSV/JSON)
- [ ] At least one money workflow is running (affiliate link in price alert, or client data delivery)


## When to Use
Use this skill when working with scrapers.


## Workflow
See the parent skill for authoritative workflow documentation.
