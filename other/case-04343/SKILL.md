---
name: amz-hot-keywords
description: "Scrape Amazon Brand Analytics (ABA) weekly hot keyword rankings from AMZ123 and return structured keyword trend data. Use when the user asks about Amazon keyword rankings, hot search terms, keyword trends, ABA data, or wants a CSV/JSON of popular Amazon search terms. Trigger phrases include: 'hot keywords', 'search term rank', 'keyword trend', 'Amazon keyword', 'ABA data', '热搜词', '关键词排名', '关键词趋势'."
version: "1.0.0"
---




### Cleanup Review

`python scripts/_reset_state.py` is an optional cleanup helper for the `Amazon Hot Keywords Skill` skill. It may recursively remove /tmp/skill_build/*, /tmp/skill_build/.cache. Show the exact paths first, explain whether they are skill-private temporary paths or user state, and run the cleanup only after the user confirms.

# Amazon Hot Keywords Skill

## Overview
This skill extracts weekly search‑term rankings from Amazon Brand Analytics via the public AMZ123 site. It returns a CSV (or JSON) containing the keyword, current week rank, last week rank, and trend (up/down/flat/new).

## Core Workflow
1. User provides a base keyword.
2. `scripts/amz_scraper.py` launches a headless Selenium Chrome session, navigates to AMZ123, searches the keyword, and scrapes up to 200 related terms.
3. The script calculates the trend by comparing the current rank with the previous week’s rank.
4. Results are saved to `amz123_hotwords_<keyword>_<timestamp>.csv` (or `.json`).
5. The file path is returned to the caller.

## Usage
```bash
# Basic usage – CSV output
python3 $(pwd)/scripts/amz_scraper.py --keyword "dog bed"

# Limit results to 100 entries and specify output folder
python3 $(pwd)/scripts/amz_scraper.py \
    --keyword "yoga mat" \
    --max-results 100 \
    --output-dir ./data
```
### Parameters
| Flag | Required | Description | Default |
|------|----------|-------------|---------|
| `--keyword` | Yes | Search term to seed the scrape | - |
| `--max-results` | No | Max number of keywords to collect (max 200) | 200 |
| `--output-dir` | No | Directory for the CSV/JSON file | current directory |
| `--format` | No | `csv` or `json` (default `csv`) |
| `--headless` | No | Run Chrome headlessly (`true`/`false`) | true |

## References
- See `references/workflow.md` for a step‑by‑step guide and troubleshooting tips.
- See `references/output.md` for the exact CSV column order and JSON schema.

## Scripts
The scraper implementation lives in `scripts/amz_scraper.py`.

---


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
