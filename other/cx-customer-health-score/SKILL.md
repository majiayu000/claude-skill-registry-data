---
name: cx-customer-health-score
description: Use to design or audit the support contribution to a customer health score, so the score predicts something instead of averaging weakly-related signals into a colour. Trigger for "build a customer health score", "add support signal to health scoring", "our health scores don't predict churn", red/amber/green account scoring, or a health score nobody trusts.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Support signal in a customer health score

Most health scores are a weighted average of whatever was available, with weights
someone chose in a meeting, rendered as red/amber/green. They feel useful and predict
very little — and because nothing ever tests them, the weights survive for years.

This is about the support contribution specifically, and about the one property that
makes any of it worth doing: **the score has to be validated against an outcome.**

## Validate first, design second

Before adding a single support signal, establish what the score is *for*:

- **Churn or non-renewal** — the usual claim.
- **Expansion likelihood** — a different score with different inputs. A score cannot do
  both; the same account can be highly likely to renew and highly unlikely to expand.
- **Intervention triage** — which accounts a CSM should look at this week. Needs
  precision and lead time, not calibration.

Then test candidate signals against that outcome on historical data:

> For accounts that churned, what did this signal look like 90 days before, compared
> with accounts that renewed?

A signal with no separation at useful lead time does not belong in the score, however
intuitive it is. **Most candidate signals fail this test**, and cutting them is the
main way a health score becomes useful.

Report the discriminating power of each input, not just the final score's. A score with
one strong input and six decorative ones should be one input, and saying that is more
valuable than tuning the weights.

## Which support signals actually carry information

In rough order of usefulness, and all of them need testing on your own data:

- **Repeat and unresolved contacts.** The customer telling you twice. Consistently the
  strongest support-side input.
- **Unkept commitments.** Promises in transcripts that did not happen. Strong, and
  requires reading conversations rather than aggregating fields.
- **Escalations and complaints**, weighted by end-to-end time from the customer's first
  contact.
- **Service attainment against the account's own tier**, not the org average.
- **Sentiment trajectory** — direction across contacts, not level.
- **Champion contact going quiet** after a period of engagement.

Signals that look useful and usually are not:

- **Raw contact volume.** Ambiguous in both directions and dominated by account size and
  usage. If you use it, normalise by seats or usage, and expect the direction to be
  weaker than you assume.
- **CSAT alone.** Response rates are low and self-selected; the accounts most at risk
  are the least likely to answer.
- **Ticket count with no resolution context.** Counts effort, not outcome.

## Design rules that keep it honest

**Composite scores hide the thing you need.** An account can reach amber through six
mediocre inputs or through one severe unresolved failure, and those need different
responses. Always surface **the top contributing factors alongside the score**; a
number with no reason attached gets ignored, then gamed.

**Do not average across dimensions that fail independently.** Support experience,
product usage and commercial engagement are separate axes. Averaging them lets healthy
usage mask a support disaster. Report them separately, and let a severe score on any
one axis raise the overall flag rather than being diluted.

**Prefer a small number of trip-wires to a continuous score.** "Two unresolved repeat
contacts in 30 days" is actionable, explainable and hard to argue with. A score of 62
is none of those. Continuous scores are for ranking a review queue; trip-wires are for
deciding something.

**Set thresholds from the outcome data**, not from round numbers. Pick the threshold
that gives the precision your intervention capacity can absorb, and report the expected
volume — the same forecast an alert needs.

**Include the base rate.** At a low churn rate, even a good score's "red" bucket is
mostly accounts that will renew. State the precision so nobody reads red as doomed.

## Auditing an existing score

When the complaint is "our health scores don't predict churn", check in this order:

1. **Has it ever been validated?** Usually not. Run the retrospective test before
   anything else; it frequently ends the investigation.
2. **Are the weights doing anything?** Compare the full score against its single
   strongest input. If they perform the same, the score is one input plus decoration.
3. **Is any input stale or broken?** A field that stopped being populated when a tool
   changed will quietly sit at its default and drag every score toward the middle.
4. **Is it self-fulfilling?** If CSMs work the red accounts and red accounts then
   churn less, the score's apparent accuracy is suppressed by the intervention it
   triggers. This is a *good* outcome and it makes naive validation look like failure —
   account for the intervention, or you will conclude a working score is broken.
5. **Does anyone act on it?** A score with no attached motion cannot be evaluated and
   should be retired rather than refined.

## Guardrails

- **A health score is not a service-level decision.** Do not use it to deprioritise
  support for low-scoring accounts. In regulated sectors, differential service on this
  basis is a conduct issue, and in any sector it is a self-fulfilling prophecy.
- **Do not include protected characteristics or proxies for them**, and do not include
  ability-to-pay signals in a score that influences service quality.
- **Do not show internal health scores to customers**, and write them expecting that
  one day one will leak. "At risk — poor support experience" is defensible; a
  pejorative label about the customer is not.
- **State the precision wherever the score is displayed.** A red flag read as certainty
  produces the wrong conversation.
- **Joining support, product and billing data** creates a personal-data profile none of
  the sources held. Flag purpose and retention.

## Present results to the user

1. **What the score is for**, and the outcome it was validated against.
2. **Per-input discriminating power** at a useful lead time, with the inputs that failed
   named and recommended for removal.
3. **Whether the composite beats its best single input.** If not, say so plainly.
4. **The axes kept separate**, with the rule for how a severe single-axis score escalates.
5. **Trip-wires with thresholds set from data**, plus the expected volume each produces.
6. **Precision at the real base rate**, for every threshold shown.
7. **The intervention confound**, if CSMs act on the score, and how you accounted for it.
8. **What could not be validated**, and what data would settle it.
