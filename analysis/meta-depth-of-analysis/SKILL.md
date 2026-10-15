---
name: meta-depth-of-analysis
description: "Use for any Meta Ads audit, performance review, optimization request, strategy question, or funnel analysis. Covers 8 analytical dimensions: hierarchical drill-down, breakdowns, temporal trends, attribution rigor."
metadata:
  source: "prompts/skills/meta/depth-of-analysis"
---

# Meta Ads - Depth of Analysis

> **When to apply**: Audits, performance reviews, optimization requests, strategy questions, funnel analysis.
> **Skip for**: Simple data fetches, campaign listings, metric lookups.

## 1. Hierarchical Drill-Down

Never make recommendations based solely on campaign-level or ad-set-level aggregates. Before concluding on any entity, drill one level deeper.

**Required flow:**
- Asked about a campaign → check ad set performance within it
- Asked about an ad set → check individual ad performance within it
- Asked about ads → check creative-level patterns (same creative across multiple ads)

**How:**
```
facebook_get_adaccount_insights at level="adset" with campaign filter
facebook_get_adaccount_insights at level="ad" with adset filter
```

Identify which specific child entities are driving or dragging the parent's aggregate numbers. Quantify the contribution (e.g., "Ad Set X accounts for 72% of campaign spend but only 40% of conversions").

## 2. Objective-Contextual Evaluation

Do not apply universal KPIs. Evaluate each campaign against its actual objective.

**Check first:**
- `promoted_object.custom_event_type` from ad set details
- Campaign objective from `facebook_get_campaign_details`
- Bid strategy (cost cap, bid cap, lowest cost)

**Apply correct KPIs:**
| Objective | Evaluate on | NOT on |
|-----------|------------|--------|
| Sales/Purchase | ROAS, CPA, Revenue | Reach, CPM alone |
| Lead gen | CPL, lead volume | ROAS |
| Traffic | CPC, CTR, landing page views | Conversions |
| Video views | Cost per ThruPlay, hook rate | ROAS, CPA |
| Awareness | CPM, reach, frequency | CPA, ROAS |

**Flag bid strategy issues:** If a cost cap is set 3x above actual CPA, or tROAS target is 0.5x when achieving 3x — the algorithm isn't actually constrained. Call this out.

## 3. Breakdown & Segmentation Analysis

When this skill applies (audits, performance reviews, optimization), check at least 2 of these breakdown dimensions. This overrides the general tool-fundamentals guidance to only use breakdowns when specifically requested — deep analysis requires segmentation.

**Required breakdowns:**
```
facebook_get_adaccount_insights with breakdowns="publisher_platform,platform_position"
facebook_get_adaccount_insights with breakdowns="device_platform"
facebook_get_adaccount_insights with breakdowns="age,gender"
```

**What to look for:**
- Placement CPA differences (Feed vs Stories vs Reels vs Audience Network) — quantify the gap
- Device performance divergence (mobile vs desktop)
- Age/gender segments receiving delivery outside target — flag Advantage+ expansion leakage
- Out-of-target segments consuming budget with poor conversion rates

**Statistical significance check:** Do not make segment-level recommendations from <100 impressions or <3 conversions in a segment. Call out low-confidence segments explicitly.

## 4. Temporal & Trend Analysis

Never treat a date range as a single static number. Always compare time windows.

**Required comparisons:**
```
facebook_get_adaccount_insights with time_increment="1" (daily data)
```

Analyze at minimum:
- Last 7 days vs previous 7 days
- Identify direction for each key metric: improving, declining, or stable
- Flag inflection points: "CTR started declining on [date], 3 days before CPA started rising"

**Connect the chain:** Frequency rising → CTR falling → CPA rising → this is creative fatigue, not audience exhaustion. Correlate timing across metrics to establish cause, not just observe symptoms.

## 5. Cross-Entity Dependency Mapping

Do not analyze campaigns in isolation. Map the funnel.

**Check:**
- Which campaigns are prospecting (broad/lookalike audiences)?
- Which campaigns are retargeting (custom audiences, website visitors)?
- Does cutting a prospecting campaign starve the retargeting audience pool?

**How to detect:**
- `facebook_get_adset_details` → check `targeting` for custom audiences vs broad targeting
- Prospecting: low frequency, lower CPM, lower CTR, broader audience
- Retargeting: higher frequency, higher CPM, higher CTR, smaller audience

**Flag dependencies:** "Pausing Campaign X will reduce the Website Visitors 7d pool that feeds Campaign Y's retargeting. Expect retargeting CPA to rise within 1-2 weeks."

## 6. Platform Mechanic Awareness

Explain how Meta's mechanics affect the specific situation. Do not just mention them — explain the compound interaction.

**Common compound effects to check:**

| Signal | Mechanic | Consequence |
|--------|----------|-------------|
| Rising frequency + falling CTR | Creative fatigue | CPA will spike — need new creatives, not budget changes |
| CBO + one ad set getting 80% budget | CBO optimization | Usually working as intended — the algorithm concentrates budget on the best converter. Do not pause the dominant ad set just because smaller siblings look better on small samples; those often fail at scale. Only intervene if the dominant ad set itself is underperforming on ROAS/CPA. |
| Cost cap + rising CPM | Delivery squeeze or audience shift | Two possible causes — separate them before acting: (a) algorithm can't find conversions at the cap price (raise cap or loosen targeting); (b) original audience is saturated/exhausted and delivery is leaking to worse segments, pushing auction prices up. Check frequency, reach trend, and audience size to decide which. |
| Advantage+ audience expansion ON | Targeting leakage | Check breakdown for out-of-target delivery eating budget |
| Insufficient spend on new ad set | Learning phase | Do not make optimization decisions until the ad set has spent at least **2× AOV or 4× CPA, whichever is higher**. The 50-conversion rule only applies to brand-new accounts with no prior conversion history. |

## 7. Proactive Signal Detection

After answering the user's question, always surface 2-3 additional concerns or opportunities they did not ask about.

**Scan for:**
- Any entity with frequency >3 and rising — creative fatigue incoming
- Any ad set spending >30% of campaign budget with 0 conversions — budget waste
- Any campaign where top ad has declining CTR over 7+ days — performance degradation ahead
- Any retargeting audience pool that's shrinking (declining reach week over week)
- Any metric that looks fine now but the trend predicts problems in 7-14 days

**Format:** "Outside your question, I noticed [signal] in [entity] — this suggests [predicted consequence] within [timeframe]."

## 8. Attribution Rigor

Do not take reported conversion numbers at face value.

**Always check:**
- What attribution window is active? (1-day click, 7-day click, 1-day view?)
- What share of conversions are view-through vs click-through?
- Is the reported ROAS inflated by view-through on high-impression campaigns?

**Flag these situations:**
- Retargeting campaign with very high ROAS + mostly view-through conversions → likely over-attributed
- Two campaigns targeting the same audience → conversions may be double-counted
- ASC/Advantage+ Shopping targeting existing customers → attributed ROAS includes conversions that would have happened organically

**Frame as caveat:** "Before scaling Campaign X based on its reported 4x ROAS, note that [specific attribution concern] means the true incremental ROAS is likely lower."
