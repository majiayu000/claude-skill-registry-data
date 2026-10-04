---
name: cpq-guided-selling
description: "Use this skill when configuring or troubleshooting the Salesforce CPQ Guided Selling wizard: Quote Process records, ProcessInput questions that filter products by field value, mapping answers to Product2 classification fields, and search type choice (Standard, Enhanced, Custom). Trigger keywords: CPQ guided selling, quote process wizard, product selection wizard, SBQQ__QuoteProcess__c, SBQQ__ProcessInput__c, guided product selection, auto select product, product search plugin. NOT for bundles, product options, or product rules — use admin/cpq-product-catalog-setup. NOT for writing a custom ProductSearchPlugin in Apex — use apex/cpq-apex-plugins."
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
  - "add an inventory filter to a CPQ guided selling prompt with the product search plugin"
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
  - "SBQQ__QuoteProcess__c record configured for guided selling"
  - "SBQQ__ProcessInput__c records mapping each wizard question to a Product2 classification field"
  - "Mirrored custom fields on SBQQ__ProcessInput__c matching Product2 API names (if custom fields used)"
  - "Documented search type choice and rationale"
  - "Completed guided selling configuration checklist"
dependencies:
  - cpq-product-catalog-setup
  - products-and-pricebooks
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-10-03
---

# CPQ Guided Selling

Use this skill when configuring or troubleshooting the Salesforce CPQ Guided Selling wizard. Reps answer a structured set of questions, and CPQ filters the catalog to products that match. This skill covers Quote Process and Process Input setup, classification field mirroring, the Enhanced and Custom plugin modes, Auto Select Product behavior, and common filtering failures. It does not cover OmniStudio product selection, standard product browsing, bundle setup, or pricing rules.

Product status: the Salesforce CPQ Developer Guide (Summer '26) states that the Salesforce CPQ managed package "continues to be available for existing customers, however, there is no longer any new feature development", and recommends Revenue Cloud for new implementations. Use this skill for orgs already on CPQ.

Field-name caution: the CPQ object reference is published only on help.salesforce.com, which did not fetch for this pass. UNVERIFIED (2026-10-03): the field API names below for `SBQQ__QuoteProcess__c` and `SBQQ__ProcessInput__c` (`SBQQ__GuidedProductSelection__c`, `SBQQ__SearchType__c`, `SBQQ__AutoSelectProduct__c`, `SBQQ__SearchField__c`, `SBQQ__Operator__c`, `SBQQ__InputType__c`, `SBQQ__Label__c`, `SBQQ__Active__c`, `SBQQ__Required__c`, `SBQQ__Order__c`) and `Pricebook2.SBQQ__GuidedSelling__c` come from earlier versions of this skill and are not in the CPQ Developer Guide or the CPQ Plugins Guide. Confirm each in Object Manager before writing data loads or automation. The documented names are `SBQQ__Quote__c.SBQQ__QuoteProcessId__c` and `SBQQ__Quote__c.SBQQ__Pricebook__c`, and the quote process's Product Search Executor and Product Configuration Initializer fields (labels).

---

## Before Starting

- Confirm the CPQ managed package (`SBQQ__`) is installed and the Quote Process and Process Input objects exist.
- Identify every Product2 field the wizard filters on. For custom fields, plan a field with the same API name on the Process Input object (see Core Concepts).
- Decide whether plain guided selling is enough, or whether the product search plugin is needed: Enhanced mode (the plugin appends a WHERE clause) or Custom mode (the plugin builds the whole query).
- Decide how the Quote Process is chosen: the org default, or set per quote (`SBQQ__Quote__c.SBQQ__QuoteProcessId__c`).
- Decide whether Auto Select Product should add the single match automatically.

---

## Questions to Ask Before Configuring

Ask these before creating a Quote Process. Each one traces to a gotcha in `references/gotchas.md`.

| Question | Why it matters | What a good answer adds | What proper configuration adds over just doing it |
|---|---|---|---|
| "Is this org staying on CPQ, or moving to Revenue Cloud?" | The CPQ package has no new feature development (gotcha 1) | A decision on how much to invest in custom plugin code | Effort spent where the platform is still developed |
| "Which Product2 fields do the questions filter on, and are any custom?" | Custom fields need a same-name field on Process Input (gotcha 2) | A field list with types, mirrored where custom | Answers that actually filter instead of returning the whole catalog |
| "Can every answer be expressed as a simple field filter, or is extra logic needed (inventory, region, ranking)?" | Extra logic means the product search plugin, in Enhanced or Custom mode (gotcha 3) | The plugin mode, or a decision not to use one | No Apex where configuration was enough, and correct Apex where it was not |
| "Which quote fields would plugin logic need?" | Plugins see only a subset of quote fields by default; others need SOQL (gotcha 4) | The quote fields the plugin must query | Plugin logic that works on the first quote |
| "Should a bundle be pre-configured from the answers?" | The configuration initializer works only for standard product option fields (gotcha 6) | Which option fields the answers set | No initializer built for fields it cannot set |
| "Do all possible single matches have a price book entry in every price book used?" | Auto Select can fail on a missing entry (gotcha 7) | A price book coverage check | Auto Select that adds a line instead of raising an error |

What a proper configuration adds over "just turning on the wizard": every answer narrows the catalog as intended, plugin code exists only where configuration cannot express the rule, and reps never see an unexplained empty or unfiltered result.

---

## Core Concepts

### Quote Process and the Guided Selling Wizard

A Quote Process record (`SBQQ__QuoteProcess__c`) holds the wizard configuration; its Process Input records (`SBQQ__ProcessInput__c`) are the questions. A quote records the quote process it uses in `SBQQ__QuoteProcessId__c` (CPQ Developer Guide, quote model JSON). The quote process can also name a Product Search Executor (a Visualforce page that further filters guided selling results) and a Product Configuration Initializer (a Visualforce page that preselects bundle options from the answers); both are entered as `c__` followed by the page name.

UNVERIFIED (2026-10-03): earlier versions of this skill said the wizard activates only when `SBQQ__GuidedProductSelection__c` is true, that the org default is set in CPQ Settings, and that a price book can carry its own quote process in `Pricebook2.SBQQ__GuidedSelling__c`. These are help-only claims; confirm the field and setting names in the org.

### Process Input Questions and Field Mapping

Each Process Input defines one question: its label, order, whether it is active and required, how the rep answers, the Product2 field it filters, and the operator. The plugin guide confirms the runtime shape: the answers reach the plugin as a map whose "key is a Product2 API name and the value is the desired search value". UNVERIFIED (2026-10-03): the field-level detail of how CPQ stores each answer on the Process Input record is help-only.

### Custom Classification Field Mirroring

When a question filters on a custom Product2 field (for example `Deployment_Model__c`), earlier versions of this skill state that a field with the identical API name and a compatible type must exist on `SBQQ__ProcessInput__c`, and that without it the question silently applies no filter. UNVERIFIED (2026-10-03): this mechanism is help-only. It is the first thing to check when answers return the whole catalog, and the mirror field is deployable metadata (see `references/metadata-examples.md`).

### Standard, Enhanced, and Custom Search

| Mode | What runs | Grounding |
|---|---|---|
| Standard | CPQ's own filter from the Process Input answers, no plugin | UNVERIFIED (2026-10-03): help-only |
| Enhanced | CPQ's query plus a WHERE fragment returned by `getAdditionalSuggestFilters(quote, fieldValuesMap)` | CPQ Plugins Guide: `isSuggestCustom` returning false selects Enhanced searching |
| Custom | The plugin's `suggest(quote, fieldValuesMap)` builds and runs the whole query and returns `List<PricebookEntry>` | CPQ Plugins Guide: `isSuggestCustom` returning true selects Custom searching |

The guided selling interface of `SBQQ.ProductSearchPlugin` has five methods: `isInputHidden(quote, fieldName)`, `getInputDefaultValue(quote, fieldName)`, `isSuggestCustom(quote, fieldValuesMap)`, `suggest(quote, fieldValuesMap)`, and `getAdditionalSuggestFilters(quote, fieldValuesMap)`. CPQ calls `isInputHidden` and `getInputDefaultValue` for each input, then `isSuggestCustom`, then either `suggest` or `getAdditionalSuggestFilters`. Earlier versions of this skill described a `search(SBQQ.ProductSearchContext ctx)` method returning `List<Id>`; that signature is not in the guide. UNVERIFIED (2026-10-03): the claim that Enhanced mode renders multi-select questions with OR matching is help-only.

### Auto Select Product

When Auto Select is on and the answers return exactly one product, CPQ adds it to the quote without showing the results list. With zero matches the wizard shows an empty result; with two or more it shows the results grid. UNVERIFIED (2026-10-03): this behavior and the field name `SBQQ__AutoSelectProduct__c` are help-only.

---

## Common Patterns

### Pattern: Guided Selling with Custom Classification Fields

**When to use:** The catalog has custom classification fields (industry, deployment model, service tier) and reps should narrow it with dropdown questions.

**How it works:**
1. Create the custom fields on Product2.
2. Create same-name, same-type fields on `SBQQ__ProcessInput__c` (deployable, see `references/metadata-examples.md`).
3. Populate the classification fields on every product that should appear.
4. Create the Quote Process for guided selling.
5. Create one Process Input per question, pointing at the Product2 field API name.
6. Make the Quote Process the default or assign it to the quotes that need it.
7. Test from a quote with Add Products, answering every question.

### Pattern: Enhanced Mode for a Business Rule the Questions Cannot Express

**When to use:** Reps answer the questions, but the results must also respect a rule they do not control, such as "urgent shipments only show products with inventory above 3".

**How it works:** Implement `SBQQ.ProductSearchPlugin` with `isSuggestCustom` returning false, and return an extra WHERE fragment from `getAdditionalSuggestFilters` (the guide's own example returns `AND Product2.Inventory_Level__c > 3` when the "Urgent Shipment" input is "Yes"). Register the class on the Plugins tab of the CPQ package settings. UNVERIFIED (2026-10-03): the guide describes that tab for the quote calculator and recommended products plugins but does not name the product search plugin field. The full class, test, and manifest are in `references/metadata-examples.md`.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Filter on standard Product2 fields | Point the question at the standard field API name | No mirror field needed |
| Filter on a custom Product2 field | Mirror field with the same API name on Process Input | Required for the answer to filter (help-only mechanism) |
| Extra rule the rep does not control | Plugin in Enhanced mode (`getAdditionalSuggestFilters`) | CPQ keeps its query; the plugin appends a WHERE fragment |
| Results need external data or ranking | Plugin in Custom mode (`suggest`) | The plugin owns the whole query and returns price book entries |
| Results need a post-filter the rep cannot override | Product Search Executor on the quote process | A Visualforce page that filters guided selling results |
| Answers should preselect bundle options | Product Configuration Initializer | Works only for standard product option fields |
| New implementation, no CPQ yet | Evaluate Revenue Cloud | The CPQ package has no new feature development |

---

## Recommended Workflow

1. **Confirm the platform and fields.** CPQ installed and staying in use; every filter field listed; custom fields flagged for mirroring; every CPQ field API name confirmed in Object Manager.
2. **Deploy the mirror fields.** Create the same-name fields on `SBQQ__ProcessInput__c` from metadata, with field-level security for the users who run the wizard.
3. **Populate classification data.** Every product that should appear has values on the filter fields; null values never match an equals filter.
4. **Create the Quote Process and Process Inputs.** One input per question, pointing at Product2 field API names.
5. **Add plugin logic only if needed.** Enhanced mode for appended filters, Custom mode for full control. Use bind variables, query any quote fields the plugin needs, and register the class on the Plugins tab of the CPQ package settings.
6. **Activate and test.** Make the Quote Process the default or assign it, then test every question with matching, non-matching, and blank answers, and test Auto Select against every price book.

---

## Review Checklist

- [ ] CPQ field API names confirmed in Object Manager (help-only names flagged in this skill)
- [ ] Every custom Product2 filter field has a same-name field on `SBQQ__ProcessInput__c`, with field-level security granted
- [ ] Filter fields populated on every product that should appear
- [ ] Plugin used only where questions cannot express the rule; mode (Enhanced or Custom) documented
- [ ] Plugin SOQL uses bind variables, not string concatenation
- [ ] Quote fields the plugin needs are queried explicitly
- [ ] Quote Process activated (default or assigned)
- [ ] Auto Select tested against every price book in use
- [ ] End-to-end wizard test completed in a sandbox

---

## Salesforce-Specific Gotchas

The deep versions, with sources, live in `references/gotchas.md`.

| # | Gotcha | One-line consequence |
|---|---|---|
| 1 | CPQ package has no new feature development | Large new investments may be stranded |
| 2 | Missing mirror field returns the whole catalog | No error, just unfiltered results |
| 3 | Enhanced and Custom are plugin modes chosen by `isSuggestCustom` | Wrong method gets ignored |
| 4 | Plugins see only some quote fields | Logic fails on null quote values |
| 5 | The guide's sample plugin concatenates strings into SOQL | Copying it invites SOQL injection |
| 6 | Initializer sets only standard product option fields | Custom option fields stay unset |
| 7 | Auto Select needs a price book entry for the single match | Rep sees an error instead of a line |
| 8 | Null classification values never match equals filters | Valid products disappear |

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Quote Process record | Guided selling configuration, with executor and initializer if used |
| Process Input records | One per question; label, field, operator, order, required |
| Mirror custom fields on Process Input | Deployable `CustomField` metadata matching Product2 API names |
| Product search plugin (if needed) | Apex class implementing `SBQQ.ProductSearchPlugin`, with test |
| Guided selling configuration checklist | Setup decisions and test results |

---

## Related Skills

- `admin/cpq-product-catalog-setup`: Product2 catalog and bundles before guided selling
- `admin/products-and-pricebooks`: standard Product2 and price book setup that guided selling filters
- `admin/cpq-pricing-rules`: price rules and discount schedules applied after selection
- `admin/quote-to-cash-requirements`: whether guided selling is the right selection mechanism
- `apex/cpq-apex-plugins`: deeper plugin development beyond the guided selling interface
