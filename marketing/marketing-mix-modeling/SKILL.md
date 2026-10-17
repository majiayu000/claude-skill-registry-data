---
name: marketing-mix-modeling
description: Decide when marketing mix modeling (MMM) is the right tool, what data it needs, how to read its output, and where it beats or loses to multi-touch attribution and geo lift. Use when the user asks about marketing mix modeling, MMM, "media mix model", Meridian, Robyn, "budget allocation model", "model the whole media plan", "measure offline and TV together", "MMM vs MTA", "MMM vs incrementality", channel contribution, response curves, saturation, adstock, or measuring channels you cannot experiment on.
---

# Marketing mix modeling

Marketing mix modeling (MMM) answers one question well: across every channel including offline and the ones you cannot experiment on, where should the next dollar go. It is a top-down statistical model of aggregate outcomes against media spend and external factors, privacy-safe because it never touches user-level data. This skill decides when MMM is the right tool, what data it actually needs, how to read its output without overclaiming, the honest limits, and how it sits against multi-touch attribution and geo lift. The modern open-source references are Google Meridian and Meta Robyn.

For what each metric means and the KPI math, see the `programmatic-foundations` skill. For designing a report by objective and reading it like an expert, see the `reporting-by-campaign-goal` skill. For the causal ground truth that calibrates an MMM (conversion lift, geo lift, brand lift) and the statistics behind a valid test, see the `incrementality-and-experimentation` skill.

## When to use this skill

- "How should we split next quarter's budget across all channels?"
- "Marketing mix modeling," "MMM," "media mix model," "build an MMM."
- "Meridian" or "Robyn," or "which open-source MMM tool should we use?"
- "Measure TV, offline, and digital in one model" or "include offline media."
- "How do we measure now that signal loss broke our user-level tracking?"
- "Read this MMM output," "channel contribution," "ROI by channel," "response curve," "saturation," "adstock," "diminishing returns."
- "MMM vs MTA," "MMM vs multi-touch attribution," "MMM vs incrementality," "MMM vs geo lift."

Boundary: if the question is whether one channel's conversions are causally incremental, that is an experiment in `incrementality-and-experimentation`, not an MMM. If it is which report a campaign goal needs, that is `reporting-by-campaign-goal`. If it is what a metric means, that is `programmatic-foundations`. MMM is the portfolio-allocation tool; it is not a replacement for an experiment and not a per-user attribution method.

## Quick reference

Pick MMM for the cross-channel allocation question, calibrate it with experiments, and do not ask it to do an experiment's job.

| You need | Reach for | Why |
| --- | --- | --- |
| Budget split across all channels, including offline and TV | MMM | Aggregate, top-down, covers channels you cannot tag or experiment on |
| Whether a specific channel's conversions are incremental | A controlled experiment (conversion lift or geo lift) | MMM is correlational; an experiment is causal ground truth |
| Per-user, in-channel credit for a tactical optimization | Multi-touch attribution (MTA) | MTA assigns credit along observed user paths; MMM has no user paths |
| Causal read on TV or upper-funnel where you cannot suppress users | Geo lift | Randomizes geography; MMM infers, geo lift tests |
| A privacy-safe measurement that survives signal loss | MMM | Uses only aggregate spend and outcomes, no cookies or user-level data |
| An open-source MMM to build on | Google Meridian or Meta Robyn | Both are open-source, documented, and calibrate against experiments |

Rule of thumb: MMM is for the portfolio question (how to allocate across everything at once), experiments are for the causal truth that anchors it, and MTA is for tactical in-channel credit. Triangulate the three. Crowning any one as the single source of truth is the classic mistake, called out in `reporting-by-campaign-goal` and `incrementality-and-experimentation`.

## What MMM is and when to use it

MMM is a regression of a business outcome (sales, revenue, conversions) on media spend per channel and on external factors (seasonality, price, promotions, distribution, macro), fit over a long history, to estimate how much each channel contributed and how the outcome responds as spend changes. Meridian and Robyn both frame MMM as a causal-inference approach to budget allocation that uses observational data at an aggregate level that is privacy safe. Reach for it when:

- **The question is cross-channel budget allocation.** MMM compares channels on a common outcome and produces a recommended allocation and response curves, which a per-channel report cannot do because every platform claims the same conversion.
- **Offline and unaddressable media are in scope.** TV, radio, print, out-of-home, direct mail, and any channel without a user-level signal can sit in an MMM because it works on aggregate spend, not on tags. This is MMM's home turf and the reason it predates digital attribution.
- **Signal loss has degraded user-level measurement.** As cookies, device IDs, and cross-site tracking erode, user-path methods lose coverage. MMM is resilient to this because it never needed user-level data; it reads spend and outcomes in aggregate. This is a primary reason MMM has returned to favor.

Do not reach for MMM to prove a single channel is incremental, to optimize a campaign day to day, or to assign credit to an individual user's path. Those are experiment and MTA jobs.

## Data requirements and the need for variation

MMM is only as good as the variation in its inputs. The honest prerequisites:

- **A long, granular history.** Enough time periods (commonly two to three years of weekly data, more is better) so the model can separate media effects from trend and seasonality. Too few periods and the model cannot identify the effects at all.
- **Spend (and ideally exposure) per channel.** Media spend for every channel, by period. Where available, an exposure metric (impressions, or reach and frequency) per channel can sharpen the estimate, because modeling on reach and frequency instead of a single spend figure can yield more precise impact estimates and frequency guidance. Include organic and non-spend activity (email, social posts, PR) as separate variables where it drives the outcome.
- **The outcome and the controls.** The target KPI (often sales) by period, plus the external factors that also move it: price, promotions, distribution, seasonality, holidays, weather, and macro conditions. Omitting a real driver makes the model blame media for something else.
- **Media variation, the make-or-break input.** A channel whose spend never changes cannot have its effect estimated, because there is no contrast to learn from. The model needs channels to vary over the history (flights on and off, budgets up and down, regional differences) so it can attribute changes in the outcome to changes in spend. Flat, always-on spend at a constant level is the silent killer of an MMM: the channel looks like a constant and the model cannot tell its contribution from the baseline. Where natural variation is thin, deliberate experimentation (geo holdouts, planned flighting) both improves the model and provides calibration.

If the data is short, the channels do not vary, or the major external drivers are missing, the model will produce confident-looking numbers that are not trustworthy. The fix is more history, more variation, and experiments to calibrate, not a fancier model.

## The modern open-source tools

Two open-source MMM frameworks are the current references. Name them as references, not as a required dependency; the decision logic in this skill is tool-agnostic.

- **Google Meridian.** An open-source MMM built by Google, designed to estimate the causal impact of marketing using a Bayesian approach. It builds in real-world effects like the lagged effect of advertising (adstock) and saturation, offers the option to use reach and frequency data as inputs for more precise estimates and frequency recommendations, supports setting custom ROI priors from past experiments to calibrate the model, and outputs ROI estimates with credible intervals, response curves, and budget-optimization recommendations.
- **Meta Robyn.** An experimental, open-source, AI/ML-powered MMM package from Meta Marketing Science. It uses ridge regression to handle multicollinearity across many channels, a gradient-free evolutionary optimizer (Nevergrad) for hyperparameter search, and Prophet for trend, season, holiday, and weekday decomposition, fits adstock and Hill-function saturation curves, supports organic (non-spend) variables, and strongly recommends calibrating the model against experimental ground truth. It needs no PII or individual-level data.

Both share the same shape: aggregate inputs, adstock and saturation built in, experiment calibration recommended, no user-level data. Choose based on the team's stack and statistical comfort (Bayesian priors in Meridian, evolutionary hyperparameter search in Robyn); the read-out and the caveats below apply to either.

## How to read MMM output

The output is a set of estimates with uncertainty, not facts. Read each piece for what it claims and what it does not.

- **Channel contribution.** How much of the modeled outcome the model attributes to each channel over the period, usually a decomposition of total sales into baseline plus each channel's contribution. Read it as the model's best estimate of incremental effect given the data, with its uncertainty band, not as a measured truth. A channel with a wide interval is poorly identified, often because its spend did not vary.
- **ROI (or mROI) by channel.** Contribution divided by spend is the average return; the marginal return (mROI, the return on the next dollar) is what should drive reallocation, because a channel can have a high average ROI while its next dollar is nearly wasted from saturation. Move budget on marginal return read off the response curve, not on average ROI.
- **Saturation and response curves.** The response curve plots outcome against spend for a channel and bends over: each additional unit of spend adds less (diminishing returns, often a Hill or S-shaped curve). Read where the channel sits on its curve. Below saturation, more spend pays; near the flat top, the next dollar is wasted and belongs in an underspent channel. This curve is the actual allocation tool, more than the single ROI number.
- **Adstock (carryover).** Advertising effect lags and decays after exposure rather than landing all at once, so adstock spreads a burst of spend across later periods. Read it to understand that this week's sales reflect prior weeks' media, and that turning a channel off does not zero its effect immediately. Misreading adstock makes a channel look dead the week it pauses when its carryover is still working.
- **Credible or confidence intervals.** Every estimate carries uncertainty. Lead with the interval, exactly as in an experiment read: a tight interval is a confident estimate, a wide one means the data could not pin the channel down. Reallocating hard on a point estimate with a wide interval is the modeling version of reading a noisy lift number as truth.

## The honest caveats

State these every time, especially to a stakeholder who wants MMM to be the single answer.

- **Correlational, not experimental.** MMM explains correlation in aggregate history. On its own it cannot prove causation the way a randomized holdout does; an omitted variable or two collinear channels can mislead it. Its causal claim is only as strong as its specification and its calibration against experiments. Use it for allocation, anchor its channel estimates with conversion lift and geo lift, and never present a model contribution as proven incrementality.
- **Needs enough variation, or it cannot identify effects.** A channel that did not vary cannot be estimated, and collinear channels (always advertised together) cannot be separated cleanly. Thin variation produces wide intervals and unstable estimates that swing between refits.
- **Slow to refresh and coarse in grain.** An MMM is built on long histories and refreshed on the order of quarterly, so it cannot steer a daily optimization or evaluate a change made last week. It answers the strategic allocation question, not the in-flight tactical one. Pair it with fast in-platform reporting for the day-to-day.
- **Garbage in, confident-looking garbage out.** Missing external drivers, mislabeled spend, or too short a history yield numbers that look authoritative and are not. The remedy is better data and calibration, not a more elaborate model.

## MMM vs multi-touch attribution vs geo lift

These three measure different things; the error is treating them as competitors for one crown. Match the method to the decision.

- **MMM: cross-channel and offline allocation.** Top-down, aggregate, privacy-safe, covers every channel including the unaddressable. Strategic and slow. Best for "how do we split the total budget." Weakness: correlational, coarse, needs variation.
- **Multi-touch attribution (MTA): tactical in-channel credit.** Bottom-up, assigns credit along observed user paths across touchpoints. Best for "within the addressable channels, which touchpoints and tactics get credit for this conversion." Weakness: needs user-level path data (eroding under signal loss), cannot see offline, and is observational so it overcredits exposed users unless calibrated. The path view itself lives in `path-to-conversion-analysis`.
- **Geo lift: causal read where you cannot suppress users.** Randomizes geography to measure the incremental effect of a channel you run everywhere or cannot tag at the user level (CTV, linear, upper funnel). Best for "is this channel actually causing outcomes." Weakness: lower statistical power than user-level tests (tens of markets, not millions of users) and needs well-matched markets and a clean pre-period. Full design and statistics are in `incrementality-and-experimentation`.

The expert posture: use MMM to set the allocation across everything, geo lift and conversion lift to establish the causal truth for the channels that matter, and MTA for tactical credit inside the addressable channels. Feed the experiment results back as calibration on the MMM (Meridian's ROI priors, Robyn's calibration step). Triangulate; do not crown one. This is the same triangulation called out in `reporting-by-campaign-goal` and `incrementality-and-experimentation`.

## Core process

1. **Confirm MMM is the right tool for the decision.** Cross-channel allocation including offline or signal-loss-resilient measurement points to MMM. A single-channel incrementality question points to an experiment; a per-user tactical-credit question points to MTA. Pick the tool from the decision, not from what is available.
2. **Check the data can support a model.** Enough history (commonly two to three years weekly), spend and where possible exposure per channel, the outcome, the real external drivers, and crucially genuine variation in media. If a channel never varied, plan to flight it or run a geo test rather than expect the model to estimate it.
3. **Build or commission the model with adstock and saturation, on an open-source reference if building.** Meridian or Robyn give a documented, calibratable starting point. Include carryover and diminishing returns, and the controls for seasonality, price, and promotions.
4. **Calibrate against experiments.** Feed conversion lift and geo lift results in as priors or calibration so the model's channel estimates are anchored to causal truth, not left to correlation alone. This is the step that separates a credible MMM from a curve-fitting exercise.
5. **Read the output as estimates with intervals.** Lead with marginal ROI and where each channel sits on its response curve, report credible intervals, and treat wide-interval channels as poorly identified. Translate the read into an allocation recommendation, not a claim of proven incrementality.
6. **Refresh on a strategic cadence and pair with fast reporting.** Refit on the order of quarterly, and use in-platform reporting and experiments for anything faster than the model can see. Re-run the allocation when spend mix, market conditions, or new experiment results change the picture.

## Decision rules and thresholds

- **Use MMM for allocation, experiments for causal truth, MTA for tactical credit.** Three jobs, three tools. Do not substitute one for another.
- **No media variation, no estimate.** A channel that did not vary cannot be measured; plan flighting or a geo test instead of trusting a flat-spend coefficient.
- **Reallocate on marginal ROI and the response curve, not average ROI.** A high average ROI near saturation still wastes the next dollar.
- **Lead with the interval, not the point estimate.** A wide credible interval means the channel is poorly identified; do not move hard budget on it.
- **Calibrate with experiments or label the model uncalibrated.** An MMM anchored to lift tests is credible; one fit on correlation alone is a hypothesis, and should be presented as one.
- **Do not use MMM for in-flight tactical decisions.** It refreshes too slowly and is too coarse; use fast reporting for the day to day.
- **Never present a model contribution as proven incrementality.** It is correlational. Say so to the stakeholder who wants it to be the final word.

## Templates and examples

- **Cross-channel budget split.** Question: "How should we allocate next quarter across CTV, display, search, social, and linear TV?" Tool: MMM, because the question spans addressable and offline channels at once. Read: marginal ROI and response-curve position per channel, with credible intervals, calibrated against the geo lift on CTV and the conversion lift on search already run. Output: a recommended reallocation that shifts budget from channels near saturation to underspent channels with headroom on their curves. Misread to avoid: presenting the model's channel contributions as proven incremental effects rather than calibrated estimates.
- **Offline plus digital in one view.** Question: "We spend heavily on linear TV and direct mail that our digital attribution cannot see, are they working?" Tool: MMM, the only method that brings unaddressable media into the same model as digital. Prerequisite: ensure TV and mail spend varied over the history (flighting, regional differences); if they ran flat and always-on, commission a geo test to create the variation and the calibration. Misread to avoid: concluding offline "does not work" when flat spend simply gave the model nothing to estimate.
- **Signal-loss resilience.** Question: "Our user-level tracking lost half its coverage, how do we still measure?" Tool: MMM as the durable backbone, because it never needed user-level data, with geo lift for causal reads on key channels and whatever MTA coverage survives for tactical credit. Misread to avoid: trying to rebuild a complete user-path picture under signal loss instead of moving the strategic measurement to aggregate methods.
- **MMM vs MTA disagreement.** Situation: "MMM says social is underperforming, MTA says social drives a lot of conversions." Resolution: they measure different things. MTA credits social along observed user paths (and can overcredit exposed users); MMM estimates social's aggregate marginal contribution net of other drivers. Run or cite a geo lift on social to get the causal truth, then trust the method the experiment supports and recalibrate the MMM. Misread to avoid: picking the answer you prefer instead of letting an experiment arbitrate.

## Common pitfalls

- **Treating MMM as an experiment.** It is correlational. Use it for allocation and calibrate it with lift tests; never present its output as a causal incrementality result.
- **Crowning one method.** MMM, MTA, and geo lift answer different questions. Triangulate; do not declare a single source of truth.
- **Modeling flat-spend channels.** No variation means no identifiable effect. Flight the channel or run a geo test to create contrast and calibration.
- **Reallocating on average ROI.** The next dollar follows marginal ROI and the response curve; average ROI hides saturation.
- **Ignoring the intervals.** A point estimate with a wide credible interval is a poorly identified channel, not a finding. Lead with the interval.
- **Omitting real external drivers.** Leaving out price, promotions, or seasonality makes the model blame media for their effects. Include the controls.
- **Expecting MMM to move fast.** It refreshes on a strategic cadence and cannot steer daily optimization. Pair it with fast reporting.
- **Reading a paused channel as dead.** Adstock carryover means effect persists after spend stops; do not zero a channel the week it pauses.

## Sources

- Meridian overview, Google for Developers: https://developers.google.com/meridian (as of June 2026)
- Meridian, about the project, Google for Developers: https://developers.google.com/meridian/docs/basics/about-the-project (as of June 2026)
- About MMM as a causal inference methodology, Meridian, Google for Developers: https://developers.google.com/meridian/docs/causal-inference/about-mmm-causal-inference-methodology (as of June 2026)
- Welcome to Robyn, Meta open source: https://facebookexperimental.github.io/Robyn/docs/welcome/ (as of June 2026)
- Key features, Robyn, Meta open source: https://facebookexperimental.github.io/Robyn/docs/features/ (as of June 2026)
- An Analyst's Guide to MMM, Robyn, Meta open source: https://facebookexperimental.github.io/Robyn/docs/analysts-guide-to-MMM/ (as of June 2026)
