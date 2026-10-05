---
name: lead-scraper-pro
description: "Scrape Google Maps leads — extract business name, phone, email, website, rating"
version: 1.0.0
author:
  name: "LeadForge"
  github: "nous-hermeshub"
tags: [lead-generation, scraping, google-maps, business-data, sales]
category: business
platforms: [macos, linux]
published: 2026-06-18
license: MIT
metadata:
  hermes:
    related_skills: [web-scraping, n8n-automation, whatsapp-crm]
    icon: 🎯
---

## Overview

Scrapes Google Maps search results for any business category and location. Extracts: business name, address, phone number, website, rating, reviews count, and Google Maps URL. Outputs to CSV/JSON ready for CRM import.

## When to use

- Building a lead list for a new city/category
- Weekly lead generation batch jobs
- Market research — how many businesses in a niche?

## Prerequisites

- Python 3.8+
- `pip install requests beautifulsoup4`

## Step-by-step

### 1. Install

```bash
pip install requests beautifulsoup4
```

### 2. Basic usage

```bash
python scripts/scrape-maps.py --query "plumbers in Bangalore" --output leads.csv
```

### 3. Advanced usage

```bash
# Multiple categories, single location
python scripts/scrape-maps.py \
  --query "real estate agents in Mumbai" \
  --output mumbai-agents.csv \
  --max 200 \
  --format json

# Batch from file
python scripts/scrape-maps.py \
  --input cities.txt \
  --category "dentist" \
  --output all-leads.csv
```

## Output format

```csv
name,address,phone,website,rating,reviews,google_maps_url,source
"ABC Dental","MG Road, Mumbai","+91 98765 43210","https://abcdental.com","4.5","127","https://maps.google.com/...","maps"
```

## Pitfalls

- Google rate-limits aggressively — add `--delay 5` for 5-second pauses between results
- Use a VPN or proxy for large batches (500+ results)
- Free tier limited to ~200 results per session; upgrade to pro for unlimited

## Verification

```bash
# Check output file
head -5 leads.csv

# Count results
wc -l leads.csv

# Validate phone numbers
python3 -c "
import csv
with open('leads.csv') as f:
    reader = csv.DictReader(f)
    total = sum(1 for _ in reader)
    print(f'{total} leads collected')
"
```