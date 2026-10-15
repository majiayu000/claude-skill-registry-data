---
name: meta-guardrails
description: "Guardrails for Meta Ads recommendations and mutations. Hard rules on what NOT to recommend, prohibited phrasing, data-quality requirements. Used internally for any Meta optimization or change."
metadata:
  source: "prompts/skills/meta/guardrails"
---

# Meta Ads Guardrails

**READ BEFORE GENERATING ANY RECOMMENDATION.**

## Budget Reallocation Prohibition

You CANNOT allocate, shift, increase, reduce, or scale budget for: ads (only campaigns and ad sets have budgets), placements (Meta controls distribution), demographics (age, gender, location breakdowns), user segments (new, existing, engaged).

**Before writing ANY recommendation, ask:** Does it imply moving money between ads, placements, demographics, or segments? If YES → rewrite using valid controls below.

## Valid Budget Controls

1. Campaign budget (CBO) or ad set budget (ABO)
2. Bid caps / cost caps
3. Turning ads/ad sets on or off

If a recommendation does not map to one of these three controls, it is not actionable.

## Mandatory Rewrites

❌ "Reallocate $X from [ad A] to [ad B]"
✅ "Pause [ad A]. Increase campaign/ad set budget by 15–20% to give [ad B] more spend opportunity."

❌ "Allocate more to [placement/demographic/segment]"
✅ "Create a new ad set targeting [dimension] with its own budget, OR exclude underperforming [dimension] via ad set placement settings."

**Rule**: Breakdowns (age, gender, placement, device, region, user segment) show how Meta distributed YOUR budget. They are not levers you control. The only way to influence them is creating new ad sets with specific targeting or placement selections.

## Metric Selection by Conversion Type

- **Ecommerce** (purchases/revenue): Use ROAS, revenue, AOV, cost per purchase. Never use ROAS for leadgen.
- **Leadgen** (form submits, leads): Use CPL, cost per qualified lead. Never use ROAS unless offline revenue is mapped.
- **App** (installs, in-app events): Use CPI, cost per activation. Never use ROAS unless in-app revenue tracking is confirmed.
- **Unclear**: Ask user. Do not assume.

## User Segment Breakdown

Segments (New Audience, Existing Customers, Engaged Audience) are Meta internal classifications. These cannot be targeted without custom audiences.

- Before recommending segmentation, ask: "Do you have a customer custom audience already built?"
- If yes → suggest exclusions or separate campaigns using custom audience targeting
- If no → suggest building custom audiences first

## STOP Rules

**PRE-CHECK**: Can I point to the exact Ads Manager UI field? If no → do not recommend.

- No ad-level budget moves
- No demographic or placement budget allocation
- No frequency caps for conversion objectives (Sales, Leads, App install)
- No scaling individual ads (only campaign/ad set level)
- No scaling > 20% at once
- Do not pause ads or ad sets younger than 7 days without enough signals
- Do not increase budget on entities below ROAS/CPL/CPA targets — diagnose first
- Do not call something scalable with < 10% revenue share of total account or statistically weak conversion volume
- Minimum signals: 3–5 conversions per ad set per week before performance judgments
- Avoid suggestions that restart learning unless absolutely required
- Do not rely on first 24–48 hours of data as reliable

## Top Performer Protection (CRITICAL)

**NEVER recommend pausing the top-converting ad in an ad set.** If Meta's algorithm allocates 60-80% of an ad set's budget to one ad and that ad produces the majority of conversions, that is Meta's optimization working correctly — not a problem.

**Pause decision matrix**:
| Condition | Action |
|-----------|--------|
| Ad has highest conversion volume in ad set | **KEEP** — regardless of budget share |
| Ad has 0 conversions AND spend > 2x ad set CPA target | PAUSE |
| Ad has conversions but CPA > 3x ad set average AND 3+ conversions (statistically significant) | PAUSE |
| Ad has 1-2 conversions with high CPA | WATCH — insufficient data, do not pause yet |
| Ad is < 7 days old | WATCH — let it exit learning phase |

**Self-check before any pause recommendation**: "Am I about to pause the ad that drives the most conversions in this ad set?" If yes → DO NOT PAUSE. Instead, recommend testing new creatives alongside it.

## Methodology Consistency

Once you establish a methodology for evaluating ad performance in a conversation, do NOT change it unless the user explicitly asks you to. Changing criteria mid-analysis destroys trust. If you realize your methodology was wrong, say so clearly, explain what you're changing and why, and then apply the new methodology consistently from that point forward.

## Required Diagnostics Before Action

Before any scale/pause/duplicate/structural suggestion:
1. User segments: New vs Existing vs Engaged distribution
2. Delivery metrics: CPM, CTR, Reach, Frequency (with Spend context)
   - High frequency alone ≠ fatigue
   - Frequency rising + CTR falling over 14+ days = creative fatigue
3. Engagement relevance: offer-aligned comments vs spam/backlash
4. Attribution windows: 1dc vs 7dc vs incremental if platform/external data mismatch
5. Confirm results not dominated by warm/small pools before scaling

## Scaling Guardrails

- Only campaign or ad set budget fields
- Max increase: 20% at once
- Require before scaling: performance target hit, ad set revenue share ≥ 10% of account, not dominated by 80%+ warm/customer pocket
- If data is noisy or contradictory → say **insufficient data**, shift to structured testing
- All scaling must include: deterioration risk warning + review window + spend cap

## Recommendation Workflow

1. Fetch setup first (`facebook_get_campaign_details` + `facebook_get_adset_details`): targeting, budget type (CBO/ABO), optimization event, learning phase status, estimated audience size
2. Self-check: breakdown-based budget move detected? → STOP. Can state exact Ads Manager field? → continue.
3. Validate: If breakdown insight from broad audience → cannot scale that slice, can recommend new ad sets or creative angles
4. Placement: Never budget moves between placements. Can suggest exclusions via new/duplicated ad set.
5. Learning phase: Avoid resets unless required.
6. Risk framing: All scaling includes risk warning + review window + cap.
