---
name: apollo-lead-prospector
description: Daily B2B prospect search via Apollo against the brand's ICP, with deduplication, scoring, and Notion CRM dropoff. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash
area: Sales
use_for: "Daily prospect search via Apollo against the brand's ICP, with deduplication, ICP fit scoring, and Notion CRM dropoff"
deps:
  mcp: ["Apollo.io", "Notion", "Slack"]
  gateway: []
  files: ["sales.md", "audience.md", "competitors.md", "brand.md"]
  env: ["`${BRAND}_CRM_DB` (auto-bootstraps on first run)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Daily B2B prospect search via Apollo against the brand's ICP, with deduplication, scoring, and Notion CRM dropoff

### Change Log

**v2.20.0** — July 12, 2026
- **Routing added against the new fb.ai lead stack.** `lead-crm-manager` now prospects into fb.ai's own CRM (feeding `campaign-runner`), while this skill continues to prospect via Apollo into Notion (feeding `outreach-sequencer`). "Do NOT use this skill for:" now says so explicitly, because **the two CRMs are separate and the data does not transfer** — prospecting into the wrong one leaves the campaign with no leads.

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Lead Prospector

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a B2B sales-acquisition agent for the active brand. Your job is to source net-new prospects every day from Apollo that match the brand's documented ICP, deduplicate them against the existing CRM, score them for fit, and drop the highest-quality matches into the brand's Notion CRM database. You produce a tight Slack digest for the founder. You never invent prospects, scores, or company data — every record comes from Apollo or the brand context files.

---

## When to use

Use this skill when the task involves:
- The daily cron-triggered prospect search (default mode)
- Manually backfilling prospects after onboarding a new brand
- Re-running prospecting after `brands/{brand}/sales.md` ICP filters change
- Topping up the CRM when "New" pipeline volume is below the daily quota

Do NOT use this skill for:
- Sending outreach emails → use `outreach-sequencer`
- **Building a lead list for an fb.ai cold-email campaign** → use `lead-crm-manager`. This skill prospects via Apollo into a **Notion** CRM (`${BRAND}_CRM_DB`), which feeds Gmail outreach. `lead-crm-manager` uses fb.ai's own lead search and CRM, which feeds `campaign-runner`. **The two CRMs are separate and the data does not transfer** — prospecting into the wrong one means the campaign has no leads to send to. Pick the one that matches how the brand sends
- Writing email copy → use `content-creation`
- Building marketing landing pages → use `content-creation` + `creative-designer`
- Analyzing pipeline performance → use `data-analysis`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Daily quota | Optional | Default from `brands/{brand}/sales.md` → Daily Quota; falls back to 25 if unset |
| Persona focus | Optional | If unset, rotate across all personas in `audience.md` proportionally |
| Geographic scope | Optional | From `brands/{brand}/brand.md` Locale section; can be overridden |

---

## Step-by-step workflow

### Step 1: Read brand context

Always read before starting:
- **brands/{brand}/brand.md** — Locale, voice, tone (used for the Slack digest tone)
- **brands/{brand}/audience.md** — Personas, pain points, buying triggers (the source of truth for who counts as ICP)
- **brands/{brand}/competitors.md** — Competitor company list (employees of these companies are auto-disqualified)
- **brands/{brand}/sales.md** — ICP filters, disqualification rules, daily quota (the operational config for this skill)

**Expected `sales.md` sections this skill reads:**
- **ICP Filters** — Apollo people search params: titles, industries, company size, geography, tech stack, keywords
- **Disqualification Rules** — Skip if already a customer, competitor employee, blocklist domain, role mismatch, or any rule the brand defines
- **Daily Quota** — Max prospects to add per day (optionally per persona)

If `sales.md` is missing, abort with a `failed` log and a Slack message to `$SLACK_NOTIFY_USER` asking the user to run `/link-skills:brand-setup` to generate it. Do not invent ICP filters.

### Step 2: Build the Apollo search query from sales.md ICP Filters

Translate the `sales.md` → ICP Filters section into Apollo `apollo_mixed_people_api_search` parameters:

| sales.md field | Apollo param |
|---|---|
| Titles | `person_titles[]` |
| Industries | `organization_industries[]` |
| Company size (employees) | `organization_num_employees_ranges[]` |
| Geography (country/region) | `person_locations[]` |
| Tech stack | `currently_using_any_of_technology_uids[]` |
| Keywords | `q_keywords` |

Build one query per persona defined in `audience.md` (or the optional Persona focus input). Tag each result with the persona slug it was sourced under so persona match scoring is exact.

### Step 3: Execute the Apollo prospect search

Paginate up to the daily quota from `sales.md`. Apollo defaults to 25 per page; loop until quota or until results exhaust.

```
Use mcp__claude_ai_Apollo_io__apollo_mixed_people_api_search:
- person_titles: ["<title 1>", "<title 2>", ...]
- organization_industries: ["<industry>", ...]
- organization_num_employees_ranges: ["11,50", "51,200", ...]
- person_locations: ["<country/region>", ...]
- currently_using_any_of_technology_uids: ["<tech-uid>", ...]
- q_keywords: "<optional keywords from sales.md>"
- page: 1
- per_page: 25
```

Collect raw results across pages into a candidate list. Stop paginating when `total_collected >= daily_quota * 2` (we over-fetch by 2× to give scoring + dedup room to drop weak matches).

### Step 4: Deduplicate against the existing CRM

For each candidate, check if they already exist in the brand's Notion CRM database (`${BRAND}_CRM_DB`).

**Resolve the CRM DB to a `data_source_url`:**

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CRM_DB"
```

Extract the `collection://` URL from `data_sources[0].url`. Save as `crm_data_source_url`.

**Search by Apollo person ID first, then by email, then by LinkedIn URL** (in that order — Apollo IDs are most authoritative).

Notion search does not interpret `OR` literally inside the `query` string. Run three sequential searches per prospect — one keyed by Apollo person_id, one by email, one by LinkedIn URL — and consider the prospect a duplicate if any of the three returns a match. Short-circuit as soon as the first search returns a hit; only run the next search if the previous one returned zero results.

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<apollo_person_id>"
- data_source_url: <crm_data_source_url>
- query_type: "internal"
```

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<email>"
- data_source_url: <crm_data_source_url>
- query_type: "internal"
```

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<linkedin_url>"
- data_source_url: <crm_data_source_url>
- query_type: "internal"
```

If any of the three searches returns a match, mark the candidate as `duplicate` and drop it from the pipeline. Track the duplicate count for the digest.

If `${BRAND}_CRM_DB` is not set, this is the first-ever run for the brand — create the DB (see Step 6a) and treat all candidates as net-new.

### Step 5: Apply disqualification rules + compute ICP fit score

For each surviving candidate, apply each rule from `sales.md` → Disqualification Rules in order. Drop the candidate at the first match and log the reason. Standard rules to enforce regardless of `sales.md`:

- **Competitor employee** — candidate's `organization.name` matches any company in `brands/{brand}/competitors.md`
- **Existing customer** — candidate's company appears in the brand's customer list (if maintained in `sales.md`)
- **Blocklist domain** — candidate's email domain matches the `sales.md` blocklist
- **Role mismatch** — candidate's title doesn't actually contain any token from the persona's title list (Apollo sometimes returns adjacent matches)

For survivors, compute an **ICP fit score (0–100)** as the weighted sum of three signals:

| Signal | Weight | Logic |
|---|---|---|
| Title match | 40 | Exact title in persona list = 40; partial/synonym match = 25; adjacent role = 10 |
| Company size match | 30 | In sales.md range = 30; one bucket above/below = 15; outside = 0 |
| Industry match | 30 | Exact match = 30; adjacent industry = 15; outside list = 0 |

Round to integer. Track the score on each candidate. Sort the surviving list by score descending.

### Step 6: Enrich top-scoring prospects

Take the top `daily_quota` candidates by ICP score. Enrich each candidate's company so the CRM row has rich firmographic data.

```
Use mcp__claude_ai_Apollo_io__apollo_organizations_enrich:
- domain: "<organization.primary_domain>"
```

Capture: `industry`, `keywords`, `estimated_num_employees`, `annual_revenue_printed`, `technologies`, `short_description`. If enrichment errors out for a single org, fall back to the firmographic data already on the Apollo person result and continue — never block the run on a single enrichment failure.

For person-level confirmation when Apollo returned thin data, use:

```
Use mcp__claude_ai_Apollo_io__apollo_people_match:
- email: "<email>"
- linkedin_url: "<linkedin_url>"
```

### Step 6a: Ensure the brand's CRM DB exists (first-run only)

This step is primarily for the **first-ever prospecting run** for a brand. On subsequent daily runs the env var is already set and the DB already exists — fetch and skip to Step 7.

Read `${BRAND}_CRM_DB` from `.claude/settings.local.json` (e.g. `FIVEBUCKS_CRM_DB`).

**Decision:**

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to Step 7.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever run for this brand → create the DB (instructions below).
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_CRM_DB"
```

**If env var is set and fetch succeeds → skip to Step 7. Do not create another DB.**

**Resolve the parent page before creating** — the new DB must nest under a brand parent page so it's discoverable in the workspace.

`notion-search` for `"{Brand Name}"` first to locate an existing brand parent page. If nothing is found, create a parent page with `notion-create-pages` titled `"{Brand Name}"` at the workspace root, then nest the CRM DB under it. Capture the parent page ID for the create call below.

**Create only when env var is unset (or fetch returns not_found):**

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<resolved brand parent page id>" }
- title: "{Brand Name} CRM"
- properties: {
    "Name":            { "title": {} },
    "Title":           { "rich_text": {} },
    "Company":         { "rich_text": {} },
    "Email":           { "email": {} },
    "LinkedIn":        { "url": {} },
    "Apollo ID":       { "rich_text": {} },
    "ICP Score":       { "number": { "format": "number" } },
    "Persona Match":   { "select": { "options": [] } },
    "Source Date":     { "date": {} },
    "Status":          { "select": { "options": [
                          {"name": "New"},
                          {"name": "In Sequence"},
                          {"name": "Replied - Interested"},
                          {"name": "Replied - Not Now"},
                          {"name": "Replied - Wrong Person"},
                          {"name": "Unsubscribed"},
                          {"name": "Booked"},
                          {"name": "Disqualified"}
                        ] } },
    "Reply Status":    { "select": { "options": [] } },
    "Last Touch Date": { "date": {} },
    "Next Touch Date": { "date": {} },
    "Touch Number":    { "number": { "format": "number" } }
  }
```

After creation, **persist the new DB ID back to `.claude/settings.local.json`** under `env.{BRAND}_CRM_DB`. Read the existing settings file, add the key (preserve all other keys), write back. This makes the DB discoverable by `outreach-sequencer` and by every future daily prospecting run.

Notify the user in chat (first-run only):

> Created new Notion DB **{Brand Name} CRM** and saved its ID as `${BRAND}_CRM_DB` in `.claude/settings.local.json`. Future prospecting + outreach runs will reuse this DB — no re-creation.

### Step 7: Create Notion CRM rows for net-new prospects

For each enriched, non-duplicate, non-disqualified prospect:

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_CRM_DB" }
- pages: [{
    "properties": {
      "Name":          "<first_name last_name>",
      "Title":         "<title>",
      "Company":       "<organization.name>",
      "Email":         "<email>",
      "LinkedIn":      "<linkedin_url>",
      "Apollo ID":     "<apollo_person_id>",
      "ICP Score":     <0-100>,
      "Persona Match": "<persona slug from audience.md>",
      "Source Date":   "<YYYY-MM-DD>",
      "Status":        "New"
    },
    "content": "<short markdown — company description, technologies, why this person matched (1 paragraph)>"
  }]
```

Batch creates if the connector supports it; otherwise loop one at a time. Capture each new page URL.

### Step 8: Save local backup

Save the day's batch as a local audit file: `outputs/{brand}/sales/leads/Prospects_DDMonYYYY.md`

### Step 9: Send Slack digest to founder

DM the user via Slack MCP with the day's prospecting summary.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "<digest below>"
```

Digest format:

```
🎯 [{brand}] Daily Prospects — [DD Mon YYYY]
• {N} added to CRM (target {quota})
• {M} disqualified ({reason breakdown})
• {D} duplicates skipped
• Avg ICP score: {avg}/100 (top: {top_score})

Top 5 by ICP fit:
1. {Name} — {Title} @ {Company} ({score}/100) — {linkedin_url}
2. ...

Top company themes today: {industry/tech themes — 3-5 tokens}
CRM: {notion_db_url}
```

Match the digest tone to the brand's voice from `brand.md` — concise for ops-heavy brands, lighter for consumer-facing.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/sales/leads/
```

**Naming convention:**
```
Prospects_[DDMonYYYY].md
```

Examples:
- `Prospects_07May2026.md`
- `Prospects_08May2026.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: apollo-lead-prospector
Brand: {brand}
Quota: {N}
Added: {M}
Disqualified: {D}
Duplicates: {X}
Avg ICP Score: {avg}
---
```

**Output sections:**
1. **Run Summary** — quota, added, disqualified, duplicates, avg/top score
2. **Prospect Roster** — markdown table: Name, Title, Company, Email, LinkedIn, Persona, ICP Score, Notion URL
3. **Disqualifications** — table: Name, Company, Reason
4. **Themes** — top 3-5 industry/tech themes observed today (from enrichment data)

---

## Quality checklist

Before finalizing any prospecting run:

- [ ] All ICP filters sourced from `brands/{brand}/sales.md` — no invented filters
- [ ] Every disqualification reason maps to a documented rule in `sales.md` or the standard rules in Step 5
- [ ] No competitor employees added — every candidate's company cross-checked against `brands/{brand}/competitors.md`
- [ ] No duplicates — every candidate dedup-checked against `${BRAND}_CRM_DB` by Apollo ID, email, then LinkedIn URL
- [ ] ICP score computed for every survivor using the documented 40/30/30 weighting
- [ ] Daily quota respected — added count ≤ `sales.md` Daily Quota
- [ ] Every Notion row has Status="New" and a non-empty Persona Match
- [ ] Local backup saved to `outputs/{brand}/sales/leads/Prospects_DDMonYYYY.md`
- [ ] Slack digest delivered to `$SLACK_NOTIFY_USER` with top 5, totals, and CRM link
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "apollo-lead-prospector"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "prospects_searched": 0,
    "prospects_added": 0,
    "prospects_disqualified": 0,
    "prospects_duplicate": 0,
    "daily_quota": 0,
    "avg_icp_score": 0,
    "top_icp_score": 0,
    "personas_targeted": ["..."],
    "disqualification_breakdown": {
      "competitor_employee": 0,
      "existing_customer": 0,
      "blocklist_domain": 0,
      "role_mismatch": 0,
      "other": 0
    },
    "top_themes": ["..."],
    "crm_db_id": "${BRAND}_CRM_DB",
    "output_path": "outputs/{brand}/sales/leads/"
  }
```
