---
name: browser
description: Web scraping using shot-scraper. Read web pages, extract content, interact with websites.
---

# Browser Skill

## IMPORTANT: Fix Chinese Encoding
Before using shot-scraper with Chinese content, set UTF-8 encoding:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Basic Usage

### Extract headings
```powershell
shot-scraper javascript "URL" "Array.from(document.querySelectorAll('h1,h2,h3')).map(h=>h.innerText).join('\n')" -r
```

### Get full page text
```powershell
$text = shot-scraper javascript "URL" "document.body.innerText" -r
```

### Search for keywords
```powershell
$text -split "`n`n" | Where-Object { $_ -match "keyword" } | Select-Object -First 3
```

### Get main content (first 2000 chars)
```powershell
shot-scraper javascript "URL" "document.querySelector('main')?.innerText.substring(0,2000)" -r
```

## Advanced
- Use `shot-scraper --help` for more options
- Can perform clicks and interactions

## Notes
- Purchased: 2025-12-17 (10 Ciallo coins)
- Encoding fix discovered: 2025-12-17