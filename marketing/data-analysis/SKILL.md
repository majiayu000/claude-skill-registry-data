---
name: data-analysis
description: Analyze campaign performance data — KPI dashboards, weekly/monthly reports, traffic and lead analysis for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Analyze campaign performance data — KPI dashboards, weekly/monthly reports, traffic and lead analysis"
deps:
  mcp: ["Windsor.ai", "Zernio (ads) (opt — fallback data pull + act-on-findings)"]
  gateway: []
  files: ["brand.md", "funnel.md"]
  env: ["`${BRAND}_ZERNIO_GOOGLE_ADS` + `${BRAND}_ZERNIO_GOOGLE_ADS_CID` (opt — Google Ads Zernio fallback pair)", "`${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID` (opt — Meta Ads Zernio fallback)", "`${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` (opt — LinkedIn Ads Zernio fallback pair)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.19.0 | July 03, 2026 |

**Description:** Analyze campaign performance data — KPI dashboards, weekly/monthly reports, traffic and lead analysis for any active brand

### Change Log

**v2.19.0** — July 03, 2026
- **Corrected Zernio ads-fallback tool names + date params to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 assumed Zernio just drops the `late_` prefix, but Zernio's tools are resource-prefixed. Repointed: `get_ads_timeline` → **`ad_campaigns_get_ads_timeline`**, `get_ad_tree` → **`ad_campaigns_get_ad_tree`**, `list_ad_campaigns` → **`ad_campaigns_list_ad_campaigns`**, `get_ad_analytics` → **`ads_get_ad_analytics`** (requires `ad_id`). Date filters corrected from `date_from`/`date_to` to **`from_date`/`to_date`** — the wrong names were silently returning empty (the same silent-failure class the v2.18.0 note claimed to fix, but with the wrong names).

**v2.18.0** — July 01, 2026
- **Zernio ads/analytics tools migrated to Zernio's own MCP (gateway v1.7.4).** Repointed all `late_*` ads/analytics fallback calls to Zernio's native tool names (drop the `late_` prefix; `late_search_ad_targeting_locations` → `search_ad_targeting`); dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*`. Windsor.ai remains the primary source; Zernio stays the optional fallback.

**v2.3.3** — May 16, 2026
- Bug fix (silent-failure): Zernio Windsor-fallback tool params standardized to snake_case (`date_from`/`date_to`, `account_id`) across `late_get_ads_timeline`, `late_get_ad_tree`, `late_list_ad_campaigns`, `late_get_ad_analytics`. Old `fromDate`/`toDate`/`accountId` were silently returning empty results.
- Tool reference expanded: `late_get_ad_tree` documented as the recommended path for Campaign → Ad Group/Set → Ad hierarchy in Google + Meta fallbacks (date-filterable, paginated 20/page default, max 100). `late_list_ad_campaigns` flagged as **lifetime-only** (no date filter) — campaign metadata only.
- Field mapping cleanup: documented Google Ads quirks (conversions always 0 — source proxy from brand's primary GA4 event; `adSets[]` IS ad-groups; keywords unavailable) and Meta Ads quirks (`late_get_ad_tree` returns 0 for paused campaigns).
- Brand-agnostic refactor: removed FA-specific `2026-03-08` GA4 tracking-bug date (now read from `brands/{brand}/funnel.md` `ga4_clean_data_start` if set); Google Ads conversion-proxy guidance references the brand's primary funnel event (no hardcoded event name).

**v2.3.2** — May 16, 2026
- Change log history trimmed — housekeeping pass to keep file-level history compact. No functional change.

**v2.3.1** — May 15, 2026
- Step 1a Windsor fallback — Google Ads Zernio fallback now passes **both** `account_id=${BRAND}_ZERNIO_GOOGLE_ADS` and `ad_account_id=${BRAND}_ZERNIO_GOOGLE_ADS_CID`. Passing only the SocialAccount ID returned empty results (the existing bug). Env-var gate added: if either var is missing, the Google Ads Zernio fallback is skipped and noted in Data Gaps.
- Step 1a now includes a **LinkedIn Ads** path (opt-in — only when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set). Windsor primary (`source: "linkedin"`, fields incl. `lead_form_opens` / `lead_form_completions`); Zernio fallback uses the same two-ID pattern as Google Ads (`platform: "linkedin"`). Field map covers `externalWebsiteConversions` → `conversions` and `qualifiedLeads` → `qualified_leads`.
- 429 rate-limit handling — note in Data Gaps "&lt;Platform&gt; rate-limited — retry after Xs" and continue with whatever Windsor or other-platform data is available; don't block the run.

# Data Analysis Skill

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a marketing analyst for the active brand. Your job is to interpret campaign and platform performance data, identify trends, and produce clear reports with actionable recommendations. You work with traffic metrics, lead generation data, and email campaign analytics. You never invent data—if data is missing, you flag it and recommend how to collect it.

---

## When to use

Use this skill when the task involves:
- Reviewing traffic performance (SERP rankings, AI citations, traffic volume)
- Analyzing email campaign results (opens, clicks, replies)
- Building KPI dashboards or reporting templates
- Producing weekly/monthly performance reports
- Identifying what's working and what needs optimization
- Setting benchmarks or tracking goals against them

Do NOT use this skill for:
- Writing marketing copy → use content-creation
- Building campaign strategy → use research-strategy
- Designing visual assets → use creative-designer
- Creating presentation decks from analysis → use campaign-presenter (after this skill)

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Data source | Yes | Windsor.ai (Google Ads, GA4, Meta Ads) — primary. Zernio ads fallback if Windsor.ai unavailable (Google Ads + Meta Ads only; GA4 Windsor-only). Or email metrics, lead data, raw numbers pasted by user. |
| Time period | Yes | e.g., last 30 days, Q1 2026, week of March 10 |
| Goal / benchmark | Yes | What were we trying to achieve? What's the target KPI? Read from `brands/{brand}/funnel.md` if available. |
| Persona / campaign | Optional | Which campaign or audience segment does this data relate to? |
| Report format | Optional | Summary, full report, dashboard layout, or slide-ready bullets |

---

## Step-by-step workflow

### Step 1: Clarify the data and goal
Before analyzing, confirm:
- What data is available? (traffic numbers, email metrics, lead counts, SERP positions)
- What period does the data cover?
- What was the goal or expected outcome?
- Is the data for a specific campaign, persona, or channel?

If data is incomplete or missing, flag what's needed before proceeding.

### Step 1a: Pull data from Windsor.ai or Meta Ads MCP (if applicable)

**Windsor.ai is the universal source** for Google Ads, GA4, **and** Meta Ads (Facebook + Instagram) — every brand has all three connected per brand-setup. The Meta Ads MCP at `https://mcp.facebook.com/ads` is an optional opt-in alternative for Meta data only; it is in limited rollout and most accounts won't have it. **LinkedIn Ads** is opt-in per brand (only pulled when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set) — see the LinkedIn Ads block below.

Branch on the `META_ADS_SOURCE` env var (saved by brand-setup, loaded into `os.environ` by the `CLAUDE.md` credential loader):

- **Default (env var unset)** → Pull Meta data from Windsor.ai with `source: "facebook"`. Universal path, works for every brand.
- **Opt-in (`META_ADS_SOURCE=meta_ads_mcp`)** → Pull Meta data from the Meta Ads MCP. On MCP error at runtime, fall back to the Windsor path (it is always connected for Meta per brand-setup).

Same approach as digital-marketing-analyst.

**Windsor.ai (Google Ads + GA4):**

```
Use Windsor.ai MCP tool `get_data`:
- source: "google_ads" / "googleanalytics4"
- date_preset: match the user's requested time period; always use "last_NdT" variants (e.g. "last_30dT") — never "last_Nd" which excludes today's UTC data
- fields: see connector-specific field lists below
```

- Google Ads: `["date", "campaign", "campaign_status", "ad_group", "clicks", "impressions", "ctr", "cost", "conversions", "cpa"]` — `keyword` returns null, omit it; `ad_group` returns raw resource paths
- GA4: `["date", "session_source_medium", "sessions", "bounce_rate"]` — `source`, `session_source`, `session_medium` are invalid; use only `session_source_medium`

**Meta Ads — default: Windsor.ai (`source: "facebook"`):**

```
Use Windsor.ai MCP tool `get_data`:
- source: "facebook"
- date_preset: "last_NdT" (match user's requested period)
- fields: [
    "date",
    "campaign", "campaign_effective_status",
    "adset_name", "adset_id", "adset_effective_status",
    "ad_name", "ad_id",
    "clicks", "impressions", "ctr", "spend", "reach",
    "frequency", "cpm", "cpc",
    "actions_landing_page_view",
    "actions_video_view",
    "<conversion-actions-field>",
    "<cost-per-conversion-field>"
  ]
```

Windsor field map for canonical Meta dimensions: `ad_set` → `adset_name`/`adset_id`, `ad` → `ad_name`/`ad_id`, `lp_views` → `actions_landing_page_view`, `video_views` → `actions_video_view` (3-sec plays; ThruPlays via the `*_thruplay_*` family), `conversions` → the `actions_*` field that matches the brand's funnel objective (e.g. `actions_omni_purchase` for e-commerce, `actions_lead` / `actions_offsite_conversion_fb_pixel_lead` for lead-gen, `actions_complete_registration` for SaaS, `actions_mobile_app_install` for apps). For cost-per-conversion use the matching `cost_per_action_type_<event>`. If `brands/{brand}/funnel.md` doesn't pin a specific Meta event, pull the broad set and report whichever returns non-zero.

**Meta Ads — opt-in alternative: Meta Ads MCP (only when `META_ADS_SOURCE=meta_ads_mcp`):**

List the Meta Ads MCP's available tools at runtime and pick the one that returns campaign-level insights for the requested date range. Typical fields: `campaign`, `clicks`, `impressions`, `ctr`, `spend`, `reach`. Drill-down via Meta's Marketing API: `ad_set`, `ad`, `lp_views`, `video_views`, `conversions`, `frequency`, `cpm`, `cpc`. On MCP error, fall back to the Windsor path above.

**LinkedIn Ads — opt-in per brand (only when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set):**

LinkedIn Ads is **not pulled by default**. The skill only fetches LinkedIn data when both env vars are present — otherwise it silently skips LinkedIn analysis. When set, the primary source is Windsor.ai; the fallback is Zernio (see the Windsor fallback section below).

```
Use Windsor.ai MCP tool `get_data`:
- source: "linkedin"
- date_preset: "last_NdT" (match user's requested period)
- fields: [
    "date",
    "campaign", "campaign_status",
    "clicks", "impressions", "ctr", "cost", "cpm", "cpc",
    "conversions", "cpa",
    "lead_form_opens", "lead_form_completions"
  ]
```

LinkedIn-specific field notes: `cost` is in the account's local currency (already in the LinkedIn ad account's billing currency — same as Google Ads, no USD conversion needed). LinkedIn-native conversion events surface as `externalWebsiteConversions` / `qualifiedLeads` in the underlying API; Windsor exposes them under `conversions` / `qualified_leads` — confirm the exact field names at query time via `get_fields` if a column comes back null.

**Currency:** Meta `spend` is USD on both paths — convert to the brand's local currency using exchange rate from `brands/{brand}/brand.md`. Google Ads `cost` and LinkedIn Ads `cost` are already in the account's local currency.
**Data lag:** Windsor.ai connectors (Google Ads, GA4, Facebook) and the Meta Ads MCP are all near-real-time. No lag adjustments needed.
**GA4 data reliability:** Check `brands/{brand}/funnel.md` for a `ga4_clean_data_start` date — if set, clamp the earliest start date to that value (covers per-brand tracking bugs or instrumentation gaps). Skip the check if the brand's funnel.md doesn't define one.
**Paid traffic segments:** Filter `google / cpc` for Google Ads sessions; filter `meta / paid_social` for Meta paid sessions.

**Windsor fallback — Google Ads, Meta Ads, and LinkedIn Ads:**

If Windsor.ai `get_data` errors **or** returns 0 rows, fall back to Zernio before asking the user for data:

```
Param-name reference (verified against the live Zernio MCP schema):
  - Tool names are resource-prefixed: ad_campaigns_get_ads_timeline, ad_campaigns_get_ad_tree, ad_campaigns_list_ad_campaigns (the `late_` prefix is NOT simply dropped)
  - Date params are from_date / to_date (YYYY-MM-DD) — NOT date_from / date_to (and NOT fromDate / toDate); the wrong names silently return empty
  - account_id and ad_account_id are correct as-is
  - ad_campaigns_get_ads_timeline and ad_campaigns_get_ad_tree accept from_date / to_date — date-filterable
  - ad_campaigns_list_ad_campaigns accepts from_date / to_date but its metrics are LIFETIME since campaign creation (the date range does not window them) — use only for campaign metadata
  - ad_campaigns_get_ad_tree and ad_campaigns_list_ad_campaigns default limit=20 (max 100); paginate when needed
  - ad_campaigns_get_ad_tree returns zero metrics for paused campaigns regardless of date range

Google Ads fallback (REQUIRES BOTH env vars — account_id + ad_account_id):
  ad_campaigns_get_ads_timeline  (account_id: ${BRAND}_ZERNIO_GOOGLE_ADS, ad_account_id: ${BRAND}_ZERNIO_GOOGLE_ADS_CID, platform: "google", from_date, to_date)
  ad_campaigns_get_ad_tree       (same IDs + from_date/to_date, platform: "google", limit: 100) — for Campaign → Ad Group → Ad hierarchy. In Google's response the `adSets[]` array IS the ad-groups array (Zernio's schema label is "adSets" but the data is ad-group level).
  ad_campaigns_list_ad_campaigns (same IDs, platform: "google") — campaign metadata only (objective, status, name). Metrics are LIFETIME — do not use as period totals.

Meta Ads fallback:
  ad_campaigns_get_ads_timeline  (account_id: ${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID, platform: "facebook", from_date, to_date) — the ONLY reliable date-filtered source for Meta account totals
  ad_campaigns_get_ad_tree       (account_id, platform: "facebook", from_date, to_date, limit: 100) — campaign→adset→ad hierarchy (but returns 0 metrics for paused campaigns)
  ad_campaigns_list_ad_campaigns (account_id, platform: "facebook") — campaign metadata only (names, IDs, objective, status). Metrics are LIFETIME — label as `spend_*_lifetime` in any payload.

LinkedIn Ads fallback (REQUIRES BOTH env vars — account_id + ad_account_id; opt-in per brand):
  ad_campaigns_get_ads_timeline  (account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS, ad_account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS_CID, platform: "linkedin", from_date, to_date)
  ad_campaigns_list_ad_campaigns (same IDs, platform: "linkedin") — campaign metadata only; metrics LIFETIME

Field mapping (Zernio → Windsor):
  spend → cost/spend · ctr, cpc, cpm, clicks, impressions, reach → direct
  conversions → conversions (Meta + LinkedIn; ⚠️ Google returns 0 — source the proxy conversion count from GA4 using the brand's primary conversion event defined in `brands/{brand}/funnel.md`. Do NOT hardcode an event name — each brand has different key events.)
  costPerConversion → cpa
  actions["landing_page_view"] → actions_landing_page_view (Meta)
  actions["video_view"] → actions_video_view (Meta)
  actions["lead"] / actions["offsite_conversion.fb_pixel_*"] → brand-specific actions_* (Meta — pull the broad set when funnel.md doesn't pin a specific event)
  externalWebsiteConversions → conversions (LinkedIn)
  qualifiedLeads → qualified_leads (LinkedIn)
  campaignName → campaign · status → campaign_effective_status
  adSets[].adSetName → ad_groups[].name (Google) / ad_sets[].name (Meta)
  keywords → NOT available at any level via Zernio — omit keywords table
```

Note in Data Gaps: "Zernio fallback used — adset-level breakdown and GA4 sessions not available."

⚠️ **Google Ads env var gate:** the Google Ads fallback requires **both** `${BRAND}_ZERNIO_GOOGLE_ADS` (Zernio SocialAccount `_id`) **and** `${BRAND}_ZERNIO_GOOGLE_ADS_CID` (Google Ads customer ID). If either is missing, skip the Google Ads Zernio fallback and note in Data Gaps: "Google Ads Zernio fallback skipped — `${BRAND}_ZERNIO_GOOGLE_ADS` / `${BRAND}_ZERNIO_GOOGLE_ADS_CID` not configured. Run brand-setup Step 7b Step D or plugin-update Step 3e."

⚠️ **LinkedIn Ads env var gate:** the LinkedIn Ads fallback requires **both** `${BRAND}_ZERNIO_LINKEDIN_ADS` (Zernio SocialAccount `_id`) **and** `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` (LinkedIn sponsored account ID). LinkedIn Ads is opt-in — if neither var is set, silently skip LinkedIn analysis (the brand likely does not run LinkedIn Ads). If one is set but not the other, note in Data Gaps: "LinkedIn Ads Zernio fallback skipped — partial env var configuration. Run brand-setup Step 7b Step D or plugin-update Step 3e."

⚠️ **Rate-limit handling:** if Zernio returns a 429 with `retryDelay`, note in Data Gaps "<Platform> rate-limited — retry after Xs" and continue with whatever Windsor or other-platform data is available. Do not block the run waiting for the retry window.

⚠️ **GA4 is Windsor-only — no Zernio fallback.** If Windsor is unavailable, GA4 session data cannot be retrieved. Add to Data Gaps: "GA4 unavailable — Windsor.ai offline; no fallback source for session data."

If Windsor.ai is not connected (which would mean brand-setup wasn't completed), and the user hasn't provided their own data, ask:
> "I need data to analyze. Either (1) complete brand-setup so Windsor.ai is connected for Google Ads, GA4, and Meta Ads, or (2) paste your data here as CSV, table, or numbers."

Do not proceed to analysis without data.

### Step 1b: Research industry benchmarks via WebSearch
When the user has not provided benchmarks or targets, use the **WebSearch tool** to find current industry standards to compare against:
- Email open/click/reply benchmarks for B2B SaaS (e.g., "B2B SaaS email open rate benchmark 2026")
- SEO and traffic benchmarks for the relevant segment
- AI search citation rates or visibility benchmarks
- Lead generation conversion rate norms for SaaS tools

Use Perplexity benchmarks only when no internal target exists. Label any externally sourced benchmark clearly in the report as "(Industry benchmark via Perplexity)".

### Step 2: Define the KPIs to analyze
Map the data to the brand's KPI categories (from dashboard-template.md):

**Traffic KPIs:**
- Total traffic (visits/month) and % change vs prior period
- SERP ranking positions (1-3, 4-10, 11-20 distribution)
- Keyword ranking changes (up/down movements)
- AI search citations (ChatGPT, Claude, Perplexity mentions)
- Content performance by URL

**Lead Generation KPIs:**
- Leads captured (widget conversions)
- Leads found (database searches)
- Leads enriched (% completion rate)
- Email campaign: sent, open rate, click rate, reply rate
- Cost per lead (if budget data is provided)

**Funnel KPIs:**
- Traffic → leads conversion rate (widget captures / total visits)
- Lead → email engagement rate (opens / leads contacted)
- Email → reply rate (replies / emails sent)

### Step 3: Analyze the data
For each KPI:
1. **State the metric**: What is the actual number?
2. **Compare to benchmark**: Is it above, at, or below target?
3. **Identify the trend**: Is it improving, declining, or flat vs. prior period?
4. **Flag anomalies**: Any significant spikes, drops, or unexpected patterns?

### Step 4: Identify insights
For each notable finding, write one clear insight sentence:
- Format: "[What happened] because [likely reason], which means [implication]"
- Example: "Email open rate dropped to 18% (from 31% last week) likely due to subject line change, which means we should revert to question-format subject lines."

Produce 3-5 key insights maximum per report.

### Step 5: Produce recommendations
For each insight, provide one specific, actionable recommendation:
- Reference specific brand features that can address the finding (brands/{brand}/product.md)
- Be specific about what to change, test, or continue
- Prioritize by impact: High / Medium / Low

### Step 6: Format the report
Structure the output clearly using the output format below.

### Step 7: Optional — Act on findings via Zernio Ads

After delivering the report, offer to apply recommendations directly when the user confirms:

| Finding | Action | Tool |
|---|---|---|
| Campaign wasting spend (high cost, 0 conv) | Pause campaign | `ad_campaigns_update_ad_campaign_status` |
| Multiple underperforming campaigns | Bulk pause | `ad_campaigns_bulk_update_ad_campaign_status` |
| Ad set audience fatigue (frequency > 2.5) | Pause ad set | `ad_campaigns_update_ad_set_status` |
| Drill-down needed on specific ad | Ad-level analytics | `ads_get_ad_analytics` (requires `ad_id`; `from_date`/`to_date` = report period) |
| Conversion tracking gaps flagged | Audit tracking | `ads_list_conversion_destinations` · `tracking_tags_get_tracking_tag_stats` |
| Top organic post worth promoting | Boost post | `ads_boost_post` |

Always confirm with the user before pausing or modifying campaigns. Read-only actions (analytics, tracking audit) can run immediately.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/dashboards/
```

**Folder by channel:**
| Channel | Local Folder |
|---|---|
| Google Ads | `outputs/{brand}/dashboards/` |
| LinkedIn Ads | `outputs/{brand}/dashboards/` |
| Facebook/Instagram Ads | `outputs/{brand}/dashboards/` |
| Email campaigns | `outputs/{brand}/dashboards/` |
| SEO / traffic | `outputs/{brand}/dashboards/` |

**Naming convention:**
```
[AnalysisType]_[DDMonYYYY].md
```

Examples:
- `CampaignAnalysis_10Mar2026.md`
- `EmailReport_10Mar2026.md`
- `TrafficReport_10Mar2026.md`
- `SEOAudit_10Mar2026.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: data-analysis
Data Source: [Traffic report | Email metrics | Lead data | Mixed]
Time Period: [e.g., March 1-7, 2026]
Campaign: [Campaign name, if applicable]
Persona: [Persona name, if applicable]
Status: Draft | Final
---
```

**Report sections:**
1. **Summary** — 2-3 sentence overview of performance (positive or negative)
2. **KPI Scorecard** — Table of key metrics vs. targets/benchmarks
3. **Key Insights** — 3-5 bulleted insights using the [What → Why → Implication] format
4. **Recommendations** — 3-5 prioritized, actionable next steps
5. **Data Gaps** — Any missing data that would improve the analysis (if applicable)

**KPI Scorecard table template:**
```markdown
| KPI | Target | Actual | vs. Target | Trend |
|-----|--------|--------|------------|-------|
| Total traffic | 2,000/mo | 2,140 | +7% ✅ | ↑ +28% vs prior |
| SERP positions 1-3 | 5 keywords | 3 | -40% ⚠️ | → Flat |
| Email open rate | 25% | 31% | +24% ✅ | ↑ +6pp vs prior |
```

---

## Quality checklist

Before finalizing any analysis output:

- [ ] All metrics are from actual data provided — no invented numbers
- [ ] KPIs match the brand's platform metric definitions (from dashboard-template.md)
- [ ] Each insight uses the [What → Why → Implication] format
- [ ] Each recommendation is specific and actionable (not vague like "improve open rates")
- [ ] Recommendations reference brand features where relevant (from `brands/{brand}/product.md`)
- [ ] Data gaps are clearly flagged if data is incomplete
- [ ] Output saved to outputs/{brand}/dashboards/ with correct naming and metadata
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "data-analysis"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "report_type": "<daily-paid-ads|weekly-traffic|monthly-leads>",
    "time_period": "YYYY-MM-DD",
    "campaign": "all",
    "content_status": "Final",
    "kpis": [{ "name": "Total Sessions", "value": 0, "benchmark": null, "status": "neutral" }],
    "recommendations": ["..."],
    "data_gaps": ["..."],
    "deliverable": "<filename>",
    "output_path": "outputs/{brand}/dashboards/"
  }
```
