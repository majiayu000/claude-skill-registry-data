---
name: shift-budget
description: "Use when the user wants to move, raise or cut budget: where to put the next $X, which campaigns can scale inside target, budget pacing against the monthly plan, underspending or capped campaigns, or reallocating across Meta, Google, TikTok and Microsoft Ads. Finds headroom from pacing, marginal efficiency and targets, then proposes the exact budget and bid-target changes for approval."
---

# Shift budget

Move budget while the opportunity is still open. Find campaign headroom, correct pacing, and approve the exact budget moves while the signal is fresh.

## When to use

- "Where can we move $12k without pushing CAC above target?"
- "Which campaigns should get more budget?"
- "Are we on pace for the month?"
- "This campaign is capped — should we raise it?"
- "Cut spend on what isn't working."

## Before you start

1. **Targets.** ROAS, CPA or CAC target per campaign or channel. If there isn't one, use the trailing 30-day average and say so.
2. **Protected budgets.** Ask whether any campaigns, tests or budget floors must not move (brand search, prospecting floors, active tests). `recall_memory` may already know.
3. **The plan.** For pacing questions, the monthly or flight budget per channel.

## Workflow

### 1. Pacing

Compare spend so far with the plan and each campaign's budget.
- Budget utilization = spend ÷ (daily budget × days). Below about 85% means the campaign can't spend what it has; look for the cause (bid cap, small audience, low rank) before adding money.
- Google: `google_ads_run_gaql` for spend by day, budget, and search impression share lost to budget vs rank.
- Meta: `facebook_list_campaigns` and `facebook_list_adsets` for budgets (returned in cents), and `facebook_get_adaccount_insights` for spend.
- TikTok: `tiktok_get_campaigns`, `tiktok_get_adgroups` and `tiktok_get_basic_report_enhanced`. Account balance and ad group quota: `tiktok_get_account_finance`.
- Microsoft Ads: `bing_ads_list_campaigns`, `bing_ads_list_budgets` (shared budgets) and `bing_ads_get_performance`.

### 2. Headroom: where the next dollar works hardest

A campaign can take more budget only when **all** of these hold:
- It's at or better than target over 7 and 14 days, not just yesterday.
- It's actually constrained: impression share lost to budget (Google), sustained full spend of its budget, or a stable 3-day ROAS against a 7-day ROAS.
- It has enough conversions to trust (see the guardrails skill for each platform).
- Nothing changed in the last 48–72 hours.

Cut or cap where results are below target and trending worse. Diagnose first (`diagnose-performance`); don't cut a campaign that's just in its learning phase.

Default to **hold** when the data is thin or contradictory.

### 3. Size the moves

Read `meta-guardrails` or `google-ads-guardrails` first. Key limits:
- At most **20% per move** on Meta and Google Search/Shopping. Up to **50%** on mature Performance Max (`google-ads-pmax-scaling`).
- Budgets exist only at campaign (CBO) or ad set (ABO) level on Meta, and campaign level on Google. Never "move budget between ads, placements, audiences or keywords"; those aren't controls.
- Don't change the budget and the bid strategy of the same campaign at the same time.
- Always say whether a budget is daily or lifetime. Warn on increases above 100% or cuts above 50%.

## Output

1. **Pacing:** spend vs plan by channel and campaign.
2. **Headroom:** campaigns that can scale inside target, and why.
3. **Proposed moves:** a table with campaign, current budget, new budget, change %, reason and expected effect. Show that the total fits the plan.
4. **Held:** what you chose not to move, and why.

## Making the change

- Meta: `facebook_propose_update_campaigns` (campaign budgets, bid strategy, spend cap) or `facebook_propose_update_adsets` (ad set budgets on ABO campaigns). Pass budgets in account currency; the tools convert.
- Google: `google_ads_propose_update_campaigns` (budget, tCPA/tROAS targets). Call `google_ads_get_currency` first.
- TikTok (beta): `tiktok_propose_update_campaigns` and `tiktok_propose_update_adgroups`. For Smart+ campaigns, `tiktok_propose_manage_smart_plus` with `UPDATE_BUDGETS`, one ad group per proposal. Check `tiktok_get_automated_rules` first so a rule doesn't undo the change.
- Microsoft Ads: read-only through the connector. Give the user the exact moves to make.

Every change: one item per field change → dry run → show current and new values → the user approves in chat → `mode: "live"` with only the approved `operation_ids`. Never go live without that yes.

## Put it on a schedule

Offer a daily budget pacing agent. With write access and `ask_approval`, it proposes moves for approval, capped by `maxBudgetChangePct` (see `automate-with-agents`).
