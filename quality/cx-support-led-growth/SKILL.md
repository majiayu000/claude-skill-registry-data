---
name: cx-support-led-growth
description: Use to find where support can drive adoption, referral and retention without turning into a sales channel, and to measure whether it worked. Trigger for "can support drive growth", "support-led growth programme", "should agents mention other features", advocacy and referral from support, adoption nudges in support conversations, or a support team being given a revenue target.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Support-led growth

Someone has noticed support talks to more customers than any other team and asked what
it could be doing commercially. The question is reasonable and the usual answers are
bad.

The framing that works: **support drives growth by removing the reasons customers do
not grow, not by promoting.** Those are different mechanisms with different costs, and
only one of them survives contact with a support queue.

## The mechanisms, best first

**1. Removing adoption blockers.** A customer who cannot get a capability working will
not expand into it. Fixing that is unambiguously support's job, it requires no change of
posture, and it is the largest of these effects in most businesses. This is where to
start, and it is mostly an onboarding-friction and knowledge problem rather than a new
programme.

**2. Resolving the failure that is blocking a decision.** Accounts frequently pause an
expansion until an open problem is fixed. Identifying those and prioritising them is
high-value and needs no selling — just knowing which open issues sit on accounts with a
pending decision.

**3. Closing the loop on requests.** Telling a customer the thing they asked for now
exists is the highest-converting, lowest-risk growth motion available to support, and
almost nobody does it systematically. It requires only a record of who asked for what.
Start here if you want a quick, safe win.

**4. Contextual adoption nudges.** Pointing out an existing, already-included capability
that solves the problem at hand. Safe when it is *relevant to the conversation* and
already paid for. Becomes promotion the moment it involves an upgrade.

**5. Advocacy and referral.** Customers who have had a genuinely good recovery experience
are unusually willing to refer or give a reference. Timing and consent decide whether
this is graceful or grubby.

**6. Flagging commercial signal to the account owner.** Detection only, and it is a
handoff design problem rather than a growth programme.

Everything past 4 needs an explicit design; everything past 6 is sales.

## The line, stated plainly

Support may **help the customer do more of what they already bought**. Anything that
requires the customer to spend more is a commercial conversation and belongs to whoever
owns the account.

Concretely, do not:

- Mention an upgrade, a paid tier, or a price in an unresolved conversation.
- Give agents revenue targets, quotas, or commission. This is the single change most
  likely to damage a support operation, and its effects show up in quality and repeat
  contact within a quarter.
- Ask for a referral or review from a customer whose issue is open, or whose issue was a
  failure you caused, until it is genuinely resolved and they say they are happy.
- Route a complaint, a vulnerable customer, or an account in financial difficulty into any
  growth motion.
- Add a promotional footer to support replies. It reads as advertising in a service
  interaction and it measurably reduces trust in the reply above it.

## Design the safe motions properly

**Request loop-closing.** Needs a record of who asked for what, a trigger when it ships,
and a message that is a genuine notification rather than a pitch. Send it from support,
reference their original conversation, and do not attach an upsell. Measure adoption of
the shipped capability among those told versus comparable customers not told.

**Adoption nudges.** Rules, not agent discretion: relevant to the resolved issue,
included in their current plan, at most one, after resolution. Anything else and it
becomes a habit that spreads to the wrong conversations.

**Advocacy asks.** Only after a resolved interaction the customer has confirmed they are
happy with, only once in a defined period, and never for a case where you caused the
problem. Make the ask separable from the support conversation so declining costs the
customer nothing.

## Measure it as an experiment, with a guardrail

Every one of these is testable and almost none are tested.

- **Withhold at random.** Tell half the customers who asked for a feature that it shipped;
  compare adoption and expansion. This is cheap, it is the only way to know the effect is
  real, and it converts an anecdote into a number that survives review.
- **Report the guardrail every time**: satisfaction, complaint rate, and repeat contact for
  customers who received the motion versus comparable customers who did not. **If the
  guardrail moves the wrong way, the programme is net negative regardless of the revenue
  line** — and support-side damage is slow, so you will only see it if you look.
- **Watch agent-side effects** — handle time, quality scores, and whether participation
  correlates with anything worse.
- **Attribute honestly.** Without a holdout, report influence rather than causation.

## Traps

- **The team gets a revenue target.** Almost always the beginning of the end: quality
  drops, then repeat contact rises, then the revenue gain reverses. If a target is
  imposed, argue for a support-quality guardrail with a stopping condition attached, and
  get the stopping condition agreed in writing before launch.
- **Measuring activity instead of outcome.** Nudges delivered, features mentioned — these
  rise on command and mean nothing.
- **Ignoring the trust cost.** It is real, it is slow, and it does not appear in a
  monthly pipeline review. The guardrail metric is the only instrument for it.
- **Assuming the requester is the buyer.** The person who asked for the feature may have
  no authority and no interest in the commercial consequence.
- **Consent.** Outbound notification and advocacy asks are governed by marketing-consent
  rules regardless of how helpful the message is. Flag it; do not assume the support
  relationship covers it.

## Present results to the user

1. **The mechanisms in scope**, ordered, with the line between helping customers use what
   they bought and asking them to buy more stated explicitly.
2. **What is excluded** — complaints, vulnerability, unresolved conversations, financial
   difficulty, consent gaps.
3. **The design for each motion in scope**, as rules rather than agent discretion.
4. **The experiment** — what is withheld from whom, and what will be compared.
5. **The guardrail metric and its stopping condition**, agreed before launch.
6. **Results as influence unless a holdout ran**, and the holdout design if a causal claim
   is wanted.
7. **Agent-side effects**, so a revenue gain paid for with support quality is visible
   rather than discovered later.
