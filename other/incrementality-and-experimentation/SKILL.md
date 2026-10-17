---
name: incrementality-and-experimentation
description: Design and read an incrementality test with real statistical rigor. Use when the user asks about incrementality, "is it incremental", lift test, conversion lift, geo lift, matched markets, holdout, ghost ads, PSA control, brand lift, experiment design, statistical significance, statistical power, minimum detectable effect, sample size, time to significance, confidence intervals, peeking, "how do I prove the ads worked", or whether observed conversions would have happened anyway.
---

# Incrementality and experimentation

The rest of this library names incrementality, lift, and holdout constantly. This skill is where you actually design a test that can prove it and read the result without fooling yourself. Two things sink most lift tests: the wrong method for the data you have, and reading a noisy number as if it were truth. This skill picks the method from data availability, budget, and channel, then enforces the statistics: a minimum detectable effect set before launch, enough power and volume to clear it, a comparison group defined and frozen up front, and a result read as a confidence interval rather than a point estimate.

For what each metric means and the KPI math, see the `programmatic-foundations` skill. For choosing a report shape by objective, see the `reporting-by-campaign-goal` skill. For Floodlight, attribution models, and the platform Brand Lift and reach mechanics, see the `dv360-measurement-and-attribution` skill. For event-level lift built from impression logs in a clean room, see the `dv360-advanced-analytics-adh` skill and the `amazon-marketing-cloud` skill.

## When to use this skill

- "Is this incremental?" or "would these conversions have happened anyway?"
- "Run a lift test," "conversion lift," "set up a holdout," "ghost ads," "PSA control."
- "Geo lift," "matched markets," "geo holdout," "how do I test CTV or upper funnel?"
- "Brand lift," "did the campaign move perception?"
- "Is this result statistically significant?" or "what is the confidence interval?"
- "What sample size do I need?" or "how long until this reaches significance?"
- "What is the minimum detectable effect / MDE / power for this test?"
- "Can I stop the test early?" or "the result looks good after three days, are we done?"
- "How do I prove the ads worked?" to a finance stakeholder who distrusts last-click.

Boundary: if the question is which attribution model to pick or how Floodlight counts, that is `dv360-measurement-and-attribution`. If it is which report to pull for a goal, that is `reporting-by-campaign-goal`. If it is how to write the clean-room SQL that computes a lift, that is `dv360-advanced-analytics-adh` or `amazon-marketing-cloud`. This skill decides the experiment design and the statistical read; the sibling skills execute the mechanics on a given platform. Marketing mix modeling is a different tool with a different job, covered below only enough to keep you from confusing it with an experiment.

## Quick reference

Pick the method from what you can actually randomize and observe, not from what is easiest to run. Full decision logic is below the table.

| Method | Randomizes at | Use when | Reads out |
| --- | --- | --- | --- |
| Conversion lift (user holdout / ghost ads / PSA) | The user or device | You can hold out eligible users from exposure and observe their conversions | Incremental conversions, incremental CPA, lift percentage with a confidence interval |
| Geo lift / matched markets | The geographic market | User-level holdout is not feasible (most CTV, linear, upper funnel, walled-garden cross-channel) | Incremental conversions or revenue inferred from treated vs control market gap |
| Brand lift survey | The user (survey panel) | The outcome is perception (awareness, recall, consideration), not a conversion | Absolute and relative lift in survey responses, lifted users, with a confidence interval |
| Marketing mix modeling | Nothing (observational) | You need cross-channel and offline budget allocation, including channels you cannot experiment on | Modeled channel contributions and response curves, not an experimental causal estimate |

Rule of thumb: prefer a user-level holdout when you can randomize users and the outcome is a tracked conversion, because it is the cleanest causal read. Move to geo when you cannot suppress at the user level (CTV, linear, upper-funnel reach, or measuring a whole channel). Use a brand lift survey when the outcome is in someone's head, not in a conversion log. Use marketing mix modeling for portfolio allocation across everything at once, and treat its output as calibration to validate against experiments, never as the experiment itself.

## How to choose the method

1. **Name the outcome.** A tracked conversion (purchase, signup, install) points to conversion lift or geo lift. A perception shift (recall, awareness, consideration) points to a brand lift survey. Revenue across many channels including offline points to marketing mix modeling, with experiments as the calibrator.
2. **Decide the unit you can randomize.** If you can withhold exposure from a clean, eligible set of individual users, you can run a user-level holdout, the strongest design. If the channel does not let you suppress at the user level (most connected TV, linear TV, audio, and broad upper-funnel buys), or you want to measure an entire always-on channel, randomize geography instead.
3. **Check the data you will observe.** User-level lift needs the conversion to be trackable back to the exposed and held-out users. Geo lift needs a conversion signal you can total by market (store sales, site conversions by region, calls) and enough comparable markets. A brand lift survey needs enough survey responses per metric, which broad reach provides and narrow targeting starves.
4. **Check budget and time.** A smaller effect or a rarer conversion needs more volume and more time to detect (see sample size below). If the budget or flight cannot produce the volume the minimum detectable effect requires, the honest move is to widen the effect you are willing to call, lengthen the test, or pick a coarser method, not to run an underpowered test and over-read the result.
5. **Confirm platform availability before promising a method.** The platform lift products are gated by eligibility, minimum volume, and sometimes a sales representative. Confirm availability for the specific account before you design around a product (see platform hooks below).

### The methods in practice

- **Conversion lift, user-level holdout.** Randomly assign eligible users to a treatment group (can be served the ads) and a control group (suppressed). After the flight, compare the conversion rate of the two groups. The difference is the incremental effect, because randomization makes the groups equivalent on everything except exposure. Variants: a **ghost ads** design logs the ad the control user would have been served and won at auction, so the comparison is exposed-eligible vs would-have-been-exposed rather than a crude on/off, which removes selection bias from who actually qualified. A **public service announcement (PSA) control** serves the control group an unrelated charity ad so both groups clear the same auction and ad-load, isolating the brand message; it costs control-group media and is being supplanted by ghost-ads-style designs where available.
- **Geo lift and matched markets.** When you cannot suppress individual users, split geography. Choose a set of treatment markets that get the campaign and control markets that do not, matched on pre-period conversion trend, size, and seasonality so they would have moved together absent the ads. Run the campaign in treatment only, then read the gap between treated and control markets against their pre-period relationship. This is the workhorse for CTV, linear, audio, and upper-funnel measurement, and for measuring a channel you run everywhere at the user level. Its cost is statistical power: you have tens of markets, not millions of users, so it detects only larger effects and needs a clean pre-period and well-matched controls.
- **Brand lift survey.** Survey an exposed group against an eligible-but-unexposed control and measure the difference in recall, awareness, consideration, favorability, or purchase intent. The control must stay unexposed and unretargeted or the baseline is contaminated. Accuracy scales with responses, so broad targeting and adequate budget per question are prerequisites, not nice-to-haves. Survey design lives partly in `dv360-measurement-and-attribution` for the DV360 product.
- **Marketing mix modeling (MMM).** A regression of outcomes (sales, revenue) on media spend and external factors across all channels and offline, producing modeled contribution and response curves. It is observational, not experimental: it explains correlation in aggregate history and cannot, on its own, prove causation the way a randomized holdout can. Its right role is cross-channel and offline budget allocation, and it is strongest when its channel estimates are calibrated against incrementality experiments. Use it for the portfolio question; use experiments for the causal truth that anchors it.

## Statistical rigor

This is where most tests fail, after the design is fine. Set these before launch and write them into the test plan.

- **Minimum detectable effect (MDE).** The smallest true lift the test is designed to detect at your chosen power and significance. Set it from the business: what lift would change a decision? If a 2 percent lift would not change the budget, do not design a test that strains to detect 2 percent. A smaller MDE demands disproportionately more sample, so choosing the MDE is choosing the cost of the test. Fix it first; everything else follows from it.
- **Statistical power.** The probability the test detects a real effect of at least the MDE when one exists. Plan for 80 percent power as a floor, higher for a decision you cannot revisit. Low power is the silent killer: an underpowered test that returns "not significant" has told you almost nothing, because it was never able to see the effect even if it was there.
- **Significance level and what it means.** The significance level (commonly 5 percent, a 95 percent confidence level) is the false-positive rate you accept: the chance of calling a lift real when it is noise. It is not the probability the result is true. Set it before the test and do not move the goalposts after seeing the data.
- **Sample size and time to significance.** Required sample rises as the MDE shrinks, as the baseline conversion rate falls, and as the variance rises. Rare conversions and small effects need large audiences and long flights. Estimate the sample (a power calculation, from baseline rate, MDE, power, and significance) before launch, then translate it into how long the planned spend takes to accumulate that many users or conversions. If the flight cannot reach it, the test is underpowered by construction; fix the design, do not run it and hope.
- **Read the confidence interval, not the point estimate.** A lift result is a range, not a number. "Lift was 8 percent" is incomplete; "lift was 8 percent, 95 percent confidence interval 3 percent to 13 percent" is the result. The interval shows the precision: a tight interval well above zero is a confident win, a wide interval that crosses zero means you cannot rule out no effect. Always report and reason from the interval. A point estimate with no interval is a guess dressed as a finding.
- **"No measurable lift" is not "no effect."** A non-significant result means the test could not distinguish the effect from zero at the chosen power, which can happen because the effect is genuinely near zero or because the test was too small to see it. Distinguish the two by the confidence interval and the power: a tight interval around zero is evidence of little or no effect; a wide interval from an underpowered test is evidence of nothing at all. Never let a stakeholder hear "not significant" as "proven not to work."
- **Peeking and early stopping.** Checking a frequentist test repeatedly and stopping when it first crosses significance massively inflates the false-positive rate, because with enough looks a pure-noise series will eventually cross by chance. Decide the run length and sample from the power calculation up front and read the result at the end. If you genuinely need to monitor and stop early, that requires a method built for it (a sequential or always-valid test with corrected boundaries), not naked daily peeking at a fixed-horizon test. Treat an early "we hit significance on day three" as a red flag to investigate, not a green light to ship.

## Design integrity

A clean statistic on a dirty design is still wrong. Protect the comparison.

- **Define and freeze the comparison group before launch.** Decide who is treatment and who is control, and the exact metric and window, before any spend. Pre-register it in the test plan. A control defined or adjusted after seeing results is not a control; it is a story.
- **Balance treatment and control.** Randomization should make the groups equivalent on size and pre-period behavior. Check it: compare the groups on the pre-period conversion rate and key composition before the flight. If they are not balanced going in, the post-period difference is confounded. Geo tests especially need explicit matching on pre-period trend, market size, and seasonality.
- **Prevent contamination.** Keep the control genuinely unexposed. Do not retarget, suppress, or separately advertise to the holdout, and watch for cross-contamination paths: a household sharing devices, a user crossing geo boundaries, a retargeting pool that quietly re-includes control users. In geo tests, contamination shows up as spillover between adjacent treated and control markets. Contamination shrinks the measured gap toward zero, so a contaminated test understates real lift and can hide a true effect.
- **Beware the confounded comparison.** The most common invalid lift is exposed versus organic: comparing people the ads reached to people they did not, when exposure itself was non-random. Exposed users differ from unexposed users in ways that drive conversion regardless of the ad (they were already in-market, already searching, already on the site). That gap is selection bias, not lift. A valid test makes treatment and control equivalent by randomization or by matching, so the only systematic difference is the ad.
- **Pre-register the analysis, not just the groups.** Write down the primary metric, the MDE, the run length, and the single read at the end before launch. This is what stops the test from drifting into "we found something significant if we slice by device and weekend," which is just multiple comparisons mining noise.

## Platform hooks

These are gated. Confirm eligibility and availability for the specific account with your platform representative before you design around any of them; do not treat them as always-on.

- **DV360 Conversion Lift.** A user-level randomized holdout run inside DV360. It is eligibility-gated and volume-gated: the documentation indicates campaigns should generate on the order of several thousand conversions during the study and run within a bounded window (about 7 to 56 days), and setup is handled with your Google sales representative rather than fully self-serve. Confirm the current minimums and that the account is eligible before promising it. Details on the surrounding measurement stack are in `dv360-measurement-and-attribution`.
- **DV360 Brand Lift.** A survey-based lift study set up under Experiments in DV360, with budget-per-question minimums (the YouTube and partners path lists per-question budget floors, and connected TV has a recommended per-question budget). Keep targeting broad enough to power the survey and protect the control. The survey policy and metric choices are covered in `dv360-measurement-and-attribution`.
- **Amazon Marketing Cloud exposed-versus-unexposed.** AMC lets you compute lift from the pseudonymized event log by comparing an exposed group to an unexposed group, returned as an aggregate that clears the privacy threshold. The hard part is not the SQL; it is constructing a valid unexposed group. Exposed-versus-organic inside AMC is just as confounded as anywhere else, because the people the campaign happened to reach are not a random sample. Build the comparison from a genuine holdout or a matched unexposed cohort, and design the query so groups clear the aggregation floor. The clean-room mechanics and privacy model are in `amazon-marketing-cloud`.
- **Google Ads experiments.** Google Ads runs A/B campaign experiments that split traffic between the original and the experiment arm (a cookie-based split assigns a user to one arm consistently; a search-based split can reach significance faster but lets a user see both). Use a 50/50 split for the cleanest comparison, and read the experiment's reported difference rather than eyeballing raw totals. This tests campaign changes against each other; it is the in-platform experiment surface, distinct from a media-level conversion lift holdout.
- **Event-level lift in a clean room.** When you want a custom holdout or a bespoke lift definition on impression logs, build it in Ads Data Hub (`dv360-advanced-analytics-adh`) or AMC (`amazon-marketing-cloud`). Both enforce aggregation thresholds on output, so design the groups coarse enough to return a result.

## Core process

1. **State the hypothesis as one decision sentence.** "Does the retargeting line drive incremental purchases, and is the incremental CPA under 40 dollars, this quarter?" fixes the outcome, the comparison, and the threshold that makes the answer actionable. A vague "did it work" produces an unfalsifiable test.
2. **Pick the method from outcome, randomization unit, data, and budget.** Use the table and the choosing logic above. A tracked conversion with user-level suppression goes to conversion lift; a CTV or upper-funnel buy goes to geo; a perception goal goes to brand lift; portfolio allocation goes to marketing mix modeling calibrated by experiments.
3. **Set the statistics before launch.** Choose the MDE from what would change a decision, set power (80 percent floor) and significance (commonly 95 percent confidence), run a power calculation for the required sample, and translate that into a run length given the planned spend. If the flight cannot reach the sample, redesign now.
4. **Define and freeze the comparison.** Pre-register treatment, control, the primary metric, the window, and the single end-of-test read. Confirm pre-period balance between the groups. Confirm platform eligibility and minimums with your representative.
5. **Run without peeking.** Let it reach the planned sample and run length. Do not stop early on a fixed-horizon test because it crossed significance; that inflates false positives. Guard the control against contamination throughout.
6. **Read the interval and tie it to the decision.** Report the lift with its confidence interval, state whether it clears the MDE and excludes zero, and distinguish "no measurable lift" from "no effect" using the interval and power. Close with the budget, bid, or channel decision the result drives. A test that changes nothing was a vanity test.

## Decision rules and thresholds

- **Prefer user-level holdout when you can randomize users and the outcome is tracked.** It is the cleanest causal read. Drop to geo only when user-level suppression is not possible or you are measuring a whole channel.
- **Set the MDE before the test, from the decision it informs.** A test designed to detect an effect smaller than what would change your action is wasting power; a test that can only detect an implausibly large effect cannot inform. Right-size the MDE first.
- **Floor power at 80 percent and confidence at the level you pre-commit.** Below that, a null result is uninformative. Higher for irreversible decisions.
- **Never read a point estimate without its confidence interval.** The interval is the result. Crosses zero means you cannot claim lift; tight and above zero is a confident win.
- **Do not peek and stop early on a fixed-horizon test.** Decide the run length up front. If you need to monitor and stop, use a sequential method designed for it.
- **A confounded comparison is worse than no test.** Exposed-versus-organic measures selection, not lift, and it reliably overstates impact. Make the groups equivalent by randomization or matching, or do not run it.
- **Confirm platform availability before designing around a product.** DV360 Conversion Lift, Brand Lift, and clean-room lift each carry eligibility and minimum-volume gates. Verify for the account first.
- **Use marketing mix modeling for allocation, experiments for truth.** Calibrate the model with lift tests; do not present a model output as an experimental result.

## Templates and examples

- **Direct-response retargeting, is it incremental?** Hypothesis: "The retargeting line drives incremental purchases at an incremental CPA under 40 dollars this quarter." Method: user-level conversion lift holdout (ghost ads if available), because purchases are tracked and users can be suppressed. Stats: MDE set to the smallest CPA improvement that would change the budget, 80 percent power, 95 percent confidence, sample sized from the baseline purchase rate, run length set so the planned spend reaches that sample. Read: incremental conversions and incremental CPA with a 95 percent confidence interval; ship more budget only if the interval clears the CPA threshold and excludes zero. Misread to avoid: comparing retargeted users to site visitors who were not retargeted, which is exposed-versus-organic selection bias and will overstate lift.
- **Connected TV awareness, did it drive site visits?** Hypothesis: "The CTV campaign drove incremental branded site visits over the eight-week flight." Method: geo lift with matched markets, because CTV cannot suppress at the user level. Design: treatment and control markets matched on pre-period visit trend, size, and seasonality; campaign in treatment only; read the treated-minus-control gap against the pre-period relationship. Stats: accept a larger MDE than a user-level test, because tens of markets give less power than millions of users; confirm enough comparable markets and a clean pre-period. Misread to avoid: reading a noisy market gap without a confidence interval, or letting spillover from treated into adjacent control markets shrink the measured lift.
- **Brand campaign, did perception move?** Hypothesis: "The campaign lifted unaided awareness among adults 18 to 34." Method: brand lift survey, exposed versus eligible unexposed control. Design: broad targeting to power the survey, control left unexposed and unretargeted, brand named early in the creative. Read: absolute and relative lift with a confidence interval and the baseline response rate. Misread to avoid: over-narrow targeting that starves responses and returns "no measurable lift," then reporting that as "the campaign did not work."
- **Cross-channel budget, where should the next dollar go?** Question: "How should we split next quarter across CTV, display, search, and offline?" Tool: marketing mix modeling for the allocation, with its channel estimates calibrated against the conversion lift and geo lift tests already run. Read: modeled contributions and response curves, presented as allocation guidance, with the experiments cited as the causal anchor. Misread to avoid: presenting the model's channel contribution as proven incrementality, or running no experiments and trusting the model's causality on faith.

## Common pitfalls

- **Exposed-versus-organic dressed as a lift test.** The single most common error. It measures who the ad reached, not what the ad caused, and overstates impact. Require randomization or matching.
- **Underpowered tests over-read.** A small or short test that returns "not significant" has told you little, not that the channel failed. Size for the MDE and report power.
- **Reporting a point estimate with no interval.** A lift number without its confidence interval hides whether it is a confident win or noise. Lead with the interval.
- **Confusing "no measurable lift" with "no effect."** Use the interval and power to tell them apart, and never let a stakeholder hear the stronger claim.
- **Peeking and early stopping.** Repeated looks at a fixed-horizon test inflate false positives. Fix the run length up front or use a sequential method.
- **Contaminating the control.** Retargeting the holdout, geo spillover, or shared-device leakage shrinks the gap toward zero and hides real lift. Guard the control end to end.
- **Defining the comparison after seeing data.** A control chosen post hoc, or a metric and window picked to flatter the result, is mining noise. Pre-register before launch.
- **Treating a platform lift product as always-on.** DV360 Conversion Lift, Brand Lift, and clean-room lift are gated by eligibility, volume, and sometimes a sales representative. Confirm before designing around them.
- **Crowning marketing mix modeling as the experiment.** It is observational. Use it for allocation and calibrate it with experiments; do not present its output as an experimental causal estimate.

## Sources

- Set up Conversion Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/16804790 (as of June 2026)
- Set up Brand Lift measurement, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9570506 (as of June 2026)
- Brand Lift surveys (policy), Display & Video 360 Help: https://support.google.com/displayvideo/answer/9724628 (as of June 2026)
- Set up a custom experiment, Google Ads Help: https://support.google.com/google-ads/answer/6261395 (as of June 2026)
- Introduction to Ads Data Hub, Google for Developers: https://developers.google.com/ads-data-hub/guides/intro (as of June 2026)
- Privacy checks in Ads Data Hub, Google for Developers: https://developers.google.com/ads-data-hub/guides/privacy-checks (as of June 2026)
- Attention Measurement Guidelines (IAB and MRC), Interactive Advertising Bureau: https://www.iab.com/guidelines/attention/ (as of June 2026)

Statistical methodology in this skill (minimum detectable effect, statistical power, significance level, sample size and time to significance, confidence-interval reading, the distinction between no measurable lift and no effect, and the bias from peeking and early stopping) is standard experimental-design and hypothesis-testing practice rather than the claim of any single vendor page, and is presented here as established best practice without attribution to one source.
