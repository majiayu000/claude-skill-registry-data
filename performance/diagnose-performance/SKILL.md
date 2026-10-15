---
name: diagnose-performance
description: "Use when the user asks why performance changed or what's going on with an account: ROAS dropped, CPA spiked, spend jumped, conversions fell, blended results slipped, or 'what moved this week'. Traces the move across Meta, Google, TikTok, LinkedIn and Microsoft Ads plus GA4 and Shopify to the real driver, then proposes the smallest fix. Also for account audits and weekly performance reads."
---

# Diagnose performance

Find the cause before changing the account. Trace a performance move to its real driver, then recommend the smallest action that fixes it.

## When to use

- "Why did ROAS drop last week?" / "Why is CPA up?"
- "What changed in my account?" / "What moved this week?"
- "Audit my Meta (or Google) account."
- Blended results slipped and the user doesn't know which channel caused it.

## Before you start

1. Find the accounts (see `get-started`) and confirm the currency.
2. Call `recall_memory` for the account: its baselines, targets, known patterns and earlier findings. Judge the move against **this account's normal range**, not a universal benchmark.
3. Settle the comparison: the period in question vs the one before it (for example last 7 days vs the prior 7), and the target KPI (ROAS, CPA, CPL). If there's no target, use the account's trailing 30-day average and say so.

## Workflow

### 1. The movement

Confirm the move is real before explaining it.
- Pull both periods at account level for every channel involved.
- Check that the change is outside normal variance and isn't partial data. Recent days can still be missing conversions.
- Check volume. Ten conversions moving to eight is noise, not a trend.

### 2. The driver

Drill down one level at a time until the change is isolated to a specific line.

| Where to look | What it can show |
|---|---|
| **Channel** | Which channel owns the move. Compare with GA4 sessions and conversions by channel, and Shopify revenue, to separate platform attribution from real business change. |
| **Campaign → ad set / ad group → ad** | Where spend and results actually shifted. Quantify it: "Campaign X is 60% of spend and 90% of the CPA increase." |
| **Changes in the account** | Budget, bid, targeting, status or creative edits right before the move. |
| **Creative** | Hook rate, hold rate and CTR decay together with rising frequency means fatigue (see `analyse-creative`). |
| **Audience and placement** | Delivery shifting to a worse segment, placement or geography. |
| **Search terms** | New low-intent queries or match-type leakage (see `clean-wasted-spend`). |
| **Auction** | CPM or CPC up with impression share down means competition, not quality. |
| **Tracking** | Conversions falling while GA4 or Shopify stay flat usually means a tracking or attribution break, not a performance problem. |

Apply the platform methodology:
- Meta: `meta-performance-analysis`, with `meta-depth-of-analysis`. Read `meta-custom-event-interpretation` before judging any sales campaign that optimizes for COMPLETE_REGISTRATION.
- Google: `google-ads-search-analysis`, `google-ads-shopping` or `google-ads-pmax-evaluation`, with `google-ads-depth-of-analysis`.
- TikTok, LinkedIn, Microsoft Ads: the matching channel skill.
- Before any recommendation, read `meta-guardrails` or `google-ads-guardrails`.

### 3. The proposed actions

Recommend the smallest change that addresses the driver. Refreshing creative is often better than cutting budget. For each action give the entity, what to change, the evidence, and the expected effect. Then surface one or two things the user didn't ask about but should know: a trend that will become a problem in the next 7–14 days.

## Output

Use three parts:

1. **The movement.** The metric, the change and the period, against the account's normal range. Example: "ROAS 2.1 vs a normal 2.8–3.2, down 27% week over week."
2. **The driver.** The root cause with evidence. Example: "Hook rate and conversion rate fell together on the two top-spend ads, which are 70% of spend."
3. **The proposed actions.** A ranked list with entity, change, reason and expected effect.

End by offering to make the changes (with approval) or to keep watching with an agent.

## Acting on it

If the user wants to apply a fix, hand off to the matching skill: `shift-budget`, `clean-wasted-spend` or `manage-campaigns`. Every change goes dry run → the user approves in chat → live (see `get-started`).

## Put it on a schedule

Offer a daily "performance analyst" agent that flags the next meaningful move (see `automate-with-agents`).

## Tools

| Source | Tools |
|---|---|
| Meta Ads | `facebook_get_details_of_ad_account`, `facebook_get_adaccount_insights`, `facebook_get_async_adaccount_insights` (large pulls), `facebook_fetch_pagination_url`, `facebook_list_campaigns`, `facebook_list_adsets`, `facebook_list_ads`, `facebook_get_campaign_details`, `facebook_get_adset_details`, `facebook_get_activities_by_adaccount` (change history) |
| Google Ads | `google_ads_run_gaql`, `google_ads_get_change_logs` (changes joined with performance) |
| TikTok Ads | `tiktok_get_basic_report_enhanced`, `tiktok_get_async_report`, `tiktok_get_audience_report`, `tiktok_get_campaigns`, `tiktok_get_adgroups`, `tiktok_get_ads`, `tiktok_fetch_pagination`, `tiktok_get_change_log` |
| LinkedIn Ads | `linkedin_get_ad_analytics`, `linkedin_get_campaigns` |
| Microsoft Ads | `bing_ads_get_performance`, `bing_ads_get_change_history` |
| GA4 | `google_analytics_run_report`, `google_analytics_get_traffic_sources` (read `ga4-source-of-truth` first) |
| Shopify | `shopify_run_analytics_query` (read `shopify-order-discipline` first) |
| Memory | `recall_memory` |

Reach, frequency and rate metrics can't be summed across rows. Recompute them from totals.
