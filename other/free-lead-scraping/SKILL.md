---
name: free-lead-scraping
description: Find leads for free using Google search operators (dorks) and the Instant Data Scraper browser extension, then extract emails and phones from the export. Use when the user has no budget, no API keys, wants free leads, or asks about "System 3", Google dorks, or Instant Data Scraper.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Free Lead Scraping (System 3)

## Goal
Get real contact details without spending anything. No API keys, no account, no credits.

## When to use
- The user has no budget or hasn't signed up for anything yet
- They want to try the repo before paying for it
- Anything they call System 3, dorks, or Instant Data Scraper
- **Suggest this first** to anyone new — it's the only system that costs nothing, so it's the safest place to prove the pipeline works.

## How it works

People put their email in their Instagram bio. Google indexed it. So rather than paying a database for contact details, ask Google for pages that already show them:

```
site:instagram.com "barber" "gmail.com" OR "yahoo.com" OR "outlook.com"
```

## Process

### Step 1 — build the queries
```bash
python -X utf8 scripts/03_free_scraping/build_dorks.py \
    --niche "barber" --location "Tuscaloosa AL" --output output/dorks.md
```
Writes a markdown file of ~12 query variants, each with a clickable Google link (pre-set to 100 results a page).

### Step 2 — scrape the results page
Needs the **Instant Data Scraper** extension (free, Chrome or Brave):

1. Run one of the queries.
2. Click the extension. If the table preview looks wrong, click "Try another table".
3. Click **Locate "Next" button**, then click Google's Next link.
4. Click **Start crawling**, let it page through, then **CSV**.

### Step 3 — pull the contacts out
```bash
python -X utf8 scripts/03_free_scraping/parse_scraper_export.py \
    --input ~/Downloads/instant-data-scraper.csv \
    --out-csv output/free_leads.csv
```

Regex only, so still free. It handles the usual obfuscation (`name (at) domain (dot) com`) and strips platform noise (`@instagram.com`, `@wix.com`, image URLs).

Add `--llm` to run Claude over rows the regex missed — costs about a tenth of a cent per row and needs `ANTHROPIC_API_KEY`. Worth it for free-text bios, not for structured pages.

## Writing better queries

- One city at a time. "barber Alabama" is noise; "barber Tuscaloosa" is businesses.
- Use the word they use. Plumbers say "plumbing", lawyers say "attorney" or "law firm".
- `-site:yelp.com -site:yellowpages.com` strips aggregators so you get the businesses.
- Nothing returned? Drop the location first, then a provider. Too many quoted terms means no page contains all of them.
- `filetype:pdf` is underrated — association member lists and sponsor sheets leak contacts constantly.

## Edge cases

- **Google shows a CAPTCHA** — you're paging too fast. Wait, or use a smaller `&num=`.
- **Everything got dropped** — the parser discards rows with no email and no phone. Pass `--keep-empty` to see them.
- **Business names look wrong** — the parser guesses from the longest short text cell. On messy pages it guesses badly; the emails are still right.

## Cost
Zero.
