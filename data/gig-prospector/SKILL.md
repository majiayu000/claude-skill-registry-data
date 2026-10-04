---
name: gig-prospector
description: Daily inbound freelance-job discovery across the markets and platforms the brand chose — scrapes job posts via Claude in Chrome (Freelancer.com API where available), scores each for service fit, deduplicates, and drops matches into a Notion opportunities DB. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__computer
area: Sales
use_for: "Daily inbound freelance-job discovery across chosen markets/platforms, scored for service fit, deduplicated, dropped into a Notion opportunities DB"
deps:
  mcp: ["Notion", "Slack", "Claude in Chrome (opt — primary job-scrape source; degrades to Freelancer.com API + web research when absent)"]
  gateway: ["FiveAgents (logging)"]
  files: ["sales.md", "product.md", "brand.md", "audience.md", "competitors.md"]
  env: ["`${BRAND}_GIGS_DB` (auto-bootstraps on first run)", "`FREELANCER_OAUTH_TOKEN` (opt — enables the Freelancer.com API source)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.17.0 | June 21, 2026 |

**Description:** Daily inbound freelance-job discovery across the brand's chosen markets/platforms, scored for service fit, deduplicated, dropped into a Notion opportunities DB

### Change Log

**v2.17.0** — June 21, 2026
- Now the **Discover** phase of the full **Inbound Gig Engine**. Forward-references corrected: the bid is written by the new **`gig-proposal-writer`** (cover letter + 60s VSL), then `n8n-workflow-builder` (proof workflow) and `vsl-demo-producer` (demo) complete the chain — `proposal-generator` remains CRM-deal-only (Gamma deck + Stripe link). **The `${BRAND}_GIGS_DB` bootstrap now seeds the full pipeline `Status` set** — `New → Reviewing → Drafted → Workflow Built → Demo Ready → Ready to Submit → Proposed → Won → Lost → Skipped → Disqualified` — so the whole engine's states exist in the Notion dropdown from day one (downstream skills still add-if-missing for DBs created before this change). Discovery logic itself is unchanged.

**v2.16.0** — June 20, 2026
- New skill (Sales). The **inbound** counterpart to `apollo-lead-prospector` (which is outbound): instead of sourcing people to email, it sources *open freelance jobs the brand can bid on* across the markets and platforms the user selected in `sales.md → Inbound Job Filters` (written by `brand-setup` Step 5g Step H). Search terms are derived from `product.md` / `brand.md` (what the brand actually sells) — never hardcoded. Scrapes via **Claude in Chrome** (the user's own authenticated, non-automated browser — beats Cloudflare and reads jobs behind login walls), uses the **Freelancer.com API** as a deterministic source where a token is set, and degrades to web research when Chrome MCP is absent. Dedupes against `${BRAND}_GIGS_DB` by job UID/URL, scores each job for service fit, and drops matches as `Status="New"` for review.

---

# SKILL.md — Gig Prospector

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are an **inbound** sales-acquisition agent for the active brand. Your job is to find open freelance/contract jobs every day — across the markets and platforms the brand selected during setup — that match **what the brand actually sells**, deduplicate them against the opportunities already tracked, score each for fit, and drop the strongest matches into the brand's Notion opportunities database. You produce a tight Slack digest for the founder. You never invent jobs, clients, budgets, or scores — every record comes from a real job post or the brand context files.

This is the mirror of `apollo-lead-prospector`: that skill sources *people to reach out to* (outbound); this one sources *jobs to apply to* (inbound).

---

## When to use

Use this skill when the task involves:
- The daily cron-triggered job scan (default mode)
- Manually backfilling opportunities after onboarding a brand or changing markets/platforms
- Re-running discovery after `brands/{brand}/sales.md` → Inbound Job Filters change
- Topping up the opportunities DB when "New" volume is low

Do NOT use this skill for:
- Sourcing people to cold-email → use `apollo-lead-prospector`
- Writing the actual bid/cover letter → use `gig-proposal-writer` (this skill feeds it). (`proposal-generator` is for CRM **deals** — Gamma deck + Stripe link — not inbound gigs)
- Writing marketing copy → use `content-creation`
- Outbound email sequencing → use `outreach-sequencer`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Markets | From config | `sales.md` → Inbound Job Filters → Markets; abort if the section is missing |
| Platforms + accounts | From config | `sales.md` → Inbound Job Filters → Platforms (each tagged "have account" / "no account") |
| Freshness window | Optional | Default 48h; jobs posted older than this are disqualified (hard cutoff). Widen to 72h for a backfill |
| Daily cap | Optional | `sales.md` → Inbound Job Filters → Daily Cap; falls back to 30 |

---

## Step-by-step workflow

### Step 1: Read brand context — derive search terms (never hardcode them)

Always read before scanning:
- **brands/{brand}/product.md** — Overview, Features, Differentiators. **This is the source of truth for what the brand sells** — the search keywords are derived from here.
- **brands/{brand}/brand.md** — niche, voice, Locale (for the digest tone)
- **brands/{brand}/audience.md** — who the brand serves (helps judge whether a job's client is a fit)
- **brands/{brand}/competitors.md** — the space the brand competes in (informs adjacent-service matching)
- **brands/{brand}/sales.md** — **Inbound Job Filters** section (the operational config for this skill)

**Build the search-term set from `product.md`, do NOT hardcode a keyword like "automation".** Read the Features / Overview / Differentiators and extract the concrete services the brand delivers and the tools it delivers them with (e.g. a workflow-automation agency yields terms like its platform names, "integration", "workflow", "API", the specific apps it connects). If `sales.md → Inbound Job Filters` lists explicit `Search Keywords`, use those as the authoritative set and treat the product.md-derived terms as supplements. Tag every term with the service it maps to so service-fit scoring in Step 4 is exact.

**Expected `sales.md → Inbound Job Filters` fields this skill reads:**
- **Markets** — which of Singapore / Indonesia / Malaysia / Thailand / Australia / Global-Remote to scan
- **Platforms** — the marketplaces to search, each flagged **have account** or **no account** (drives the access method in Step 3)
- **Search Keywords** (optional) — explicit terms; if absent, derive from `product.md`
- **Budget Floor** — minimum acceptable budget / rate (optional)
- **Exclusions** — keywords, client types, or geographies to skip
- **Daily Cap** — max opportunities to add per day

If `sales.md` is missing **or** has no `## Inbound Job Filters` section, abort with a `failed` log and a Slack message to `$SLACK_NOTIFY_USER` asking the user to run `/link-skills:brand-setup` (or `/link-skills:plugin-update`) to configure inbound job discovery. Do not invent markets, platforms, or keywords.

### Step 2: Ensure `${BRAND}_GIGS_DB` exists (first-run bootstrap)

Same DB-bootstrap pattern as `apollo-lead-prospector` Step 6a. Read `${BRAND}_GIGS_DB` from `.claude/settings.local.json`.

```
IF env var set: notion-fetch → if it resolves, the DB exists → skip to Step 3.
   (only create if the fetch returns not_found, meaning the DB was deleted)
IF unset (or not_found): first-ever run → create it (below), persist the new ID, notify once.
```

**Resolve the brand parent page** (`notion-search` for `"{Brand Name}"`; create a parent page at workspace root if none), then create:

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<resolved brand parent page id>" }
- title: "{Brand Name} Opportunities"
- properties: {
    "Name":          { "title": {} },                     // job title
    "Platform":      { "select": { "options": [] } },      // Upwork / Freelancer / Airtasker / Fastwork / ...
    "Market":        { "select": { "options": [
                        {"name":"Singapore"}, {"name":"Indonesia"}, {"name":"Malaysia"},
                        {"name":"Thailand"}, {"name":"Australia"}, {"name":"Global-Remote"}
                      ] } },
    "URL":           { "url": {} },
    "Job UID":       { "rich_text": {} },
    "Posted":        { "date": {} },
    "Posted Text":   { "rich_text": {} },
    "Budget":        { "rich_text": {} },
    "Budget Type":   { "select": { "options": [ {"name":"Hourly"}, {"name":"Fixed"}, {"name":"Unknown"} ] } },
    "Client":        { "rich_text": {} },                  // location · verification · spend/hire signals
    "Fit Score":     { "number": { "format": "number" } },
    "Service Match": { "select": { "options": [ {"name":"Strong"}, {"name":"Partial"}, {"name":"Weak"} ] } },
    "Source Date":   { "date": {} },
    "Status":        { "select": { "options": [
                        {"name":"New"}, {"name":"Reviewing"},
                        {"name":"Drafted"}, {"name":"Workflow Built"}, {"name":"Demo Ready"}, {"name":"Ready to Submit"},
                        {"name":"Proposed"}, {"name":"Won"}, {"name":"Lost"}, {"name":"Skipped"}, {"name":"Disqualified"}
                      ] } }
  }
```

After creation, **persist the new DB ID to `.claude/settings.local.json`** under `env.{BRAND}_GIGS_DB` (read existing settings, add the key, preserve all others, write back). Notify the user once:

> Created new Notion DB **{Brand Name} Opportunities** and saved its ID as `${BRAND}_GIGS_DB`. Future gig-discovery runs (and `proposal-generator`) reuse this DB — no re-creation.

### Step 3: Scan each chosen platform × market

Iterate the platforms listed in `sales.md → Inbound Job Filters`, scoped to the chosen Markets. The **access method** depends on the platform and whether the brand has an account:

**Platform reference (access method per platform).** Use this to choose how to reach each one; the *which* platforms to scan comes from `sales.md`, not from this table. **Recommended daily scan order:** Upwork → Freelancer.com → Projects.co.id → Sribu → Fastwork → Freelancing.my (then any extras the brand added).

| Platform | Markets | Access method | Login? |
|---|---|---|---|
| Upwork | Global-Remote | Claude in Chrome (Cloudflare-protected; real browser required) | yes |
| Freelancer.com (`.com`, `.sg`, `.com.au`, `.co.id`) | Global + SG/MY/ID/AU | **Freelancer.com API** if `FREELANCER_OAUTH_TOKEN` set; else Claude in Chrome | API: token · Chrome: optional |
| Projects.co.id | Indonesia | Claude in Chrome | optional |
| Sribu / Sribulancer | Indonesia | Claude in Chrome | optional |
| Fastwork | Thailand, Indonesia (+Vietnam) | Claude in Chrome | optional |
| Freelancing.my | Malaysia | Claude in Chrome | optional |
| PeoplePerHour | Global-Remote | Claude in Chrome (secondary global source) | optional |
| Jobbers.io | Singapore, Malaysia, SEA | Claude in Chrome (lower-confidence source) | optional |
| Airtasker | Australia | Claude in Chrome — **task/services-oriented; low yield for tech/automation work** (Freelancer.com covers AU project work better) | optional |

**Singapore note:** there is no strong SG-specific project marketplace — SG demand surfaces on the global platforms (Freelancer.com / Upwork / PeoplePerHour). Don't expect a dedicated SG source.

For any platform not in this table that the user added in `sales.md`, default to Claude in Chrome and build the search URL from the platform's public job-search page. Skip listing-only / gig-catalog sites (e.g. Fiverr) and pure employment boards (JobStreet, Indeed) — they aren't client-posts-a-project marketplaces and don't fit this workflow.

**3a — Freelancer.com via API (preferred when token is set).** If `FREELANCER_OAUTH_TOKEN` is set, query the active-projects endpoint instead of scraping — deterministic and Cloudflare-free:

```bash
curl -s "https://www.freelancer.com/api/projects/0.1/projects/active/?query=<keyword>&limit=50&job_details=true&full_description=true" \
  -H "freelancer-oauth-v1: $FREELANCER_OAUTH_TOKEN"
```

Run one query per derived Search Keyword; map `seo_url` → job URL, `id` → Job UID, `title`, `budget`, `submitdate` (epoch → ISO), `preview_description`. If the token is absent or the call errors, fall back to Claude in Chrome for Freelancer.com.

**3b — Claude in Chrome scrape (primary for everything else).** Requires the Chrome MCP tools (`mcp__Claude_in_Chrome__*`). For each platform × applicable market:

1. **Navigate** to the platform's job-search URL with the keyword + market/recency filters applied (e.g. Upwork `…/nx/search/jobs/?q=<keyword>&sort=recency`; Airtasker the AU jobs feed; Freelancer the localized domain). Build the keyword from the Step 1 derived terms.
2. If a login wall or CAPTCHA appears, **pause and ask the user to sign in** in the open Chrome window, then continue (the extension cannot complete logins). This mirrors `trend-radar` Step 2c's manual-login rule.
3. Use `mcp__Claude_in_Chrome__get_page_text` / `mcp__Claude_in_Chrome__read_page` to read the rendered results. **Read the page semantically — extract per job:** title, job URL, job UID (from the URL), posted-relative text, budget + budget type, and the client/qualification block (location, payment-verified badge, spend/hire history, rating) when present.
4. Convert posted-relative text ("Posted 5 hours ago", "yesterday") to an ISO timestamp. Results are recency-sorted, so once a job is older than the freshness window, stop paginating that platform.
5. Collect into a candidate list, tagging each with `Platform` and `Market`.

Over-fetch by ~2× the Daily Cap across platforms to give scoring + dedup room to drop weak matches.

**Fallback — if Chrome MCP is unavailable** (tools not connected): scan only the API-backed source (Freelancer.com, if its token is set) and use `WebSearch` to surface public job posts for the derived keywords + markets. Log a warning: "Chrome MCP not available — scraped only API + web-research sources; Cloudflare-protected platforms (Upwork, Airtasker) skipped this run." Never abort the whole run for a missing Chrome MCP.

### Step 4: Deduplicate, disqualify, and score

**Dedupe against `${BRAND}_GIGS_DB`.** Resolve the DB to a `data_source_url` (`notion-fetch` → `data_sources[0].url`). For each candidate, search by **Job UID first, then job URL** (sequential — short-circuit on first hit):

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<job_uid>"          (then "<job_url>" if zero results)
- data_source_url: <gigs_data_source_url>
- query_type: "internal"
```

If either search returns a match, mark `duplicate` and drop it. Track the duplicate count.

**Disqualify** using `sales.md → Inbound Job Filters → Exclusions`, dropping at the first match and logging the reason. Standard rules to enforce regardless:
- **Stale** — posted older than the freshness window (default 48h, measured from the run time); drop and log the age
- **Below budget floor** — budget/rate under the `Budget Floor`
- **Excluded keyword/geo** — title/description matches an exclusion term, or market not in the chosen list
- **Service mismatch** — the job doesn't actually ask for any service the brand sells (the next score makes this precise)

**Compute a Job-Fit Score (0–100)** for survivors as the weighted sum:

| Signal | Weight | Logic |
|---|---|---|
| Service match | 45 | Job names a service the brand sells (Step 1 terms): exact = 45; adjacent/related service = 25; weak/tangential = 10 |
| Budget fit | 20 | At/above floor & preferred type = 20; above floor = 15; unstated = 10; below floor = 0 (already disqualified) |
| Client quality | 20 | Payment-verified + spend/hire history + good rating = 20; partial signals = 10; brand-new/unverified = 5; unknown = 10 (neutral) |
| Freshness | 15 | ≤6h = 15; ≤24h = 12; ≤48h = 8 (older already disqualified) |

Set `Service Match` = Strong (service ≥ 35) / Partial (20–34) / Weak (< 20). Round the score, sort survivors descending, take the top `Daily Cap`.

### Step 5: Create Notion opportunity rows

For each surviving, non-duplicate candidate (Status `New`):

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_GIGS_DB" }
- pages: [{
    "properties": {
      "Name":          "<job title>",
      "Platform":      "<platform>",
      "Market":        "<market>",
      "URL":           "<job url>",
      "Job UID":       "<uid>",
      "Posted":        "<YYYY-MM-DD or ISO>",
      "Posted Text":   "<relative text>",
      "Budget":        "<budget string>",
      "Budget Type":   "Hourly | Fixed | Unknown",
      "Client":        "<location · verification · spend/hire signals>",
      "Fit Score":     <0-100>,
      "Service Match": "Strong | Partial | Weak",
      "Source Date":   "<YYYY-MM-DD>",
      "Status":        "New"
    },
    "content": "<short markdown — job description excerpt, which brand service(s) it maps to and why it scored as it did, plus any client metadata observed>"
  }]
```

Capture each new page URL. These rows are what `proposal-generator` and the founder's review pull from — **do not** auto-draft proposals here.

### Step 6: Save local backup

Save the day's batch as `outputs/{brand}/sales/gigs/Opportunities_DDMonYYYY.md`.

### Step 7: Send Slack digest to founder

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the deferred tool schema** — otherwise the task hangs.

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "<digest below>"
```

Digest format:

```
💼 [{brand}] Daily Gigs — [DD Mon YYYY]
• {N} added (cap {cap}) across {platform count} platforms / {market count} markets
• {D} duplicates skipped · {X} disqualified ({reason breakdown})
• Avg fit: {avg}/100 (top: {top_score})

Top 5 by fit:
1. {Title} — {Platform}/{Market} · {Budget} · {score}/100 — {url}
2. ...

Sources this run: {platforms scanned} {⚠ note any skipped for login/Cloudflare/Chrome-MCP-absent}
Opportunities DB: {notion_db_url}
```

Match the digest tone to the brand's voice from `brand.md`.

---

## Output format

**Save location:** `outputs/{brand}/sales/gigs/`
**Naming:** `Opportunities_[DDMonYYYY].md` (e.g. `Opportunities_20Jun2026.md`)

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: gig-prospector
Brand: {brand}
Markets: [...]
Platforms scanned: [...]
Daily Cap: {N}
Added: {M}
Disqualified: {D}
Duplicates: {X}
Avg Fit Score: {avg}
---
```

**Output sections:**
1. **Run Summary** — markets, platforms scanned (+ any skipped & why), cap, added, disqualified, duplicates, avg/top score
2. **Opportunity Roster** — table: Title, Platform, Market, Budget, Service Match, Fit Score, Notion URL
3. **Disqualifications** — table: Title, Platform, Reason
4. **Source notes** — which platforms used Chrome vs API vs web-research; any login/Cloudflare/CAPTCHA pauses

---

## Quality checklist

- [ ] Active brand resolved; `agents/link.md` + brand context read first
- [ ] Search terms **derived from `product.md` / `sales.md` Search Keywords — never hardcoded** (no default "automation")
- [ ] Markets + platforms read from `sales.md → Inbound Job Filters`; aborted cleanly with a Slack note if the section is absent
- [ ] `${BRAND}_GIGS_DB` exists (bootstrapped + ID persisted if first run)
- [ ] Freelancer.com used via API when `FREELANCER_OAUTH_TOKEN` is set; Chrome fallback otherwise
- [ ] Claude in Chrome used for Cloudflare-protected / login-walled platforms; login/CAPTCHA pauses handed to the user, not failed
- [ ] Chrome-MCP-absent fallback logged (API + web-research only; protected platforms skipped) — run never aborted
- [ ] Every candidate dedup-checked against `${BRAND}_GIGS_DB` by Job UID then URL
- [ ] Every disqualification maps to a documented exclusion or a standard rule
- [ ] Job-Fit score computed for every survivor using the 45/20/20/15 weighting; Daily Cap respected
- [ ] Every Notion row has Status="New", a Platform, a Market, and a non-empty Service Match
- [ ] No fabricated jobs, clients, budgets, or links — every record from a real post
- [ ] Local backup saved to `outputs/{brand}/sales/gigs/Opportunities_DDMonYYYY.md`
- [ ] Slack digest delivered to `$SLACK_NOTIFY_USER` with top 5, totals, source notes, and DB link
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "gig-prospector"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "markets": ["..."],
    "platforms_scanned": ["..."],
    "platforms_skipped": ["..."],
    "jobs_seen": 0,
    "jobs_added": 0,
    "jobs_disqualified": 0,
    "jobs_duplicate": 0,
    "daily_cap": 0,
    "avg_fit_score": 0,
    "top_fit_score": 0,
    "disqualification_breakdown": { "below_budget": 0, "excluded": 0, "service_mismatch": 0, "other": 0 },
    "source_methods": { "chrome": 0, "freelancer_api": 0, "web_research": 0 },
    "gigs_db_id": "${BRAND}_GIGS_DB",
    "output_path": "outputs/{brand}/sales/gigs/"
  }
```

---

## Part of the pipeline

The **Discover** phase of the **Inbound Gig Engine** — the inbound sales-acquisition entry point. Feeds reviewed opportunities into the bid flow:

```
gig-prospector (this skill → ${BRAND}_GIGS_DB, Status="New")
  → founder review (set Status="Reviewing")
  → gig-proposal-writer (cover letter + 60s VSL, Status="Drafted")
  → n8n-workflow-builder (real demo workflow + URL, Status="Workflow Built")
  → vsl-demo-producer (screenshot + recording script, Status="Demo Ready" → "Ready to Submit")
```

Run daily on cron.
