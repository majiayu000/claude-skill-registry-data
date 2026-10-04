---
name: market-sizing-sanity-check
description: Use when the user needs to estimate, validate, reconcile, or stress-test TAM, SAM, SOM, market size, demand, capacity, revenue pools, unit volumes, or growth assumptions. Apply it to strategy, market entry, investment, product launch, business cases, and executive reviews where a defensible range and the assumptions behind it matter more than a single impressive number.
---

# Market Sizing Sanity Check

Build a decision-useful market range from explicit assumptions, triangulate it with independent methods, and show which uncertainties can change the decision.

## Reference Loading

Read `references/sizing-methods.md` when selecting methods, translating evidence into equations, reconciling estimates, or designing sensitivity cases.

Read `references/worked-example.md` when the user wants a worked example, calculation audit trail, executive-ready sizing output, or guidance on presenting conflicting estimates.

## First Frame

Define the market before calculating it:

1. Decision: what action could the estimate support or reject?
2. Unit: customers, users, sites, transactions, tonnes, seats, or currency per year.
3. Boundary: product, customer, use case, geography, channel, and time period.
4. Metric: demand, spend, supplier revenue, gross profit, capacity, or addressable value.
5. Scenario: current, forecast, steady state, or adoption-adjusted.

Do not use TAM, SAM, or SOM until each term has a written boundary. A large TAM does not establish reachable demand.

## Workflow

1. Write the sizing question.
   - State the decision, boundary, base year, forecast year, currency, and output unit.
   - Record exclusions and distinguish buyer spend from vendor revenue.
   - Define the precision the decision needs; avoid false decimal accuracy.

2. Build a driver tree.
   - Express the estimate as auditable multiplication, addition, conversion, and constraint steps.
   - Separate observed inputs from assumptions and derived values.
   - Prevent overlap by defining mutually exclusive segments or reconciling duplicates explicitly.

3. Calculate a primary estimate.
   - Prefer a bottom-up route when customer counts, usage, price, or capacity data are credible.
   - Show units on every input and confirm that they cancel to the intended output.
   - Use low, base, and high cases for genuinely uncertain drivers.

4. Build an independent cross-check.
   - Use a different evidence base or causal route, not the same assumptions rearranged.
   - Choose top-down, supply-side, value-based, capacity-constrained, or analogue methods as appropriate.
   - Treat published market reports as one input, not automatic ground truth.

5. Reconcile the estimates.
   - Explain differences through scope, units, price basis, adoption, utilization, timing, or channel markups.
   - Correct mismatched definitions before averaging numbers.
   - Retain a range when uncertainty is real; do not manufacture convergence.

6. Stress-test the decision.
   - Identify the 2-4 assumptions with the greatest impact and weakest evidence.
   - Test break-even values and downside cases, not only symmetric percentage changes.
   - State whether the recommendation survives the plausible range.

7. Produce the decision output.
   - Lead with the range, the base case, the decision implication, and confidence.
   - Include the equation tree, source/assumption register, reconciliation, and next validation actions.
   - Make dated assumptions and forecast mechanics visible.

## Sizing Standards

| Standard | Required practice |
| --- | --- |
| Boundary integrity | Use the same scope, period, currency, and revenue basis across estimates |
| Unit integrity | Annotate units and show conversions |
| Independence | Cross-check with a genuinely different method or evidence base |
| Evidence traceability | Give each material input a source, date, and confidence label |
| Uncertainty | Use scenario ranges for decision-sensitive assumptions |
| Reachability | Separate total demand from serviceable and realistically obtainable demand |
| Decision relevance | Link the range to a threshold, investment, capacity, or strategic choice |

## Confidence Labels

| Label | Meaning | Treatment |
| --- | --- | --- |
| Observed | Direct, appropriately scoped, recent evidence | Use as the anchor |
| Corroborated | Multiple credible signals align | Use with limited range |
| Directional | Plausible evidence with scope or sample limitations | Use a wider range |
| Assumed | No direct evidence yet | Make sensitivity and validation action explicit |

## Default Output

```markdown
# Market Size: <defined market>

## Executive Answer
- Base estimate: <value and year>
- Plausible range: <low-high>
- Decision implication: <what this supports or rejects>
- Confidence: <high / medium / low, with reason>

## Definition
- Customer / use case:
- Product or service:
- Geography and channel:
- Metric and period:
- Exclusions:

## Primary Estimate
<equation with units>

| Driver | Low | Base | High | Evidence status | Source / rationale |
| --- | ---: | ---: | ---: | --- | --- |

## Independent Cross-Check
<different method, equation, and result>

## Reconciliation
<why estimates differ and which scope corrections were made>

## Decision Sensitivity
| Assumption | Break-even or downside case | Decision impact | Validation action |
| --- | --- | --- | --- |

## Caveats and Next Evidence
<the smallest set of evidence that would materially improve the decision>
```

## Guardrails

- Do not quote a market figure without defining what is counted and for which period.
- Do not add segment estimates that overlap or mix end-customer spend with supplier revenue.
- Do not present a CAGR forecast without showing the base, horizon, mechanism, and resulting end value.
- Do not use the same source assumptions for both the estimate and its claimed cross-check.
- Do not imply that market share is obtainable without testing capacity, competition, channel access, sales cycle, and adoption.
- Do not hide uncertainty in a precise midpoint; expose the range and the assumptions that drive it.
- For investment or financial decisions, present the estimate as analytical support and identify inputs requiring finance, legal, regulatory, or specialist validation.
