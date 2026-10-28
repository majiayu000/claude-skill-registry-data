---
name: discovering-live-events
description: Find local or niche live events, conferences, expos, forums, conventions, trade shows, association meetings, and networking rooms for a client, niche, city, suburb, state, or date range. Use when Codex needs to discover upcoming or historical event opportunities and create an outreach-ready event list.
---

# Discovering Live Events

## Workflow

1. Read `references/cost-controls.md` before any paid actor use.
2. Generate layered queries with `scripts/generate_event_queries.py`.
3. Prefer official pages, association calendars, Google SERP, and 10times before broad event marketplaces.
4. Save raw results under `data/` and normalized deliverables under `reports/`.
5. Normalize with `scripts/normalize_events.py`, dedupe with `scripts/dedupe_events.py`, then report with `scripts/generate_event_report.py`.

## Commands

```powershell
python scripts/generate_event_queries.py --niche "manufactured housing" --city "Las Vegas" --year 2026 --event-name "MHI 2026 Congress & Expo" --output reports/event-queries.csv
python scripts/discover_events_serp.py --niche "manufactured housing" --city "Las Vegas" --year 2026 --output data/event-serp-results.csv
python scripts/normalize_events.py --input data/event-serp-results.csv --output reports/events-normalized.csv
python scripts/dedupe_events.py --input reports/events-normalized.csv --output reports/events-deduped.csv
```

## Free-Tier Fallback (No Paid Apify Subscription)

Third-party Apify actors (`zen-studio/10times-events-scraper`, `santamaria-automations/eventbrite-scraper`, `scraperlink/google-search-results-serp-scraper`) return **403 on free-tier Apify accounts** — they require a paid subscription.

**Check account tier first:**
```powershell
curl -s "https://api.apify.com/v2/users/me?token=$env:APIFY_API_TOKEN" | python -c "import sys,json; d=json.load(sys.stdin)['data']; print(d.get('plan',{}).get('id'))"
```
If output is `FREE`, skip to the fallback below.

**Fallback: `scripts/run_apify_google_serp.py`**

Uses the official `apify/google-search-scraper` (available on free tier) to run targeted Google searches and extract organic results. Output is compatible with the full normalize → dedupe → rank pipeline.

```powershell
python -m scripts.run_apify_google_serp `
  --queries "BNI chapter Augusta GA 2026 networking meeting
Augusta Metro Chamber of Commerce events 2026
business networking events Augusta Georgia 2026
chamber of commerce mixer Augusta GA" `
  --output data/google-serp-results.csv `
  --results-per-page 10

python -m scripts.normalize_events --input data/google-serp-results.csv --output reports/events-normalized.csv
python -m scripts.dedupe_events --input reports/events-normalized.csv --output reports/events-deduped.csv
python -m scripts.rank_opportunities --input reports/events-deduped.csv --output reports/events-ranked.csv
python -m scripts.generate_event_report --events reports/events-ranked.csv --contacts "" --output reports/final-report.md
```

**Cost:** ~$0.02 per 5-query run. Quality: returns organic Google results including BNI chapter detail pages, chamber event registrations, and local networking pages not surfaced by Tavily.

## Guardrails

- Do not claim a complete attendee list when the source is gated, app-only, or LinkedIn-restricted.
- Use `confirmed`, `probable`, `weak`, `historical-reference`, or `needs-manual-verification` labels.
- Avoid broad AllEvents scans by default.
- Require explicit approval for paid runs above the configured cap.
## 2026 Outcome-First Update

If prior research is pasted as training context, read `references/outcome-first-opportunity-mapping.md` and use it to decide what matters. For known niches, read the relevant section of `references/niche-playbooks.md` before generating queries.

Add ranking after dedupe:

```powershell
python scripts/rank_opportunities.py --input reports/events-deduped.csv --output reports/events-ranked.csv
```

Capture online summits, webinars, magazines, newsletters, member directories, and official publications when they create access to the ICP.

## Association-Level Event Discovery

For local/regional/national association research, use `--association-levels` with any of: `local`, `regional`, `national`.

```powershell
python scripts/generate_event_queries.py --niche "family law" --city "Chicago" --state IL --year 2026 --association-levels local regional national --output reports/family-law-association-queries.csv
python scripts/discover_events_serp.py --niche "family law" --city "Chicago" --state IL --year 2026 --association-levels local regional national --output data/family-law-association-serp.csv
```

Use this mode to find bar sections, state associations, chapters, committees, CLEs, annual meetings, webinars, sponsor pages, exhibitor lists, and recurring lunches/breakfasts.
