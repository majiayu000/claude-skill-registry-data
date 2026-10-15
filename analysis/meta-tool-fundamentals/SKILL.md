---
name: meta-tool-fundamentals
description: "Foundation tool reference for any Meta (Facebook/Instagram) Ads task — Marketing API quirks, common entity relationships, currency in cents. Used internally when working with Meta tools."
metadata:
  source: "prompts/skills/meta/tool-fundamentals"
---

# Meta Ads - Tool Fundamentals

How to use Meta Ads tools effectively, plus the canonical metric definitions used across all Meta skills. Auto-loaded with every Meta skill request.

## Insights Query Optimization

When using `facebook_get_adaccount_insights`:

**Level selection** — use the highest level that answers the question:
- `account` — total spend, overall ROAS, account-level metrics
- `campaign` — compare campaign performance
- `adset` — analyze targeting/audience performance
- `ad` — individual ad performance, creative analysis

**Field selection** — request only what's needed:
- Basic: `spend`, `impressions`, `clicks`, `ctr`, `cpm`, `cpc`
- With conversions: add `conversions`, `conversion_values`, `purchase_roas`
- With names: add `campaign_name`/`adset_name`/`ad_name` matching the level
- For video: add `video_play_actions`, `video_thruplay_watched_actions`

**Default filtering**: Always apply `filtering=[{"field":"impressions","operator":"GREATER_THAN","value":0}]` unless user wants non-delivered entities.

**Active entity filtering (CRITICAL)**: When analyzing current performance, ALWAYS add an `effective_status` filter to exclude paused/deleted entities. The insights API returns data for ANY entity that had spend in the date range, even if it is now inactive.
- Ad sets: `{"field":"adset.effective_status","operator":"IN","value":["ACTIVE"]}`
- Ads: `{"field":"ad.effective_status","operator":"IN","value":["ACTIVE"]}`
- Campaigns: `{"field":"campaign.effective_status","operator":"IN","value":["ACTIVE"]}`

Combine with impressions filter: `filtering=[{"field":"impressions","operator":"GREATER_THAN","value":0},{"field":"adset.effective_status","operator":"IN","value":["ACTIVE"]}]`

Only omit the `effective_status` filter when the user explicitly asks for historical or paused entity data.

**Default sorting**: Use `sort='spend_descending'` unless user specifies otherwise.

**Breakdowns**: Only include when specifically requested. Each breakdown multiplies result rows exponentially. Available: `age`, `gender`, `country`, `region`, `publisher_platform`, `platform_position`, `device_platform`, `user_segment_key`.

**Creative fatigue analysis**: Use `time_increment='1'` for daily trend data.

**Date range discipline (CRITICAL)**: For fixed historical comparisons (named weeks, calendar months, W1/W2/W3, or exact date ranges), use explicit `time_range` for each period. Do NOT use `date_preset` unless the user explicitly asks for a relative period such as `last_7d`, `last_14d`, `this_month`, or `yesterday`.

## Purchase De-Duplication (CRITICAL)

Facebook returns overlapping purchase action_types: `omni_purchase`, `purchase`, `offsite_conversion.fb_pixel_purchase`, `onsite_web_purchase`, `web_in_store_purchase`, `app_custom_event.fb_mobile_purchase`.

**Rule**: Use ONLY ONE. Check `omni_purchase` first; if absent, fall back to `purchase`. NEVER sum multiple types — this double-counts revenue and inflates ROAS.

## Pagination (CRITICAL)
Meta insights can paginate at ANY level (`account`, `campaign`, `adset`, or `ad`), especially with breakdowns, `time_increment`, or broad date ranges. If any Meta insights response contains `paging.next` or `_gomarble_meta_insights_data_quality.paging_next_present=true`, the response is incomplete.

Before using Meta insights data for totals, rankings, CPA/ROAS, budget allocation, campaign comparisons, or Python/advanced analysis:
1. Call `facebook_fetch_pagination_url` with the exact `paging.next` URL.
2. Continue fetching until the latest response has no `paging.next` and the data-quality block says `response_complete=true`.
3. Only then combine pages and analyze.

Never present totals or conclusions from a partial Meta insights page. If pagination cannot be completed, state that the Meta data is incomplete and avoid numeric conclusions from it.

## Currency
ALL Meta propose tools — `facebook_propose_create_campaign_structure` AND every `facebook_propose_update_*` tool — take budgets/bids in **ACCOUNT CURRENCY, human-readable** (50 means $50, 300 means ₹300). NEVER convert to cents for a propose tool; the server converts. Values from `facebook_get_campaign_details`/adset details are already in account currency too.

Only Meta's RAW response fields — insights and `account_structure` budget fields — are in **cents** ($50 = 5000): divide those by 100 when displaying. Confirm account currency from `facebook_get_details_of_ad_account` before presenting monetary values — never assume USD.

## Account Context
Always call `facebook_get_details_of_ad_account` first. It returns:
- Account currency (for correct monetary display)
- `account_structure` with top 10 spending ads, their campaigns and ad sets
- Use this to find entity IDs and understand what's running before deeper analysis

## Async Insights
If `facebook_get_adaccount_insights` fails with "reduce the amount of data", use `facebook_get_async_adaccount_insights` instead. Same parameters, handles large datasets asynchronously.

## Filtering Guide
- **Status (most important)**: `{"field":"adset.effective_status","operator":"IN","value":["ACTIVE"]}`
- Name matching: `{"field":"campaign.name","operator":"CONTAIN","value":"brand"}`
- Performance threshold: `{"field":"spend","operator":"GREATER_THAN","value":100}`
- Multiple filters combine as AND conditions
- Use `CONTAIN`/`NOT_CONTAIN` for text, `GREATER_THAN`/`LESS_THAN` for numbers, `IN`/`NOT_IN` for multiple values

**Standard filter combo for current performance analysis**:
```json
[
  {"field": "impressions", "operator": "GREATER_THAN", "value": 0},
  {"field": "adset.effective_status", "operator": "IN", "value": ["ACTIVE"]}
]
```

## Metric Glossary

Canonical definitions used across all Meta skills. Workflow skills (`meta-creative-analysis`, `meta-performance-analysis`, `meta-depth-of-analysis`) reference these — they do NOT redefine them.

### Direct Metrics (from API response)

| Metric | API Field | How to Extract |
|---|---|---|
| Spend | `spend` | Direct |
| CPM | `cpm` | Direct |
| CTR | `ctr` | Direct |
| Impressions | `impressions` | Direct |
| Clicks | `clicks` | Direct |
| Reach | `reach` | Direct |
| Frequency | `frequency` | Direct |
| Video Plays | `video_play_actions[0].value` | Initial impressions of the video |
| 3-Second Views | `actions` array, `action_type=video_view` | Hook engagement — NOT a separate field |
| ThruPlays | `video_thruplay_watched_actions[0].value` | 15s+ watch or completion |
| Purchases | `actions` array, `action_type=omni_purchase` (fallback `purchase`) | Use ONE only — see Purchase De-Duplication |
| Leads | `actions` array, `action_type=lead` | |
| Revenue | `action_values` array, `action_type=omni_purchase` | |
| Purchase ROAS | `purchase_roas` | Direct |

### Additive vs Non-Additive Metrics (CRITICAL)

Additive across complete rows at the same date/entity grain: `spend`, `impressions`, `clicks`, action counts, and `action_values` after purchase de-duplication.

Non-additive: `reach`, `frequency`, `ctr`, `cpm`, `cpc`, `cpp`, `purchase_roas`, `cost_per_*`, CPA/CPR/CPL, and other rate/cost fields. Do NOT sum or average row-level `reach` or `frequency` and call it account/campaign/week/month reach or frequency.

For weekly/monthly/account reach or frequency, query `facebook_get_adaccount_insights` at the exact output level (for example `level="account"` for account totals) with explicit `time_range` and no unnecessary breakdown/time_increment. Reach/frequency cannot be recomputed from lower-grain rows.

For rate fields, prefer the API value at the intended grain; otherwise recompute valid rates from additive numerator/denominator fields only after all pages are fetched.

### Calculated Metrics

| Metric | Formula | Notes |
|---|---|---|
| Hook Rate | `(3-sec views / video plays) * 100` | Uses `actions[video_view]`, NOT `video_p25_watched_actions` |
| Hold Rate | `(thruplays / 3-sec views) * 100` | |
| Cost Per Purchase | `spend / actions[purchase].value` | |
| Cost Per Lead (CPL) | `spend / actions[lead].value` | |
| Cost Per Result (CPR) | `spend / actions[<custom_event>].value` | Use the SPECIFIC `custom_event_str` — never `conversions` totals |
| Conversion Rate (CVR) | `actions[<event>].value / clicks * 100` | |
| Budget Utilization | `spend / (daily_budget * days_in_period)` | Daily budget is in cents |
| Campaign Spend Share | `entity_spend / parent_total_spend` | For ad-set comparison; require ≥ 25% before comparing |
| Pareto Set | Sort ads by spend desc; cumulative spend ≤ 90% | These ads drive the majority of activity |

### Video Funnel
```
Video Plays → Hook Rate → 3-Second Views → Hold Rate → ThruPlays
```

### Account Type → Primary Conversion Metric (PCM)

Read `promoted_object.custom_event_type` from the ad set (`facebook_get_details_of_ad_account` returns it for top spenders; otherwise `facebook_get_adset_details`). NEVER infer from campaign or ad set names.

| `custom_event_type` | Account Type | PCM |
|---|---|---|
| `PURCHASE` | E-commerce | Purchase ROAS |
| `LEAD` | Lead Generation | Cost Per Lead |
| `COMPLETE_REGISTRATION` | Registration | Cost Per Registration |
| `OTHER` + `custom_event_str` | Custom Conversion | Cost Per Result for that specific event |

If `promoted_object` is missing → ASK the user. Never assume.
**Mixed accounts**: group ad sets by `custom_event_type` and apply each group's PCM separately.

### Performance Benchmarks

| Metric | Good | Average | Poor |
|---|---|---|---|
| Hook Rate | ≥ 40% | 26–39% | < 25% |
| Hold Rate | > Account Avg + 25% | ≈ Account Avg | < Account Avg |
| CTR | ≥ 1.25% | 0.65 – 1.24% | < 0.65% |
| CPM variance vs Pareto avg | ≤ 20% | 20 – 60% | > 60% |
| PCM variance vs Pareto avg | Above avg | ± 20% | > 30% below |
| Budget utilization | ≥ 85% | — | < 85% |
| Min ad-set spend share for comparison | ≥ 25% of campaign | — | — |

For Hold Rate, compute `account_avg_hold_rate` from a 90-day account-level pull (`facebook_get_adaccount_insights` at `level="account"` with `date_preset="last_90d"` and the video fields) before applying.

### Diagnostic Signals (definitions only — workflow lives in `meta-depth-of-analysis`)

| Signal | Means |
|---|---|
| Frequency rising AND CTR falling over 14+ days | Creative fatigue |
| CBO with one ad set holding 80%+ of budget | Algorithm working as intended — do NOT pause the dominant ad set on small-sample noise |
| High frequency alone (no CTR drop) | Not fatigue |
| Cost cap + rising CPM | Either delivery squeeze or audience saturation — separate before acting |

### Statistical Significance Floors

| Decision | Minimum signal |
|---|---|
| Per-ad-set performance judgment | 3–5 conversions / week |
| Per-segment recommendation (placement, age, device) | ≥ 100 impressions AND ≥ 3 conversions |
| Pause ad on high CPA | ≥ 3 conversions if non-zero, OR spend ≥ 2× ad-set CPA target if zero |
| Ad set learning phase exit | Spend ≥ 2× AOV OR 4× CPA, whichever is higher |
