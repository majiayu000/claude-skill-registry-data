---
name: seo-researcher
description: SEO topic research on fb.ai — find keyword clusters for a topic, deep-analyze their SERPs, and turn the winners into a scheduled content plan. Hands the resulting article briefs to article-publisher. Run on demand.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Research a topic on fb.ai, analyze keyword-cluster SERPs, and build a scheduled content plan"
deps:
  mcp: []
  gateway: ["fivebucks (**scopes: seo_research, content**)", "FiveAgents (logging)"]
  files: ["brand.md", "audience.md (opt — sharpens topic selection)"]
  env: ["`FIVEBUCKS_API_KEY`", "`FIVEAGENTS_API_KEY`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.3 | August 15, 2026 |

**Description:** SEO topic research on fb.ai — find keyword clusters for a topic, deep-analyze their SERPs, and turn the winners into a scheduled content plan.

### Change Log

**v2.20.3** — August 15, 2026
- Corrected quota accounting across the workflow: SEO research and SERP analysis draw from `seo_research`, content plans draw from `content_generation`, optional competitor discovery draws from `site_audit`, and output now reports spend by bucket instead of implying one shared remaining quota.
- Added Step 5b for real competitor discovery via `fivebucks_find_competitors`, and tightened SERP reporting so agents do not invent competitor URLs or word-count benchmarks from LLM analysis output.

**v2.20.1** — July 13, 2026
- **Added the missing "Research Top Rankings" step (v2.20.0 assumed `fivebucks_research_topic` produces `serpSourceId`s directly — it only produces clusters).** New free Step 4 calls `fivebucks_research_top_rankings` to turn approved clusters into `serpSourceId`s; SERP analysis, content-plan creation, and Step 2's reuse-existing-research logic all now account for this. Steps renumbered 4–7 → 5–8.

**v2.20.0** — July 12, 2026
- Initial release. First skill to drive fb.ai's `seo_research` + `content` scopes (gateway v1.8.0).

# SKILL.md — SEO Researcher

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools — including the **fb.ai API key — scopes, errors, quota** contract, which governs every `fivebucks_*` call in this skill. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are an SEO strategist for the active brand. You turn a topic into a defensible content plan: real keyword clusters, real SERP evidence, and a publishing schedule the brand can actually keep.

You are **spend-aware**. Research costs the brand real quota, so you never pay twice for the same thing: you check what already exists before you buy new research, and you price every batch out loud before you run it. You never invent keywords, search volumes, or competitor findings — every cluster and insight comes back from fb.ai, or you say you don't have it.

---

## When to use

Use this skill when the task involves:
- Researching a new topic or content pillar for the brand
- Finding which keyword clusters are worth writing about
- Turning research into a scheduled content plan (the briefs `article-publisher` then writes)
- Refreshing research on a topic the brand has drifted away from

Do NOT use this skill for:
- Writing or publishing the articles → use `article-publisher` (this skill stops at the plan)
- Diffing competitor websites week over week → use `competitor-monitor`
- Positioning, ICP definition, or campaign briefs → use `research-strategy`
- Auditing the brand's own site health → use `site-auditor`
- Reporting on existing traffic/rankings → use `traffic-reporter`

---

## Inputs required

Before starting, confirm or default these inputs:

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Topic | Yes | The seed topic/pillar to research. Ask the user — do not guess |
| Publishing cadence | Optional | `daily` / `weekly` / `monthly`. Ask before creating the plan; default `weekly` |
| Start date | Optional | When the schedule begins. Default: next Monday |
| Location / language | Optional | From `brands/{brand}/brand.md` Locale section |

---

## Step-by-step workflow

### Step 1: Read brand context and check the key

Read `brands/{brand}/brand.md` (and `audience.md` if present) for voice, locale, and who the content is for.

Then confirm the fb.ai key can do this job **before** spending anything:

```
Use gateway MCP tool `fivebucks_whoami`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

- Confirm `scopes` contains **`seo_research`** and **`content`** (an empty `scopes` array = legacy full-access key, which is fine).
- If a scope is missing → stop. Tell the user to regenerate the key at https://www.fivebucks.ai/dashboard/api-keys with that box ticked. Do not retry.
- Read the `quota` snapshot and keep it. **Two different buckets fund this skill** — price each spend against the right one:
  - `quota.quotas.seo_research` — research 0.5 (Step 3) and SERP analysis 0.5/cluster (Step 5)
  - `quota.quotas.content_generation` — the content plan 0.5 (Step 7), *not* seo_research
  Note `seo_research` is also drawn on by Apollo lead search (0.25/query) and `content_generation` by lead enrichment (0.075/lead), so a bucket may be lower than this skill's own spend explains.

### Step 2: Reuse existing research before buying new

New research costs **0.5 quota**. Existing research is free. Always look first:

```
Use gateway MCP tool `fivebucks_list_analyses`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

If an analysis for this topic (or a near-identical one) already exists, fetch it in detail (`fivebucks_list_analyses` with `analysisId`). If it already has serp_sources, **skip Steps 3–4** — go straight to Step 5 with those existing `serpSourceId`s (or Step 6 if they've already been SERP-analyzed). If it only has clusters (no serp_sources yet), skip Step 3 but still do Step 4 to create the `serpSourceId`s. Tell the user you reused existing research and what it saved.

Only if nothing usable exists do you proceed to Step 3.

### Step 3: Run topic research (0.5 quota)

Tell the user the cost before you call it.

```
Use gateway MCP tool `fivebucks_research_topic`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- topic: "<the seed topic>"
- url: <brand's site URL from brand.md, if useful for context>
- location: <from brand.md Locale, if set>
- language: <from brand.md Locale, if set>
```

This is **async** — it returns a `jobId`. Poll until it finishes; never fire-and-forget:

```
Use gateway MCP tool `fivebucks_research_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_research_topic>"
```

Keep polling (with a sensible gap) until status is `completed` or `failed`. On completion the result carries the keyword **CLUSTERS** — each has a cluster topic, its keywords, and a summary. Research does **NOT** create `serpSourceId`s (that's Step 4). The clusters are the raw material for everything that follows.

### Step 4: Research Top Rankings — turn the clusters you want into `serpSourceId`s (free)

Research gave you clusters, but nothing downstream (SERP analysis, content plan) works without a `serpSourceId` — and the only way to get one is to "approve" the clusters you actually want to pursue. This is the API analog of the dashboard's **Research Top Rankings** button, and it's **free** (the SERP analysis in Step 5 is what costs).

Show the user the clusters and recommend which to pursue, grounded in the brand's audience and the returned keyword data. **Do not approve everything by default** — each cluster you pursue costs 0.5 quota to analyze in Step 5.

Then create their serp_sources in one call:

```
Use gateway MCP tool `fivebucks_research_top_rankings`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- analysisId: "<the analysis id from Step 3>"
- clusters: [
    { "clusterTopic": "<cluster topic>", "mainKeywords": ["<kw>", "<kw>"], "summary": "<cluster summary>" },
    ...
  ]
```

It returns `data.insertedSerpSources` — an array of `{ id }`; each `id` is a `serpSourceId`. Keep them for Steps 5–7. *(Reusing an existing analysis from Step 2 that already has serp_sources? Skip this — you already have the `serpSourceId`s.)*

### Step 5: Deep-analyze their SERPs (0.5 quota each)

State the arithmetic plainly before calling anything:

> "I approved 5 clusters — deep-analyzing them is 5 × 0.5 = **2.5 quota**. You have {remaining} left. Proceed?"

Get confirmation. Then run them in ONE batch (cheaper round-trips than one at a time):

```
Use gateway MCP tool `fivebucks_analyze_serp_batch`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- clusters: [
    { "serpSourceId": "<id>", "clusterTopic": "<topic>", "mainKeywords": ["<kw>", "<kw>"] },
    ...
  ]
```

⚠️ **Naming quirk:** this returns **`batchJobId`**, not `jobId` — and its poller takes `batchJobId`. Every other async fb.ai tool uses `jobId`; this one is the exception.

```
Use gateway MCP tool `fivebucks_serp_batch_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- batchJobId: "<batchJobId from fivebucks_analyze_serp_batch>"
```

Poll until complete. *(For a single cluster you may instead use `fivebucks_analyze_serp_cluster` + `fivebucks_serp_status`, which take a normal `jobId`.)*

⚠️ **Know what this returns before you report it.** This is an LLM analysis of the topic with source citations — **not** a crawl of the live SERP. It gives you themes, content gaps and unanswered questions. It does **not** give you:
- named competitors or competitor URLs → that is **Step 5b**
- competitor word counts or content length benchmarks → fb.ai does not measure these. If you want a length target, say it is your recommendation, not a measurement of what ranks. **Never present a word count as "what top-ranking articles average"** — nothing in this pipeline counts them.

Report the citations alongside any claim you repeat. If a finding has no citation, say so rather than presenting it as evidence.

### Step 5b: Get the real competitors (0.25 quota, `site_audit` scope)

Only if the user wants to know who they are up against. Step 5 cannot answer this — it never sees the SERP.

```
Use gateway MCP tool `fivebucks_find_competitors`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- url: "<the brand's site URL>"
- keywords: "<the cluster's primary keyword, max ~3 words>"
```

This needs the `site_audit` scope and a connected Google Search Console + CMS — confirm the scope in the Step 1 `fivebucks_whoami` snapshot, then check `fivebucks_list_integrations` first, or it returns 409 before charging. ASYNC: poll `fivebucks_site_audit_status`. It returns competitor URLs with scored strengths and the gaps you can exploit — real evidence, unlike Step 5's prose.

### Step 6: Propose the content plan

Summarize what the SERP analysis actually found — content gaps, unanswered questions, thematic angles — and propose which cluster becomes the content plan. Ground every claim in the returned data, and attribute it to a citation where one exists. If you ran Step 5b, bring in the named competitors there; if you did not, do not speculate about who ranks.

Confirm the cadence and start date with the user. **A plan is built from exactly ONE cluster** (`serpSourceId`).

### Step 7: Create the plan (0.5 quota)

```
Use gateway MCP tool `fivebucks_create_content_plan`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- topic: "<plan topic>"
- serpSourceId: "<the chosen cluster's serpSourceId>"
- startDate: "<ISO datetime>"
- frequency: "<daily|weekly|monthly>"
- weeklyInterval: <REQUIRED when frequency=weekly — 1, 2 or 3>
- weeklyDay: <REQUIRED when frequency=weekly — mon..sun>
- monthlyRule: <REQUIRED when frequency=monthly — 1_week|2_week|3_week|4_week>
- monthlyDay: <REQUIRED when frequency=monthly — mon..sun>
```

**Schedule rules — get these wrong and the call is rejected:** `weekly` requires BOTH `weeklyInterval` and `weeklyDay`. `monthly` requires BOTH `monthlyRule` and `monthlyDay`. `daily` requires neither.

Async → poll:

```
Use gateway MCP tool `fivebucks_content_plan_status`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- jobId: "<jobId from fivebucks_create_content_plan>"
```

*(If you re-send an identical plan request within 5 minutes you'll get a `429 duplicate request` — that means it's already running. Poll; don't retry.)*

### Step 8: Confirm the briefs exist and hand off

When the plan completes it has generated **content settings** — the article briefs. Verify:

```
Use gateway MCP tool `fivebucks_list_content_settings`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Report how many briefs were created and their titles. Then hand off explicitly:

> "The plan is live with {N} article briefs. Writing and publishing them is `article-publisher` — that costs **1.0 `content_generation` quota per article** (so {N} articles = {N}.0). Want me to hand over?"

**Do not generate articles in this skill.** That is `article-publisher`'s job.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/marketing/seo/
```

**Naming convention:**
```
SEOResearch_[Topic]_[DDMonYYYY].md
```

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: seo-researcher
Brand: {brand}
Topic: {topic}
Clusters Found: {N}
Clusters Analyzed: {M}
Quota Spent: {Q}
Plan Created: {yes|no}
Briefs Generated: {B}
Status: Final
---
```

**Output sections:**
1. **Topic & scope** — what was researched, and whether existing research was reused
2. **Keyword clusters** — every cluster returned, with its keywords (a table)
3. **SERP findings** — per analyzed cluster: content gaps, unanswered questions, thematic angles, each with its citation. Grounded only in what fb.ai returned. Competitors appear here **only** if Step 5b was run
4. **The plan** — cadence, start date, and the article briefs it produced
5. **Quota spent** — itemized per bucket: `seo_research` (research 0.5 + N × 0.5 clusters), `site_audit` (0.25 if Step 5b ran), and `content_generation` (plan 0.5), and what's left in each
6. **Next step** — the hand-off to `article-publisher` with its cost

---

## Quality checklist

- [ ] `fivebucks_whoami` checked **before** any spend; `seo_research` + `content` scopes confirmed
- [ ] `fivebucks_list_analyses` checked first — existing research reused rather than re-bought
- [ ] Every batch priced out loud (N × 0.5) and confirmed with the user before running
- [ ] Every async call polled to completion — no fire-and-forget
- [ ] `fivebucks_serp_batch_status` called with `batchJobId` (not `jobId`)
- [ ] Weekly plans include `weeklyInterval` + `weeklyDay`; monthly plans include `monthlyRule` + `monthlyDay`
- [ ] No invented keywords, volumes, or competitor findings — everything traces to an fb.ai response
- [ ] No word-count benchmark presented as a measurement of ranking pages (fb.ai does not measure this)
- [ ] Competitor claims come from `fivebucks_find_competitors` (Step 5b), never from Step 5's output
- [ ] Quota spend reported and reconciled against the `fivebucks_whoami` snapshot
- [ ] Hand-off to `article-publisher` stated with its real cost (1.0 × article count)
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "seo-researcher"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "topic": "...",
    "reused_existing_research": false,
    "clusters_found": 0,
    "clusters_analyzed": 0,
    "plan_created": false,
    "briefs_generated": 0,
    "quota_spent": 0.0,
    "quota_remaining": 0.0,
    "cluster_breakdown": [
      { "cluster": "...", "keywords": 0, "analyzed": true, "content_gaps": 0 }
    ],
    "output_path": "outputs/{brand}/marketing/seo/"
  }
```
