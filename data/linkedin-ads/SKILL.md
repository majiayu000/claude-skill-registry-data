---
name: linkedin-ads
description: "Use for LinkedIn Ads (Campaign Manager) questions: campaign and campaign group performance, spend, CTR, CPC, CPL and conversions, breakdowns by company, job title, industry or seniority, and looking up targeting values. Read-only through GoMarble; changes are given as instructions for Campaign Manager."
---

# LinkedIn Ads

Analyze LinkedIn Ads through GoMarble. The connector reads LinkedIn; it can't change campaigns. When a change is needed, give the user the exact edit to make in Campaign Manager.

## Tools

| Need | Tool |
|---|---|
| Ad accounts | `linkedin_list_ad_accounts` (start here; other tools need the `account_id`) |
| Campaign groups (status, budget, schedule) | `linkedin_get_ad_campaign_groups` |
| Campaigns (type, objective, status, bidding, targeting summary) | `linkedin_get_campaigns` |
| Performance: impressions, clicks, spend, conversions, leads, with pivots such as campaign, creative, company, job title, industry, seniority or country | `linkedin_get_ad_analytics` |
| Targeting values for a facet (industries, titles, companies, skills, and so on) | `linkedin_get_targeting_entities` |

## How to analyze

- **Judge by objective.** Lead gen campaigns: cost per lead, lead volume, and form completion rate where available. Website conversions: CPA. Awareness: CPM, reach and frequency. Don't judge an awareness campaign on CPL.
- **B2B context.** LinkedIn CPCs and CPMs are high by design. Compare against the account's own history and the value of a lead, not other channels' costs.
- **Who is actually seeing the ads.** Pivot analytics by company, job title, seniority and industry to check delivery matches the intended buyer. Delivery drifting to junior titles or irrelevant industries is the most common waste.
- **Creative fatigue.** LinkedIn audiences are small, so frequency climbs fast. Watch CTR decay as frequency rises.
- **Enough data.** Don't judge a campaign or segment with only a handful of conversions; say it's too early.
- **Cross-check.** Compare LinkedIn-reported leads with the CRM or GA4 (`ga4-source-of-truth`) when available; view-through conversions can inflate results.

## Output

Performance by campaign group and campaign against the target, who the ads reached, what's fatiguing, and specific recommendations written as Campaign Manager steps, for example "In campaign X, exclude seniority 'Entry' and 'Training'".

For cross-channel questions, use `diagnose-performance` or `build-reports`.
