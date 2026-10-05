---
name: cx-conversation-sampling
description: Use to draw a defensible sample of support conversations for QA review, an audit or a manual analysis, so the results generalise to the population rather than to whatever was easy to pull. Trigger for "which tickets should we review", "how do we pick a sample", "is our QA sampling representative", stratified or risk-based sampling, review coverage design, or a finding based on a handful of hand-picked tickets.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Sampling conversations

Every manual review of support conversations is a sample, including the ones nobody
calls a sample. The question is only whether it was drawn deliberately.

This is about **how to draw it and how to weight the results**. How many you need for a
given precision is a different question — a sample can be perfectly sized and still
answer about the wrong population.

## The frame comes first

The **sampling frame** is the list of conversations you could have drawn from. Almost
every generalisation failure is a frame problem, not a size problem.

Write down explicitly:

- **What is in the frame** — window, channels, queues, statuses, languages.
- **What is silently missing.** Conversations not synced from a channel; deleted,
  merged or redacted records; anything the API does not return; a channel connected
  halfway through the window. Each of these removes a non-random slice.
- **What you excluded on purpose**, and the rule.

**A frame that omits a channel cannot support any organisation-wide claim**, however
large the sample. Say which population your result actually describes — that sentence
is the deliverable as much as the number is.

## Choose the design to match the question

**Simple random.** The default, and correct when you want one overall estimate. Boring
and defensible. Use it unless you have a specific reason not to.

**Stratified.** Split the frame into strata — channel, queue, team, language, risk band
— and sample within each. Use it when:

- you need per-stratum estimates, not just an overall one (almost always true for QA);
- strata differ a lot in the thing you are measuring, which improves precision for the
  same total sample;
- some stratum is small but important and simple random would return three of them.

**Sample small strata at a higher rate**, then **weight the results back by the
stratum's true share** when computing an overall figure. This is the step that gets
skipped, and skipping it means the overall number silently over-weights the segments
you oversampled. If you cannot weight, report per-stratum results only and no overall
figure.

**Risk-weighted / purposive.** Deliberately over-sample high-risk conversations —
complaints, low scores, regulated topics, vulnerable customers. Correct for finding
problems, and **it cannot produce a rate that describes the population**. A defect rate
from a risk-weighted sample describes risky conversations, and reporting it as the
overall defect rate is a serious and common error.

Run both when both questions matter: a random core for estimating, plus a risk-weighted
supplement for finding. Keep them separate in the analysis and never pool them into one
rate.

**Census.** For rare, high-severity categories — regulatory complaints, safeguarding —
review everything. Sampling a population of forty to save effort is a false economy.

## Randomise properly

- **Use a real random draw over the frame**, with a recorded seed so the sample is
  reproducible and auditable.
- **"The first 100 returned" is not random.** API results carry an implicit order —
  usually recency or id — and both correlate with the things you are measuring.
- **Neither is "conversations from last Tuesday".** Day of week and time of day
  correlate strongly with staffing, contact mix and quality.
- **Sample the whole window, not a convenient slice of it.**
- **Record the seed, the frame definition and the draw date.** Someone will ask how the
  sample was picked, and "randomly" is not an answer that survives an audit.

## Sampling for QA coverage

Ongoing QA sampling is the same problem with an extra constraint: it must also be
*fair to the people being measured*.

- **Every agent needs enough evaluations for the use.** If scores drive coaching only,
  a handful is fine. If they drive ranking or pay, they need the volume that supports
  it — and if the programme cannot afford that volume, the honest conclusion is that
  the scores may not be used for ranking.
- **Equalise by agent, not by ticket**, when the purpose is per-agent measurement.
  Ticket-proportional sampling gives high-volume agents narrow intervals and low-volume
  agents useless ones, and then compares them.
- **Do not let reviewers self-select** which conversations to review. Reviewer choice
  is the largest single source of bias in QA programmes, and it is invisible in the
  output.
- **Check what the sampler actually did.** Compare the composition of what was reviewed
  against the composition of what was eligible, periodically. Samplers drift, rules get
  edited, and a channel or team silently drops out. This check is cheap and it
  invalidates comparisons when it fails.

## Traps

- **Post-hoc filtering breaks the sample.** Drawing 200 and then analysing "the ones
  that were interesting" produces a purposive sample with a random sample's confidence
  intervals attached. If you filter after drawing, report the filter and treat the
  result as purposive.
- **Replacing unavailable items non-randomly.** If a drawn conversation cannot be
  reviewed — unavailable transcript, wrong language — record it as a non-response and
  either replace it with another random draw or report the non-response rate. Quietly
  picking the next one down the list re-introduces the ordering bias.
- **Reviewing until you find something.** That is search, not sampling, and it produces
  no rate at all.
- **Stale frames.** A frame built a week ago no longer matches the population.
- **Language.** A sample drawn without regard to language, reviewed only by reviewers
  who speak one of them, silently becomes a single-language sample.

## Present results to the user

1. **The frame** — what was in it, what is silently missing, what you excluded.
2. **The design** — simple, stratified, risk-weighted or census — and why it matches the
   question.
3. **The draw** — seed, date, sizes per stratum, and the sampling rate each implies.
4. **Weighting**, if strata were sampled at different rates, and the weighted overall
   estimate. Or a plain statement that no overall estimate is available.
5. **Non-response** — drawn items that could not be reviewed, and how they were handled.
6. **The population your result actually describes**, in one sentence. This is the
   sentence that stops a risk-weighted finding being quoted as an overall rate.
