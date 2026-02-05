---
name: context-scrapers
description: Web scraping spiders (Scrapy), parsers, and source management.
tags: [backend, data, scrapers]
---

# Scrapers Context

## Overview
Web scraping infrastructure using Scrapy. Handles data acquisition from city councils (Legistar) and municipal codes (Municode).

## Active Files

### Spiders
- `backend/affordabot_scraper/affordabot_scraper/spiders/sanjose_meetings.py` - Legistar meeting scraper
- `backend/affordabot_scraper/affordabot_scraper/spiders/sanjose_municode.py` - Municode scraper

### Configuration
- `backend/affordabot_scraper/affordabot_scraper/pipelines.py` - Item pipelines (DB storage)
- `backend/affordabot_scraper/affordabot_scraper/settings.py` - Scrapy settings

### Verification Scripts
- `scripts/verify_raw_scrapes.py` - Check raw_scrapes table
- `scripts/verify_municode_discovery.py` - Verify discovery logic

## Usage
Use this skill when modifying scrapers, adding new jurisdictions, or debugging ingestion.
