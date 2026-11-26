---
name: pricing-strategy
description: Choose the right freelance pricing model (hourly/project/retainer/package/value-based) and generate a rate-increase email. Computes recommended rates via runtime/pricing_calculator.py. Free-first, bilingual.
personas:
  - FREELANCE
triggers:
  - pricing strategy
  - pricing
  - retainer
  - value-based
tech_stack:
  - invoiceninja/invoiceninja

---
[SKILL] pricing-strategy
[OBJ] Help a freelancer select a pricing model and compute a defensible recommended rate, then draft a client-ready rate-increase or proposal-pricing email. Ground every number in `runtime/pricing_calculator.py` rather than guesswork.

[RULES]
1. [REQ] Model selection: recommend among hourly, fixed-project, retainer (recurring), packaged/productized, and value-based. Pick by client maturity, scope clarity, and outcome leverage — not default.
2. [REQ] Compute the rate: call `runtime/pricing_calculator.py` with inputs (income target, fixed expenses, effective tax rate, target utilization %, platform fees). Present the recommended hourly/project rate and the break-even floor.
3. [REQ] Show the math: output income target → expenses → tax → utilization → platform fee → recommended rate as a small table so the freelancer can defend or adjust it.
4. [REQ] Currency awareness: for Arabic-platform clients default to SAR/AED/EGP and show USD-equivalent; respect local market rates, not just Western ones.
5. [REQ] Rate-increase email: when raising rates, draft a short, respectful bilingual message (Arabic + English) citing added value/scope, with a grace period for existing clients. Route final copy to `proposal-writer` when persuasion is the core ask.
6. [REQ] Free-first: no paid pricing tool required; the calculator is a pure function in the repo. Closed estimators only as parity.
7. [REQ] Storage: cache computed scenarios via `StorageFactory`; never log client financials or PII.

[PROHIBIT]
1. No inventing a client's budget or pretending a rate was "market-standard" without a source.
2. No sending the rate-increase or pricing email without explicit user approval.
3. No storing client financial data outside the approved storage backend.
