---
name: cx-fraud-and-scam-signal
description: Use to surface fraud, scam and financial-crime signals that customers describe to support before detection systems see them, and to check whether agents recognised and routed them. Trigger for "are customers reporting scams", "new scam pattern targeting our customers", "did we spot the fraud signals", authorised push payment scams, "customer was coached by someone on the phone", or fraud reports arriving through support.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Fraud and scam signals in support conversations

Support hears about fraud before fraud systems do. Transaction monitoring sees a payment
that fits a pattern; a support agent hears a customer say someone called them claiming to be
from the bank. The second is earlier, richer, and usually not analysed.

Two distinct jobs, and both are worth doing:

- **Detection support** — finding signals in conversations that indicate a customer is being
  or has been defrauded, particularly where they do not yet realise it.
- **Handling assurance** — checking whether agents recognised the signals and routed them
  correctly.

**This is a read-only analysis feeding specialist teams.** Fraud determination, intervention
and reporting belong to fraud, financial crime and compliance — including the reporting
obligations, which have their own clocks and their own confidentiality rules.

## Signal categories

**Scam-in-progress**, the highest-value and most time-critical. Customers describe the
mechanics without recognising them:

- Someone contacted them claiming to be from your firm, a government body, a delivery
  company, or a technology provider.
- They were asked to move money "for safety", to a "safe account", or to verify by
  transferring.
- They were told not to tell anyone, or to say the payment was for something else. **Coaching
  the customer to lie is among the strongest available signals**, and it is precisely what
  the payment record cannot show.
- They are being walked through the app by someone on the phone, or have installed remote
  access software.
- Unusual urgency tied to a threat — an account closure, an arrest, a fine.
- An investment opportunity with a contact who has been messaging them.
- A romance or long-relationship framing around a payment.

**Already-defrauded**, arriving as a dispute, an unrecognised transaction, or a complaint
about a payment they now regret.

**Account takeover** — locked out, credentials changed, receiving notifications for actions
they did not take, or a third party contacting support on their behalf with suspicious
knowledge.

**First-party and mule indicators**, which need careful, non-accusatory handling and go
straight to the specialists rather than into a general report.

## Why support text beats transaction data here

The payment looks legitimate. The customer authorised it, from their own device, in a normal
pattern. **The only evidence that it was a scam is in what they said** — and that evidence is
frequently in a support conversation days before the loss, or in the same conversation as the
payment.

That makes conversation analysis genuinely additive rather than a duplicate control. Say so
when presenting it, because it is the argument for resourcing the work.

## Detection method

- **Search in every language and channel.** Scam framings are localised and market-specific,
  and a single-language sweep misses whole markets. Voice matters especially — scams are
  described on the phone more than in writing.
- **Include internal notes.** Agents record suspicions there that they never formally
  escalated.
- **Expect novel patterns**, which is what a keyword list cannot catch. Pair the pattern
  search with an open scan for uncategorised harm, because a new scam arrives with vocabulary
  nobody has listed.
- **Report recall honestly.** Hand-label a sample and estimate what you missed. A detection
  count presented without a recall estimate will be read as coverage.
- **Watch vocabulary change over time.** New terms appearing in customer language — a new app,
  a new platform, a new impersonated brand — are the earliest signal of a new pattern
  available anywhere in the business.

## Handling assurance

For conversations with a signal present:

- **Was it recognised?** Or did the agent process the request and move on?
- **Was the required intervention attempted** — a warning, a hold, verification, escalation to
  fraud?
- **Was it routed** to the specialist team, and how quickly?
- **Did the customer proceed anyway**, and was that recorded? Where a warning was given and
  ignored, the record of the warning matters later.
- **Was vulnerability considered?** Scam victims are frequently vulnerable at that moment, and
  the two duties interact.
- **For an already-defrauded customer, was the claim handled to the right standard**, rather
  than treated as an ordinary dispute?

Report recognition rate and intervention rate separately. The gap is the training finding, and
it is usually large because recognising a scam mid-conversation is genuinely hard.

## Feeding it back

The durable output is not a list of cases — it is what changes:

- **New patterns to the fraud team**, with the mechanics described in customers' own words,
  which is more useful than a classification.
- **Impersonation of your own brand** to whoever owns brand and security. If scammers are
  successfully claiming to be you, the mechanism they exploit is frequently something you do —
  a message format, a caller ID, a real process that looks like the fake one.
- **Agent-facing prompts** for the top current patterns, refreshed as they change, since a
  static list decays fast.
- **A monitor for confirmed patterns**, with a volume forecast so it is workable.
- **Product friction findings** — where a scam depends on a step in your product being easy.

## Guardrails

- **Do not determine that fraud occurred, and do not label a customer as a fraudster.** Signals
  go to specialists. A first-party or mule suspicion in particular must not be recorded as a
  conclusion anywhere in an analytics artefact.
- **Reporting obligations are not yours.** Suspicious activity reporting has legal
  requirements, timeframes, and **confidentiality rules that may prohibit telling the customer
  or discussing the report internally**. Route through the defined channel; do not discuss a
  suspicion in general circulation.
- **Do not tip off.** Nothing in an output should end up visible to the customer or in a
  channel where it might be.
- **An in-progress scam is not an analytics finding.** If the data shows a customer currently
  being defrauded, that goes to the intervention route immediately, by whatever process
  exists.
- **Do not build a customer risk label from a detector.** Signals inform a human decision.
- **Restrict distribution tightly**, and keep attack mechanics out of broadly-shared documents
  — a report describing exactly how a scam defeats your controls is a liability.
- **Cite ids; do not reproduce conversation content**, and keep vulnerability detail aggregated.

## Present results to the user

1. **Anything in progress, escalated already** rather than reported — stated first.
2. **Detection method**, with languages, channels, internal notes included, and an estimated
   recall so the count is not read as coverage.
3. **Signals by category**, with counts, and the time between the signal and any loss where
   that is knowable.
4. **Recognition and intervention rates, separately**, with the gap named.
5. **Routing performance** — whether and how fast signals reached the specialist team.
6. **New or changing patterns**, in customers' own framing, with vocabulary change over time.
7. **Impersonation findings** — where scammers exploit something you do — routed to brand and
   security.
8. **Product friction** the scams depend on.
9. **What belongs to fraud, financial crime and compliance**, with the confidentiality
   constraint stated.
