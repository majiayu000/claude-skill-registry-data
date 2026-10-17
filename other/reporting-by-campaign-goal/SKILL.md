---
name: reporting-by-campaign-goal
description: Build the right report for a campaign objective and read it like an expert. DSP-agnostic framework for what a great report looks like per goal. Use when the user asks "what report for an awareness campaign", "best report for conversions", "how do I measure a brand campaign", "reporting for my campaign goal", "state of the art report", "which KPIs for [objective]", "how should I report this campaign", "what does good look like for [goal]", or "am I reading this report right". Pairs with the platform reporting skill for build mechanics.
---

# Reporting by campaign goal

Start from the objective, not the metric menu. A report is good when it answers the one question the campaign goal asks, slices that answer the way an expert would, and is hard to misread. This skill is the goal-to-report framework: for each objective it names the primary KPI set, the report type that surfaces it, the dimensions to slice by, the quality bar a strong report clears, and the misread that sinks a weak one. It is DSP-agnostic on purpose. The mechanics of clicking a report together in a given tool stay in the platform reporting skill (for example `dv360-reporting`); this skill decides what to build and how to read it.

For what each metric means and the KPI math, see the `programmatic-foundations` skill. For building and scheduling the actual reports, see the `dv360-reporting` skill. For attribution models, Floodlight, Brand Lift, and reach methodology, see the `dv360-measurement-and-attribution` skill. For the multi-touch path to conversion, see the `path-to-conversion-analysis` skill. For privacy-safe, event-level, and lifetime-value analysis, see the `dv360-advanced-analytics-adh` skill.

## When to use this skill

- "What report should I pull for an awareness / brand campaign?"
- "Best report for conversions" or "how do I report a performance campaign?"
- "How do I measure a brand campaign?" or "did awareness actually move?"
- "Reporting for my campaign goal" or "which KPIs matter for [objective]?"
- "What does a state of the art report look like for this?"
- "Am I reading this report correctly?" or "what is the common misread here?"
- Planning a reach and frequency buy, or a combined pacing-plus-performance view.

Boundary: if the question is what a metric means or how to compute it, that is `programmatic-foundations`. If it is which report type exists in the platform, how to add a metric or dimension, or how to schedule a pull, that is `dv360-reporting`. If it is which attribution model to choose or how a conversion is counted, that is `dv360-measurement-and-attribution`. If it is the ordered sequence of touchpoints before a conversion, that is `path-to-conversion-analysis`. This skill sits above all of them: it picks the goal-appropriate report and tells you when to hand off.

## Quick reference

Match the objective to its report shape first. Full recipe tables, with every KPI, dimension, quality bar, and misread, are in `references/goal-report-recipes.md`.

| Objective | Primary KPIs | Report type that surfaces it | Slice by |
| --- | --- | --- | --- |
| Awareness / brand | Unique reach, on-target reach and percentage, frequency distribution, viewability rate, VCR, Brand Lift | Reach report, Cross-Media or unique reach, Brand Lift study | Audience, frequency bucket, device, geo, creative |
| Consideration / engagement | CTR, engagement rate, qualified site visits, video views and view rate, Search Lift | Standard with engagement and video metrics, site analytics, Search Lift study | Creative, placement, audience, device |
| Performance / conversion | Conversions, CPA, ROAS, CVR, conversion lag, attribution-model comparison, incremental conversions | Conversion report, attribution-model comparison, Conversion Lift study | Line item, creative, audience, device, conversion type |
| Retention / loyalty | Repeat conversion rate, returning-user cohorts, lifetime-value proxies | Cohort exploration, user-lifetime analysis, segment-level analysis (often outside the DSP) | Cohort by acquisition date, audience segment, new vs returning |
| Reach and frequency planning | Forecast reach curve, frequency at saturation, on-target percentage | Planning and forecast tools, reach curve | Frequency cap scenario, audience, channel mix |
| Pacing plus performance | Pace vs flight, plus the goal KPI in the same view | Delivery report joined to the goal KPI | Date, line item, plus the goal dimension |

Rule of thumb: upper-funnel goals are reach and lift questions, lower-funnel goals are conversion and incrementality questions, and retention is a cohort and lifetime-value question that usually needs site analytics or event-level data, not the DSP alone. Match the report to the funnel stage, never to whatever data is easiest to pull. The funnel-to-KPI map lives in `programmatic-foundations`.

## Core process

1. **State the objective as one decision sentence.** "Did the brand campaign reach 60 percent of women 25 to 54 at a frequency of 3 to 5, last flight?" fixes the goal, the audience, the KPI, the target, and the window. A goal stated this tightly tells you the report type, the dimensions, and the benchmark in one line. "Show me how the campaign did" does not, and produces a wide table no one reads.
2. **Name the primary KPI set from the objective, not from the column list.** Each stage has a small set of metrics that answer it and a larger set that are guardrails or diagnostics. Awareness is reach, frequency, and lift, with viewability as a guardrail. Conversion is CPA, ROAS, and CVR, with CTR as a weak diagnostic, not the goal. Pick the primary set first so the report stays legible.
3. **Pick the report type that actually surfaces those KPIs.** Reach is modeled and deduplicated, so it needs a Reach report, not a sum of daily rows. A perception shift needs a Brand Lift study, not a proxy. Incrementality needs a controlled Conversion Lift experiment, not a last-click conversion column. Choosing the type from the KPI prevents building a standard delivery report that structurally cannot answer the question.
4. **Add only the dimensions the question needs, in the order an expert would read them.** Every extra dimension splits the data into more rows and can change how a metric aggregates (reach does not add up across an added split). Start at the coarsest grain that could answer the question. Add a dimension only to explain a number you already see, for example breaking conversions by creative once the line-item CPA looks off.
5. **Set the benchmark before you read the number.** A 0.40 percent CTR, a 2.1 average frequency, a 4.2x ROAS are good or bad only against the plan target and the format benchmark. Write the target next to each KPI so the read is a comparison, not a vibe. If there is no target, the first deliverable is to set one, not to report a naked number.
6. **Read against the goal, then end in one action or finding.** Compare each primary KPI to its target, check the guardrails did not break (reach bought at the cost of viewability, conversions bought at the cost of incrementality), and close with the single decision the report informs. A report that does not change a budget, a cap, a creative, or a target was a vanity pull.

## The five reading lenses for a state of the art report

These are the marks of an expert read, regardless of objective or platform. The full version of each, with the failure it prevents, is in `references/sota-reporting-practices.md`.

- **Deduplicated cross-channel reach, not summed reach.** People reached across channels and devices is a modeled, deduplicated number. Adding reach across line items, days, channels, or segments overcounts people. When the goal is reach, read it at the grain you need from a reach surface, and use Cross-Media Reach to combine digital and TV. Never sum it yourself.
- **On-target percentage, not just gross reach.** Gross reach counts everyone the ad touched. On-target reach counts the people who actually match the target demographic, and on-target percentage is that over the target population. A campaign can post huge gross reach while wasting half of it off-target. Report on-target percentage so reach is judged against the audience that was bought, not the audience that happened to be cheap.
- **Incrementality and lift over last-click.** Last-click counts conversions that touched the ad last, including ones that would have happened anyway. Incrementality, measured by a controlled experiment (Conversion Lift, holdout, or an event-level lift analysis), counts conversions the ad actually caused. When budget decisions are at stake, lead with incremental conversions and treat last-click as a directional diagnostic, not truth.
- **Attention as an emerging signal next to viewability.** Viewability says the ad had the opportunity to be seen. Attention estimates whether it was actually noticed and to what depth. The IAB and MRC have published a framework for measuring it, and it is becoming a complementary signal to viewability, not a replacement. Where attention data is available, read it alongside viewability and outcomes; do not treat a high viewability rate as proof of attention.
- **Blended ROAS read next to platform ROAS, with MMM and MTA in their place.** Platform ROAS is what one DSP claims for itself, and every platform claims the same conversion. Blended ROAS is total revenue over total spend across all channels, which double-counts nothing but attributes nothing either. Read both: platform ROAS to optimize within a channel, blended ROAS to sanity-check the whole. Multi-touch attribution (MTA) is for tactical, in-channel credit; marketing mix modeling (MMM) is for cross-channel budget allocation including offline; incrementality experiments are the ground truth that calibrates both. Triangulate, do not crown one.

## Decision rules and thresholds

- **Reach goal: read frequency distribution, not just average frequency.** An average frequency of 4 can hide a tail of users seeing the ad 30 times while half the audience saw it once. Pull the frequency distribution (reach by frequency bucket) and check effective frequency, the band (commonly around 3 to 10 exposures, set by brand and creative) where the message lands before it wastes. Effective frequency is a planning judgment, not a single documented constant; set it per brand and creative. The cap mechanics live in `dv360-frequency-and-brand-safety`.
- **Awareness goal: pair delivery proof with perception proof.** Reach, frequency, viewability, and VCR prove the ad was delivered to people and seen. They do not prove it changed anyone. For a true awareness read, run a Brand Lift study against an unexposed control so you can report lifted users and absolute and relative lift, not just impressions served. Study design and response thresholds live in `dv360-measurement-and-attribution`.
- **Consideration goal: count qualified visits, not raw clicks.** CTR measures interest in the ad, not interest in the brand. A high CTR with a high bounce rate is a creative that overpromised. Tie the click to a qualified site visit or engagement event in site analytics, and where the goal is search intent, run a Search Lift study to measure the rise in branded search the campaign caused.
- **Conversion goal: read CPA and ROAS against the plan, and post-click separate from post-view.** Compare CPA and ROAS to the media-plan target, never across line items on different goals. Keep post-click and post-view conversions in separate columns, because collapsing them overstates view-through credit. Check conversion lag before judging a fresh campaign, because a long lag means conversions are still maturing. Counting and attribution rules live in `dv360-measurement-and-attribution`.
- **Conversion goal: compare attribution models before reallocating.** Run the same conversions through last-click and through a data-driven model side by side. If a line item looks weak on last-click but strong under data-driven, last-click is underpricing the upper-funnel work it does. Move budget on the model that reflects the real path, not the one that flatters the closer. The path view is in `path-to-conversion-analysis`.
- **Retention goal: use cohorts and lifetime value, and expect to leave the DSP.** Repeat conversion rate and returning-user retention are cohort questions keyed to an acquisition date, and lifetime-value proxies need user-lifetime or event-level data. The DSP reports media delivery, not customer lifetime, so these usually live in site analytics (cohort and user-lifetime explorations) or in event-level analysis joined to first-party value. Route lifetime and segment-value work to `dv360-advanced-analytics-adh`.
- **Any goal: if the report cannot fail, it cannot inform.** A report with no target, no control, and no comparison can only confirm. Build in the benchmark, the prior period, or the holdout so a bad result can actually show up. A dashboard that always looks fine is not measuring anything.

## Reference material

- `references/goal-report-recipes.md`: the full per-goal recipe. For each objective (awareness, consideration, performance, retention, reach and frequency planning, pacing plus performance) it gives the primary KPI set, the report type, the dimensions to slice by, the state of the art quality bar, and the common misread, as scannable tables. Read this when you need the complete recipe for a specific goal rather than the summary.
- `references/sota-reporting-practices.md`: the cross-cutting best practices in depth. Deduplicated cross-channel reach, on-target percentage, incrementality and lift over last-click, attention as an emerging signal, blended versus platform ROAS, and where MMM and MTA fit. Read this when you need to justify or explain a practice, or to audit an existing report against the bar.

## Templates and examples

Worked objective sentences and the report each one implies:

- **Brand launch.** "Reach 50 percent of adults 18 to 34 at an effective frequency of 3 to 5 over the 6-week flight, with viewability above 70 percent, and prove a lift in ad recall." Report: a Reach report sliced by audience and frequency bucket for delivery, viewability and VCR as guardrails, and a Brand Lift study with Ad recall and Awareness as the lift metrics. Misread to avoid: declaring success on impressions and viewability alone, with no lift study, so perception change is assumed, not measured.
- **Direct-response retargeting.** "Drive purchases at a CPA under 25 dollars and a ROAS above 4x last month, and confirm the conversions are incremental." Report: a conversion report by line item and creative with CPA, ROAS, CVR, and conversion lag, post-click and post-view split, plus a last-click versus data-driven comparison, and a Conversion Lift experiment for the incrementality read. Misread to avoid: reporting platform ROAS as the whole truth and never testing whether the retargeting converted people who would have bought anyway.
- **Always-on consideration.** "Grow qualified site visits and branded search at a cost per qualified visit under 2 dollars this quarter." Report: a standard report with CTR, view rate, and engagement by creative and audience, joined to qualified-visit and engagement events in site analytics, plus a Search Lift study for the branded-search rise. Misread to avoid: optimizing to CTR, which rewards clickbait creative that bounces, instead of to qualified visits.
- **Loyalty and retention.** "Lift the 30-day repeat purchase rate of customers acquired in Q1 and grow their lifetime value." Report: a cohort exploration keyed to Q1 acquisition with returning-user retention and repeat conversion rate, plus a user-lifetime analysis for the value proxy, run in site analytics or event-level analysis rather than the DSP. Misread to avoid: trying to read retention from DSP delivery reporting, which has no concept of a returning customer.

## Common pitfalls

- **Judging a stage by the wrong KPI.** CPA on an awareness buy, or reach on a conversion buy. Anchor every metric to the objective. The funnel-to-KPI map is in `programmatic-foundations`.
- **Summing modeled reach.** Reach is deduplicated and not additive across days, segments, channels, or line items. Read it at the grain you need from a reach surface.
- **Reading average frequency without the distribution.** The average hides the over-exposed tail. Pull reach by frequency bucket and read effective frequency.
- **Treating viewability as attention or as success.** Viewability is opportunity to see, not proof of being seen or of impact. Pair it with attention where available and with a lift study for awareness goals.
- **Leading with last-click for a budget decision.** Last-click credits conversions that would have happened anyway. Lead with incrementality and use last-click as a diagnostic.
- **Reporting platform ROAS as the truth across channels.** Every platform claims the same conversion. Read blended ROAS alongside, and use MMM and incrementality for cross-channel allocation.
- **Collapsing post-click and post-view.** They answer different questions and collapsing them overstates view-through. Keep them separate.
- **Expecting the DSP to report retention.** Cohorts, returning users, and lifetime value live in site analytics or event-level analysis, not in DSP delivery reporting. Route them to `dv360-advanced-analytics-adh`.
- **Building a report that cannot fail.** No target, no control, no comparison means the report can only confirm. Add the benchmark, the prior period, or the holdout.

## Sources

- Reach reports, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6170584 (as of June 2026)
- Cross-Media Reach reporting, Display & Video 360 Help: https://support.google.com/displayvideo/answer/13955444 (as of June 2026)
- On-target reach, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9545617 (as of June 2026)
- Set up Brand Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9570506 (as of June 2026)
- Set up Search Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/15001171 (as of June 2026)
- Set up Conversion Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/16804790 (as of June 2026)
- Report on video campaigns, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3521206 (as of June 2026)
- Report on YouTube and partners line items, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6274610 (as of June 2026)
- About Active View, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3214556 (as of June 2026)
- Metrics in reports, Display & Video 360 Help: https://support.google.com/displayvideo/table/3187025 (as of June 2026)
- Conversion paths (key event attribution paths) report, Google Analytics 4 Help: https://support.google.com/analytics/answer/10595568 (as of June 2026)
- Key event attribution models report, Google Analytics 4 Help: https://support.google.com/analytics/answer/10596865 (as of June 2026)
- Get started with attribution, Google Analytics 4 Help: https://support.google.com/analytics/answer/10596866 (as of June 2026)
- User lifetime exploration, Google Analytics 4 Help: https://support.google.com/analytics/answer/9947257 (as of June 2026)
- Cohort exploration, Google Analytics 4 Help: https://support.google.com/analytics/answer/9670133 (as of June 2026)
- Attention Measurement framework (IAB and MRC), Interactive Advertising Bureau: https://www.iab.com/guidelines/attention/ (as of June 2026)
