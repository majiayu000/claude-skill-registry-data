---
name: cx-cost-of-poor-quality
description: Use to quantify what support quality failures cost — rework, credits, escalation handling, complaints and churn — with the causal limits stated. Trigger for "what do our quality failures cost", "cost of rework in support", "business case for improving quality", "how much is bad support costing us", or a quality investment that needs a number attached.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# The cost of poor quality

Quality programmes are funded on faith and cut on arithmetic. The counter-argument needs
a number, and the number is buildable — but the version that gets built is usually
indefensible, because it multiplies a failure rate by an average customer value and
presents the result as savings.

This is the backward-looking counterpart to a forward-looking risk analysis: what has
already been spent because work was done wrong, rather than what might yet be lost.

## Four cost layers, in descending order of defensibility

Build them separately. The first two are close to countable; the last is an estimate
with wide bounds. Presenting them as one figure means the whole number inherits the
weakest layer's credibility.

**1. Rework — the most defensible and most often ignored.** A contact handled wrongly
produces another contact. That second contact has a real, measurable cost:

```
rework cost = repeat contacts attributable to a first-contact failure
              × the allocated cost of a contact
```

You already have repeat-contact measurement and a cost-per-contact allocation. Restrict to
repeats where the *first* contact failed — not every repeat is a quality failure — and use
the cost of the contacts actually involved rather than a blended average, since repeats
skew longer and more complex than average.

**2. Direct redress.** Credits, refunds and goodwill paid because of a handling failure,
as distinct from redress owed for a product or billing defect. Countable if reason codes
exist, and the split matters: only the handling-caused portion belongs here.

**3. Escalation and complaint handling.** The internal cost of the machinery a failure
sets off — escalation handling, complaint investigation, executive time, and in regulated
sectors formal complaint processing, which is expensive per case. Estimate from case
volume × measured handling time, and include the second and third teams a case touches.

**4. Churn and revenue loss.** The largest claimed number and the weakest. It requires a
causal estimate you almost certainly do not have. Treat it as a range built from an
uplift calculation, and label it as an estimate wherever it appears.

## Do not multiply a failure rate by a customer's value

This is the specific error that discredits these analyses:

> "We had 4,000 low-scoring interactions and average customer value is £900, so poor
> quality cost us £3.6m."

Every step is wrong. A low QA score is not a lost customer. Most customers who
experience a poor interaction stay. And the score is measured on a *sample*, so the count
is not the population.

What is defensible instead:

- **Uplift, not raw rate.** Among customers who experienced a quality failure, what share
  churned, compared with matched customers who did not? Use the difference.
- **Match on the confounders.** Customers who experience failures are not a random sample —
  they contact more, have harder problems, and are often larger accounts.
- **Scale from the sample to the population honestly.** If QA covers 3% of contacts, say
  the estimate is extrapolated from a 3% sample, and give the interval.
- **Partial loss, not total.** Reduced spend is far more common than departure.

## Rework is where the argument is actually won

Layer 1 tends to be both the largest countable cost and the easiest to act on, and it is
usually absent from these business cases entirely.

Rank rework by the **failure mode that caused it**, not by volume:

- Wrong information given
- Incomplete resolution — the answer was right and omitted a condition or a next step
- No resolution — deflected or closed without addressing it
- Process not followed, requiring a redo
- Handoff failure, requiring the customer to repeat themselves

Each has a different fix and a different owner, and "incomplete resolution" is
consistently one of the largest and least visible: the answer was not wrong, so QA passes
it and the customer comes back anyway. **A quality programme that only measures
correctness will not see it.**

## The counterfactual is the hard part

"Improving quality would save this" is a causal claim, and the honest position is that
observational data does not support it.

- **What the analysis supports:** the cost already incurred, and that failures are
  associated with higher downstream cost by a measured margin.
- **What it does not:** that a specific intervention recovers that cost.

If someone wants the second claim, propose the design rather than a stronger reading:
fix the failure mode for a random subset and compare downstream cost. It is usually
cheaper to run than the analysis was to argue about.

Also net off the cost of the improvement. A programme that costs more than the rework it
removes is worth knowing about before it is funded.

## Traps

- **Double counting.** A failure that produced a repeat contact *and* a credit *and* an
  escalation is one failure with three cost lines — legitimate, as long as the lines are
  not also summed into a per-failure average that is then multiplied by failure count.
- **Counting all repeat contacts as rework.** Many are legitimate follow-ups.
- **Ignoring the cost of quality itself.** QA, coaching and calibration have a cost.
  Cost-of-poor-quality is one side of a comparison, not the whole case.
- **Using the org-average contact cost** for rework, when repeats are longer than average.
- **Assuming a QA score maps to customer experience.** It measures conformity to a rubric.
  Where the rubric has not been validated against an outcome, the link between score and
  cost is assumed rather than shown — say so.
- **Sampling bias in the failure population.** If QA over-samples low scores or disputed
  cases, the failure rate is not the population rate.

## Guardrails

- **Never present the four layers as one number.** State each with its own confidence, and
  put the weakest last rather than folding it into the headline.
- **Do not attribute the cost to named agents.** These are process and system costs, and
  building an individual-cost figure from a handful of evaluations is both statistically
  unsound and a poor use of the analysis.
- **Do not use this to justify cutting service.** The most common misuse: a cost-of-quality
  number repurposed as an argument for lower handling standards, which raises rework.
- **Cite ids and aggregates.**

## Present results to the user

1. **The four layers separately**, with the method and confidence for each and the churn
   estimate last.
2. **Rework in detail** — volume, the cost basis used, and the ranked failure modes with
   owners. The actionable core.
3. **The uplift calculation** for any churn claim: matched comparison, margin, interval,
   and what was matched on.
4. **Extrapolation stated** — QA coverage, and the interval on scaling the sample to the
   population.
5. **The cost of the quality programme itself**, so the comparison is two-sided.
6. **What is not claimed** — that improvement recovers the cost — plus the experiment that
   would establish it.
