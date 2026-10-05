---
name: cx-revenue-at-risk
description: Use to quantify the revenue exposed by unresolved support failures, complaints and escalations without inflating the number. Trigger for "how much revenue is at risk", "what are these support failures costing us", "revenue behind our open escalations", building a business case for fixing a support problem, or a revenue-at-risk figure that looks too large to believe.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Revenue at risk

The number gets built the same way almost every time: take every account with an open
complaint or escalation, sum their annual revenue, present the total.

That is not revenue at risk. It is **revenue that happens to have a ticket attached**,
and in a business where most accounts contact support at some point it converges on
total revenue. Anyone senior will discount it in one question, and the credibility
cost lands on the next analysis too.

## Exposure and risk are different quantities

```
risk = exposure × probability
```

- **Exposure** is the revenue attached to the affected accounts. Easy, and you can
  always compute it.
- **Probability** is the chance those accounts actually leave or reduce spend given
  what happened. Hard, and it requires evidence.

**If you do not have a defensible probability, report exposure and call it exposure.**
"£4.2m of ARR sits on accounts with an unresolved escalation" is a true, useful,
defensible sentence. "£4.2m of ARR is at risk" is not the same claim, and the
difference is the whole credibility of the analysis.

## Getting a probability that survives scrutiny

The only honest source is your own history: among accounts that had this signal, what
share subsequently churned or downgraded, compared with otherwise-similar accounts
that did not?

- **Compute it per segment.** The conditional churn rate after an unresolved
  escalation differs enormously between an enterprise account on a three-year
  contract and a self-serve monthly subscription.
- **Use the uplift, not the raw rate.** If 12% of flagged accounts churned and 9% of
  comparable unflagged accounts also churned, the signal-attributable probability is
  roughly 3 points, not 12. Reporting the raw rate triple-counts the baseline churn
  that was going to happen anyway.
- **Match on the obvious confounders** — segment, tenure, size, contract type, usage
  trend. Accounts that escalate are not a random sample; they are often larger and
  more engaged.
- **Give a range, not a point.** Report the interval on the conditional rate, and
  propagate it. A range of £300k–£900k is more useful and more defensible than a
  spuriously precise £612k.

If you cannot compute an uplift because outcomes are not joinable, say so plainly.
Exposure with a stated absence of probability beats a probability you invented.

## Contract timing dominates

The same exposure carries very different near-term risk depending on when the
customer can actually leave:

- **Inside the renewal or notice window** — the risk is live now.
- **Mid-term on a multi-year contract** — the revenue is contractually secured for
  now; the risk is a non-renewal much later, or a reduction at the next true-up.
- **Monthly or usage-based** — the risk is continuous and can materialise next week.

Bucket exposure by **time to the next decision point** and report near-term risk
separately. A total that mixes revenue leaving next month with revenue that cannot
leave for two years is not decision-ready, and executives will correctly ignore it.

For usage-based revenue, the risk is often a *reduction* rather than a departure.
Model partial loss; treating every at-risk account as a total loss is a large source
of inflation.

## Do not double count

Four ways the number gets inflated by construction:

- **One account, several issues.** Deduplicate to the account. An account with six
  open tickets is one exposure.
- **Parent and child accounts.** Group hierarchies mean the same revenue appears
  under several records.
- **Overlapping signals.** An account with a complaint *and* an escalation *and* a
  churn signal is one account. Take the strongest signal, not the sum.
- **Renewal and expansion double-counted.** Revenue you might lose and revenue you
  might not gain are different lines. Never add them.

## What you cannot claim

**You cannot claim support caused the churn.** Accounts that escalate differ from
accounts that do not in ways you have not controlled for, and the customer who left
after a bad support experience may have left anyway. The uplift calculation narrows
this; it does not close it.

Say what the analysis supports:

- **Supported:** "accounts with this signal churn at a higher rate than comparable
  accounts without it, by this margin, with this interval."
- **Not supported:** "fixing this will save that revenue."

The second claim needs an intervention with a control group — fix the failure for a
random subset and compare — and if someone wants it, that is the design to propose
rather than a stronger reading of the observational number.

## The version of this that actually gets acted on

A total is a headline. What changes a decision is the **ranked list of specific
failures**, each with the accounts behind it and the exposure it carries:

- **Rank by exposure × uplift × imminence**, not by exposure alone.
- **Attach the cost to fix**, where you can estimate it. A £200k exposure fixable in a
  sprint outranks a £2m exposure needing a platform rebuild.
- **Name the owner.** Most of these are product, billing or process failures, not
  support failures, and the analysis is only useful if it reaches the person who can
  fix the cause.
- **Separate the fixable from the already-lost.** An account that has given notice is
  a lesson, not a save opportunity. Reporting them together overstates what any
  intervention can recover.

## Guardrails

- **Do not present exposure as risk**, in the summary, the chart title, or the
  headline. This is the single most common failure and it is a wording problem with a
  credibility consequence.
- **Do not use this to prioritise service by revenue** in a way you could not defend
  to a customer or, in regulated sectors, a regulator. Fixing a systemic failure for
  the accounts that pay most and leaving it for everyone else is a conduct issue.
- **Cite account and conversation ids; do not paste transcripts.** These decks reach
  boards and sometimes investors.
- **Joining support data to revenue data** creates a personal-data record neither
  source held. Flag purpose and retention; do not decide them.

## Present results to the user

1. **Exposure and risk as separate numbers**, with the probability method named — or an
   explicit statement that no probability was available.
2. **Bucketed by time to the next decision point**, with near-term risk called out.
3. **The uplift calculation** — flagged versus comparable unflagged rate, the interval,
   and what was matched on.
4. **Deduplication** — accounts, hierarchies and overlapping signals, with counts
   before and after.
5. **The ranked failure list**, with accounts, exposure, imminence, cost to fix and
   owner. This is the deliverable.
6. **Already-lost separated from still-fixable.**
7. **What is not claimed** — causation, and what an intervention study would take.
