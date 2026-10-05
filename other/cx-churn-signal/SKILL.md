---
name: cx-churn-signal
description: Use to find cancellation, downgrade and switching intent in support conversations, and to be honest about how much of your churn support can actually see. Trigger for "which customers are at risk of leaving", "find cancellation intent", "customers asking how to export their data", "top reasons customers asked to close their account", competitor mentions, or building a churn early-warning signal from support data.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Churn signal in support conversations

Support holds the clearest churn language a company has access to: customers say
they are leaving, ask how to get their data out, and name the competitor. That makes
it tempting to build a churn early-warning system on it.

It works, within a boundary that has to be stated first.

## Most churn never appears in support

**The majority of customers who leave never contact you about it.** They stop using
the product, the subscription lapses, and the first record of the decision is a
billing event.

So the first number to produce is not accuracy. It is coverage:

> Of customers who churned in the last N months, what share had **any** support
> contact in the window before it?

That single figure bounds everything the signal can ever do. If 30% of churners
contacted support, a perfect detector catches at most 30% of churn — and the 70% it
cannot see are not a random 70%. Silent churners skew toward low-engagement,
low-touch, and often lower-value accounts, so a support-derived churn model is
systematically better at the customers who talk to you and blind to the ones who
disengage.

Report coverage before any performance metric, and never let the signal be presented
as a complete churn model. It is one input.

## Three signal classes with opposite error profiles

**1. Explicit intent** — asking to cancel, close, downgrade, or not renew. High
precision, low recall, and **usually too late to act on**. By the time someone asks
how to close the account, the decision is generally made. Still worth capturing for
reason coding.

**2. Implicit intent** — asking how to export data, questions about contract notice
periods or termination terms, procurement asking for a data-processing agreement to
be terminated, sudden interest in a competitor's integration, "we're evaluating
alternatives". Lower precision, materially better lead time. **This is where the
usable signal is.**

**3. Behavioural** — a contact-frequency spike followed by silence, repeated
unresolved contacts on the same issue, escalation followed by nothing, sentiment
trajectory declining across several conversations. Weakest per instance, and the
only class that catches customers who never say anything about leaving.

Build and evaluate the three separately. Blending them into one score hides that
class 1 is a lagging indicator and class 3 is the only leading one.

## Lead time is the metric, not accuracy

A detector that fires the day someone cancels is a very accurate, completely useless
detector.

For every signal, report the **distribution of lead time** between the signal and the
churn event. Then state the minimum lead time your retention motion actually needs —
if a save play takes two weeks to execute, anything under two weeks of warning is
reporting, not early warning.

Rank signals by usable lead time × precision, not by precision alone.

## The base rate will ruin a naive classifier

Churn is rare per period. At a 2% monthly churn rate, a detector with 90%
sensitivity and 90% specificity produces roughly one true positive for every five
false positives — the precision is about 15%, not 90%.

So:

- **Compute precision at your actual base rate**, and state it. Sensitivity and
  specificity quoted alone are how a useless detector gets shipped.
- **Report the expected volume** the signal will produce per week against the capacity
  of whoever handles it. This is the same forecast a monitor needs, and skipping it is
  why churn alerts get muted.
- **Prefer a small, high-precision list** over a broad risk score nobody works.

## Validate against outcomes, not sentiment

The signal must be labelled against **what actually happened** — did the account
churn or downgrade — which means joining support data to billing or CRM outcomes. If
you cannot make that join, you cannot validate the signal, and you should say so
rather than validating against a proxy.

Sentiment is not an outcome. A frustrated customer who stays and a calm customer who
leaves are both common, and a model trained on sentiment learns to detect
frustration, which you already knew about.

**Watch the direction of the confound.** Contacting support correlates with
engagement, and engaged customers often churn *less*. In several businesses, "has
contacted support" is associated with **lower** churn overall. That means a raw
"contacted support" feature can point the wrong way, and it means the comparison has
to be within-contactor: at-risk versus not, among customers who contacted, not
contactors versus everyone.

## Reason coding is the durable output

The at-risk list decays; the reason taxonomy compounds.

For explicit and implicit intent, code **why** — price, a missing capability, a
competitor, reliability, a specific unresolved failure, an organisational change at
their end, or a reason outside your control. Then rank reasons by the revenue behind
them.

Two things this needs to be honest:

- **Separate what you can influence from what you cannot.** A customer whose company
  was acquired is not a product problem, and including them inflates every actionable
  category.
- **The stated reason is not always the real one.** Price is the socially easy answer.
  Where you have both the stated reason and the conversation history, note where they
  disagree, and report the disagreement rate rather than trusting either alone.

## Guardrails

- **This is an input to a human review, not an automated retention action.** Do not
  trigger a save offer, a discount, or an outbound contact automatically from a
  detector with this precision.
- **Never route a complaint or a vulnerable customer into a retention push.** Someone
  in the middle of an unresolved failure, in financial difficulty, or showing
  vulnerability signals needs the failure fixed, not a discount. Build the exclusion
  before the signal.
- **Do not degrade service to retained-risk accounts, or prioritise on ability to
  pay** in a way you could not defend. In regulated sectors, differential treatment on
  this basis is a conduct issue.
- **Do not build a pressure system.** A detector that flags people for aggressive
  retention contact damages the relationship and, where cancellation is a right,
  obstructing it is a compliance problem.
- **Cite conversation ids; do not paste transcripts.** Churn analyses circulate widely.
- **Linking support conversations to billing outcomes creates a richer personal-data
  record** than either source alone. Flag the purpose and retention question; do not
  decide it.

## Present results to the user

1. **Coverage** — the share of actual churners who had any support contact. First,
   before anything else, because it bounds every other number.
2. **The three signal classes separately**, each with volume, precision at the real
   base rate, and lead-time distribution.
3. **Whether outcome labels were available.** If not, say the signal is unvalidated
   and stop short of a risk score.
4. **The at-risk list**, short and high-precision, with the evidence id per account
   and the reason code.
5. **Reason ranking by revenue behind it**, split into influenceable and not.
6. **The confound check** — whether contacting support is associated with more or less
   churn in your data.
7. **What this cannot see** — silent churn, and which customer segments that omission
   concentrates in.
