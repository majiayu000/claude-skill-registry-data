---
name: cx-onboarding-friction
description: Use to find the activation blockers visible in support contacts from new customers, before they show up in retention numbers months later. Trigger for "why aren't new customers activating", "what do new customers contact us about", onboarding drop-off, time-to-value analysis, first-90-days support experience, or a retention problem that traces back to activation.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Onboarding friction in support contacts

New customers contact support about the things that are stopping them getting started.
That makes the first weeks of a customer's support history the most direct evidence
available of what blocks activation — and it arrives months before the retention curve
shows the consequence.

Two things make this analysis different from ordinary contact-driver work, and both
change the method.

## New-customer contacts are not the same population

**A contact from a new customer is usually a blocker; a contact from an established
one is usually an exception.** The same category means different things at different
tenures — "how do I invite a user" is onboarding friction in week one and an edge case
in year two.

So:

- **Segment by tenure, in short buckets** early on: days 0–7, 8–30, 31–90. A single
  "new customer" bucket of 90 days blurs the week-one cliff, which is where most of
  the signal is.
- **Never compare new-customer contact rates to the org average.** New customers
  contact more; that is expected and not a problem in itself.
- **Compare cohorts to each other** — this month's new customers against last quarter's
  — because the interesting question is whether onboarding is getting better.

## Contacting support is a sign of *effort*, and silence is ambiguous

The customer who contacts support is trying. The one who hit the same blocker and
silently stopped is the more expensive case, and they are invisible here.

That means support data over-represents the persistent and under-represents exactly the
customers who churn fastest. Two consequences:

- **Pair support contacts with product activation data** wherever you can. A blocker
  that generates few contacts but sits at a high drop-off step is more important than a
  chatty one that everyone gets past.
- **State the coverage** — what share of non-activating customers ever contacted support.
  If it is low, this analysis names *some* blockers and cannot claim to be the ranked
  list of all of them.

## The classification that makes this actionable

Ordinary contact-driver taxonomy names topics. For onboarding, classify by **what kind
of failure it is**, because each has a different owner:

- **Missing capability** — they need something the product does not do.
- **Discoverability** — the product does it and they could not find it. The most common,
  the cheapest to fix, and the one most often misread as a training problem.
- **Setup complexity** — technical steps beyond what the buyer can self-serve
  (integrations, DNS, SSO, data import). Look for where these stall rather than fail.
- **Data migration** — getting their existing data in. Reliably underestimated at
  purchase and a frequent silent killer.
- **Permissions and access** — someone internal has to approve or provision something.
  Not your product's fault and entirely your problem, because it stalls the clock.
- **Expectation mismatch** — they bought something that does not do what they thought.
  This is a sales or marketing finding, and it should be routed there rather than
  absorbed by support.
- **Wrong-fit** — they should not have bought. Worth counting honestly; a rising rate
  here is a targeting problem.

Report the mix. An onboarding problem that is 60% discoverability is a very different
programme from one that is 60% expectation mismatch.

## Measure time, not just volume

Volume tells you what people hit. Time tells you what it costs.

- **Time-to-first-value**, and the gap between cohorts who contacted support and those
  who did not. If contacting support *shortens* time to value, support is a working part
  of onboarding and should be resourced as such rather than minimised.
- **Stall duration** — how long between a blocker being raised and the customer
  progressing. A blocker that adds three days is different from one that adds three
  weeks even at the same volume.
- **Contact latency** — how long a customer struggled before asking. Long latency on a
  common blocker means many others hit it and never asked.
- **The unresolved tail** — new customers whose blocker was never resolved and who then
  went quiet. Cross-reference activation status. This small list is the most valuable
  output of the analysis and the easiest to act on.

## Traps

- **Counting onboarding contacts as a support cost to reduce.** Suppressing them by
  making support harder to reach makes activation worse. If the goal is fewer
  onboarding contacts, the mechanism has to be removing the blocker, not the channel —
  and the guardrail is activation rate, not contact volume.
- **Attributing everything to the customer's setup.** "They configured it wrong" is
  usually a discoverability finding wearing a blame hat.
- **Ignoring the assisted cohort.** Customers with a dedicated onboarding manager
  generate few tickets and hit the same blockers. Their friction is in call notes and
  internal threads, not the queue, and excluding them biases the ranking toward
  self-serve segments.
- **Seasonal cohorts.** Customers who signed up during a promotion, an event, or a
  competitor's outage are not comparable to steady-state cohorts.
- **Reading a mid-funnel improvement as success** when the earlier step got harder and
  fewer people reached it.

## Guardrails

- **This names blockers; it does not size them.** Support-visible frequency is not
  population frequency. Say which claim you are making.
- **Route findings to the owner** — product, docs, sales, provisioning — rather than
  filing them all as support improvements. Most onboarding friction is not support's to
  fix.
- **Cite ids and counts; do not paste transcripts.** New-customer conversations often
  contain implementation detail and credentials-adjacent material.

## Present results to the user

1. **Coverage** — what share of non-activating customers contacted support, and therefore
   what this analysis can and cannot rank.
2. **Contacts by tenure bucket**, cohort over cohort, so the direction is visible.
3. **The failure-type mix**, not just the topic list, with an owner per type.
4. **Time costs** — time-to-value with and without support contact, stall duration,
   contact latency.
5. **The unresolved-and-went-quiet list**, by id, cross-referenced against activation.
   The most actionable output.
6. **Expectation-mismatch and wrong-fit volumes**, routed to sales and marketing rather
   than buried in a support report.
7. **What product data would settle** that support data cannot.
