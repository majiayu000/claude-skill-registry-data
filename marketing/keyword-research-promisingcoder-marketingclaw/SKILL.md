---
name: keyword-research
description: "Finding and expanding keyword opportunities for free — mining Search Console queries for high-impression/low-position pages, expanding via Google Autocomplete, and snapshotting SERPs with web search; optional paid DataForSEO volume/difficulty data."
metadata: { "marketingclaw": { "emoji": "🗝️", "requires": { "bins": ["curl", "jq"] } } }
---

# Keyword Research Skill

A free-first keyword research playbook. No API key is required to use the core workflow — it
loads without any environment variables. An optional paid data section (DataForSEO) is documented
at the bottom for real search-volume/difficulty numbers, but it's intentionally not in this
skill's required env so the skill works out of the box.

## Step 1 — Mine existing opportunities from Search Console

The highest-signal keyword ideas are queries you already rank for but aren't capturing clicks on.
Requires the `gsc` skill configured (`GOOGLE_APPLICATION_CREDENTIALS`, `GSC_SITE_URL`):

```bash
TOKEN=$(node <path-to-gsc-skill>/scripts/google-sa-token.mjs)
SITE_URL_ENC=$(jq -rn --arg u "$GSC_SITE_URL" '$u | @uri')

curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/${SITE_URL_ENC}/searchAnalytics/query" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2026-05-01",
    "endDate": "2026-06-30",
    "dimensions": ["query", "page"],
    "rowLimit": 25000,
    "dataState": "final"
  }' | jq '[.rows[] | select(.impressions > 100 and .position > 10)] | sort_by(-.impressions) | .[] | {query: .keys[0], page: .keys[1], impressions, position, clicks}'
```

**The opportunity filter: `impressions > 100 and position > 10`** — Google is showing the page
for that query often enough to matter, but it's ranking on page 2+ (position > 10), so there's
real headroom without starting from zero. Sort by impressions descending and work the top of the
list first — those are the closest wins.

Also check queries with `position <= 10` but low `ctr` relative to their position (title/meta
description isn't earning the click it should — hand off to `seo-audit`).

## Step 2 — Expand with Google Autocomplete (keyless, free)

```bash
expand_query() {
  local seed="$1"
  curl -s "https://suggestqueries.google.com/complete/search?client=firefox&q=$(jq -rn --arg q "$seed" '$q | @uri')" | \
    jq -r '.[1][]'
}

expand_query "best project management software"
```

Autocomplete returns a JSON array shaped `["<echoed query>", ["suggestion 1", "suggestion 2", ...]]`
— the `jq -r '.[1][]'` above pulls just the suggestion strings. No API key needed (this is the
same public endpoint browser address bars use).

Widen coverage with alphabet/question seeding — run `expand_query` for the base term plus each of
these variants to surface long-tail phrasing:

```bash
for letter in a b c d e f g h i j k l m n o p q r s t u v w x y z; do
  expand_query "best project management software $letter"
done

for prefix in "how to" "what is" "why" "best" "vs" "alternative to" "how much does" "when to"; do
  expand_query "$prefix project management software"
done
```

Dedupe and skim, don't dump the raw list into a report — group similar phrasings, drop anything
off-topic or clearly not commercial/informational intent-relevant.

## Step 3 — SERP snapshot for shortlisted terms

For each keyword that survives steps 1-2, use the project's web-search tool (not this skill's own
API — none is defined here) to see the current SERP: who ranks, what content format wins (listicle
vs. product page vs. tool), and whether there's a featured snippet/People Also Ask worth targeting.
This tells you what to build, not just what to target.

## Step 4 — Prioritize

Rank shortlisted keywords by a rough formula: **(estimated relevance to the business) × (estimated
traffic potential, using GSC impressions as a proxy where available, or SERP result count/ad
density as a weak signal otherwise) ÷ (estimated difficulty, using how entrenched/authoritative
current top-10 results look)**. Without paid volume/difficulty data this is directional, not
precise — say so when reporting rather than presenting fabricated confidence.

## Optional: DataForSEO for real volume/difficulty

If the team has a DataForSEO account, set (not required for the skill to load):

```bash
export DATAFORSEO_LOGIN="your-login"
export DATAFORSEO_PASSWORD="your-password"
```

```bash
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live" \
  -u "${DATAFORSEO_LOGIN}:${DATAFORSEO_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["best project management software", "project management software free"], "location_code": 2840, "language_code": "en"}]' | \
  jq '.tasks[0].result[] | {keyword, search_volume, competition, cpc}'
```

`location_code` 2840 is the United States; see DataForSEO's locations reference for others.
**Verify on first use**: confirm current endpoint path and response shape against
`https://docs.dataforseo.com/` — DataForSEO's API surface changes across their product lines
(Labs vs. Keywords Data vs. SERP) and this is only one of several equivalent endpoints.

## Notes

- No environment variables are required for steps 1-3's autocomplete/SERP-snapshot path; step 1
  needs the `gsc` skill's env if you want the Search-Console-mining step.
- Respect Google's autocomplete endpoint as a lightweight, unofficial public API — don't hammer
  it in tight loops; a few requests per second is plenty and avoids getting rate-limited.
- Hand shortlisted keywords + target page to `blog-git` (new content) or `seo-audit` (existing
  page needs to actually earn the ranking it's getting impressions for).
