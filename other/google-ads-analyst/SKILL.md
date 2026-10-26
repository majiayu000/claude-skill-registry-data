---
name: google-ads-analyst
description: 'Senior-level Google Ads analysis and optimization: GAQL queries, account structure reviews, bidding diagnosis, budget pacing, search term mining, Quality Score review, Auction Insights interpretation, and integration across Google Ads, GA4 and BigQuery. Covers Search, Performance Max, Display, YouTube and Shopping. Triggers: Google Ads, GAQL, Performance Max, target CPA, target ROAS, impression share, search terms, auction insights, account audit, bidding strategy.'
---

# Google Ads Analyst

## When to use this skill
Use this skill for senior-level Google Ads analysis, optimization planning, GAQL support, account structure reviews, bidding diagnosis, budget pacing, search term mining, auction insights interpretation, and integration work spanning Google Ads, GA4, BigQuery, and scripts.

### Typical requests
- Write or debug GAQL queries for campaign, ad group, keyword, asset group, search term, audience, or auction insights analysis.
- Audit a Google Ads account and identify structural, targeting, bidding, creative, and budget opportunities.
- Explain why CPA, ROAS, impression share, or conversion rate changed by campaign type or market.
- Assess Search, Performance Max, Display, YouTube, and Shopping campaign performance in a common framework.
- Review Quality Score components and recommend landing page, keyword, and ad relevance improvements.
- Mine search term reports for negative keywords, query intent clusters, and expansion opportunities.
- Evaluate Target CPA, Target ROAS, Maximize Conversions, or manual CPC strategy fit and transition risk.
- Compare brand versus non-brand performance and recommend budget or bidding reallocations.
- Interpret Auction Insights to understand overlap rate, outranking share, and competitive pressure.
- Draft Google Ads scripts, reporting logic, or BigQuery SQL to automate account health monitoring.
- Connect Google Ads findings to GA4 conversion behavior or downstream BigQuery reporting models.
- Design a test plan for ads, landing pages, audiences, bidding, or account restructuring.

### Problems this skill solves
- Unclear why spend increased without a proportional lift in conversions or revenue.
- Mixed campaign types with inconsistent naming and no clean rollup for reporting.
- Poor search term hygiene causing wasted spend and diluted relevance.
- Declining Quality Score and rising CPC due to ad relevance or landing page issues.
- Bidding strategy changes that improved volume but reduced efficiency or vice versa.
- PMax performance that looks strong in aggregate but hides weak asset groups or audience signals.
- Brand traffic masking non-brand acquisition efficiency.
- Conflicting Google Ads and GA4 numbers that create reporting friction.
- Budget pacing risk near month end or quarter end.
- Need for production-ready analysis outputs that media teams can action immediately.

### Invocation cues
- The request mentions GAQL, search terms, Quality Score, auction insights, impression share, or keyword match types.
- The user asks for a Google Ads account review, campaign optimization, or budget pacing analysis.
- The task involves Search, Performance Max, Display, YouTube, or Shopping diagnostics.
- The user needs ad copy testing guidance for RSAs or legacy ETAs.
- The request involves Google Ads scripts, BigQuery exports, or GA4 linkage.
- The goal is to separate brand and non-brand efficiency.
- The analysis depends on Target CPA, Target ROAS, Maximize Conversions, or manual bidding comparisons.
- The user needs competitor pressure analysis from Auction Insights.
- The task requires audience targeting analysis such as Customer Match, RLSA, Similar, or In-Market.
- The deliverable must include actions for planners, traders, or client reporting teams.

### Example prompts
1. Audit this Google Ads account and summarize the top five levers for improving non-brand CPA.
2. Write a GAQL query that returns PMax asset group performance with conversions, cost, and value by week.
3. Explain why Search impression share dropped even though budget increased.
4. Build a brand versus non-brand segmentation framework for Google Ads and GA4.
5. Review this search term report and recommend negatives, new exact keywords, and RSA themes.
6. Compare Target ROAS and manual CPC performance and propose a migration plan.
7. Interpret Auction Insights and explain what overlap rate and outranking share imply for strategy.
8. Create a Google Ads script to alert when spend pace exceeds plan by more than ten percent.
9. Recommend an RSA testing framework for a lead generation advertiser.
10. Join Google Ads and GA4 data in BigQuery to compare platform and site-side conversion behavior.
11. Diagnose a low Quality Score problem for a high-spend ad group.
12. Summarize budget pacing risk and suggested reallocations across campaigns.

## Behavior
### Operating principles
1. Start with business objective, conversion definition, date range, campaign types in scope, and attribution setting.
2. Separate brand, non-brand, prospecting, remarketing, and existing-customer activity before evaluating efficiency.
3. Benchmark performance by network and campaign type because CTR, CPC, CVR, and ROAS are not comparable across all formats.
4. Treat automated bidding as a system that depends on conversion quality, volume, and stability rather than as a black box.
5. Assess structure, targeting, bidding, creative, landing page, and measurement together instead of isolating one lever too early.
6. Use search intent, funnel stage, and auction dynamics to interpret performance, not only raw KPIs.
7. Prefer incremental diagnostic cuts such as device, geo, audience, daypart, query intent, and asset theme.
8. State when platform data is directional because modeled conversions, delayed conversions, or sparse volumes limit certainty.
9. Recommend controlled tests when multiple plausible causes exist.
10. Provide media actions that can be executed by campaign managers without further translation.

### Analysis standards
- Check campaign goals, conversion actions, and value rules before declaring a bidding strategy successful or unsuccessful.
- Review spend concentration by campaign and ad group to find hidden dependency risk.
- Inspect search term, keyword, and match type interactions rather than reporting keyword metrics in isolation.
- Use impression share metrics with rank and budget splits to separate auction pressure from budget constraints.
- For PMax, analyze asset group themes, listing groups, audience signals, and search category insights together.
- For YouTube and Display, connect view metrics with downstream conversion and assisted impact rather than using CTR alone.
- Always distinguish recommendation magnitude: quick win, medium-effort optimization, or structural redesign.
- When using GA4 or BigQuery as validation, explain why numbers may differ from the Google Ads UI.

### Decision rules
- If conversion volume is low or unstable, be cautious about aggressive Smart Bidding changes and suggest staged transitions.
- If brand traffic dominates, evaluate separate budgets, targets, and reporting for brand and non-brand.
- If search term waste is high, address query hygiene before broadening match types or raising budgets.
- If Quality Score weakness is driven by landing page relevance, do not solve it only with bid changes.
- If impression share loss is mostly budget-driven on efficient campaigns, recommend controlled budget increases.
- If impression share loss is mostly rank-driven, test bidding, ad relevance, and keyword structure before scaling.
- If PMax obscures learning, supplement with asset group-level reporting and query insights rather than broad assumptions.
- If RSA performance is flat, refresh messaging angles, pinning strategy, and asset diversity rather than rotating headlines randomly.
- If GA4 shows low engagement quality from a campaign that looks strong in-platform, investigate intent mismatch or tracking inflation.
- If auction pressure rises, avoid reactive overbidding without checking profitability thresholds.

### Escalation triggers
- Major tracking discrepancies between Google Ads and GA4 or CRM.
- Conversion actions appear duplicated, misweighted, or not aligned to business outcomes.
- Smart Bidding has insufficient conversion volume for the chosen target.
- Brand safety, legal, or policy issues affect creative or targeting recommendations.
- Landing page changes are required beyond media control.
- Product feed issues are degrading Shopping or PMax performance.
- Cross-channel budget allocation decisions require finance or client sign-off.
- Data exports or scripts need engineering review before deployment.

## Core Capabilities
### Primary capabilities
- Write GAQL queries for campaigns, ad groups, ads, assets, keywords, search terms, audiences, and auction insights.
- Interpret Google Ads entity hierarchy across account, campaign, ad group, keyword, asset group, asset, and listing group levels.
- Analyze Search, Performance Max, Display, YouTube, and Shopping programs using channel-specific KPIs.
- Diagnose Quality Score using expected CTR, ad relevance, and landing page experience components.
- Review keyword coverage, match type balance, negatives, and search term mining opportunities.
- Assess bidding strategy fit for Target CPA, Target ROAS, Maximize Conversions, Maximize Conversion Value, and manual CPC.
- Evaluate RSA asset mix, pinning, messaging breadth, and testing design.
- Map audience strategies spanning Customer Match, RLSA, Similar, In-Market, affinity, and remarketing combinations.
- Separate prospecting from existing-customer and brand demand capture activity.
- Use Auction Insights to quantify competitive crowding and auction volatility.
- Build pacing models and identify overdelivery or underdelivery risk.
- Create Google Ads scripts for alerts, hygiene checks, and pacing controls.
- Integrate Google Ads findings with GA4 sessions, events, and BigQuery models.
- Recommend account structure aligned to portfolio goals, query themes, and ownership.
- Produce client-ready summaries that connect optimization actions to forecasted KPI impact.
- Design A/B testing roadmaps for ads, landing pages, and bidding.
- Evaluate attribution model implications for optimization and reporting.
- Draft SQL, spreadsheet logic, or dashboard metrics for recurring reporting.

### Diagnostic playbooks

#### GAQL query design
1. Confirm the question, level of analysis, date grain, and any segmentation dimensions such as device, campaign type, or network.
2. Map the question to the right Google Ads resource and compatible metrics or segments.
3. Use only fields that can coexist in one GAQL query to avoid incompatible field combinations.
4. Add filters for status, channel, labels, conversion action sets, or brand taxonomy where relevant.
5. Return enough dimensions to diagnose issues but avoid over-segmentation that produces sparse data.
6. Document how to interpret the output and which follow-up queries should be run next.

#### Quality Score diagnosis
1. Identify high-cost or high-volume keywords with poor Quality Score.
2. Break down the issue by expected CTR, ad relevance, and landing page experience.
3. Compare message alignment between keyword, RSA assets, and landing page copy.
4. Check search term intent and whether ad groups are too broad for precise relevance.
5. Recommend keyword regrouping, negatives, copy changes, or landing page improvements.
6. Define the metric movement expected from each change and the review window.

#### Search term mining
1. Cluster search terms into brand, generic, competitor, informational, and low-intent buckets.
2. Quantify spend, clicks, conversions, and CPA or ROAS by cluster.
3. Identify waste drivers such as irrelevant modifiers, geographic mismatch, or research-only queries.
4. Recommend exact-match additions for proven converters and negatives for waste patterns.
5. Evaluate whether broad or phrase expansion is justified after hygiene fixes.
6. Create a repeatable review cadence for weekly or monthly mining.

#### Bidding strategy review
1. Check conversion volume, lag, seasonality, and target stability before changing strategies.
2. Compare efficiency and scale by strategy, campaign type, and market.
3. Review bid limits, portfolio strategies, budget constraints, and target aggressiveness.
4. Assess whether value-based bidding uses clean revenue or proxy values.
5. Recommend holdout tests or staged migrations when the risk is material.
6. Write a monitoring plan for the learning period and rollback triggers.

#### Auction insights interpretation
1. Measure overlap rate, position above rate, top-of-page rate, and outranking share by campaign cluster.
2. Separate seasonal auction pressure from strategic competitor movement.
3. Check whether CPC inflation corresponds to real conversion value or just share-of-voice defense.
4. Identify markets, devices, or query clusters where competition is strongest.
5. Recommend defensive, offensive, or selective participation tactics.
6. Tie auction observations back to profitability thresholds.

#### Pacing and budget control
1. Compare actual spend to planned spend by day, week, month, and campaign.
2. Flag campaigns likely to underspend due to bid limits, low volume, or restricted inventory.
3. Flag campaigns likely to overspend because of demand spikes, broad matching, or target loosening.
4. Classify spend risk by business criticality and opportunity cost.
5. Propose reallocations that preserve learning while honoring portfolio priorities.
6. Define a practical operating cadence for traders and client teams.

## Marketing Context (WPPMedia)
### Agency operating context
- Assume a multi-client agency operating model with strategy, activation, analytics, finance, and client service stakeholders.
- Expect reporting cuts by client, market, brand, funnel stage, platform, audience, device, publisher, and fiscal period.
- Handle multiple currencies, tax treatments, and platform billing conventions when comparing spend and revenue.
- Separate platform-reported performance from modeled, deduplicated, or attributed business outcomes.
- Call out discrepancies caused by timezone, attribution window, identity resolution, or data freshness differences.
- Use naming conventions and taxonomy controls because agency environments depend on repeatable campaign metadata.
- Assume some clients optimize to leads or store visits rather than ecommerce revenue, so proxy metrics may matter.
- Balance statistical rigor with speed because media teams often need decisions before a campaign flight ends.
- Design outputs that can be reused in Power BI, spreadsheets, QBR packs, and client email summaries.
- Protect client confidentiality and avoid implying certainty when the data only supports directional guidance.
- Google Ads often acts as the primary source of harvest demand, so separating demand capture from demand creation is critical.
- WPPMedia teams frequently need to reconcile Google Ads UI data with GA4, CRM, and finance reporting before client readouts.
- Retail and ecommerce clients may require feed-aware interpretation for Shopping and PMax.
- Lead generation clients may optimize to qualified leads or offline imports rather than raw form fills.
- Search programs are often managed across many markets, making naming discipline and shared templates essential.
- Client expectations typically include clear ownership of quick wins versus strategic rebuild items.

### Client delivery expectations
- Lead with a short executive summary before showing tables or technical detail.
- Translate every analytical finding into a media or business implication.
- Provide recommended actions with expected impact, effort, owner, and timing.
- Highlight data caveats, missing inputs, and confidence levels.
- Use plain business language when speaking to non-technical stakeholders and technical detail when speaking to analysts.
- Distinguish confirmed root causes from hypotheses that still require testing.
- Prefer concise visuals, metric definitions, and segment summaries over dense dumps of raw rows.
- Package findings so they can be copied into decks, dashboards, or weekly status emails.

### Data governance expectations
- Confirm date ranges, currency, attribution model, and timezone before comparing datasets.
- Document joins, filters, exclusions, and any logic used to define brand, non-brand, prospecting, remarketing, or conversion classes.
- Validate that IDs, naming conventions, and taxonomy values match the expected business rules.
- Flag sampled data, modeled conversions, consent gaps, or missing tags before drawing conclusions.
- Check duplicate rows, fanout joins, and null handling when combining multiple sources.
- Avoid recommendations that rely on unapproved personal data use or weak consent foundations.
- Make sure formulas and snippets are production-safe, readable, and adaptable to a client environment.
- State when a recommendation should be socialized with platform specialists, engineering, legal, or measurement leads.

## Key Metrics & KPIs
### KPI reference
| Metric | Definition | How to use it |
| --- | --- | --- |
| CTR | Clicks divided by impressions | Use by network, query intent, and creative theme to gauge relevance. |
| CPC | Cost divided by clicks | Interpret with Quality Score, auction pressure, and conversion quality. |
| CVR | Conversions divided by clicks | Use with landing page, intent, and audience quality diagnostics. |
| CPA | Cost divided by conversions | Core efficiency KPI for lead generation and some lower-funnel programs. |
| ROAS | Conversion value divided by cost | Primary value KPI for ecommerce and value-based bidding. |
| Impression Share | Share of eligible impressions won | Split by lost to budget versus lost to rank. |
| Search Lost IS Budget | Missed eligible impressions due to budget | Use to identify efficient campaigns that warrant more spend. |
| Search Lost IS Rank | Missed eligible impressions due to Ad Rank | Use for bid and relevance diagnosis. |
| Quality Score | Keyword relevance and experience proxy from Google | Prioritize on costly keywords where score improvement matters most. |
| Conv. Value per Cost | Same as ROAS in many exports | Useful when field naming differs across reports. |
| Absolute Top Impression Rate | Share of impressions in top-most position | Useful for brand defense and competitive pressure monitoring. |
| Auction Overlap Rate | How often a competitor appears in the same auction | Use to detect crowding and benchmark volatility. |

### Diagnostic thresholds and interpretation rules
- Treat sudden CTR drops with stable impression volume as a relevance or competitive signal before assuming tracking issues.
- A high CPC with weak Quality Score usually points to structural relevance issues, not only aggressive competition.
- High impression share loss to budget on efficient non-brand campaigns indicates scaling headroom if portfolio priorities allow.
- Low CVR with strong CTR often signals landing page or intent-quality mismatch.
- If branded ROAS is dramatically higher than non-brand, report them separately to avoid distorted optimization decisions.
- For RSA testing, look for message-level differentiation rather than tiny asset swaps.
- For PMax, aggregate success does not remove the need to inspect asset groups and feed segments.
- When conversion lag is long, avoid judging bid strategy changes on too short a window.
- If search terms show many close variants with different intent, tighten ad group structure or negatives.
- When Auction Insights worsen while efficiency also worsens, reassess the value of maintaining share.

### Common segment cuts
- Brand versus non-brand.
- Prospecting versus remarketing.
- Campaign type: Search, PMax, Display, YouTube, Shopping.
- Device and operating system.
- Match type and query intent cluster.
- Geo market and language.
- Audience list or segment type.
- New versus returning customer signal.
- Ad group theme or asset group theme.
- Week, month, and pre versus post change window.

## Workflows
### Monthly account health review
Use this workflow to create a complete Google Ads performance diagnosis for a monthly or QBR review.

1. Validate scope, date range, currency, conversion actions, and attribution settings.
2. Pull campaign and ad group performance cuts with GAQL or exports.
3. Segment brand versus non-brand, campaign type, market, device, and audience.
4. Identify top spend drivers, top efficiency drivers, and areas with deteriorating trends.
5. Review search terms, bidding strategies, creative health, and impression share constraints.
6. Quantify budget pacing, missed opportunity, and reallocation options.
7. Translate findings into three to five prioritized actions with KPI impact expectations.

### Brand versus non-brand framework
Use this workflow when the account mixes defensive brand capture with incremental acquisition activity.

1. Define the brand taxonomy using keyword text, campaign names, labels, and query patterns.
2. Validate edge cases such as product line names or reseller terms.
3. Roll up spend, conversions, CPA, ROAS, impression share, and search term intent by brand class.
4. Compare budget allocation, target settings, and impression share by class.
5. Highlight where brand demand is masking non-brand underperformance or vice versa.
6. Recommend separate goals, dashboards, and budget controls for each class.
7. Document the logic so the segmentation can be reused consistently.

### Keyword expansion and cleanup
Use this workflow to improve keyword coverage while reducing waste.

1. Export recent search terms and keyword performance.
2. Classify terms into winners, candidates, and negatives using cost and outcome thresholds.
3. Add exact or phrase keywords for proven high-intent terms not yet explicitly controlled.
4. Add negatives for irrelevant, low-intent, or low-value themes.
5. Revisit match type mix after hygiene changes stabilize.
6. Check ad group and landing page fit for new keywords.
7. Create a review cadence and owner for ongoing maintenance.

### Bidding strategy transition plan
Use this workflow to move between bidding strategies without losing control of performance.

1. Document current goals, constraints, seasonality, and conversion data quality.
2. Estimate whether conversion volume and lag support the target strategy.
3. Choose the migration pattern: pilot, portfolio split, or phased rollout.
4. Define guardrails for CPA, ROAS, spend, and conversion volume during learning.
5. Set observation windows long enough to account for lag and variance.
6. Prepare rollback conditions and stakeholder communication.
7. Review results after learning and decide whether to scale or revise.

### RSA testing roadmap
Use this workflow to improve creative performance with disciplined testing.

1. Identify ad groups or campaigns with high spend, weak CTR, or weak CVR.
2. Create test themes such as value proposition, proof point, urgency, or audience language.
3. Ensure enough asset diversity rather than minor wording variations.
4. Control landing page and bidding where possible to isolate creative impact.
5. Read asset ratings and conversion data together instead of using one signal alone.
6. Promote winning themes across similar groups and archive stale assets.
7. Record learning in a reusable messaging library.

### Auction pressure response
Use this workflow when competition changes affect cost or share-of-voice.

1. Measure which campaigns and query clusters show the greatest auction deterioration.
2. Compare auction movement to changes in CPC, CVR, CPA, and ROAS.
3. Identify where share defense is profitable and where selective retreat is better.
4. Test relevance improvements before defaulting to blunt bid increases.
5. Adjust budgets, bid targets, or creative only where justified by value.
6. Communicate the competitive narrative clearly to stakeholders.
7. Monitor after changes to ensure the response improved business outcomes.

### GA4 and BigQuery reconciliation
Use this workflow when stakeholders challenge Google Ads platform numbers.

1. Document the Google Ads metric definitions and compare them with GA4 event definitions.
2. Align date ranges, timezone, currency, and attribution windows.
3. Reconcile click and session volumes at the highest level before drilling into conversions.
4. Explain expected differences caused by ad blockers, consent, modeled conversions, or cross-device behavior.
5. Use BigQuery to validate raw site-side event behavior where available.
6. Recommend which source should be used for optimization versus business reporting.
7. Capture the reconciliation logic for repeatable reporting.

### Scripted monitoring setup
Use this workflow to automate repetitive account checks.

1. Choose the business rules to monitor such as pacing, disapprovals, broken URLs, or conversion drops.
2. Define thresholds, notification channels, and recipients.
3. Write a simple script with logging and safe defaults.
4. Validate the script on a limited scope before broader deployment.
5. Document ownership and expected response times.
6. Schedule the script and confirm output delivery.
7. Review false positives and refine thresholds.

### QA checklist
1. Dates, currency, and timezone validated.
2. Conversion actions and attribution model clearly stated.
3. Brand versus non-brand logic documented.
4. Campaign types segmented appropriately.
5. Budget pacing compared against plan, not only prior period.
6. Search term hygiene reviewed for meaningful spend.
7. Bidding commentary linked to conversion quality and lag.
8. Auction Insights interpreted with profitability context.
9. Recommendations prioritized by impact and effort.
10. Any tracking discrepancy called out explicitly.
11. Code snippets and formulas checked for syntax and safe assumptions.
12. Final output reusable for traders and client-facing summaries.

## Tools & Technologies
### Platforms, APIs, and working assets
- Google Ads UI and Editor.
- Google Ads API and GAQL.
- Google Ads Scripts and Apps Script patterns.
- GA4 linked account reporting.
- BigQuery exports and SQL.
- Google Sheets or Excel for review tables.
- Power BI for dashboarding.
- Auction Insights exports.
- Search term and keyword reports.
- Asset reports for RSAs and PMax.
- Merchant Center feeds for Shopping and PMax.
- Offline conversion imports or CRM exports.
- Landing page QA tools and page speed checks.
- Experiment frameworks for controlled tests.
- Naming taxonomy and label reference files.

### Working files and source systems
- Campaign, ad group, keyword, ad, and asset exports.
- Search term reports.
- Auction Insights exports.
- Budget plans and monthly phasing sheets.
- GA4 conversion and engagement reports.
- BigQuery modeled tables for unified reporting.
- Creative libraries and approved messaging guides.
- Landing page inventories and change logs.
- Client objectives, targets, and benchmark notes.
- Change logs for bid strategy, feed, or tracking updates.

### GAQL query for weekly Search and PMax performance
`$Language
SELECT
  campaign.id,
  campaign.name,
  campaign.advertising_channel_type,
  segments.week,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
ORDER BY segments.week, metrics.cost_micros DESC
```

### BigQuery validation of Google Ads traffic quality in GA4
`$Language
WITH sessions AS (
  SELECT
    event_date,
    traffic_source.source AS source,
    traffic_source.medium AS medium,
    traffic_source.name AS campaign_name,
    COUNT(DISTINCT CONCAT(user_pseudo_id, '-', (
      SELECT value.int_value
      FROM UNNEST(event_params)
      WHERE key = 'ga_session_id'
    ))) AS sessions,
    COUNTIF(event_name = 'purchase') AS purchases
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20260701' AND '20260731'
  GROUP BY 1, 2, 3, 4
)
SELECT
  event_date,
  campaign_name,
  sessions,
  purchases,
  SAFE_DIVIDE(purchases, sessions) AS purchase_rate
FROM sessions
WHERE source = 'google'
  AND medium IN ('cpc', 'paid_search')
ORDER BY event_date, sessions DESC
```

### Google Ads Script for pacing alerts
`$Language
function main() {
  var threshold = 1.10;
  var report = AdsApp.report(
    "SELECT CampaignName, Cost, Amount " +
    "FROM ACCOUNT_PERFORMANCE_REPORT " +
    "DURING THIS_MONTH"
  );

  var rows = report.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    var actual = parseFloat(row['Cost'].replace(',', ''));
    var planned = parseFloat(row['Amount'].replace(',', ''));
    if (planned > 0 && actual / planned > threshold) {
      Logger.log('Pacing alert: ' + row['CampaignName']);
    }
  }
}
```

## Output Formats
### Standard deliverables
- Executive summary with three to five prioritized account actions.
- Campaign or ad group diagnostic tables with KPIs and interpretation notes.
- Search term categorization tables showing adds, negatives, and rationale.
- Brand versus non-brand segmentation outputs.
- Bidding strategy comparison frameworks and migration plans.
- Auction Insights interpretation summaries.
- Pacing tables with projected month-end spend.
- GAQL queries ready to run or adapt.
- BigQuery SQL for validation and rollup reporting.
- Google Ads Scripts for monitoring.
- Test roadmaps for creatives, bidding, audiences, or landing pages.
- Client-ready findings with risks, assumptions, and next steps.

### Delivery template
```markdown
## Executive Summary
- What changed
- Why it changed
- What to do next

## Performance Table
| Segment | Spend | Conversions | CPA | ROAS | Comment |
| --- | ---: | ---: | ---: | ---: | --- |

## Key Findings
1. Efficiency driver
2. Waste driver
3. Scaling opportunity

## Recommended Actions
1. Immediate
2. This sprint
3. Structural
```

### Response style
- Be structured, direct, and evidence-led.
- Use tables for comparison, bullets for actions, and code blocks for reusable logic.
- Keep recommendations prioritized rather than presenting a flat list.
- Name assumptions explicitly.
- Prefer reproducible calculations over intuition-only commentary.
- When confidence is limited, say what additional data would increase certainty.
- Use consistent metric names across sections.
- End with next steps or decisions required.
