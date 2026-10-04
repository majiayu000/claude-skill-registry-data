---
name: 01-prospeo-discover
description: >
  B2B company discovery and list building via the Prospeo search API. Use when the
  user wants to find companies from an ICP, build a prospect or TAM list, search by
  ICP, or size a market - e.g. "build a list of B2B SaaS in the US", "how many companies
  match this ICP", "TAM sizing", "company search", or any mix of industry + location +
  headcount + funding filters. Handles seed-based "similar to X" requests too by building an
  ICP from the seeds; 01-prospeo-lookalike is the deeper specialist when you want the matches
  themselves returned and ranked.
---

# Prospeo Discover - B2B Company List Builder

Turn a plain-English ICP into Prospeo filter JSON, run a company search against Prospeo's
30M+ company database (33 filters), present the result, and export to Google Sheets on request.

## Your job

1. Work out what the user has given you and what's still missing.
2. Map their language to exact Prospeo filter values. Resolve anything you're unsure of via the API rather than inventing enum values.
3. Cover the mandatory filters, using the smart defaults below for anything they skip.
4. Recommend a few high-impact optional filters, then stop.
5. Run the search, show the count plus a 25-row preview, and export only when asked.

Credits are real money: each search page costs 1 credit; account and suggestion calls are free. Guard spend, especially on export.

## Setup

Auth reads from environment variables. Nothing is hardcoded.

- `PROSPEO_API_KEY` - required for every Prospeo call.
- Google Sheets export reads OAuth credentials from `GOOGLE_TOKEN_PATH` (default `~/.google/token.json`). Only needed when exporting.

The curl examples use `$PROSPEO_API_KEY` as the key. **A `.env` file is not
visible to curl** - load it into the shell first, in the same command as the
call, or curl sends an empty `X-KEY` header and the API returns a confusing
auth error instead of a missing-key one:

```bash
set -a; [ -f .env ] && . ./.env; set +a
curl -s -H "X-KEY: $PROSPEO_API_KEY" https://api.prospeo.io/account-information
```

Check `$PROSPEO_API_KEY` is non-empty before the first paid call. The Python
scripts under `scripts/` read `.env` themselves and need no such prelude.

## API basics

```
Base URL: https://api.prospeo.io
Auth header: X-KEY: $PROSPEO_API_KEY
Content-Type: application/json
```

Three endpoints:

- `GET /account-information` - plan and credit balance (free)
- `POST /search-company` - the search (1 credit per page)
- `POST /search-suggestions` - resolve locations, technologies, industries, and other open-ended values (free)

The one body-shape rule that breaks searches when you get it wrong: filters go inside a `"filters": {}` wrapper, and `"page"` is a sibling of `"filters"`, not inside it.

```bash
curl -s -X POST "https://api.prospeo.io/search-company" \
  -H "X-KEY: $PROSPEO_API_KEY" -H "Content-Type: application/json" \
  -d '{"filters": { ...filter JSON... }, "page": 1}'
```

`search-suggestions` takes exactly one search key per request (min 2 chars) and is how you resolve any value you are not certain of. The full table of search keys and response keys, the worked curl examples, and the wrong formats to avoid live in `references/api-curl.md` - read it before resolving values for the first time in a session.

## Step 0 - Plan and enum check (internal, run once)

Do this silently before prompting the user. Don't narrate it or show step numbers.

**Plan and credits.** Call `GET /account-information` and read `current_plan` and `remaining_credits` from the `response` object (plus the renewal date if the response carries one). Store them. If `remaining_credits` is under 10, tell the user their balance and that each page costs 1 credit before spending anything.

Gate filters by plan. Only offer what the plan supports, and don't ask about filters it lacks. Full mapping in `references/plan-filter-map.md`:

- **Free**: 18 filters (no revenue, funding, technology, lookalike, or job postings)
- **Starter**: adds revenue, funding, technology, lookalike, job postings
- **Growth**: adds ICP, integrations, awards, key customers, headcount-by-location
- **Pro**: all 33 (adds exec changes, website traffic/search, SEO keywords)

**Enum cache.** Read `references/prospeo-enums.json` and check `last_updated`. If it's missing or older than 21 days, refresh it with `references/enum-refresh.md`; otherwise use the cached values. The cache holds valid values for industries (256), subtypes, funding stages, employee and revenue ranges, departments, and more. Technologies (4,946) and locations are too large to cache - resolve those at runtime via `search-suggestions`.

If the invoking request already describes the ICP - which is the common case - go straight to mapping it; don't re-ask for what you were just told. Only when you have nothing to work from, ask what companies they're looking for, mentioning the plan and credit balance. Don't show examples or sample company names.

## Step 1 - Read the input, pick the approach

Sort what the user gave you into three buckets:

- **ICP filters** - industry, size, location, funding, revenue, keywords, company type
- **Seed signals** - seed domains, "similar to X", named companies to match
- **Vague terms** that need mapping - "tech", "healthcare", "fintech"

That tells you how to proceed. You don't need to announce a "type" to the user, just route:

| What they gave | Approach |
|---|---|
| A full ICP (4-5 mandatory filters covered) | Map it to filter JSON and confirm |
| A partial or vague ICP | Guide them: interpret vague terms against the enum cache, then ask for missing mandatory filters one at a time with smart defaults |
| Seed domains or "similar to" | Build an ICP from the seed pattern (see below), then search |

A user can hand you a partial ICP *and* a seed domain - build the ICP from the seeds (below), merge it with
the filters they already gave, and run the search.

### Mandatory filters and smart defaults

A usable list needs these covered. Fill anything the user skips with the default, and tell them what you defaulted to:

1. **Location** - no safe default, always ask.
2. **Company size** - default `["11-20","21-50","51-100","101-200","201-500"]`.
3. **Industry / keywords / subtype** - at least one definition of the company.
4. **Status** - default `"Private"`.
5. **Revenue** (Starter+ only) - default by size: 11-50 employees → `"1M"`-`"10M"`, 51-200 → `"5M"`-`"50M"`, 201-500 → `"10M"`-`"100M"`.

On Free, revenue isn't available, so only the first three are mandatory.

For vague terms, read the enum cache, show the matching industries, subtypes, and attributes grouped by filter type, and let the user pick rather than guessing for them. `references/mapping-examples.md` has 20+ worked plain-English → filter JSON mappings - use it instead of inventing mappings.

### Seed domains → build an ICP from the pattern

When the user gives seed domains ("similar to X", "like these logos", a closed-won list), use them to *find
an ICP*, not as a search filter - stacking `company_lookalike` with a full ICP collapses results to single
digits.

1. For multiple domains, resolve them to Prospeo company IDs first (search `company.websites.include`,
   1 credit), then run `company_lookalike` with `company_oids`, `match_all: false`, `minimum_tier: "T2"`.
   A single domain can use `{"domain": "..."}` directly.
2. Fetch page 1 only (25 results, 1 credit) - it already carries industry, headcount, location, funding,
   revenue, and keywords, so no export is needed to analyze.
3. Read the 25 for patterns across the mandatory filters: dominant industries, typical size, location
   concentration, funding stages, common keywords.
4. Present the pattern-built ICP, let the user confirm or adjust, merge with anything they gave, and run the
   final search **without** `company_lookalike` - make sure the user understands the seeds found the pattern
   rather than acting as a filter. If they insist on keeping the lookalike filter, allow it and restate the
   trade-off.

> Related skill (optional): if [`01-prospeo-lookalike`](../01-prospeo-lookalike/SKILL.md) is installed, it's
> the specialist for seed work - it can return the similar companies as the deliverable (not just an ICP)
> and export them ranked by similarity. Reach for it when the user wants the *matches themselves*; this
> skill handles seed → ICP on its own without it.

## Step 2 - Recommend optional filters, then stop

Once the mandatory filters are covered, recommend a few optional filters before running. The skill has 33 filters - use the ones that fit, don't stop at the mandatory five and don't dump all 33.

Draw recommendations from whatever context you have:

- **Seed-pattern data** - if you built the ICP from seed-domain lookalikes (above), reuse the patterns you saw in the 25 matches (funding stages, common tech, founding years, recurring keywords).
- **The user's own language** - "funded"/"raised"/"VC-backed" → funding filters; named tools → `company_technology`; "growing"/"scaling" → headcount growth; "hiring" → job postings; "new companies" → founded year.
- **What the industry implies** - SaaS → `has_api`, `uses_ai`, subscription model; compliance-heavy (healthcare, fintech) → SOC 2, GDPR, HIPAA; hardware → physical offices, specific NAICS.
- **Plan capabilities** - only premium filters the plan supports.

Present 3-5 specific, actionable recommendations with real values, each tied to why it fits their search. "Series A-C funding in the last 12 months" beats "you could add a funding filter."

**Example (after an `01-prospeo-lookalike` Mode 2 handoff on AV/robotics seeds):**

> Optional filters to sharpen your list:
> 1. **Funding** - 40% of the similar companies had no funding data. Filter to funded only? Series A-D fits the AV space.
> 2. **Technology** - common here: AWS, Python, TensorFlow. Target a specific stack?
> 3. **Headcount growth** - 20%+ over 12 months to catch the scaling ones.
> 4. **Founded year** - most were 2010-2020; exclude legacy players?
> 5. **Attributes** - `uses_ai = true` to keep it genuinely AI-focused.
>
> Pick any, or skip to run the search.

Rules: be specific, explain why, reuse anything you discovered, cap at 5, don't recommend a filter the user already set, and if they say "skip" or "just run it" go straight to the search without pushing.

## Step 3 - Search and present

Run `POST /search-company` with the assembled filters, `page: 1`. Present:

```
Found {total_count} companies matching your filters.

Filters applied:
- Location: {locations}
- Industry: {industries}
- Size: {headcount_ranges}
- Status: {status}
- Revenue: {revenue_range}
{any additional filters}

Preview (top 25):
| # | Company | Domain | Industry | Employees | Location | Revenue | Funding |
|---|---------|--------|----------|-----------|----------|---------|---------|
| 1 | ...     | ...    | ...      | ...       | ...      | ...     | ...     |

Credits used: 1 | Full export: {total_pages} credits | Balance: {credits - 1}

Next steps:
1. Export full list
2. Narrow down
3. Adjust filters
```

If `total_count` is over 2,000, suggest narrowing before a full export. If it's under 10, suggest loosening - a broader headcount range or more industries.

## Step 4 - Export (only when asked)

Export uses the Python script, which paginates the search and writes the chain run folder. Don't paginate the API by hand for exports.

**Script**: `scripts/sheets_export.py` · **Deps**: `pip install -r ../headless-gtm-shared/requirements.txt` (only the opt-in Sheets export needs the `gspread`/`google-auth` extras in that file)

```bash
# Preview count without spending export credits
python3 scripts/sheets_export.py --filters filters.json --dry-run

# Standard chain export - writes runs/<run-id>/ (records.jsonl + tracker + meta)
python3 scripts/sheets_export.py --filters filters.json --run-id 2026-07-26-saas-us

# Also export to Google Sheets (new spreadsheet, or an existing one)
python3 scripts/sheets_export.py --filters filters.json --sheets
python3 scripts/sheets_export.py --filters filters.json --spreadsheet-id SHEET_ID --tab-name "my-search"

# Cap pages for very large result sets
python3 scripts/sheets_export.py --filters filters.json --max-pages 20
```

Save the current filter JSON to the path you pass in `--filters`, then run the script. The Google Sheets export is **opt-in** (`--sheets`, or implied by `--spreadsheet-id`/`--tab-name`); it writes a **Results** tab (15 columns) and a **Search Info** tab, and handles 3,000-5,000+ company exports that the MCP tools can't. The chain never depends on the Sheet.

**Before exporting**, show the cost and confirm:

> Full export: {total_pages} pages = {total_pages} credits. Your balance: {credits}. Proceed?

The script also asks for confirmation itself before fetching more than 10 pages, and `--dry-run` previews the count for free.

## Shared output (runs/<run-id>/)

Every export writes a run folder under `./runs/` in the working directory, per
`headless-gtm-shared/CONVENTIONS.md`: `records.jsonl` (the file downstream skills consume),
`tracker.json` (pages fetched / status), and `meta.json` (filters, counts,
credits). Each record carries the stage-01 fields:

```jsonl
{"company": "Acme Corp", "domain": "acme.com", "person": null, "industry": "Software Development", "size": "51-100", "location": "Austin, Texas, United States", "funding": {"stage": "Series A", "total": "12M", "last_date": "2025-11-02"}, "revenue": "$10M-$50M", "keywords": ["vertical saas", "field service"], "filters_matched": ["Industry: Software Development", "Headcount Range: 51-100, 101-200"]}
```

## References

- `references/api-curl.md` - exact curl formats, the full search-suggestions key table, formats to avoid
- `references/filters-full.md` - all 33 filters with accepted values and types
- `references/plan-filter-map.md` - which filters each plan supports
- `references/mapping-examples.md` - 20+ plain-English → filter JSON examples
- `references/enum-refresh.md` - how to refresh the enum cache
- `references/prospeo-enums.json` - cached valid enum values
