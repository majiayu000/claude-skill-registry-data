---
name: amazon-marketing-cloud
description: Decide when to use Amazon Marketing Cloud and how to query it. Use when the user mentions Amazon Marketing Cloud, AMC, Amazon clean room, custom attribution on Amazon, AMC audiences, path or overlap analysis on Amazon, incrementality on Amazon, pseudonymized event-level Amazon Ads signals, or activating an AMC audience back into Amazon DSP. Covers the privacy model, aggregation thresholds, and when AMC beats standard reporting.
---

# Amazon Marketing Cloud

Answer the questions standard Amazon DSP reporting cannot: custom attribution you define, cross-media path and overlap analysis, audiences built from behavior and pushed back into the DSP, and incrementality measured from the event log itself. Amazon Marketing Cloud (AMC) is a privacy-safe clean room that holds event-level but pseudonymized Amazon Ads signals (impressions, clicks, and conversions across Amazon DSP and sponsored ads) plus your own pseudonymized inputs, and lets you query all of it with SQL. The defining constraint: you write SQL against user-level events but only get aggregated, privacy-checked output back, never a single user-level row.

AMC is built on AWS Clean Rooms. It is the Amazon analog of a privacy-safe data clean room for advertising: Amazon's signals and your first-party signals meet inside a dedicated instance, your query runs across them, and only an aggregate that clears the privacy checks is returned.

For Amazon DSP's standard reports and the retail-funnel metrics, see the `amazon-dsp-measurement-and-reporting` skill. For what each metric means and the KPI math, see the `programmatic-foundations` skill. For choosing a report shape by objective, see the `reporting-by-campaign-goal` skill. For the multi-touch path framework that AMC lets you compute on Amazon signals, see the `path-to-conversion-analysis` skill.

## When to use this skill

- "Analyze this in Amazon Marketing Cloud" or "write an AMC query."
- "Custom attribution on Amazon" or "build my own attribution model from the events."
- "Path analysis on Amazon," "which ad sequences led to purchase," "cross-media path."
- "Audience overlap on Amazon," "how much do DSP and sponsored ads overlap."
- "Incrementality on Amazon," "lift," "exposed vs unexposed purchase rate."
- "AMC audiences," "build an audience in AMC and activate it in Amazon DSP."
- "Why can I not see user-level rows on Amazon" or "what is the Amazon clean room."
- "Should I use AMC or standard Amazon DSP reporting for this?"

Boundary: if a standard Amazon DSP report answers it (delivery, the retail funnel, reach and frequency, ROAS, new-to-brand), stay in `amazon-dsp-measurement-and-reporting`. AMC is for analysis that needs event-level joins, a custom credit model, de-duplication across sources, overlap, or incrementality that aggregated reports cannot express. If the question is what a metric means in general, that is `programmatic-foundations`. If it is the path-to-conversion concept across platforms, frame it in `path-to-conversion-analysis` and compute it here.

## Quick reference

Decide first whether the question even needs event-level analysis. Most reporting questions do not.

| Need | Surface | Why |
| --- | --- | --- |
| Delivery, retail funnel, reach and frequency, ROAS, new-to-brand | Standard Amazon DSP reporting (`amazon-dsp-measurement-and-reporting`) | The report already answers it. Do not pay the AMC tax. |
| Custom attribution model defined by you, from impression, click, and conversion events | Amazon Marketing Cloud | Standard reports ship a fixed last-touch model. AMC lets you write the credit logic in SQL. |
| Cross-media path and the overlap between Amazon DSP, sponsored ads, and other signals | Amazon Marketing Cloud | Needs event-level joins on a user key across sources, de-duplicated, then aggregated. |
| De-duplicated reach across campaigns or media, frequency analysis beyond a single report | Amazon Marketing Cloud | Reach must be counted from events on a user key, not summed from report rows. |
| Incrementality: exposed vs unexposed (or control) outcomes | Amazon Marketing Cloud | Needs the event log and a comparison group, with privacy enforced on output. |
| An audience defined by behavior across signals, then activated for buying | Amazon Marketing Cloud audiences | Build from engagement and conversion events over a long lookback, then push to Amazon DSP. |

Default position: try a standard Amazon DSP report first. Reach for AMC only when the question needs event-level joins, custom logic, de-duplication, overlap, or incrementality. The price of AMC is SQL, latency, and designing around privacy checks, so do not pay it for a question a report already answers.

## What AMC is and is not

AMC lets you query pseudonymized, event-level Amazon Ads signals joined to your own pseudonymized inputs, inside a dedicated clean-room instance, and returns only aggregated results. Two facts shape every AMC design decision.

- **You write SQL over user-level events but receive aggregates.** You can join ad-exposure events to a conversion or first-party table on a pseudonymous user key to compute, for example, purchase rate by exposure pattern, but you receive the group-level aggregate, never the per-user rows. Inputs must be pseudonymized; the instance does not accept raw personal identifiers, and your uploaded inputs stay inside your instance and are not exported to or accessed by Amazon.
- **The privacy checks decide whether a query returns anything.** A query that is logically correct still returns nothing if a group is too small to clear the aggregation threshold. Designing for the checks is part of writing the query, not an afterthought.

What AMC is not: it is not a way to extract user-level Amazon data, not a real-time reporting surface, and not a replacement for standard reporting on questions standard reporting already answers. There is also a self-service experience that surfaces prebuilt analyses with little or no SQL, but the custom work in this skill (bespoke attribution, overlap, incrementality) is the SQL clean room.

## Use cases that standard reporting cannot do

Route these to AMC, because each needs event-level data or a join that aggregated Amazon DSP reports cannot produce:

- **Custom attribution.** Build a position-based, time-decay, or bespoke-rule model directly from the impression, click, and conversion events, instead of accepting the standard last-touch model. This is the single most common reason to use AMC.
- **Cross-media and cross-tactic path.** Sequence the ordered Amazon DSP and sponsored-ads exposures that preceded a purchase, then read path length, common sequences, and which tactic initiates versus closes. The path concept lives in `path-to-conversion-analysis`; AMC is where you compute it on Amazon signals.
- **Audience overlap.** Measure how much two audiences, two campaigns, or two tactics (for example Amazon DSP and sponsored ads) overlap in the people they reached, to find redundant targeting or net-new reach.
- **De-duplicated reach and frequency.** Count distinct people across campaigns or media on a user key and analyze true frequency, which summing report rows overcounts.
- **Incrementality and lift.** Compare exposed and unexposed (or held-out control) groups to estimate the incremental purchases, sales, or new-to-brand customers a campaign drove beyond what last-touch credits.
- **Segment outcomes with first-party data.** Join your pseudonymized CRM or value data to Amazon ad exposure and report purchase rate, sales, or ROAS by your own segments, returned as aggregates.

If a request is none of these and a standard report covers it, use the report.

## AMC audiences and activation

AMC is not only analysis; it is an audience-building engine. You define an audience in SQL from engagement records, conversion events, and segment information across the available signals, over a multi-year lookback that standard audience tools do not reach. Then you activate that audience for buying. Audiences created in AMC can be pushed to Amazon DSP (and to eligible sponsored-ads and video placements) and used as a targeting or suppression segment.

The value is precision the standard audience picker cannot express: "people who viewed the detail page twice but did not purchase in 90 days," or "purchasers of product A who have not seen the product B campaign." Build the logic once in the clean room, activate it in the DSP, and the same privacy model that governs analysis governs the audience: it is built from pseudonymized events and respects a minimum-size floor before it can be activated.

## The privacy model

AMC enforces privacy on the output, not the input. Design every query and every audience expecting these gates.

- **Aggregation threshold (minimum users per row).** Each returned row must aggregate over at least a minimum number of distinct users, or the row is dropped. Rows below the floor do not return, which is the usual reason a logically correct query yields nothing. Treat the exact number as a value to confirm against the current AMC documentation rather than a fixed constant, and design groups coarse enough to clear it comfortably.
- **Audience minimum size.** An audience must contain at least a minimum number of users before it can be activated, for the same reason: a tiny audience could expose individuals. Build audiences broad enough to clear the floor.
- **Pseudonymized inputs only.** AMC accepts only pseudonymized inputs and never returns user-level rows. Your uploaded inputs stay in your instance and cannot be exported or read by Amazon.
- **Output checks on small or unusual results.** The clean room is designed so that no single user can be isolated by differencing or by a result that is too granular. Expect very small groups, single-day slices on thin data, and over-narrow filters to be suppressed.

The practical consequence: write queries and define audiences that produce groups comfortably above the minimum-users floor, avoid tiny segments and single-user logic, and settle the query logic before you run the real cut.

## Core process

1. **State the question as one measurable statement.** "What is the incremental purchase rate of the Amazon DSP awareness line versus an unexposed group, last quarter?" names the metric, the comparison, and the window. A vague question produces a query that fails the checks or answers nothing.
2. **Confirm it actually needs AMC.** If a standard Amazon DSP report answers it, stop and use `amazon-dsp-measurement-and-reporting`. Continue only when the question needs event-level joins, custom credit logic, overlap, de-duplication, or incrementality.
3. **Identify the signals and the join key.** Decide which event tables you need (Amazon DSP exposures, sponsored-ads exposures, conversions) and which first-party input you are joining, on what pseudonymous user key. The key determines what de-duplication and segmentation are possible.
4. **Write the SQL to aggregate above the privacy floor.** Group to a grain coarse enough to clear the minimum-users-per-row threshold. Avoid tiny segments and thin single-day slices that fragment users into sub-threshold groups.
5. **Run it and read the privacy result, not just the numbers.** Missing rows usually mean the aggregation threshold, not a logic bug. Widen the grouping or the window rather than re-running the same narrow cut.
6. **Tie the output to a decision.** A custom-attribution result changes budget weighting; an overlap result changes targeting or suppression; an incrementality result validates or kills a tactic; an audience gets activated in Amazon DSP. The aggregate is the means, not the deliverable.

## Decision rules and thresholds

- **Standard report first, AMC second.** AMC costs SQL, latency, and privacy design. Spend it only on event-level questions a report cannot answer.
- **Design for the aggregation floor from the start.** Group coarse, avoid tiny segments, and confirm the current minimum-users value in the AMC documentation rather than assuming a number.
- **Custom attribution is the headline use case.** When a stakeholder distrusts the standard last-touch model, AMC is the answer: build the model from the events and show the credit shift.
- **Use overlap to cut waste.** High overlap between Amazon DSP and sponsored ads on the same buyers signals redundant spend or a suppression opportunity.
- **Incrementality needs a clean comparison group.** A lift read is only as good as the unexposed or control definition. Decide the comparison before writing the query.
- **Audiences must clear the activation minimum.** A behaviorally precise audience that is too small will not activate. Broaden the definition until it clears the floor.

## Templates and examples

Custom attribution, framed as a question to a query:

> "Across all purchasers last month, credit each purchase with a position-based model (40 percent first touch, 40 percent last touch, 20 percent middle) over Amazon DSP and sponsored-ads exposures, and compare the resulting channel credit to the standard last-touch report." Output: channel-level credit shares, aggregated. Decision: reweight budget if upper-funnel earns materially more credit than last-touch shows.

Overlap, framed for a suppression decision:

> "How many users were reached by both the Amazon DSP prospecting line and the sponsored-products campaign in the last 30 days, and what share of each tactic's reach is the overlap?" Output: overlap count and percentages, aggregated above the floor. Decision: suppress the overlap from prospecting to stop paying twice.

Audience, built for activation:

> "Build an audience of users who viewed the detail page for ASIN X at least twice but did not purchase within 60 days, over a 12-month lookback, with at least the minimum activation size." Activate in Amazon DSP as a retargeting segment. The same privacy floor that governs analysis governs the audience.

## Common pitfalls

- **Reaching for AMC when a report would do.** AMC adds SQL, latency, and privacy constraints. If a standard Amazon DSP report answers it, use the report.
- **Designing a query that cannot clear the aggregation threshold.** Slicing to tiny segments or single users returns nothing. Aggregate above the minimum-users floor from the start.
- **Expecting user-level rows.** The clean room never returns them. If the analysis requires per-user output, AMC is the wrong tool and the requirement is the problem.
- **Summing reach instead of de-duplicating.** The point of AMC reach and overlap work is de-duplication on a user key. Adding reach across rows or sources overcounts people.
- **Treating the self-service prebuilt analyses as the custom clean room.** The low-SQL experience answers common questions; bespoke attribution, overlap, and incrementality are the SQL clean room. Know which one the question needs.
- **Assuming a fixed privacy threshold.** The minimum-users and audience-size floors are configured by Amazon and change. Confirm current values in the AMC documentation before relying on a number.
- **Ignoring latency on a time-sensitive read.** AMC data lands with a lag. A question that needs today's numbers belongs in standard Amazon DSP reporting, not AMC.

## Sources

- Amazon Marketing Cloud product overview, Amazon Ads (clean room, pseudonymized signals, audiences, privacy): https://advertising.amazon.com/solutions/products/amazon-marketing-cloud (as of June 2026)
- Amazon Marketing Cloud APIs are now part of the Amazon Ads API, Amazon Ads (reporting, audiences, signal management): https://advertising.amazon.com/resources/whats-new/amc-api-available-on-amazon-ads-api (as of June 2026)
- Amazon Marketing Cloud documentation overview, Amazon Ads advanced tools: https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-cloud/overview (as of June 2026)
- AMC on AWS Clean Rooms, Amazon Ads advanced tools documentation: https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-cloud/acr/1_overview (as of June 2026)
- Plan your advertising campaigns with Amazon Marketing Cloud on AWS Clean Rooms (now generally available), AWS News Blog: https://aws.amazon.com/blogs/aws/plan-your-advertising-campaigns-with-amazon-marketing-cloud-on-aws-clean-rooms-now-generally-available/ (as of June 2026)
- Amazon Ads advanced tools documentation code samples and AMC playbooks (official repository), amzn/ads-advanced-tools-docs: https://github.com/amzn/ads-advanced-tools-docs (as of June 2026)

Note on sources: the AMC advanced-tools documentation (advertising.amazon.com/API/docs) renders client-side and cannot be machine-verified line by line, and the exact aggregation threshold (minimum users per row) and audience-minimum values are not stated on a stable public page and do change. This skill states those thresholds and the privacy mechanics as general AMC practice and points to the AMC documentation and the official code-samples repository above; confirm the current minimum-users and audience-size values in the live AMC documentation before relying on a specific number.
