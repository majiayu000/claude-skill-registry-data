---
name: meta-performance-analysis
description: "Use when analyzing Meta (Facebook/Instagram) ad performance: account type detection, Pareto analysis, baselines, performance thresholds, issue diagnosis."
metadata:
  source: "prompts/skills/meta/performance-analysis"
---

# Meta Ads - Performance Analysis Workflow

> Metric definitions (CTR, CPM, ROAS, CPL, CPR, conversion rate, account-type → PCM mapping, performance benchmarks, Pareto definition) live in `meta/tool-fundamentals` and auto-load with this skill. Do NOT redefine them here. This skill is the workflow for performance audits after the metrics are loaded.

## Step 1: Identify Account Type & PCM

Read `promoted_object.custom_event_type` from the ad set to determine the Primary Conversion Metric (PCM). The mapping table is in `tool-fundamentals → Account Type → Primary Conversion Metric`.

Where to read it:
- `facebook_get_details_of_ad_account` → returns `account_structure.adsets` with `promoted_object` for top spending ad sets. Use this first.
- `facebook_get_adset_details` → use when you need conversion events for ad sets not in the account structure.

***PROHIBITED***: Never extract or infer conversion events from names. Ad set names frequently don't match the actual config.

**Mixed accounts**: group ad sets by their `custom_event_type`. Each group gets its own PCM. Do not mix conversion types.

**If `promoted_object` is missing**: ASK the user which conversion event is the business outcome.

## Step 2: Pareto Pull (90% Spend)

1. Get ad-level insights sorted by spend descending.
2. Calculate cumulative spend percentage for each ad.
3. Keep ads where cumulative % ≤ 90% — these are your Pareto ads.
4. Focus analysis on Pareto ads.

**Query for Pareto ads** (MUST include active status filter):
```
Tool: facebook_get_adaccount_insights
level: "ad"
fields: ["ad_name", "ad_id", "adset_id", "adset_name", "spend", "impressions", "cpm", "ctr", "clicks", "actions", "action_values", "purchase_roas"]
date_preset: "last_30d"
filtering: [
  {"field": "impressions", "operator": "GREATER_THAN", "value": 0},
  {"field": "ad.effective_status", "operator": "IN", "value": ["ACTIVE"]}
]
sort: "spend_descending"
```

**CRITICAL**: Always include `ad.effective_status` (or `adset.effective_status`) filter. Without it, the API returns data for paused/deleted entities that had historical spend, producing analysis that includes inactive entities. Fetch ALL pages before analyzing — ad-level results paginate at 25 per page (see `tool-fundamentals → Pagination`).

## Step 3: Establish Baselines

From the Pareto set, compute:
- `avg_cpm` = mean CPM across Pareto ads
- `avg_ctr` = mean CTR across Pareto ads
- `avg_pcm` = mean ROAS (e-commerce) or mean CPL/CPR (lead gen / custom) across Pareto ads

These become the comparison points for individual-ad assessment. Apply the variance benchmarks from `tool-fundamentals → Performance Benchmarks`.

## Step 4: Diagnose Issues

**High CPM + Low PCM**:
- Expensive audience, not converting
- Action: pause ad or test different targeting

**Low CTR + Low PCM**:
- Ad not resonating with audience
- Check comments for negative sentiment
- If comments fine: test copy/creative variations with stronger CTA

**Good metrics but declining trend**:
- Check frequency — see fatigue signal in `tool-fundamentals → Diagnostic Signals`
- Action: new creative variations, not just budget changes

## Step 5: Generate Recommendations

**MANDATORY**: After completing the analysis, generate specific, actionable recommendations for each Pareto ad and for the account overall.

### Per-Ad Recommendations
For each Pareto ad, based on its diagnostic profile:
- **What to do**: specific action (pause, scale, create variation, change targeting)
- **Why**: metrics-based justification (e.g., "CPM 40% above Pareto avg with 0.3× ROAS")
- **How**: concrete next steps

### Account-Level Recommendations
Summarize the top 3–5 strategic recommendations:
1. Budget reallocation (shift spend from poor → good performers; respect guardrails)
2. Creative strategy (what's working, what to test next)
3. Targeting adjustments (if CPM issues are widespread)
4. Structure changes (campaign / ad set consolidation if needed)

### Output Format

```markdown
## Performance Summary

| Ad | Format | Spend | CPM | CTR | ROAS/CPA | Status |
|----|--------|-------|-----|-----|----------|--------|
| [Name] | Image | $X | $X | X% | X | [Scale/Pause/Test] |

**Benchmarks (Pareto avg)**: CPM: $X | CTR: X% | ROAS: X

## Recommendations

### Per-Ad Actions
1. **[Ad Name]**: [Action] — [Justification]
2. **[Ad Name]**: [Action] — [Justification]

### Strategic Recommendations
1. [Actionable recommendation with metrics basis]
2. [Actionable recommendation with metrics basis]
3. [Actionable recommendation with metrics basis]
```

**If creative analysis is needed** (video performance, hook rates, ad copy evaluation):
- The Creative Analysis skill should already be loaded for audits.
- If not loaded, use the `meta-creative-analysis` skill.
