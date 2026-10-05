---
name: cx-renewal-risk-review
description: Use to build an account's cumulative support record ahead of a renewal or QBR, so the review reflects the whole relationship rather than the most recent ticket. Trigger for "prepare for this renewal", "what has this account's support experience been", "which accounts are at risk before renewal", QBR preparation, account health review, or an account that renewed badly with no warning.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Renewal risk from the support record

A renewal conversation is usually prepared from the last few tickets and the CSM's
impression. Both are dominated by recency, and both miss the thing that actually
decides these outcomes: **the cumulative experience**, and specifically whether the
things this account was promised happened.

Two failure shapes this skill exists to prevent:

- **A clean recent quarter hiding a decided outcome.** The bad experience was in
  Q1, the decision was made in Q2, and Q3 looks fine because they have stopped
  bothering to contact you.
- **Volume mistaken for health, in either direction.** High contact volume can mean a
  struggling account or a deeply engaged one. Low volume can mean everything works or
  that they have disengaged and are running down the contract.

## Build the record over the whole term, not the last quarter

For the full contract term, or at least twelve months:

- **Contact volume trend**, normalised by usage or seats. Absolute volume rising as an
  account grows is expected; volume per seat rising is not.
- **Unresolved and repeat contacts** — the same issue raised more than once. This is the
  strongest single indicator in the record, because it is the customer telling you
  twice.
- **Escalations**, with end-to-end time measured from their first contact rather than
  from the handoff.
- **Complaints**, formal or informal.
- **Service performance against what they were sold.** If the account is on a tier with
  a response commitment, measure attainment for *them*, not the org average. A premium
  account receiving median service is a specific, defensible finding.
- **Sentiment trajectory** across contacts, as a direction rather than a level.
- **Channel switching**, which frequently signals a customer failing to get resolution
  the way they prefer.

## Promises made, and whether they were kept

This is the highest-value part of the review and it is almost never done, because it
requires reading transcripts rather than aggregating fields.

Search the account's conversations for **commitments**: "we'll have that fixed in the
next release", "someone will follow up on Monday", "I'll escalate that to the product
team", "we'll credit that back". Then check what happened.

An account with three unkept commitments is a renewal risk regardless of how good the
metrics look — and unlike a satisfaction score, it is something you can actually go
and fix before the conversation. It is also the thing the customer will raise, so
finding it first is strictly better than hearing it.

Report each as: the commitment, who made it, the date, and its status. Where a
commitment was kept but never communicated back, that is a closing-the-loop failure
rather than a delivery failure — different fix, and worth separating.

## Whose experience is it?

An account is several people, and their experiences differ in ways the aggregate hides.

- **Aggregate per contact as well as per account.** One person having a consistently bad
  time matters, especially if that person is the champion, the admin, or the person who
  signs.
- **Identify the roles where you can.** An economic buyer with two bad experiences is a
  larger risk than a support requester with twenty routine ones.
- **Watch for a champion going quiet.** A named contact who used to raise things and has
  stopped is a signal, not an improvement.
- **New contacts appearing** can mean the account is growing, or that your champion has
  left. Both matter and they look identical in the data — check.

## Confounders to check before concluding anything

- **Usage growth drives contact volume.** Normalise, or a growing account looks like a
  deteriorating one.
- **Seasonality.** Some accounts contact more at period end, year end, or during their
  own peak.
- **Onboarding contacts are not failures.** A new account contacting frequently in its
  first weeks is normal, and including that period in a trend fabricates an improvement.
- **A migration, integration or upgrade** on their side generates contacts that say
  nothing about your service.
- **Silence is ambiguous.** Check product usage alongside contact volume. Low contacts
  plus falling usage is the dangerous combination; low contacts plus healthy usage is
  fine.

## Output: a brief the account owner can act on

The deliverable is not a score. It is a short document with evidence attached, because
the CSM has to hold this conversation with the customer.

```
Renewal support review — <account> — renewal <date>
Term reviewed: <start> to <end>. Prepared <date>.

Headline
  <one sentence: is the support record a risk to this renewal, and why>

The record
  Contacts: <n> (<trend, normalised by seats/usage>)
  Repeat/unresolved: <n> — <the issues>
  Escalations: <n>, median end-to-end <t> from first contact
  Complaints: <n>
  Service vs their tier: <attainment> against <commitment>
  Sentiment trajectory: <direction>

Commitments
  <commitment> — <who, date> — kept / not kept / done but not communicated

By person
  <contact, role> — <n> contacts, <experience summary>, <trajectory>

What to fix before the conversation
  <specific, owned, with a date>

What they will raise
  <the two or three things, with ids, so nobody is surprised>

Confounders and gaps
  <what was normalised, what could not be assessed>
```

The **"what they will raise"** section is what makes this get used. A CSM walking into
a renewal knowing the three things the customer is going to bring up, with the ids to
hand, is in a completely different position from one holding a health score.

## Guardrails

- **This is one input, not a renewal forecast.** Support signal is blind to
  procurement changes, budget cuts, reorganisations, and a competitor's pricing.
  Say so; the CSM has context you do not.
- **Do not present correlation as causation.** A poor support record and a
  non-renewal may share a cause rather than one producing the other.
- **Never use the review to justify differential service levels** beyond what the
  customer contracted for. Prioritising fixes for high-value accounts and leaving the
  same defect for everyone else is, in regulated sectors, a conduct issue.
- **Cite ids and quote minimally.** These briefs get shared, sometimes into a
  customer-facing deck. Redact anything about individuals that is not necessary.
- **Do not include agent names in a customer-facing version**, and be careful that a
  document blaming named agents does not become the renewal conversation.
- **One account per review.** Batching twenty produces twenty documents nobody reads.

## Present results to the user

1. **The headline judgement**, one sentence, with the evidence behind it.
2. **The record**, over the full term, normalised, with trends rather than levels.
3. **Commitments made and their status** — the section most likely to change what
   happens next.
4. **Per-person experience**, flagging champions and buyers specifically.
5. **What to fix before the conversation**, with owners and dates.
6. **What the customer will raise**, with ids.
7. **Confounders normalised and gaps remaining**, including anything support data
   cannot see.
