---
name: d4vinci--scrapling
description: "Adaptive web scraping framework — handles everything từ single request đến full-scale crawl, tự động thích nghi khi site thay đổi. 59K stars."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Scrapling là adaptive web scraping framework: tự động adapt khi website thay đổi layout, không cần update selector.

## Install

```bash
pip install scrapling
scrapling install   # install browsers
```

## Quick start

```python
from scrapling import Fetcher

fetcher = Fetcher()
page = fetcher.get('https://example.com')

# Smart element finding — adapts to site changes
products = page.find_all('div.product', auto_match=True)
for p in products:
    print(p.find('span.price').text)
```

## Features

- Auto-match selectors khi site thay đổi
- Playwright + requests + httpx backends
- Anti-bot bypass built-in
- Agent Skill available

## Source

https://github.com/D4Vinci/Scrapling · ⭐59.8K
