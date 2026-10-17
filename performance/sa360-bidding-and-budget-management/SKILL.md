---
name: sa360-bidding-and-budget-management
description: Choose between Search Ads 360 portfolio bid strategies and Google Ads native strategies, then pace and forecast spend with plans and budget bid strategies. Use when the user asks whether to use an SA360 or Google Ads bid strategy, about portfolio bidding, Multi-Target portfolios, auction-time vs intraday bidding, Target CPA, Target ROAS, maximize conversions or value, Target impression share, budget bid strategies, plans, forecasting, or budget pacing across engines.
---

# SA360 bidding and budget management

Decide which layer owns the bidding (an SA360 portfolio strategy or a Google Ads native strategy), pick the goal that matches intent, then control spend with a plan and a budget bid strategy so a cross-engine budget lands on target without manual daily babysitting. In the new Search Ads 360, bidding and budget are two separate systems that work together: bid strategies decide how much to bid per auction, budget bid strategies and plans decide how the money is paced and split across campaigns and engines.

This skill assumes you know CPC, CPA, CPM, ROAS, and impression share. For that KPI math see the `programmatic-foundations` skill. For where campaigns sit in the Manager and engine-account hierarchy see `sa360-account-structure-and-engines`. For wiring conversion sources and pulling data through the Reporting API see `sa360-conversions-and-reporting-api`. Everything here is written for the new SA360 experience only.

## When to use this skill

- "Should I use an SA360 bid strategy or a Google Ads bid strategy?"
- "Set up portfolio bidding / a Multi-Target portfolio / Target CPA / Target ROAS / maximize conversions / maximize conversion value / Target impression share / maximize clicks."
- "What is auction-time bidding vs intraday bidding?"
- "How do I pace a monthly budget across Google, Microsoft, and other engines?"
- "Set up a plan, forecast spend, and add a budget bid strategy."
- "Why is my budget bid strategy underspending or overspending?"
- "Why did the strategy stop optimizing after I switched it?"

Boundaries with sibling skills:
- Manager, sub-manager, engine and engine-track account setup: `sa360-account-structure-and-engines`.
- Conversion sources (Floodlight, Google Ads, GA4) and the read-only Reporting API v0: `sa360-conversions-and-reporting-api`.
- The bidding decision logic native to Google Ads campaigns in a Google Ads account: `google-ads-bidding`. This skill covers the SA360 layer that sits over it.
- KPI definitions and shared math: `programmatic-foundations`.

## Quick reference

| Situation | Use | Why |
| --- | --- | --- |
| One goal across campaigns in multiple engines (Google + Microsoft) | SA360 portfolio bid strategy | Only the SA360 layer optimizes cross-engine to one portfolio target |
| Two goals at once (hit a CPA and a spend ceiling) | SA360 Multi-Target portfolio | Google Ads native strategies cannot express two SA360 targets |
| Google-only account, deep in Smart Bidding, want auction-time signals native | Google Ads bid strategy | Google Ads optimizes it directly; SA360 only reads it |
| Efficiency target, enough conversion history | Target CPA or Target ROAS | Strategy meets or beats a cost or value target |
| Volume within a budget | Maximize conversions or Maximize conversion value | Spends the budget for the most conversions or value |
| Rank/visibility goal | Target impression share | Bids to a share-of-page position, not a conversion goal |
| Traffic goal, thin conversion data | Maximize clicks | No conversion signal needed |
| Pace a fixed budget across campaigns and engines to a target end spend | Plan plus budget bid strategy | Automates allocation and pacing; separate from the bid strategy |

Two systems, kept separate:
- Bid strategy: how much to bid per auction to hit a performance goal.
- Budget bid strategy plus plan: how much to spend and how to split and pace it over the flight.

## Core process

1. Decide who owns the bidding. If campaigns span more than one engine and you want one performance goal across them, or you need two targets at once, use an SA360 portfolio bid strategy, because only the SA360 layer optimizes cross-engine and only it supports Multi-Target portfolios. If you are Google-only and want Google to optimize directly with its auction-time signals, use a Google Ads bid strategy and let SA360 read it. A Google Ads native strategy is visible in SA360 but optimizes only in Google Ads and is not compatible with SA360 features like Multi-Target portfolios.
2. Name the goal before you name the strategy. Efficiency (hit a CPA or ROAS), volume (most conversions or value for the budget), visibility (a share of impressions), or traffic (clicks). The goal picks the strategy type, not the reverse.
3. Confirm the conversion signal. Target CPA, Target ROAS, Maximize conversions and Maximize conversion value all need conversion history to learn from, and value strategies need conversion value tracked. If the signal is thin, start with Maximize clicks or Target impression share, or consolidate campaigns so one strategy sees enough volume. Conversion setup lives in `sa360-conversions-and-reporting-api`.
4. Pick the bidding cadence. Auction-time bidding sets a bid at the moment of each auction using live signals; intraday bidding recalculates bids on a schedule (every 6 hours). Prefer auction-time where the engine supports it, because it reacts per query instead of on a fixed clock.
5. Create the portfolio and attach campaigns, or set the strategy at the campaign. For a portfolio, set one target for the group and let SA360 raise bids on stronger biddable items and adjust weaker ones to hold the portfolio average. Recommend, do not apply live spend or bid changes without human sign-off.
6. Set up budget separately. Build a plan (a campaign group with a spend target and a date range), forecast it, then add a budget bid strategy so SA360 allocates and paces the budget toward the target end spend. Watch the budget pacing chart, not just daily spend, because pacing is measured against the plan, not a flat daily cap.
7. Hold the setup stable through the learning window. Switching the strategy type or moving the target resets learning and discards calibration. Change targets in small steps and give each change time before you judge it.

## Decision rules and thresholds

### SA360 portfolio strategy vs Google Ads native strategy

- Use an SA360 portfolio bid strategy when the goal spans multiple engines, when you need SA360-only features (Multi-Target portfolios, minimum-traffic support for low-volume items, cross-engine reporting on the strategy), or when you want one portfolio target to govern many campaigns.
- Use a Google Ads bid strategy when the account is Google-only and you want Google Ads to optimize with its own auction-time signals. SA360 shows the strategy and reports on it, but does not optimize it and cannot layer SA360 portfolio features on top.
- A Google Ads portfolio bid strategy is owned by the Google Ads account, visible in SA360, but optimized only by Google Ads. Do not expect SA360 portfolio behavior from it.

### Picking the SA360 bid strategy goal

| Goal | Strategy | Needs | Watch out for |
| --- | --- | --- | --- |
| Hit a cost per action | Target CPA | Conversion history | Target below the clearing cost starves delivery |
| Hit a return on ad spend | Target ROAS | Conversion value tracked | Thin value data makes ROAS unstable |
| Most conversions for the budget | Maximize conversions | Conversion history | Will spend the full budget; pair with a spend control |
| Most conversion value for the budget | Maximize conversion value | Conversion value tracked | Same as above; value tracking must be clean |
| A share of top or absolute-top impressions | Target impression share | None (no conversion signal) | Optimizes rank, not efficiency or conversions |
| Traffic when conversion data is thin | Maximize clicks | None | Clicks are not conversions; use as a bridge |

A Multi-Target portfolio lets one portfolio pursue two constraints at once (for example a CPA target and a spend target). This is an SA360-native capability; a Google Ads native strategy cannot express it.

### Auction-time vs intraday bidding

- Auction-time bidding computes the bid at the instant of the auction using live query and user signals. Use it wherever the engine supports it, because it reacts per auction.
- Intraday bidding recalculates bids on a fixed cadence (every 6 hours) rather than per auction. It is the fallback where auction-time is not available for the engine or campaign type.

### Budget bid strategies and plans

- A plan sets a spend target, key metrics, and a date range for a campaign group. Forecast the plan before committing so the projected spend and results are visible.
- A budget bid strategy uses the campaigns' budgets and their performance history to allocate and pace spend toward the plan's target end spend. It is a spend-pacing system, separate from the per-auction bid strategy, and the two run at the same time.
- Judge pacing against the plan on the budget pacing chart, not against a flat daily number. A plan that front-loads or back-loads on purpose will look "off" on a daily view but correct against the plan.

### Learning and stability

- Automated strategies need conversion history and a stabilization window before their performance should be read. Give a new or newly switched strategy time before judging it.
- Changing the strategy type or moving the target resets learning. Decide the goal up front, then adjust targets in small steps rather than swapping strategies.

## Reference material

- `references/portfolio-vs-native-bidding.md`: SA360 portfolio strategy vs Google Ads native strategy side by side, the full SA360 bid strategy goal table, Multi-Target portfolios, and the Reporting API v0 `bidding_strategy_type` enum with the target fields. Read this when deciding who owns the bidding or reading a strategy through the API.
- `references/auction-time-and-intraday.md`: how auction-time and intraday bidding differ, the 6-hour intraday cadence, engine and campaign-type support, and how the cadence choice interacts with signal freshness and reporting. Read this when a strategy reacts too slowly or you are choosing a cadence.
- `references/performance-plans-and-pacing.md`: the plan and budget-bid-strategy workflow end to end (create group, set spend target and key metrics, forecast, add budget bid strategy, read the pacing chart), pacing diagnostics, and the fields that surface it in reporting. Read this when setting up or debugging cross-engine budget pacing.

## Templates and examples

- Cross-engine efficiency, healthy conversions: one SA360 portfolio Target CPA at $32 covering Google and Microsoft search campaigns, auction-time bidding, attached campaigns sharing one target. Hold two to three weeks before reading performance.
- Two constraints at once: a Multi-Target portfolio holding a Target CPA of $45 and a monthly spend target of $60,000, so SA360 chases the CPA while pacing to the spend ceiling. A Google Ads native strategy cannot do both.
- Google-only, deep in Smart Bidding: leave the Google Ads Target ROAS 400% strategy in the Google Ads account, let Google optimize it, and read it in SA360 for cross-account reporting rather than re-creating it as an SA360 portfolio.
- Thin conversion data on a new engine account: start Maximize clicks or Target impression share at 65% absolute-top share to buy traffic and visibility, build conversion volume, then move to Target CPA once the signal is there.
- Quarterly budget pacing: a plan for the Q3 brand campaign group with a $250,000 spend target from Jul 1 to Sep 30, forecast first, then a budget bid strategy that allocates across campaigns and paces to the target end spend, monitored on the budget pacing chart.

## Common pitfalls

- Expecting SA360 optimization from a Google Ads native strategy. A Google Ads bid strategy is visible in SA360 but optimizes only in Google Ads and cannot use SA360 features like Multi-Target portfolios. If you need cross-engine portfolio behavior, build an SA360 portfolio strategy.
- Mixing up the two systems. The bid strategy controls per-auction bids; the budget bid strategy and plan control spend pacing. Underspend or overspend is usually a budget-side problem, not a bid-strategy problem, and the fix is in the plan and pacing chart.
- Target set below the clearing cost. A Target CPA or Target ROAS the inventory cannot clear starves delivery because the strategy cannot find auctions at that price. Loosen the target or widen targeting, then let it relearn.
- Too few conversions for a conversion strategy. Target CPA, Target ROAS, and the maximize-value strategies cannot learn without conversion (and, for value, conversion-value) history. Bridge with Maximize clicks or Target impression share, or consolidate campaigns so one strategy sees enough volume.
- Switching strategies mid-flight. Changing the strategy type or moving the target resets learning and discards calibration. Decide the goal up front and adjust targets in small steps.
- Reading pacing off daily spend. Pacing is measured against the plan across the flight, not a flat daily cap. Use the budget pacing chart so an intentional front- or back-load does not read as a problem.
- Applying changes without a human gate. Recommend bid, target, and budget changes; do not push live spend or configuration changes automatically. See `approval-and-escalation-governance` for the sign-off pattern.

## Sources

- [Search Ads 360 bid strategies overview](https://support.google.com/sa360/answer/14270628?hl=en) (as of July 2026)
- [About Google Ads bid strategy functionality in Search Ads 360](https://support.google.com/sa360/answer/16856529?hl=en) (as of July 2026)
- [Budget management and pacing in Search Ads 360](https://support.google.com/sa360/answer/13648245?hl=en) (as of July 2026)
- [Search Ads 360 Reporting API, campaign fields (v0)](https://developers.google.com/search-ads/reporting/api/reference/fields/v0/campaign) (as of July 2026)
- [Search Ads 360 Reporting API release notes](https://developers.google.com/search-ads/reporting/api/reference/release-notes) (as of July 2026)
