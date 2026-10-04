---
name: 02-apify-maps-discover
description: >-
  Find local-business (SMB) prospects via Google Maps using the Apify Compass
  actor. Use for Zevenue Step-2 Discovery (Vertical) when the ICP is
  Maps-addressable - laundromats, salons, HVAC, yoga studios, gyms, clinics -
  and you need a normalized list of name, domain, address, phone, rating, and
  review count ready for enrichment. Estimates cost and prompts before any run
  over $10. Requires APIFY_API_TOKEN.
---

# Apify Maps Discovery

Turn a vertical + a place into a clean prospect list, scraped from Google Maps
via the maintained **Apify Compass** actor (`compass~crawler-google-places`). We
wrap the best existing actor rather than build our own scraper - Compass already
handles proxies, anti-bot, and layout drift, and offers built-in email/contact
enrichment. Output is the normalized Zevenue ProspectRecord schema (JSON + CSV).

## Process
1. **Confirm inputs.** Need `search_term` (the vertical) and `geo` (the area).
   Defaults: `max_results=200`, `min_rating=4.0`. Ask only if missing/ambiguous.
2. **Estimate cost and gate.** The skill prints an estimate before calling the
   API. If it exceeds **$10**, it requires explicit confirmation (`--yes` or an
   interactive y/N). Never bypass this silently.
3. **Run the actor.** Calls the Compass sync endpoint with the built input
   (`searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch`,
   `placeMinimumStars`). Add enrichment only when asked (see flags).
4. **Normalize.** Each raw place is mapped to the shared 15-field ProspectRecord
   so it's comparable with the Outscraper / Google Places skills.
5. **Write the run folder.** Writes `runs/<run-id>/` per `headless-gtm-shared/CONVENTIONS.md`:
   `records.jsonl` (the shared chain format 03+ consume - `company`, `domain`,
   `person`, plus the firmographic fields), `tracker.json`, `meta.json` (count +
   spend estimate), `prospects.json` (all 15 ProspectRecord fields), and
   `records.csv` for humans. Report the row count and path; downstream skills
   read `runs/<run-id>/records.jsonl` (e.g. 05's `collect --records`).

## Usage
```bash
# install deps once (use a venv - system Python is externally-managed)
pip install -r ../headless-gtm-shared/requirements.txt
export APIFY_API_TOKEN=...        # console.apify.com → Settings → Integrations

python discover.py \
  --search-term "yoga studios" \
  --geo "California" \
  --max-results 200 \
  --min-rating 4.0 \
  [--include-emails] [--with-review-dates] \
  [--out DIR] [--estimate-only] [--yes]
```

### Inputs
| Flag | Maps to | Default |
|---|---|---|
| `--search-term` | actor `searchStringsArray` | required |
| `--geo` | actor `locationQuery` | required |
| `--max-results` | `maxCrawledPlacesPerSearch` | 200 |
| `--min-rating` | `placeMinimumStars` | 4.0 |
| `--include-emails` | `scrapeContacts` (+$2/1K) | off |
| `--with-review-dates` | `scrapePlaceDetailPage` (extra cost) | off |
| `--estimate-only` | print cost, no API call | - |
| `--yes` | skip the >$10 prompt | - |

### Output (normalized ProspectRecord)
`name, domain, website, phone, full_address, city, region, rating,
reviews_count, latitude, longitude, place_id, category, last_review_date,
source` → see [../headless-gtm-shared/schema.py](../headless-gtm-shared/schema.py).

## Cost
| Mode | Flags | Est. price |
|---|---|---|
| Discovery | (default) | ~$2.10 / 1K |
| Discovery + emails | `--include-emails` | ~$4.10 / 1K |
| Typical 2K-record run | either | **$4–8** |

`last_review_date` is **off by default** - it needs Compass's per-place detail
page (`--with-review-dates`), which adds cost and latency. The cheap default pull
leaves it blank. Edit the cost constants at the top of `discover.py` if your
account pricing differs from the doc's $2.10/1K figure.

## What good output looks like
- Every row has at least `name` + (`domain` or `phone`) - usable for outreach.
- `domain` is a bare host (no scheme/www) so it dedups cleanly downstream.
- Closed businesses are skipped (`skipClosedPlaces`), ratings ≥ `min_rating`.
- Row count is in the ballpark of what the geo realistically contains - a tiny
  count usually means the `geo` was too narrow or the term too specific.

## Scope boundaries (what this skill does NOT do)
- **Not** directory-only businesses with no Maps listing → use the extraction
  skill.
- **Not** tech-stack-defined ICPs (e.g. "stores on Shopify") → signal layer.
- **Not** qualitative web-observable ICPs → separate ICP discovery.
- **Not** email validation or company firmographics → downstream enrichment /
  validation skills.
- Outscraper is kept proprietary for client work; **Compass is the public/
  distributable Maps tool** chosen here. Google Places was rejected (60-result
  per-query cap + Enterprise-tier cost for contact fields).

## Reference
Deeper detail lives in the `reference/` folder - load the file you need:

- [reference/compass-actor.md](reference/compass-actor.md) - actor ID, sync &
  async endpoints, the full input schema (every field + type), raw output fields,
  and limits.
- [reference/output-schema.md](reference/output-schema.md) - the normalized
  15-field ProspectRecord, the raw→normalized field map, domain-extraction and
  dedup-key rules, and JSON/CSV samples.
- [reference/cost-model.md](reference/cost-model.md) - pricing per mode, how the
  $10 gate is computed, worked cost examples, and how to edit the constants.
- [reference/verticals-and-geo.md](reference/verticals-and-geo.md) - recommended
  `search_term` phrasings per Zevenue vertical, `geo` formatting, and how to size
  `max_results` / `min_rating`.
- [reference/examples.md](reference/examples.md) - copy-paste recipes for common
  jobs (quick test, full 2K list with emails, multi-city, estimate-only dry run).
- [reference/troubleshooting.md](reference/troubleshooting.md) - empty results,
  auth/token errors, timeouts, rate limits, the 300s sync cap, and field-name
  caveats.
