---
name: finding-b2b-contacts
description: Find B2B contacts and decision-makers by searching LinkedIn with filters (job title, location, company size, recently changed jobs). Use when the user wants to build a prospect list, find people at companies, find founders or owners in an area, or asks for "B2B leads" or "System 1".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Finding B2B Contacts (System 1)

## Goal
Build a list of real decision-makers with job titles, companies, LinkedIn URLs, and optionally emails — by searching LinkedIn live rather than querying a stale contact database.

## When to use
- "Find me 50 marketing directors in Texas"
- "I need a list of agency owners in Alabama"
- "Who are the founders at companies with 50-200 staff in fintech?"
- Anything the user calls System 1, B2B leads, or prospecting

## Check this first: it needs a paid Apify plan

`harvestapi/linkedin-profile-search` allows free Apify accounts **10 runs total**,
then returns zero results with a SUCCEEDED status. The script detects this and
explains it, but know it up front.

**If the user is on the free plan**, steer them to `finding-local-businesses`
(System 2, no cap) or `free-lead-scraping` (System 3, no Apify at all). Don't let
them burn time tuning filters against a run that never started.

The video's original actor (`scrape_apify.py`) works on free, but Apify requires
a one-time browser approval of full-account permissions. The error message it
returns contains the exact URL to do that.

## Inputs

| Flag | Required | What it does |
|---|---|---|
| `--titles` | one of these | Job titles: `--titles Owner Founder "General Manager"` |
| `--query` | one of these | Free-text search if titles are too rigid |
| `--locations` | No | `--locations "Alabama" "Georgia"`. Use full country names — LinkedIn reads "UK" as Ukraine. |
| `--headcount` | No | Company size bands: `"11-50"`, `"51-200"` |
| `--limit` | No | Default 25. Always start here. |
| `--mode` | No | `short` (~$0.004/profile), `full` (~$0.008), `email` (~$0.014) |
| `--recently-changed-jobs` | No | Only people who just started a role |
| `--recently-posted` | No | Only people currently active on LinkedIn |

## Process

### Step 1 — always test 25 first
```bash
python -X utf8 scripts/01_b2b_contacts/search_linkedin.py \
    --titles "Owner" "Founder" --locations "Alabama" --limit 25 \
    --out-csv output/test_leads.csv
```

**Then read the CSV before going further.** If fewer than 20 of the 25 are the kind of person the user meant, the filters are wrong. Fix them and test again. Scraping 1,000 of the wrong people faster is not progress.

### Step 2 — the full run
```bash
python -X utf8 scripts/01_b2b_contacts/search_linkedin.py \
    --titles "Owner" --locations "Alabama" --limit 500 \
    --mode email --output output/leads.json --out-csv output/leads.csv
```

### Step 3 — research each lead
```bash
python -X utf8 scripts/01_b2b_contacts/research_lead.py \
    --input output/leads.json --output output/researched.json
```

### Step 4 — write the outreach
See the `writing-cold-outreach` skill.

## The trigger-event shortcut

`--recently-changed-jobs` is the highest-leverage flag here. Someone three weeks into a new role is rebuilding their stack and has budget to prove. It also means every lead arrives with a trigger event already attached, so the research step has something concrete to work with instead of hunting.

## Edge cases

- **Fewer results than `--limit`** — normal. The filters were narrow. Drop one and retry.
- **"give the search something to go on"** — you passed only `--locations`. Location alone isn't a search; add `--titles` or `--query`.
- **Locations behaving oddly** — LinkedIn's own location matching is fuzzy. Use "United Kingdom", not "UK". Test the term in LinkedIn's search box first.
- **Empty `email` fields in `--mode email`** — the actor found the profile but not a verified address. Expected for a minority of profiles; don't guess an address from the name and domain.

## Following the video exactly

The course used `code_crafter/leads-finder`. It's still here:
```bash
python -X utf8 scripts/01_b2b_contacts/scrape_apify.py --query "Plumbers" --location "Alabama" --max_items 25 --no-email-filter
```
It's cheaper (~$0.0015/lead) but it queries a scraped database rather than LinkedIn, and that actor category now rates 2.1–3.9 stars on Apify, largely for stale records and bounced emails. Prefer `search_linkedin.py` unless the user specifically wants the video's path.

## Cost
Roughly $0.10 for a 25-lead test, $2–7 for 500 leads depending on mode. See `docs/COSTS.md`.
