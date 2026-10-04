---
name: data-scraper
description: "Extract data from websites, APIs, and files. Supports structured extraction, pagination, and anti-bot bypass."
triggers:
  - "scrape website"
  - "爬虫"
  - "extract data"
  - "web scraping"
---

# Data Scraper

Extract data from websites, APIs, and files.

## Features

- 🌐 **Web Scraping** — Extract from any website
- 📡 **API Scraping** — GET/POST requests
- 📄 **File Parsing** — CSV, Excel, PDF, JSON
- 🔄 **Pagination** — Auto-handle paginated content
- 🛡️ **Anti-bot** — Bypass protection
- 📊 **Data Cleaning** — Clean extracted data

## Usage

### Scrape Website

```bash
# Simple scrape
hermes scrape "https://example.com/products" \
  --selector ".product-item" \
  --fields name,price,image

# With pagination
hermes scrape "https://example.com/products" \
  --selector ".product" \
  --fields name,price \
  --pages 10
```

### Extract from API

```bash
hermes scrape-api "https://api.example.com/data" \
  --headers "Authorization: Bearer TOKEN" \
  --output data.json
```

### File Parsing

```bash
# Parse CSV
hermes scrape file data.csv --format json

# Parse Excel
hermes scrape file report.xlsx --sheet "Sales"

# Parse PDF
hermes scrape file document.pdf --extract text
```

## Configuration

```yaml
# scraper-config.yml
scraping:
  delay: 1000  # ms between requests
  retries: 3
  timeout: 30
  
anti_bot:
  rotate_user_agent: true
  use_proxy: false
  bypass_cloudflare: true
  
output:
  format: json
  encoding: utf-8
```

## Extractors

### CSS Selector
```bash
hermes scrape --selector ".product .title" --attr text
hermes scrape --selector "img.product" --attr src
```

### JSON Path
```bash
hermes scrape-json --path "$.data[*].name" --file data.json
```

### XPath
```bash
hermes scrape --xpath "//div[@class='product']/span" --file page.html
```

## Pitfalls

1. **Legal Issues** — Check robots.txt and terms of service
2. **Rate Limits** — Don't overload servers
3. **Data Quality** — Verify extracted data accuracy
4. **Anti-bot** — Some sites block scrapers