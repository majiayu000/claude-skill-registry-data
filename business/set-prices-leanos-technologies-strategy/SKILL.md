---
name: set-prices
description: Recommend prices for each offer's exact entitlement, with unit, currency and payment timing, the commercial rules (discounts, anchors, tests, exceptions) within declared authority, and the economic basis and expected response, and write the price-book candidate. Use when offers are new or changed, when no price has been set, or when a purchase observation, cost or alternative price changes the basis of a price.
---

# set-prices

**Transformation:** `offer-catalogue` × buyer value and purchasing context × alternatives × economic scenarios → [`price-book`](../../../../.group/contracts/price-book.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use it

- An offer exists without a price, or its entitlement changed.
- A purchase observation, a delivery cost, or an inspected alternative price changes the basis of a current price.
- A discount, test or exception rule is needed.

A missing owner price is the normal starting point, not a blocker: the result is a reasoned proposed price.

## Inputs and authority

| Input | Use | When missing |
| --- | --- | --- |
| `offer-catalogue` | The exact entitlement priced | Nothing to price; name the offer decision needed |
| `revenue-model` | Charging unit and payment timing per exchange | Name the unit you price per, and the exchange design-revenue-model must confirm |
| `market-landscape` | Alternatives and their inspected prices | Reason from the status-quo alternative; no competitor rate is quoted |
| `customer-knowledge` | Value indications, willingness-to-pay observations, purchasing constraints | Value terms stay hypotheses with the observation that would test them |
| `unit-economics` (Finance) | Observed delivery costs and fees | Cost drivers stay `unknown`; contribution is computed only from known inputs |
| `autonomy-policy`, `decision-rights` | Who may approve prices and concessions, and their bounds | Rules carry `Authority: owner` until a delegation exists |

You recommend prices and rules. Accepted prices come only from the declared decider. A recommended price is never evidence of willingness to pay.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Fix what is being priced

For each offer: entitlement, charging unit (exactly the revenue-model unit), currency, payment timing, eligibility and purchasing constraints. Compare alternatives only on equivalent scope and time ([price, packaging, response and friction §1](../../../knowledge/price-packaging-response-and-friction.md)): a one-off licence against a monthly tool is compared over the period the buyer would use it.

### 2. Develop the price from value, alternatives and delivery economics

Build the reasoning, then the number:
- **Reference value:** what the buyer's next-best alternative costs them, in money or time. Payer value is only the part that returns to the payer ([payer, value and payment §1](../../../knowledge/payer-value-and-payment.md)).
- **Differentiation value:** what the offer adds or removes compared with that alternative (from `differentiation`).
- **Delivery floor:** the variable cost of fulfilling the entitlement. With known inputs, compute contribution with `python3 workers/strategy/business-model-designer/tools/commercial.py contribution --price "{amount}" --fee "{rate + fixed}"|none|unknown --variable-cost NAME=VALUE|none`; the fee and each variable cost are stated, never defaulted, and an unknown input returns `unknown` with its name.
- **Purchase context:** how this payer pays (card, invoice, approval threshold) and what amount crosses a friction line.

Choose an amount below the plausible value ceiling and above the delivery floor where both are known, positioned for the commercial role of the offer (entry, core, scoped service). State why that amount is worth trying, which consideration fixed it, and which observation would move it. When value and cost are both weakly known, recommend the price as a bounded commercial test with its period and its decision rule.

Decision rules:
- Recommend a price for every requested offer. `unknown` is acceptable only when a named material decision prevents a useful recommendation (the entitlement itself is undecided), and the row names that decision.
- A free offer states its declared purpose, delivery costs and support boundaries, consistent with the owner's policy; it need not profit by itself. Free pricing alone does not imply an upgrade path, and full usefulness is not itself a reason to charge.
- Use anchors only when the comparison is accurate and helps the buyer decide.
- A public price claim needs an inspected source with its date; otherwise leave it out.
- Lifetime value is never inferred from unobserved retention.

### 3. Examine response and economics under scenarios

Write one row per material scenario or assumption in Economic basis and response: the relationship (with the expression where calculated), its basis in Basis, the consequence for the price, and the observation that would change it. A scenario keeps its premises: "if conversion takes one working session" stays conditional in every consumer. An illustrative figure never substantiates a margin.

### 4. Write commercial rules within authority

Each discount, anchor, test or exception has a reason, eligibility, bound, expiry or decision point, and the authority that approves it. Check a proposed concession with `python3 workers/strategy/business-model-designer/tools/commercial.py discount --list "{price}" --discount "{d}" --bound "{bound}" [--floor "{floor}"]`; exit 1 means it is outside authority and needs that authority's decision. A discount that makes a fixed-scope service unprofitable to deliver is outside the rule whatever its percentage.

### 5. Connect

State what Engagement can sell now (accepted prices) and what awaits acceptance (proposed prices), and the first purchase observation that will confirm or move each price.

## Defects to detect and correct

| Defect | Correction |
| --- | --- |
| An offer has no price row | Add a recommended price, `free` with its role, or `unknown` with the deciding question |
| Price unit differs from the revenue-model unit | Change the unit, or return the unit question to design-revenue-model |
| A price labelled as owner-set without an owner quote | Quote the owner material, or label `[proposed]` |
| Unused but known-free usage treated as willingness to pay | Record it as usage; willingness to pay stays a hypothesis |
| A margin argued from a number with no origin | Replace with `unknown` and the driver's effect on the choice |
| A discount without bound or authority | Add both, or remove the rule |
| Blank prices because none were supplied | Develop the recommendation; blanks block the offer |

Run `python3 workers/strategy/.group/tools/check.py {strategy-dir} --owner-material {paths}`: rules PRICED and UNIT check every offer is priced and units match the revenue model; ARITH checks pasted expressions.

## Output

A candidate at `venture/{v}/strategy/candidate/price-book.md`, recorded in the request's work-result.

Illustrative fixture: fictional venture; the example supplies USD as a reversible test-market assumption. The entitlement is settled and the owner has supplied no price.

```markdown
## Conclusion
Test the desktop licence and one template conversion at the proposed prices below, with the template pack free. These prices make a concrete commercial choice available; measure conversion effort before accepting service orders.

## Prices
| ID | Offer | Eligibility | Amount | Price status | Charging unit | Payment timing | Applicability | Basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRC-1 | OFR-2 | Independent inspectors | 99 USD | proposed | licence | At purchase | First offer cycle | [proposed] reversible USD test; repeated report production gives the licence greater scope than one conversion |
| PRC-2 | OFR-3 | Licence buyers | 49 USD | proposed | conversion | At agreed start | One inspected template | [proposed] bounded entry service; confirm delivery effort on the sample |
| PRC-3 | OFR-1 | Anyone | free | accepted | n/a: free | n/a | Ongoing | [owner: "The free template pack stays free."] |

## Economic basis and response
| Scenario | Relationship | Basis | Consequence | Would change the price |
| --- | --- | --- | --- | --- |
| Licence plus conversion | 99 USD + 49 USD = 148 USD | [derived: proposed licence plus proposed conversion]; [proposed] test prices | Gives a concrete combined purchase to evaluate | Buyer comparisons or measured conversion effort |
| Conversion contribution | unknown: processing fee and delivery cost need measurement | [hypothesis] service economics; measure the representative conversion and inspect processor terms | Bound scope and confirm cost before service acceptance | Observed cost exceeds the tested price |
```

The price proposal lets the owner assess a concrete offer. Research the relevant purchase context and measure delivery cost; revise the amount or currency when that evidence changes the decision. The test supplies no claim of willingness to pay.

## Recovery

| Condition | Next action |
| --- | --- |
| No value or WTP evidence | Recommend a bounded test price; name the observation and decision point |
| No cost data | Keep contribution `unknown`; scope the entitlement so cost is bounded; name the measurement for Finance |
| Unit question open in the revenue model | Price per the most likely unit, name the alternative in one line, and return the question to design-revenue-model |
| Requested concession exceeds the bound | Prepare the concession with its effect and route it to the authority that set the bound |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
