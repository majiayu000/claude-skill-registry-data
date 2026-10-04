---
name: 04-theirstack-jobs
description: >
  Pulls open job postings from the TheirStack API and turns them into
  structured hiring signals - open roles per domain, titles, seniority,
  posting dates, hiring team, plus free firmographics (headcount, funding
  stage, industry). Step 04 (signals) of the API-first GTM chain, and the
  discovery entry for hiring-defined ICPs. Use when the user wants hiring
  signals, open reqs, job postings, "who is hiring", "which of these
  companies are hiring X", "find companies hiring Y right now", open-role
  checks on a domain list or records.jsonl, or anything TheirStack. Sizing
  counts bound every pull before spend - free without company filters, ~1
  credit against a domain list - then 1 credit per job returned. For people
  who already joined - recent hires, headcount growth, funding rounds - use
  04-crustdata-signals; for scoring and campaign angles, hand the records
  to 05-signal-builder.
---

# TheirStack Jobs - open-req hiring signals (04)

Open job postings are the "what they're about to do" signal: a company hiring
its first SDRs is building outbound, a VP Sales req is a strategy shift, three
engineering reqs after a raise is product investment. This skill pulls those
postings per company and emits chain records ready for judgment. Its sibling
04-crustdata-signals covers what already happened (funding, joins, headcount);
this one covers what's open right now.

## Two modes

| Mode | Input | Use when |
|---|---|---|
| **check** | Domains (`--domains` or an upstream `--records` records.jsonl) | You have a list and want hiring evidence per company - the standard step-04 position in the chain |
| **discover** | Filters only (title/seniority/tech + geo/size/funding) | The ICP is the req itself: "companies hiring SDRs in the US right now". This is the direct entry for hiring-defined ICPs - no firmographic superset needed first |

## Prerequisites

- `THEIRSTACK_API_KEY` in env or `.env` - get one at
  [app.theirstack.com/settings/api](https://app.theirstack.com/settings/api)
- No Python packages required (stdlib only; `python-dotenv` is optional - the
  script falls back to reading `.env` itself)

## Credit rules

Credits are money. The script's whole flow is built around four facts
verified live against the balance ledger (2026-07-24):

| Operation | Cost |
|---|---|
| Count without company filters (`blur_company_data` + `include_total_results` + limit 1) | 0 credits - exact totals of matching jobs AND companies, free. Discover mode sizing is genuinely free |
| Count WITH `company_domain_or` | Blur silently disables on company-identifier filters (HTTP 200, unblurred, billed per returned job). At limit 1 that is ~1 credit per count - and 0 when the domain has no matches. There is no zero-credit domain-scoped count |
| Job fetch | 1 credit per job returned, exactly |
| Re-fetching a job you already pulled | Charged again - TheirStack has no charge dedup |

Because re-pulls cost full price, every fetched domain is cached as
`domains/<domain>.json` keyed by a query hash. Re-running the same query
reuses the cache for 0 credits (any prior run folder counts, not just the
current one). `--no-cache` forces a refetch.

Every paid pull is preceded by a sizing count, and anything estimated over
the gate (default 500 credits, `--credit-gate` to change) stops for
confirmation. `--count-only` answers "how many / what would it cost" for 0
credits in discover mode and ~1 credit against a domain list. When the user
says "spend nothing", say the ~1-credit floor out loud instead of silently
eating it. Ledger postings can lag by minutes - read actual spend from
`meta.json`'s `balance_before`/`balance_after` delta after it settles, not
from assumptions.

## Process

All paths relative to this skill's folder. The script prints the free count
and estimate before any spend - no separate estimation step needed.

```bash
# Size it first when the user only wants numbers (0 credits)
python3 scripts/theirstack_jobs.py count \
  --domains stripe.com,notion.so --title "SDR,BDR" --days 30

# Check a domain list (per-domain pulls, cached, resumable)
python3 scripts/theirstack_jobs.py check \
  --domains stripe.com,notion.so --title "SDR,BDR,Sales Development" \
  --days 30 --per-domain 10

# Chain position: read domains from an upstream records.jsonl -
# every upstream field carries through into the output records
python3 scripts/theirstack_jobs.py check \
  --records ./runs/<run-id>/records.jsonl \
  --title "Head of Sales,VP Sales,CRO" --days 30

# Discover companies currently hiring for a role
python3 scripts/theirstack_jobs.py discover \
  --title "Revenue Operations,RevOps" --country US \
  --min-employees 50 --max-employees 500 --days 14 --max-jobs 200

# Resume an interrupted run (no double spend - cache + tracker)
python3 scripts/theirstack_jobs.py check --resume --run-dir runs/<run-id>

# Balance
python3 scripts/theirstack_jobs.py credits
```

Spend levers, in order of effect: `--title` (narrows what counts as a match),
`--per-domain` (check-mode cap, default 10), `--max-jobs` (discover-mode
ceiling, default 200), `--days` (window, default 30). A company with 50 open
roles costs 50 credits uncapped - the caps exist so it costs 10.

## Building title filters

`--title` is keyword matching on the title (comma-separated, OR). Compose
from what the client's offer makes relevant:

| Signal target | Title keywords |
|---|---|
| Outbound buildout | SDR, BDR, Sales Development, Outbound |
| Sales leadership shift | Head of Sales, VP Sales, CRO, Sales Director |
| Marketing motion | Marketing, Growth, Demand Gen, Product Marketing |
| RevOps maturity | Revenue Operations, RevOps, Sales Operations, GTM Operations |
| Product investment | Engineer, Founding Engineer, CTO, Head of Engineering |

Interpretation stays downstream: multiple same-department reqs = team
buildout, a single senior req = strategy change, one junior backfill = weak
signal. 05-signal-builder scores this; this skill only gathers the facts.

## Output contract

Each run writes `runs/<run-id>/` per `headless-gtm-shared/CONVENTIONS.md`:

```
runs/<run-id>/
├── records.jsonl     # one line per domain - what the chain consumes
├── records.csv       # human export (derived)
├── domains/*.json    # per-domain cache: curated jobs + query hash
├── tracker.json      # resume state
├── filters.json      # the exact API filters used
└── meta.json         # counts, credits estimate, balance before/after
```

Records are additive: upstream fields pass through untouched, `domain` is
normalized (lowercase, no www., no scheme), `filters_matched` unions. Fields
this skill adds: `open_roles_count`, `roles_window_days`, `roles_title_filter`,
`jobs[]` (title, url, date_posted, location, remote, seniority, salary,
hiring_team, description_snippet), plus free firmographics when present:
`employee_count`, `funding_stage`, `total_funding_usd`, `industry`,
`company_hq`. Real example (trimmed):

```jsonl
{"company": "Stripe", "domain": "stripe.com", "person": null, "open_roles_count": 2, "roles_window_days": 30, "jobs": [{"title": "Sales Development Representative", "url": "https://stripe.com/jobs/search?gh_jid=8083685", "date_posted": "2026-07-24", "location": "Dublin", "seniority": "mid_level"}], "employee_count": 16807, "funding_stage": "secondary_market", "filters_matched": ["2 open 'SDR,BDR' role(s) in last 30d (latest 2026-07-24)", "hiring: Sales Development Representative; Head of Sales Development, AMER"]}
```

Domains checked with zero matches still get a record (`open_roles_count: 0`,
a "no open roles" line in `filters_matched`) - downstream needs to distinguish
checked-and-quiet from never-checked.

## Key behaviors

- The API requires at least one of: a posting-age filter, a company domain
  filter, or a company name filter. The script always sends
  `posted_at_max_age_days`, so any filter combination on top is valid.
- Domain matching is exact; name matching (`--names` is deliberately not
  exposed - pass domains) is fuzzy and pulls false positives.
- Discover mode refuses to run without at least `--title`, `--seniority`, or
  `--tech` - an unfiltered pull of every recent posting is never worth credits.
- Observed enum values: `seniority` = `junior` / `mid_level` / `senior` /
  `c_level`; `funding_stage` includes `seed`, `series_a`..., and
  `secondary_market` for late-stage. Treat as observed, not exhaustive.
- `hiring_team` (name, title, LinkedIn) is present on some postings - when it
  is, that person is a resolution shortcut for 06.
- The balance endpoint (`/v0/billing/credit-balance`) is undocumented but
  live; if it ever disappears the script degrades to a dashboard pointer.
- Results order newest-first; discover mode's `--max-jobs` ceiling therefore
  keeps the freshest postings.

## Chain handoff

- **05-signal-builder**: pass the run's records file via
  `--records runs/<run-id>/records.jsonl`. Open-req evidence usually lands as
  a WHEN/timing signal; 05 owns the 1-10 score and approach call.
- **04-crustdata-signals**: run both when the play needs open reqs AND recent
  joins/funding - same records.jsonl in, additive fields out, 05 merges by
  domain.
- **06-resolution-email-person**: `hiring_team` entries and senior req titles
  ("Head of Sales") tell 06 who to resolve.
- **email-writer**: `filters_matched` lines are situation-line raw material
  ("saw you're hiring your first SDRs...").

## Scope boundaries

| Not this skill | Use instead |
|---|---|
| Who already joined, headcount growth, funding rounds | 04-crustdata-signals |
| Firmographic TAM building (industry + size + geo) | 01-prospeo-discover |
| Scoring signals / picking the campaign approach | 05-signal-builder |
| Tech-stack lookups without job postings | Not built yet - TheirStack's technographics endpoint (3 credits/company) is a natural sibling if needed |

## References

- `references/jobs-api.md` - full filter list, response fields, free-count
  recipe, curl examples, verified credit mechanics
- [TheirStack API docs](https://theirstack.com/en/docs/api-reference) - the
  vendor source of truth
