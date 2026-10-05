---
name: cx-survey-design
description: Use to design or fix a customer support survey — CSAT, NPS, or CES — and to diagnose response bias. Trigger for "design a CSAT survey", "our CSAT doesn't match reality", "should we use NPS", survey response rate, non-response bias, survey timing or scale choice, comparing satisfaction across teams or channels, or interpreting a satisfaction trend.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Designing support surveys that measure something

A satisfaction score is a statistic about the people who chose to answer. Most
survey programmes treat it as a statistic about customers. The gap between those
two things is usually larger than any real change in service quality — which is
why CSAT moves for reasons nobody can explain, and why it so often fails to
predict churn.

## Diagnose before redesigning

| Symptom | Likely cause |
| --- | --- |
| CSAT is high, churn and complaints are rising | Non-response bias; the unhappy majority never answered |
| Score jumped with no operational change | Survey timing, channel, or scale changed |
| Scores differ by team but so do response rates | You are comparing samples, not teams |
| Agents' scores are suspiciously high | Agents influence who gets surveyed |
| Almost all responses are 1s and 5s | Self-selected response; the mean is meaningless |
| Nobody acts on it | You collected a number and no verbatims |

## Step 1: pick the right instrument

| Instrument | Measures | Use for | Do not use for |
| --- | --- | --- | --- |
| **CSAT** | Satisfaction with a specific interaction | Transactional support quality | Relationship health, loyalty |
| **CES** | Perceived effort to get resolved | Friction, self-service, process design | Emotional response, agent quality |
| **NPS** | Stated likelihood to recommend the *company* | Relationship / brand health | Judging an individual interaction or agent |

**NPS after a support contact is the most common mis-specification in CX.** A
customer's willingness to recommend your company is driven mostly by the product,
price, and their overall history — not by whether one agent was helpful. Using it
transactionally holds agents responsible for things they do not control, and adds
so much noise that real signal disappears. If you must report NPS, keep it as a
separate relationship survey on its own cadence.

**CES is under-used and often the most actionable**, because effort is something
process design can actually reduce. When the goal is "make support less painful"
rather than "score agents", it is usually the better instrument.

## Step 2: fix solicitation before anything else

**Nobody may choose who gets surveyed.** If agents can trigger, suppress, or
influence survey sends, the programme is measuring agent selection and nothing
else. This is not a minor bias — it is fatal, and it is common.

Send automatically to a **random sample** of eligible contacts, or to all of them.
Define eligibility explicitly and apply it uniformly:

- Which channels, which contact types, which languages.
- Whether internal-only or auto-closed contacts count.
- Frequency capping per customer, so heavy contactors aren't surveyed weekly.

Excluding spam and auto-closed contacts is legitimate. Excluding transfers,
escalations, or long conversations is not — those are the interactions most likely
to have gone badly.

## Step 3: choose a scale and then leave it alone

- **5-point CSAT** is the workhorse. Report **top-2-box** (the two most positive
  responses) rather than the mean; means on ordinal scales imply arithmetic the
  scale does not support.
- **Binary (thumbs up/down)** raises response rate and loses granularity. A
  reasonable trade when the goal is volume of signal rather than precision.
- **1–10** invites cultural response bias and adds little over 5 points.
- **Avoid a neutral midpoint** if you want a decision; include one if you want an
  honest distribution.

**A scale change breaks the time series permanently.** There is no valid
conversion. If you must change, run both in parallel for a period and report the
break explicitly in every chart thereafter. Treat this as a one-way door.

## Step 4: decide when to ask, and know what that decides

- **Immediately after the interaction** measures the interaction: agent, tone,
  clarity. Higher response rate, and it captures relief rather than outcome.
- **After resolution (24–72h)** measures whether the fix worked. Lower response
  rate, higher business relevance.

Both are valid. **They are not comparable**, and averaging them produces a number
that means nothing. Pick one per programme and document it.

Ask on the **channel of the interaction**. Emailing a survey to someone who
contacted by chat changes both the response rate and who responds.

## Step 5: write questions that don't lead

- One question, one construct. "Was the agent friendly and knowledgeable?" cannot
  be answered when they were one and not the other.
- No leading stems. "How helpful was our excellent support team?" is not a
  question.
- Put the rating question first. Anything before it primes the answer.
- **Always include an open verbatim field.** It is where the actionable content
  is; the score is a tripwire that tells you to go read them.
- Two questions is a good survey. Five is a worse one.

## Step 6: measure your response bias

This is the step almost everyone skips, and it is the one that determines whether
the score means anything.

```bash
node scripts/response-bias.mjs contacts.jsonl
```

The input must include **non-respondents** — a file of survey responses cannot
measure response bias, which is precisely why survey tools never show you this.
Export all eligible contacts with a `responded` flag plus any covariates you
observe for everyone: channel, handle time, message count, agent, repeat contact.

**Arguments**

- `--covariates <list>` — restrict which fields are tested. Default: all scalars.
- `--min-group <n>` — suppress statistics below this group size. Default 30.
- `--json` — machine-readable output.

It reports the **standardised mean difference** for numeric covariates and
response rate per level for categorical ones. |SMD| > 0.1 is the conventional
threshold for meaningful imbalance. It also flags a bimodal score distribution,
which is the fingerprint of self-selected response.

Method and interpretation: [references/bias-and-sampling.md](references/bias-and-sampling.md).

**What a clean result does and does not buy you.** Balanced covariates mean the
sample is not obviously skewed on the things you can see. It cannot rule out bias
on the thing you care about — customers with strong opinions respond more, and
sentiment is unobservable for non-respondents by construction. Balance raises
confidence; it never establishes representativeness.

## Step 7: compare fairly, or don't compare

Comparing CSAT across teams, channels, or periods is only valid when response
rates are comparable. A team with a 30% response rate and one with 10% are
different samples, and the difference in their scores may be entirely sampling.

Options, in order of rigour:

1. **Report response rate beside every score.** Cheapest and most honest.
2. **Weight** responses to match the contact population on observable covariates.
3. **Restrict** comparison to segments with similar response rates.
4. **Compare within-segment over time** rather than between segments.

Never rank agents on raw CSAT without accounting for contact mix. Agents handling
escalations and refusals will score lower for reasons that have nothing to do with
how they handled them.

## Step 8: sample size, honestly

Same arithmetic as any proportion. For a top-2-box rate `p` from `n` responses,
the 95% interval is roughly `±1.96·√(p(1−p)/n)`:

| n responses | ±95% CI at p = 0.85 |
| --- | --- |
| 30 | ±13 pp |
| 100 | ±7 pp |
| 400 | ±3.5 pp |
| 1,000 | ±2.2 pp |

At small `n`, use a Wilson interval — it is asymmetric and honest near the
boundary. And note that **this only covers sampling error**. If your sample is
biased, a bigger sample gives you a tighter interval around the wrong number,
which is worse than a wide interval around it.

## Present results to the user

1. **Response rate first, then the score.** A score without its response rate is
   not a finding. Below ~30%, say plainly that non-response bias dominates.
2. **Whether the sample is representative** on the covariates tested, and which
   ones are imbalanced. Name what each imbalance means — "email customers are 6×
   more likely to respond, so this is largely an email score".
3. **Distribution, not just the mean.** If responses are bimodal, report top-box
   and bottom-box rates and say the mean is misleading.
4. **The confidence interval**, in plain terms, for any segment comparison.
5. **Verbatim themes.** This is the actionable output. If you only report the
   number, nothing will change.
6. **What you cannot conclude** — cross-segment comparisons at unequal response
   rates, agent rankings without contact-mix adjustment, trends across a scale or
   timing change.

## Troubleshooting

**CSAT is high but customers are churning** — check response bias first. This is
the classic signature of a self-selected sample.

**The score changed sharply with no operational change** — look for a change in
survey timing, channel, scale, wording, or eligibility before looking for a
service explanation.

**One team is always top** — check their response rate and contact mix. If either
differs, the ranking is an artifact.

**Response rate is falling** — survey fatigue, frequency capping absent, or the
survey moved off the interaction channel.

**Everyone scores 1 or 5** — expected under self-selection. Report the
distribution and stop using the mean.
