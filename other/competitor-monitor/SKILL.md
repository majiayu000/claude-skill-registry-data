---
name: competitor-monitor
description: Weekly diff of competitor websites, pricing pages, blogs, careers pages, and exec movements. Classifies and scores every change, archives to Notion, alerts Slack on high-signal events. Runs weekly on Monday morning cron schedule.
allowed-tools: Read, Grep, Glob, Bash
area: Strategy
use_for: "Weekly diff of competitor websites, pricing, blogs, careers. Alerts on price changes, exec moves, new features"
deps:
  mcp: ["Notion", "Slack"]
  gateway: []
  files: ["competitors.md (with v2.4.0 extension fields: `monitor_urls`, `track_pages`, `exec_team`)", "brand.md"]
  env: ["`${BRAND}_COMPETITOR_DB` (auto-bootstraps)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.4.0 | May 07, 2026 |

**Description:** Weekly diff of competitor websites, pricing pages, blogs, careers pages, and exec movements. Classifies and scores every change, archives to Notion, alerts Slack on high-signal events.

### Change Log

**v2.4.0** — May 07, 2026
- Initial production release as part of the v2.4.0 business-operations expansion.

# SKILL.md — Competitor Monitor

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a strategic intelligence analyst for the active brand. Your job is to monitor every competitor listed in `brands/{brand}/competitors.md` on a weekly cadence, fetch their public surfaces (homepage, pricing, blog, careers, changelog, exec LinkedIns), diff against last week's snapshot, classify every meaningful change, score it for novelty, archive it to Notion, and alert the founder on high-signal events. You never invent changes, never inflate signal — every entry is grounded in fetched HTML or a verified WebSearch result with a citable URL. Voice and signal-threshold rules come from `brands/{brand}/competitors.md`; this skill is content-free.

---

## When to use

Use this skill when the task involves:
- The weekly cron-triggered scan (default mode — runs Monday morning for the prior 7 days)
- Backfilling a missed week after a connector outage
- Re-running after `brands/{brand}/competitors.md` adds a new competitor or new monitor URL
- Producing an ad-hoc deep scan before a board meeting or product launch

Do NOT use this skill for:
- Writing counter-positioning briefs → use `research-strategy`
- Building a competitor-feature comparison page → use `content-creation`
- Pricing-strategy recommendations → use `research-strategy`
- Keyword / SEO analysis on competitor domains → use `research-strategy` + DataforSEO

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Scan window | Optional | Default: previous 7 days (Mon→Sun). Accepts custom ISO range |
| Competitor focus | Optional | Default: all competitors in `competitors.md`. Accepts a subset list |
| Recipient channel | Optional | Default: `$SLACK_NOTIFY_USER` |

---

## Step-by-step workflow

### Step 1: Read brand context

Always read before starting:
- **brands/{brand}/brand.md** — Locale (drives WebSearch region/language), voice for the digest tone
- **brands/{brand}/competitors.md** — Competitor roster + per-competitor monitoring config (the operational config for this skill)

**Expected `competitors.md` extension this skill reads (per competitor):**
- **`monitor_urls`** — list of URLs to diff weekly. Standard set: homepage, pricing page, blog index, careers page, changelog/changelog.md, product/features page
- **`track_pages`** — per-URL focus rules describing what to look for on each page. Examples: `pricing → "price changes, new tiers, removed tiers, plan rename"`; `careers → "exec roles, role count delta, layoffs language"`; `blog → "new product launches, customer stories, exec posts"`; `changelog → "any new entry"`
- **`exec_team`** — list of LinkedIn URLs for key execs to watch (CEO, CRO, CPO, CMO, Head of Eng). Used for exec-movement detection
- **`signal_thresholds`** *(optional)* — per-classification override on what counts as "high signal" worth a per-event Slack alert. Defaults are in Step 4 below if absent

If `competitors.md` is missing the extended fields, run a degraded mode: scan only the homepage of each competitor, skip exec scanning, and log a warning to Slack asking the user to run `/link-skills:brand-setup` to extend the file.

### Step 2: Resolve the scan window and load last week's snapshot

Set `scan_start = today - 7 days` and `scan_end = today` unless a custom window was provided. Capture `week_label` as `YYYY-WW` (ISO week, e.g. `2026-W19`).

Resolve the brand's competitor changelog DB to a `data_source_url`.

**Decision:**

IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → proceed.
  (only create if fetch returns 404 / not_found)

IF env var is NOT set:
  → first run for this brand → skip fetch and proceed to Step 5a (create competitor DB).

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_COMPETITOR_DB"
```

On a successful fetch, extract the `collection://` URL from `data_sources[0].url` and save as `competitor_data_source_url` for the dedupe and snapshot lookups in Step 3. If the env var is unset, defer the DB creation to Step 5a and skip the snapshot lookups for this run (every URL becomes a baseline scrape).

For each competitor + monitor URL pair, query Notion for the most recent snapshot:

```
Use mcp__claude_ai_Notion__notion-search:
- query: "<competitor> <url_label>"
- data_source_url: <competitor_data_source_url>
- query_type: "internal"
```

Sort returned pages by `Captured` desc and grab the first as `prior_snapshot` for diffing. If none exist, this URL has no baseline — record the first scrape as the baseline and skip diff classification for it this week.

### Step 3: Fetch and diff every monitor URL

For each competitor in scope, walk the `monitor_urls` list:

```
Use WebFetch:
- url: "<monitor_url>"
- prompt: "Extract: page title, h1, all visible text content sectioned by heading. Then summarise: any prices visible, any product names visible, any new/removed sections vs a typical SaaS site, any 'announcement' or 'new' badges, and any executive name + title pairs visible. Return as structured markdown."
```

WebFetch already de-duplicates and cleans HTML; we ask it for a structured extract rather than raw HTML so the diff is semantic, not whitespace-noise.

For each URL pair (prior_snapshot vs current_fetch):
1. Compute a semantic diff focused on the `track_pages` rules for this URL — ignore noise (footer timestamp drift, A/B-test copy variants, tracking-pixel changes)
2. Run each diff hunk through the **classification rubric** (Step 4) to assign a category and a novelty score
3. Discard hunks classified as `noise` (score < 20)
4. For surviving hunks, build a change record: `{competitor, url, category, summary, evidence_quote, prior_quote, novelty_score, captured_at}`

For **exec LinkedIns** in `exec_team`:

```
Use WebFetch:
- url: "<linkedin_url>"
- prompt: "Extract current job title, current company, start date of current role, and any 'started a new position' update visible in the past 7 days. Return as structured markdown."
```

If a `started new role` event lands inside the scan window, classify as `exec_hire` (if joining the competitor) or `exec_departure` (if leaving). LinkedIn often blocks unauthenticated WebFetch — when it does, fall back to the WebSearch supplement in Step 3b for that exec and log the connector failure (do not block the run).

#### Step 3b: WebSearch supplementary scans

For each competitor, run targeted web searches scoped to the last 7 days to catch things that don't show up on monitored pages (funding announcements, layoff coverage, acquisition rumours, exec departures covered by press):

```
Use WebSearch:
- query: "{competitor} layoff OR layoffs OR \"workforce reduction\" past 7 days"
```

```
Use WebSearch:
- query: "{competitor} funding OR raise OR \"Series\" past 7 days"
```

```
Use WebSearch:
- query: "{competitor} acquisition OR acquired OR \"acquires\" past 7 days"
```

```
Use WebSearch:
- query: "{competitor} CEO OR CRO OR CPO OR CMO new hire OR departure past 7 days"
```

For each result with a publication date inside the scan window, build a change record with `source: "websearch"` and the result URL as `evidence_url`. Drop results older than the window or where the date is unparseable.

### Step 4: Classify, score, and dedupe every change

**Classification categories** (each change must be exactly one):

| Category | Trigger |
|---|---|
| `price_change` | Any visible price, plan name, or tier on the pricing page changed |
| `new_feature` | New feature copy, new product launch, new section on homepage/features/changelog |
| `exec_hire` | New exec joined competitor (visible on careers page, LinkedIn, or press) |
| `exec_departure` | Exec left competitor (LinkedIn role end, press coverage, careers page removal) |
| `layoff_signal` | Layoff press coverage, careers headcount drop > 10%, "restructuring" language |
| `launch` | Public product launch — TechCrunch / blog / changelog announcement during window |
| `pivot` | Significant repositioning — homepage hero copy fundamentally changed, ICP shift visible |
| `funding` | Funding round announcement covered by press during window |
| `acquisition` | Acquired-by or acquired-of event during window |
| `noise` | Cosmetic / copy-tweak / A-B variant — discarded, not archived |

**Novelty score (0–100)** — weighted sum:

| Signal | Weight | Logic |
|---|---|---|
| Recency | 30 | Inside scan window = 30; older = 0 (auto-discarded) |
| Magnitude | 30 | Major (price ±10%+, exec at C-level, public launch) = 30; minor (single tier rename, IC-level hire, blog post) = 15; cosmetic = 0 |
| Strategic relevance to brand | 25 | Touches the brand's positioning angles per `brands/{brand}/competitors.md` messaging gaps = 25; tangential = 12; unrelated = 0 |
| Source confidence | 15 | Direct fetch with quote = 15; press coverage = 12; LinkedIn unverified = 8; rumour / single-source social = 4 |

Round to integer. Sort all surviving changes by novelty score descending.

**Per-change Slack alert threshold**: novelty score ≥ 70 OR category ∈ {`price_change`, `exec_departure` (C-level), `launch`, `funding`, `acquisition`, `layoff_signal`}. These get an immediate per-event Slack alert in addition to the weekly digest. Override per-category thresholds via `competitors.md` → `signal_thresholds` if present.

**Dedupe**: before archiving, search the Notion DB for any record matching `{competitor, category, week_label}`. If a same-category record exists for this competitor in the same week with overlapping evidence, merge into the existing record rather than creating a duplicate.

### Step 5: Archive to Notion `${BRAND}_COMPETITOR_DB`

#### Step 5a: First-run only — create `${BRAND}_COMPETITOR_DB` if missing

This step runs only when the env var is unset (first-ever competitor scan for the brand). On subsequent runs the DB exists — skip to Step 5b.

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to 5b.
  (only create if fetch returns 404 / not_found)

IF env var is NOT set:
  → first-ever run for this brand → create the DB below.
```

```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page>" }
- title: "{Brand Name} Competitor Intelligence"
- properties: {
    "Name":          { "title": {} },
    "Competitor":    { "select": { "options": [] } },
    "Category":      { "select": { "options": [
                        {"name": "price_change"},
                        {"name": "new_feature"},
                        {"name": "exec_hire"},
                        {"name": "exec_departure"},
                        {"name": "layoff_signal"},
                        {"name": "launch"},
                        {"name": "pivot"},
                        {"name": "funding"},
                        {"name": "acquisition"},
                        {"name": "snapshot"}
                      ] } },
    "URL":           { "url": {} },
    "Source":        { "select": { "options": [
                        {"name": "webfetch"},
                        {"name": "websearch"},
                        {"name": "linkedin"}
                      ] } },
    "Week":          { "rich_text": {} },
    "Captured":      { "date": {} },
    "Novelty Score": { "number": { "format": "number" } },
    "Severity":      { "select": { "options": [
                        {"name": "low"},
                        {"name": "medium"},
                        {"name": "high"}
                      ] } },
    "Summary":       { "rich_text": {} },
    "Evidence URL":  { "url": {} },
    "Created":       { "created_time": {} }
  }
```

If no brand parent page exists yet, `notion-search` for `"{Brand}"`; if nothing is found, create a parent page with `notion-create-pages` titled `"{Brand Name}"` at the workspace root, then nest the DB under it.

After creation, persist the new DB ID to `.claude/settings.local.json` under `env.{BRAND}_COMPETITOR_DB`. Read existing settings, add the key (preserve all other keys), write back. Notify the user in chat once:

> Created new Notion DB **{Brand Name} Competitor Intelligence** and saved its ID as `${BRAND}_COMPETITOR_DB` in `.claude/settings.local.json`. Future weekly competitor scans will reuse this DB.

#### Step 5b: Create one Notion row per surviving change

```
Use mcp__claude_ai_Notion__notion-create-pages:
- parent: { "database_id": "${BRAND}_COMPETITOR_DB" }
- pages: [{
    "properties": {
      "Name":          "<competitor> — <category> — <DD Mon YYYY>",
      "Competitor":    "<competitor>",
      "Category":      "<category>",
      "URL":           "<monitor_url>",
      "Source":        "<webfetch|websearch|linkedin>",
      "Week":          "<YYYY-WW>",
      "Captured":      "<YYYY-MM-DD>",
      "Novelty Score": <0-100>,
      "Severity":      "<low|medium|high>",
      "Summary":       "<1 sentence change summary>",
      "Evidence URL":  "<source url>"
    },
    "content": "<markdown — full change record: prior_quote (if any), current_quote, diff explanation, why this matters to {brand} per competitors.md positioning>"
  }]
```

Also archive a per-URL **`snapshot`** row (category=`snapshot`) for every monitored URL fetched this week, with the cleaned content body in `content`. This is the baseline future weeks will diff against — without it, the next run has nothing to compare to.

#### Step 5c: Update `brands/{brand}/competitors.md` with a recent-changes log

Append (idempotent) a dated subhead under a `## History` section at the bottom of `brands/{brand}/competitors.md`. Read the existing file, find or create the `## History` heading, append a new `### Week of YYYY-WW` subhead with a compact bullet list of every change with novelty ≥ 50. Preserve all prior entries — never rewrite or reorder them.

Bullet format:
```
- **[{Competitor}]** {category} — {1-line summary} (novelty {score}, [evidence]({evidence_url}))
```

This keeps competitors.md as a living strategic doc that the founder and `research-strategy` skill can read for context without opening Notion.

### Step 6: Save local backup

Save the week's full scan as a local audit file:

```
outputs/{brand}/strategy/CompetitorScan_{YYYY-WW}.md
```

This includes the full WebFetch extracts, all WebSearch results, the classification + scoring trace, and the final change list. Useful for audit and for re-running the classifier if scoring rules change.

### Step 7: Send Slack — weekly digest + per-event alerts

DM the user via Slack MCP. There are two Slack messages per run: per-event alerts (only for high-signal items, posted in real-time as the run proceeds), then a single weekly digest at the end.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

#### Step 7a: Per-event high-signal alerts

For each change passing the per-event threshold (Step 4), send a focused alert:

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "<recipient channel — default $SLACK_NOTIFY_USER>"
- text: "<alert below>"
```

Alert format:
```
🚨 [{brand}] Competitor signal — {Competitor}
Category: {category} (novelty {score}/100)
{1-2 line summary}

Quote: "{evidence_quote — verbatim, ≤160 chars}"
Source: {evidence_url}
Notion: {notion_page_url}
```

#### Step 7b: Weekly digest (single message at end of run)

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "<recipient channel — default $SLACK_NOTIFY_USER>"
- text: "<digest below>"
```

Digest format:

```
🗞 [{brand}] Weekly Competitor Scan — Week of {DD Mon YYYY}

Scanned: {N} competitors / {M} URLs
Changes captured: {C} (high-signal: {H})

By competitor (top 3 changes each, or "No changes" if none):

▸ {Competitor 1}
  • {category} — {summary} (novelty {score})
  • ...

▸ {Competitor 2}
  • No meaningful changes this week

▸ {Competitor 3}
  • {category} — {summary} (novelty {score})
  • ...

High-signal alerts sent this week: {H}
Notion archive: {notion_db_url}
Local snapshot: outputs/{brand}/strategy/CompetitorScan_{YYYY-WW}.md
```

Match the digest tone to the brand's voice from `brand.md` — terser for ops-heavy brands, slightly warmer for founder-led brands. Never editorialise on what a change *means* in the digest body — leave interpretation to `research-strategy`.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/strategy/
```

**Naming convention:**
```
CompetitorScan_[YYYY-WW].md
```

Examples:
- `CompetitorScan_2026-W19.md`
- `CompetitorScan_2026-W20.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: competitor-monitor
Brand: {brand}
Week: YYYY-WW
Scan Start: YYYY-MM-DD
Scan End: YYYY-MM-DD
Competitors Scanned: {N}
URLs Fetched: {M}
Changes Captured: {C}
High-Signal Alerts: {H}
Status: Final
---
```

**Output sections:**
1. **Run Summary** — competitors scanned, URLs fetched, changes captured, high-signal count
2. **Per-Competitor Changes** — one section per competitor with all surviving changes, sorted by novelty desc
3. **Cross-Competitor Themes** — patterns observed across the roster (e.g. "3 of 5 competitors raised prices this week")
4. **Source Trace** — every URL fetched + every WebSearch query + each result's classification verdict (audit trail)
5. **Snapshot Index** — list of `snapshot` Notion page URLs created this week, by competitor + URL

---

## Quality checklist

Before finalizing any weekly scan:

- [ ] Every competitor in `brands/{brand}/competitors.md` was scanned, or its absence is explicitly noted with a connector-failure reason
- [ ] Every `monitor_urls` entry per competitor was fetched (or logged as a fetch failure)
- [ ] Every change is classified into exactly one category and carries a novelty score with a documented rationale
- [ ] No invented changes — every entry has either a `webfetch` evidence_quote, a `websearch` evidence_url, or a `linkedin` evidence_url, all dated inside the scan window
- [ ] Dedup pass run before archiving — no duplicate `{competitor, category, week_label}` rows in Notion
- [ ] Every change with novelty ≥ 70 (or matching the per-event category list) triggered a real-time Slack alert
- [ ] `snapshot` rows created for every fetched URL — next week's diff has a baseline
- [ ] `brands/{brand}/competitors.md` `## History` section appended idempotently — prior weeks preserved, new week dated subhead added
- [ ] Local backup saved to `outputs/{brand}/strategy/CompetitorScan_{YYYY-WW}.md` with full source trace
- [ ] Weekly digest delivered to `$SLACK_NOTIFY_USER` with per-competitor sections (or "No changes") and aggregate counts
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "competitor-monitor"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "week": "YYYY-WW",
    "scan_start": "YYYY-MM-DD",
    "scan_end": "YYYY-MM-DD",
    "competitors_scanned": 0,
    "urls_fetched": 0,
    "fetch_failures": 0,
    "changes_captured": 0,
    "changes_discarded_noise": 0,
    "high_signal_alerts": 0,
    "category_breakdown": {
      "price_change": 0,
      "new_feature": 0,
      "exec_hire": 0,
      "exec_departure": 0,
      "layoff_signal": 0,
      "launch": 0,
      "pivot": 0,
      "funding": 0,
      "acquisition": 0
    },
    "per_competitor": [{ "competitor": "...", "changes": 0, "high_signal": 0, "top_category": "..." }],
    "cross_competitor_themes": ["..."],
    "competitor_db_id": "${BRAND}_COMPETITOR_DB",
    "output_path": "outputs/{brand}/strategy/"
  }
```
