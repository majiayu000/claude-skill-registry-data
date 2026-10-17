---
name: path-to-conversion-analysis
description: Analyze the multi-touch path to conversion. Use when the user asks "path to conversion", "how many touchpoints to convert", "conversion path report", "assisted conversions", "time to conversion", "path length", "multi-touch report", "P2C report", "what are the top conversion paths", or "how long is the sales cycle". The cross-DSP hub for the concept; routes to the right report in each tool.
---

# Path to conversion analysis

Answer two questions a last-click number cannot: how many ad interactions it takes to convert, and what the most common sequences of those interactions look like. A conversion path is the ordered list of impressions and clicks a user saw before converting. From that path you read path length, time lag, the top paths, and how much credit upper-funnel media earns that last-click hides. This skill frames the concept so it carries to any DSP, then points you at the specific report that produces it today.

For what each metric means and the KPI math, see the `programmatic-foundations` skill. For attribution models, Floodlight setup, and lookback windows, see the `dv360-measurement-and-attribution` skill. For building and reading standard DV360 reports, see the `dv360-reporting` skill. For privacy-safe event-level path work in BigQuery, see the `dv360-advanced-analytics-adh` skill. For picking the report that matches a campaign goal, see the `reporting-by-campaign-goal` skill.

## When to use this skill

- "Path to conversion," "P2C report," "conversion path report," "multi-touch report."
- "How many touchpoints does it take to convert?" or "what is our average path length?"
- "What are our top conversion paths?" or "show me the most common sequences."
- "Assisted conversions," "assisted interactions," "what is upper funnel actually doing?"
- "Time to conversion," "days to conversion," "how long is the sales cycle?"
- "First touch vs last touch," "what initiates vs closes conversions?"

Boundary: this skill is about reading the multi-touch path. If the question is which attribution model to choose or how Floodlight counts a single conversion, that is `dv360-measurement-and-attribution`. If it is what a metric means in the abstract, that is `programmatic-foundations`. If it is a standard delivery or performance pull, that is `dv360-reporting`. The dedicated path report does not live in the DSP reporting surface; it lives in Campaign Manager 360, Google Analytics 4, or Ads Data Hub, and this skill sends you to the right one.

## Quick reference

Pick the tool by what the path question needs, not by where you happen to be reporting.

| Question | Tool | Why this one |
| --- | --- | --- |
| Full sequence of ad impressions and clicks before a Floodlight conversion | Campaign Manager 360 Path to Conversion report | The only Google report that lists the raw ordered ad exposures per conversion |
| Path length, days to conversion, and first/assist/close credit across attribution models, including non-ad channels | Google Analytics 4 conversion paths report | Models the path across paid and organic touchpoints with a model selector |
| Assists, view-through vs click-through paths, single vs multi-touch segments | Campaign Manager 360 attribution modeling segments | Slices conversion-path data into assisted, unassisted, and channel-position segments |
| De-duplicated cross-device paths and custom touchpoint credit, privacy-safe | Ads Data Hub | Event-level joins with privacy enforced on output, when aggregated reports cannot express it |
| Did a single conversion happen post-click or post-view, by line item | DSP conversion reporting (`dv360-reporting`) | Counts and attributes the conversion, but does not sequence the full path |

Rule of thumb: if you need the literal ordered list of ad exposures, start in Campaign Manager 360. If you need path length and time lag read against an attribution model and across non-ad channels, start in GA4. If you need de-duplicated cross-device paths or a credit model you define yourself, go to Ads Data Hub. The DSP tells you a conversion happened and whether it was post-click or post-view; it does not draw the path.

## The four measures and what each tells a trader

These are the readings you extract from any conversion-path report. The label changes by tool; the meaning does not. Definitions of the underlying terms live in `programmatic-foundations`.

- **Path length.** The number of touchpoints (ad interactions) before the conversion. It tells you how much support a conversion needs. A path length near 1 means conversions close on a single exposure, so tight frequency caps and lean upper-funnel spend are defensible. A long average path means conversions are built over many exposures, which justifies frequency headroom and upper-funnel investment. Read path length before you cut a frequency cap or zero out prospecting, because both decisions hinge on it.
- **Time lag (days or hours to conversion).** The elapsed time from the first exposure, or from the credited exposure, to the conversion. It reveals the real sales cycle. If most conversions land within a day, a short conversion window and fast optimization cycles fit. If they trail over weeks, a short lookback window is silently undercounting influence, and you should widen the window and slow your read so you are not judging a campaign before its conversions have matured. Set the conversion and lookback windows to the observed lag, not to a default.
- **Top conversion paths.** The most common ordered sequences, for example "Display impression, then Display impression, then Search click." They show how channels actually hand off to each other. Use them to spot the real role each line item plays: a tactic that rarely closes but constantly appears early is doing prospecting work, and the top-paths view is where that shows up.
- **Assisted conversions and first vs last touch.** An assist is a touchpoint that appeared on a converting path without being the final credited interaction. Assisted conversions quantify the upper-funnel and mid-funnel media that a last-click view writes off entirely. First-touch credit shows what initiates demand; last-touch shows what closes it. When a channel has a high assist count but low last-click conversions, last-click is underpricing it, and that is the single most common reason good prospecting gets cut by mistake.

## Core process

1. **State the path question in one sentence.** "What is our average path length and top three paths for the signup Floodlight, last 30 days?" fixes the conversion event, the grain, and the date range. A vague "show me the funnel" produces an unreadable table.
2. **Match the conversion event first.** Every path report keys off a conversion definition. In the Google stack that is a Floodlight activity (Campaign Manager 360, Ads Data Hub) or a key event (GA4). Confirm the same activity is in scope across tools, or the numbers will not reconcile. Floodlight setup lives in `dv360-measurement-and-attribution`.
3. **Pick the tool from the quick-reference table.** Ordered raw ad exposures go to the Campaign Manager 360 Path to Conversion report. Path length and time lag across models and channels go to the GA4 conversion paths report. De-duplicated cross-device or custom-credit paths go to Ads Data Hub.
4. **Set the conversion window to the observed lag, not a default.** If you do not yet know the lag, run the report once on a wide window, read the days-to-conversion distribution, then tighten. A window shorter than the real cycle truncates long paths and hides assists.
5. **Read length and lag together before you read the paths.** Length tells you how many touchpoints; lag tells you over how long. The top paths only make sense once you know whether a "3-touch" path closed in an hour or over three weeks.
6. **Translate into one media action.** Path length informs the frequency cap and upper-funnel budget. Time lag informs the conversion window and how long to let a campaign run before judging it. Assists inform whether a low-last-click tactic is actually pulling its weight. Every path read should end in one of those three decisions, or it was a vanity pull.

## Decision rules and thresholds

Path data is directional, so anchor decisions to your own baseline rather than to absolute numbers. The triggers below are starting points to set against that baseline.

- **Path length near 1 and lag under a day.** Conversions close on a single fast exposure. Defensible to tighten frequency and trim upper-funnel. Confirm the assist count is genuinely low first, because a low-funnel-only read can hide prospecting that the conversion event does not capture.
- **Path length materially above your baseline.** Conversions are built over many touchpoints. Give frequency headroom and protect upper-funnel budget. Cutting prospecting here will quietly starve the closers downstream.
- **Time lag tail beyond your lookback window.** Your window is undercounting. Widen the click and view windows toward the observed lag and stop reading conversions before they have had time to mature. Lookback-window mechanics are in `dv360-measurement-and-attribution`.
- **High assist count, low last-click conversions on a channel.** Last-click is underpricing it. Do not judge that channel on last-click conversions alone; move to a position-based or data-driven model, or to a custom credit model in Ads Data Hub, before reallocating budget away from it.
- **Top paths dominated by one repeated tactic.** Likely over-frequency on that tactic. Cross-check the average frequency in a reach read (`dv360-reporting`) and cap if the repeats are not adding incremental converters.
- **Path counts look thin or rows drop out in Ads Data Hub.** Privacy aggregation is filtering low-volume touchpoints. Widen the date range or coarsen the touchpoint grain rather than trusting a sparse result. Thresholds are in the reference file.

## Reference material

- `references/per-tool-setup.md`: read this when you need the exact setup for each report. Covers the Campaign Manager 360 Path to Conversion report (configuration, conversion window, interaction limits, pivot view, available path dimensions), the Campaign Manager 360 attribution segments (assisted, unassisted, view-through, channel-position), the GA4 conversion paths report (location, metrics, 20-touchpoint limit, early/mid/late touchpoints, model selector), and the Ads Data Hub touchpoint and Markov path approach with its privacy thresholds and touchpoint cap.

## Other platforms

This skill is the cross-DSP hub for the concept. The same four measures apply everywhere, but each platform produces them through its own surface, to be detailed in that platform's skill set:

- **The Trade Desk** has its own conversion and attribution reporting, including a conversion-touches view of how often a campaign, ad group, or creative touched a conversion. Details belong in the Trade Desk skill set.
- **Amazon DSP** reports its own attribution and path or assisted-conversion views, often alongside Amazon Marketing Cloud for event-level path analysis. Details belong in the Amazon DSP skill set.
- **Google Ads** has native attribution reporting with conversion-paths, path-metrics (average days and interactions to conversion), and assisted-conversions reports. Details belong in the Google Ads skill set.
- **StackAdapt** provides its own attribution and conversion-path reporting. Details belong in the StackAdapt skill set.

Keep the concept here; keep the click-path for each platform in its own skill so this hub does not drift.

## Common pitfalls

- **Reading a path report as a delivery report.** Path tools answer "how did conversions happen," not "how did the campaign deliver." Pull pacing and viewability from `dv360-reporting`, not from a P2C report.
- **Trusting a path length read on a window shorter than the lag.** A short conversion window truncates long paths and erases assists, making every conversion look like a one-touch close. Set the window to the observed days-to-conversion first.
- **Treating assists as conversions.** An assist is influence, not an additional conversion. Counting assists as incremental conversions double-counts. Use them to value a channel, not to inflate the total.
- **Reconciling path counts across tools that key off different events.** A Campaign Manager 360 Floodlight, a GA4 key event, and an Ads Data Hub query can each define the conversion differently. Align the event before comparing, or accept the numbers will differ.
- **Citing the deprecated Ads Data Hub paths tables.** The older CM360 and DV360 paths tables were retired. Use the current touchpoint and Markov path approach in `dv360-advanced-analytics-adh` instead.
- **Assuming the DSP draws the path.** DSP reporting attributes a conversion and labels it post-click or post-view, but it does not sequence the full multi-touch path. For the sequence, go to Campaign Manager 360, GA4, or Ads Data Hub.

## Sources

- Path to Conversion reports, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823644 (as of June 2026)
- Segment conversion path data, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823657 (as of June 2026)
- Conversion paths (key event attribution paths) report, Google Analytics 4 Help: https://support.google.com/analytics/answer/10595568 (as of June 2026)
- Ads Data Hub introduction, Google for Developers: https://developers.google.com/ads-data-hub/guides/intro (as of June 2026)
- Markov chain analysis, Ads Data Hub, Google for Developers: https://developers.google.com/ads-data-hub/guides/markov (as of June 2026)
- Conversion counting for line items, Display & Video 360 Help: https://support.google.com/displayvideo/answer/2997485 (as of June 2026)
- About Floodlight and Floodlight activities, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3027419 (as of June 2026)
- About attribution reports, Google Ads Help: https://support.google.com/google-ads/answer/1722023 (as of June 2026)
