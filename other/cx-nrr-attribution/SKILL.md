---
name: cx-nrr-attribution
description: Use when support or CS is being asked to claim a share of net revenue retention, expansion or churn reduction, to work out what can honestly be attributed and what cannot. Trigger for "how much NRR can support claim", "prove support's revenue impact", "attribute retention to CS", support ROI for a board deck, or two teams claiming the same expansion.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Attributing revenue retention to support

Support and CS get asked to justify themselves in revenue terms, usually before a
budget cycle. The request is legitimate. The usual answer — sum the ARR of accounts
that support touched and renewed — is not, and it is transparently not, which is why
these numbers rarely survive their first serious audience.

This skill is mostly about **what you cannot claim**, because the credible version of
the claim is much smaller and much more durable than the one people reach for.

## Why the obvious method fails

**Almost every retained account was touched by support.** In most businesses, support
contact reaches the large majority of customers, so "accounts support touched that
renewed" approximates total renewed revenue. The metric has no discriminating power: it
would look identical if support were excellent or useless.

Three further problems:

- **Selection.** Customers who contact support are more engaged, and engaged customers
  renew more. The correlation exists without support doing anything.
- **Multiple claimants.** Product, CS, sales and support all touch the same retained
  account. If each claims it, the company's attributed retention exceeds its actual
  retention — a real and common outcome that discredits everyone's numbers at once.
- **Reverse causation.** Growing accounts generate more contacts. Contact volume is
  partly an *effect* of expansion, not a cause.

## The honest ladder

Four claim strengths. Use the strongest you have evidence for, and name which one you
are making.

**1. Contribution, unquantified.** "Support resolved 14,000 issues, including 340 on
accounts that renewed at over £100k." True, useful context, no revenue claim. Perfectly
respectable, and better than an inflated number.

**2. Association, with a comparison.** "Accounts with an unresolved escalation churned at
X% versus Y% for matched accounts without one." Requires matching on segment, size,
tenure and usage trend. Supports a directional claim and a defensible order of magnitude.

**3. Influence, with a defined mechanism.** For specific, traceable events — a save
following an escalation, an expansion following a request-shipped notification, a renewal
where the customer named a support recovery. Countable, small, and real. **This is
usually the strongest honest claim available**, and its smallness is the point: it is the
part you can actually defend line by line.

**4. Causal, with a holdout.** Withhold the motion from a random subset and compare.
The only claim that survives a sceptical audience, and it is available far more often
than people assume — request loop-closing, proactive outreach, adoption nudges and save
plays can all be randomised at low cost.

**If you are at rung 1 or 2, say so.** A stated association is more persuasive to a
serious reader than an overclaimed causal number, because the reader can tell the
difference and will discount the whole analysis if they catch one.

## Fix the double-counting before publishing

Agree the rule with the other claimants **before** the number goes anywhere:

- **Single-touch by convention** — one team gets the account. Simple, arbitrary, and it
  makes the totals add up.
- **Explicitly non-additive** — each team reports its own influenced figure, clearly
  labelled as overlapping and never summed. Honest and requires discipline in every deck
  that quotes it.
- **Split by agreed weights.** Feels rigorous, is arbitrary, and produces an argument
  every quarter. Avoid unless finance owns the weights.

The failure to avoid is each team quietly using method two while leadership adds them up.
Say in the deliverable whether the figure is additive with other teams' claims. That
sentence is the most valuable thing in the analysis.

## What support can measure that is genuinely its own

Rather than competing for credit on the revenue line, measure things support uniquely
controls and that plausibly precede revenue:

- **Repeat contact and unresolved rate** — the strongest support-side predictors of
  account risk.
- **Unkept commitments** — countable, clearly support-owned, and clearly bad.
- **Service attainment against what each account was sold**, per account rather than in
  aggregate.
- **Time to resolution from the customer's first contact**, including escalation paths.
- **Recovery outcome** — for accounts that had a serious failure, what share were still
  there a year later, against matched accounts.

These are defensible, they are not contested by other teams, and they move before
revenue does — which makes them more useful to manage by than an attributed revenue
figure anyway.

## Framing the negative case

Sometimes the honest finding is that support's revenue effect cannot be isolated. That is
not a failure of the analysis and it is not an argument against funding support — plenty
of essential functions cannot be attributed a revenue share, and nobody asks security to
prove its NRR contribution.

Say it directly, offer the strongest available alternative (rung 1 or 2 plus the
support-owned metrics above), and propose the holdout that would settle it. A team that
declines to invent a number and instead proposes the experiment tends to be trusted with
the next question too.

## Guardrails

- **Do not sum influenced figures across teams**, and say so explicitly in the artifact.
- **Do not present rung 2 language as rung 4.** "Support drove £2m of retention" is a
  causal claim; "accounts with resolved escalations retained at a higher rate" is not.
  The wording is the claim.
- **Do not build the number backwards from the budget** you want to defend. It will be
  caught, and the cost is every future analysis.
- **Do not use attribution to deprioritise low-revenue accounts.** In regulated sectors,
  differential service on that basis is a conduct issue.
- **Joining support, CRM and billing data** creates a personal-data record none of the
  sources held. Flag purpose and retention.
- **Cite ids and aggregates**, never transcripts. These figures go to boards and
  investors.

## Present results to the user

1. **Which rung of the ladder** the claim sits on, named, at the top.
2. **Why the naive method was rejected**, briefly — it pre-empts the first question.
3. **The comparison** for any association claim: what was matched on, the margin, the
   interval.
4. **The traceable influence cases**, counted individually, with evidence ids.
5. **Whether the figure is additive with other teams' claims**, stated in one sentence.
6. **The support-owned leading metrics**, as the thing to manage by.
7. **The holdout design** that would upgrade the claim, with its cost — so the choice
   between a weak number now and a strong one next quarter is the reader's.
