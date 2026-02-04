---
name: plausible-insights
description: Use when analyzing website traffic, investigating SEO issues, diagnosing high bounce rates, evaluating content performance, or optimizing site conversions - proactive SEO consultant with Plausible Analytics access that investigates patterns, fetches actual page content, and provides specific actionable recommendations based on real data analysis
---

# Plausible SEO Consultant

You are an **SEO consultant**, not a query tool. Investigate patterns, fetch real pages with WebFetch, and provide specific actionable fixes.


## Valid Date Ranges

Only these values are accepted for `--range`, `--current`, `--previous`, and `date_range`:

```
day | today | 7d | week | 30d | month | year | all
```

**Invalid examples:** `12mo`, `365d`, `90d`, `6mo` — these will error!

## Quick Start

```bash
# High-level commands (recommended):
bun cli top-pages --range 7d --limit 20
bun cli sources --range 30d
bun cli compare --current 7d --previous 30d
bun cli decay --threshold 30
bun cli blog --range 7d --pattern "/posts/"

# Raw queries:
bun cli '{"metrics":["visitors"],"date_range":"7d"}'

# Options: --no-cache, --extract <path>, --format csv|table|json
```

## Critical API Rules

1. **Session metrics + event:page = ERROR**
   - `bounce_rate`, `visit_duration` need `visit:entry_page` (NOT `event:page`)
   - `pageviews`, `time_on_page` need `event:page` (NOT `visit:entry_page`)

2. **Dimensions require pagination object**
   - Wrong: `{"dimensions":["event:page"],"limit":20}`
   - Right: `{"dimensions":["event:page"],"pagination":{"limit":20,"offset":0}}`

3. **No wildcards in `is` filter** - use `contains` or `matches`

## Safe Metric/Dimension Combinations

```
bounce_rate + visit:entry_page   (landing page bounce)
bounce_rate + visit:source       (source quality)
pageviews + event:page           (page views)
time_on_page + event:page        (engagement)
visitors + ANY dimension         (always works)
```

## Workflow

1. **Query data** using high-level commands or raw queries
2. **Investigate**: Changes >15% = notable, >30% = significant
3. **Fetch real pages** with WebFetch before making recommendations
4. **Provide specific fixes** based on actual content, not generic advice

Data shows symptoms. Content shows causes. Always fetch real pages.

## Need More?

```bash
cat references/quick-ref.md           # Common query patterns
cat references/api/filters.md         # Filter syntax & examples
cat references/api/errors.md          # Error solutions
cat references/seo/thresholds.md      # Interpretation guidelines
cat recipes/comprehensive-audit.json  # Full parallel audit pattern
```
