---
name: microsoft-ads
description: "Use for Microsoft Advertising (Bing Ads) questions: campaign, ad group, keyword and ad performance, shared budgets, quality score, change history, search term and keyword waste, and keyword ideas with volume and bid estimates. Read-only through GoMarble; changes are given as instructions for Microsoft Advertising."
---

# Microsoft Ads (Bing)

Analyze Microsoft Advertising through GoMarble. The connector reads Microsoft Ads; it can't change campaigns. When a change is needed, give the user the exact edit to make in Microsoft Advertising, or to import from Google Ads.

## Tools

| Need | Tool |
|---|---|
| Accounts | `bing_ads_list_accounts` (start here) |
| Performance at account, campaign, ad group, keyword or ad level | `bing_ads_get_performance` |
| Campaigns with status, budget and bid strategy | `bing_ads_list_campaigns` |
| Ad groups in a campaign | `bing_ads_list_ad_groups` |
| Keywords in an ad group, with bids and quality score | `bing_ads_list_keywords` |
| Ads in an ad group (all types) | `bing_ads_list_ads`. A filtered zero count doesn't mean the ad group has no ads. |
| Shared budgets and which campaigns use them | `bing_ads_list_budgets` |
| What changed, and when | `bing_ads_get_change_history` |
| Keyword ideas with volume, competition and bid estimates | `bing_ads_keyword_ideas` (US, UK, CA, AU, FR and DE only; English, French or German) |

## How to analyze

Microsoft Ads search campaigns work like Google Search, so apply the Google methodology:
- Search terms and keywords: Q1–Q5 classification and rank vs budget pressure (`google-ads-search-analysis`).
- Keyword research: intent first, real volume and bids only, never estimates (`google-ads-keywordplanner`).
- Guardrails: at most 20% per budget move, don't raise bids with wasteful terms present, and don't change bids and budget together (`google-ads-guardrails`).

Microsoft-specific checks:
- **Imported from Google?** Many accounts are imported. Settings that don't translate (bid strategies, audiences, extensions) and stale imports are common problems.
- **Quality score** from `bing_ads_list_keywords` explains high CPCs.
- **Search partners and syndication** can drive cheap, low-quality traffic; compare partner performance where reported.
- **Shared budgets** mean one campaign can starve another. Check `bing_ads_list_budgets` before recommending budget changes.

## Output

Performance against target, the specific waste and opportunities, and recommendations written as Microsoft Advertising steps (negatives to add, bids to change, budgets to move).

For cross-channel questions, use `diagnose-performance` or `build-reports`.
