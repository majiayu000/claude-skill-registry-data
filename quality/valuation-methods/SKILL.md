---
name: valuation-methods
description: Value businesses with discipline — DCF, comparables, scenarios, margin of safety, honest assumptions.
version: 1
triggers: valuation, dcf, value a business, comparables, margin of safety
category: Money & markets
blurb: Value businesses with discipline — DCF, comparables, scenarios and a margin of safety.
archetype: knowledge
example: Value this business with a DCF and comparables.
---

# Valuation Methods

A valuation is an argument about the future — build it like an engineer: driver-based, conservative, and auditable. Point estimates lie; ranges inform.

## When to use
- Before any entry, add, or exit decision.
- Stress-testing a price ("is this still worth it?").
- Building or reviewing a financial model.

## Method
1. **Pick methods to fit**: DCF for cash-generative businesses; comparables (multiples) as a market cross-check; dividend discount for stable payers; asset-based for holding/investment entities — use ≥2 and reconcile.
2. **DCF discipline**: revenue driver-based (volume × price × mix), not hockey-stick percentages; capex and working capital respected; terminal value conservative (fade growth, don't extrapolate peaks); WACC from honest inputs; cyclical earnings normalized.
3. **Comparables discipline**: like-for-like (growth, margins, capital intensity); adjustments stated; multiples are shorthand for DCF assumptions — treat them so.
4. **Scenarios over points**: base / bear / bull with the assumptions that move them; sensitivity tables on the 2–3 drivers that matter; probabilities only if you mean them.
5. **Margin of safety**: size the discount to uncertainty (more uncertainty → wider gap between price and value); write the entry range, not a number.
6. **Model hygiene**: inputs / calculations / outputs separated; single source of truth; versioned; auditable — someone else could rerun it (`engineering-work-packages` check discipline).
7. **Pitfalls sweep**: garbage growth, ignoring capex, peak-cycle margins, currency/FX blindness, ESG/litigation blind spots — run the sweep before believing the number.

## Quality gates
- [ ] ≥2 methods cross-checked; divergences explained.
- [ ] Sensitivity shown for the key drivers; scenarios written.
- [ ] Assumptions sourced; model auditable + versioned.
- [ ] Entry range + margin-of-safety logic recorded (journal).

## Red lines
- No single-point certainty; no "it's up, so it's good"; no valuation without reading the fundamentals underneath (`equity-fundamentals`).

## Related
`equity-fundamentals` · `investment-decision-process` · `quant-research`.
