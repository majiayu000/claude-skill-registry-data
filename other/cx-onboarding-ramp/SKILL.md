---
name: cx-onboarding-ramp
description: Use to measure how long new support agents take to reach proficiency and where their ramp stalls, so training and nesting can be targeted. Trigger for "how long until new hires are productive", "time to proficiency", "how is the new cohort doing", nesting or ramp design, comparing training cohorts, or a new hire being assessed before they have had time to ramp.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# New-hire ramp

Two questions, and they are usually conflated: **how long does it take a new agent to
reach proficiency**, and **is this particular new agent on track**. The first is a
cohort analysis; the second is an individual judgement that depends entirely on having
done the first.

Without a measured ramp curve, "on track" means whatever the team lead feels, and new
hires get assessed against the tenured average from week two.

## Define proficiency before measuring time to it

Pick the definition deliberately and state it. Options, none of which is uniquely
correct:

- **Quality-based** — sustaining the tenured median QA score. Best where quality is the
  binding constraint.
- **Throughput-based** — handling volume at the tenured median rate.
- **Autonomy-based** — escalation and assistance rate falling to the tenured level.
  Often the most operationally meaningful and the least instrumented.
- **Composite** — all three within a band. Most defensible, hardest to hit.

**Require it to be sustained.** A single good week is noise, particularly on the
handful of evaluations a new agent has. "Four consecutive weeks at or above the
threshold" is a reasonable rule; state whichever you use.

**Anchor the clock explicitly** — from hire date, from end of classroom training, or
from first live contact. These differ by weeks and are frequently mixed up between two
reports of the same programme.

## Build the curve, not the average

Plot the metric against tenure, by cohort. What to look for:

- **The plateau point** — where the curve flattens. That is the ramp length, and it is
  usually longer than the training plan assumes.
- **The plateau level** — if a cohort flattens below the tenured median, that is a
  training or selection finding, not a ramp finding. It will not fix itself with time.
- **The stall** — a common shape is fast early improvement, then a plateau well before
  proficiency. The stall point usually marks a specific capability nobody taught: a
  system, an escalation path, or a class of contact.
- **Variance within the cohort**, not just its mean. High variance means the ramp
  depends on who happened to mentor them, which is a process finding.

## Beware what the early data actually is

Three biases all point the same way — they make new hires look better than they are —
and they invalidate naive ramp curves:

**1. Easy-work assignment.** New agents are usually given simpler contacts, so their
early scores reflect the work, not their capability, and the curve looks flat when they
are actually improving. **Control for contact mix across the ramp** or the analysis
measures the assignment policy.

**2. Survivorship.** Agents who leave or are managed out during ramp disappear from the
cohort, so later weeks contain only those who did well. Track the cohort as a fixed set
from day one and report attrition explicitly; a curve computed on survivors will always
rise.

**3. Sample size.** A new agent has very few evaluations. At n=4, the 95% interval on a
score is about ±29 points — wide enough that any two new hires are indistinguishable
and any week-to-week movement is noise. **Never rank a cohort in its first weeks**, and
never open a performance conversation on a ramp score without the interval attached.

Also check **coverage**: new hires are often evaluated at a higher rate than tenured
agents. Good practice, but it means their scores are more precise, not that they are
more scrutinised for cause — and it needs saying if anyone compares.

## Cohort comparison

Comparing cohorts is how you learn whether a training change worked. It is only valid
if you hold the rest constant:

- **Same definition of proficiency and same clock anchor.**
- **Same scorecard version.** A rubric change between cohorts makes the comparison
  meaningless — the most common error here.
- **Similar work mix and channel assignment.**
- **Account for the environment.** A cohort that ramped during a product launch or a
  volume spike had a different job.

With realistic cohort sizes — often under twenty — differences of a few days in time to
proficiency are noise. Say so rather than attributing them to the training change.

## The output that gets used

- **Ramp length**, with the definition, and the interval around it.
- **The stall point and what it is**, which is the actionable finding: a specific
  capability to add to training or nesting.
- **A per-week expectation band**, so leads can tell on-track from behind without
  guessing. This is the deliverable most teams actually want, and it is cheap once the
  curve exists.
- **The tenure profile of the team**, which explains a surprising share of team-level
  score movements. A team that hired six people last month will see its average fall
  for reasons that have nothing to do with quality management — and knowing that
  prevents a pointless investigation.

## Present results to the user

1. **Definition and clock anchor**, stated first.
2. **The curve by cohort**, with cohort sizes and attrition.
3. **Ramp length and plateau level**, with intervals, and whether the plateau reaches
   the tenured median.
4. **The stall point**, and what capability it corresponds to.
5. **Mix control** — whether contact assignment was held comparable across the ramp, or
   an explicit statement that it was not.
6. **The per-week expectation band**, for operational use.
7. **What cannot be concluded** — individual comparisons at low n, cohort differences
   inside the noise, and any scorecard change that breaks comparability.
