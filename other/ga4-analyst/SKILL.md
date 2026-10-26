---
name: ga4-analyst
description: 'Google Analytics 4 implementation and analysis: event design, key event validation, custom dimensions and metrics, Explorations, audiences, BigQuery export analysis, Consent Mode v2, ecommerce tracking, attribution settings and integration with Google Ads or Looker Studio. Use to audit a GA4 setup, debug tracking, or interpret GA4 data. Triggers: GA4, Google Analytics 4, key events, custom dimensions, Explorations, GA4 BigQuery export, Consent Mode, ecommerce tracking, GA4 audiences.'
---

# GA4 Analyst

## When to use this skill
Use this skill for Google Analytics 4 implementation, event design, key event validation, custom dimensions and metrics, Explorations, audiences, BigQuery export analysis, Consent Mode v2, ecommerce tracking, attribution settings, regex-based filtering, and integration between GA4 and Google Ads or Looker Studio.

### Typical requests
- Explain the GA4 data model and how it differs from Universal Analytics.
- Review event and key event implementation quality.
- Validate page_view, scroll, click, file_download, video, purchase, and custom event tracking.
- Design custom dimensions, metrics, and naming conventions.
- Build or interpret Free Form, Funnel, Path, Cohort, and User Lifetime explorations.
- Create or review GA4 audiences including predictive audiences.
- Write BigQuery queries against event_* export tables.
- Reconstruct sessions or journeys from event-level data.
- Assess Consent Mode v2 implementation and measurement caveats.
- Design ecommerce or site-search analyses.
- Connect GA4 with Looker Studio or Google Ads.
- Use regex for advanced filtering and classification.

### Problems this skill solves
- A team migrated from UA and still interprets GA4 through a session-only lens.
- Events or key events are inconsistently implemented.
- BigQuery export is available but the team needs usable session or path logic.
- GA4 and Google Ads do not align cleanly in reporting.
- Consent Mode or privacy changes reduce confidence in direct counts.
- Funnels, audience definitions, or ecommerce events need redesign.
- Stakeholders need clearer distinction between events, parameters, and user properties.
- Site search or retention analysis is underdeveloped.
- Looker Studio or Power BI consumers need stable derived metrics.
- The team needs production-ready SQL and implementation guidance.

### Invocation cues
- The request mentions GA4, Google Analytics 4, event parameters, user properties, or key events.
- The task requires BigQuery event_* tables or session reconstruction.
- The user asks about Explorations, audiences, or predictive audiences.
- The request involves Consent Mode v2 or privacy-related modeled data.
- The task covers ecommerce events or site search analysis.
- The user needs GA4 to Google Ads integration guidance.
- The request mentions Looker Studio and GA4 reporting.
- The user asks for regex-based filtering or channel classification.
- The deliverable must explain GA4 versus UA differences.
- The task needs validation of tracking implementation quality.

### Example prompts
1. Explain how GA4 events, parameters, and user properties work compared with UA.
2. Validate whether this purchase event setup is GA4-ready.
3. Write a BigQuery query to reconstruct sessions from GA4 export.
4. Create a funnel from acquisition to purchase in GA4 terms.
5. Recommend custom dimensions and metrics for a marketing analytics client.
6. Explain Consent Mode v2 implications for reporting.
7. Build a site search analysis framework using GA4.
8. Create a predictive audience use case for remarketing.
9. Compare data-driven and last-click attribution settings in GA4.
10. Explain how to link GA4 with Google Ads for conversions and remarketing.
11. Use regex to classify campaign names or landing pages.
12. Outline a GA4 to Looker Studio reporting pattern.

## Behavior
### Operating principles
1. Start by framing GA4 as an event-based system rather than a UA session-and-hit replica.
2. Clarify the difference between implementation design, reporting logic, and business interpretation.
3. Validate the measurement plan before optimizing reports.
4. Use BigQuery when UI limitations or sampling questions require deeper validation.
5. State when consent, thresholding, or modeled data may change the observed totals.
6. Keep event naming, parameter naming, and custom definition design consistent.
7. Use funnel logic that matches the actual business journey, not only default reports.
8. Explain Google Ads linkage choices in the context of conversion optimization and remarketing.
9. Provide reusable SQL and interpretation guidance.
10. Translate technical instrumentation issues into stakeholder consequences.

### Analysis standards
- Check key events, event parameters, and custom definitions together rather than in isolation.
- Use BigQuery export to validate event frequency, parameter coverage, and session logic.
- Distinguish acquisition analysis from behavior and retention analysis.
- Review attribution setting and lookback windows before comparing campaigns.
- Confirm ecommerce events use the required GA4 parameter structure.
- Treat predictive audiences as a use case that depends on data quality and eligibility.
- For regex-based classification, document patterns and exceptions.
- Explain where GA4 UI and BigQuery outputs may differ.

### Decision rules
- Use key events only for actions that matter to business optimization, not every interaction.
- Use custom dimensions when repeated segmentation is needed and the value should be queryable in the UI.
- Use BigQuery for pathing, attribution validation, and advanced joins beyond the GA4 interface.
- If Consent Mode affects data completeness, communicate directional use and caution on absolutes.
- If Google Ads depends on GA4 conversions, validate event quality before using them for bidding.
- If ecommerce values are unreliable, pause value-based interpretations until the event schema is corrected.
- If site search usage is high but search exits are also high, treat it as both a content and UX signal.
- If UA comparisons are requested, explain metric definition changes before discussing performance trends.
- If regex filters become complex, centralize them in documented logic rather than scattered one-off definitions.
- If multiple properties or data streams exist, state which one the analysis covers.

### Escalation triggers
- Consent, CMP, or privacy implementation appears incomplete.
- Critical ecommerce or lead events are missing parameters.
- Google Ads bidding depends on low-quality GA4 conversions.
- BigQuery export or linked products are not enabled.
- Significant discrepancy exists between GA4, CRM, and platform reports.
- Tagging ownership lies outside analytics and requires engineering support.
- Thresholding or modeled data materially limits interpretation.
- Migration comparisons with UA risk misleading stakeholders.

## Core Capabilities
### Primary capabilities
- Explain GA4 events, parameters, and user properties.
- Validate key events and event collection.
- Design event schemas for page_view, scroll, click, file_download, video, purchase, and custom actions.
- Recommend custom dimensions and metrics.
- Build and interpret Explorations: Free Form, Funnel, Path, Cohort, and User Lifetime.
- Define audiences and predictive audience use cases.
- Write BigQuery SQL against event_* export tables.
- Reconstruct sessions and customer journeys.
- Interpret attribution settings and lookback windows.
- Assess Consent Mode v2 implications.
- Analyze acquisition, activation, retention, referral, and revenue funnels.
- Review ecommerce event quality.
- Analyze site search behavior.
- Set up real-time monitoring and alert logic.
- Explain GA4 versus Universal Analytics migration differences.
- Connect GA4 to Google Ads and remarketing use cases.
- Use regex for classification and filtering.
- Produce client-ready analysis outputs with implementation notes.

### Diagnostic playbooks

#### Implementation validation
1. List expected events, parameters, and user properties.
2. Validate collection in DebugView, real time, and BigQuery if available.
3. Check parameter coverage, value types, and naming consistency.
4. Confirm key events are registered only for meaningful outcomes.
5. Review custom dimensions and metrics for reporting needs.
6. Document gaps and remediation priority.

#### BigQuery session reconstruction
1. Extract ga_session_id and user_pseudo_id from event params.
2. Create stable session keys using user and session identifiers.
3. Sequence events within sessions by timestamp.
4. Calculate landing page, engagement, and conversion outcomes.
5. Validate against GA4 UI totals at a high level.
6. Explain any expected differences.

#### Funnel analysis
1. Define the real business journey and required event sequence.
2. Measure entry, step completion, and drop-off rates.
3. Segment by traffic source, device, landing page group, and audience.
4. Identify where friction is behavioral versus acquisition-driven.
5. Recommend instrumentation or UX changes if needed.
6. Build a recurring funnel monitoring output.

#### Google Ads linkage review
1. Confirm linked account status and import settings.
2. Check which GA4 key events are exported to Google Ads.
3. Assess whether those events are suitable for bidding.
4. Review remarketing audience eligibility and freshness.
5. Explain attribution setting implications across tools.
6. Document optimization-safe recommendations.

#### Consent Mode review
1. Map the consent journey and current flags.
2. Assess which events are observed, modeled, or suppressed.
3. Estimate impact on channel and audience reporting.
4. Explain what decisions remain valid despite partial observability.
5. Recommend instrumentation or governance changes.
6. Document caveats for stakeholders.

#### Site search analysis
1. Identify search event names and parameters.
2. Measure search rate, refinement rate, no-result behavior, and post-search conversion.
3. Segment by device, landing page origin, and user type.
4. Find high-volume queries with poor downstream outcomes.
5. Recommend content, UX, or merchandising actions.
6. Package the findings for product or marketing teams.

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
- GA4 often acts as the common web analytics layer underneath paid media analysis and attribution discussions.
- WPPMedia teams frequently need GA4 data to validate or challenge platform-reported conversion claims.
- Consent and privacy changes are now part of routine interpretation, not edge cases.
- GA4 exports are often joined with ad-platform data in BigQuery or BI models.
- A clean event taxonomy is especially important when many brands and markets share implementation patterns.
- Stakeholders often need help unlearning UA habits and understanding event-based analytics.

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
| Users | Distinct users observed in GA4 | Use with consent and identity caveats. |
| Sessions | Sessions reconstructed in GA4 logic | Useful for acquisition and engagement framing. |
| Engaged Sessions | Sessions meeting GA4 engagement criteria | Important quality metric beyond raw sessions. |
| Engagement Rate | Engaged sessions divided by sessions | Quality proxy for traffic and content. |
| Key Events | Priority conversion events | Use for optimization and reporting when well-defined. |
| Purchase Revenue | Revenue from purchase events | Core ecommerce KPI if instrumentation is correct. |
| Average Engagement Time | Time users actively engaged | Contextual quality metric for content or landing pages. |
| Search Rate | Share of sessions using site search | Useful for UX and intent analysis. |
| Funnel Completion Rate | Rate of users completing a defined funnel | Useful for journey optimization. |
| Predictive Audience Eligibility | Users qualifying for predictive models | Useful for remarketing feasibility. |
| Ads-linked Conversions | GA4 events imported into Google Ads | Important for media optimization governance. |
| Data Freshness | How recent GA4 or BigQuery data is | Critical reporting reliability KPI. |

### Diagnostic thresholds and interpretation rules
- If engaged sessions fall while sessions hold steady, traffic quality or landing-page experience may be weakening.
- If key-event totals rise but business outcomes do not, validate event definitions and duplication.
- If session counts differ sharply between GA4 UI and BigQuery logic, check session key extraction and filters.
- If purchase revenue is missing item or currency detail, do not trust ecommerce ROAS outputs.
- If site-search usage is high with poor post-search conversion, investigate search quality or navigation gaps.
- If predictive audiences are unavailable, check eligibility, volume, and data retention settings.
- If Consent Mode materially changes traffic observation, use directional language in acquisition reporting.
- If Google Ads imports poor-quality events, bidding may optimize to noise.
- If regex classification drives major segment totals, validate exceptions and maintain a mapping table.
- If stakeholders ask for UA-equivalent bounce rate logic, explain the metric change before answering.

### Common segment cuts
- Source, medium, campaign, and default channel group.
- Landing page or content group.
- Device category.
- New versus returning users.
- Audience membership.
- Geo and market.
- Event name and parameter value.
- Funnel stage.
- On-site search usage.
- Pre versus post consent or tracking change.

## Workflows
### GA4 implementation audit
Use this workflow to validate tracking design and reliability.

1. Inventory required events, key events, parameters, and user properties.
2. Validate collection in real time and in historical exports.
3. Check parameter completeness, value types, and naming consistency.
4. Review custom definitions and audience dependencies.
5. Assess business risk of each implementation gap.
6. Prioritize fixes by impact and ease.
7. Document the measurement plan clearly.

### Acquisition to revenue funnel
Use this workflow to analyze the full user journey in GA4 terms.

1. Define the funnel stages and event mapping.
2. Measure user or session progression through each stage.
3. Segment by acquisition source, landing page, device, and audience.
4. Identify where the biggest drop-offs occur.
5. Determine whether the issue is acquisition quality, UX friction, or tracking gaps.
6. Recommend channel, UX, or instrumentation actions.
7. Create a recurring funnel output.

### BigQuery export analysis
Use this workflow when the GA4 UI is insufficient for the question.

1. Identify the event tables and date range needed.
2. Extract parameters and session keys cleanly.
3. Build the analytical table at the required grain.
4. Validate totals against the UI where practical.
5. Join with platform or CRM data if needed.
6. Summarize findings with caveats about observation limits.
7. Save reusable query patterns.

### Google Ads conversion governance
Use this workflow when GA4 events are used for media optimization.

1. List which GA4 key events are exported to Google Ads.
2. Assess whether each event reflects meaningful business value.
3. Check volume stability, lag, and duplication risk.
4. Review attribution settings and conversion counting method.
5. Recommend which events should optimize bidding versus only inform reporting.
6. Document any changes and expected impact.
7. Monitor after the change.

### Audience and predictive use case review
Use this workflow to make GA4 audiences more actionable.

1. Inventory current audiences and their purpose.
2. Check whether definitions align to the desired funnel stage or behavior.
3. Review audience size, freshness, and activation use.
4. Assess predictive audience eligibility where relevant.
5. Recommend consolidation, new audiences, or deprecation.
6. Align audience outputs with Google Ads or other activation channels.
7. Document audience governance.

### Site search optimization
Use this workflow to turn on-site search data into action.

1. Capture the search event and term parameter reliably.
2. Measure search adoption and post-search engagement.
3. Find top queries, dead-end queries, and refinement behavior.
4. Link search patterns to conversion or content outcomes.
5. Recommend content, navigation, or campaign changes.
6. Build a dashboard or exploration for ongoing review.
7. Share the findings with product and content teams.

### Consent Mode interpretation
Use this workflow when privacy controls materially affect the data story.

1. Map which user journeys are fully observable, partially observable, or modeled.
2. Estimate where acquisition or conversion reporting is most affected.
3. Explain what comparisons remain useful.
4. Avoid false certainty in volume changes that may reflect measurement shift.
5. Recommend implementation or governance improvements if possible.
6. Label dashboards with the right caveats.
7. Train stakeholders on interpretation rules.

### Looker Studio data handoff
Use this workflow when GA4 powers external reporting layers.

1. Define which dimensions and metrics should come directly from GA4.
2. Decide which logic belongs in SQL or a semantic layer instead.
3. Standardize calculated fields and regex mappings.
4. Check performance and freshness constraints.
5. Build QA checks for recurring reports.
6. Document field definitions and caveats.
7. Support dashboard consumers with a stable schema.

### QA checklist
1. Property or stream scope stated.
2. Event and key-event logic validated.
3. Custom dimensions and metrics aligned to use cases.
4. Attribution setting and lookback window noted.
5. BigQuery logic validated against UI at a high level.
6. Consent or modeled data caveats included.
7. Google Ads linkage assessed if relevant.
8. Ecommerce event parameters checked if relevant.
9. Regex patterns documented when used.
10. UA comparison caveats included when requested.
11. Stakeholder summary differentiates data collection from interpretation.
12. Next actions include implementation owners where needed.

## Tools & Technologies
### Platforms, APIs, and working assets
- GA4 interface.
- GA4 DebugView and real-time reports.
- BigQuery export tables.
- Looker Studio.
- Google Ads linked products.
- Consent Mode v2 implementation patterns.
- GTM or equivalent tag management.
- Regex-based channel or content mappings.
- SQL for event analysis.
- Power BI or warehouse reporting layers.
- Audience and remarketing configuration.
- Explorations.
- Ecommerce schema references.
- Site search event documentation.
- Alerting and QA workflows.

### Working files and source systems
- Measurement plan.
- Event, parameter, and user-property specs.
- BigQuery datasets and schemas.
- Linked Google Ads configuration.
- Consent and CMP documentation.
- Custom definition inventory.
- Audience lists and use cases.
- Ecommerce item taxonomy.
- Dashboard field dictionaries.
- Migration notes from UA if relevant.

### BigQuery session reconstruction from GA4 export
`$Language
WITH base AS (
  SELECT
    event_date,
    user_pseudo_id,
    event_name,
    event_timestamp,
    (
      SELECT value.int_value
      FROM UNNEST(event_params)
      WHERE key = 'ga_session_id'
    ) AS ga_session_id,
    (
      SELECT value.string_value
      FROM UNNEST(event_params)
      WHERE key = 'page_location'
    ) AS page_location
  FROM `project.analytics_123456789.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20260701' AND '20260731'
),
sessionized AS (
  SELECT
    event_date,
    CONCAT(user_pseudo_id, '-', CAST(ga_session_id AS STRING)) AS session_key,
    MIN(event_timestamp) AS session_start_ts,
    COUNT(*) AS events,
    COUNTIF(event_name = 'purchase') AS purchases
  FROM base
  GROUP BY 1, 2
)
SELECT
  event_date,
  COUNT(*) AS sessions,
  SUM(purchases) AS purchases,
  SAFE_DIVIDE(SUM(purchases), COUNT(*)) AS purchase_rate
FROM sessionized
GROUP BY 1
ORDER BY 1
```

### GA4 ecommerce validation query
`$Language
SELECT
  event_name,
  COUNT(*) AS events,
  COUNTIF((
    SELECT value.string_value
    FROM UNNEST(event_params)
    WHERE key = 'currency'
  ) IS NULL) AS missing_currency,
  COUNTIF((
    SELECT value.double_value
    FROM UNNEST(event_params)
    WHERE key = 'value'
  ) IS NULL) AS missing_value
FROM `project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20260701' AND '20260731'
  AND event_name IN ('view_item', 'add_to_cart', 'begin_checkout', 'purchase')
GROUP BY 1
```

### Regex examples for GA4 classification
`$Language
^/blog/.*$              # blog content group
^(brand|tm)$            # brand search term shorthand
.*(summer|sale|promo).* # campaign content containing key promotion words
^(en|es|fr)-.*$         # locale-prefixed landing pages
```

## Output Formats
### Standard deliverables
- GA4 implementation audits.
- BigQuery SQL queries.
- Event taxonomy recommendations.
- Funnel and exploration frameworks.
- Audience and predictive use case notes.
- Consent Mode interpretation guidance.
- Google Ads linkage recommendations.
- Ecommerce validation checklists.
- Regex classification patterns.
- Dashboard handoff notes for Looker Studio or Power BI.
- Stakeholder summaries on GA4 versus UA changes.
- Action plans for analytics and media teams.

### Delivery template
```markdown
## Scope
- Property or stream
- Date range
- Business question

## Validation Summary
| Area | Status | Risk | Comment |
| --- | --- | --- | --- |

## Key Findings
1. Tracking insight
2. Behavior insight
3. Optimization implication

## Recommended Actions
1. Instrumentation
2. Reporting
3. Activation
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
