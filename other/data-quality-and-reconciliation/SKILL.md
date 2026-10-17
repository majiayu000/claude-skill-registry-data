---
name: data-quality-and-reconciliation
description: Reconcile conversion and delivery numbers across tools, set acceptable discrepancy bands, gate a report on a data-quality check before it reaches a client, and run a real anomaly-detection method that accounts for weekday and seasonality. Use when the user asks about data quality, "reconcile conversions", "the numbers do not match across tools", "DSP vs GA4 vs Campaign Manager", "anomaly detection method", "is this a real change or a tracking break", "discrepancy band", "acceptable variance between platforms", "why are conversions different", "freshness check", "null check", or "the report looks wrong".
---

# Data quality and reconciliation

Two numbers for the same thing rarely match across a DSP, Campaign Manager 360, and GA4, and most of the gap is legitimate, not a bug. This skill does three jobs: explain why measurement tools disagree and set the band where a difference is expected rather than broken, gate a report with a pre-ship data-quality check so a freshness gap or a null column never reaches a client, and replace flat-tolerance alerting with an anomaly-detection method that knows the difference between a Tuesday, a holiday, and a tracking break. It is the method layer under the `anomaly-detection` loop, which scans daily but needs a real statistical band to scan against.

For what each metric means and the KPI math, see the `programmatic-foundations` skill. For pulling the report whose numbers you are reconciling, see the `dv360-reporting` skill. For deciding which report a goal needs and how to read it, see the `reporting-by-campaign-goal` skill. For whether a difference is a real lift rather than noise in a controlled test, see the `incrementality-and-experimentation` skill.

## When to use this skill

- "The DSP, Campaign Manager, and GA4 all show different conversion numbers, which is right?"
- "Reconcile conversions across platforms" or "why do impressions differ between the DSP and the ad server?"
- "What is an acceptable discrepancy between two tools?" or "is a 12 percent gap a problem?"
- "Is this drop a real change or a tracking break?"
- "I need an anomaly-detection method that is not just a flat percent tolerance."
- "Check this report before it goes to the client" (freshness, nulls, volume drops).
- "Conversions fell off a cliff yesterday, what happened?"
- "Consent Mode is on, how does that change the GA4 number?"

Boundary: if the question is what a metric means or how to compute a KPI, that is `programmatic-foundations`. If it is how to build or schedule the report itself, that is `dv360-reporting`. If it is which report a goal needs, that is `reporting-by-campaign-goal`. If it is whether an observed difference is causal lift, that is a controlled experiment in `incrementality-and-experimentation`, not a reconciliation. This skill decides whether a number is trustworthy and whether a change is real; it does not design the campaign or the test.

## Quick reference

Run the data-quality gate before anyone reads the report. Reconcile before anyone escalates a gap. Use the statistical band before anyone calls a change an anomaly.

| Question | Do this first | Pass condition |
| --- | --- | --- |
| Is this report safe to send? | Freshness, null, and volume-drop check (below) | All three clear, or the exceptions are explained in the report |
| Why do two tools disagree? | Identify the legitimate causes (windows, timezone, dedup, IVT, Consent Mode) before assuming a bug | Gap sits inside the expected band for that pair of tools |
| Is this gap acceptable? | Compare against the discrepancy band for the metric and the source pair | Inside band: note it. Outside band: investigate, do not just report |
| Is yesterday an anomaly? | Compare to a weekday-and-seasonality baseline with a statistical band, not a flat percent | Inside the band: normal variation. Outside: flag with the size of the deviation |
| Real change or tracking break? | Check whether correlated metrics moved together (a true demand shift) or one signal broke alone | Coherent move across metrics points to real; a lone broken signal points to a break |

Rule of thumb: never reconcile to zero. Different tools count different events, in different timezones, after different filters, over different windows. The job is to explain the gap and confirm it sits in the expected band, not to force two systems to agree.

## Why a DSP, Campaign Manager 360, and GA4 legitimately differ

These are not the same number measured three times. They are three different definitions of the event. Walk the causes before you call anything broken.

- **Attribution window and model.** Each tool credits a conversion over its own lookback and to its own touchpoint. Campaign Manager 360 counts a conversion against the Floodlight conversion window for clicks and impressions, and its model treats a click as more significant than an impression. GA4 uses a key-event lookback window that defaults to 90 days for most key events (30 for acquisition events such as first_visit and first_open) and a reporting attribution model that is data-driven by default, spreading credit across touchpoints. A DSP counts conversions on its own post-click and post-view windows. The same purchase can land in a different day, be credited to a different channel, and be counted or not depending on whose window it falls inside.
- **Timezone.** A DSP, an ad server, and an analytics property can each run on a different reporting timezone, so a conversion at 11pm local lands on different calendar days in each tool. A timezone boundary alone produces a daily gap that nets out over a week. In GA4, changing the reporting timezone applies only going forward and can itself create a one-time flat spot or spike in the data, so a recent timezone change is a reconciliation cause in its own right.
- **Deduplication.** An ad server deduplicates conversions across the placements it serves; a DSP deduplicates within itself; GA4 deduplicates by its own session and user logic. The same user converting once can be counted once in one tool and more than once across tools that do not share a dedup key. Post-click and post-view collapsed into one column also inflates the total, which is why they belong in separate columns.
- **Bot and invalid-traffic filtration.** Impression and click counts diverge because each system filters invalid traffic on its own schedule and to its own standard. Display & Video 360 and Campaign Manager 360 remove general invalid traffic (GIVT, known spiders and bots and routine checks) and sophisticated invalid traffic (SIVT, which needs deeper analysis), some pre-bid (never bought) and some post-serve (credited back), with an additional HUMAN integration. A third-party tracker or a site analytics tool filtering on a different definition will not match the ad server's filtered count. A gap between a "raw" counter and a filtered counter is expected, not a defect.
- **Consent Mode and modeled conversions.** Where Consent Mode is deployed, GA4 can model the behavior of users who declined analytics storage from the behavior of similar users who consented, once the property clears the data thresholds (on the order of 1,000 events per day with analytics_storage denied for at least 7 days, and at least 1,000 daily users with analytics_storage granted across 7 of the previous 28 days). Modeled conversions are an estimate the DSP and the ad server do not produce, so the GA4 number can legitimately exceed an observed-only count. Know whether the number you are comparing is observed, modeled, or both.

Sequence the explanation: window, then timezone, then dedup, then IVT filtration, then Consent Mode modeling. Most cross-tool gaps are fully accounted for by these five before any tag or pipeline bug is in play.

## Acceptable discrepancy bands

A band is the range where a difference is expected and needs only a note, versus the range where it needs investigation. Bands are directional defaults for setting expectations; calibrate them per account from its own clean-period history, because the right band depends on the tools, the windows, and the traffic mix.

- **Impressions, DSP vs ad server (Campaign Manager 360):** small, commonly within a few percent. Both count served impressions and both filter IVT, so a clean integration sits low single digits apart. A gap above roughly 10 percent points at a trafficking or tag problem, not just timing.
- **Clicks, DSP vs ad server:** typically a few percent, similar logic to impressions, with click-measurement timing adding a little noise.
- **Conversions, ad server vs GA4 (or DSP vs GA4):** wide and expected to be wide, often tens of percent, because the window, the model, the dedup, and Consent Mode modeling all differ. Here the band is not a tight number; the deliverable is to explain the composition of the gap (how much is window, how much is model, how much is modeling) rather than to chase a single tolerance.
- **Same metric, same tool, period over period:** use the statistical band below, not a fixed percent, because the right tolerance depends on the day of week and the season.

The rule that matters more than any specific percent: decide the band before you read the number, write it next to the metric, and treat inside-band as "note and move on" and outside-band as "investigate before reporting." A gap with no pre-agreed band is just an argument.

## Pre-ship data-quality check

Run this gate on every report before it reaches a client. It is three fast checks, and any failure is a hold, not a footnote.

1. **Freshness.** Confirm the data covers the full intended window and is not partial. Check the max date in the data against the expected date, and account for known reporting lag (reach and some conversion metrics lag a few days, so a same-day pull is structurally incomplete). A report that silently stops a day short reads as a cliff that is not real. If the latest day is partial, either exclude it or label it partial, never average it in.
2. **Nulls and zeros.** Scan the key metric and dimension columns for unexpected nulls, zeros, or empty strings. A conversion column that went all-zero, a creative dimension that came back blank, or a cost column with nulls is a pipeline or join failure, not a performance result. Distinguish a true zero (no spend that day) from a missing value (the feed broke); a sudden block of nulls in a previously populated column is the tell.
3. **Sudden volume drop or spike.** Compare each core metric's latest value to its recent baseline using the weekday-and-seasonality band below, not a flat percent. A volume that falls outside the band is either a real change or a tracking break, and the report should not ship asserting it is performance until that is resolved. A drop that lines up exactly with a timezone change, a tag deploy, or a pipeline run is a break to fix, not a finding to send.

If all three clear, the report is safe to send. If any fails, hold the report, find the cause, and either fix it or annotate the exception explicitly. A client who learns later that a "30 percent drop" was a broken feed loses trust in every future report.

## A real anomaly-detection method

A flat tolerance ("alert if a metric moves more than 20 percent") fails twice: it screams every Monday when weekend traffic returns, and it stays silent when a metric drifts 15 percent below where its own seasonality says it should be. Replace it with a band built from the metric's own recent, comparable history. The `anomaly-detection` loop runs this daily; this is the band it compares against.

1. **Build a like-for-like baseline, not a flat average.** Compare a day to the same weekday in recent weeks, not to the trailing average across all days. Weekday and weekend behave differently for almost every programmatic metric (spend, conversions, CTR, CVR), so the baseline for a Saturday is the recent Saturdays. Use a trailing window of several weeks (commonly 4 to 8) so the baseline reflects the current season without being swamped by stale history.
2. **Compute a statistical band, not a fixed percent.** From the comparable baseline days, take the median (robust to one prior outlier) and a spread measure. A simple, defensible band is the median plus or minus a multiple of the spread: for example, flag a point that falls outside roughly 3 standard deviations of the comparable baseline, or use the median absolute deviation scaled similarly when the data is noisy and you do not want one past spike to widen the band. The multiple is the sensitivity dial: about 3 is a reasonable default that catches real breaks without crying wolf, tighten it for a high-stakes metric, loosen it for a naturally volatile one.
3. **Account for known seasonality and events explicitly.** A holiday, a sale, a flight start or end, and a pacing reset are expected deviations, not anomalies. Maintain a short list of known events and either widen the band on those days or exclude them from the baseline, so a Black Friday spike does not flag and does not poison next week's baseline. Year-over-year context helps for strong-seasonal businesses where last month is not a fair baseline for this month.
4. **Read direction and coherence to separate a real change from a tracking break.** An anomaly is more likely a real change when correlated metrics move together in a sensible way (spend up with impressions up, conversions down with CVR down across all sources). It is more likely a tracking break when one signal breaks alone while its neighbors hold, when the drop is a clean step to zero rather than a slope, or when it aligns exactly with a deploy, a timezone change, or a pipeline run. Always pull fresh data and note where conversion lag could distort a same-day read before calling it.
5. **Make every flag reproducible.** A flag states the metric, the baseline value, the current value, the size of the move in band terms (how many standard deviations or how far outside the band), and a likely cause to check. That is an alert an expert can act on; "conversions look low" is not. Normal variation inside the band is never flagged.

This is standard time-series and statistical-process-control practice (a control band around a seasonal baseline), applied to programmatic metrics. It is method, not a vendor feature, so it works against any platform's numbers.

## Decision rules and thresholds

- **Never reconcile to zero; reconcile to the expected band.** Two tools that count different events under different rules should not match. Confirm the gap is composed of known causes and sits in the band, then stop.
- **Walk the five causes in order before blaming a bug.** Window, timezone, dedup, IVT filtration, Consent Mode modeling. Most gaps are fully explained before a tag is in question.
- **Hold any report that fails the freshness, null, or volume check.** A partial day, a null column, or an unexplained drop is a hold, not a footnote. Fix or annotate before sending.
- **Exclude or label a partial latest day.** Reporting lag makes a same-day pull incomplete; averaging it in manufactures a fake decline.
- **Use a weekday-and-seasonality band, not a flat percent, for "is this an anomaly."** The flat tolerance both false-alarms on weekends and misses seasonal underperformance.
- **Set the band multiple from the stakes.** About 3 standard deviations of the comparable baseline is a sane default. Tighten for a high-value metric, loosen for a volatile one.
- **Coherence across metrics points to real; a lone broken signal points to a break.** Check whether neighbors moved together before calling a change performance.
- **Know whether a conversion number is observed, modeled, or both.** A modeled GA4 number can legitimately exceed an observed DSP or ad-server count under Consent Mode.

## Templates and examples

- **Three tools, three conversion numbers.** "The DSP shows 1,180 conversions, Campaign Manager 360 shows 1,020, GA4 shows 1,310 for the same week, which is right?" None is wrong. Reconcile by composition: the DSP and ad server differ on window and dedup and post-view credit; GA4 differs further because its 90-day data-driven model and Consent Mode modeling add credit the others do not produce. Deliverable: a short table attributing the spread to window, model, dedup, and modeling, with the recommendation to standardize on one source of truth per decision (the ad server for media-credited conversions, GA4 for on-site behavior), not to force them equal. Misread to avoid: declaring the lowest number "the real one" or the highest "inflated" without decomposing the gap.
- **Pre-ship gate catches a fake cliff.** A weekly performance report shows conversions down 28 percent on the final day. The freshness check shows the final day is partial (the pull ran before the day closed and before conversion lag matured). Action: exclude or label the partial day; the real week-over-week is flat. Misread to avoid: sending "conversions fell 28 percent" as a finding.
- **Statistical band beats flat tolerance.** A flat 20 percent rule flags every Monday (weekend-to-weekday return) and never flags a creative that is quietly running 15 percent under its weekday baseline. The weekday-and-seasonality band ignores the expected Monday lift (Mondays sit inside their own comparable baseline) and flags the 15 percent drift because it falls outside the band for that weekday. The flag reads: "Tuesday CVR 1.8 percent vs comparable-Tuesday median 2.4 percent, 3.4 standard deviations low, check the conversion tag and a recent landing-page change."
- **Real change versus tracking break.** Conversions drop 40 percent overnight. If spend, impressions, and clicks held while conversions alone stepped to near zero, that is a tag or pipeline break: investigate the Floodlight or GA4 tag, a recent deploy, and the pipeline run. If spend and impressions fell with conversions in proportion, that is a real delivery change: investigate pacing, budget, and auction dynamics. The coherence test routes the investigation.

## Common pitfalls

- **Chasing a perfect match across tools.** They count different events under different rules. Explain the gap and confirm the band; do not force agreement.
- **Reporting a number with no pre-agreed band.** A gap or a change with no benchmark is unactionable. Set the band before reading the number.
- **Averaging a partial latest day.** Reporting lag and a same-day pull make the last day incomplete; including it fabricates a decline. Exclude or label it.
- **Flat-percent anomaly tolerance.** It false-alarms on weekday and seasonal swings and misses seasonal underperformance. Use a comparable-baseline statistical band.
- **Letting one past spike widen or poison the baseline.** Use the median and a robust spread, and exclude known events, so Black Friday does not set next week's expectations.
- **Calling a tracking break a performance change (or vice versa).** Check coherence across metrics and alignment with deploys and timezone changes before attributing.
- **Comparing observed to modeled numbers as if they were like for like.** Consent Mode modeling adds estimated conversions; know what each number includes.
- **Ignoring a recent timezone change.** A timezone switch shifts conversions across calendar days and can create a one-time flat spot or spike; treat it as a reconciliation cause.

## Sources

- Filtering invalid traffic to ensure quality, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6076504 (as of June 2026)
- Filtering invalid traffic to ensure quality, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/6076504 (as of June 2026)
- How Floodlight counts conversions, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823400 (as of June 2026)
- About attribution modeling, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/6173082 (as of June 2026)
- Behavioral modeling for consent mode, Google Analytics 4 Help: https://support.google.com/analytics/answer/11161109 (as of June 2026)
- Select attribution settings, Google Analytics 4 Help: https://support.google.com/analytics/answer/10597962 (as of June 2026)
- Set up Analytics for a website and/or app (reporting time zone behavior), Google Analytics Help: https://support.google.com/analytics/answer/9304153 (as of June 2026)
- Comparing metrics: Google Analytics 4 vs Universal Analytics (sources of discrepancy), Google Analytics Help: https://support.google.com/analytics/answer/11986666 (as of June 2026)

The anomaly-detection method in this skill (a weekday-and-seasonality baseline, a robust statistical band from the median and a spread measure, explicit handling of known seasonal events, and the coherence test that separates a real change from a tracking break) is standard time-series and statistical-process-control practice rather than the claim of any single vendor page, and is presented here as established best practice without attribution to one source.
