---
name: cx-redress-consistency
description: Use to audit whether similar customers with similar failures received similar redress, and to find variation that could not be defended. Trigger for "are our refunds consistent", "do we compensate similar cases the same way", "audit our goodwill decisions", redress fairness review, customers who escalate getting more, or a complaint that someone else was treated better.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Redress consistency

Two customers, same failure, same circumstances, different outcomes. It is one of the
few CX findings that is indefensible on its face — and unlike most conduct questions, it
is measurable from data most firms already hold.

This audits **outcomes for consistency**. Designing the framework that produces the
outcomes is a different job; without a framework, expect the variation to be large and
the finding to be that one is needed.

## Compare like with like, or find nothing

Raw variation in redress amounts is meaningless — cases genuinely differ. The audit only
works once you have defined comparable groups.

Build the comparison on:

- **The failure type**, at the level of cause rather than category.
- **The loss** — the actual detriment, where recorded. Two customers with the same failure
  and different losses should get different amounts.
- **Whether redress was owed or discretionary.** These follow different rules and pooling
  them destroys the analysis. Owed redress should show *very* little variation for a given
  loss; goodwill legitimately shows more.
- **Product, market and period**, since policy changes over time.

Then look for variation *within* those groups. Between-group variation is expected;
within-group variation is the finding.

**If the data does not let you group by loss, say so.** Without it you can still detect
gross disparities and cannot distinguish justified variation from unjustified. That is a
useful, limited result — report it as limited.

## The dimensions to test

For each comparable group, test whether outcome varies with:

- **Escalation intensity** — how hard the customer pushed, how many contacts, whether they
  threatened to leave, complain or go to a regulator. **The most important test in this
  audit.** A system that pays more to whoever escalates loudest is a system that teaches
  escalation, and it systematically under-compensates customers least able or willing to
  advocate for themselves — which is a fairness problem before it is a cost problem.
- **Agent and team.** Wide agent-level variation points at an unclear framework or absent
  guidance, not at bad agents.
- **Channel.** Voice customers frequently do better than email customers for the same
  failure, because it is harder to say no in real time.
- **Tenure, value and tier.** Some differentiation may be legitimate and contracted;
  differentiation on inferred value or ability to pay is not.
- **Market and language.** Also check whether the *process* differed, not just the amount.
- **Whether the customer asked.** Redress paid only to those who requested it, where
  something was owed, is usually indefensible — and it is easy to check.
- **Protected characteristics or proxies for them.** Where you lawfully hold the data,
  test it. Where you do not, say you could not test it rather than inferring it from a
  proxy. **A disparity here is not a cost-control finding — it stops being this report and
  becomes an escalation.**

## Measuring it

- **Report the distribution within comparable groups**, not the mean. Spread is the
  subject; a mean hides it entirely.
- **Give both the rate of any redress and the amount given redress.** These fail
  separately: a group might be equally likely to receive something and consistently
  receive less.
- **Use a robust measure of spread** — the interquartile range, or the ratio of an upper
  to a lower percentile — because redress distributions have long tails driven by a few
  large cases.
- **Suppress small cells.** With realistic complaint volumes, most cells are small.
  Report the count, suppress the rate, and do not rank individuals on a handful of
  decisions.
- **Check the interval before concluding a disparity is real.** Redress volumes are low
  and apparent gaps are frequently noise; a difference that does not clear its interval
  is not a finding yet, and saying so protects the ones that are.
- **Look at zero separately.** Cases where nothing was given, in a group where others
  received something, are the most important subset and they disappear into an average of
  amounts.

## What justified variation looks like

Not all variation is a problem, and an audit that treats it all as one will be dismissed.
Legitimate reasons, each of which needs to be *recorded* to count:

- A different loss.
- A different failure despite a shared category label.
- Non-monetary remedy given instead, and accepted.
- Customer declined, or asked for something else.
- Contractual entitlement genuinely differs by product or tier.
- A recorded exception with a stated reason.

**Variation with a recorded reason is defensible. Variation with no recorded reason is
not**, whatever the reason might have been. That makes reason-code completeness the
enabling condition for this whole audit — report it first, because a low completeness
rate is itself the primary finding and it bounds everything else.

## The remediation question

Where the audit finds a group that was systematically under-compensated, the next
question is not analytical:

- **Should the under-compensated cases be topped up?** Frequently yes, and it is a
  compliance and legal determination rather than an operational choice.
- **Does the pattern indicate a wider affected population** who never received anything
  because they never asked? Size it from operational data rather than from the redress
  records, which by construction only contain people who got something.

Flag both. Do not decide either.

## Guardrails

- **Do not rank or discipline individual agents on this.** Wide variation is nearly always
  a framework problem, and turning it into individual performance produces defensive
  under-compensation, which is the worse failure.
- **Do not use the audit to argue for lower redress.** The finding is consistency. A
  consistency audit repurposed as a cost-reduction exercise will land on "pay less", and
  the cases that get cut are the ones where someone was owed.
- **A disparity correlated with a protected characteristic is not a normal finding.**
  Escalate it separately and immediately.
- **Whether under-compensation requires remediation is a compliance and legal
  determination.**
- **Cite ids and aggregates.** Redress records contain payment details and financial
  circumstances.

## Present results to the user

1. **Reason-code completeness**, first. It bounds the whole audit.
2. **The comparability basis** — how groups were formed, and whether loss was available.
3. **Owed and discretionary redress, separately.** Variation in owed redress is the more
   serious finding.
4. **Within-group distributions**, with rate-of-any-redress and amount reported
   separately, using a robust spread measure.
5. **The escalation-intensity test**, called out explicitly — it is the finding most likely
   to be present and most likely to be actionable.
6. **The zero cases** in groups where others received something.
7. **Disparities that clear their intervals**, with the indefensible ones escalated
   separately rather than listed alongside.
8. **The wider-population question** — customers who never asked and may have been owed.
9. **What needs a compliance determination**, and what is a framework fix.
