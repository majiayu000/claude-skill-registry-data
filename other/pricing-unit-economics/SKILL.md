---
name: pricing-unit-economics
description: Evaluate pricing options and customer or transaction economics using explicit revenue, cost, acquisition and retention assumptions. Use for packaging, discount, SaaS or service pricing decisions that need contribution margin, CAC, payback and break-even analysis; not a full valuation, accounting opinion or live price-change authorization.
---

# Pricing and Unit Economics

Connect a pricing choice to customer value, contribution and cash recovery. Show which demand or cost assumptions can reverse the choice rather than recommending the highest modeled price.

## Inputs and References

Start with buyer/segment, decision, pricing unit, realized net price, delivery costs, acquisition spend and acquired customers, retention/cohort evidence, fixed costs and capacity. Align currency, tax basis, cost classification and period before calculating. If inputs are missing, produce a partial model and targeted data request; do not fill gaps with industry averages without permission.

Read `references/economics-methods.md` for equations, pricing design, cohort limits and experiments. Read `references/source-notes.md` when checking definitions or updating guidance. Use `assets/pricing-experiment.csv` to track validation; `assets/unit-economics-input.json` is explicitly fictional training data.

## Workflow

1. Define the actual choice: price, packaging, discount, billing metric or segment. Keep the current offer as the comparison; state buyer value, alternatives, ability to meter and bill predictably, and the cost driver.
2. Audit inputs. Separate list from realized price, VAT/tax from net revenue, annual contract cash from monthly earned revenue, and fixed from incremental cost. Match fully loaded acquisition spend to an appropriate acquisition cohort, with sales-cycle lag disclosed.
3. Calculate contribution, operating break-even and CAC recovery. Use a contribution definition that names included costs; do not label it accounting gross margin if those costs differ. Keep one-off onboarding and recurring service costs distinct.
4. Compare alternatives under explicit volume, mix, retention and cost assumptions. Calculate the customer/transaction threshold needed to preserve baseline contribution. A price change can affect cost-to-serve and churn; holding them fixed is an assumption, not a forecast.
5. Use LTV only when the retention evidence supports it. A constant-churn approximation is a labelled proxy, not a cohort forecast. Missing/zero churn is not proof of infinite lifetime. Prefer observed cumulative cohort contribution for unstable or early products.
6. Recommend a bounded pricing test or data collection action when demand is unverified. Define eligible cohort, outcome window, contribution/retention gates, owner, cost/exposure limit and rollback rule. Separate stated willingness to pay from observed purchase behavior.
7. Handoff a pricing memo: options, auditable model, sensitivity thresholds, confidence and owned validation actions. Send assumptions and cost definitions to the decision memo or value plan so benefits are not double counted.

## Portable Calculation

The standard-library helper expects monthly, net-per-customer inputs. It is a simple steady-state audit, not a demand forecast. From the skill folder:

```bash
python scripts/calculate_unit_economics.py --input assets/unit-economics-input.json
```

The default input is the same fictional example. Currency is a label, not an FX conversion. Money and ratios are emitted as decimal strings; undefined metrics are `null` with warnings. Normalize annual inputs explicitly before use; do not divide an annual churn percentage by 12.

## Guardrails

- Do not use revenue-only payback while presenting it as margin-adjusted recovery.
- Do not conflate contribution, accounting gross profit, operating profit or cash flow.
- Do not fabricate elasticity, conversion lift, churn improvement or willingness to pay.
- If contribution is nonpositive, do not report a finite recovery period or volume-based break-even.
- Do not use universal CAC/LTV benchmarks as a decision gate without the user's business context.
- Separate a proposed test from authorization to alter prices, bill customers or contact them; flag finance/legal validation for material investment, tax or contractual decisions.
