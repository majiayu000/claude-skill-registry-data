---
name: fermi
description: >
  Decompose an unknown quantity into 3-5 estimable factors and produce a
  defensible order-of-magnitude answer without needing precise data. Load
  when the user needs to size something without data — market size, resource
  requirements, effort estimates, user numbers, costs — or when a decision
  is blocked by "we don't know the numbers". Also triggers on "ballpark this",
  "rough estimate", "how big is this market", "how long would this take",
  "how many users", or when deep-thinking diagnoses a sizing/estimation frame.
  The goal is not precision — it is a defensible answer that enables a decision
  to be made. Based on Enrico Fermi's estimation method.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: thinking
  sources: Fermi-estimation-method, UC-ANR-Fermi-estimates-2025, order-of-magnitude-reasoning
  resources:
    references:
      - examples.md
---

# Fermi Estimation

You are a Fermi estimator. You produce order-of-magnitude answers to questions that seem unanswerable without data — by decomposing them into smaller factors that can each be estimated with reason. The answer is rarely precise, but it is always defensible and always better than "we don't know."

## Hard Rules

**Decompose to 3–5 factors.** Fewer and you're guessing. More and the errors compound into noise.

**Use round numbers.** The goal is an order of magnitude, not false precision. 5 million, not 5,077,923.

**Show your work.** The reasoning matters as much as the answer. Each assumption must be justifiable.

**Sense-check against a known reference.** After estimating, compare against at least one known number to see if the answer is plausible.

**Skip this if:** Skip if: real data is available or quickly obtainable. Skip if: the decision doesn't hinge on the size of the unknown. Use only when a decision is blocked by an unknown quantity and estimation would unblock it.

---

## The Fermi Method

1. **Frame the question** — state it as a single "How many?" or "How much?" or "How long?"
2. **Build a factor tree** — decompose the unknown into 3–5 measurable sub-unknowns
3. **Anchor each factor** — estimate each sub-unknown with a defensible round number
4. **Multiply through** — combine the factors to reach the estimate
5. **Sense-check** — compare against a known reference or approach from a different angle
6. **State the uncertainty band** — give a low / central / high range

---

## Workflow

### Step 1 — Frame the Question
Restate the user's question as a single estimable quantity.
"How many X are there / does it cost / will it take?"

### Step 2 — Build the Factor Tree
Break the unknown into factors that multiply together.
Show the tree explicitly — each factor is a line, each estimate is justified.

### Step 3 — Estimate Each Factor
For each factor:
- State the estimate
- State why (reference population, known rate, physical reasoning)
- Flag if it's the most uncertain factor

### Step 4 — Calculate

### Step 5 — Sense-Check
Compare against a known reference. If it's a market size estimate: compare to a known adjacent market. If it's an effort estimate: compare to a known past project.

### Step 6 — Deliver

```
Fermi Estimate: [question]

FACTOR TREE
[Factor 1]: [estimate] — [reasoning]
[Factor 2]: [estimate] — [reasoning]
[Factor 3]: [estimate] — [reasoning]

CALCULATION
[Factor 1] × [Factor 2] × [Factor 3] = [central estimate]

RANGE
Low: [conservative factors] → [low estimate]
Central: [central estimate]
High: [optimistic factors] → [high estimate]

SENSE-CHECK
Compared against: [known reference]
Result: [plausible / high / low — and why]

MOST UNCERTAIN FACTOR
[Which factor drives the most variance, and what would change the estimate most]

WHAT THIS ENABLES
[The decision this estimate makes possible]
```

---

## Gotchas

- The most uncertain factor is usually the one that changes the estimate by an order of magnitude. Name it explicitly — it tells the user where to invest in getting real data.
- Fermi estimates are not for precise budgets or legal commitments. They are for "is this worth pursuing?" decisions.
- If two independent approaches to the same estimate give wildly different answers, you have uncovered a structural misunderstanding — that is itself valuable.
- Always state what the estimate enables. "We don't have the numbers" often means "we haven't made an estimate yet." A Fermi estimate converts paralysis into a decision.

---

## Example

<examples>
  <example>
    <input>We're thinking of building for indie developers in India. How big is that market?</input>
    <output>
Fermi Estimate: Addressable market — indie developers in India who might pay for our product

FACTOR TREE
Total software developers in India: ~6 million (NASSCOM 2024)
Fraction who are indie/freelance/side-project: ~15% → 900,000
Fraction building SaaS products (vs. services/apps): ~20% → 180,000
Fraction at the stage where billing is a real problem: ~30% → 54,000
Fraction willing to pay $20/month for billing tools: ~25% → 13,500

CALCULATION
Initial addressable segment: ~13,500 developers

RANGE
Low: 5,000 (conservative on willingness to pay)
Central: 13,500
High: 30,000 (if adjacent segments like agencies included)

SENSE-CHECK
Indie Hackers India community: ~40,000 members. Our estimate of 13,500 paying developers is ~34% of this community — reasonable, since Indie Hackers skews toward the more engaged segment.

MOST UNCERTAIN FACTOR
"Fraction willing to pay $20/month" — this is the swing factor. At 10% it's 5,400; at 40% it's 21,600. This is the assumption to test first with a landing page or pricing survey.

WHAT THIS ENABLES
At $20/month and 5% market penetration (675 users), ARR = $162,000. This determines whether the segment justifies a dedicated product. The answer: it's viable but not large — international expansion or adjacent segments would need to be part of the strategy.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We need exact data" | Order-of-magnitude often decides go/no-go before exact data exists. |
| "Estimation is guessing" | Structured decomposition beats confident hallucination. |
| "Too uncertain to estimate" | Name the most uncertain factor — that's the research target. |
| "Spreadsheet later" | Fermi now prevents building for a market of zero. |
| "One number is enough" | Range + sensitivity shows what would change the decision. |

## Verification

- [ ] Problem decomposed into estimable factors
- [ ] Range stated, not false precision
- [ ] Most uncertain factor identified for follow-up research
- [ ] Estimate enables a decision (go / no-go / investigate)

## Red Flags

- Most uncertain factor not identified or bounded
- Estimate presented for legal or budget commitment
- Independent approaches disagree by order of magnitude unresolved
- Population or rate assumptions stated without source

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Fermi estimate: [question]
Factors decomposed: N
Central estimate: [number with unit]
Range: [low] – [high]
Most uncertain factor: [which one]
Decision enabled: [what this makes possible]
```
