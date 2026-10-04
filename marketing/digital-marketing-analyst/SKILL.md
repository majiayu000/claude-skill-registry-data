---
name: digital-marketing-analyst
description: Daily and weekly paid ads analysis — Google Ads, Meta Ads, GA4 funnel analysis with structured JSON email briefs for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Marketing
use_for: "Daily and weekly paid ads analysis — Google Ads, Meta Ads, LinkedIn Ads (opt), GA4 funnel analysis with structured JSON email briefs"
deps:
  mcp: ["Windsor.ai", "Slack", "Gmail (opt — fallback when fiveagents_send_email returns 403)", "Meta Ads MCP (opt — Windsor covers Meta when absent)", "Zernio (ads) (opt — Windsor fallback data pull; Phase 4 ads actions)"]
  gateway: ["email"]
  files: ["brand.md", "funnel.md"]
  env: ["`${BRAND}_ZERNIO_GOOGLE_ADS` + `${BRAND}_ZERNIO_GOOGLE_ADS_CID` (opt — Google Ads Zernio fallback pair)", "`${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID` (opt — Meta Ads Zernio fallback)", "`${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` (opt — LinkedIn Ads Zernio fallback pair; gates Phase 2.5 and weekly Step 1d)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.19.0 | July 03, 2026 |

**Description:** Daily and weekly paid ads analysis — Google Ads, Meta Ads, LinkedIn Ads (opt), GA4 funnel analysis with structured JSON email briefs for any active brand

### Change Log

**v2.19.0** — July 03, 2026
- **Corrected all Zernio ads/analytics tool names + date params to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 assumed Zernio just drops the `late_` prefix, but Zernio's tools are resource-prefixed. Repointed every ads-fallback and action-table call: campaign tools → `ad_campaigns_*` (`get_ads_timeline`, `get_ad_tree`, `list_ad_campaigns`, `update_ad_campaign[_status]`, `bulk_update_ad_campaign_status`, `duplicate_ad_campaign`, `update_ad_set_status`); ad/targeting/boost/conversion tools → `ads_*` (`get_ad_analytics` [requires `ad_id`], `get_ad_comments`, `list_ad_accounts`, `search_ad_interests`, `search_ad_targeting`, `boost_post`, `create_ctwa_ad`). Date filters corrected from `date_from`/`date_to` to **`from_date`/`to_date`** (the wrong names silently returned empty). Corrected the "no date params" caveats — `ad_campaigns_list_ad_campaigns` does accept the range, but its metrics are lifetime regardless.

**v2.18.0** — July 01, 2026
- **Zernio ads/analytics tools migrated to Zernio's own MCP (gateway v1.7.4).** Repointed all `late_*` ads/analytics fallback calls to Zernio's native tool names (drop the `late_` prefix; `late_search_ad_targeting_locations` → `search_ad_targeting`); dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*`. Windsor.ai remains the primary source; Zernio stays the optional fallback.

**v2.3.3** — May 16, 2026
- Bug fix (silent-failure): Zernio tool params standardized to snake_case (`date_from`/`date_to`, `account_id`) across `late_get_ads_timeline`, `late_get_ad_tree`, `late_get_ad_analytics`. Old `fromDate`/`toDate`/`accountId` were silently returning empty/wrong data.
- `late_get_ad_tree` added as the recommended path for Campaign → Ad Group → Ad hierarchy in both Google and Meta Zernio fallbacks (date-filterable; paginated 20/page default, max 100). `late_list_ad_campaigns` clearly flagged as **lifetime-only** (no date filter) — use only for campaign metadata.
- Google Ads Zernio quirks documented: conversions always 0 (source proxy from brand's primary GA4 event in `funnel.md`); `adSets[]` IS the ad-groups array; keywords not available at any level; no currency field — assume account default. Meta `late_get_ad_tree` returns 0 metrics for paused campaigns regardless of date.
- Critical template gotcha: `meta_ads.no_active_campaigns: true` skips the entire Meta summary box — always set `false`; use the new `all_campaigns_paused` field for pause state instead.
- Payload schema additions: new Meta fields (`all_campaigns_paused`, `last_spend_date`, `days_dark`, `lp_views`/`leads`/`video_views` in account_totals, `spend_*_lifetime` + `note` on campaign rows for lifetime data, `spend_usd: null` for Zernio source); new Google Ads `conversions_note`; richer GA4 funnel block (`click_to_session_google_pct` / `click_to_session_meta_pct` plus per-stage event counts keyed off brand `funnel.md`).
- Brand-agnostic refactor: removed FA-specific `2026-03-08` GA4 tracking-bug date (now read from `brands/{brand}/funnel.md` `ga4_clean_data_start` if set); replaced hardcoded `trials` KPI in Slack/log/`combined_summary` templates with generic `primary_conversions` driven by the brand's primary conversion event; removed "signup form" assumption from analysis guidelines.

**v2.3.2** — May 16, 2026
- Change log history trimmed — housekeeping pass to keep file-level history compact. No functional change.

**v2.3.1** — May 15, 2026
- Phase 1 Step 1 Google Ads Zernio fallback — now passes **both** `account_id=${BRAND}_ZERNIO_GOOGLE_ADS` and `ad_account_id=${BRAND}_ZERNIO_GOOGLE_ADS_CID`. Passing only the SocialAccount ID returned empty results (the existing bug). Env-var gate updated: if either is missing, set `all_campaigns_paused: true` with a clear "run brand-setup Step 7b Step D or plugin-update Step 3e" note.
- **New Phase 2.5 — LinkedIn Ads Data Pull** (`linkedin-data-pull`, optional). Runs only when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are both set. Windsor primary (`source: "linkedin"`, fields incl. `lead_form_opens` / `lead_form_completions`); Zernio fallback with same two-ID pattern (`platform: "linkedin"`). Dedicated JSON shape (`tmp/linkedin-{date}.json` with `linkedin_ads` block + LinkedIn-specific CTR/CPC/CPM/lead-form benchmarks).
- Daily Brief Architecture table extended with the optional 4th `linkedin-data-pull` cron job. Phase 3 Step 1 (Email Stitcher) optionally loads `tmp/linkedin-{date}.json`; absent file is silent (no retry, no warning) — opt-in per brand.
- Weekly Workflow — new Step 1d (Pull Weekly LinkedIn Ads Data, optional). Weekly job table extended with `linkedin-weekly-data-pull` cron. Weekly Google Ads fallback line clarified — explicitly passes both `account_id` + `ad_account_id` (was ambiguous; relied on "same as daily" which itself was wrong before this fix).
- Slack DM template includes a conditional LinkedIn line; omit when LinkedIn JSON absent.
- 429 rate-limit handling — note in `flags.notes` "&lt;Platform&gt; rate-limited via Zernio — retry after Xs" and continue with available data; don't block the run.

# SKILL.md — Digital Marketing Analyst

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a senior Digital Marketing Expert with deep expertise in Google Ads, Facebook Ads, TikTok Ads, SEO, and full-funnel performance marketing. Your job is to analyze campaign data, identify opportunities and problems, and deliver clear, prioritized, actionable recommendations.

---

## Daily Brief Architecture

The daily brief runs as **3 cron jobs by default** (plus an optional 4th for LinkedIn Ads) to stay within the 5-minute execution limit:

| Job | Cron | What it does | Output |
|---|---|---|---|
| `gads-data-pull` | cron schedule daily | Google Ads + GA4 pull + analysis | `tmp/gads-{YYYY-MM-DD}.json` |
| `meta-data-pull` | cron schedule daily | Meta Ads pull + analysis | `tmp/meta-{YYYY-MM-DD}.json` |
| `linkedin-data-pull` *(optional — only when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set)* | cron schedule daily | LinkedIn Ads pull + analysis | `tmp/linkedin-{YYYY-MM-DD}.json` |
| `paid-ads-email-sender` | cron schedule + 15min daily | Reads all available JSONs, builds JSON payload, sends via Postmark | Email to $REPORT_EMAIL |

Data-pull jobs run in parallel. The email sender waits 15 minutes to ensure files exist before sending; LinkedIn data is included only if the file exists, otherwise the email omits the LinkedIn section.

The **weekly brief** runs as the same job pattern (Saturdays — 3 required + 1 optional LinkedIn) — see Weekly Workflow section.

### Email rendering
The agent sends **structured JSON** (not HTML) as `html_body` to `fiveagents_send_email`. The fiveagents.io server renders the JSON into styled HTML using a dedicated template (`paid-ads-brief.ts`) matched by the `tag` parameter. The agent's job is to build the correct JSON structure — all styling, tables, and layout are handled server-side.

### Date rule — never fall back to older data

⚠️ **The brief always covers yesterday's date. Never substitute an older date's data because yesterday returned zero.**

If a platform returns zero campaigns or empty Sheets for yesterday:
- Set `no_active_campaigns: true` (Meta) or `all_campaigns_paused: true` (Google Ads)
- Report it honestly as "No Active Campaigns" for that date
- Both platforms must cover the **same date** — mixing dates (e.g. Meta from 3 days ago, Google Ads from yesterday) produces an inconsistent brief

Zero spend on a given date is valid data. It means campaigns were paused or budgets exhausted that day.

---

## Phase 1 — Google Ads + GA4 Data Pull (`gads-data-pull`)

### Step 1 — Pull Google Ads Data

Pull Google Ads data via **Windsor.ai MCP** connector.

```
Use Windsor.ai MCP tool `get_data`:
- source: "google_ads"
- date_preset: "last_30dT" (includes today — never use "last_30d" which excludes the current UTC day)
- fields: ["date", "campaign", "campaign_status", "ad_group", "clicks", "impressions", "ctr", "cost", "conversions", "cpa"]
```

⚠️ **Known issues:**
- `keyword` field returns null — omit keyword table
- `ad_group` returns raw resource paths, not human-readable names
- `cost` is returned in the account's local currency (no conversion needed)
- Data is near-real-time — no lag. Use yesterday's date as the report date; today's data may be partial.

Pull data for **two dates** — yesterday + the day before for DoD comparison.

If yesterday is a Monday, note "Weekend — structurally lower volume" for DoD comparisons.

#### Windsor.ai field reference

Windsor returns named fields directly — no column mapping needed:
- `date`, `campaign`, `campaign_status`, `ad_group`, `clicks`, `impressions`, `ctr`, `cost`, `conversions`, `cpa`

⚠️ **Invalid fields** (not available in Windsor for Google Ads): keyword-level data returns null. Omit keyword table.

#### Date validation
Check `max(date)` from the Windsor response to confirm the data covers the expected report date.

#### Windsor fallback — Google Ads

If Windsor.ai `get_data` errors **or** returns 0 rows for the target date, fall back to Zernio:

```
Log: "Windsor.ai unavailable — falling back to Zernio for Google Ads"

1. Call ad_campaigns_get_ads_timeline (for daily account totals — date-filterable):
   - account_id: ${BRAND}_ZERNIO_GOOGLE_ADS
   - ad_account_id: ${BRAND}_ZERNIO_GOOGLE_ADS_CID
   - from_date: day_before_yesterday (YYYY-MM-DD)
   - to_date: yesterday (YYYY-MM-DD)
   - platform: "google"
   → Returns daily rows: { date, spend, impressions, clicks, ctr, cpc, cpm, conversions, costPerConversion, reach }

2. Call ad_campaigns_get_ad_tree (for Campaign → Ad Group → Ad hierarchy — date-filterable):
   - account_id: ${BRAND}_ZERNIO_GOOGLE_ADS
   - ad_account_id: ${BRAND}_ZERNIO_GOOGLE_ADS_CID
   - from_date / to_date: same as timeline
   - platform: "google"
   - limit: 100 (default 20 — paginate via `page` if > 20 campaigns)
   → Returns nested Campaign → adSets → ads hierarchy with rolled-up metrics for the period.
     In Google's response, the `adSets[]` array IS the ad-groups array — Zernio's schema labels them "adSets" but the data is ad-group level. Map `response.campaigns[].adSets[]` → `ad_groups[]` in the intermediate JSON.

3. Optionally call ad_campaigns_list_ad_campaigns for campaign metadata only (objective, status, name):
   - account_id: ${BRAND}_ZERNIO_GOOGLE_ADS
   - ad_account_id: ${BRAND}_ZERNIO_GOOGLE_ADS_CID
   - platform: "google"
   ⚠️ This tool's metrics are LIFETIME totals since campaign creation — the `from_date`/`to_date` range does not window them. Use `ad_campaigns_get_ad_tree` for date-filtered metrics; use `ad_campaigns_list_ad_campaigns` only for campaign-level metadata.

⚠️ Both `account_id` (Zernio SocialAccount `_id`) and `ad_account_id` (Google Ads customer ID, 10-digit) are required. Passing only `account_id` returns empty results.

Field mapping — Zernio → Windsor schema:
  spend             → cost            (no currency field in Google Ads response — assume the account's default currency as configured in Zernio; the brand's reporting currency is in `brands/{brand}/brand.md`)
  ctr, cpc, cpm     → direct
  clicks, impressions → direct
  conversions       → conversions     (⚠️ Google Ads Zernio always returns 0 — conversion tracking is not wired to Zernio. Source the proxy conversion count from GA4 using the brand's primary conversion event defined in `brands/{brand}/funnel.md` — do NOT hardcode an event name, each brand has different key events.)
  costPerConversion → cpa
  campaignName      → campaign
  status            → campaign_status
  adSets[].adSetName → ad_groups[].name (the `adSets` label in the response is Zernio's naming — Google's actual hierarchy is ad-groups)
  keywords          → NOT available at any level via Zernio — omit keywords table

Set in intermediate JSON: "data_source": "zernio_fallback"
Set in email flags.notes: "⚠️ Windsor.ai unavailable — Google Ads data sourced from Zernio (conversions sourced from GA4)"
```

⚠️ **If either `${BRAND}_ZERNIO_GOOGLE_ADS` or `${BRAND}_ZERNIO_GOOGLE_ADS_CID` is not set:** skip the fallback and set `all_campaigns_paused: true` with note "Google Ads data unavailable — Windsor.ai offline and Zernio Google Ads env vars (`${BRAND}_ZERNIO_GOOGLE_ADS` + `${BRAND}_ZERNIO_GOOGLE_ADS_CID`) not configured. Run brand-setup Step 7b Step D or plugin-update Step 3e."

⚠️ **If Zernio returns 429 with `retryDelay`:** note in `flags.notes` "⚠️ Google Ads rate-limited via Zernio — retry after Xs" and continue with whatever Windsor or other-platform data is available. Do not block the run waiting for the retry window.

### Step 2 — Pull GA4 Data

⚠️ **GA4 is Windsor-only — no Zernio fallback.** Zernio does not expose GA4 session data. If Windsor.ai is unavailable, set `ga4.sessions_total: null` and add `"GA4 unavailable — Windsor.ai offline; no fallback source"` to `ga4.funnel_flags`. Do not attempt to substitute GA4 data from any other source.

⚠️ **Data reliability note:** Check `brands/{brand}/funnel.md` for a `ga4_clean_data_start` date — if the brand had a tracking bug or instrumentation gap, clamp the earliest start date to that value. Skip the check if the brand's funnel.md doesn't set one.

Pull GA4 data via **Windsor.ai MCP** connector:

```
Use Windsor.ai MCP tool `get_data`:
- source: "googleanalytics4"
- date_preset: "last_30dT"
- fields: ["date", "session_source_medium", "sessions", "bounce_rate"]
```

Filter results for the report date. Segment by `session_source_medium`:
- `meta / paid_social` → Meta Ads sessions (paid)
- `google / cpc` → Google Ads sessions (paid)

⚠️ **Invalid fields** (not in Windsor for GA4): `source`, `session_source`, `session_medium` — use only `session_source_medium`.
⚠️ **GA4 data is near-real-time** in Windsor — yesterday's data is available immediately.

### Step 3 — Analyze Google Ads + GA4

Evaluate each dimension against benchmarks. Compute DoD deltas.

#### Campaign Level benchmarks
| Metric | Watch For |
|---|---|
| CTR | < 2% = low (search) |
| CPC | Sudden spike >20% vs prior day |
| Conversion Rate | Drop >15% vs 7-day avg |
| Impression Share | < 50% = budget or quality issue |
| Budget Utilization | >95% = limiting reach; <50% = delivery issue |

#### Ad Group Level
| Metric | Watch For |
|---|---|
| Quality Score | ≤ 4 = urgent fix |
| CTR vs campaign avg | >30% below avg = ad relevance issue |
| Wasted spend | High cost + 0 conversions over 7 days |

#### Keyword Level
| Metric | Watch For |
|---|---|
| Quality Score | ≤ 4 = fix landing page or ad copy |
| High spend, 0 conversions | Pause or bid down |
| Match type | Broad match with no negatives = risk |

**DoD format:**
- Green ▲ for improvement (lower CPA/CPC, higher CTR/conv)
- Red ▼ for deterioration
- Grey `—` if prior day had 0 data (new campaign, paused day, Day 1)

### Step 4 — Compute Full Funnel (GA4 side)

**Funnel structure is brand-specific.** Read from `brands/{brand}/funnel.md` for the active brand's stages, GA4 events, and benchmarks. Examples below show two common funnel types for reference:

#### Example A — SaaS signup + trial flow (10 stages):
1. Impressions → Clicks (CTR)
2. Clicks → GA4 Sessions / Paid Search (click-to-session)
3. Sessions → Trial CTA Click (`start_free_trial_click`)
4. CTA → Signup Form Start (`form_start` on `/auth/signup`)
5. Form Start → Signup Form Submit (`form_submit` on `/auth/signup`)
6. Submit → Profile Form Start (`form_start` on `/auth/signup/profile`)
7. Profile Start → Profile Submit (`form_submit` on `/auth/signup/profile`)
8. Profile Submit → Trial Activated
9. Trial → Paid Conversion (Paid_Basic_Monthly + Paid_Pro_Monthly etc.)
10. Sessions → Schedule Call (`schedule_call_click`)

Example benchmarks for SaaS trial funnel:
- Click-to-Session: 80–90% normal; <70% = fix tracking
- Session-to-CTA: 5–15% avg
- CTA-to-Form Start: >60%
- Form Start-to-Submit: >50%
- Form Submit-to-Trial: >70%
- Trial-to-Paid: 15–25%
- Cost/trial and Cost/paid: read target ranges from `brands/{brand}/funnel.md`

#### Example B — Lead gen flow (3 stages):
1. Sessions (pageview)
2. Sessions → Lead (`click_schedule_call`)
3. Lead → Booked (`calendly_booked`)

Example benchmarks for lead gen funnel:
- Session-to-Lead: 3–8% avg
- Lead-to-Booked: >50%
- Cost/lead: track and flag spikes >20% DoD
- Cost/booked: primary CPA metric

Status: 🟢 on/above benchmark · 🟡 within 20% below · 🔴 below or critical

### Step 5 — Save Intermediate JSON

Save all data to `tmp/gads-{YYYY-MM-DD}.json` where the date is **yesterday's date** (the report period).

⚠️ **This schema must match what the email template (`paid-ads-brief.ts`) expects.** The stitcher merges these files into the final email JSON payload.

```json
{
  "report_date": "YYYY-MM-DD",
  "generated_at": "ISO timestamp",
  "google_ads": {
    "all_campaigns_paused": false,
    "account_totals": {
      "spend_sgd": 0.0,
      "clicks": 0,
      "impressions": 0,
      "ctr_pct": 0.0,
      "conversions": 0,
      "cpa_sgd": 0.0
    },
    "account_dod": { "spend": "▲ +5%", "clicks": "▼ -8%", "conv": "—", "ctr": "—", "cpa": "—", "impressions": "—" },
    "campaigns": [
      {
        "name": "Campaign Name", "status": "Eligible",
        "spend_sgd": 0.0, "clicks": 0, "impr": 0, "ctr_pct": 0.0,
        "conv": 0, "cpa_sgd": 0.0, "dod": "▲ +5%"
      }
    ],
    "ad_groups": [{ "name": "", "campaign": "", "status": "", "clicks": 0, "impr": 0, "ctr_pct": 0.0, "cost_sgd": 0.0, "dod": "" }],
    "ads": [{ "headline_1": "", "campaign": "", "ad_group": "", "clicks": 0, "impr": 0, "ctr_pct": 0.0, "cost_sgd": 0.0, "conv": 0, "dod": "" }],
    "keywords": [{ "keyword": "", "campaign": "", "clicks": 0, "ctr_pct": 0.0, "cost_sgd": 0.0, "conv": 0, "dod": "" }],
    "flags": {
      "urgent": ["flag text"],
      "optimize": ["flag text"],
      "monitoring": ["flag text"]
    },
    "notes": ["any data warnings, e.g. 'GA4 data unavailable'"],
    "top_recommendation": "Best single action for this platform"
  },
  "ga4": {
    "date": "YYYY-MM-DD",
    "sessions_total": 0,
    "paid_search_sessions": 0,
    "meta_sessions": 0,
    "funnel": {
      // Keys match funnel stages from brands/{brand}/funnel.md
      // Example — lead gen funnel:
      "sessions": 0,
      "click_schedule_call": 0,
      "calendly_booked": 0
    },
    "funnel_flags": ["flag text — one per flagged stage"]
  }
}
```

After saving, log to `memory/YYYY-MM-DD.md`:
```markdown
## gads-data-pull — [ISO timestamp]
- Report date: [date]
- Google Ads: Spend [currency] [x] / [clicks] clicks / [conv] conv / CPA [currency] [x]
- GA4: [sessions] paid search sessions / [primary_conv_count] [primary_conv_label]   ← read primary conversion event + display label from brands/{brand}/funnel.md
- Saved: tmp/gads-[date].json
```

---

## Phase 2 — Meta Ads Data Pull (`meta-data-pull`)

### Step 1 — Pull Meta Ads Data

**Branch on `META_ADS_SOURCE` env var** (saved by brand-setup Step 7c, loaded into `os.environ` by the credential loader in `CLAUDE.md`). Windsor.ai is the universal default because every brand has it connected with Meta Ads — the optional Meta Ads MCP just lets some accounts opt into Marketing-API-direct access:
- `META_ADS_SOURCE` unset (default) → use **Windsor.ai for Meta** — universal path, works for every brand
- `META_ADS_SOURCE=meta_ads_mcp` → use **Meta Ads MCP** — user explicitly opted in during brand-setup because their account had MCP rollout access. If the MCP errors at runtime, fall back to Windsor.ai (it's always connected with Meta Ads, per brand-setup Step 7c).

#### Windsor.ai — universal default (recommended path)

Pull Meta data via the existing Windsor.ai MCP connector with `source: "facebook"`. This is the path used unless the user opted into the MCP. Windsor.ai's Facebook source has near-parity with Meta's Marketing API — campaign / ad-set / ad breakdowns, landing-page views, video views, and conversion actions are all surfaced under their Windsor field names. Use this request shape:

```
Use Windsor.ai MCP tool `get_data`:
- source: "facebook"
- date_preset: "last_30dT" (includes today — never use "last_30d" which excludes the current UTC day)
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

**Field mapping — Windsor.ai field names for the canonical Meta dimensions:**

| Canonical (MCP-style) field | Windsor.ai equivalent |
|---|---|
| campaign / campaign status | `campaign` / `campaign_effective_status` |
| ad_set | `adset_name` (with `adset_id`, `adset_effective_status`) |
| ad | `ad_name` (with `ad_id`) |
| clicks / impressions / ctr / spend / reach | same names: `clicks`, `impressions`, `ctr`, `spend`, `reach` |
| frequency / cpm / cpc | same names: `frequency`, `cpm`, `cpc` |
| lp_views (landing page views) | `actions_landing_page_view` |
| video_views (3-sec plays) | `actions_video_view` (also `cost_per_thruplay_video_view` for ThruPlays) |
| conversions | `actions_*` family — pick by the brand's funnel objective from `brands/{brand}/funnel.md`: e.g. `actions_omni_purchase` (e-commerce), `actions_lead` / `actions_offsite_conversion_fb_pixel_lead` (lead-gen), `actions_complete_registration` (SaaS signup), `actions_mobile_app_install` (apps). For cost-per-conversion use the matching `cost_per_action_type_<event>` field. |

If `funnel.md` doesn't pin a specific Meta conversion event, pull the broad set (`actions_lead`, `actions_omni_purchase`, `actions_complete_registration`) and report whichever returns non-zero values.

Filter results for the report date and roll up by `adset_name` / `adset_id` and `ad_name` / `ad_id` for the ad-set / ad arrays, and aggregate up to campaign / account totals.

#### Meta Ads MCP — opt-in alternative (only when `META_ADS_SOURCE=meta_ads_mcp`)

Pull via the **Meta Ads MCP** custom connector (`https://mcp.facebook.com/ads`) — Meta's official MCP for Facebook + Instagram campaign data. Use this only when the user explicitly added the connector during brand-setup; otherwise stick with the Windsor default above.

At runtime, list the Meta Ads MCP's available tools and pick the one that returns campaign-level insights for the requested date range. Typical request shape:

- **Ad accounts:** the brand's connected Meta Business ad accounts (the MCP knows these from the OAuth session)
- **Date range:** yesterday's date in the brand's timezone (also fetch the prior day for DoD comparison)
- **Required fields:** campaign name + status, clicks, impressions, ctr, spend, reach
- **Drill-down:** ad_set, ad, lp_views (landing page views), video_views, conversions, frequency, cpm, cpc

**Runtime fallback:** if the MCP errors (auth, rate limit, listing failure), fall back to the Windsor.ai path above using the same field map. Windsor is always connected with Meta Ads per brand-setup Step 7c, so the fallback is guaranteed to work — log a warning to memory but do not fail the run.

#### Windsor fallback — Meta Ads

If Windsor.ai `get_data` with `source: "facebook"` errors **or** returns 0 rows for the target date, fall back to Zernio:

```
Log: "Windsor.ai unavailable — falling back to Zernio for Meta Ads"

1. Call ad_campaigns_get_ads_timeline (the ONLY reliable date-filtered source for Meta account totals):
   - account_id: ${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID
   - from_date: day_before_yesterday (YYYY-MM-DD)
   - to_date: yesterday (YYYY-MM-DD)
   - platform: "facebook"
   → Returns one row per calendar day with: { date, spend, impressions, clicks, ctr, cpc, cpm, reach, conversions, costPerConversion, actions, actionValues, purchaseValue, roas }
   → Sum all rows for period totals. Zero rows are returned for days with no spend — that is valid data.

2. Call ad_campaigns_list_ad_campaigns for campaign metadata only (names, IDs, objective, status):
   - account_id: ${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID
   - platform: "facebook"
   - limit: 100 (default 20)
   ⚠️ This tool's `metrics.spend` etc. are LIFETIME totals since campaign creation, not the report period — the `from_date`/`to_date` range does not window them. Do NOT use these as MTD/daily spend. In the payload, label them `spend_sgd_lifetime` (etc.) and add a `note` field so the dashboard knows the scope.

3. Optionally call ad_campaigns_get_ad_tree for Campaign → Ad Set → Ad hierarchy (date-filterable but with caveats):
   - account_id: ${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID
   - from_date / to_date: same as timeline
   - platform: "facebook"
   - limit: 100 (default 20 — paginate if > 20 campaigns)
   ⚠️ Returns zero metrics for paused campaigns regardless of date range. If a brand has all campaigns paused but you still need the hierarchy for the email, the ad-set / ad arrays will be empty — that is expected.

Field mapping — Zernio → Windsor schema:
  spend                              → spend                 (native currency — same as Windsor)
  ctr, cpc, cpm, clicks, impressions, reach → direct map
  actions["landing_page_view"]       → actions_landing_page_view
  actions["link_click"]              → link_clicks (raw)
  actions["video_view"]              → actions_video_view
  actions["lead"]                    → actions_lead (lead-gen)
  actions["offsite_conversion.fb_pixel_purchase"] → actions_omni_purchase (e-commerce)
  actions["offsite_conversion.fb_pixel_lead"]     → actions_lead (alt lead-gen path)
  actions["complete_registration"]   → actions_complete_registration (SaaS)
  costPerConversion                  → cost_per_action_type_<event>
  purchaseValue, roas                → bonus fields (not in Windsor schema)
  campaignName                       → campaign
  status                             → campaign_effective_status

Compute account totals from the timeline rows:
  account_totals.spend_sgd  = sum(rows[].spend)        // payload field is named `spend_sgd` per template contract; value is in the account's reporting currency
  account_totals.lp_views   = sum(rows[].actions.landing_page_view)
  account_totals.leads      = sum(rows[].actions.lead)
  account_totals.video_views = sum(rows[].actions.video_view)
  last_spend_date           = max(date) where spend > 0
  days_dark                 = today − last_spend_date (in days)

Set in intermediate JSON: "source": "zernio_fallback"
Set in email flags.notes: "⚠️ Windsor.ai unavailable — Meta Ads data sourced from Zernio (campaign metrics are lifetime; ad-set MTD breakdown not available via timeline)"
```

⚠️ **If `${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID` is not set:** skip fallback and set `all_campaigns_paused: true` (NOT `no_active_campaigns: true` — see template gotcha in Phase 3 Step 2) with note "Meta Ads data unavailable — Windsor.ai offline and no Zernio ads account ID configured."

#### Common to both paths

⚠️ Data is near-real-time — no lag. Use yesterday's date as the report date; today's data may be partial.

- **Currency:** Meta `spend` is USD. Convert to the brand's local currency using the exchange rate from `brands/{brand}/brand.md`.
- **Date resolution:** Use the brand's timezone from `brands/{brand}/brand.md` for dates.
- Record which path was used in the intermediate JSON (`meta_ads.source: "meta_ads_mcp" | "windsor"`) so the dashboard knows whether ad-set / conversion gaps are real or just a fallback artifact.

### Step 2 — Analyze Meta Ads

Meta CTR benchmarks (video/social ads):
| Metric | Watch For |
|---|---|
| CTR | < 1% = low for video TOF; < 0.5% = urgent |
| LP View Rate | < 25% = page load issue; > 40% = strong |
| Frequency | > 2.5 = audience fatigue, rotate creative |
| CPM | Spike >30% day-over-day = auction pressure |
| Learning phase | Each ad set needs ~50 conversion events to exit |

Compute DoD deltas (same format: ▲/▼/—).

### Step 2b — Pull GA4 Sessions for Meta Traffic

Pull GA4 data filtered to Meta paid traffic for the same date range:

```
Use Windsor.ai MCP tool `get_data`:
- source: "googleanalytics4"
- date_preset: "last_30dT"
- fields: ["date", "session_source_medium", "sessions", "bounce_rate"]
- Filter: session_source_medium contains "meta / paid_social"
```

⚠️ **Invalid fields** (not in Windsor for GA4): `source`, `session_source`, `session_medium` — use only `session_source_medium`.

### Step 2c — Compute Full Funnel (Meta Ads → GA4)

Cross-reference Meta Ads clicks with GA4 sessions from Meta paid traffic:

| Metric | Formula | Benchmark |
|---|---|---|
| Click-to-Session Rate | GA4 paid_social sessions / Meta clicks | Good: 80-90%, Warn: 70-80%, Critical: <70% |
| Weighted Bounce Rate | sum(sessions × bounce_rate) / total_sessions | Warn: >85%, Critical: >90% |

⚠️ **Zero paid traffic alert:** If GA4 shows 0 sessions from `meta / paid_social` for 3+ consecutive days, flag as critical: "Meta paid traffic not reaching site — check UTM parameters, pixel, or landing page."

### Step 3 — Save Intermediate JSON

Save to `tmp/meta-{YYYY-MM-DD}.json` where the date is **yesterday's date**.

**Both paths populate the same JSON shape.** Windsor's field names differ from the Meta Ads MCP's, but the data covers the same dimensions (ad-set, ad, lp_views, video_views, conversions). Map Windsor's `adset_name` → `ad_sets[].name`, `ad_name` → `ads[].name`, `actions_landing_page_view` → `lp_views`, `actions_video_view` → `video_views`, and the brand's chosen `actions_*` conversion field → conversion fields.

**Always set the `source` field inside the `meta_ads` block** — `"windsor"` (default path) or `"meta_ads_mcp"` (opt-in path). The dashboard uses this to know which field-name space the data came from when surfacing data-quality alerts. If the run started on the MCP path but failed over to Windsor, set `"source": "windsor"` (the source of the *data actually used*, not the path attempted first).

```json
{
  "report_date": "YYYY-MM-DD",
  "generated_at": "ISO timestamp",
  "meta_ads": {
    "source": "meta_ads_mcp | windsor",
    "no_active_campaigns": false,
    "account_totals": {
      "spend_usd": 0.0,
      "spend_sgd": 0.0,
      "clicks": 0,
      "impressions": 0,
      "ctr_pct": 0.0,
      "reach": 0,
      "cpa_sgd": 0.0
    },
    "account_dod": { "spend": "▲ +5%", "clicks": "▼ -8%", "reach": "—", "ctr": "—", "impressions": "—" },
    "campaigns": [
      {
        "name": "", "impr": 0, "clicks": 0, "ctr_pct": 0.0,
        "spend_sgd": 0.0, "reach": 0, "dod": ""
      }
    ],
    "ad_sets": [],
    "ads": [],
    "flags": {
      "urgent": ["flag text"],
      "optimize": ["flag text"],
      "monitoring": ["flag text"]
    }
  }
}
```

**`ad_sets` and `ads` arrays:** On Path A, populate from the MCP response (Meta's Marketing API returns ad-set and ad-level breakdowns). On Path B, populate by aggregating Windsor rows on `adset_name` / `adset_id` and `ad_name` / `ad_id`. If either path genuinely returns no ad-set / ad rows for a brand (e.g. account uses Advantage+ campaigns with the breakdowns hidden), leave the arrays empty — the template renders "No ad set data available." gracefully.

After saving, log to `memory/YYYY-MM-DD.md`:
```markdown
## meta-data-pull — [ISO timestamp]
- Report date: [date]
- Meta Ads: Spend [currency] [x] (USD [x]) / [clicks] clicks / [reach] reach
- Saved: tmp/meta-[date].json
```

---

## Phase 2.5 — LinkedIn Ads Data Pull (`linkedin-data-pull`, optional)

**Runs only when both `${BRAND}_ZERNIO_LINKEDIN_ADS` and `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set.** If either is missing, skip this phase silently — the brand likely does not run LinkedIn Ads. The Email Stitcher (Phase 3) tolerates an absent `tmp/linkedin-{YYYY-MM-DD}.json`.

### Step 1 — Pull LinkedIn Ads Data

Pull LinkedIn Ads data via **Windsor.ai MCP** connector.

```
Use Windsor.ai MCP tool `get_data`:
- source: "linkedin"
- date_preset: "last_30dT"
- fields: [
    "date",
    "campaign", "campaign_status",
    "clicks", "impressions", "ctr", "cost", "cpm", "cpc",
    "conversions", "cpa",
    "lead_form_opens", "lead_form_completions"
  ]
```

Pull data for **two dates** — yesterday + the day before for DoD comparison.

⚠️ **Known issues:**
- `cost` is returned in the LinkedIn ad account's local currency (same convention as Google Ads — no USD conversion needed)
- LinkedIn-native conversion events (`externalWebsiteConversions`, `qualifiedLeads` in the underlying API) surface in Windsor as `conversions` / `qualified_leads` — confirm field names at query time via `get_fields` if anything returns null
- LinkedIn Ads data is near-real-time — no lag adjustments

#### Windsor fallback — LinkedIn Ads

If Windsor.ai `get_data` with `source: "linkedin"` errors **or** returns 0 rows for the target date, fall back to Zernio:

```
Log: "Windsor.ai unavailable — falling back to Zernio for LinkedIn Ads"

1. Call ad_campaigns_get_ads_timeline (date-filterable account totals):
   - account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS
   - ad_account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS_CID
   - from_date: day_before_yesterday (YYYY-MM-DD)
   - to_date: yesterday (YYYY-MM-DD)
   - platform: "linkedin"
   → Returns daily rows: { date, spend, impressions, clicks, ctr, cpc, cpm, conversions, costPerConversion, externalWebsiteConversions, qualifiedLeads, costInLocalCurrency }

2. Call ad_campaigns_list_ad_campaigns for campaign metadata (lifetime metrics — no date filter):
   - account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS
   - ad_account_id: ${BRAND}_ZERNIO_LINKEDIN_ADS_CID
   - platform: "linkedin"
   - limit: 100
   ⚠️ No from_date/to_date params — `metrics.spend` is LIFETIME since campaign creation. Use timeline for date-filtered totals; use this tool only for campaign-level metadata (names, status, budget).
   → Returns campaigns with AdMetrics + { campaignName, status, currency, budget }

Field mapping — Zernio → Windsor schema:
  spend / costInLocalCurrency        → cost                  (native currency)
  ctr, cpc, cpm, clicks, impressions → direct
  externalWebsiteConversions         → conversions
  qualifiedLeads                     → qualified_leads
  costPerConversion                  → cpa
  campaignName                       → campaign
  status                             → campaign_status

Set in intermediate JSON: "source": "zernio_fallback"
Set in email flags.notes: "⚠️ Windsor.ai unavailable — LinkedIn Ads data sourced from Zernio"
```

⚠️ Both `account_id` (Zernio SocialAccount `_id`) and `ad_account_id` (LinkedIn sponsored account ID, numeric — e.g. `517258773`) are required. Passing only `account_id` returns empty results.

⚠️ **If either `${BRAND}_ZERNIO_LINKEDIN_ADS` or `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` is not set:** do not run this phase at all. LinkedIn Ads is opt-in per brand — most brands skip it.

⚠️ **If Zernio returns 429 with `retryDelay`:** note in `flags.notes` "⚠️ LinkedIn Ads rate-limited via Zernio — retry after Xs" and continue. Do not block waiting for the retry window.

### Step 2 — Analyze LinkedIn Ads

LinkedIn CTR benchmarks (B2B / sponsored content):
| Metric | Watch For |
|---|---|
| CTR | < 0.4% = low; > 0.65% = strong |
| CPC | LinkedIn CPCs run 3–5× Google Search — flag spikes > 25% DoD |
| CPM | $30–$80 typical for B2B; spikes > 30% DoD = auction pressure |
| Lead form completion rate | < 10% on opened forms = friction; > 25% = strong |
| Conversion Rate | Drop > 15% vs 7-day avg |

Compute DoD deltas (same format: ▲/▼/—).

### Step 3 — Save Intermediate JSON

Save to `tmp/linkedin-{YYYY-MM-DD}.json` where the date is **yesterday's date**.

```json
{
  "report_date": "YYYY-MM-DD",
  "generated_at": "ISO timestamp",
  "linkedin_ads": {
    "source": "windsor | zernio_fallback",
    "no_active_campaigns": false,
    "account_totals": {
      "spend_local": 0.0,
      "spend_sgd": 0.0,
      "clicks": 0,
      "impressions": 0,
      "ctr_pct": 0.0,
      "conversions": 0,
      "qualified_leads": 0,
      "cpa_sgd": 0.0
    },
    "account_dod": { "spend": "▲ +5%", "clicks": "▼ -8%", "ctr": "—", "cpa": "—" },
    "campaigns": [
      {
        "name": "", "impr": 0, "clicks": 0, "ctr_pct": 0.0,
        "spend_local": 0.0, "conversions": 0, "qualified_leads": 0, "dod": ""
      }
    ],
    "flags": {
      "urgent": ["flag text"],
      "optimize": ["flag text"],
      "monitoring": ["flag text"]
    }
  }
}
```

`spend_local` is in the LinkedIn ad account's billing currency (LinkedIn `cost` is not USD-normalized). Use the brand's exchange rate from `brands/{brand}/brand.md` to compute `spend_sgd` (or whatever the brand's reporting currency is).

After saving, log to `memory/YYYY-MM-DD.md`:
```markdown
## linkedin-data-pull — [ISO timestamp]
- Report date: [date]
- LinkedIn Ads: Spend [currency] [x] / [clicks] clicks / [conversions] conv / [qualified_leads] QLs
- Saved: tmp/linkedin-[date].json
```

---

## Phase 3 — Email Stitcher (`paid-ads-email-sender`)

Runs 15 minutes after Phase 1 & 2 start.

### Step 1 — Load Intermediate Files

Determine yesterday's date. Look for:
- `tmp/gads-{YYYY-MM-DD}.json` (required)
- `tmp/meta-{YYYY-MM-DD}.json` (required)
- `tmp/linkedin-{YYYY-MM-DD}.json` (optional — present only when the brand runs LinkedIn Ads)

**If one or both required files are missing:** Wait 2 minutes and retry once. If still missing after retry, send email anyway with a note: `⚠️ [Google Ads / Meta Ads] data unavailable — data pull job did not complete in time.` Use an empty/paused placeholder section for the missing platform.

**The LinkedIn file is opt-in.** If it is absent, send the email without a LinkedIn section — do **not** retry, wait, or emit a warning. Its presence/absence determines whether the LinkedIn block renders. If it is present, include the `linkedin_ads` block in the email payload alongside `google_ads` and `meta_ads`.

### Step 2 — Build Email JSON Payload

Email title: **"📊 Paid Ads Daily Brief — [DD Mon YYYY]"**

⚠️ **Do NOT generate HTML.** Build a JSON object with the data below. The server-side template (`paid-ads-brief.ts`) handles all rendering, styling, tables, and layout.

⚠️ **CRITICAL template gotcha — `no_active_campaigns`:** Setting `meta_ads.no_active_campaigns: true` causes the template to skip rendering the entire Meta summary box. Set it to `true` ONLY if there are literally zero campaigns in the account (account is empty). For "all campaigns currently paused but campaigns exist", set `no_active_campaigns: false` and use the separate `all_campaigns_paused: true` field to convey pause state. Same applies to LinkedIn.

Build the JSON payload from the intermediate files. The structure matches `fiveagents_log_run` metrics with these additional top-level fields:

```json
{
  "date": "YYYY-MM-DD",
  "brief_type": "daily",
  "report_date": "DD Mon YYYY",
  "brand": "{brand}",
  "currency": "<read from brands/{brand}/brand.md — e.g. Rp, SGD, USD>",
  "generated_at": "ISO timestamp",
  "google_ads": {
    "source": "windsor | zernio_fallback",
    "all_campaigns_paused": false,
    "account_totals": {
      "spend_sgd": 0,
      "clicks": 0,
      "impressions": 0,
      "ctr_pct": 0,
      "cpc_sgd": 0,
      "conversions": 0,
      "cpa_sgd": null,
      "conversions_note": "Sourced from GA4 — primary conversion event defined in brands/{brand}/funnel.md. Google Ads conversion tracking is not wired to Zernio (returns 0)."
    },
    "account_dod": { "spend": "▲ +5%", "clicks": "▼ -8%", "conv": "—", "ctr": "—", "cpa": "—", "impressions": "—" },
    "campaigns": [{ "name": "", "status": "active | paused", "spend_sgd": 0, "clicks": 0, "impr": 0, "ctr_pct": 0, "cpc_sgd": 0, "conv": 0, "cpa_sgd": null, "dod": "" }],
    "ad_groups": [{ "name": "", "campaign": "", "status": "", "clicks": 0, "impr": 0, "ctr_pct": 0, "cpc_sgd": 0, "cost_sgd": 0, "dod": "" }],
    "ads": [{ "headline_1": "", "campaign": "", "ad_group": "", "clicks": 0, "impr": 0, "ctr_pct": 0, "cost_sgd": 0, "conv": 0, "dod": "" }],
    "keywords": [{ "keyword": "", "campaign": "", "clicks": 0, "ctr_pct": 0, "cost_sgd": 0, "conv": 0, "dod": "" }],
    "flags": { "urgent": [], "optimize": [], "monitoring": [] },
    "notes": ["any data warnings, e.g. 'GA4 data unavailable via Windsor.ai'"],
    "top_recommendation": ""
  },
  "meta_ads": {
    "source": "meta_ads_mcp | windsor | zernio_fallback",
    "no_active_campaigns": false,
    "all_campaigns_paused": false,
    "last_spend_date": "YYYY-MM-DD",
    "days_dark": 0,
    "account_totals": {
      "spend_sgd": 0,
      "spend_usd": null,
      "clicks": 0,
      "impressions": 0,
      "ctr_pct": 0,
      "cpc_sgd": 0,
      "reach": 0,
      "lp_views": 0,
      "leads": 0,
      "video_views": 0,
      "cpa_sgd": null
    },
    "account_dod": { "spend": "", "clicks": "", "reach": "", "ctr": "", "impressions": "" },
    "campaigns": [
      {
        "name": "",
        "status": "active | paused",
        "objective": "",
        "optimization": "",
        "spend_sgd_lifetime": 0,
        "impressions_lifetime": 0,
        "clicks_lifetime": 0,
        "lp_views_lifetime": 0,
        "leads_lifetime": 0,
        "note": "Lifetime since campaign start — ad_campaigns_list_ad_campaigns is not date-filterable. For period totals use account_totals (from ad_campaigns_get_ads_timeline)."
      }
    ],
    "ad_sets": [],
    "ads": [],
    "flags": { "urgent": [], "optimize": [], "monitoring": [] }
  },
  "ga4": {
    "date": "YYYY-MM-DD",
    "period": "YYYY-MM-DD to YYYY-MM-DD",
    "sessions_total": 0,
    "paid_search_sessions": 0,
    "meta_sessions": 0,
    "other_sessions": 0,
    "funnel": {
      "clicks_gads": 0,
      "ga4_sessions_cpc": 0,
      "click_to_session_google_pct": 0,
      "clicks_meta": 0,
      "ga4_sessions_meta": 0,
      "click_to_session_meta_pct": 0
      // Then add one key per funnel stage defined in brands/{brand}/funnel.md
      // (event counts) plus one *_rate_pct per stage transition (computed rates).
      // Do NOT hardcode event names here — each brand has different key events.
    },
    "funnel_flags": []
  },
  "linkedin_ads": {
    "source": "windsor | zernio_fallback",
    "no_active_campaigns": false,
    "account_totals": { "spend_local": 0, "spend_sgd": 0, "clicks": 0, "impressions": 0, "ctr_pct": 0, "conversions": 0, "qualified_leads": 0, "cpa_sgd": 0 },
    "account_dod": { "spend": "", "clicks": "", "ctr": "", "cpa": "" },
    "campaigns": [{ "name": "", "impr": 0, "clicks": 0, "ctr_pct": 0, "spend_local": 0, "conversions": 0, "qualified_leads": 0, "dod": "" }],
    "flags": { "urgent": [], "optimize": [], "monitoring": [] }
  },
  "top_recommendation": "Single most impactful action — name the specific campaign/ad set."
}
```

⚠️ **The `linkedin_ads` block is included only when `tmp/linkedin-{YYYY-MM-DD}.json` exists.** Omit the entire key when the LinkedIn JSON is absent (opt-in per brand); the server-side template renders the LinkedIn section conditionally on the key's presence.

**Analysis guidelines** (apply when writing flags and top_recommendation):
- Do NOT flag a funnel-stage anomaly on a single day's data — require 3+ consecutive days before raising the flag. (Applies to any stage defined in `brands/{brand}/funnel.md`, not a specific signup form.)
- On Day 1–3 of Meta: focus on learning phase signals.
- On Google Ads paused days: recommendation should focus on Meta or pre-reactivation prep.
- Tone: direct, expert, no fluff. Name specific campaigns.

**Currency:** Read from `brands/{brand}/brand.md`. The template uses the `currency` field for all money labels.

**For weekly briefs:** Set `"brief_type": "weekly"`, add `"week_start"` and `"week_end"` fields, use `account_wow` / `wow` keys instead of `account_dod` / `dod`.

### Step 3 — Send Email

**Try `fiveagents_send_email` first** (Postmark — requires Basic or Active maintenance plan):

```
fiveagents_send_email({
  fiveagents_api_key: $FIVEAGENTS_API_KEY,
  to: $REPORT_EMAIL,
  subject: "📊 Paid Ads Daily Brief — DD Mon YYYY",
  html_body: JSON.stringify(payload_from_step_2),
  tag: "paid-ads-daily"
})
```

⚠️ **Subject date** must be the report date, not today. Format: `DD Mon YYYY` (e.g., "27 Mar 2026").

⚠️ **`html_body` must be a JSON string** — the server-side template parses it and renders the styled HTML. Do NOT send raw HTML.

⚠️ **`tag` must be exactly `"paid-ads-daily"` or `"paid-ads-weekly"`** — this is how the server routes to the correct template renderer.

**If `fiveagents_send_email` returns 403** ("requires a maintenance plan"), fall back to Gmail MCP:
- Use `gmail_create_draft` to create a draft email with the HTML body
- Tell the user: "Email draft created in Gmail — send manually. Upgrade to a maintenance plan for automated sending via Postmark."

### Step 5 — Notify via Slack

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

Send a DM to the user (user ID: `$SLACK_NOTIFY_USER`) via Slack MCP with a brief summary:

```
📊 [{brand}] Daily Brief Sent — [DD Mon YYYY]
• Google Ads: [currency] [x] spend / [clicks] clicks / [conv] conv
• Meta Ads: [currency] [x] spend / [clicks] clicks / [reach] reach
• LinkedIn Ads (if present): [currency] [x] spend / [clicks] clicks / [QLs] qualified leads
• GA4: [paid_search] paid search / [meta] meta sessions / [primary_conv_count] [primary_conv_label]   ← read from brands/{brand}/funnel.md
• 🔴 Top flag: [most urgent flag]
• 💡 Top rec: [one-line recommendation]
```

Omit the LinkedIn line if `tmp/linkedin-{YYYY-MM-DD}.json` is absent.

Use `slack_send_message` with `channel_id: "$SLACK_NOTIFY_USER"`.

### Step 6 — Log to Memory

Append to `memory/YYYY-MM-DD.md`:

```markdown
## Paid Ads Daily Brief — [ISO timestamp]
- Skill: digital-marketing-analyst (stitcher)
- Report period: [date]
- Google Ads: [status] / Spend [currency] [x] / [clicks] clicks / [conv] conv / CPA [currency] [x]
- Meta Ads: [status] / Spend [currency] [x] (USD [x]) / [clicks] clicks / [reach] reach
- LinkedIn Ads (if present): [status] / Spend [currency] [x] / [clicks] clicks / [conv] conv / [QLs] qualified leads
- GA4: [paid_search_sessions] paid search sessions / [meta_sessions] meta sessions / [primary_conv_count] [primary_conv_label] / [secondary_conv_count] [secondary_conv_label]   ← read primary/secondary conversion events + labels from brands/{brand}/funnel.md; omit secondary if the brand only defines one
- Key flags: [top 2-3 urgent]
- Top recommendation: [the one action]
- Email sent: $REPORT_EMAIL
- Gmail message_id: [id]
```

Omit the LinkedIn line if `tmp/linkedin-{YYYY-MM-DD}.json` is absent.

---

## Weekly Workflow

The weekly brief uses the same job architecture as the daily brief, with an optional LinkedIn job:

| Job | Cron | What it does | Output |
|---|---|---|---|
| `gads-weekly-data-pull` | Sat cron schedule | Google Ads + GA4 weekly pull + analysis | `tmp/gads-weekly-{week_end}.json` |
| `meta-weekly-data-pull` | Sat cron schedule | Meta Ads weekly pull + analysis | `tmp/meta-weekly-{week_end}.json` |
| `linkedin-weekly-data-pull` *(optional — only when `${BRAND}_ZERNIO_LINKEDIN_ADS` + `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set)* | Sat cron schedule | LinkedIn Ads weekly pull + analysis | `tmp/linkedin-weekly-{week_end}.json` |
| `paid-ads-weekly-email-sender` | Sat cron schedule + 15min | Reads all available JSONs, builds JSON payload, sends via Postmark | Email to $REPORT_EMAIL |

**JSON schema:** same as daily — use `wow` key instead of `dod` in all campaign/ad/keyword rows. Add `week_start` and `week_end` fields at root level. The LinkedIn weekly JSON follows the same shape as the daily `linkedin_ads` block.

Run this workflow when triggered by `gads-weekly-data-pull`, `meta-weekly-data-pull`, or `linkedin-weekly-data-pull` (Saturdays at cron schedule). The LinkedIn weekly job only runs for brands that have both LinkedIn env vars set.

**Week definition:** Sunday–Saturday. On Saturday morning, report covers the full past week (last Sunday to yesterday/Friday).

⚠️ **Data reliability:** If `brands/{brand}/funnel.md` defines a `ga4_clean_data_start` date and `week_start` falls before it, clamp `week_start` to that date. Skip the check if the brand's funnel.md doesn't set one.

⚠️ **Never fall back to a prior week's data.** If Google Ads Sheets or Meta API return zero for this week's date range, report both as "No Active Campaigns" for the week — do not substitute data from a previous week. Both platforms must cover the **same date range**. Zero spend for the week is valid data.

---

### Step 1 — Pull Weekly Google Ads Data

Pull weekly Google Ads data via **Windsor.ai MCP**:

```
Use Windsor.ai MCP tool `get_data`:
- source: "google_ads"
- date_preset: "last_30dT"
- fields: ["date", "campaign", "campaign_status", "ad_group", "clicks", "impressions", "ctr", "cost", "conversions", "cpa"]
```

Filter results for the target week range. Also pull prior week for WoW comparison.

**Windsor fallback — weekly Google Ads:** if Windsor errors or returns 0 rows for the target week, call `ad_campaigns_get_ads_timeline` (account_id: `${BRAND}_ZERNIO_GOOGLE_ADS`, ad_account_id: `${BRAND}_ZERNIO_GOOGLE_ADS_CID`, platform: "google", `from_date`: week_start, `to_date`: week_end + prior week) + `ad_campaigns_get_ad_tree` (same IDs + `from_date`/`to_date`, platform: "google", limit: 100 — paginate if needed) for campaign → ad-group hierarchy. Use `ad_campaigns_list_ad_campaigns` only for campaign metadata (its metrics are lifetime — no date filter). **Both** env vars are required — passing only `account_id` returns empty results. Apply the same field mapping as the daily fallback (including `adSets[]` → ad-groups, conversions sourced from GA4 since Zernio returns 0). Set `"data_source": "zernio_fallback"` in the weekly JSON. GA4 has no fallback — mark as unavailable.

### Step 1b — Pull Weekly Meta Ads Data

**Branch on `META_ADS_SOURCE`** — same rule as Phase 2 Step 1 in the daily flow:

- **Default (env var unset)** — Pull via **Windsor.ai** with `source: "facebook"` using the field set documented in Phase 2 Step 1 (campaign / `adset_name` / `ad_name` / `clicks` / `impressions` / `ctr` / `spend` / `reach` / `frequency` / `cpm` / `cpc` / `actions_landing_page_view` / `actions_video_view` / brand-specific `actions_*` conversion field). `date_preset: "last_30dT"`. Pull the target week plus the prior week for WoW comparison.
- **Opt-in (`META_ADS_SOURCE=meta_ads_mcp`)** — Pull via the **Meta Ads MCP** custom connector (`https://mcp.facebook.com/ads`). Request campaign-level fields (campaign, clicks, impressions, ctr, spend, reach) plus drill-down (ad_set, ad, lp_views, conversions, cpm, frequency) for the target week range, plus the prior week for WoW comparison. On MCP error, fall back to the Windsor path.
- **Windsor/MCP both unavailable** — Fall back to Zernio: `ad_campaigns_get_ads_timeline` (account_id: `${BRAND}_ZERNIO_META_ADS_ACCOUNT_ID`, platform: "facebook", `from_date`: week_start, `to_date`: week_end + prior week) is the ONLY reliable date-filtered source. Use `ad_campaigns_list_ad_campaigns` only for campaign metadata (its metrics are lifetime — no date filter; label as `spend_sgd_lifetime` in the payload with a `note` field). Apply same field mapping as daily Phase 2 fallback. Set `"source": "zernio_fallback"` in weekly JSON.

Filter for the target week. Convert USD spend to the brand's local currency using the exchange rate from `brands/{brand}/brand.md`. Include WoW comparison from prior week.

### Step 1c — Pull Weekly GA4 Data

```
Use Windsor.ai MCP tool `get_data`:
- source: "googleanalytics4"
- date_preset: "last_30dT"
- fields: ["date", "session_source_medium", "sessions", "bounce_rate"]
```

Filter for the target week range.

### Step 1d — Pull Weekly LinkedIn Ads Data (optional)

**Runs only when both `${BRAND}_ZERNIO_LINKEDIN_ADS` and `${BRAND}_ZERNIO_LINKEDIN_ADS_CID` are set.** Skip the step entirely when either is missing.

Pull via **Windsor.ai** with `source: "linkedin"` using the field set from Phase 2.5 Step 1 (`date` / `campaign` / `campaign_status` / `clicks` / `impressions` / `ctr` / `cost` / `cpm` / `cpc` / `conversions` / `cpa` / `lead_form_opens` / `lead_form_completions`). `date_preset: "last_30dT"`. Pull the target week plus the prior week for WoW comparison.

**Windsor fallback — weekly LinkedIn Ads:** if Windsor errors or returns 0 rows, call `ad_campaigns_get_ads_timeline` (account_id: `${BRAND}_ZERNIO_LINKEDIN_ADS`, ad_account_id: `${BRAND}_ZERNIO_LINKEDIN_ADS_CID`, platform: "linkedin", `from_date`: week_start, `to_date`: week_end + prior week) for date-filtered totals + `ad_campaigns_list_ad_campaigns` (same IDs and platform) for campaign metadata only (its metrics are lifetime — no date filter). Both env vars are required — passing only `account_id` returns empty results. Apply the same field mapping as the daily Phase 2.5 fallback. Set `"source": "zernio_fallback"` in the weekly LinkedIn JSON.

Filter for the target week. Include WoW comparison from prior week. LinkedIn `cost` is already in the ad account's local currency.

### Step 2 — Analyze Weekly Performance

- Compare this week vs last week (WoW) for all metrics
- Flag consistently underperforming keywords/ads across the week
- Identify budget pacing issues and learning phase status for Meta
- Note if Meta ad sets exited learning phase (need ~50 conversion events each)

### Step 3 — Build Weekly JSON Payload

Same JSON structure as daily (see Step 2 above) with these differences:
- `"brief_type": "weekly"`
- Add `"week_start": "YYYY-MM-DD"` and `"week_end": "YYYY-MM-DD"` at root
- Use `account_wow` instead of `account_dod` in google_ads/meta_ads
- Use `wow` instead of `dod` in all campaign/ad/keyword rows

The server-side template automatically handles WoW labels, "Fix Before Next Week" flag labels, and "Top Recommendation for Next Week" heading based on `brief_type`.

### Step 4 — Send Weekly Email

```
fiveagents_send_email({
  fiveagents_api_key: $FIVEAGENTS_API_KEY,
  to: $REPORT_EMAIL,
  subject: "📊 Paid Ads Weekly Brief — Week of DD Mon YYYY",
  html_body: JSON.stringify(payload_from_step_3),
  tag: "paid-ads-weekly"
})
```

**If 403**, fall back to `gmail_create_draft` (same as daily Step 3 fallback).

### Step 6 — Notify via Slack

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

DM the user (`$SLACK_NOTIFY_USER`) via Slack MCP:

```
📊 [{brand}] Weekly Brief Sent — Week of [DD Mon YYYY]
• Google Ads: [currency] [x] spend / [clicks] clicks / [conv] conv / WoW: [+/-x%] spend
• Meta Ads: [currency] [x] spend / [clicks] clicks / [reach] reach / WoW: [+/-x%] spend
• LinkedIn Ads (if present): [currency] [x] spend / [clicks] clicks / [QLs] qualified leads / WoW: [+/-x%] spend
• GA4: [sessions] sessions / [primary_conv_count] [primary_conv_label]   ← read from brands/{brand}/funnel.md
• 🔴 Top flag: [most urgent flag]
• 💡 Top rec for next week: [one-line recommendation]
```

Omit the LinkedIn line if `tmp/linkedin-weekly-{week_end}.json` is absent.

### Step 7 — Log to Memory

```markdown
## Paid Ads Weekly Brief — [ISO timestamp]
- Skill: digital-marketing-analyst (weekly)
- Report period: [week_start] to [week_end]
- Google Ads: [status] / Spend [currency] [x] / [clicks] clicks / [conv] conv / CPA [currency] [x] / WoW: [+/-x%]
- Meta Ads: [status] / Spend [currency] [x] (USD [x]) / [clicks] clicks / [reach] reach / WoW: [+/-x%]
- LinkedIn Ads (if present): [status] / Spend [currency] [x] / [clicks] clicks / [conv] conv / [QLs] qualified leads / WoW: [+/-x%]
- GA4: [sessions] sessions / [primary_conv_count] [primary_conv_label] / [secondary_conv_count] [secondary_conv_label]   ← read primary/secondary conversion events + labels from brands/{brand}/funnel.md; omit secondary if the brand only defines one
- WoW: Spend [+/-x%] / Conv [+/-x%] / CPA [+/-x%]
- Key flags: [top 2-3]
- Top recommendation for next week: [the one action]
- Email sent: $REPORT_EMAIL
- Gmail message_id: [id]
```

Omit the LinkedIn line if `tmp/linkedin-weekly-{week_end}.json` is absent.

---

## Notes

- **Data sources:** Google Ads, GA4, and Meta Ads (Facebook + Instagram) data are all pulled via the **Windsor.ai MCP** connector (`get_data` tool) by default — Windsor is the universal source for every brand. When `META_ADS_SOURCE=meta_ads_mcp` (the user opted into the optional Meta Ads custom connector at `https://mcp.facebook.com/ads`), Meta data is pulled from the MCP instead, with automatic fallback to Windsor on MCP error. Both Meta paths cover the same dimensions — campaign / ad-set / ad / lp_views / video_views / conversions — under different field names; see the field map in Phase 2 Step 1. Always record `meta_ads.source` in the JSON so the dashboard knows which field-name space the data came from.
- **Email sending:** Use `fiveagents_send_email` (Postmark, requires Basic/Active maintenance plan). Falls back to `gmail_create_draft` if client has no maintenance plan (403).
- **Data lag:** Windsor.ai (Google Ads, GA4, Meta) and the Meta Ads MCP are all near-real-time — no significant lag. For Windsor calls, always use `last_30dT` (not `last_30d`) so today's UTC data is included. Report on yesterday's date; today may be partial.
- **Currency:** Google Ads cost is in the account's local currency. Meta Ads spend is USD — convert using the exchange rate from `brands/{brand}/brand.md`.
- GA4 clean data start: read `ga4_clean_data_start` from `brands/{brand}/funnel.md` if set (e.g. when a tracking bug or migration left pre-cutoff data unreliable). If the brand defines one, never pull or compare pre-cutoff data; otherwise no clamp.
- Brand-specific known issues should be documented in `brands/{brand}/funnel.md` notes section.
- If one platform has no data yet, still send email with available data. Note the gap.
- Future data sources to add: TikTok Ads (when an official MCP becomes available)

---

---

## Phase 4 — Ads Actions (optional, after analysis)

After the daily or weekly brief is sent, the skill can act on the flags it just raised. This phase runs when:
- The user explicitly asks to apply a recommendation (e.g. "pause that campaign", "boost this post"), **or**
- The skill is invoked with `--auto-optimize` (reserved for future automation)

**Autonomy rule:** Always confirm before taking destructive actions (pause, delete, status changes). Read-only actions (analytics drill-down, targeting research, comments) run immediately.

### Step 1 — Resolve Zernio ad accounts

If not already cached in `brands/{brand}/ads.md`, call:

```
ads_list_ad_accounts
```

to discover all connected Zernio ad accounts (Meta, Google, TikTok, LinkedIn) for the brand. Store the relevant account IDs for use in subsequent steps.

### Step 2 — Apply flags as actions

Based on `flags.urgent` and `flags.optimize` from the analysis, offer these actions:

| Situation | Action | Tool |
|---|---|---|
| Campaign wasting spend (high cost, 0 conv) | Pause campaign | `ad_campaigns_update_ad_campaign_status` |
| Multiple bad campaigns | Bulk pause | `ad_campaigns_bulk_update_ad_campaign_status` |
| Ad set audience fatigue (frequency > 2.5) | Pause ad set | `ad_campaigns_update_ad_set_status` |
| Campaign budget needs adjustment | Update budget | `ad_campaigns_update_ad_campaign` |
| Winning ad to duplicate | Duplicate | `ad_campaigns_duplicate_ad_campaign` |
| Ad creative comments review (dark posts) | Fetch comments | `ads_get_ad_comments` |
| Drill-down on specific ad performance | Ad-level analytics | `ads_get_ad_analytics` (requires `ad_id`; `from_date`/`to_date` = report period) |

### Step 3 — Targeting research (when user asks to expand or change targeting)

```
ads_search_ad_interests   — find interest targeting options by keyword
ads_search_ad_targeting   — find location targeting by name/country
```

### Step 4 — Boost post (when analysis identifies a top organic post worth promoting)

```
ads_boost_post
```

Confirm with user: post ID, target audience, budget, duration.

### Step 5 — CTWA ad (when brand has WhatsApp and user requests a Click-to-WhatsApp campaign)

```
ads_create_ctwa_ad
```

Confirm with user: ad creative, WhatsApp number, target audience.

### Step 6 — Conversion tracking audit (when user asks to check or set up tracking)

```
ads_list_conversion_destinations    — list existing pixels / conversion rules
ads_create_conversion_destination   — create a new conversion destination
tracking_tags_list_tracking_tags    — list platform measurement tags (Meta Pixel, etc.)
tracking_tags_get_tracking_tag_stats — check tag health and firing status
tracking_tags_create_tracking_tag   — create a new tracking tag
ads_send_conversions                — relay server-side conversion events to platform APIs
```

---

## Final Step — Log to Dashboard

After the skill completes, log the run to Supabase. The `metrics` JSONB must match the schema in `docs/new_agent_onboarding/metrics-spec.md` — the dashboard renders widgets from these exact key paths.

⚠️ **Critical: populate every field with ACTUAL values computed during this run.** The schema below shows field names and types only — every numeric field must be replaced with the real number from the analysis. Do NOT copy zeros or empty strings. A log entry with zeros is worse than no entry — it overwrites real data with blanks.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "digital-marketing-analyst"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars — shown in activity feed>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "<report_date YYYY-MM-DD>",
    "brief_type": "<daily|weekly>",
    "google_ads": {
      "totals": {
        "spend": <actual total cost in local currency>,
        "clicks": <actual total clicks>,
        "impr": <actual total impressions>,
        "ctr": <actual avg CTR as decimal, e.g. 0.028>,
        "conv": <actual total conversions>,
        "cpa": <actual CPA or null if no conversions>
      },
      "campaigns": [
        {
          "name": "<campaign name>",
          "status": "<ENABLED|PAUSED>",
          "spend": <actual spend>,
          "clicks": <actual clicks>,
          "ctr": <actual ctr>,
          "conv": <actual conversions>,
          "cpa": <actual cpa or null>
        }
      ],
      "ad_groups": [
        { "name": "<ad group path>", "campaign": "<campaign name>", "status": "<status>", "clicks": <actual>, "impr": <actual>, "ctr": <actual>, "cost": <actual> }
      ],
      "keywords": []
    },
    "google_ads_funnel": [
      { "stage": "Impressions", "volume": <actual>, "rate": null, "cost_per": null, "benchmark": null, "status": null },
      { "stage": "Clicks", "volume": <actual>, "rate": <ctr decimal>, "cost_per": <actual cpc>, "benchmark": 0.02, "status": "<on_track|watch|critical>" },
      { "stage": "GA4 Sessions", "volume": <actual ga4 cpc sessions>, "rate": <click_to_session_rate>, "cost_per": null, "benchmark": 0.8, "status": "<status>" },
      { "stage": "Conversions", "volume": <actual>, "rate": <conv_rate>, "cost_per": <actual cpa or null>, "benchmark": null, "status": "<status>" }
    ],
    "meta_ads": {
      "totals": {
        "spend": <actual spend in local currency>,
        "clicks": <actual clicks>,
        "impr": <actual impressions>,
        "ctr": <actual ctr decimal>,
        "lp_views": null,
        "cpm": <actual cpm>
      },
      "campaigns": [
        {
          "name": "<campaign name>",
          "impr": <actual>,
          "clicks": <actual>,
          "ctr": <actual>,
          "lp_views": null,
          "lp_rate": null,
          "spend": <actual in local currency>,
          "cpc": <actual>,
          "cpm": <actual>
        }
      ],
      "ad_sets": [],
      "ads": []
    },
    "meta_ads_funnel": [
      { "stage": "Impressions", "volume": <actual>, "rate": null, "cost_per": null, "benchmark": null, "status": null },
      { "stage": "Clicks", "volume": <actual>, "rate": <ctr decimal>, "cost_per": <actual cpc>, "benchmark": 0.01, "status": "<status>" },
      { "stage": "GA4 Sessions (Meta)", "volume": <actual meta ga4 sessions>, "rate": <click_to_session>, "cost_per": null, "benchmark": 0.8, "status": "<status>" }
    ],
    "combined_summary": {
      "primary_conversion_event": "<brand's primary GA4 conversion event name from brands/{brand}/funnel.md — e.g. 'calendly_booked', 'purchase', 'sign_up'>",
      "primary_conversion_label": "<short display label for the dashboard — e.g. 'bookings', 'purchases', 'trials'>",
      "google_ads": { "spend": <actual>, "clicks": <actual>, "lp_views": null, "ga4_sessions": <actual cpc sessions>, "primary_conversions": <count for the brand's primary event, or 0>, "cpa": <actual or null>, "status": "<Active|Paused|No Data>" },
      "meta_ads":   { "spend": <actual>, "clicks": <actual>, "lp_views": null, "ga4_sessions": <actual meta sessions>, "primary_conversions": <count for the brand's primary event, or 0>, "cpa": null, "status": "<Active|Paused|No Data>" },
      "total":      { "spend": <sum of both platforms in local currency>, "clicks": <sum>, "lp_views": null, "ga4_sessions": <sum>, "primary_conversions": <sum> }
    },
    "flags": { "urgent": ["<actual flag text>"], "optimize": ["<actual flag text>"], "monitoring": ["<actual flag text>"] },
    "top_recommendation": "<actual recommendation — name the specific campaign>",
    "gmail_message_id": "<message_id from send step or null>"
  }
```

**Status values:** `success` (all data pulled + email sent), `partial` (one platform missing or email failed), `failed` (skill errored before completion).
**All numeric fields must be numbers, not strings** — the dashboard uses these for DoD/WoW math. `null` is valid when a metric is unavailable (e.g. CPA with 0 conversions). With the Meta Ads MCP, `lp_views` and conversion-derived fields are now expected to be populated whenever the MCP returns them — only set them to `null` if Meta itself returned no value.
