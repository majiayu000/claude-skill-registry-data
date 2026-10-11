---
name: cpq-data-model
description: "Use when querying, mapping, or building against Salesforce CPQ managed-package objects (SBQQ__ namespace): Quote, QuoteLine, QuoteLineGroup, DiscountSchedule, PriceRule, Subscription. Trigger keywords: SBQQ__Quote__c, QuoteLineModel, CPQ object graph, CPQ subscription, CPQ price rule. NOT for standard Quote/QuoteLineItem, Industries CPQ (Vlocity), or standard Product/Pricebook data model."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
  - Operational Excellence
triggers:
  - "How do I query CPQ quote lines and their prices programmatically?"
  - "What is the relationship between SBQQ__Quote__c and SBQQ__Subscription__c?"
  - "I need to update CPQ prices or discounts via Apex — what objects should I touch?"
  - "How does CPQ store contracted products and renewal quotes?"
  - "What CPQ objects are created when a quote is contracted?"
tags:
  - cpq
  - sbqq
  - quote
  - quotelinemodel
  - subscription
  - pricing
  - data-model
inputs:
  - "Whether the org has Salesforce CPQ (SBQQ) managed package installed"
  - "The operation type: read-only query, programmatic write, contract creation, or renewal"
  - "Which part of the CPQ lifecycle is in scope: quoting, ordering, contracting, or renewal"
outputs:
  - "Correct SBQQ__ object names, field references, and SOQL queries"
  - "Guidance on when to use CPQ Quote API (QuoteModel/QuoteLineModel) vs direct DML"
  - "Object relationship map for the full SBQQ__ graph"
  - "Checklist for validating CPQ data model usage in Apex or Flow"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# CPQ Data Model

This skill activates when work involves Salesforce CPQ managed-package objects in the SBQQ__ namespace — quoting, pricing, contracting, or renewal. It provides the complete SBQQ__ object graph, explains why standard Quote/QuoteLineItem is not the quoting layer in CPQ orgs, and defines when programmatic operations must use the CPQ Quote API instead of direct DML.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the org has the Salesforce CPQ managed package installed (namespace `SBQQ`). Check Setup > Installed Packages for "Salesforce CPQ" or query `SELECT Id FROM SBQQ__Quote__c LIMIT 1` in Developer Console.
- The most common wrong assumption: practitioners believe `Quote` and `QuoteLineItem` are the CPQ quoting objects. They are not. CPQ installs a parallel object graph under the SBQQ__ namespace. The standard `Quote` may be synced from a CPQ quote for downstream processes but does not hold pricing logic.
- Direct DML on CPQ-managed calculated fields (e.g., `SBQQ__NetPrice__c`, `SBQQ__RegularPrice__c`, `SBQQ__CustomerPrice__c`) bypasses the CPQ pricing engine and corrupts quote totals. Programmatic writes to quote lines require the CPQ Quote API.
- CPQ governor limits: the pricing engine runs synchronously during save; complex quotes with many lines, price rules, and discount schedules can approach CPU time limits. Keep price rule conditions tightly scoped.

---

## Core Concepts

### The SBQQ__ Object Graph

Salesforce CPQ installs a self-contained managed-package object graph with the `SBQQ__` namespace prefix. The top-level quoting object is `SBQQ__Quote__c`, not `Quote`. Every downstream CPQ object rolls up to it.

**Primary quoting objects:**
- `SBQQ__Quote__c` — The CPQ quote. Linked to an Opportunity via `SBQQ__Opportunity2__c`. Contains header-level pricing fields (`SBQQ__NetAmount__c`, `SBQQ__Discount__c`) and subscription term fields (`SBQQ__StartDate__c`, `SBQQ__EndDate__c`, `SBQQ__SubscriptionTerm__c`).
- `SBQQ__QuoteLine__c` — One record per product on the quote. Key fields: `SBQQ__Product__c` (lookup to Product2), `SBQQ__Quantity__c`, `SBQQ__ListPrice__c`, `SBQQ__CustomerPrice__c`, `SBQQ__NetPrice__c`, `SBQQ__Discount__c`. Parent is `SBQQ__Quote__c` via `SBQQ__Quote__c` field.
- `SBQQ__QuoteLineGroup__c` — Optional grouping container for quote lines. Useful for multi-product bundles and segment-level subtotals. Quote lines reference a group via `SBQQ__Group__c`.

**Pricing and discount objects:**
- `SBQQ__PriceRule__c` — Conditional pricing automation. Each price rule contains one or more `SBQQ__PriceCondition__c` records (when to fire) and `SBQQ__PriceAction__c` records (what field to set and to what value). Evaluated by the pricing engine on quote save.
- `SBQQ__DiscountSchedule__c` — Volume or term-based discount tiers. Linked to a product or price book entry. Contains `SBQQ__DiscountTier__c` child records that define discount percentages by quantity or term bands.

**Contract and subscription objects:**
- `SBQQ__Subscription__c` — Created from quote lines when a CPQ quote is contracted (via the "Contract" action on a closed-won opportunity). One `SBQQ__Subscription__c` record is created per contracted quote line that has `SBQQ__SubscriptionPricing__c` set on Product2. The subscription records link to the standard `Contract` object via `SBQQ__Contract__c`.
- `SBQQ__Asset__c` (optional) — Tracks purchased assets; used in amendment and renewal flows when asset-based quoting is enabled.

### CPQ Quote API: QuoteModel and QuoteLineModel

For any programmatic write to a CPQ quote — adding lines, changing quantities, applying discounts — the CPQ Quote API must be used instead of direct DML. The API is invoked via a SBQQ namespace Apex class call or via the REST endpoint `https://<instance>/services/apexrest/SBQQ/ServiceRouter`.

- **`QuoteModel`** — A JSON-serializable Apex class (`SBQQ.QuoteModel`) that wraps an `SBQQ__Quote__c` record and its related quote lines and groups. It is the in-memory representation the CPQ pricing engine operates on.
- **`QuoteLineModel`** — A JSON-serializable class (`SBQQ.QuoteLineModel`) that wraps a single `SBQQ__QuoteLine__c` record, including its product configuration and pricing inputs.

The typical read-calculate-save flow:
1. Call `SBQQ.QuoteService.read(quoteId)` to retrieve a `QuoteModel`.
2. Mutate inputs (quantities, discounts) on the `QuoteLineModel` objects inside.
3. Call `SBQQ.QuoteService.calculate(quoteModel, callbackClass)` to trigger the pricing engine asynchronously.
4. In the callback, call `SBQQ.QuoteService.save(quoteModel)` to persist the calculated output back to `SBQQ__Quote__c` and `SBQQ__QuoteLine__c`.

Skipping the calculate step and writing directly to `SBQQ__NetPrice__c` corrupts the quote because rollup formulas and approval thresholds depend on engine-calculated values.

### Contract-to-Subscription Relationship

When a CPQ quote is contracted:
1. The Opportunity is marked Closed Won with a primary quote set (`SBQQ__Primary__c = true` on `SBQQ__Quote__c`).
2. The "Contract" action creates a standard `Contract` record and links it to the quote via a custom field.
3. For each `SBQQ__QuoteLine__c` with a subscribed product, one `SBQQ__Subscription__c` is created. It stores `SBQQ__StartDate__c`, `SBQQ__EndDate__c`, `SBQQ__Quantity__c`, and `SBQQ__NetPrice__c` from the contracted line.
4. Renewals are generated from `SBQQ__Subscription__c` records, not from the original quote lines. The renewal quote's lines pull `SBQQ__RenewalPrice__c` from each subscription.

---

## Common Patterns

### Pattern: Query CPQ Quote with Lines for Reporting

**When to use:** Read-only reports, validations, or integrations that need the full quote header and line details without triggering recalculation.

**How it works:**

```soql
SELECT
    Id,
    Name,
    SBQQ__Opportunity2__c,
    SBQQ__NetAmount__c,
    SBQQ__StartDate__c,
    SBQQ__EndDate__c,
    SBQQ__SubscriptionTerm__c,
    SBQQ__Status__c,
    (
        SELECT
            Id,
            SBQQ__ProductName__c,
            SBQQ__Quantity__c,
            SBQQ__ListPrice__c,
            SBQQ__CustomerPrice__c,
            SBQQ__NetPrice__c,
            SBQQ__Discount__c,
            SBQQ__Group__c
        FROM SBQQ__LineItems__r
    )
FROM SBQQ__Quote__c
WHERE SBQQ__Opportunity2__c = :opportunityId
```

**Why not the alternative:** Querying `Quote` and `QuoteLineItem` returns standard quote objects. In a CPQ org the standard Quote may not exist or may have stale synced data. Pricing always lives on `SBQQ__Quote__c`.

### Pattern: Programmatic Quote Line Update via CPQ Quote API

**When to use:** Apex automation that must change quantity or discount on an existing CPQ quote and have prices correctly recalculated.

**How it works:**

```apex
// 1. Read the quote into a QuoteModel
SBQQ.QuoteModel quoteModel = SBQQ.QuoteService.read(quoteId);

// 2. Mutate the first line quantity
quoteModel.lineItems[0].record.SBQQ__Quantity__c = 5;

// 3. Calculate (async — provide a callback class name)
String quoteJSON = JSON.serialize(quoteModel);
SBQQ.QuoteService.calculate(quoteJSON, 'MyQuoteCalculatorCallback');

// 4. In the callback implementation:
// global class MyQuoteCalculatorCallback implements SBQQ.QuoteCalculatorPlugin {
//     global void onAfterCalculate(SBQQ.QuoteModel quote) {
//         SBQQ.QuoteService.save(quote);
//     }
// }
```

**Why not the alternative:** Direct DML `update new SBQQ__QuoteLine__c(Id=..., SBQQ__Quantity__c=5)` will save the quantity but will NOT recalculate `SBQQ__NetPrice__c`, `SBQQ__CustomerPrice__c`, or the quote-level `SBQQ__NetAmount__c`. The quote totals become stale and approval rules may fire incorrectly.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Read CPQ quote data for a report or integration | SOQL on `SBQQ__Quote__c` / `SBQQ__QuoteLine__c` | Direct query is safe for reads; no pricing engine involved |
| Update quantity or discount on an existing quote | CPQ Quote API (QuoteModel/QuoteLineModel) | Ensures pricing engine recalculates all derived fields |
| Create a net-new quote programmatically | CPQ Quote API with `SBQQ.QuoteService.save()` | Required for product configuration and bundle resolution |
| Query contracted subscriptions for renewal | SOQL on `SBQQ__Subscription__c` with `SBQQ__Contract__c` lookup | Subscriptions, not quote lines, are the source of truth for active terms |
| Check if a product has volume discounts | Query `SBQQ__DiscountSchedule__c` and `SBQQ__DiscountTier__c` | Discount schedules are managed-package objects, not standard pricebook entries |
| Apply conditional pricing logic | Configure `SBQQ__PriceRule__c` with conditions and actions | Price rules fire during the CPQ save event; do not implement pricing in Apex triggers |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm CPQ is installed** — Verify the SBQQ__ namespace exists in the org (check Installed Packages or run a SOQL query on `SBQQ__Quote__c`). Do not proceed with SBQQ__ object references if CPQ is not installed.
2. **Identify the operation type** — Determine whether the task is read-only (SOQL), programmatic write (CPQ Quote API), contract creation, or renewal. Each path has different object entry points and constraints.
3. **Map the relevant objects** — For quoting work, start at `SBQQ__Quote__c`. For pricing logic, check `SBQQ__PriceRule__c` and `SBQQ__DiscountSchedule__c`. For subscription/renewal work, start at `SBQQ__Subscription__c` joined to `Contract`.
4. **Avoid direct DML on calculated fields** — If the task involves changing prices, quantities, or discounts, route through the CPQ Quote API (`SBQQ.QuoteService.read`, `calculate`, `save`). Flag any direct DML on `SBQQ__NetPrice__c`, `SBQQ__CustomerPrice__c`, or `SBQQ__RegularPrice__c` as a defect.
5. **Validate field-level security for CPQ objects** — CPQ objects require separate permission set assignments. Confirm the running user has access to the relevant SBQQ__ objects and fields before querying or writing.
6. **Test with the CPQ pricing engine in a sandbox** — Changes to price rules, discount schedules, or quote line fields must be validated in a sandbox with CPQ fully configured. Unit tests that mock `SBQQ.QuoteService` are required for Apex automation.
7. **Check for managed-package version constraints** — Some CPQ API behaviors differ between CPQ package versions. Note the installed version and check the CPQ Release Notes for deprecation notices on any API class or method used.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All quote references use `SBQQ__Quote__c`, not `Quote` or `QuoteHeader`
- [ ] All quote line references use `SBQQ__QuoteLine__c`, not `QuoteLineItem`
- [ ] Any programmatic price/quantity/discount write routes through the CPQ Quote API
- [ ] No direct DML on `SBQQ__NetPrice__c`, `SBQQ__CustomerPrice__c`, or `SBQQ__RegularPrice__c`
- [ ] SOQL relationship queries use the correct child relationship names (e.g., `SBQQ__LineItems__r`)
- [ ] Subscription references use `SBQQ__Subscription__c`, not standard `Asset` or `OrderItem`
- [ ] User permissions include CPQ permission sets for SBQQ__ object access

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Standard Quote vs SBQQ__Quote__c confusion** — In CPQ orgs the standard `Quote` object may exist (synced from CPQ) but is NOT the pricing source of truth. Writing prices to standard `Quote` or `QuoteLineItem` has no effect on CPQ-calculated values and will be overwritten on the next CPQ save.
2. **Direct DML corrupts CPQ totals** — Updating `SBQQ__NetPrice__c` directly via DML saves the value but does not trigger the CPQ pricing engine. The quote-level `SBQQ__NetAmount__c` rollup becomes stale. Approval rules that evaluate `SBQQ__NetAmount__c` may fire incorrectly or not at all.
3. **Child relationship names are namespace-prefixed** — The relationship from `SBQQ__Quote__c` to `SBQQ__QuoteLine__c` is traversed as `SBQQ__LineItems__r`, not `QuoteLineItems`. Using the wrong relationship name in SOQL silently returns zero rows rather than throwing an error.
4. **Subscriptions are per-line, not per-quote** — When a quote is contracted, one `SBQQ__Subscription__c` is created for each contracted line with a subscription-type product. Developers expecting a single subscription per contract are surprised to find N subscription records for N lines.
5. **Price rules fire on every CPQ save, not just API calls** — `SBQQ__PriceRule__c` records with no well-scoped conditions execute against every line on every save. A poorly scoped price rule can cause unexpected price overrides and CPU timeout in large quotes.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| SOQL query template | Ready-to-use queries for `SBQQ__Quote__c` with lines, groups, and subscriptions |
| CPQ Quote API code sketch | Apex pattern for read-calculate-save using `SBQQ.QuoteService` |
| Object relationship map | Reference listing of SBQQ__ objects, their parent/child relationships, and key fields |
| CPQ data model checklist | Review checklist for Apex, Flow, or integration code that touches CPQ objects |

---

## Related Skills

- `architect/cpq-vs-standard-products-decision` — When to choose Salesforce CPQ vs standard Products/Pricebooks; covers the decision criteria that leads to the SBQQ__ object graph.
- `admin/cpq-quote-templates` — CPQ quote template configuration using `SBQQ__QuoteTemplate__c` and `SBQQ__LineColumn__c`; references SBQQ__ objects built by this skill.
- `admin/contract-and-renewal-management` — CPQ contract and renewal workflow; builds on the SBQQ__Subscription__c and Contract relationship documented here.
- `omnistudio/industries-cpq-vs-salesforce-cpq` — Decision guidance for orgs evaluating Industries CPQ (Vlocity) vs Salesforce CPQ; clarifies namespace differences.
