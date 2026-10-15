---
name: own-creative-diagnosis
description: Diagnose why the user's own Meta ad creatives are (or aren't) working using Hook Rate / Hold Rate / CTR scenario analysis, format-specific rules, and pattern recognition across top performers. Use whenever the user asks why a creative isn't performing, wants to know what's working across their winning ads, needs a Pareto/creative teardown of their own account, or is planning variations of a winning ad. Works via GoMarble MCP (preferred), a Meta Ads Manager CSV export, or user-shared screenshots/creative files — degrades gracefully by source.
---

# Own Creative Diagnosis

Diagnoses the user's own ad creative performance: which ads perform strongly and what patterns are worth testing in variations. Adapted from the Meta Ads Creative Analysis framework — the numeric half (Hook/Hold/CTR) works from any complete data source; the qualitative half requires creative content from the MCP creative endpoint or files/descriptions supplied by the user because CSV exports do not contain it.

> **Read-and-recommend only.** Produce analysis and recommendations for the user to review and apply manually; do not execute changes in the ad account.

## When to use this skill

- "Why isn't this ad working?"
- "What's working across my top ads?"
- "Help me plan variations of [winning ad]"
- As the "own creative" input into `winning-pattern-synthesis`, alongside `competitor-ad-intelligence`

## Step 0: Data Inventory

Identify the source before anything else:

| Priority | Source | Notes |
|---|---|---|
| 1 | GoMarble MCP (`facebook_get_adaccount_insights`, `facebook_analyze_ad_creative_by_id_or_url`) | All rules work directly |
| 2 | Ads Manager CSV export | Numeric metrics work if video columns enabled; creative content is NEVER in a CSV — must be shared separately |
| 3 | Screenshots / copy-paste | Spot-checks only |

State what's available and missing in one short line before proceeding. If GoMarble MCP is connected, default to it — never ask the user for a CSV export first, as it exists already.

**Default account:** unless the user specifies otherwise, use their default Meta ad account. In all output, reference campaigns/ad sets/creatives by name only — never surface account IDs or account names.

Set the account's **Primary Conversion Metric (PCM)** before comparing performance: use ROAS for ecommerce and cost per lead/result for lead generation or custom conversion accounts. Treat ROAS as weak when it is below target and cost per result as weak when it is above target; never compare mixed conversion types in one baseline.

Record the PCM target and an explicit, current analysis window before applying an action rule. Use 30 days by default when the user has not requested another period. If either the target or dated window is missing, diagnose the creative but do not recommend pausing it.

## Step 1: Establish the high-spend review set

Sort ads by spend descending and include rows until cumulative spend first reaches or exceeds 90% of total, including the row that crosses the threshold. This is the **high-spend review set**, not a top-performer set; performance is assessed in the following steps.

## Step 2: Format-agnostic first pass

Apply to every ad in the high-spend review set:

| Profile | Diagnosis | Action |
|---|---|---|
| High CPM (≥30% above review-set avg) + weak PCM (ROAS ≥30% below target or cost per result ≥30% above target) | Expensive delivery with weak conversion efficiency | Apply the pause evidence gate below; otherwise watch |
| Low CTR (≥30% below review-set avg) + weak PCM | Weak click-through and conversion efficiency | Check comments and offer/landing-page alignment; recommend a stronger-CTA test |
| Good metrics (within 20% of avg, PCM meeting or beating target) | Working | Candidate for variation — carry into Step 4 |

**Pause evidence gate:** never recommend pausing an ad younger than 7 days or the highest-converting ad in its ad set. For an ad with conversions, require at least 3 ad-level conversions in the analysis window before using weak PCM as pause evidence. For an ad with zero conversions, require spend above 2× the target cost per result (or 2× a known break-even acquisition cost for ROAS accounts). If the applicable threshold cannot be computed, classify the ad as **WATCH**.

## Step 3: Video-specific diagnostic scenarios

For video ads, classify using Hook Rate / Hold Rate / CTR:

- **Hook Rate (%)** = 3-second views ÷ video plays × 100. Good ≥40%, average ≥26% and <40%, poor <26%.
- **Hold Rate (%)** = ThruPlays ÷ 3-second views × 100, benchmarked against a 90-day account average. Poor is below the baseline, average is from the baseline to <1.25× baseline, and good is ≥1.25× baseline (a relative 25% lift, not 25 percentage points).
- **CTR (%)**: good ≥1.25%, average ≥0.65% and <1.25%, poor <0.65%.

Compare unrounded values and round only for display. If a denominator is zero or missing, mark the metric unavailable instead of classifying it.

| Scenario | Hook | Hold | CTR | Working hypothesis | Next test |
|---|---|---|---|---|---|
| 1 | ≥40% | Poor | Avg | The opening attracts attention, but the post-hook content may not deliver the promise | Keep the hook; test showing the product sooner, quicker pacing, and a clearer tie to the hook's promise |
| 2 | 26–<40% | Avg | Avg | No single stage is clearly strong; the opening is the first testable constraint | Test a more relevant or direct visual/text opener, then reassess hold |
| 3 | <26% | Any | Any | The opening may not stop the scroll for this audience or placement | Compare with high-spend strong performers and test a different visual open, overlay, audio treatment, or question-versus-statement |
| 4 | ≥40% | ≥1.25× avg | <0.65% | Attention and retention are strong, while CTA, offer, or landing-page alignment may constrain clicks | Check comments and landing-page alignment; then test a clearer, more prominent CTA |

These scenarios localize where performance may weaken; they do not prove a root cause. Treat the diagnosis as a hypothesis and check audience, placement, offer, delivery, and landing-page differences before presenting a causal explanation.

## Step 4: Format-specific rules

- **Single image**: same high-CPM/low-CTR pause logic as Step 2; good metrics → variation candidate
- **Single video**: apply Step 3 scenarios
- **Catalog/Advantage+ ads**: Meta doesn't provide per-product conversion data — use spend+CTR to build a high-spend product review set. High CPM+weak PCM → test a different product set or remove products pushing CPM up. Low CTR+weak PCM → identify and remove low-CTR products.

## Step 5: Pattern recognition across strong performers

Across the high-spend set's good-performing ads, extract and log the actual creative content. Use `facebook_analyze_ad_creative_by_id_or_url` when MCP is connected; otherwise ask the user for video/image files or descriptions because CSV exports do not include the creative:

- Common angle (which selling points repeat)
- Common format (video vs image vs carousel)
- Common hook mechanism
- Common copy structure/tone/length

This output is the direct input to `winning-pattern-synthesis`.

## Guardrails

- Never recommend pausing the ad with the highest conversion volume in its ad set, regardless of budget share — that's the algorithm working correctly.
- Before judging an ad set's efficiency trend, require 3–5 conversions/week; the zero-conversion pause exception instead uses the explicit spend gate in Step 2.
- Apply the ad-level pause evidence gate in Step 2; the ad-set minimum does not substitute for ad-level evidence.
- Budget/scale recommendations are out of scope for this skill — it diagnoses creative, not delivery mechanics.
- Never invent Hook/Hold/CTR numbers if the data isn't available — state what's missing and ask for it, or proceed on qualitative creative review only and say so.
- Do not execute pause, edit, or launch actions; recommendations are for manual user review and application.

## Output Format

```
### Creative Diagnosis: [Account/Campaign scope]

High-spend review set: [N ads, cumulative spend first reaches/exceeds 90%]

Per-ad diagnosis:
| Ad | Hook | Hold | CTR | PCM | Scenario | Verdict |
|---|---|---|---|---|---|---|

Performance patterns (shared across strong performers):
- Angle: ...
- Hook: ...
- Format: ...
- Copy: ...

Recommendations:
1. [ad-specific fix, with metric justification]
2. ...
```
