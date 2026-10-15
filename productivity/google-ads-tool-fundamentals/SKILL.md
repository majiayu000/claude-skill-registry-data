---
name: google-ads-tool-fundamentals
description: "Foundation tool reference for any Google Ads task — GAQL syntax, common entity relationships, default reporting windows. Used internally when working with Google Ads tools."
metadata:
  source: "prompts/skills/google_ads/tool-fundamentals"
---

# Google Ads - Tool Fundamentals

How to use Google Ads tools effectively, plus the canonical metric definitions used across all Google Ads skills. Auto-loaded with every Google Ads skill request.

## Tools

- **`google_ads_run_gaql`**: primary read tool for Google Ads Query Language. Use for any structural or performance pull from `campaign`, `ad_group`, `keyword_view`, `search_term_view`, `asset_group`, `geographic_view`, `shopping_performance_view`, etc.
- **`google_ads_propose_update_*`**: write tools for bid, budget, status, and structural changes (`…_campaigns`, `…_adgroups`, `…_ads`, `…_asset`, `…_bid_modifiers`, `…_negative_keyword_list`, `…_pmax_asset_group`). Money is in account currency, not micros. Always dry-run first and apply only after the user approves.
- **`google_ads_keyword_discover` / `google_ads_keyword_metrics`**: keyword research; volume, CPC, competition, and forecast data.
- **`google_ads_get_change_logs`**: audit account changes within a window.
- **`google_ads_list_accounts`**: discover MCC structure and customer IDs.

## Currency: Micros

Google Ads cost and bid fields are returned in **micros** (1,000,000 micros = 1 unit of the account currency).

| Field | Conversion |
|---|---|
| `metrics.cost_micros` | divide by 1,000,000 to get cost in account currency |
| `cpc_bid_micros` | divide by 1,000,000 |
| `amount_micros` (campaign budget) | divide by 1,000,000 |
| `metrics.average_cpc` | already in account currency — do NOT divide |

Always confirm account currency before showing monetary values; never assume USD.

## Date Filtering

Use GAQL relative ranges where possible — they're more reliable than fixed dates:
- `segments.date DURING LAST_7_DAYS`
- `segments.date DURING LAST_30_DAYS`
- `segments.date DURING LAST_90_DAYS`
- `segments.date DURING THIS_MONTH` / `LAST_MONTH`

For week-over-week or month-over-month comparison, run two queries with different `DURING` clauses and compute deltas locally.

## Status Filtering

Always include `campaign.status = 'ENABLED'` (and `ad_group.status = 'ENABLED'` where relevant) when analyzing current performance — historical paused entities will otherwise pollute aggregates.

## Pagination

GAQL responses can be large. Use `LIMIT` with `ORDER BY metrics.cost_micros DESC` to keep result sizes manageable; default to `LIMIT 200` for entity-level pulls, `LIMIT 100` for breakdown segments.

## Account Context

Always run `google_ads_list_accounts` first to confirm the customer ID and check whether this is an MCC vs a leaf account. For MCC, ask the user which sub-account to operate on.

## Metric Glossary

Canonical definitions used across all Google Ads skills. Workflow skills (`google-ads-search-analysis`, `google-ads-pmax-evaluation`, `google-ads-shopping`, `google-ads-depth-of-analysis`) reference these — they do NOT redefine them.

### Direct Metrics (GAQL `metrics.*`)

| Metric | GAQL Field | Notes |
|---|---|---|
| Cost | `metrics.cost_micros` | Divide by 1e6 |
| Conversions | `metrics.conversions` | Includes all configured conversion actions unless filtered |
| Conversion value | `metrics.conversions_value` | Revenue for value-based conversions |
| Clicks | `metrics.clicks` | |
| Impressions | `metrics.impressions` | |
| Average CPC | `metrics.average_cpc` | Already in account currency |
| CTR | `metrics.ctr` | Decimal (0.05 = 5%) |
| Search IS | `metrics.search_impression_share` | |
| IS Lost (Rank) | `metrics.search_rank_lost_impression_share` | |
| IS Lost (Budget) | `metrics.search_budget_lost_impression_share` | |
| Top of Page Rate | `metrics.search_top_impression_percentage` | |
| Absolute Top Rate | `metrics.search_absolute_top_impression_percentage` | |

### Calculated Metrics

| Metric | Formula | Notes |
|---|---|---|
| CPA | `(cost_micros / 1e6) / conversions` | Cost per conversion in account currency |
| ROAS | `conversions_value / (cost_micros / 1e6)` | Decimal multiple, e.g. 3.5 = 3.5× |
| CVR (Conversion Rate) | `conversions / clicks * 100` | |
| AOV | `total_conversions_value / total_conversions` | Account-level over the same window |
| CPC trend WoW | `(this_week_cpc - last_week_cpc) / last_week_cpc * 100` | Use two relative-date queries |
| CPC trend MoM | `(this_month_cpc - last_month_cpc) / last_month_cpc * 100` | |
| Spend Share | `entity_cost / total_cost * 100` | For prioritization within a campaign or account |

### Account-Type Inference

When the user has not stated account type, infer from data:

- **E-commerce**: `purchase` conversion actions present AND non-zero `metrics.conversions_value` → use ROAS, AOV, CPA
- **Lead gen**: conversions present AND `metrics.conversions_value = 0` → use CPA only; ROAS unreliable unless offline conversion import is configured
- **Mixed**: group campaigns by primary conversion action and apply each group's PCM separately
- **Unclear**: ASK the user. Don't default.

### Maturity & Statistical-Significance Gates

| Gate | Threshold | Rationale |
|---|---|---|
| Smart Bidding minimum (Search) | ≥ 30 conversions / 30 days | Below this, `tCPA`/`tROAS` lacks signal |
| Smart Bidding minimum (PMax / Shopping) | ≥ 50 conversions / 30 days | Wider channel mix needs more signal |
| PMax maturity gate | Age ≥ 30 days (ideally 60) OR conversions ≥ 50 | Required before any PMax optimization |
| Segment-level recommendation | ≥ 50 clicks AND ≥ 5 conversions | Below this → flag as low-confidence |
| Scaling step cap | ≤ 20% per move (search/shopping); ≤ 50% per move on mature PMax | From guardrails / pmax-scaling |
| Lookback for Shopping | 14 days if ≥ 100 purchases / month, else 30 days | |

### PMax vs Search ROAS Comparison

Apply only after the PMax maturity gate passes.

| PMax ROAS Ratio | Assessment | Default Action |
|---|---|---|
| < 0.5× Search ROAS | Poor | Monitor closely; consider pausing if not improving |
| 0.5 – 0.9× Search ROAS | Below par | Optimize assets and negatives before any scaling |
| ≥ 0.9× Search ROAS | Healthy | Optimize, scale eligible |
| > Search ROAS | Outperforming | Prioritize scaling |

### PMax Asset Performance Labels

Google returns `performance_label` per asset (NOT cost / conversion data per asset).

| Label | Interpretation | Default Action |
|---|---|---|
| `BEST` | Top performer in its asset group | Create variations with similar style |
| `GOOD` | Acceptable | Keep, monitor |
| `LOW` | Underperforming | Remove; replace with `BEST` variations |
| `PENDING` / `UNSPECIFIED` | Insufficient data | Wait 14+ days |

### Shopping Item Classification (definitions only — workflow in `google-ads-shopping` skill)

| Classification | Trigger |
|---|---|
| KILL | `cost ≥ 2× AOV` AND `conversions = 0` |
| DOWNGRADE | `ROAS < 0.7× target` AND `cost ≥ 0.5× AOV` |
| PROMOTE | `conversions ≥ 2` AND `ROAS ≥ target` |

### Quality Score Components (when CPC is high)

Decompose Quality Score into:
- Expected CTR
- Ad relevance
- Landing page experience

Identify which dragged and recommend fixes for that component — do NOT recommend bid changes alone to compensate for low QS.


## Account-Purpose Classification (CRITICAL — must run before any KPI application)

Before computing or presenting CPA / ROAS / Conv. Value:

1. Check chat title for keywords: "GMB", "footfall", "store visits", "calls",
   "directions", "awareness", "reach"
2. Check campaign objectives loaded via google_ads_run_gaql:
   - ,  → footfall account
   - ,  → awareness account
   - ,  → conversion-tracking-capable
3. Check conversion actions in the account: are they store visits, phone
   calls, directions — or actual purchases / leads?

If the account is footfall / awareness / local-service:
- REPLACE CPA / ROAS in headline metrics with: Cost Per Footfall Action,
  Cost Per Call, Cost Per Direction, CPM, Reach, Frequency
- State explicitly: "This account is configured for [footfall/awareness];
  purchase-derived CPA/ROAS do not apply."
