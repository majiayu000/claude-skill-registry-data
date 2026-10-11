---
name: cpq-pricing-rules
description: "Use this skill when configuring or troubleshooting Salesforce CPQ pricing: Price Rules, Price Conditions, Price Actions, Lookup Queries, Discount Schedules, Block Pricing, Percent of Total, and Contracted Prices. Trigger keywords: CPQ price rule, price action, discount schedule, block pricing, percent of total, contracted price, SBQQ__PriceRule__c, CPQ quote calculation engine, price waterfall. NOT for standard Salesforce pricebook pricing (use the products-and-pricebooks skill), CPQ product bundle configuration (use cpq-product-catalog-setup), or quote template/document setup."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Performance
  - Reliability
triggers:
  - "configure CPQ price rules to automatically set discounts on quote lines"
  - "discount schedule not applying correctly on CPQ quote when quantity changes"
  - "set up contracted pricing in CPQ so account-specific rates override list price"
  - "block pricing in CPQ to charge a fixed price per quantity range instead of per unit"
  - "percent of total pricing for a support or maintenance product priced as a percentage of other lines"
  - "CPQ price waterfall order and why a price rule is not applying as expected"
tags:
  - cpq
  - pricing
  - price-rules
  - discount-schedules
  - contracted-pricing
  - block-pricing
  - percent-of-total
  - quote-calculation
inputs:
  - "Business pricing model: volume tiers, flat discounts, contracted account rates, percentage-of-total products"
  - "Whether discounts are per-line or across the full order (volume vs. term-based discount schedules)"
  - "List of products that need block pricing or percent-of-total pricing methods"
  - "Accounts with contracted prices and the contract source (generated from contract activation or manual)"
  - "Required execution sequence for price rules if multiple rules interact"
outputs:
  - "Configured Price Rule records with Price Conditions and Price Actions"
  - "Discount Schedule records with tiers attached to products"
  - "Block Price records on products for quantity-range pricing"
  - "Contracted Price records for account-specific overrides"
  - "Documented price waterfall and evaluation order for all active price rules"
  - "Completed CPQ pricing configuration checklist"
dependencies:
  - cpq-product-catalog-setup
  - products-and-pricebooks
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-07
---

# CPQ Pricing Rules

Use this skill when configuring the Salesforce CPQ pricing engine: creating Price Rules that fire during quote calculation, building Discount Schedules for volume-based pricing, setting up Block Pricing for fixed-price quantity ranges, configuring Percent of Total products, and establishing Contracted Prices for account-specific rate overrides. This skill does not cover standard Salesforce Pricebook pricing or CPQ product catalog configuration.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the Salesforce CPQ managed package (`SBQQ__`) is installed. All CPQ pricing objects (`SBQQ__PriceRule__c`, `SBQQ__DiscountSchedule__c`, `SBQQ__ContractedPrice__c`, `SBQQ__BlockPrice__c`) require it.
- Understand the full pricing waterfall the business requires. CPQ applies pricing in this order: list price → contracted price → block pricing → discount schedules → price rules. Changes to any layer can be overwritten by a later layer if rules are not ordered correctly.
- Identify whether discounts are per-line, volume-based across the order, or account-specific contracted rates. Each requires a different CPQ mechanism.
- Determine the required execution order of price rules early. Two rules with the same Evaluation Order fire in undefined sequence — this is the most common source of inconsistent pricing bugs.
- Verify whether CPQ's debug logging is available in the org. The CPQ Calculator debug mode logs each pricing step to the browser console, which is essential for diagnosing waterfall issues.

---

## Core Concepts

### CPQ Quote Calculation Engine and the Price Waterfall

When a CPQ quote is saved or manually recalculated, the CPQ calculation engine runs synchronously and applies pricing in a defined sequence known as the price waterfall:

1. **List Price** — The `PricebookEntry.UnitPrice` for the product/pricebook combination.
2. **Contracted Price** — If an active `SBQQ__ContractedPrice__c` record exists for the Account + Product combination, it overrides the list price.
3. **Block Pricing** — If the product has `SBQQ__BlockPrice__c` records, per-unit pricing is replaced with the fixed price for the matching quantity range.
4. **Discount Schedules** — `SBQQ__DiscountSchedule__c` volume or term tiers apply an additional percentage discount.
5. **Price Rules** — `SBQQ__PriceRule__c` records fire in ascending Evaluation Order and can overwrite any field on the quote or quote line, including the net price.

Understanding this sequence is critical: a Price Rule that sets the unit price executes after contracted prices, so a contracted price can still be further modified by a price rule if the rule targets the correct field.

### Price Rules: Conditions, Lookup Queries, and Actions

A Price Rule (`SBQQ__PriceRule__c`) is the core mechanism for conditional pricing logic. Each rule has three parts:

**Price Conditions** (`SBQQ__PriceCondition__c`) define *when* the rule fires. Conditions evaluate fields on the Quote (`SBQQ__Quote__c`), Quote Line (`SBQQ__QuoteLine__c`), or a Lookup table. Supported operators include: equals, not equals, greater than, less than, contains. All conditions on a rule must be true for the rule to fire (AND logic). Multiple rules with OR logic require separate rule records.

**Lookup Queries** (`SBQQ__LookupQuery__c`) are optional. They pull values from a CPQ Lookup Object (`SBQQ__LookupData__c`) — a custom data table useful for pricing matrices (e.g., a tier rate that depends on both product family and contract term). The Lookup Query maps input fields from the quote line to rows in the data table and returns a result field that Price Actions can reference.

**Price Actions** (`SBQQ__PriceAction__c`) define *what* the rule does. Each action sets a target field on the quote or quote line to a value sourced from a static value, a field on the quote/line, or a Lookup result field. Common targets: `SBQQ__SpecialPrice__c` (the adjusted price), `SBQQ__Discount__c`, `SBQQ__AdditionalDiscount__c`.

**Evaluation Order** (`SBQQ__EvaluationOrder__c`) is a numeric field on each Price Rule. Rules fire in ascending numeric order. Rules with the same evaluation order fire in undefined sequence — always assign unique evaluation order values across all active price rules.

### Discount Schedules

A Discount Schedule (`SBQQ__DiscountSchedule__c`) applies tier-based discounts based on quantity or term. Tiers (`SBQQ__DiscountTier__c`) define the lower bound of each range and the discount percentage for that range.

**Volume-based** schedules: the applicable tier is determined by the quantity on the quote line. The entire line receives the tier's discount.

**Term-based** schedules: the applicable tier is determined by the subscription term in months. Used for term-length incentives.

Discount Schedules are attached to a product via `SBQQ__DiscountSchedule__c` on the Product2 record. They apply during the calculation engine run after block pricing.

### Block Pricing

Block Pricing (`SBQQ__BlockPrice__c`) replaces per-unit pricing with a fixed price for a given quantity range. When block pricing is active for a product, the CPQ engine does not multiply the unit price by quantity — instead it returns the fixed block price directly. This is the correct mechanism for software licensing tiers where 1–10 seats cost $500 flat, 11–25 cost $900 flat, etc.

Block Pricing records require: Product (`SBQQ__Product__c`), Pricebook (`SBQQ__Pricebook__c`), lower bound quantity (`SBQQ__LowerBound__c`), upper bound quantity (`SBQQ__UpperBound__c`), and price (`SBQQ__Price__c`).

**Important:** Block Pricing and Discount Schedules can coexist on the same product but will both apply, risking double-discounting. When Block Pricing is in use, Discount Schedules attached to the same product should typically be removed or the price rule should be designed to avoid stacking.

### Percent of Total Pricing

Products with `SBQQ__PricingMethod__c = 'Percent of Total'` are priced as a percentage of other line items on the quote. The `SBQQ__PercentOfTotalBase__c` field controls which lines are included in the base (Regular lines, all lines, or a specific product category). This is the correct mechanism for maintenance or support products priced as a percentage of the software they cover — no price rule is needed.

### Contracted Prices

`SBQQ__ContractedPrice__c` records establish account-specific pricing overrides. Each record links an Account, a Product, and a price (or discount). Contracted Prices are generated automatically when a CPQ contract is activated (from a Won Opportunity with a Subscription product), or they can be created manually.

The CPQ engine checks for a matching Contracted Price record during calculation and applies it before block pricing or discount schedules. A price rule can still modify the resulting price if it fires after the contracted price is applied.

---

## Common Patterns

### Pattern: Volume Discount via Discount Schedule

**When to use:** A product should receive a larger discount as the ordered quantity increases, using pre-defined tier breakpoints.

**How it works:**
1. Create a Discount Schedule record with `SBQQ__Type__c = 'Range'` and `SBQQ__DiscountUnit__c = 'Percent'`.
2. Create Discount Tier records for each quantity breakpoint: e.g., 1–10: 0%, 11–25: 10%, 26–100: 20%.
3. Set `SBQQ__DiscountSchedule__c` on the Product2 record to point to the schedule.
4. Test by adding the product to a CPQ quote at different quantities and confirming the correct tier fires.

**Why not the alternative:** Using a Price Rule to replicate volume tiers with multiple conditions is possible but creates maintenance overhead. Discount Schedules are the correct, first-class mechanism for quantity-based tier pricing and are easier to update without changing rule logic.

### Pattern: Conditional Price Rule with Lookup Matrix

**When to use:** The discount or price depends on a combination of quote attributes — for example, a rate that varies by product family AND contract term, requiring a matrix lookup rather than simple conditions.

**How it works:**
1. Create a CPQ Lookup Object (custom object with `SBQQ__` fields) with columns representing the matrix inputs (e.g., Product Family, Term) and the result (e.g., Discount).
2. Create records in the Lookup Object for each combination in the pricing matrix.
3. Create a Lookup Query that maps Quote Line fields (e.g., `SBQQ__ProductFamily__c`, `SBQQ__SubscriptionTerm__c`) to the lookup input columns.
4. Create a Price Rule with a Price Condition that always evaluates to true (or targets a specific product family), a Lookup Query reference, and a Price Action that sets `SBQQ__Discount__c` from the lookup result field.
5. Assign a unique Evaluation Order. Test with quote lines at multiple term/family combinations.

**Why not the alternative:** Hardcoding matrix values as multiple Price Conditions per rule creates a combinatorial explosion of rules. The Lookup Object pattern externalizes the matrix data, making it maintainable without rule changes.

### Pattern: Account Contracted Pricing

**When to use:** A specific account has negotiated rates that should always override list price for designated products.

**How it works:**
1. For contract-generated contracted prices: ensure CPQ contract activation is configured (`SBQQ__RenewedContract__c` flow, Contracted Price generation enabled in CPQ settings under Contracting).
2. For manual contracted prices: create `SBQQ__ContractedPrice__c` records directly, setting Account, Product, and the contracted price or discount.
3. Verify CPQ settings have "Generate Contracted Prices" enabled under Setup > Installed Packages > CPQ Settings > Contracting.
4. Test by creating a quote for the contracted account and confirming the line price shows the contracted rate, not the list price.

**Why not the alternative:** Using a Price Rule with an Account condition to hardcode account-specific rates creates a maintenance burden as accounts scale. Contracted Price records are the correct mechanism — they are account-data-driven, not rule-logic-driven.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Quantity-based tier discounts on a product | Discount Schedule with tiers | First-class CPQ mechanism; easier to maintain than rules |
| Fixed price for a quantity range (not per-unit) | Block Pricing records | Disables per-unit math; correct for seat-tier licensing |
| Support/maintenance product priced as % of software | `SBQQ__PricingMethod__c = 'Percent of Total'` | No rule needed; built-in pricing method |
| Account-specific negotiated rates | Contracted Price records | Account-data-driven; scales without rule proliferation |
| Pricing dependent on multiple quote attributes (matrix) | Price Rule + Lookup Query + Lookup Object | Externalizes matrix data; avoids rule explosion |
| Simple conditional discount (e.g., specific product family) | Price Rule with Price Conditions | Appropriate when logic is simple and stable |
| Multiple price rules that interact | Assign unique Evaluation Order values | Same evaluation order = undefined execution sequence |
| Block Pricing + Discount Schedule on same product | Remove or disable one; or use Price Rule to control | Both apply during waterfall — double-discounting risk |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Map the full pricing model before touching configuration.** Document all pricing mechanisms required: which products use discount schedules, block pricing, percent of total, contracted pricing, or price rules. Identify any interactions between mechanisms (e.g., a product that has both block pricing and a price rule). This prevents waterfall ordering surprises.
2. **Configure base pricing mechanisms first.** Set up Discount Schedules, Block Price records, and Percent of Total pricing methods on products before creating Price Rules. These are evaluated earlier in the waterfall and establishing them first makes it easier to test price rule behavior in isolation.
3. **Create Contracted Price records for applicable accounts.** If contracted pricing is required, set up Contracted Price records (manually or via contract activation) before configuring price rules that interact with contracted rates. Test with a quote for a contracted account to confirm the correct base price before rules are applied.
4. **Build Price Rules with unique Evaluation Orders.** For each conditional pricing requirement, create a Price Rule with explicit, unique Evaluation Order values (use increments of 10 to allow future insertion). Create Price Conditions for the when logic, Lookup Queries if matrix data is needed, and Price Actions for the field targets. Do not create rules with the same Evaluation Order.
5. **Test each rule in isolation, then in combination.** Create a test quote and add products that trigger each rule. Verify the correct field is set to the correct value. Then test quotes that trigger multiple rules and confirm the combined result matches the intended waterfall output. Use CPQ Calculator debug logging (available via browser console when CPQ debug mode is enabled) to trace which rules fired and in what order.
6. **Document evaluation order and field targets for every active rule.** Record the purpose, Evaluation Order, Conditions, and Action targets of every Price Rule in a pricing design document. This is the single highest-value maintenance artifact — undocumented evaluation orders are the primary source of pricing regression bugs.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All active Price Rules have unique Evaluation Order values — no two rules share the same order number
- [ ] Each Price Rule has at least one Price Condition and at least one Price Action
- [ ] Price Actions reference valid field API names on the Quote or Quote Line
- [ ] Discount Schedules have at least one Discount Tier with a defined lower bound and discount percentage
- [ ] Block Price records have non-overlapping quantity ranges for each product/pricebook combination
- [ ] Contracted Price records are linked to the correct Account and Product, and CPQ Settings has "Generate Contracted Prices" enabled
- [ ] Percent of Total products have `SBQQ__PricingMethod__c = 'Percent of Total'` and the correct `SBQQ__PercentOfTotalBase__c` value
- [ ] Waterfall has been tested end to end with a real quote in a sandbox covering all rule combinations
- [ ] Evaluation Order and field targets for all Price Rules are documented

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Price Rules with the same Evaluation Order produce unpredictable results** — CPQ does not guarantee execution order between rules sharing the same `SBQQ__EvaluationOrder__c` value. The result changes between quote saves. Always use unique evaluation order values, spaced with gaps (10, 20, 30) to allow future insertions.
2. **Block Pricing disables per-unit math entirely** — When a `SBQQ__BlockPrice__c` record matches the quantity range, CPQ returns the block price as-is, ignoring the unit price. If a Discount Schedule is also attached to the product, the schedule's percentage discount still applies to the block price, causing unintended double-pricing reduction. Remove the Discount Schedule from block-priced products unless stacking is explicitly intended.
3. **Contracted Prices do not cascade to related products** — A `SBQQ__ContractedPrice__c` on a bundle parent does not automatically apply to bundle components. Each component product needs its own Contracted Price record if a contracted rate is required at the component level.
4. **Price Actions targeting the wrong field in the waterfall can be silently overwritten** — If a Price Action sets `SBQQ__ListPrice__c` but a later waterfall step recalculates from that field, the action's effect is lost. The safest target for a rule that should produce a final net price is `SBQQ__SpecialPrice__c`, which sits lower in the waterfall. Review the CPQ price field documentation before choosing a target field.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Price Rule records | `SBQQ__PriceRule__c` with linked Conditions, Lookup Queries (if used), and Actions |
| Discount Schedule records | `SBQQ__DiscountSchedule__c` with `SBQQ__DiscountTier__c` records attached to products |
| Block Price records | `SBQQ__BlockPrice__c` quantity-range records attached to products |
| Contracted Price records | `SBQQ__ContractedPrice__c` account-specific overrides |
| Pricing design document | Evaluation Order table, field targets, and waterfall diagram for all active rules |
| CPQ pricing configuration checklist | Completed checklist from this skill |

---

## Related Skills

- cpq-product-catalog-setup — Use to configure product bundles and product rules before setting up pricing
- products-and-pricebooks — Use for standard Pricebook and PricebookEntry setup that CPQ builds on top of
- cpq-vs-standard-products-decision — Use during requirements gathering to confirm whether CPQ pricing is the right tool
- quote-to-cash-requirements — Use during requirements gathering to map pricing requirements to CPQ mechanisms
