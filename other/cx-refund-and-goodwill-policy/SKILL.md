---
name: cx-refund-and-goodwill-policy
description: Use to design a refund, credit and goodwill framework that agents can apply consistently without escalating everything, and to control what it costs. Trigger for "should we give this customer a credit", "design our goodwill policy", "refund authority limits", "our credits are out of control", compensation decision frameworks, or agents escalating every refund request.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Refund, credit and goodwill frameworks

Two failure modes, and most organisations have both at once:

- **No framework.** Every request is escalated, decisions depend on which agent and which
  manager, similar customers get different outcomes, and the cost is invisible until
  finance asks.
- **A framework that is really a budget.** A per-agent credit allowance, which agents
  spend to end difficult conversations regardless of whether anything was owed.

A working framework separates **what is owed** from **what is a gesture**, and gives
agents authority to decide the common cases alone.

## Owed and goodwill are different decisions

**Owed** — the customer is entitled to it. A billing error, a service failure against a
contractual commitment, a statutory or regulatory right, a failed transaction. This is
not a negotiation, it is not discretionary, and it should not depend on the customer
asking well or escalating. **Where something is owed, the right target is to find and
fix it proactively**, not to pay it only to the customers who complain — which is
usually indefensible and, in regulated sectors, may be a reportable failure.

**Goodwill** — nothing is strictly owed and you choose to give something. Discretionary,
and the place a framework adds most value.

Getting the classification right is the whole job. Most disputes about "our goodwill
costs too much" turn out to be redress that was owed, misfiled as generosity — which
means the real problem is the underlying failure rate, and cutting the goodwill budget
would leave customers under-compensated.

**Report the two separately, always.** Owed redress trending up is a service-quality
signal. Goodwill trending up is a policy or process signal. Combined, they are neither.

## The decision structure agents can actually use

Write it as a decision procedure, not a set of principles:

1. **Is anything owed?** Against the four tests: billing accuracy, contractual
   commitment, statutory or regulatory right, transaction integrity. If yes → owed path,
   at the amount owed, with no discretion and no negotiation.
2. **Did we fail, and did the customer lose something?** Effort, time, money, an
   opportunity. Name the loss; a gesture with no identified loss is a habit.
3. **What is proportionate to that loss?** Banded, not free-form.
4. **Has this customer had goodwill recently, and why?** Repeat goodwill for the same
   underlying issue means the issue is unresolved — the answer is a fix and an
   escalation, not a third credit.
5. **Is a non-monetary remedy better?** Frequently yes, and frequently cheaper: fixing
   it faster, a named contact, a workaround, a genuine explanation of what went wrong.
   **Money is not the only currency, and it is often not the one the customer wanted.**

## Authority, set from the distribution

Push authority down as far as the data supports:

- **Look at the actual distribution of amounts.** In most operations the large majority of
  requests sit in a narrow low band. Setting frontline authority above that band removes
  nearly all escalation, and escalation is expensive for both sides.
- **A tiered ladder**: frontline up to a threshold, team lead above it, then a named owner
  for anything large or unusual.
- **Authority is not an allowance.** Frame it as "you may decide up to X where the
  framework applies", never as "you have X to spend". A budget gets spent; authority gets
  exercised.
- **Log the reason, not just the amount.** A single reason code plus the failure it
  relates to. This is what makes consistency auditable later, and it costs the agent one
  click.
- **No authority to give nothing where something is owed.** Agents should not be able to
  refuse redress that the owed tests establish — that is the more damaging error and it
  is the one an incentive to control cost produces.

## Consistency is the property that matters most

Two customers with the same failure should get the same outcome. When they do not, and
they compare notes, the framework has cost you more than the money.

- **Audit outcomes for unjustified variation**: by agent, by channel, by tenure, by
  region, and — this one matters — by how loudly the customer complained. **A system that
  pays more to people who escalate is a system that teaches escalation**, and it
  systematically under-compensates the customers least able to advocate for themselves.
- **Check for variation by anything you could not defend.** Differences correlated with a
  protected characteristic, with a proxy for one, or with inferred ability to pay are a
  conduct and discrimination exposure, not a cost-control finding. Look for it
  deliberately rather than waiting for it to surface.
- **Suppress small cells** and do not rank individual agents on a handful of decisions.

## Cost control that does not break the framework

The right lever is almost never the amount:

- **Reduce the failures.** Goodwill volume is a downstream metric. Rank goodwill spend by
  the failure that caused it and route the top items to their owner — this is the only
  lever that reduces cost and improves the customer experience simultaneously.
- **Fix the surprise cases.** A large share of goodwill goes to customers who were
  charged correctly and unexpectedly. A clearer notice is cheaper than the credits.
- **Cut the repeat cases.** Second and third goodwill payments on the same underlying
  issue are pure waste and a strong signal the issue was never fixed.
- **Reduce escalation, not authority.** Escalating a small credit costs more in handling
  time than the credit.

**Do not set a cost target on goodwill spend without a quality guardrail.** It will be
met, by declining redress that was owed, and the cost will reappear as complaints and
churn.

## Guardrails

- **Do not decide an individual case.** This designs and audits the framework; the
  decision is the authorised person's. If asked to approve a specific credit, produce the
  framework's answer and the evidence, and leave the decision.
- **Never condition redress on silence.** Tying a payment to withdrawing a complaint, a
  review, or a regulatory referral is a serious conduct problem. Flag it if you see it in
  the data.
- **Whether something is legally owed is a question for legal and compliance.** Produce
  the tests and the evidence; do not rule on the entitlement.
- **Financial difficulty is not a goodwill case.** Route it to the process that handles
  it, with vulnerability signals flagged.
- **Cite ids and aggregates.** These records contain payment details and financial
  circumstances.

## Present results to the user

1. **Owed versus goodwill, split**, with volume and cost for each, and the proactive-fix
   position on anything owed.
2. **The decision procedure**, written so an agent can follow it on a live conversation.
3. **The amount distribution**, and the authority thresholds it implies.
4. **Consistency audit** — variation by agent, channel, tenure, region, and by escalation
   intensity, with anything indefensible flagged separately and urgently.
5. **Goodwill ranked by causing failure**, with owners. The cost-reduction lever.
6. **Repeat goodwill on the same issue**, as a list — waste and an unresolved-issue signal.
7. **What needs a legal or compliance determination** rather than an operational decision.
