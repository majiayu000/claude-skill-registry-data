---
name: google-ads-pmax-evaluation
description: "Use when evaluating Google Ads Performance Max campaigns: maturity gate, PMax vs Search comparison, asset performance labels, device/location thresholds."
metadata:
  source: "prompts/skills/google_ads/pmax-evaluation"
---

# Google Ads PMax — Evaluation & Optimization

Evaluate PMax campaign readiness, compare to Search, analyze assets and segments.

## Maturity Gate (BLOCKING)

Campaign must meet ONE of:
- Age ≥ 30 days (ideally 60)
- Total conversions ≥ 50

**If neither met → WAIT. Do not optimize.** ML has not stabilized. Exception: if campaign is clearly burning money (ROAS < 0.3× target after spend ≥ 3× AOV), recommend pausing.

---

## Data Pull

Query using `google_ads_run_gaql`:

1. **Campaign performance**: id, name, status, start_date, impressions, clicks, ctr, cost, conversions, conv_value. Filter: `PERFORMANCE_MAX`, `LAST_30_DAYS`, `ENABLED`.
2. **Asset group details**: campaign id, asset_group id/name/status. Filter: `PERFORMANCE_MAX`.
3. **Asset performance labels**: campaign id, asset_group name, field_type, performance_label, asset type, image URL, youtube video ID. Filter: `PERFORMANCE_MAX`, asset types `IMAGE`, `YOUTUBE_VIDEO`, `TEXT`. Limit 200.
4. **Device performance**: campaign id, device, cost, conversions, conv_value, clicks, impressions. Filter: `PERFORMANCE_MAX`, `LAST_30_DAYS`.
5. **Geographic performance**: campaign id, geo_target_region, cost, conversions, conv_value. Filter: `PERFORMANCE_MAX`, `LAST_30_DAYS`. Sort by cost DESC, limit 200.
6. **PMax vs Search comparison**: campaign id/name, channel_type, cost, conversions, conv_value. Filter: `PERFORMANCE_MAX` and `SEARCH`, `LAST_30_DAYS`, `ENABLED`.
7. **Search term insights** (limited for PMax): category_label, clicks, impressions, conversions, cost from `campaign_search_term_insight`. Filter: `PERFORMANCE_MAX`, `LAST_30_DAYS`. Limit 200.

---

## Step 1: PMax vs Search Comparison

Calculate ROAS for both channel types and compare:

| PMax ROAS Ratio | Assessment | Action |
|----------------|------------|--------|
| < 0.5× Search ROAS | Poor | Monitor closely, consider pausing if not improving |
| 0.5–0.9× Search ROAS | Below par | Optimize assets and negatives before any scaling |
| ≥ 0.9× Search ROAS | Healthy | Proceed with optimization, eligible for scaling |
| > Search ROAS | Outperforming | Prioritize scaling |

---

## Step 2: Asset Performance Analysis

Google provides performance labels per asset (NOT cost/conversion data per asset):

| Label | Action |
|-------|--------|
| **BEST** | Create variations with similar style/messaging. This is working — make more like it. |
| **GOOD** | Keep, monitor. No changes needed. |
| **LOW** | Remove from asset group. Replace with variations of BEST performers. |
| **PENDING / UNSPECIFIED** | Wait for more data (typically 14+ days). |

Group by asset type (images, videos, headlines, descriptions) when reporting.

---

## Step 3: Device & Location Analysis

### Device
| Device CPA vs Account | Action |
|----------------------|--------|
| > 1.5× account CPA | Check site/funnel usability on that device first. If no issues → consider -50% bid adjustment or exclusion |
| > 2× account CPA | Strong candidate for exclusion after confirming no technical issues |
| CVR < 0.5× account CVR | Check landing page experience on that device |

### Location
| Location CPA vs Account | Action |
|------------------------|--------|
| > 1.5× account CPA | Consider excluding |
| > 2× account CPA | Exclude |
| Spend but 0 conversions | Wait for more data OR exclude if spend ≥ 2× AOV |

Always check for technical/usability issues before excluding a device or location.

---

## PMax Limitations (do NOT recommend these)

- No keyword targeting
- No budget per asset group
- No placement control
- No demographic control
- No channel-level budget control
- Search term data is aggregated categories only, not individual terms

---

## Next Steps

If campaign is profitable and ready to scale, read the `google-ads-pmax-scaling` skill for budget scaling, location expansion, and asset expansion rules.

Output must include: maturity status, PMax vs Search comparison, asset label summary (BEST/GOOD/LOW counts), device/location flags, scaling eligibility assessment.
