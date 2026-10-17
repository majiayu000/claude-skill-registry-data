---
name: dv360-measurement-and-attribution
description: Measure outcomes and assign credit in Display & Video 360. Use when the user asks about Floodlight, conversion tracking, attribution models, view-through vs click-through, lookback windows, Brand Lift, reach and frequency, unique reach, de-duplicated or cross-media reach, or which measurement method to use.
---

# DV360 measurement and attribution

Decide how a conversion is counted, how credit is assigned across touchpoints, and which lift or reach study answers the brand question. This skill covers Floodlight, attribution models, Brand Lift, and reach and frequency methodology, plus when to reach for each. For metric definitions and KPI math, see the `programmatic-foundations` skill. For building and reading the actual reports, see the `dv360-reporting` skill. For event-level analysis in BigQuery or Ads Data Hub, see the `dv360-advanced-analytics-adh` skill.

## When to use this skill

- "Set up Floodlight" or "is this conversion counting right?"
- "Which attribution model should I use?" or "last click vs data-driven."
- "View-through vs click-through, what is the difference?"
- "What lookback window should I set?"
- "Run a Brand Lift study" or "did the campaign move awareness?"
- "Reach and frequency," "unique reach," "de-duplicate across channels," "co-viewing on CTV."

Boundary: if the question is which report to pull or how to add a metric, that is `dv360-reporting`. If it is what a term means in the abstract, that is `programmatic-foundations`. Floodlight tags and attribution models are defined in Campaign Manager 360 and shared across DV360 and Search Ads 360; configuration steps that live in CM360 are noted as such here.

## Quick reference

| Question | Method | Notes |
| --- | --- | --- |
| Did a user convert after seeing or clicking? | Floodlight | Counter or sales activity, defined in CM360, shared to DV360 and SA360 |
| How is credit split across touchpoints? | Attribution model | Last interaction by default; data-driven only when Floodlight is in CM360 |
| Did the campaign change perception? | Brand Lift survey | Survey-based lift in Association and Video ad recall |
| How many distinct people, how often? | Reach and frequency | Modeled, deduplicated across devices; do not sum |
| Combined reach across digital and TV? | Cross-Media Reach | Deduplicated across channels with third-party TV data |

Rule of thumb: lower-funnel goals (sales, signups, ROAS) are a Floodlight plus attribution question. Upper-funnel goals (awareness, recall) are a Brand Lift question. Frequency management and incremental audience are a reach question. Match the method to the funnel stage, not to whatever data is easiest to pull.

## Floodlight

Floodlight is the conversion-tracking layer. You place tags on the advertiser site, and Floodlight records actions after a user sees or clicks an ad. Activities are defined in Campaign Manager 360 and shared across DV360 and Search Ads 360, so one definition feeds every platform and avoids double instrumentation.

- **Activity types.** A counter activity records non-monetary actions (page views, signups) and counts how many times users reach a page after an impression or click. A sales activity records monetary actions and tracks items purchased and total value. Choose sales when you need revenue and ROAS; counter otherwise.
- **Counting methods.** Counter activities count Standard (every conversion), Unique (first conversion per user per 24-hour day), or Per session. Sales activities count transactions or items sold and can record more than one conversion per event (for example, quantity of items). Pick the method that matches the business event so you do not over- or under-count.
- **Post-click and post-view.** Floodlight records both. It treats a click as more significant than an impression, so to avoid double counting it credits a conversion as click-through if the user clicked within the click window, even when an impression also qualifies. Report post-click and post-view separately; collapsing them overstates view-through credit.
- **Tags and variables.** Activities emit tags (Google tag, image, or iframe); DV360 now supports the Google tag and recommends migrating to it. Custom Floodlight variables capture extra dimensions and metrics (order value, product category) for richer reporting. Define variables once in CM360 so they are consistent across platforms.
- **Conversions vs All Conversions.** Reporting shows "Conversions" (the activities you explicitly selected, which also feed bidding) and "All Conversions" (the raw count). Bid strategies optimize to the selected set, so be deliberate about which activities you include.

## Attribution

Attribution decides how conversion credit is split across the touchpoints that preceded it. Models are created on the Floodlight group, and the primary model is what reporting and bid optimization use.

- **Model types.** DV360 attribution follows the Floodlight activity's model. Historically the choices included last interaction (the default), first interaction, linear, time decay, and position-based, with data-driven available where Floodlight is managed in Campaign Manager 360 and volume is sufficient. Google has been retiring the rules-based models (first interaction, linear, time decay, position-based) across its ads stack in favor of data-driven and last interaction, the same shift documented in the `google-ads-conversion-tracking-and-attribution` skill, so confirm which models are currently selectable in CM360 and DV360 before relying on one. Prefer data-driven when you have the conversion volume and Floodlight is in CM360, because it allocates credit from observed paths rather than a fixed rule.
- **Click vs view lookback windows.** Set separate windows for click-through and view-through conversions. A click window is typically longer than a view window because a click is a stronger signal. Match the window to the real consideration cycle: a long window inflates view-through credit on incidental impressions; a short window undercounts genuine influence. Definitions of click-through and view-through live in `programmatic-foundations`.
- **Cross-channel attribution.** Floodlight already deduplicates conversions across DV360, SA360, and CM360 because they share the activity. For unified cross-channel modeling beyond Floodlight, use Campaign Manager 360 reporting or Ads Data Hub for path-level and privacy-safe analysis; see the `dv360-advanced-analytics-adh` skill.

## Brand Lift

Brand Lift measures whether ad exposure changed perception, by surveying an exposed group against an eligible but unexposed control group. Use it for upper-funnel goals where a conversion is not the outcome.

- **What it measures.** Choose up to 3 lift metrics from Association (the brand and message), Awareness, Consideration, Favorability, Purchase intent, and Video ad recall. Reported metrics include absolute brand lift, relative brand lift, lifted users, cost per lifted user, and the baseline response rate.
- **Response thresholds.** Accuracy scales with responses. Expect to detect lift around 2,000 responses per metric on high-performing line items and roughly 5,600 at the recommended budget minimum. Under-powered studies return no measurable lift, which is not the same as no effect.
- **Design tips.**
  - Do not over-narrow targeting. Tight targeting starves the survey of responses and slows or blocks measurement.
  - Preserve the control group. Do not separately retarget or exclude the holdout, or you contaminate the baseline and the lift is unreadable.
  - Set frequency for reach. Lift needs enough exposed users; very high frequency on a small audience trades the reach the study needs.
  - Match the survey language to the line item language. Serving the survey to users who do not speak it produces dismissals and noise.
  - Brand early in the creative. Recall and association rise when the brand appears in the first seconds, not only at the end.
  - Name the product, not just the brand, and check spelling so the study is not rejected.
- **Policy.** Brand Lift surveys must follow Google policies and cannot collect personally identifiable or sensitive information (demographics, sexual orientation, race, and similar are not allowed in the survey).

## Reach and frequency

Reach is the count of distinct people exposed; frequency is how often each saw the ad. DV360 models both with statistical methods that deduplicate across browsers and devices, so these numbers are not the sum of impressions or daily rows.

- **Unique reach.** Estimated unique users, with viewable unique reach, click reach, average impression frequency, and incremental reach. It is deduplicated across devices, so adding per-day or per-segment reach overcounts people.
- **Co-viewing for connected TV.** On CTV, more than one person can watch one impression. Co-viewed reach metrics account for multiple viewers per stream, so CTV reach is not undercounted as one person per impression.
- **Cross-media de-duplication.** Cross-Media Reach reporting combines digital (including CTV) and linear TV into one deduplicated view using third-party TV data, to show incremental reach TV and digital add to each other. Use it to plan and prove combined reach rather than reading channels in isolation.
- **Constraints.** Reach metrics run on windows of about 92 to 93 days or less, lag roughly 3 days, require Country, Gender, and Age dimensions, and are available only in certain countries. Building and reading these reports is covered in `dv360-reporting`.

## When to use which method

- Goal is sales, leads, or ROAS: instrument Floodlight (sales activity for revenue), pick an attribution model that matches your volume and Floodlight location, and read post-click and post-view separately. Pull it with a Floodlight report.
- Goal is awareness, consideration, or recall: run a Brand Lift study, protect the control group, and keep targeting broad enough to power the survey.
- Goal is managing exposure or proving incremental audience: use Reach reports for a single channel and Cross-Media Reach to deduplicate across digital and TV.
- Need path-level or privacy-safe cross-channel analysis beyond Floodlight: move to Ads Data Hub via the `dv360-advanced-analytics-adh` skill.

## Common pitfalls

- **Counting both post-click and post-view as one number.** They answer different questions and double-counting inflates view-through. Keep them separate.
- **Picking data-driven attribution without the prerequisites.** It is available as the primary model only when Floodlight is managed in CM360 and only with enough conversion volume. Otherwise use the default last-interaction model and confirm the currently available options.
- **Lookback windows that do not match the buying cycle.** Too long inflates view-through credit on incidental impressions; too short undercounts real influence. Set click and view windows deliberately.
- **Contaminating the Brand Lift control group.** Retargeting or excluding the holdout makes lift unreadable. Leave the control group alone.
- **Over-narrow Brand Lift targeting.** Starves responses, so the study returns no measurable lift. Keep the audience broad enough to clear the response threshold.
- **Summing unique reach.** Modeled, deduplicated reach is not additive across days or segments. Read it at the grain you need.

## Sources

- Create a Floodlight activity, Display & Video 360 Help: https://support.google.com/displayvideo/answer/2697097 (as of June 2026)
- About Floodlight and Floodlight activities, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3027419 (as of June 2026)
- The Floodlight activities tab, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823234 (as of June 2026)
- How Floodlight counts conversions, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823400 (as of June 2026)
- Create an attribution model and change your primary model, Display & Video 360 Help: https://support.google.com/displayvideo/answer/7409983 (as of June 2026)
- Set up Brand Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9570506 (as of June 2026)
- Brand Lift surveys (policy), Display & Video 360 Help: https://support.google.com/displayvideo/answer/9724628 (as of June 2026)
- Understand your Brand Lift measurement data, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9724932 (as of June 2026)
- Reach reports, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6170584 (as of June 2026)
- Cross-Media Reach reporting, Display & Video 360 Help: https://support.google.com/displayvideo/answer/13955444 (as of June 2026)
