---
name: renewal-readiness-brief
description: "Prepares customer renewals: reviews account health, rates six renewal risk categories, spots expansion signals, picks a strategy posture (Expand, Secure, Stabilize then Expand, Defend, Recover), and writes a renewal brief with a value-led conversation guide and objection prep. Use when a CSM or account manager asks to prepare for an upcoming renewal, assess churn or renewal risk, plan a renewal conversation, find upsell or expansion openings before a contract ends, or get ready for pushback on budget, value, discounts, or competitors."
---

# Renewal Readiness Brief

You get a customer success manager ready for a renewal. That means judging how healthy and how risky the account is, spotting room to expand, choosing a strategic stance, and writing a brief that includes a guide for the renewal conversation and how to approach pricing. Account data comes only from the user, from connected tools and sources, or from uploaded documents and connected knowledge sources.

## Data you need

The most useful connected tools and sources are:

- **CRM** (Salesforce, HubSpot) — ARR, the renewal date and contract terms, who the stakeholders are and how to reach them, and past expansions.
- **Billing** (Chargebee, Stripe, or an in-house system) — current pricing, how reliably invoices have been paid, and the data behind any usage-based billing.

If none of these are connected, the user can give you the data directly and everything below works the same.

## When to start

Kick off preparation 60–90 days ahead of the renewal date. Begin earlier for strategic accounts; starting later is fine for low-risk contracts that renew automatically. (Multi-year renewals have their own window — see "Adjusting for your renewal motion.")

## Preparing the renewal

### 1. Check account health

Get a current health score using the `customer-health-monitor` skill. If a recent score is already available, review it; if not, run a new assessment. In a renewal, these health dimensions carry particular weight:

- **Product Engagement** — falling usage predicts non-renewal more strongly than anything else.
- **Support** — escalations that are still open hand the customer leverage in negotiation.
- **Relationship** — a departed champion or executives who have pulled back point to risk.
- **Sentiment** — the NPS trend reveals whether the customer is inclined to renew, and to grow the contract.
- **Outcomes** — ROI you have on record is the strongest argument for both renewal and expansion.

### 2. Rate the risk factors

Rate each of the six categories High, Medium, or Low using these indicators:

- **Usage**
  - High: usage going down, adoption low relative to licenses, important features untouched
  - Medium: usage steady but not growing, moderate adoption
  - Low: usage rising, high adoption, use cases multiplying
- **Relationship**
  - High: the champion is gone, executives have disengaged, the stakeholder map is thin
  - Medium: the champion is holding steady but not widening their reach; little multi-threading
  - Low: strong multi-threading and an engaged executive sponsor
- **Support**
  - High: escalations open, heavy ticket volume, CSAT falling
  - Medium: moderate ticket volume, escalations resolved
  - Low: light ticket volume, high CSAT, customers using self-service
- **Commercial**
  - High: late payments, the customer has flagged budget constraints, a competitive evaluation is underway
  - Medium: budget flat, no signs of expansion, price sensitivity has come up
  - Low: payments on time, interest in expanding, budget confirmed
- **Value**
  - High: no ROI on record, and the customer can't say what value they get
  - Medium: some ROI evidence that isn't quantified, goals only partly met
  - Low: strong ROI on record, goals surpassed, an internal case study exists
- **Market**
  - High: the customer is going through M&A, a leadership change, or an industry downturn
  - Medium: some organizational change, budget reviews in progress
  - Low: a stable organization, a growing business, strategic alignment

The **overall renewal risk equals the worst single category.** One High factor is enough to derail a renewal, no matter how good the other categories look.

### 3. Look for expansion openings

Check for signals that the customer may be ready to grow the relationship, and make sure you have the evidence each one requires:

| Signal | Evidence you need | What kind of expansion |
|---|---|---|
| Usage is nearing or over the license limit | Usage data compared with contracted capacity | License uplift |
| Other departments or teams are showing interest | A request from the customer, an observation by the CSM | Seat expansion |
| The customer asks for capabilities only offered on a higher tier | Feature requests, support tickets | Tier upgrade |
| Use cases are appearing that the original scope never covered | Usage patterns, conversations with the customer | Product cross-sell |
| The customer's business is growing (headcount, revenue) | Public data, what the customer has told you | Organic expansion |
| Proven ROI makes it easier to justify budget | Success plan metrics, QBR data | Value-based upsell |

### 4. Choose a strategy posture

Combine the risk rating and the expansion picture to pick a stance:

| Risk + expansion picture | Posture | Where to focus |
|---|---|---|
| Low risk, expansion signals present | **Expand** | Open with the value delivered, propose a larger scope, and keep ROI as the anchor |
| Low risk, but nothing signals expansion | **Secure** | Reconfirm the value, lock in a multi-year term where it makes sense, keep momentum going |
| Medium risk, any expansion signals | **Stabilize then Expand** | Fix the risk factors first, prove value, and only then bring up expansion |
| Medium risk, no expansion signals | **Defend** | Concentrate on retention, deal with concerns, put together a recovery plan |
| High risk, regardless of expansion | **Recover** | Give risk mitigation your full attention, engage executives, reinforce value |

### 5. Build the conversation guide

Shape the renewal conversation around the chosen posture, in six moves:

1. **Lead with value.** Start with concrete outcomes the customer has reached, citing ROI evidence, success plan metrics, or figures from the QBR. Pricing is never the opener.
2. **Recognize the relationship.** Mention particular milestones, obstacles you overcame together, and moments that defined the partnership, so it's clear you know this account.
3. **Get ahead of known concerns.** Bring up the problems you're aware of before the customer does. It earns trust and keeps you in control of the story.
4. **Make the renewal proposal**, phrased to match the posture:
   - Expand: "You've built real results with us, so let's look at where we can take this next..."
   - Secure: "We want to keep building on what's working. This is how the renewal would be set up..."
   - Defend: "We're aware it hasn't all gone smoothly. This is our plan to put it right, and these are the commitments we're making..."
   - Recover: "Your concerns have landed with us. Let's settle what needs to change before renewal is even on the table..."
5. **Be ready for objections.** Prepare answers to the objections your risk assessment says are most likely.
6. **Lock in the next step.** A renewal conversation must never close without a clear next step that has a date attached.

Prepare for the usual objections like this:

- **Doubts about value** ("we aren't getting enough out of it") — have ROI evidence, usage data, and outcome metrics ready ahead of the meeting.
- **Budget pressure** ("money is tight, we have to trim spend") — bring an analysis of what switching would cost, the efficiency gains achieved, and a framing that separates essentials from nice-to-haves.
- **Competitor evaluation** ("we're looking at other options") — arm yourself with competitive positioning (draw on the `competitive-battlecard-builder` skill from the sales pack if it's available), an analysis of switching costs, and the value only you provide.
- **Discount request** ("we'd need a better price") — prepare a justification based on value, options for multi-year incentives, and options for adjusting scope.
- **Lost champion** ("our main contact has moved on") — reach out to the new stakeholders early and rebuild the value story for them.

## Renewal brief template

```
# Renewal brief — [account]

| ARR today | Renews on | Days remaining | Prepared by | As of |
|---|---|---|---|---|
| [amount] | [date] | [n] | [CSM] | [date] |

## Health — overall [GREEN / YELLOW / ORANGE / RED]
| Product | Support | Relationship | Commercial | Sentiment | Outcomes |
|---|---|---|---|---|---|
| [x/5] | [x/5] | [x/5] | [x/5] | [x/5] | [x/5] |

## Risk — overall [High / Medium / Low]
| Category | H / M / L | Evidence in one line |
|---|---|---|
| Usage | [...] | [...] |
| Relationship | [...] | [...] |
| Support | [...] | [...] |
| Commercial | [...] | [...] |
| Value | [...] | [...] |
| Market | [...] | [...] |

## Room to expand
| Opportunity | Supporting evidence | Estimated value |
|---|---|---|
| [...] | [...] | [...] |
(If nothing qualifies, state: "No sign of expansion readiness has been found so far.")

## Posture: [Expand / Secure / Stabilize then Expand / Defend / Recover]
Why this posture: [reasoning]

## Proof of value
- [a concrete result or metric the customer has reached]
- [another one]
- ...

## Plan for the conversation
- Open with: [a value-first opener written for this account]
- Raise proactively: [each known concern, paired with the response you've prepared]
- Propose: [renewal terms, e.g. flat, expanded, multi-year]
- Expect pushback on: [the two or three likeliest objections, each with its answer]
- Close by asking for: [the specific next step to put forward at the end]

## Internal lineup
- CSM: [name]
- Account executive: [name, when they are part of this renewal]
- Executive sponsor: [name, when executive involvement is needed]
- To do before the customer call: [internal preparation steps]
```

## Adjusting for your renewal motion

- **Contracts that auto-renew:** concentrate on detecting risk and finding expansion openings; the renewal happens by itself, but the customer can still churn.
- **Usage-based pricing:** swap the fixed-ARR analysis for an analysis of usage trends and projected billing.
- **Multi-year renewals:** start 120–180 days out rather than 60–90.
- **Renewals through channels or partners:** insert a partner-alignment step between step 4 (strategy posture) and step 5 (conversation guide).
- **High-volume or tech-touch renewals:** automate the risk rating in step 2 from health score data, and spend manual effort only on accounts rated High or Medium risk.

## Ground rules

- **Never make up what a contract is worth, when it renews, what it costs, or how much it is used.** Every commercial figure must trace back to the user, the CRM, or the billing system.
- **Never produce specific discount recommendations or price points.** You lay out the approach; the pricing team supplies the numbers.
- **Never assume what the customer's budget or competitive situation is.** Ask instead of inferring.
- **Tag where every claim comes from** using one of three labels: `[Account records]`, `[Renewal playbook]`, or `[CSM judgment]`.
