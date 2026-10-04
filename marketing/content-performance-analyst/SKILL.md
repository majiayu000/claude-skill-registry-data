---
name: content-performance-analyst
description: Analyze organic content performance for any active brand — your own published posts (engagement by topic, format, persona, angle, hook archetype, Direction) plus competitor content benchmarking — and produce a Performance Brief that feeds the social calendar.
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Analyze organic content performance — own published posts (engagement by topic/format/persona/angle/hook/Direction, outlier scoring) plus competitor content benchmarking — into a Performance Brief that feeds social-calendar"
deps:
  mcp: ["Notion", "Slack", "Claude in Chrome (opt — primary engagement-metrics source; degrades to Zernio/web-research when absent)", "Zernio", "Zernio Analytics add-on"]
  gateway: ["FiveAgents (logging)"]
  files: ["brand.md", "audience.md", "competitors.md", "funnel.md (opt)"]
  env: ["`${BRAND}_NOTION_DB`", "`${BRAND}_PERFORMANCE_DB` (auto-bootstraps)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.19.0 | July 03, 2026 |

**Description:** Analyze organic content performance — own posts + competitor benchmarking — into a Performance Brief that feeds the social calendar.

### Change Log

**v2.19.0** — July 03, 2026
- **Corrected Zernio tool names + date params to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 assumed Zernio just drops the `late_` prefix, but Zernio's tools are resource-prefixed. Repointed the analytics fallback: `get_analytics` → **`analytics_get_analytics`** (per-post arg is `post_id`, not `postId`) and `get_follower_stats` → **`accounts_get_follower_stats`**. Date filters corrected from `date_from`/`date_to` to **`from_date`/`to_date`** (the wrong names silently returned empty). `accounts_list`/`posts_list` were already correct.

**v2.18.0** — July 01, 2026
- **Zernio migrated to its own MCP (gateway v1.7.4).** Repointed `late_list_accounts` → `accounts_list`, `late_list_posts` → `posts_list`, `late_get_post_analytics` → `get_analytics`, and `late_get_follower_stats` → `get_follower_stats` to Zernio's native MCP tool names; dropped the `fiveagents_api_key` param from those calls; renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*`.

**v1.0.4** — June 09, 2026
- Frontmatter deps corrected: `Claude in Chrome` added to `deps.mcp` (opt) — it has been the primary engagement-metrics source since v1.0.2 but was never declared, so the generated manifest/SKILLS.md omitted it. Degrades to Zernio/web-research when absent.

**v1.0.3** — June 09, 2026
- Step 3: completeness is now mandatory — all competitors in `competitors.md` must be processed; partial runs must be flagged. `${BRAND}_PERFORMANCE_DB` competitor coverage is a hard dependency for `trend-radar` Step 2b.

**v1.0.2** — June 09, 2026
- Step 0: Primary engagement source for all rows (own + competitors) switched to **Claude in Chrome**; Zernio retained as fallback for own posts; web-research retained as fallback for competitors. Added `Source = "chrome-browser"`.
- Step 1: DB schema updated to match actual Notion columns — Platform adds Twitter/TikTok/YouTube (Facebook removed); Format adds Reel/Video; Source adds "chrome-browser"; "Impressions" renamed to "Impressions / Views"; "Engagement Rate" number field added.
- Step 2: Claude in Chrome primary added before Zernio fallback; field mapping updated for "Impressions / Views" and "Engagement Rate"; upsert Source set dynamically.
- Step 3: Claude in Chrome primary added before web-research fallback; Source tagging updated.
- Analytics Field Rules section added: per-platform required/optional/na field table, platform-specific Engagement formulas, Engagement Rate formula, YouTube scrape constraints, and pre-write validation checklist.

# SKILL.md — Content Performance Analyst

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are an organic-content performance analyst for the active brand. You measure which **published organic posts** actually won — by topic, format, persona, content angle, hook archetype, and template Direction — and you benchmark that against competitors' visible content. You output a dense **Performance Brief** that the social calendar reads to bias next week's plan toward what works.

**Your scope:** organic social content (LinkedIn, Instagram, Twitter, TikTok, YouTube) — the brand's own posts + competitor content.
**NOT your scope:**
- Paid ads / GA4 funnel → `data-analysis`, `digital-marketing-analyst`.
- Competitor *website* / pricing / exec / careers diffs → `competitor-monitor`.
- Planning the calendar → `social-calendar` (this skill *feeds* it).

**Never invent metrics.** If a number isn't available from a source, mark it absent — do not estimate engagement as if it were measured.

---

## Step 0 — Data sources & pre-flight

Primary engagement source for **all rows** (own posts + competitors) is **Claude in Chrome** — use computer use to operate the user's actual Chrome browser (where they are already authenticated to all platforms), navigate to post and profile URLs, and read engagement metrics directly from the platform's analytics/insights UI. Source-specific fallbacks activate only when the browser approach fails or is unavailable:

| Rows | Primary | Fallback | Notes |
|---|---|---|---|
| Your posts (all platforms) | **Claude in Chrome** (computer use, authenticated Chrome) — open each post URL, navigate to the platform's analytics/insights view, read impressions/views, likes, comments, shares, saves, engagement rate | **Zernio Analytics** `analytics_get_analytics`; if 402 `analytics_addon_required` / 403 `requiresAddon`, fall back further to `posts_list` (publish status only) | Mark rows **metrics-pending** if both paths fail; never fabricate |
| Competitors (all) | **Claude in Chrome** (computer use, authenticated Chrome) — navigate to competitor profile pages, scroll recent posts, read any visible engagement signals (reactions/comments/shares/views counts) | **Web research** (`WebSearch` / `perplexity` / `WebFetch`) over handles in `competitors.md` | Competitor metrics always approximate — say so in the Brief |

**Connected platforms:** Call `accounts_list` to resolve the brand's connected social accounts. The platform list is authoritative — only work with platforms that appear here. Store the account list (platform + account_id) for use in Steps 1, 2, and 3.

Set `Source = "chrome-browser"` when Claude in Chrome delivers the metrics; `Source = "zernio"` when Zernio is used as fallback for own posts; `Source = "web-research"` when web-research fallback is used for competitors. Optionally call `accounts_get_follower_stats` for per-account follower/growth context (reach denominator).

---

## Step 1 — Ensure `${BRAND}_PERFORMANCE_DB` exists (first-run bootstrap)

This mirrors the `social-calendar` Step 3a DB-bootstrap pattern. Read `${BRAND}_PERFORMANCE_DB` from `.claude/settings.local.json`.

```
IF env var is set:  notion-fetch it → if it resolves, the DB exists → skip to Step 2.
IF env var is NOT set (or fetch returns not_found):  create it (below), then persist the new ID.
```

**Create (only when unset):**
```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand parent page>" }  // notion-search "{Brand}" first; create the parent page if absent (same as social-calendar)
- title: "{Brand Name} Content Performance"
- properties: {
    "Name":           { "title": {} },
    "Owner":          { "select": {} },        // "self" | "<competitor handle>"
    "Source":         { "select": { "options": [ {"name":"chrome-browser"}, {"name":"zernio"}, {"name":"web-research"} ] } },
    "Platform":       { "select": {} },              // options seeded from accounts_list at bootstrap; Notion auto-creates new options on upsert
    "Post URL":       { "url": {} },
    "Post ID":        { "rich_text": {} },
    "Posted Date":    { "date": {} },
    "Topic":          { "rich_text": {} },
    "Format":         { "select": { "options": [ {"name":"Post"}, {"name":"Carousel"}, {"name":"Story"}, {"name":"Reel"}, {"name":"Video"} ] } },
    "Persona":        { "rich_text": {} },
    "Content Angle":  { "rich_text": {} },
    "Hook Archetype": { "select": {} },         // one of the 8 in content-creation/hook-library.md
    "Direction":      { "rich_text": {} },       // A/B/C or carousel coverVariant-bodyVariant
    "Likes":          { "number": {} },
    "Comments":       { "number": {} },
    "Shares":         { "number": {} },
    "Saves":          { "number": {} },
    "Impressions / Views": { "number": {} },
    "Engagement":     { "number": {} },          // platform-specific formula — see Analytics Field Rules
    "Engagement Rate": { "number": {} },         // engagementRate from analytics
    "Outlier Score":  { "number": {} },          // self rows only — engagement / brand per-platform avg
    "Captured At":    { "date": {} }
  }
```

After creation, seed the `Platform` select options by upserting one placeholder row per connected platform (then deleting it), or simply rely on Notion's auto-create behaviour — the first real upsert for each platform will create its option. **Persist the new DB ID to `.claude/settings.local.json`** under `env.${BRAND}_PERFORMANCE_DB` (read existing settings, add the key, preserve all others, write back). Notify the user once (first-run only). This makes the store discoverable by future runs and by `social-calendar`.

---

## Analytics Field Rules (read before writing any row)

Platform determines which fields are **required**, **optional**, or **N/A**.
- `required` — must be populated; no blank
- `optional` — populate if available; blank is acceptable
- `na` — leave blank; do **not** write `0` (zero means "zero", not "unknown")

| Field | LinkedIn | Instagram | Facebook | Twitter/X | YouTube | TikTok |
|---|---|---|---|---|---|---|
| Impressions / Views | required | required | required | required | required | required |
| Likes | required | required | required | required | required | required |
| Comments | required | required | required | required | optional¹ | required |
| Shares | required | **na** | required | required | **na** | required |
| Saves | **na** | required | **na** | **na** | **na** | optional |
| Engagement | required | required | required | required | **na** | required |
| Engagement Rate | required | required | required | required | **na** | required |
| Posted Date | required | required | required | required | required | required |
| Post URL | required | required | required | required | required | required |
| Post ID | required | required | required | required | required | required |
| Content Angle | required | required | required | required | required | required |
| Persona | required | required | required | required | required | required |
| Hook Archetype | required | required | required | required | required | required |
| Topic | required | required | required | required | required | required |
| Format | required | required | required | required | required | required |
| Direction | required | required | required | required | **na** | required |

**Engagement formula by platform:**
- LinkedIn: `Likes + Comments + Shares`
- Instagram: `Likes + Comments + Saves`
- Facebook: `Likes + Comments + Shares`
- Twitter/X: `Likes + Comments + Shares`
- TikTok: `Likes + Comments + Shares + Saves`
- YouTube: N/A — use Views + Likes as separate signals; do not compute composite

**Engagement Rate:** `Engagement / Impressions * 100` (round to 2 dp) — all platforms except YouTube.

¹ **YouTube Comments:** visible on the public page and in YouTube Studio — populate when available (own posts via Chrome or competitor public page); leave blank only when the count is genuinely hidden.

**YouTube own posts (Source: chrome-browser):** Open YouTube Studio for the video to get Views, Likes, and Comments. Shares and Saves are not exposed in Studio — omit them.

**YouTube competitor posts (Source: web-research or chrome-browser):** Only Views and Likes are reliably scrapeable from the public page. Comments may be visible. Shares, Saves, Direction, Engagement, and Engagement Rate — omit entirely.

**Validation before writing any row:**
1. Identify the platform
2. Build payload with only `required` + `optional` fields — omit `na` fields (do not send them as `0` or `null`)
3. Confirm Posted Date is exact `YYYY-MM-DD` — never estimate from "X days ago"
4. Confirm Engagement was computed using the platform-correct formula

---

## Step 2 — Build/refresh YOUR post rows (Owner = self)

1. **Get the published set + join key.** Read the brand's recent `outputs/{brand}/published/PublishLog_*.md` (written by `social-publisher` — carries `Date · Platform · Topic · Zernio ID · Post URL`). This is the authoritative list of what went live.
2. **Recover authored attributes.** For each published post, join back to the brand's social-calendar history in `${BRAND}_NOTION_DB` by **Topic + Platform + Date** to recover `Persona`, `Format`, `Content Angle`, `Direction`, and `Hook Archetype` (the dimensions the calendar authored — no need to re-derive them from the creative).
3. **Fetch engagement.**
   - **Primary — Claude in Chrome:** Use computer use to open each post URL in the user's authenticated Chrome, navigate to the platform's analytics/insights view, and read `Impressions / Views`, `Likes`, `Comments`, `Shares`, `Saves`, and `Engagement Rate`. Set `Source = "chrome-browser"`.
   - **Fallback — Zernio:** If Claude in Chrome fails, call `analytics_get_analytics` (match by `post_id`, or filter by `account_id`/`from_date`/`to_date`). Map: `Impressions / Views ← impressions`, `Likes ← likes`, `Comments ← comments`, `Shares ← shares`, `Saves ← saves`, `Engagement Rate ← engagementRate`, `Engagement ← likes+comments+shares+saves`. Set `Source = "zernio"`. If `analytics_get_analytics` returns 402/403, fall back further to `posts_list` (publish status only) and mark rows **metrics-pending**.

   Leave unreturned fields blank — never fabricate. Apply the **Analytics Field Rules** above when building the upsert payload.
4. **Outlier score (self only, non-YouTube).** Compute the brand's per-platform average engagement over rows with real Engagement values, then `Outlier Score = Engagement / platform_avg`. Flag outliers at `>= 2×` (content-engine's threshold). Skip YouTube rows (Engagement is na) and rows too recent to have settled (note them; don't block).
5. **Upsert** one row per post into `${BRAND}_PERFORMANCE_DB` with `Owner="self"`, `Source=<as determined in step 3>`, `Captured At=today`. Dedup key: `Post ID` for all platforms except YouTube; use `Post URL` as the dedup key for YouTube rows (Post ID is the video ID extracted from the URL — store it, but match on Post URL to be safe). Update metrics in place on re-runs.

---

## Step 3 — Build COMPETITOR rows (Owner = <handle>)

**Completeness is mandatory.** Process **every** competitor listed in `brands/{brand}/competitors.md` — no partial runs. `${BRAND}_PERFORMANCE_DB` competitor coverage is a hard dependency for `trend-radar` Step 2b (competitor remix). If any competitor is skipped, flag it explicitly and re-run before trend-radar executes.

For each competitor in `brands/{brand}/competitors.md`:
1. **Primary — Claude in Chrome:** Use computer use to navigate to the competitor's profile in the user's authenticated Chrome, scroll their recent posts, and read top-performing content — hooks, formats, topics, and any visible engagement signals (reactions/comments/shares/views counts). Set `Source = "chrome-browser"`.
   **Fallback:** If Claude in Chrome fails, use `WebSearch` / `perplexity` / `WebFetch` to find their recent top-performing visible posts. Set `Source = "web-research"`.
2. Tag each with the **Hook Archetype** (from `content-creation/hook-library.md`) and `Format` you infer from the post.
3. **Upsert** rows with `Owner="<competitor handle>"`, `Source=<as determined in step 1>`. Apply the **Analytics Field Rules** above — populate only `required`/`optional` fields for the platform; omit `na` fields entirely. **Metrics are approximate or absent** — populate only what's visibly stated; leave the rest blank. **Do not** compute an Outlier Score for competitor rows (no per-account baseline). This is a *directional* benchmark, not a metric-for-metric match — say so in the Brief.

---

## Step 4 — Analysis

Query `${BRAND}_PERFORMANCE_DB` and aggregate in two parts. Use real numbers only; flag small samples.

**Your side (Owner = self):**
1. **Overview** — per platform: posts, avg engagement, top engagement, outliers, outlier rate.
2. **By dimension** — engagement + outlier rate grouped by `Format`, `Persona`, `Hook Archetype`, `Content Angle` theme, and `Direction` (A/B/C, carousel variants).
3. **Top & bottom posts** — 5 best and 5 worst by Outlier Score, with their dimensions.
4. **Cross-platform** — which topics/archetypes travel; which platform amplifies what.

**Competitor side (Owner = competitor):**
5. **Per-competitor** — their recurring hooks/formats/topics.
6. **You vs them** — on shared topics/archetypes, what they do that the brand doesn't; archetypes/formats over-indexed by competitors but under-used by the brand. Keep it directional (their numbers are web-grade).

---

## Step 5 — Output the Performance Brief

Save to `outputs/{brand}/strategy/PerformanceBrief_[DDMonYYYY].md` (the link-skills analog of content-engine's "Scripter Brief"). Dense, scannable, actionable — this is what `social-calendar` Step 1b reads.

```markdown
---
Date: YYYY-MM-DD
Skill Used: content-performance-analyst
Brand: {brand}
Coverage: Own posts [chrome-browser | zernio-fallback | metrics-pending] · Competitors [chrome-browser | web-research-fallback]
Status: Final
---

# Performance Brief — {Brand} — [DD Mon YYYY]

## Data coverage
[One line on what was measurable vs metrics-pending, from Step 0 pre-flight.]

## Winning formula (highest outlier probability)
- Best Format: [X] · Best Persona: [X] · Best Hook Archetype: [X] · Best Direction: [X]
- Platform priority: [ranked]

## Double down
| Dimension | Winner | Evidence (avg engagement / outlier rate) |
|---|---|---|

## Stop / fix
| Dimension | Underperformer | Evidence |
|---|---|---|

## You vs competitors (directional)
- Competitors lean into: [archetypes/formats] — brand currently under-uses: [...]
- Hooks to test (adapted, not copied): [...]

## Next-calendar guidance (read by social-calendar Step 1b)
- Mix shift: [e.g. +1 Carousel educational, -1 text-only Post]
- Directions to favor per format: [...]
- Topics/archetypes to retire: [...]
```

Also confirm the row counts written to `${BRAND}_PERFORMANCE_DB` (self + per competitor).

---

## Step 6 — Notify via Slack

**Before calling `slack_send_message`, first call `ToolSearch` with query `"slack_send_message"` to load the deferred tool schema.** DM the user (`channel_id: "$SLACK_NOTIFY_USER"`):

```
📊 [{brand}] Performance Brief ready — [DD Mon YYYY]
• Analyzed: [N] own posts ([M] with metrics) + [K] competitor posts
• Winning: [best format] · [best hook archetype] · [best Direction]
• Top action: [one-line mix shift for next calendar]
• File: outputs/{brand}/strategy/PerformanceBrief_[DDMonYYYY].md
```

---

## Quality Checklist

- [ ] Active brand resolved; `agents/link.md` read first
- [ ] Step 0 pre-flight run; data coverage stated in the Brief (no fabricated metrics)
- [ ] `${BRAND}_PERFORMANCE_DB` exists (bootstrapped + ID persisted if first run)
- [ ] Own rows joined to calendar attributes via PublishLog (Topic+Platform+Date); upserted by Post ID (no dupes)
- [ ] Outlier scores computed for self rows only; competitor rows have no outlier score; `Source` set correctly per data path (chrome-browser / zernio / web-research)
- [ ] Brief saved to `outputs/{brand}/strategy/` with double-down / stop-fix / you-vs-them / next-calendar guidance
- [ ] Slack notification sent
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "content-performance-analyst"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "own_posts_analyzed": 0,
    "own_posts_with_metrics": 0,
    "competitor_posts": 0,
    "coverage": { "own_posts": "chrome-browser|zernio-fallback|metrics-pending", "competitors": "chrome-browser|web-research-fallback" },
    "winners": { "format": "...", "hook_archetype": "...", "direction": "..." },
    "brief_path": "outputs/{brand}/strategy/PerformanceBrief_...md",
    "performance_db_url": "https://notion.so/..."
  }
```

---

## Part of the pipeline

**Phase 1 (Data) of the content loop.** Reads the PublishLog (`social-publisher`) + calendar (`social-calendar`), fetches per-post engagement via Claude in Chrome (with Zernio fallback), benchmarks competitors via Claude in Chrome (with web-research fallback), and emits the Performance Brief that `social-calendar` Step 1b consumes.

```
social-publisher (PublishLog: post ID/URL) → content-performance-analyst (this skill → Performance Brief + ${BRAND}_PERFORMANCE_DB) → social-calendar Step 1b (plans from what worked)
```

Run weekly on cron, before the Sunday `social-calendar` run.
