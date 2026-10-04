---
name: yc-jobs-scraper
description: Scrape daily job listings from YCombinator's Workatastartup platform without duplicates. Use this skill when asked to scrape YC jobs, update the YC companies list, or retrieve the latest startup jobs. It handles authentication, extracts company slugs via Inertia.js JSON payloads, falls back to public YC job pages when necessary, and maintains a local SQLite database to track historical jobs and prevent duplicates.
---

# YC Jobs Scraper

This skill provides a robust architecture for scraping jobs from YCombinator and `workatastartup.com`. It is designed to run automatically, bypass login bottlenecks, and maintain state to never scrape duplicate jobs.

## Architecture

The scraper uses a hybrid approach to maximize reliability and minimize bot detection:

1. **Authentication:** `scripts/auth.js` uses Playwright to let a human log in once and saves the session to `scripts/state.json`.
2. **Database:** `scripts/db.js` uses `better-sqlite3` to manage `scripts/jobs.db`. It tracks every `company_slug` and `job_id` ever seen.
3. **Primary Extraction:** `scripts/scraper.js` loads `state.json`, visits YC query URLs, and extracts company slugs from the hidden Inertia.js `data-page` JSON payload.
4. **Job Extraction (JSON):** It then visits the authenticated company pages (`/companies/[slug]`) to extract jobs from the backend JSON payload to ensure we get the real `job_id` for accurate deduplication.
5. **Job Extraction (Fallback):** If the JSON extraction fails, it falls back to parsing public HTML job cards from `ycombinator.com/companies/[slug]/jobs`.

## Workflows

### 1. First-Time Setup
If this is the first time running the scraper in an environment, or if `node_modules` is missing:
```bash
cd @path/scripts
npm install
npx playwright install
```

### 2. Authentication (Manual Step)
If `scripts/state.json` is missing or expired, the scraper will fail. You must instruct the human user to run the authentication script manually:
```bash
cd @path/scripts
node auth.js
```
Tell the user a browser will open, and they must log in. Playwright will automatically save the cookies/tokens to `state.json`.

### 3. Running the Daily Scraper
To scrape for new companies and jobs:
```bash
cd @path/scripts
node scraper.js
```
This script will output exactly how many new companies and new jobs were found. Because of `jobs.db`, running it multiple times consecutively will result in `0 new jobs found`.

### 4. Querying the Database
If you need to analyze the scraped data or view the companies/jobs, you can query `scripts/jobs.db` directly using `better-sqlite3`.

**Example: Count Companies**
```bash
cd @path/scripts
node -e "const db = require('better-sqlite3')('jobs.db'); console.log('Companies:', db.prepare('SELECT COUNT(*) as count FROM companies').get().count);"
```

**Example: View Recent Jobs**
```bash
cd @path/scripts
node -e "const db = require('better-sqlite3')('jobs.db'); const jobs = db.prepare('SELECT title, company_slug, location FROM jobs ORDER BY created_at DESC LIMIT 5').all(); console.table(jobs);"
```