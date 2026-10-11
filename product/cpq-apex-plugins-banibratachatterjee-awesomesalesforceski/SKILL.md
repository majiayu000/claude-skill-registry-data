---
name: cpq-apex-plugins
description: "Use when implementing Salesforce CPQ plugin interfaces in Apex or JavaScript (JS QCP) to customize quote calculation, product search, order creation, contracting, or configuration screens. Trigger keywords: SBQQ plugin, QuoteCalculatorPlugin, ProductSearchPlugin, OrderPlugin, ContractingPlugin, ConfigurationInitializerPlugin, SBQQ__CustomScript__c, JS QCP, calculate callback, CPQ plugin registration. NOT for standard Apex triggers on SBQQ__Quote__c or SBQQ__QuoteLine__c. NOT for Flow-based customization of CPQ processes. NOT for declarative CPQ configuration such as price rules, discount schedules, or product rules that do not require code."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Reliability
  - Operational Excellence
triggers:
  - "I need to customize how CPQ calculates prices on a quote beyond what price rules support"
  - "how do I implement a CPQ plugin to intercept quote line changes before pricing runs"
  - "CPQ quote calculator plugin not being called or throwing errors during save"
  - "how to register an Apex class as a CPQ OrderPlugin or ContractingPlugin"
  - "I want to run custom logic when a user opens the CPQ configurator screen"
  - "difference between JS QCP and Apex QuoteCalculatorPlugin in CPQ"
  - "SBQQ plugin interface not found or method signature does not match"
tags:
  - cpq
  - salesforce-cpq
  - sbqq
  - apex-plugin
  - quote-calculator-plugin
  - js-qcp
  - order-plugin
  - contracting-plugin
  - product-search-plugin
  - configuration-initializer-plugin
inputs:
  - "Org's CPQ managed package version (SBQQ namespace)"
  - "Which plugin type is needed: calculator, product search, order, contracting, or configuration"
  - "Whether the org already has an active JS QCP (SBQQ__CustomScript__c record with SBQQ__Active__c = true)"
  - "Apex class names currently registered in CPQ Settings (SBQQ__CustomActionSettings__c / plugin registration fields)"
  - "Quote lines and pricing fields affected by the customization"
outputs:
  - "Compliant Apex class implementing the correct SBQQ plugin interface"
  - "JS QCP code (JavaScript) ready to store in SBQQ__CustomScript__c.SBQQ__Code__c"
  - "CPQ Settings registration guidance for each plugin type"
  - "Decision table matching business requirement to correct plugin type"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-07
---

# CPQ Apex Plugins

This skill covers implementing Salesforce CPQ plugin interfaces — both Apex-based and JavaScript Quote Calculator Plugin (JS QCP) — that let practitioners intercept and customize CPQ's calculation engine, configurator, order creation, and contracting flows. Activate when a business requirement cannot be met by declarative CPQ features alone and a coded plugin hook is required.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Identify the plugin type needed.** Nine distinct plugin interfaces exist in CPQ. Selecting the wrong type causes the customization to never fire or to conflict with other plugins. The plugin type determines the interface, the method signatures, and the registration field in CPQ Settings.
- **Check for an active JS QCP.** Only one calculator plugin type — Apex `QuoteCalculatorPlugin` OR a JavaScript QCP stored in `SBQQ__CustomScript__c` — can be active at a time. Mixing both simultaneously causes unpredictable calculation behavior. Query `SELECT Id, SBQQ__Active__c FROM SBQQ__CustomScript__c WHERE SBQQ__Active__c = true` to confirm.
- **Confirm the CPQ package version.** Plugin interfaces evolved across managed package versions. The JS QCP with its seven hooks (`onInit`, `onBeforeCalculate`, `onAfterCalculate`, `onBeforePriceRules`, `onAfterPriceRules`, `onBeforeCalculatePrices`, `onAfterCalculatePrices`) is the modern replacement for the legacy Apex `QuoteCalculatorPlugin`. Orgs on older package versions may not expose all hooks.
- **Know the governor limits context.** Plugin methods execute synchronously inside the CPQ calculation engine's managed package context. Callouts from synchronous plugin methods are not permitted. Use the `SBQQ.CalculateCallback` interface for any calculation that needs async Apex.

---

## Core Concepts

### Plugin Type Taxonomy

CPQ exposes nine distinct plugin interfaces. Each targets a different extension point:

| Plugin Interface | Apex Namespace | Primary Purpose |
|---|---|---|
| `QuoteCalculatorPlugin` | `SBQQ` | Override quote line pricing and totals (legacy — prefer JS QCP) |
| JS QCP (`SBQQ__CustomScript__c`) | JavaScript | Modern calculator hook with 7 lifecycle events |
| `ProductSearchPlugin` | `SBQQ` | Filter or reorder product catalog search results |
| `QuoteTermPlugin` | `SBQQ` | Generate or transform quote terms before finalization |
| `ProductRulePlugin` | `SBQQ` | Extend product rule evaluation logic |
| `ConfigurationAttributePlugin` | `SBQQ` | Custom behavior for configuration attribute changes |
| `ConfigurationInitializerPlugin` | `SBQQ` | Pre-populate options before configurator screen loads |
| `OrderPlugin` | `SBQQ` | Hook into order creation from a quote |
| `ContractingPlugin` | `SBQQ` | Hook into contract creation from an order |

The `CpqPlugin` interface is the base that all Apex plugins extend — never implement it directly.

### JS QCP vs. Legacy Apex QuoteCalculatorPlugin

The **JS QCP** (`SBQQ__CustomScript__c`) is the current supported approach for calculator customization. It stores JavaScript code in the `SBQQ__Code__c` field of an `SBQQ__CustomScript__c` record. The record must have `SBQQ__Active__c = true` and be associated with a quote template or set as the default script.

JS QCP exposes seven named hooks, each receiving `(quoteModel, quoteLineModels, conn)`:

1. `onInit` — fires when the calculator initializes; use to set default field values
2. `onBeforeCalculate` — fires before the calculation engine runs; use to pre-process line fields
3. `onAfterCalculate` — fires after calculation; use to post-process totals
4. `onBeforePriceRules` — fires before CPQ evaluates price rules
5. `onAfterPriceRules` — fires after price rules complete
6. `onBeforeCalculatePrices` — fires before each pricing pass
7. `onAfterCalculatePrices` — fires after each pricing pass

Each hook must return a resolved `Promise`. Returning nothing or a non-Promise causes the calculation to hang indefinitely.

The **legacy Apex `QuoteCalculatorPlugin`** implements `SBQQ.QuoteCalculatorPlugin` with `calculate(quoteLines, callback)`. It is still functional but not recommended for new development. It cannot coexist with an active JS QCP.

### Plugin Registration

Each plugin type has a dedicated registration field on the CPQ Settings record (`SBQQ__CustomActionSettings__c` or the CPQ package settings object). The Apex class name (fully qualified, no namespace prefix for the developer's own code) is entered in the corresponding field:

- **Quote Calculator Plugin:** `SBQQ__QuoteCalculatorPlugin__c` on `SBQQ__CustomActionSettings__c`
- **Product Search Plugin:** `SBQQ__ProductSearchPlugin__c`
- **Order Plugin:** `SBQQ__OrderPlugin__c`
- **Contracting Plugin:** `SBQQ__ContractingPlugin__c`
- **Configuration Initializer Plugin:** `SBQQ__InitializerPlugin__c`

For the JS QCP, no Settings field is used — the active `SBQQ__CustomScript__c` record drives activation.

### Async Calculations with CalculateCallback

Apex plugin methods that need to perform callouts or DML before returning results must use the `SBQQ.CalculateCallback` interface. The plugin's `calculate` method receives a callback object; the implementation invokes `callback.run(quoteLines)` to signal completion. This prevents synchronous blocking of the CPQ engine but adds complexity — errors thrown after `callback.run()` do not surface cleanly.

---

## Common Patterns

### Pattern 1: JS QCP for Custom Pricing Logic

**When to use:** The business requires pricing logic that reads external data (via JS `fetch` to a Salesforce endpoint), evaluates complex conditional pricing not expressible in price rules, or needs access to quote-level aggregates mid-calculation.

**How it works:**

1. Author a JavaScript object with the required hook functions exported as named exports.
2. Store the code in `SBQQ__CustomScript__c.SBQQ__Code__c`. Set `SBQQ__Active__c = true`.
3. Each hook receives `quoteModel` (the quote record + fields) and `quoteLineModels` (array of quote line records + fields).
4. Return a resolved `Promise` from each hook, even if no changes are made (`return Promise.resolve()`).
5. To modify a line, mutate properties on the `quoteLineModels` entries; CPQ reads them back after the hook resolves.

**Why not Apex triggers:** Apex triggers on `SBQQ__QuoteLine__c` fire outside the CPQ calculation transaction. CPQ recalculates on save and overwrites any values set by triggers during the calculation pass, creating an infinite loop or silent data loss.

### Pattern 2: Apex OrderPlugin for Custom Order Line Logic

**When to use:** The business requires Apex logic (DML on custom objects, platform events, callouts) to run immediately when CPQ converts a quote to an order. No JS equivalent exists for OrderPlugin.

**How it works:**

1. Create an Apex class implementing `SBQQ.OrderPlugin`.
2. Override `onBeforeInsert(List<Order> orders, SBQQ.DefaultOrderProduct defaultOrderProduct, Database.UnitOfWork uow)` and/or `onAfterInsert`.
3. Use the provided `uow` (Unit of Work) to register new records. Do not perform DML directly — register work through the UoW so CPQ's transaction management controls commit order.
4. Enter the class name in **CPQ Settings > Order Management > Order Plugin**.

**Why not a trigger:** Order triggers may fire multiple times during CPQ's order creation sequence. The `OrderPlugin` gives deterministic pre/post hooks with access to CPQ's internal Unit of Work.

### Pattern 3: ConfigurationInitializerPlugin to Pre-Select Options

**When to use:** The configuration screen must open with specific product options already selected or specific attribute values pre-populated based on the opportunity, account segment, or another quote field.

**How it works:**

1. Create an Apex class implementing `SBQQ.ConfigurationInitializerPlugin`.
2. Override `initialize(SBQQ.ProductModel productModel, String configurationId)`.
3. Mutate `productModel` to set default option quantities or attribute values.
4. Register the class in CPQ Settings under the Configuration section.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| New calculator customization, org on modern CPQ package | JS QCP (SBQQ__CustomScript__c) | Modern supported approach; seven lifecycle hooks; no Apex compilation required |
| Existing Apex QuoteCalculatorPlugin, need to extend | Extend existing Apex plugin OR migrate to JS QCP | Cannot mix; extending keeps one active type; migration preferred long-term |
| Logic needed during order creation | Apex OrderPlugin | No JS equivalent exists for OrderPlugin |
| Logic needed during contract creation | Apex ContractingPlugin | No JS equivalent exists for ContractingPlugin |
| Custom product catalog filtering | Apex ProductSearchPlugin | Exposes `search()` returning filtered SObject lists |
| Pre-populate configurator options | Apex ConfigurationInitializerPlugin | Fires before the configuration screen loads |
| Pricing logic expressible as price rules | Declarative price rules (no plugin) | Plugins add deployment and maintenance cost; use declarative where sufficient |
| Async callout needed inside calculator | Apex QuoteCalculatorPlugin + SBQQ.CalculateCallback | Only Apex plugin + callback supports async patterns; JS QCP can use JS Promises with fetch |

---

## Recommended Workflow

1. **Identify which plugin type is required.** Match the business requirement against the plugin taxonomy table. Confirm with the requester whether the hook fires in the right lifecycle phase (e.g., before vs. after price rules).
2. **Check for conflicting active plugins.** Query `SBQQ__CustomScript__c` for active JS QCP records and inspect CPQ Settings registration fields. Identify any existing Apex plugin of the same type before writing a new one.
3. **Implement the plugin class or JS QCP code.** Follow the exact method signatures from the CPQ Plugins Developer Guide. For Apex, ensure the class is `global` and `with sharing` unless the plugin needs system-mode access for a documented reason. For JS QCP, ensure every hook returns a `Promise`.
4. **Register the plugin in CPQ Settings.** Enter the Apex class name in the correct Settings field, or activate the `SBQQ__CustomScript__c` record. Verify no other plugin of the same type is registered.
5. **Test in a sandbox with full CPQ calculation flows.** Add a line, change quantity, apply discounts, and save the quote. Verify the plugin fires at the expected lifecycle point using debug logs with `SBQQ` category at `FINEST` level.
6. **Validate governor limit headroom.** Review debug logs for CPU time and SOQL counts inside the plugin execution. CPQ's own calculation logic consumes significant limits; plugin code must be lean.
7. **Deploy and verify post-deployment.** Confirm the CPQ Settings record retains the plugin registration after deployment (Settings records are not metadata — they live in the org's data layer and must be set manually or via a post-install script).

---

## Review Checklist

- [ ] Plugin interface implemented exactly matches the CPQ interface for the chosen plugin type (correct namespace, method signatures)
- [ ] Only one calculator plugin type is active (JS QCP or Apex QuoteCalculatorPlugin, not both)
- [ ] Every JS QCP hook function returns a resolved or rejected `Promise` — no hook returns `undefined` or `void`
- [ ] Apex plugin class is declared `global` (required by managed package interface)
- [ ] Plugin is registered in CPQ Settings in the correct field, not just deployed as metadata
- [ ] Debug logs confirmed the plugin fires at the expected calculation lifecycle point
- [ ] Governor limits (CPU, SOQL, heap) reviewed in debug logs under realistic quote line counts
- [ ] No Apex triggers on `SBQQ__Quote__c` or `SBQQ__QuoteLine__c` performing DML that conflicts with the plugin

---

## Salesforce-Specific Gotchas

1. **CPQ Settings is data, not metadata** — Plugin registration fields on `SBQQ__CustomActionSettings__c` are stored as org data, not in a `.settings` metadata file. A change set or package deployment does not carry these values. After every deployment, you must manually update or script the Settings record to re-register the plugin class name.

2. **JS QCP hooks that return `undefined` hang the calculator indefinitely** — CPQ's calculation engine awaits the Promise returned by each hook. If a hook function has no explicit return statement, it returns `undefined` rather than a resolved Promise. The quote save UI spins without error until the user's session times out. Always end every hook with `return Promise.resolve()` even when no changes are made.

3. **Apex triggers on SBQQ__QuoteLine__c overwrite values set during calculation** — CPQ performs multiple recalculation passes on save. An `after update` trigger that sets a field on `SBQQ__QuoteLine__c` runs between passes; CPQ's next pass reads the stored line and overwrites the field with its calculated value. The trigger's changes appear to stick briefly then revert. Use JS QCP or Apex plugin hooks — not triggers — for any field that CPQ owns.

4. **Only the first registered plugin of each type is called** — CPQ does not chain multiple plugins of the same type. If `SBQQ__OrderPlugin__c` is already set to `ExistingOrderPlugin`, registering a second class `NewOrderPlugin` in the same field simply replaces the first. There is no multi-plugin chaining mechanism; you must combine logic into a single class or use a dispatcher pattern.

5. **`global` access modifier is mandatory on Apex plugin classes** — CPQ plugin interfaces are defined inside the managed `SBQQ` namespace. Implementing a managed-package interface requires the implementing class to be `global`. An `public` implementing class compiles successfully in a scratch org or sandbox but throws a runtime `System.TypeException` when CPQ tries to instantiate it through the interface.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Apex plugin class | `global class MyPlugin implements SBQQ.<PluginInterface>` with all required methods implemented |
| JS QCP script | JavaScript object with named hook functions stored in `SBQQ__CustomScript__c.SBQQ__Code__c` |
| CPQ Settings registration steps | Which field to update and what value to enter for the specific plugin type |
| Plugin test plan | Ordered list of CPQ UI actions that confirm the plugin fires and produces correct output |

---

## Related Skills

- `apex/quote-pdf-customization` — Custom VF-based CPQ quote PDF controllers; separate extension point from the CPQ plugin framework covered here
- `admin/cpq-pricing-rules` — Declarative price rules; evaluate these before reaching for a calculator plugin
- `admin/cpq-quote-templates` — Quote template configuration; understand the template-level JS QCP association before authoring plugin code
