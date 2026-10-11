---
name: cpq-guided-selling
description: "Use this skill when configuring or troubleshooting the Salesforce CPQ Guided Selling wizard: building Quote Process records, defining ProcessInput questions that filter products by field value, mapping user responses to Product2 classification fields, and choosing the right search type (Standard, Enhanced, or Custom). Trigger keywords: CPQ guided selling, quote process wizard, product selection wizard, SBQQ__QuoteProcess__c, SBQQ__ProcessInput__c, guided product selection, auto select product, product search plugin. NOT for OmniStudio product selection flows, standard Salesforce pricebook product browsing, CPQ product bundle configuration, or CPQ pricing rules."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
triggers:
  - "set up a guided product selection wizard in CPQ so reps answer questions to find matching products"
  - "CPQ guided selling not filtering products correctly when rep answers the wizard questions"
  - "configure SBQQ__QuoteProcess__c with ProcessInput records to drive product recommendations"
  - "custom classification field on Product2 not working in guided selling filter"
  - "guided selling wizard auto-selects wrong product or adds duplicate lines to the quote"
  - "choose between Standard, Enhanced, or Custom search type in CPQ guided selling"
  - "guided selling shows no products even though products match the answers rep entered"
tags:
  - cpq
  - guided-selling
  - quote-process
  - process-input
  - product-selection
  - product-search
  - sbqq
inputs:
  - "List of questions the wizard should ask reps (labels, field types, and allowed values)"
  - "Product2 classification fields that answers will filter against (API names and data types)"
  - "Whether the org uses Standard search, Enhanced multi-select search, or a Custom Apex search plugin"
  - "Whether Auto Select Product should be enabled (single-match auto-add behavior)"
  - "Whether the Quote Process should be the org-wide default or pricebook-specific"
  - "Existing SBQQ__QuoteProcess__c and SBQQ__ProcessInput__c record structure if troubleshooting"
outputs:
  - "SBQQ__QuoteProcess__c record with SBQQ__GuidedProductSelection__c = true"
  - "SBQQ__ProcessInput__c records mapping each wizard question to a Product2 classification field"
  - "Mirrored custom fields on SBQQ__ProcessInput__c matching Product2 API names (if custom fields used)"
  - "Documented search type choice and rationale"
  - "Completed guided selling configuration checklist"
dependencies:
  - cpq-product-catalog-setup
  - products-and-pricebooks
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-07
---

# CPQ Guided Selling

Use this skill when configuring or troubleshooting the Salesforce CPQ Guided Selling wizard. Guided Selling lets reps answer a structured set of questions, and CPQ filters the product catalog to show only products that match every answer. This skill covers Quote Process and ProcessInput record setup, classification field mirroring, search type selection, Auto Select Product behavior, and common filtering failures. It does not cover OmniStudio product selection flows, standard Salesforce product browsing, CPQ product bundle setup, or CPQ pricing rules.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the Salesforce CPQ managed package (`SBQQ__`) is installed and the objects `SBQQ__QuoteProcess__c` and `SBQQ__ProcessInput__c` exist in the org schema.
- Identify every Product2 classification field the wizard should filter against. For standard Product2 fields (Family, Description, etc.) no additional setup is needed. For custom fields (e.g., `Product_Category__c`, `Deployment_Model__c`), a mirrored field with the identical API name must exist on `SBQQ__ProcessInput__c` — this is the most common source of silent filtering failure.
- Confirm which search type the business needs: Standard (basic equality or contains filter), Enhanced (multi-select, allows rep to pick multiple values per question), or Custom (Apex class implementing `SBQQ.ProductSearchPlugin`). Custom requires developer involvement.
- Determine whether the Quote Process should be the org-wide default (set in CPQ Settings) or pricebook-specific (set on the Pricebook2 record via `SBQQ__GuidedSelling__c`).
- Identify whether Auto Select Product should be enabled. When enabled, CPQ automatically adds the product to the quote if exactly one product matches the guided selling answers. If more than one matches, the wizard shows the results list instead of auto-adding.

---

## Core Concepts

### Quote Process and the Guided Selling Wizard

A `SBQQ__QuoteProcess__c` record is the top-level configuration object for Guided Selling. Setting `SBQQ__GuidedProductSelection__c = true` on this record activates the wizard mode — without this flag the Quote Process does not show the guided selling wizard when a rep adds a product to a CPQ quote.

The Quote Process is activated for a quote in one of two ways:
1. **Org-wide default:** Set the Quote Process in CPQ Settings (Setup > Installed Packages > CPQ Settings > Quote section). All new quotes use this wizard unless overridden.
2. **Pricebook-specific:** Set `SBQQ__GuidedSelling__c` on a specific `Pricebook2` record to a Quote Process Id. Quotes using that pricebook launch the associated wizard.

When a rep clicks "Add Products" on a CPQ quote and a Quote Process is active, the wizard opens and presents the ProcessInput questions in order. The rep's answers are used to filter `Product2` records using the configured operator and field mapping.

### ProcessInput Records and Field Mapping

Each `SBQQ__ProcessInput__c` record defines one question in the wizard. Key fields:

| Field | Purpose |
|---|---|
| `SBQQ__QuoteProcess__c` | Parent Quote Process lookup |
| `SBQQ__Label__c` | Question label displayed to the rep |
| `SBQQ__Active__c` | Whether this question appears in the wizard |
| `SBQQ__Required__c` | Whether the rep must answer before proceeding |
| `SBQQ__Order__c` | Display sequence within the wizard |
| `SBQQ__SearchField__c` | The API name of the Product2 field this answer filters against |
| `SBQQ__Operator__c` | Filter operator: equals, not equals, contains, starts with, greater than, less than |
| `SBQQ__InputType__c` | How the rep enters the answer: text input, picklist, or product family |

The runtime mechanism: when the rep submits their answers, CPQ reads the answer value stored on the ProcessInput record and executes a SOQL filter against `Product2` using the `SBQQ__SearchField__c` API name and `SBQQ__Operator__c`. The answer value at runtime is held on the ProcessInput record itself — this is why the ProcessInput must have a field with the same API name as the Product2 field being filtered.

### Custom Classification Field Mirroring

When a wizard question filters against a **custom field** on `Product2` (e.g., `Product_Category__c`), CPQ reads the answer value from a field of the same API name on `SBQQ__ProcessInput__c`. This means:

1. The custom field (e.g., `Product_Category__c`) must exist on `Product2`.
2. A field with the **identical API name** (`Product_Category__c`) must also exist on `SBQQ__ProcessInput__c`.
3. Both fields must have compatible data types (text, picklist, number).
4. `SBQQ__SearchField__c` on the ProcessInput record must be set to the API name (`Product_Category__c`).

If the mirror field on `SBQQ__ProcessInput__c` is missing, the wizard appears to work — the question shows and the rep can answer — but the answer silently produces no filter, and CPQ returns all products regardless of the answer. This is the most common guided selling bug reported in production.

### Search Types

CPQ Guided Selling supports three search types, set on the `SBQQ__QuoteProcess__c` record via `SBQQ__SearchType__c`:

| Search Type | Behavior | When to use |
|---|---|---|
| Standard | Basic filter: one answer per question, equality or contains operators | Most use cases; straightforward classification filtering |
| Enhanced | Multi-select: rep can pick multiple values per question; any match returns the product | When a product should appear for multiple answer values (e.g., compatible with both "SMB" and "Enterprise") |
| Custom | Executes an Apex class implementing `SBQQ.ProductSearchPlugin` interface | Complex search logic, external system lookups, or scoring/ranking requirements |

For Custom search, the Apex class must implement the `search(SBQQ.ProductSearchContext ctx)` method from the `SBQQ.ProductSearchPlugin` interface and return a `List<Id>` of matching product IDs. The class name is registered in CPQ Settings under the "Product Search" section.

### Auto Select Product

When `SBQQ__AutoSelectProduct__c = true` on the Quote Process, and the guided selling answers return exactly one matching product, CPQ skips the results list and adds that product directly to the quote. If zero products match, the wizard shows an empty results screen. If two or more products match, the standard product results grid is shown for manual selection.

This feature is useful for high-specificity wizards where the combination of answers is expected to uniquely identify a SKU. It should not be enabled when the answer set is broad enough to return multiple matches, as it can produce confusing behavior where a product appears on the quote without the rep explicitly choosing it.

---

## Common Patterns

### Pattern: Standard Guided Selling with Custom Classification Fields

**When to use:** The product catalog has custom classification fields (e.g., industry, deployment model, service tier) and reps should answer a sequence of dropdown questions to narrow the catalog.

**How it works:**
1. Create custom fields on `Product2` for each classification dimension (e.g., `Industry__c` as a Picklist, `Deployment_Model__c` as a Picklist).
2. Create matching custom fields with the **identical API names** on `SBQQ__ProcessInput__c` using compatible data types.
3. Populate the classification fields on all `Product2` records in the catalog.
4. Create a `SBQQ__QuoteProcess__c` record: set `SBQQ__GuidedProductSelection__c = true`, `SBQQ__SearchType__c = 'Standard'`.
5. Create one `SBQQ__ProcessInput__c` per question, setting `SBQQ__SearchField__c` to the API name, `SBQQ__Operator__c` to `equals`, `SBQQ__InputType__c` to `Picklist`, and `SBQQ__Order__c` for sequence.
6. Set the Quote Process as the org-wide default in CPQ Settings or attach it to the relevant Pricebook2 record.
7. Test by opening a CPQ quote, clicking "Add Products," and stepping through the wizard.

**Why not the alternative:** Using Product Families alone for guided selling limits classification to a single field. Custom classification fields on Product2 allow multi-dimensional filtering without modifying the managed package schema.

### Pattern: Enhanced Search for Multi-Value Product Eligibility

**When to use:** A product should appear in results when the rep's answer matches any of several applicable values — for example, a product that applies to both "Healthcare" and "Financial Services" industries.

**How it works:**
1. Configure the classification field on `Product2` and `SBQQ__ProcessInput__c` as above.
2. Set `SBQQ__SearchType__c = 'Enhanced'` on the Quote Process.
3. In Enhanced mode, the wizard renders a multi-select input for each question. The rep can select multiple values, and CPQ returns products that match any of the selected values for each question.
4. Ensure the classification field on Product2 stores values that exactly match the picklist values presented in the wizard — case-sensitive text matching is used.

**Why not the alternative:** Standard search with "contains" operator can partially approximate multi-value matching but is fragile when values share substrings. Enhanced search is the supported, purpose-built mechanism for OR-matching across classification values.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Filtering on standard Product2 fields (Family, Description) | Set `SBQQ__SearchField__c` to the standard field API name | No mirror field needed; standard fields are always available on ProcessInput |
| Filtering on a custom Product2 field | Create mirror field with identical API name on `SBQQ__ProcessInput__c` | Required for CPQ to store and apply the answer at runtime |
| Rep should select multiple values per question | Use Enhanced search type | Standard search only supports single-value input per question |
| Search logic depends on external data or scoring | Implement `SBQQ.ProductSearchPlugin` Apex class; use Custom search type | Only Custom search allows Apex-controlled filtering logic |
| Wizard should auto-add product when exactly one match | Set `SBQQ__AutoSelectProduct__c = true` on Quote Process | Built-in; only enable when answers reliably produce a single match |
| Default wizard for all quotes | Set Quote Process in CPQ Settings as org default | Applies to all new quotes regardless of pricebook |
| Different wizard per pricebook | Set `SBQQ__GuidedSelling__c` on Pricebook2 | Allows different question sets per price list context |
| Question should be optional (rep can skip) | Set `SBQQ__Required__c = false` on ProcessInput | CPQ skips the filter for that question if the rep leaves it blank |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm CPQ installation and identify classification fields.** Verify `SBQQ__QuoteProcess__c` and `SBQQ__ProcessInput__c` exist. List all Product2 fields the wizard will filter against. For each custom field, flag that a mirror field is required on `SBQQ__ProcessInput__c`.
2. **Create mirror custom fields on SBQQ__ProcessInput__c.** For every custom Product2 classification field involved in guided selling, create a field on `SBQQ__ProcessInput__c` with the identical API name and a compatible data type. This step is a prerequisite — skipping it causes silent filtering failures that are difficult to diagnose after the fact.
3. **Populate Product2 classification fields.** Ensure all products that should appear in guided selling results have values on the classification fields. Products with null values in a filtered field will not appear when the wizard applies that filter with an `equals` operator.
4. **Create the Quote Process record.** Set `SBQQ__GuidedProductSelection__c = true`. Choose the appropriate `SBQQ__SearchType__c` (Standard, Enhanced, or Custom). Set `SBQQ__AutoSelectProduct__c` if single-match auto-add is required.
5. **Create ProcessInput records.** For each question, create a `SBQQ__ProcessInput__c` record: set the parent Quote Process, label, order, search field API name, operator, input type, and required flag. Verify that `SBQQ__SearchField__c` matches the exact API name of the Product2 field (and the mirror field on ProcessInput).
6. **Activate the Quote Process.** Either set it as the org-wide default in CPQ Settings or link it to the relevant Pricebook2 via `SBQQ__GuidedSelling__c`. Test by opening a new CPQ quote and clicking "Add Products" to confirm the wizard launches.
7. **Test all answer combinations and verify filtering.** Test each question with a valid answer that should match products and confirm results are non-empty. Test with an answer that should produce zero matches. Test optional questions by leaving them blank and verify all products pass that filter. If any filter silently returns all products, check the mirror field on `SBQQ__ProcessInput__c`.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `SBQQ__GuidedProductSelection__c = true` is set on the Quote Process record
- [ ] Every custom Product2 classification field used in guided selling has a mirror field with identical API name on `SBQQ__ProcessInput__c`
- [ ] `SBQQ__SearchField__c` on each ProcessInput matches the exact Product2 field API name (case-sensitive)
- [ ] All product records have non-null values on the classification fields they should be filtered by
- [ ] Search type (Standard / Enhanced / Custom) is explicitly set on the Quote Process
- [ ] ProcessInput records have unique, ordered `SBQQ__Order__c` values
- [ ] Required vs. optional questions are correctly marked with `SBQQ__Required__c`
- [ ] The Quote Process is activated (org-wide default or pricebook-level assignment confirmed)
- [ ] Auto Select Product behavior has been tested — if enabled, confirmed the answer set reliably produces a single match
- [ ] End-to-end wizard test completed in a sandbox with real CPQ quotes

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Missing mirror field on SBQQ__ProcessInput__c causes silent all-product return** — When a ProcessInput's `SBQQ__SearchField__c` references a custom field that does not exist on `SBQQ__ProcessInput__c`, CPQ cannot store the rep's answer at runtime. The wizard accepts the input but applies no filter — every product in the catalog appears in results. There is no error message. The only diagnostic is to check field existence on the ProcessInput object.
2. **Products with null classification field values are excluded by equals-operator filters** — If `SBQQ__Operator__c = 'equals'` and a Product2 record has a null value on the filtered field, it will never appear in guided selling results for that question, even if the rep selects a catch-all or leaves the question blank with Required = false. Products must be data-complete on all classification fields used in the wizard.
3. **Auto Select Product fires even when the single match is not in the active pricebook** — If the Quote Process has `SBQQ__AutoSelectProduct__c = true` and the one matching product is not in the quote's active pricebook, CPQ will attempt to add it and generate a pricebook entry error at line creation. Always confirm pricebook coverage for products surfaced by guided selling before enabling Auto Select.
4. **SBQQ__GuidedProductSelection__c = false deactivates the wizard without deleting the record** — A Quote Process with `SBQQ__GuidedProductSelection__c = false` does not launch the wizard; "Add Products" falls back to the standard product selector. This is an easy configuration mistake when cloning Quote Process records — always verify this flag on newly created or cloned records.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| SBQQ__QuoteProcess__c record | Top-level guided selling configuration with GuidedProductSelection, SearchType, and AutoSelectProduct settings |
| SBQQ__ProcessInput__c records | One per wizard question; defines label, field mapping, operator, order, and required status |
| Mirror custom fields on SBQQ__ProcessInput__c | Custom fields matching Product2 classification field API names; required for custom-field-based filtering |
| Guided selling configuration checklist | Completed checklist documenting all setup decisions and test results |

---

## Related Skills

- cpq-product-catalog-setup — Use to configure the Product2 catalog and product bundles before setting up guided selling classification fields
- products-and-pricebooks — Use for standard Product2 and pricebook setup that guided selling filters operate against
- cpq-pricing-rules — Use when guided selling results feed into a pricing configuration that uses price rules or discount schedules
- quote-to-cash-requirements — Use during requirements gathering to confirm whether guided selling is the right product selection mechanism
