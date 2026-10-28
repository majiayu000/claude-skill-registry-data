---
name: finding-local-businesses
description: Scrape local businesses from Google Maps with addresses, phones, websites, emails, and decision-maker contacts. Use when the user wants local leads, businesses in a city, contractors/restaurants/salons/trades in an area, or asks for "Google Maps leads" or "System 2".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Finding Local Businesses (System 2)

## Goal
Turn "barbers in Tuscaloosa" into a spreadsheet of businesses with contact details — and, if asked, the named decision-makers inside them.

## When to use
- "Find me every roofer in Mobile Alabama"
- "I need local restaurants with emails"
- "Scrape Google Maps for HVAC companies"
- Anything the user calls System 2, local leads, or Google Maps

## The one thing to know

The actor got much better since the course was recorded. The video needed six steps to get emails: scrape Maps, loop over results, fetch each website, AI-extract the contacts, export a CSV, upload it to AnyMailFinder. That's now three flags on one command:

| Flag | What it adds |
|---|---|
| `--contacts` | Emails and social profiles pulled from each business website |
| `--leads N` | Up to N decision-makers per business: name, job title, email, phone, LinkedIn |
| `--verify-emails` | Checks each of those emails is real before you send |

Each one bills separately. Start without them.

## Process

### Step 1 — cheap test, no add-ons
```bash
python -X utf8 scripts/02_local_businesses/scrape_google_maps.py \
    --search "barbers in Tuscaloosa AL" --limit 5 --out-csv output/test.csv
```
About 2 cents. Read the CSV — right businesses? right city?

### Step 2 — the real run
```bash
python -X utf8 scripts/02_local_businesses/scrape_google_maps.py \
    --search "roofing contractors in Mobile AL" --limit 100 \
    --contacts --out-csv output/roofers.csv
```

### Step 3 — decision-makers, when the user needs a name to write to
```bash
python -X utf8 scripts/02_local_businesses/scrape_google_maps.py \
    --search "law firms in Birmingham AL" --limit 50 \
    --contacts --leads 2 --departments "C-Suite" --verify-emails \
    --out-csv output/lawyers.csv
```

### Full pipeline with AI summaries
When the user wants a 50-word summary and 5 facts per business (the video's flow):
```bash
python -X utf8 scripts/02_local_businesses/gmaps_lead_pipeline.py \
    --search "dentists in Miami FL" --limit 25 --out-csv output/dentists.csv
```
This adds `summary` and `fact_1..fact_5` columns. Google Sheets is opt-in via `--sheet-url`; without it you get CSV and no OAuth setup.

## Useful filters

- `--min-stars 4` — skip businesses with poor ratings
- `--skip-closed` — drop permanently closed places
- `--actor crawler` — richer data (reviews, hours) for more money; default `extractor` is what the course used and rates highest

## Edge cases

- **Search term matters more than anything.** "barbers in Tuscaloosa AL" beats "barbers" + `--location`. Put the city in the search string.
- **One location per run.** Two cities in one search returns mush. Loop instead.
- **~15% of business websites block scrapers** — `--contacts` will come back empty for those. Normal, not a bug.
- **Fewer results than `--limit`** — Google Maps genuinely has that many. Broaden the term or widen the area.
- **`--verify-emails` without `--leads`** does nothing; verification only applies to the decision-maker records.

## Cost
~$0.004–0.02 per place, plus each add-on. A 100-business run with contacts is usually under $1. See `docs/COSTS.md`.
