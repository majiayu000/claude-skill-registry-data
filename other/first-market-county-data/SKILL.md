---
name: first-market-county-data
description: Research and locate first-to-market distress data sources for real estate wholesaling. Use when the user needs to find WHERE to pull county-level distress lists (probates, foreclosures, tax sales, liens, code violations, etc.) for a specific county or market. Returns office names, addresses, contact info, portal links, and access difficulty ratings. This skill focuses exclusively on Tier 1 data (first-to-market county data) within the Data Priority Pyramid.
---

# First-to-Market County Data Research

This skill helps real estate investors find the exact offices, portals, and processes to pull first-to-market distress data for any U.S. county.

## Data Priority Pyramid Context

This skill focuses on **Tier 1 - First-to-Market Data** within the Data Priority Pyramid:

| Pyramid Level | Data Source | Examples |
|---------------|-------------|----------|
| **Tier 1** | First-to-market county data (THIS SKILL) | Probate, foreclosure, tax sale pulled directly from county |
| Tier 2 | Nationwide aggregated data | DataSift, Propsumer, Batch |
| Tier 3 | AI-enhanced data | DataSift AI products |

Always prioritize Tier 1 data sources before moving to Tier 2 or Tier 3.

## What is First-to-Market Data?

First-to-market data means pulling distress records (probates, foreclosures, tax sales, etc.) the day or week they become available—before competitors. This data often requires:
- Physical county visits or special access
- Signed affidavits or license verification
- FOIA/public records requests
- Understanding of county-specific regulations

## When to Use This Skill

Use when the user asks to:
- Find where to pull distress data for a county
- Research county recorder/clerk offices
- Locate probate, foreclosure, tax sale, or lien sources
- Run the "deep research prompt" for county data
- Set up first-to-market data pulling processes

## Core Workflow

1. **Collect target location**: Get county name and state from user
2. **Select data types**: Determine which distress lists are needed — default to full Priority A + B + C coverage unless the user asks for a subset
3. **Sweep the cross-cutting sources** listed in the "Always-Check Cross-Cutting Sources" section below **before** falling back to data-type-specific prompts. Many counties have statewide aggregators, court journals, and alternate-auction pipelines that get missed if you only ask "where does the county file X?"
4. **Run research prompts**: Execute prompts from `references/research-prompts.md`
5. **Populate multi-URL portal fields**: For every data row, attempt to list the **primary portal + at least one cross-validation / backup URL** in the Portal URL field (newline-separated). A single URL is only acceptable when you've confirmed no alternate exists. See "Multi-URL Portal Convention" below.
6. **Cross-check against any prior XLSX** the user has for nearby counties in the same state. State-level infrastructure (judicial vs. non-judicial, tax lien vs. tax deed, statewide aggregator URL, court-journal pattern) repeats across counties — the previous report is a checklist. Missing entries that appear on a sibling-county report are a red flag.
7. **Compile results**: Build an input JSON following the schema in `scripts/build_spreadsheet.py`
8. **Deliver XLSX via the template**: Run `python scripts/build_spreadsheet.py input.json output.xlsx` — this is the **only** sanctioned output format. Do not invent alternate layouts. See `references/spreadsheet-template.md` for the full spec.

**The XLSX file is the deliverable.** Always write it to the project's `output/ftm_county_research/` folder (create the folder if it doesn't exist; never put it at the top level of `output/`). Link it prominently at the top of your chat response, and include a short summary + recommended action order underneath. Do not stop at a markdown-only answer or a CSV.

Output file naming: `{County}_County_First_Market_Data_Sources.xlsx` — overwrite prior versions rather than date-stamping, unless the user explicitly requests versioned snapshots.

## Always-Check Cross-Cutting Sources

Most counties have distress-data sources that don't map cleanly to a single data type. These get missed when you only run the per-data-type prompts. **Sweep for all of these before finalizing the report.** If a category doesn't apply to this state/county, note that explicitly in the Notes field of a related row rather than silently omitting it.

| Category | What to look for | Why it matters |
|---|---|---|
| **Statewide public-notice aggregator** | Search `{state} public notices` — most states have one (OH: `publicnoticesohio.com`, TN: `tnpublicnotice.com`, FL: `floridapublicnotices.com`, TX: `texaspressassociation.com/publicnotice`). | Same ASP.NET platform family across states → one scraper covers many counties. Often the cleanest legal source for foreclosure + probate notices. List as its own Priority A row. |
| **State-government notice site** | Search `{state}.gov public notice` (OH: `publicnotice.ohio.gov`). Separate from the newspaper aggregator. | State agency notices, hearings, forfeitures. Second URL on the statewide aggregator row. |
| **County court journal / legal newspaper** | Search `{county} legal news` or `{county} daily record`. Designated by statute as court journal of record (e.g., Akron Legal News, Daily Legal News Cleveland, Daily Report Atlanta, New York Law Journal). | Publishes foreclosures, probate, tax delinquent lists, sheriff sale notices. Often the free source for the annual certified delinquent list. List as its own Priority A row. |
| **Forfeited / excess-land sale** | Properties that fail multiple tax-sale rounds are forfeited to the state and auctioned by the Auditor/Commissioner. | Secondary deep-distress inventory, lower competition. Separate Priority A row — do not merge with tax sale. |
| **Land bank demolition pipeline** | Search `{county} land bank` — most rust-belt / post-industrial counties have one. | Publishes demolition target addresses **before** teardown — first-to-market signal on structurally-distressed vacants. Add as a URL on the Condemned row (and in Notes). |
| **Open Data portal (Socrata / ArcGIS REST)** | Search `data.{city}.gov` or `{city} open data`. Primary cities in data-friendly states (OH Cleveland, IL Chicago, NY NYC, CA SF) publish code violations / permits / lead certs via REST API. | Easiest possible scrape target — replaces FOIA for whichever data types the city publishes. List the specific dataset URL, not just the portal root. |
| **Recorder document-type searches** | Multiple lien types (mechanic's, federal tax, state tax, Medicaid, HOA, child support, judgment) are typically all filed at **the same county recorder portal**, filtered by document type. | The portal URL repeats across 5-8 rows — that's expected, and correct. Difference is the document-type filter in the Notes field. |
| **Fraud-alert / property-alert subscription** | Many recorders offer free property-fraud alerts by email when a deed is filed against a parcel. | Passive watchlist for target-parcel distress signals. Note as a capability in the recorder row. |
| **State attorney-general registries** | State AGs often hold secondary indexes (state tax liens, Medicaid recovery, charity registrations). | Use as a cross-validation URL on the relevant rows, not primary. |
| **RealAuction vs. county-native auction sites** | Ohio sheriff sales migrated to `{county}.sheriffsaleauction.ohio.gov`; some counties keep a `sheriff.{county}.gov/sheriff-sales` native page with additional info (bidding rules, results archive). | Both URLs belong on the sheriff-sale row. RealAuction sometimes 403's bot UAs — county-native page is the fallback. |

### State-specific templates

Before researching a county, search for a prior county report from the same state. If one exists, use its non-county-specific fields (statewide aggregator, state tax-lien process, forfeited-land statute, state sheriff-sale vendor, ODNR/EPA-equivalent) as the starting point. You're researching the **county-specific** fields, not re-deriving the state infrastructure from scratch.

## Multi-URL Portal Convention

The Portal URL field (column F) accepts **newline-separated URLs**. Default to listing 2-3 URLs per row:

1. **Primary portal** — the one you'd scrape first
2. **Cross-validation source** — a different system that carries the same data (e.g., court journal publishing foreclosure notices, state aggregator filtering to the county)
3. **Backup / alternate** — fallback when primary is rate-limited, blocked, or paywalled

Only list a single URL when you have explicitly verified (WebFetch / WebSearch) that no alternate exists. If the only second URL is a thin/marketing page, leave it out rather than padding.

Example (good):
```
https://summit.sheriffsaleauction.ohio.gov
https://sheriff.summitoh.net/pages/Sheriff-Sales.html
https://www.akronlegalnews.com/notices/sheriff_sales
```

Example (bad — single URL with no cross-validation):
```
https://summit.sheriffsaleauction.ohio.gov
```
(Unacceptable unless you've confirmed no county-native page and no court-journal republishing exists.)

## Data Types Available

### Priority A - Core Lists (Big Vexation)
| Data Type | Description |
|-----------|-------------|
| Probate/Heirship | Estates, unknown heirs, heirship determinations |
| Foreclosure/Auction | Lis pendens, in-rem foreclosures, auction lists |
| Tax Sale | Properties going to tax auction |
| Tax Delinquency | Properties with unpaid property taxes |

### Priority B - Standard Lists
| Data Type | Description |
|-----------|-------------|
| Code Violations | Municipal code enforcement fines |
| Condemned Structures | Unsafe/condemned building registers |
| Mechanic's Liens | Contractor liens against property |
| IRS/State Tax Liens | Federal and state tax liens on real estate |

### Priority C - Extended Lists
| Data Type | Description |
|-----------|-------------|
| HOA/Condo Liens | Assessment liens from associations |
| Utility Shut-offs | Water/electric disconnection lists |
| Building Permits | Open/expired residential permits |
| Environmental Citations | Mold, asbestos, lead hazard citations |
| Storm/Fire Damage | Incident reports from Fire Marshal |
| Medicaid Recovery Liens | Estate recovery liens |
| Multiple-Eviction Landlords | Properties with 2+ eviction filings |
| Child Support Liens | Judgment liens on real property |
| Quiet-Title Suits | Post-tax-deed quiet title lawsuits |
| Sinkhole/Subsidence | Geological survey claims data |

## Research Prompt Format

For each data type, use this prompt structure:

```
Act as a public-records researcher. For {{COUNTY}} County, {{STATE}}, 
identify the office that [records/maintains/handles] [DATA_TYPE].

Return in one markdown table row:
• Office/division name
• Street address & phone #
• Online index/portal link (if any)
• Low / Medium / High estimate of difficulty to bulk-download the data
```

See `references/research-prompts.md` for complete copy-paste prompts for all 16+ data types.

## Output Format — Canonical Template

**Required: 10-column XLSX built via `scripts/build_spreadsheet.py`.** Full spec in `references/spreadsheet-template.md`.

Columns (A–J, fixed order):

| # | Column | Contents |
|---|--------|----------|
| A | Priority | A / B / C |
| B | Data Type | e.g., "Probate / Heirship", "Lis Pendens / Foreclosure" |
| C | Office / Division | Full office name |
| D | Address | Street + city/state/zip (multi-line OK) |
| E | Phone | Formatted with area code |
| F | Portal URL | Primary online search URL |
| G | FOIA / Contact Email | FOIA form URL or contact email |
| H | Difficulty | Low / Low-Medium / Medium / High |
| I | Notes | Access quirks, legal caveats, scraping hot-buttons |
| J | Data Freshness | e.g., "Daily filings", "Weekly auction schedule", "Annual PDF" |

Includes a second **Legend & Notes** sheet with priority/difficulty legends and county-specific context.

## Difficulty Rating Guide

| Rating | Meaning |
|--------|---------|
| **Low** | Online portal with bulk export; minimal barriers |
| **Low-Medium** | Online searchable but bulk export limited; may need account or FOIA |
| **Medium** | Account registration, limited export, or in-person pickup required |
| **High** | FOIA request, physical visit, affidavit, or paywall required |

## Example Usage

**User request**: "Find where to pull first-to-market data for Knox County, Tennessee"

**Response workflow**:
1. Run research prompts for Priority A data types (probate, foreclosure, tax sale, tax delinquency)
2. Compile findings into spreadsheet
3. Note any special requirements (e.g., Knox County requires physical visit + affidavit for tax sale data)
4. Deliver CSV/XLSX with all source details

## Important Notes

- Some counties have strict anti-predatory regulations requiring in-person visits
- Data freshness varies: probates may be weekly, auctions may be monthly
- Always verify current requirements—county processes change frequently
- Water shut-off lists are highly valuable but often difficult to obtain
- First-to-market advantage diminishes if data is also available through PropStream/BatchLeads

## Reference Files

- `references/research-prompts.md` — Complete copy-paste prompts for all data types
- `references/common-offices.md` — Typical office names by data type
- `references/spreadsheet-template.md` — Canonical XLSX output spec (columns, colors, sheet structure)
- `scripts/build_spreadsheet.py` — Template builder; takes input JSON, produces the XLSX
