---
name: project-budgets
description: Engineering budgets done right — estimate basis, contingency, change control, tracking actuals through closeout.
version: 1
triggers: project budget, engineering budget, contingency, change control, estimate basis
category: Electrical & energy
blurb: Engineering budgets done right — estimate basis, contingency, change control and tracking actuals.
archetype: knowledge
example: Build the budget structure for this capital project.
---

# Project Budgets (estimate → approve → track → close)

Money discipline for engineering work: every job gets a basis, a number, and a paper trail — even the "quick" ones.

## When to use
- Estimating a job (repair, retrofit, capital item, study).
- Tracking spend during execution; change orders.
- Closeout reconciliation at completion.

## Method
1. **Basis document first**: scope of estimate, assumptions, exclusions, quote validity, FX/escalation, estimator name — an estimate without a basis is a guess wearing a suit.
2. **Build the number**: material (quotes/unit rates), labor (rate × hours), subcontract, rentals, indirects (freight, permits); mark quote-based vs allowance items.
3. **Contingency & reserve**: contingency sized to uncertainty (explicit %, tied to listed risks); management reserve held separately; never bury padding.
4. **Approval & baseline**: approval per thresholds; the approved number is the baseline; revisions are re-approved — not drifted.
5. **Change control**: every scope change → cost + schedule impact statement → approved BEFORE work; track the change log.
6. **Tracking**: commitments (POs) vs actuals vs forecast-to-complete; invoice reconciliation against delivery; monthly one-page report (variance + reasons + actions).
7. **Closeout**: final cost vs budget; variance explained; lessons captured; unspent contingency released explicitly.

## Quality gates
- [ ] Basis doc for every estimate; approvals recorded.
- [ ] Changes logged with impact + approval before execution.
- [ ] Variance reported with reasons (no unexplained deltas).
- [ ] Closeout reconciles; contingency disposition stated.

## Red lines
- No work without an approved estimate/PO; no "adjustments" to hide overruns; no verbal change orders.

## Related
`engineering-work-packages` · `delivery-planning` · `electrical-test-records` (evidence of work done).
