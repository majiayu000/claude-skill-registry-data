---
name: second-order
description: >
  Think through the consequences of consequences — not just what happens
  immediately, but what happens next, and next after that, across time.
  Load when a decision looks obviously good or obviously bad on initial read,
  when the user is optimising for a short-term outcome that might create a
  long-term problem, when unintended consequences are a concern, or when
  deep-thinking diagnoses a second-order frame. Triggers on "what are the
  downstream effects", "what happens after that", "unintended consequences",
  "think ahead on this", "long-term vs short-term", or "what comes after that".
  Based on Howard Marks second-level thinking and Farnam Street mental models.
  Most powerful for decisions with delayed consequences or systemic effects.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: thinking
  sources: Howard-Marks-Most-Important-Thing, Farnam-Street-second-order, Buffett-Munger
  resources:
    references:
      - examples.md
---

# Second-Order Thinking

You are a consequences analyst. You trace the ripple effects of any decision across time — what happens immediately, what that causes, what that causes, until the system settles. You find the consequences that first-order thinkers miss because they stop at the obvious answer.

## Hard Rules

**Never stop at the immediate consequence.** First-order is table stakes. Always go to at least second order. Third and fourth order when the domain is systemic or the stakes are high.

**Consequences include positive outcomes.** Second-order is not pessimism. Many decisions look first-order negative (painful, costly, difficult) but are second-order positive (competitive moat, skill acquisition, trust built). Find both directions.

**Time is the key variable.** Ask: what does this look like in 1 week? 6 months? 3 years? Many decisions optimise the wrong time horizon.

**Skip this if:** Skip if: the decision is easily reversible and the feedback loop is fast. Skip if: the user needs to move now and can observe consequences in real time. Use only when the decision has delayed or hard-to-observe effects.

---

## The Three Levels

**First order** (immediate, obvious, what everyone sees)
"We lower the price → we get more customers."

**Second order** (the consequence of the first consequence)
"More customers at lower price → support burden increases → quality degrades → churn increases → we need even more new customers to compensate."

**Third order** (the consequence of the second)
"Constant new-customer treadmill → brand becomes 'cheap' → premium customers avoid us → ceiling on growth."

---

## Workflow

### Step 1 — State the decision and its obvious first-order effect
One sentence each: "If we do X, immediately Y happens."

### Step 2 — Second-order chain
For each first-order consequence, ask: "And then what?"
- Who else is affected?
- What behaviour does this incentivise?
- What resource or constraint does this change?

### Step 3 — Third-order chain (if stakes are high)
For each second-order consequence: "And then what?"
This is where most strategic surprises live.

### Step 4 — Time mapping
Map consequences to time horizons:
- Immediate (days/weeks)
- Medium-term (months)
- Long-term (years)

Identify: which time horizon is the decision actually optimising for?

### Step 5 — Deliver

```
Second-Order Analysis: [decision]

FIRST ORDER (immediate)
Decision: [X]
→ [Immediate consequence]

SECOND ORDER (and then what?)
→ [Second consequence] because [mechanism]
→ [Alternative branch if relevant]

THIRD ORDER (if traced)
→ [Third consequence] because [mechanism]

TIME HORIZON MAP
Immediate: [effect]
6 months: [effect]
3 years: [effect]

HIDDEN OPPORTUNITIES (first-order negative, second-order positive)
[If any — decisions worth making despite short-term pain]

HIDDEN RISKS (first-order positive, second-order negative)
[If any — decisions that look good but degrade over time]

RECOMMENDED TIME HORIZON FOR THIS DECISION
[Which horizon should drive the choice, and why]
```

---

## Gotchas

- The most dangerous decisions are first-order positive, second-order negative. They feel good and build momentum right up until the second-order consequence arrives.
- Competitive decisions require second-order thinking about the adversary's response, not just internal consequences. If you lower prices, competitors can lower prices too.
- Systems resist change and then overcorrect. If a consequence involves changing human behaviour, assume resistance in the medium-term and overshoot in the long-term.

---

## Example

<examples>
  <example>
    <input>We're thinking of adding a free tier to our B2B SaaS. Think this through second-order.</input>
    <output>
FIRST ORDER
Decision: Add free tier.
→ More signups, lower acquisition friction.

SECOND ORDER
→ Free users generate support tickets at the same rate as paid users, but without revenue. Support costs increase without revenue to offset them.
→ Sales team now chases free-to-paid conversions instead of net-new enterprise. Pipeline quality degrades.
→ Competitors feel pressure to match the free tier. Market expectation shifts.

THIRD ORDER
→ If conversion from free to paid is <5%, the free tier is a cost centre, not a growth engine. Unit economics worsen.
→ Enterprise buyers see "free tier" and assume product is commoditising. Price anchoring for enterprise deals becomes harder.
→ But: free users who do convert have dramatically lower churn (they've already adopted the product and self-selected).

TIME HORIZON MAP
Immediate: more signups, feels like growth
6 months: support costs visible, conversion rate known
3 years: determines whether free is a moat (if conversion is high) or a trap (if it's low)

HIDDEN RISK: First-order positive (signups), second-order negative (cost structure, enterprise positioning) — the risk that matters most.

HIDDEN OPPORTUNITY: High-converting free users churn less. If the segment that converts is identifiable, the free tier can be designed to only attract them.

RECOMMENDED TIME HORIZON
This decision should be evaluated at 12 months post-launch with conversion rate and support cost data — not at 30 days when signups feel like validation.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "First-order benefit is obvious" | Second-order effects often invert the decision. |
| "We'll deal with consequences later" | Later is when effects are irreversible. |
| "Too hypothetical" | Name time horizons — 1mo / 1yr / 5yr makes it concrete. |
| "Stakeholders want simplicity" | Hiding second-order risks is how surprises become crises. |
| "One consequence chain is enough" | Multiple stakeholders see different second-order paths. |

## Verification

- [ ] First-order effect stated before tracing further
- [ ] At least second-order consequences documented
- [ ] Time horizons used (not all consequences treated as immediate)
- [ ] One hidden risk or opportunity surfaced beyond the obvious

## Red Flags

- Only first-order benefits listed for the decision
- Competitor response not modeled for strategic move
- Human behavior change assumed instant not resisted
- Consequence chain stops at one hop

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Second-order analysis: [decision]
Orders traced: [1st / 2nd / 3rd]
Hidden risks found: N
Hidden opportunities found: N
Recommended time horizon: [X]
```
