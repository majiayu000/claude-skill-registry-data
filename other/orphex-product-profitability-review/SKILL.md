---
name: orphex-product-profitability-review
description: "Review product advertising economics using aligned net revenue, returns, and explicit variable costs; distinguish contribution from gross ROAS and company profit."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Product Profitability Review

Assess product-level contribution under the user's supplied cost and revenue definitions. Do not equate attributed gross revenue with profit or assume a universal margin.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `product` for ad cost and attributed revenue; returns and variable costs still come from the user.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Reconcile economic scope

Align order/acquisition cohort, product/variant, currency, tax/shipping convention, returns maturity, discounts, refunded revenue, recognized/recovered COGS, fulfilment, payment fees and advertising allocation. Identify whether revenue is already net of discounts/refunds and whether COGS already includes other expenses. Subtract each economic cost once. Keep unidentified shared advertising/overhead separate unless a documented allocation is supplied; do not distribute it arbitrarily by attractive ROAS.

Use totals for the same scope and horizon. Under the explicit component contract: net revenue = gross revenue − discounts − refunds; contribution before ads = net revenue − distinct COGS − fulfilment − payment fees; contribution after ads = contribution before ads − allocated ad spend. Negative net revenue or contribution can be real; report it with its definition. A missing cost is unknown, not zero, and prevents a complete contribution claim. A gross-revenue field already net of refunds must be normalized before using the helper, with the transformation documented.

Calculate gross and net revenue ROAS with their named numerators. Contribution break-even net-revenue ROAS = net revenue / pre-ad contribution only for positive net revenue and positive pre-ad contribution under stable observed cost mix. Zero/negative contribution does not have a meaningful positive advertising break-even ratio. Missing/zero ad spend makes ROAS unavailable. These are descriptive cost identities, not marginal response forecasts or target bids.

## Recommend economic checks

Rank material adverse contribution, uncertain allocations, immature returns and cost gaps. Identify whether a recommendation concerns ad allocation, merchandising, stock, pricing, returns or feed health; do not prescribe an unrequested price change. Repeat-customer value needs a separate supported cohort analysis. Report the table, explicit cost inclusions, missing overhead/future value, and a bounded next check. No company net-profit or causal incrementality claim follows from allocated contribution alone.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py profitability < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
