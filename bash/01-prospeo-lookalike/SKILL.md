---
name: 01-prospeo-lookalike
description: >
  Seed-based B2B company discovery via the Prospeo company-lookalike API. Use when the
  user has example companies and wants more like them - "find companies similar to X",
  "companies like Stripe and HubSpot", "lookalikes of these domains", "we closed these
  20 logos, find more", "expand this seed list", or hands over closed-won accounts / a
  competitor / a customer list and wants similar firmographic matches. Turns seed domains
  or an ICP description into a ranked list of similar companies, and can also hand a
  pattern-built ICP to prospeo-discover for a broader search.
---

# Prospeo Lookalike - Seed-Based Company Discovery

Turn seed companies (domains, an ICP description, or "similar to X") into similar companies via
Prospeo's `company_lookalike` filter (33-filter, 30M+ company database). Two ways to finish:

- **Mode 1 - Lookalike list** (headline): return the actual similar companies, ranked by similarity
  tier. The lookalike filter runs *alone* - no ICP stacking - so you get a full list, not single digits.
- **Mode 2 - Seed → ICP handoff**: analyze the 25 closest matches for patterns, build an ICP, and hand
  it to [`01-prospeo-discover`](../01-prospeo-discover/SKILL.md) for a broad firmographic search.

Discovery (skill 01) deliberately treats lookalike as a throwaway pattern-finder and drops it before its
real search. This skill is the opposite - here the lookalike matches are a first-class deliverable.

## Your job

1. Collect the seed(s) - domains, named companies, or an ICP paragraph - and pick the mode.
2. Resolve seeds to what the API needs (domain string, company IDs, or `icp_text`).
3. Run the lookalike search, present the ranked matches with the similarity tier.
4. Offer the next step: export the list (Mode 1) or build an ICP and route to discovery (Mode 2).

Credits are real money: each search page costs 1 credit; account and suggestion calls are free. Guard
spend, especially on export.

## Setup

Auth reads from environment variables. Nothing is hardcoded.

- `PROSPEO_API_KEY` - required for every Prospeo call.
- Google Sheets export reads OAuth credentials from `GOOGLE_TOKEN_PATH` (default `~/.google/token.json`).
  Only needed when exporting.

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
- `POST /search-company` - the search, incl. lookalike (1 credit per page)
- `POST /search-suggestions` - resolve locations, technologies, industries, other open-ended values (free)

The one body-shape rule that breaks searches when you get it wrong: filters go inside a `"filters": {}`
wrapper, and `"page"` is a sibling of `"filters"`, not inside it.

```bash
curl -s -X POST "https://api.prospeo.io/search-company" \
  -H "X-KEY: $PROSPEO_API_KEY" -H "Content-Type: application/json" \
  -d '{"filters": {"company_lookalike": { ... }}, "page": 1}'
```

Full curl formats, the search-suggestions key table, and the formats to avoid live in
`references/api-curl.md` - read it before resolving values for the first time in a session.

## Step 0 - Plan and enum check (internal, run once)

Do this silently before prompting the user. Don't narrate it or show step numbers.

**Plan and credits.** Call `GET /account-information` and read `current_plan` and `remaining_credits`
from the `response` object. Store them.

**Lookalike needs Starter or higher.** `company_lookalike` is filter #22, gated to **Starter+** (see
`references/plan-filter-map.md`). On the **Free** plan it is unavailable - if the account is Free, say so
up front and stop, rather than assembling a search that will fail:

> Lookalike needs a Starter plan or higher; this account is on Free. I can still build a list from an ICP
> description with `01-prospeo-discover` instead.

If `remaining_credits` is under 10, tell the user their balance and that each page costs 1 credit before
spending anything.

**Enum cache.** Read `references/prospeo-enums.json` and check `last_updated`. If it's missing or older
than 21 days, refresh it with `references/enum-refresh.md`; otherwise use the cached values. You only need
enums when the user layers ICP constraints (industry, size, etc.) onto the lookalike or when you build the
Mode 2 ICP. Technologies (4,946) and locations resolve at runtime via `search-suggestions`.

Then present a clean prompt and wait for input.

```
Prospeo Lookalike ready.
Plan: {plan} | Credits: {credits}

Give me the seed companies you want to find matches for - domains, names, or a short
description of the ideal company.
```

## Step 1 - Collect seeds and resolve them

The lookalike filter takes exactly ONE mode per call. Pick by what the user gave you:

| What the user gave | Mode | How to build it |
|---|---|---|
| One domain ("similar to hubspot.com") | **domain** | `{"domain": "hubspot.com"}` - no lookup needed |
| Multiple domains / named companies | **company_oids** | Resolve each to a Prospeo company ID first, then `{"company_oids": [...]}` |
| A paragraph describing the ideal company | **icp_text** | `{"icp_text": "..."}` (max 5,000 chars) - no lookup needed |

**Resolving multiple domains to company IDs** (1 credit each): search `company.websites.include` for each
domain, read the company ID off the result, collect the IDs. Full detail and the exact response field to
read live in `references/lookalike-modes.md`. A single domain skips this - use `domain` mode directly.

**Similarity tier** controls how close the matches are:

- `"T1"` - most similar (tightest, fewest results)
- `"T2"` - balanced (a good default for a usable list)
- `"T3"` - broadest (default if unset)

**`match_all`** only applies to multi-seed (`company_oids`) searches: `false` (default) = union of each
seed's lookalikes; `true` = intersection (companies similar to *all* seeds at once - much narrower).

Confirm the assembled lookalike filter with the user before spending a credit:

> Seeds: torc.ai, field.ai (resolved to 2 company IDs)
> Tier: T2 (balanced) | match_all: false (union)
> This runs the lookalike search - 1 credit for page 1. Go?

Worked plain-English → lookalike JSON examples are in `references/mapping-examples.md`.

## Step 2 - Pick the mode with the user

Once seeds are ready, ask which outcome they want (or infer it from how they framed the request):

- **"Just give me the similar companies"** / a competitor or customer list to expand → **Mode 1**.
- **"Use these to figure out who to target"** / closed-won logos → **Mode 2** (the pattern → ICP handoff).

If unsure, default to Mode 1 (the direct answer to "find similar companies") and offer Mode 2 as a
follow-up. The two aren't exclusive - you can show the Mode 1 list *and* offer to distil an ICP from it.

## Step 3a - Mode 1: lookalike list

Run `POST /search-company` with `company_lookalike` as the **only** filter (optionally plus a light
location or size constraint the user explicitly asked for - but never a full ICP stack, which collapses
the count). Fetch page 1, present:

```
Found {total_count} companies similar to {seeds} (tier {tier}).

Preview (top 25, most similar first):
| # | Company | Domain | Industry | Employees | Location | Revenue | Funding |
|---|---------|--------|----------|-----------|----------|---------|---------|
| 1 | ...     | ...    | ...      | ...       | ...      | ...     | ...     |

Credits used: 1 | Full export: {total_pages} credits | Balance: {credits - 1}

Next steps:
1. Export the full list
2. Tighten the tier (T1 for closer matches) or add a location/size constraint
3. Build an ICP from these patterns instead (Mode 2)
```

If `total_count` is over 2,000, suggest tightening the tier before a full export. If it's under 10, suggest
loosening the tier (`T3`) or dropping any extra constraint you stacked on.

## Step 3b - Mode 2: seed → ICP handoff

Use the lookalike matches to *build an ICP*, then route to discovery for the broad search.

1. Fetch page 1 only (25 results, 1 credit). The response already carries industry, headcount, location,
   funding, revenue, and keywords - no export needed to analyze.
2. Read the 25 for patterns across the mandatory ICP filters: dominant industries, typical size, location
   concentration, funding stages, common keywords.
3. Present the pattern-built ICP and let the user confirm or adjust.
4. Run the confirmed ICP as a firmographic search - **without** any `company_lookalike` filter (stacking it
   with a full ICP collapses the count). It's the same `POST /search-company` call, just with ICP filters;
   assemble it from `references/filters-full.md` and export with the script below (it accepts a plain ICP
   filter set too - see its note). Say why once:

   > These 25 are the closest matches; the ICP I pulled from them (industry, size, geo, funding) will give
   > you a much fuller list than the lookalike filter alone.

5. **Watch for broad-industry overshoot - re-inject the keyword signal.** When the seeds live in a niche
   (robotics, autonomy, biotech) but classify under a huge parent industry like `Software Development`, an
   ICP of industry + size + geo alone can balloon into six figures - the specificity that made the
   lookalikes good lived in the *keywords*, and a plain firmographic ICP drops it. Before handing off,
   sanity-check the count on page 1: if it's implausibly large (tens of thousands), add the 1-2 dominant
   recurring keywords from step 2 as a `company_keywords` constraint, or drop the broad parent industry and
   keep only the niche one. Real example: robotics seeds → `Software Development + Robotics Engineering` in
   US/Canada returned ~138K; `Robotics Engineering` alone cut it to ~980, and `+ keyword "robotics"` landed
   ~1,491 - both campaign-usable. A count in the low thousands is the target; low six figures means the
   keyword signal got lost.

> Related skill (optional): if [`01-prospeo-discover`](../01-prospeo-discover/SKILL.md) is installed, you can
> hand it the confirmed ICP instead of running the search here - it adds mandatory-filter defaults and
> optional-filter recommendations. An option, not a prerequisite; this skill runs the ICP on its own.

## Step 4 - Export (only when asked)

Export uses the Python script, which paginates the search and writes the chain run folder. Don't paginate
the API by hand for exports.

**Script**: `scripts/sheets_export.py` · **Deps**: `pip install -r ../headless-gtm-shared/requirements.txt` (only the
opt-in Sheets export needs the `gspread`/`google-auth` extras in that file)

```bash
# Preview count without spending export credits
python3 scripts/sheets_export.py --filters lookalike_filters.json --dry-run

# Standard chain export - writes runs/<run-id>/ (records.jsonl + tracker + meta)
python3 scripts/sheets_export.py --filters lookalike_filters.json

# Also export to Google Sheets (new spreadsheet, or an existing one)
python3 scripts/sheets_export.py --filters lookalike_filters.json --sheets
python3 scripts/sheets_export.py --filters lookalike_filters.json --spreadsheet-id SHEET_ID --tab-name "lookalikes"

# Cap pages for very large result sets
python3 scripts/sheets_export.py --filters lookalike_filters.json --max-pages 20
```

Save the current filter JSON (the `company_lookalike` block wrapped as `{"company_lookalike": {...}}`, plus
any extra constraint) to the path you pass in `--filters`, then run the script. The Google Sheets export is
**opt-in** (`--sheets`, or implied by `--spreadsheet-id`/`--tab-name`); it writes a **Results** tab (company
data incl. similarity tier) and a **Search Info** tab (the seeds + tier). The chain never depends on the Sheet.

**Before exporting**, show the cost and confirm:

> Full export: {total_pages} pages = {total_pages} credits. Your balance: {credits}. Proceed?

The script also confirms before fetching more than 10 pages, and `--dry-run` previews the count for free.

## Shared output (runs/<run-id>/)

Every export writes a run folder under `./runs/` in the working directory, per `headless-gtm-shared/CONVENTIONS.md`: `records.jsonl`
(the file downstream skills consume), `tracker.json`, and `meta.json` (filters, seed provenance, credits).
Records carry the stage-01 fields plus `lookalike_tier`, and the seed provenance in `filters_matched` so
downstream skills know these came from a lookalike run:

```jsonl
{"company": "Aurora Innovation", "domain": "aurora.tech", "person": null, "industry": "Autonomous Vehicles", "size": "201-500", "location": "Pittsburgh, Pennsylvania, United States", "funding": {"stage": "Series C", "total": "820M", "last_date": "2025-06-14"}, "revenue": "", "keywords": ["autonomy", "trucking"], "lookalike_tier": "T2", "filters_matched": ["Lookalike: 2 seed company IDs | tier T2 | union"]}
```

## Where this sits in the chain

- **Step 01 (discovery layer).** Sibling of [`01-prospeo-discover`](../01-prospeo-discover/SKILL.md)
  (ICP-filter build) and `02-apify-maps-discover` (local SMB). Use this one when the user starts from
  *example companies*; use discover when they start from *filters*.
- **Mode 2 output feeds `01-prospeo-discover`**; Mode 1 output feeds the rest of the chain
  (04 signals → 05 signal-builder → 06 resolution) via `records.jsonl`.
- The router ([`00-gtm-router`](../00-gtm-router/SKILL.md)) picks this skill when the ICP is defined by
  seed logos rather than firmographic filters.

## References

- `references/lookalike-modes.md` - the three lookalike modes in detail, oid resolution, tiers, pattern analysis
- `references/mapping-examples.md` - plain-English → lookalike filter JSON examples
- `references/api-curl.md` - exact curl formats, the full search-suggestions key table, formats to avoid
- `references/filters-full.md` - all 33 filters (for any ICP constraint you layer on or build in Mode 2)
- `references/plan-filter-map.md` - which filters each plan supports (lookalike = Starter+)
- `references/enum-refresh.md` - how to refresh the enum cache
- `references/prospeo-enums.json` - cached valid enum values
