---
name: design-offers
description: Construct the purchasable offers - promised outcome, included scope and customer contribution, delivery status and path to first value, and any variant, entry offer, trial or guarantee with its purpose - and write the offer-catalogue candidate. Use when a revenue model exists or changed, when target opportunities or deliverable capabilities change, or when buyers do not understand or cannot adopt the current offer.
---

# design-offers

**Transformation:** `revenue-model` × target `opportunities` × deliverable capabilities → [`offer-catalogue`](../../../../.group/contracts/offer-catalogue.md).

The document follows its contract and the group's [document rules](../../../../.group/contracts/document-rules.md).

## When to use it

- A revenue-model exchange exists and no offer implements it, or the exchange changed.
- A target opportunity or a delivery capability changed (a capability shipped, slipped or was withdrawn).
- Buyers stall between interest and purchase, or between purchase and first value.

## Inputs and authority

| Input | Use | When missing |
| --- | --- | --- |
| `revenue-model` | The exchange each offer implements | Design the offer and mark the exchange it needs as an open dependency for design-revenue-model |
| `opportunities`, `target-segments` | The outcome the buyer seeks and the buying situation | Reason from owner material; the outcome is a hypothesis |
| `documentation`, `roadmap`, owner material | What can be delivered now and what later | Only what owner material or documentation shows as working counts as available |
| `differentiation` | Why this offer beats the buyer's alternative | State the comparison as a hypothesis |
| Owner material naming commercial levels or units | Which levels the catalogue must cover | Cover the targets' needs; name the level question for the owner |

You propose offers, names, bundles and terms. They stay proposals until accepted. Governance approves legal wording; Product owns capability evidence.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

### 1. Define the outcome and the scope to first value

For each target opportunity write: the outcome the buyer wants, the smallest scope that reaches first value, what the customer must supply, and what lies outside the purchase. Scope by meaningful need and delivery boundary ([entitlement, delivery and economics §1](../../../knowledge/entitlement-delivery-and-economics.md)): every included element is an obligation with a cost driver.

What to notice:
- The buyer's switching cost (their existing template, data, habits). Removing it can matter more than any feature.
- Setup effort before first value. A long setup needs a service, a guided start or a smaller first scope.
- Whether a capability the offer needs is available, committed or only possible.

### 2. Construct offers from real capability

Build offers from what the venture can deliver and what the target needs. Develop names and bundles with their rationale in the row’s basis cell and their proposed status in Status. Cover the commercial levels the venture source names, distinguishing `available`, `proposed` and `future` in the Status column. A complete future range is not a prerequisite for releasing the first useful offer.

Decision rules:
- Each promised element is deliverable now, or sold on a stated future condition ([§2](../../../knowledge/entitlement-delivery-and-economics.md)). A roadmap capability never enters the entitlement silently.
- Introduce variants or tiers only when needs, entitlements, purchasing conditions or delivery costs differ ([price, packaging, response and friction §3](../../../knowledge/price-packaging-response-and-friction.md)). Otherwise one offer.
- A simple direct purchase is often right; never add subscriptions, tiers or guarantees by default.

### 3. Reduce purchase and adoption friction

Use the friction analysis in [price, packaging, response and friction §4](../../../knowledge/price-packaging-response-and-friction.md):
- A free standalone product delivers its stated outcome within its own boundaries. A demonstration, trial or entry component supports a stated evaluation or commercial purpose. Choose the form from the owner's policy and customer need; free pricing alone does not imply an upgrade path. State delivery costs and support boundaries for either form.
- Trial or pilot: when the decision-maker needs proof in use and setup cost is bearable for both sides.
- Guarantee: when fit is uncertain at purchase and the venture can bear refunds; not for delivered services.
Each goes in Variants and conditions with its purpose and delivery condition.

### 4. Establish delivery readiness and terms

Fill Delivery and first value for every offer: delivery status, prerequisites, path to first value, customer contribution, support boundary and exclusions. Quantitative delivery claims ("converted in two days") need a basis; otherwise state the scope without the number. Proposed commercial conditions are written as proposals with `Approval` naming who approves them.

### 5. Compare with the buyer's alternative

For each offer, say why buying beats the buyer's actual alternative (from `differentiation`). If the offer does not beat it, change scope or path to value before pricing.

### 6. Connect

set-prices prices each offer's exact entitlement; Product and Customers fulfil it; Engagement sells within its scope. Name the capability dependencies that prioritize-bets must sequence.

## Defects to detect and correct

| Defect | Correction |
| --- | --- |
| An offer includes a planned capability as available | Move it to a stated future condition, or set Status `future` |
| A tier or variant with no decision-relevant purpose | Remove it, or state the need it separates |
| An offer's scope or conditions conflict with its declared purpose or the owner's policy | Reconcile the offer with that purpose and policy. A free product fully satisfying its intended need is not itself a defect. Do not narrow it or make it paid merely to induce another purchase. |
| A fixed-price service with unbounded scope | Bound the deliverable and the customer's inputs; extra work is a separate purchase |
| A new name or term presented as existing | Label `[proposed]` |
| An offer with no revenue-model exchange | Reference one, or name the exchange design-revenue-model must add |

Run `python3 workers/strategy/.group/tools/check.py {strategy-dir} --owner-material {paths}`; references to targets, opportunities and the revenue model must resolve.

## Output

A candidate at `venture/{v}/strategy/candidate/offer-catalogue.md`, recorded in the request's work-result.

Illustrative fixture: fictional venture.

```markdown
## Conclusion
The desktop app makes an inspector's findings usable as a client report; template conversion carries their existing reporting approach into it. The free template pack lets a prospective buyer inspect the result.

## Offers
| ID | Offer | Target | Opportunity | Promised outcome | Entitlement | Revenue model | Status | Basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFR-1 | Template pack | TGT-1 | OPP-1 | Inspect a useful report format | Downloadable templates | none | available | [owner: "The free template pack stays free."] |
| OFR-2 | Desktop app | TGT-1 | OPP-1 | Findings become a client-ready report | Use of the purchased version | RM-1 | available | [owner: "The desktop app works"]; [proposed] licence entitlement |
| OFR-3 | Template conversion | TGT-1 | OPP-2 | Use the inspector's own report structure | One existing template converted | RM-2 | proposed | [owner: "convert an inspector's existing report template into ours"]; [proposed] bound and confirm delivery on a sample |

## Delivery and first value
| Offer | Delivery status | Prerequisites | First value | Customer contribution | Support and exclusions | Basis |
| --- | --- | --- | --- | --- | --- | --- |
| OFR-2 | Available | Compatible computer | Produce a complete report | Inspection findings | Purchased version; phone photo sync is future | [owner: "The desktop app works"] [owner: "Photo sync from phones is planned for next year; it does not exist yet."] |
```

The buyer can inspect the report, understand the entitlement and see the path to first value.

## Recovery

| Condition | Next action |
| --- | --- |
| Capability status unclear | Treat as not available; name the Product evidence that would confirm it |
| No revenue model yet | Design the offer; list the exchange it needs for design-revenue-model in the answer |
| Owner names a commercial level the venture cannot yet deliver | Record it as `future` with the condition that makes it available |
| Legal wording requested | Write the proposed condition; name Governance for the approved wording |

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
