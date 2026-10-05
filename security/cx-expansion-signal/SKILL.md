---
name: cx-expansion-signal
description: Use to find upgrade, seat-growth and new-use-case signals that customers give support and nobody routes anywhere. Trigger for "find upsell opportunities in support", "customers hitting plan limits", "which accounts are asking about enterprise features", expansion signals from tickets, or support-sourced pipeline.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Expansion signal in support conversations

Customers tell support things they never tell sales. They hit a plan limit, ask
whether a feature exists on a higher tier, mention a new team that wants access, or
ask an integration question that only makes sense if they are about to scale up.

Most of it goes nowhere, because the agent's job is to answer the question and close
the ticket.

The opportunity is real. The risk is specific and worth stating before any of it:
**the customer did not contact support in order to be sold to.** Every false positive
routed to a sales motion spends relationship capital, and a badly-timed approach off
the back of a support ticket does more damage than the missed expansion would have
cost. So this analysis optimises for **precision**, deliberately and at the expense of
recall.

## Signal classes, strongest first

**Capacity and limit signals** — hit a usage cap, seat limit, rate limit, or storage
quota. The strongest class: it is objective, it is in the product data as well as the
conversation, and the customer has already experienced the constraint.

**Access expansion** — a new team, department, region or subsidiary asking for access;
questions about SSO, provisioning, or role permissions at a scale their current plan
does not serve.

**Tier-gated feature interest** — asking whether something exists, where the answer is
"yes, on a higher plan". Strong, but see the frustration test below.

**Procurement and compliance activity** — security questionnaires, DPAs, procurement
forms, legal review, invoicing or PO questions. These signal a formalising
relationship and often precede a larger commitment. Frequently the earliest signal
available, and almost never captured.

**New use case** — asking how to do something outside the pattern they bought for.
Weaker, but the highest-value when it lands, because it changes the account's ceiling
rather than its volume.

**Integration and API questions** at a depth beyond current usage.

## The frustration test

The same sentence is an expansion signal or a churn signal depending on context, and
getting it backwards is the expensive error.

> "I've hit the limit again."

That is a buying signal from a growing account and a cancellation precursor from one
that feels nickel-and-dimed. Before classifying any limit or tier signal as
expansion, check:

- **Is this the first time, or the fourth?** Repeated collisions with the same limit,
  especially after previously raising it, read as a pricing grievance.
- **What is the sentiment trajectory across the account's recent contacts**, not just
  this one?
- **Is there an open complaint, escalation or unresolved failure?** If yes, this is not
  an expansion signal today, whatever the words say.
- **Did they ask about the higher tier, or did the agent tell them about it?**
  Agent-initiated is much weaker evidence.

When the two readings are genuinely ambiguous, classify as ambiguous and route it to
the account owner for a judgement call, not to a sales sequence.

## Hard exclusions

Build these before the detector, not after the first complaint:

- **Any account with an open complaint or unresolved escalation.**
- **Any conversation showing vulnerability, financial difficulty, or distress.**
- **Any account that has given notice**, or asked about cancelling.
- **Any conversation on a regulated topic** where a sales approach would be
  inappropriate or would need its own suitability assessment.
- **Accounts that have opted out of sales contact**, and, where marketing-consent rules
  apply, anyone whose consent does not cover this.

A signal that clears the detector and fails an exclusion should be *dropped*, not
queued. Making the exclusion a soft warning means it will be overridden on a busy day.

## Measure outcomes, not signals

Signal count is a vanity metric. The chain that matters:

```
signals detected -> accepted by the account owner -> qualified -> closed expansion
```

Report conversion at every step, and the **acceptance rate is the diagnostic one**. If
account owners accept fewer than about half of what you send, precision is too low
and they will stop reading the queue — which is the same failure mode as a muted
alert.

Also track a **guardrail metric**: the CSAT, complaint rate and repeat-contact rate of
accounts that received a support-sourced approach, against comparable accounts that
did not. If the guardrail moves the wrong way, the programme is losing more than it
gains, and you need that number before someone asks for it.

Attribution honesty: an account that expanded after a support-sourced flag might have
expanded anyway. Report support-sourced pipeline as *influenced*, and if a clean claim
is needed, the answer is a holdout — withhold a random share of flags and compare —
not a stronger reading of the observational number.

## Traps

- **Agent incentives.** The moment flagging is rewarded, flag volume rises and
  precision collapses. Measure the queue's precision continuously, and never pay
  commission on support-sourced flags.
- **Support contact is not intent.** High contact volume correlates with engagement,
  not with willingness to buy. Do not use raw ticket count as a feature.
- **The person contacting support is often not the buyer.** A support requester may have
  no budget authority and no idea what the contract says. Treat the signal as about the
  *account*, and let the account owner find the right person.
- **Stale signals.** A limit hit six weeks ago has probably been solved, worked around,
  or resented. Put an expiry on the queue.
- **Duplicate signals** across several contacts from the same account inflate the
  count. Deduplicate to the account.

## Guardrails

- **Never sell inside an unresolved support conversation.** The ticket is resolved
  first; the commercial conversation is separate, and ideally with a different person.
- **Detection is not permission to contact.** Marketing and privacy rules govern
  outbound contact regardless of how the signal was generated. Flag that; do not
  assume it.
- **Do not repurpose support conversation content into a sales pitch.** Quoting a
  customer's own words about their internal plans back at them, in a sales email,
  reliably lands badly.
- **Cite ids; do not paste transcripts** into a pipeline review.
- **Mining support conversations for commercial signal may exceed the purpose the data
  was collected for.** That is a real question for whoever owns data protection —
  raise it rather than resolving it.

## Present results to the user

1. **The exclusion rules applied**, and how many signals they removed. State this first;
   it is what makes the queue safe to work.
2. **Signals by class**, with the frustration test outcome for limit and tier signals.
3. **The queue itself** — account, signal class, evidence id, date, expiry — short and
   high-precision.
4. **Ambiguous cases separately**, routed for judgement rather than sequencing.
5. **The conversion chain**, with acceptance rate called out as the health metric.
6. **The guardrail metric** — satisfaction and complaint rate of approached accounts
   versus comparable ones.
7. **Attribution stated as influence**, with the holdout design offered if a causal
   claim is wanted.
