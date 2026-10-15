---
name: clean-wasted-spend
description: "Use when the user wants to find or cut wasted ad spend: bad search terms, negative keywords, money-losing placements, audiences, devices or locations, fatigued ads still spending, duplicated targeting, zombie campaigns, or Shopping products that never convert. Quantifies each leak, separates real waste from deliberate tests, and proposes the exclusions, negatives and pauses for approval."
---

# Clean wasted spend

Find wasted spend before the next budget review. Find spend with no path back to target, show the evidence, and approve the clean-up.

## When to use

- "Where are we wasting money?"
- "Find bad search terms and add negatives."
- "Which placements, audiences or locations aren't converting?"
- "Which ads should we pause?"
- "Clean up the account before the monthly review."

## Before you start

- Get the target (CPA or ROAS) and the date range. Default to 30 days; search terms need the full window.
- Ask about exceptions: tests, new launches still learning, brand terms and campaigns that are there for reach. `recall_memory` may know them.
- Waste means spend that has **no credible path back to target**. A test inside its learning window isn't waste. Something with too few conversions to judge isn't waste yet; say it's too early.

## Where to look

| Leak | How to find it | Methodology |
|---|---|---|
| **Search terms** (Google) | `google_ads_run_gaql` on `search_term_view` over the full window, sorted by cost, not just the top performers. Classify each term Q1–Q5. | `google-ads-search-analysis` |
| **Search terms and keywords** (Microsoft) | `bing_ads_get_performance` at keyword level, and `bing_ads_list_keywords` for bids and quality score. | Same Q1–Q5 logic |
| **Shopping products** | Product-level performance. Classify KILL / DOWNGRADE / PROMOTE. | `google-ads-shopping` |
| **Placements, devices, locations** | Breakdowns on Meta insights (`facebook_get_adaccount_insights` with breakdowns) and Google segments. Only judge segments with at least 50 clicks and 5 conversions. | `meta-depth-of-analysis`, `google-ads-depth-of-analysis` |
| **Audiences** | Ad sets or ad groups spending with poor results; overlapping audiences competing with each other. | `meta-performance-analysis` |
| **Fatigued creative** | Ads still spending while hook rate, CTR and conversion rate decay. | `analyse-creative` |
| **Zombie campaigns** | Campaigns with sustained spend and no conversions, well past their learning window. | Guardrails skill for the platform |
| **TikTok** | `tiktok_get_basic_report_enhanced` at ad group and ad level, and `tiktok_get_audience_report` for segments. | `tiktok-ads` |

Before recommending any pause, read `meta-custom-event-interpretation` for Meta sales campaigns that optimize for COMPLETE_REGISTRATION. Also never pause the top-converting ad in an ad set (`meta-guardrails`).

## Output

1. **Total waste:** "$6.1K in the last 30 days has no credible path back to target."
2. **Leaks:** a table with the exact query, placement, ad, audience or campaign, its spend and results against target, and the proposed fix.
3. **Held back:** items that look bad but are tests, still learning, or too small to judge.
4. **Where the savings go:** optionally, which proven campaigns could absorb the freed budget (`shift-budget`).

## Making the change

| Fix | Tool |
|---|---|
| Negative keywords, shared list | `google_ads_propose_create_negative_keyword_list` (new list, optionally attached to campaigns) or `google_ads_propose_update_negative_keyword_list` (add or remove keywords, attach or detach campaigns) |
| Negative keywords, one campaign | `google_ads_propose_update_campaigns` |
| Pause keywords or change match types | `google_ads_propose_update_adgroups` (needs criterion IDs from GAQL) |
| Exclude a device, or cut a location's bid | `google_ads_propose_update_bid_modifiers` (a device modifier of 0 excludes it) |
| Pause Google ads, ad groups or campaigns | `google_ads_propose_update_ads`, `google_ads_propose_update_adgroups`, `google_ads_propose_update_campaigns` |
| Pause Meta ads | `facebook_propose_update_ads` |
| Exclude placements or audiences, or pause Meta ad sets | `facebook_propose_update_adsets`. Targeting is a full replacement, so send the complete targeting with the change. |
| Pause Meta campaigns | `facebook_propose_update_campaigns` |
| TikTok (beta) | `tiktok_propose_update_ads`, `tiktok_propose_update_adgroups`, `tiktok_propose_update_campaigns` |
| Microsoft Ads | Read-only through the connector. Give the user the exact negatives and pauses. |

Every change: dry run → show each item with its spend and reason → the user approves in chat (they can approve some and reject others) → `mode: "live"` with only the approved `operation_ids`. Never go live without that yes.

## Put it on a schedule

Offer a weekly search term analyzer or budget leak agent. With write access and `ask_approval`, it proposes the negatives and pauses each week for approval (see `automate-with-agents`).
