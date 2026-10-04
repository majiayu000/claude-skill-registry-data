---
name: traffic-reporter
description: Report the brand's organic performance from fb.ai — Search Console clicks/impressions/positions plus AI-engine visibility (whether ChatGPT, Perplexity and friends cite the brand). All traffic-monitor tools are free, so there is no quota gate. Run weekly or monthly.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Report the brand's organic search traffic and AI-engine visibility trends from fb.ai"
deps:
  mcp: []
  gateway: ["fivebucks (**scope: traffic_monitor**)", "FiveAgents (logging)"]
  files: ["brand.md"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Report the brand's organic performance from fb.ai — Search Console metrics plus AI-engine (GEO) visibility.

### Change Log

**v2.20.0** — July 12, 2026
- Initial release. Drives fb.ai's `traffic_monitor` scope (gateway v1.8.0) — every tool it uses is free.

# SKILL.md — Traffic Reporter

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You report how the brand is actually being found — in Google, and increasingly in AI answers.

You are rigorous about **the difference between "zero" and "no data."** A page with no Search Console rows because GSC was never connected is not a page with zero clicks. Reporting the second as the first is the single worst thing this skill can do, and it is easy to do by accident. When data is missing, you say the data is missing.

Every tool here is **free**. No quota gate, no pre-flight pricing — this is the one fb.ai skill you can run as often as you like.

---

## When to use

Use this skill when the task involves:
- A weekly or monthly organic performance report
- Checking whether the brand is being cited by AI engines (ChatGPT, Perplexity, etc.)
- Seeing which pages are gaining or losing search position
- Setting up or adjusting which pages and GEO prompts are tracked

Do NOT use this skill for:
- Paid-ads performance → use `digital-marketing-analyst`
- Fixing the SEO problems behind bad numbers → use `site-auditor`
- Finding new keywords/topics to target → use `seo-researcher`
- Social engagement metrics → use `content-performance-analyst`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Domain | Yes | From `brands/{brand}/brand.md` |
| Reporting period | Optional | Default: since the last report in `outputs/{brand}/marketing/traffic/` |
| GSC property URL | Only to refresh | The exact Search Console property (e.g. `sc-domain:example.com`) |
| Refresh first? | Optional | Default yes — stale data makes a stale report |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/brand.md` for the domain.

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`traffic_monitor`** — that is the only scope this skill needs. An empty `scopes` array = legacy full-access key, which is fine.
- If it's missing → stop. Send the user to https://www.fivebucks.ai/dashboard/api-keys. Do not retry.
- **No quota check needed** — everything in this skill is free.

### Step 2: Make sure something is being tracked

An empty report usually means nothing was ever tracked, not that traffic is zero.

```
Use gateway MCP tool `fivebucks_traffic_summary`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

If it's empty, seed tracking. Two sources:

```
Use gateway MCP tool `fivebucks_discover_pages`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain: "<example.com>"
- limit: <1-100, default 50>
- locationCode: <DataForSEO location code, default 2702>
- languageCode: "<2-letter code, default en>"
```

```
Use gateway MCP tool `fivebucks_list_cms_pages`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- limit: <default 50>
```

Prune anything irrelevant (tag archives, paginated listings) with `fivebucks_untrack_items` — it takes an array of tracked-item ids and handles one or many.

### Step 3: Refresh the data

Both refreshes are **async** — poll them.

**Search Console:**
```
Use gateway MCP tool `fivebucks_refresh_gsc`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- siteUrl: "<the exact Search Console property URL>"
```
```
Use gateway MCP tool `fivebucks_gsc_refresh_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_refresh_gsc>"
```

**AI visibility:**
```
Use gateway MCP tool `fivebucks_refresh_ai_visibility`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain: "<optional domain filter>"
```
```
Use gateway MCP tool `fivebucks_ai_refresh_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_refresh_ai_visibility>"
```

⚠️ **Search Console must be connected by the user, in the dashboard.** GSC is OAuth-only — you cannot connect it with an API key. If the refresh fails or `fivebucks_gsc_data` comes back empty, the likely cause is that GSC was never connected. Send the user to https://www.fivebucks.ai/dashboard/integrations and **report the gap as a gap** — do not report the absence of data as zero traffic.

### Step 4: Read the numbers

```
Use gateway MCP tool `fivebucks_gsc_data`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain: "<optional filter>"
```

```
Use gateway MCP tool `fivebucks_ai_visibility`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- domain: "<optional filter>"
```

Compare against the previous report in `outputs/{brand}/marketing/traffic/` to get real deltas. Without a prior report, say this is the baseline — don't fabricate a trend from one data point.

### Step 5: GEO prompts — read before you write

The AI-visibility check asks the AI engines a set of questions ("GEO prompts") and looks for the brand in the answers. To see them:

```
Use gateway MCP tool `fivebucks_get_geo_settings`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

⚠️ **`fivebucks_set_geo_settings` REPLACES the whole config.** It does not merge. If you send only your new prompt, every existing prompt is deleted.

**Always `fivebucks_get_geo_settings` first, then send back the full list** — the existing prompts you want to keep (reusing their `id`s) plus your additions:

```
Use gateway MCP tool `fivebucks_set_geo_settings`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- prompts: [
    { "id": "<existing id — reuse it>", "question": "<existing question, unchanged>", "priority": 1 },
    { "id": "<new id>", "question": "<the new question>", "priority": 2 }
  ]
```

Show the user the final list and get a yes before sending it. A destructive overwrite is not recoverable from here.

### Step 6: Write the report

Lead with what changed and what it means. Not a data dump — the user can read a table; what they need from you is which of these numbers matters.

For every metric, be explicit about its provenance: measured, or missing.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/marketing/traffic/
```

**Naming convention:**
```
TrafficReport_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: traffic-reporter
Brand: {brand}
Domain: {domain}
Period: {start} to {end}
GSC Connected: {yes|no}
Pages Tracked: {N}
Status: Final
---
```

**Output sections:**
1. **Headline** — one paragraph: is organic growing, flat, or falling, and why
2. **Search Console** — clicks, impressions, CTR, average position, with deltas vs the last report. Explicitly flag any metric that is **not connected** rather than showing 0
3. **Movers** — pages that gained or lost position, ranked by impact
4. **AI visibility (GEO)** — which engines cite the brand, for which prompts, and the trend. This is the metric most brands aren't watching yet — explain what it means
5. **Data gaps** — anything not measured, and what the user must connect to fix it
6. **Recommendations** — the two or three things worth doing, each pointing to the skill that does it (`site-auditor` for health issues, `seo-researcher` for coverage gaps, `article-publisher` to ship)

---

## Quality checklist

- [ ] `fivebucks_whoami` checked first; `traffic_monitor` scope confirmed
- [ ] No quota pre-flight performed — correctly recognized that every tool here is free
- [ ] Tracking verified/seeded before reporting — an empty report diagnosed, not published
- [ ] Both refreshes polled to completion (`fivebucks_gsc_refresh_status`, `fivebucks_ai_refresh_status`)
- [ ] **Missing GSC reported as "not connected", never as zero traffic**
- [ ] Deltas compared against the previous report; a first run labelled as a baseline, not a trend
- [ ] `fivebucks_get_geo_settings` read **before** any `fivebucks_set_geo_settings` — existing prompts preserved with their ids
- [ ] Any GEO overwrite shown to the user in full and confirmed before sending
- [ ] Every number traceable to an fb.ai response — no estimated or filled-in figures
- [ ] Recommendations route to the sibling skill that can act on them
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "traffic-reporter"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "domain": "...",
    "gsc_connected": true,
    "pages_tracked": 0,
    "clicks": 0,
    "impressions": 0,
    "ctr": 0.0,
    "avg_position": 0.0,
    "clicks_delta": 0,
    "impressions_delta": 0,
    "position_delta": 0.0,
    "pages_gained": 0,
    "pages_lost": 0,
    "geo_prompts_tracked": 0,
    "ai_engines_citing_brand": 0,
    "ai_visibility_score": 0.0,
    "data_gaps": 0,
    "output_path": "outputs/{brand}/marketing/traffic/"
  }
```
