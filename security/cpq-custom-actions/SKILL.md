---
name: cpq-custom-actions
description: "Use when adding, configuring, or troubleshooting custom action buttons in the Salesforce CPQ Quote Line Editor (QLE), product configurator, or amendment/renewal screens. Trigger keywords: CPQ custom action, QLE button, SBQQ__CustomAction__c, CPQ Flow button, CPQ URL action. NOT for standard Salesforce quick actions on non-CPQ objects, Lightning Experience action bars outside the QLE, or CPQ Price Rules and Product Rules."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Security
  - Reliability
triggers:
  - "How do I add a button to the CPQ Quote Line Editor for reps to trigger a Flow?"
  - "I need a custom action in the QLE that opens an external pricing tool in a new tab"
  - "How do I show or hide a CPQ custom action button based on quote field values?"
  - "What is the limit for custom action buttons in Salesforce CPQ and how do I work around it?"
  - "Can I call Apex directly from a CPQ custom action button?"
tags:
  - cpq
  - cpq-custom-actions
  - qle
  - sbqq
  - flow
  - quote-line-editor
inputs:
  - "CPQ package version installed in the org (SBQQ namespace)"
  - "Target screen for the action: QLE (line item, group, or global), product configurator, or amendment/renewal"
  - "Desired action type: URL navigation, Flow launch, or standard CPQ operation (Save, Calculate, Add Group)"
  - "Visibility requirements: should the button always appear, or only under certain conditions?"
  - "Whether Apex logic is needed (requires workaround via Flow or Visualforce)"
outputs:
  - "Configured SBQQ__CustomAction__c record(s) surfacing buttons in the correct CPQ screen and location"
  - "Flow or Visualforce page wired to the action (if Apex execution is required)"
  - "CPQ condition records controlling conditional visibility (if applicable)"
  - "Guidance on staying within the 5-action-per-context hard limit"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# CPQ Custom Actions

This skill activates when configuring or debugging `SBQQ__CustomAction__c` records that surface as clickable buttons in the Salesforce CPQ Quote Line Editor (QLE), product configurator, or amendment/renewal screens. It covers all action types (URL, Flow, standard CPQ operations), the Location field that controls placement, conditional visibility through the CPQ condition evaluation engine, and the hard limit of five custom actions per context.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the CPQ managed package (`SBQQ__`) is installed and the user has the "Salesforce CPQ Admin" or appropriate permission set to create and edit `SBQQ__CustomAction__c` records.
- Identify the target screen: QLE (Quote Line Editor), product configurator, or amendment/renewal flow. Each is a separate `Location` value on the `SBQQ__CustomAction__c` object.
- Count the existing custom actions for the target context. The platform enforces a hard limit of five (5) custom actions per context (e.g., five for Line Item location, five for Group location). Exceeding this silently drops actions or causes unpredictable rendering.
- Determine whether Apex logic is required. Custom actions cannot invoke Apex directly — only URL navigation, Screen/Autolaunched Flow execution, or standard CPQ operations (Save, Calculate, Add Group) are supported action types.

---

## Core Concepts

### SBQQ__CustomAction__c — The Object Behind Every QLE Button

CPQ custom actions are standard Salesforce object records of type `SBQQ__CustomAction__c` in the SBQQ managed package. Each record represents one button. Fields that control behavior:

- **`SBQQ__Type__c`** — The action type. Valid values: `URL` (opens a URL in a new tab or same tab), `Flow` (launches a Screen Flow or Autolaunched Flow), `Calculate` (triggers CPQ price recalculation), `Save` (triggers CPQ quote save), `Add Group` (adds a new quote line group). Only these values are recognized; arbitrary strings fail silently.
- **`SBQQ__Location__c`** — Controls which CPQ screen and position renders the button. Values include `Line Item` (appears in each quote line row), `Group` (appears at the group header level), `Global` (appears once per quote, above the line grid). The configurator and amendment screens have their own location values.
- **`SBQQ__DisplayOrder__c`** — Integer controlling the left-to-right display order of buttons when multiple custom actions share the same location.
- **`SBQQ__Active__c`** — Boolean; only active records are rendered in the UI.
- **`SBQQ__FlowName__c`** — API name of the Flow to invoke when type is `Flow`.
- **`SBQQ__URL__c`** — The URL to navigate to when type is `URL`. Supports merge field syntax for passing CPQ record IDs.

### The Five-Action Hard Limit Per Context

Salesforce CPQ enforces a hard limit of **five custom actions per location context**. This is not a configurable setting or a governor limit — it is a rendering constraint in the QLE Lightning component. If more than five active `SBQQ__CustomAction__c` records exist for a given `Location__c` value, CPQ renders only five and silently ignores the rest (ordering is not guaranteed for the dropped actions). Architects must audit the existing action count before adding new ones.

### Conditional Visibility — CPQ Condition Engine, Not Flow or Apex

Custom action visibility can be made conditional — for example, showing a validation button only when a quote is in `Draft` status. This is controlled by CPQ's **built-in condition evaluation engine**, the same engine that drives Product Rules and Price Rules. Conditions are configured by associating `SBQQ__CustomActionCondition__c` records (or equivalent condition child records) with the custom action and setting the `SBQQ__ConditionsMet__c` picklist on the action (`All`, `Any`, or `Formula`).

This is a frequent source of confusion: practitioners often attempt to control button visibility through Flow decisions or Apex triggers on the quote. Neither approach works. The CPQ rendering layer reads conditions at page load from the CPQ condition framework — it does not evaluate Apex triggers or Flow output to decide whether to render a button.

### Apex Execution — Only via Workaround

Custom actions of type `Flow` or `URL` are the only paths to executing Apex logic from a custom button. There is no `Apex` action type on `SBQQ__CustomAction__c`. Two supported workarounds:

1. **Flow calling Apex** — Configure the action as type `Flow`, then use an Apex-defined invocable method called from an Action element inside the Flow. The Flow acts as the bridge.
2. **URL to a Visualforce page** — Configure the action as type `URL` pointing to a Visualforce page that invokes an Apex controller. Pass the quote or line ID via URL parameters using CPQ merge field syntax (e.g., `{!SBQQ__Quote__c}`).

---

## Common Patterns

### Pattern: Flow-Backed Validation Button in the QLE

**When to use:** A business rule requires reps to validate quote data (e.g., checking product compatibility or minimum order quantities) before submitting, and the validation logic is complex enough to require Apex.

**How it works:**
1. Build an Autolaunched Flow with an Apex action (invocable method) containing the validation logic. The Flow receives the Quote ID as an input variable.
2. Create an `SBQQ__CustomAction__c` record: `SBQQ__Type__c = Flow`, `SBQQ__FlowName__c` = the Flow API name, `SBQQ__Location__c = Global` (one button per quote, not per line).
3. Add a `SBQQ__CustomActionCondition__c` record if the button should only appear in Draft status: field = `SBQQ__Quote__r.SBQQ__Status__c`, operator = `Equals`, value = `Draft`.
4. Set `SBQQ__Active__c = true` and an appropriate `SBQQ__DisplayOrder__c`.

**Why not the alternative:** Using a standard CPQ Price Rule or Product Rule for validation fires automatically on save/calculate and cannot be triggered on demand by the rep. A custom action gives the rep explicit control over when validation runs.

### Pattern: URL Action Opening an External Pricing Tool

**When to use:** The org integrates with an external pricing or CPQ tool that should be launched in context from the QLE, passing the current quote and line IDs to the external system.

**How it works:**
1. Create an `SBQQ__CustomAction__c` record: `SBQQ__Type__c = URL`.
2. In `SBQQ__URL__c`, use CPQ merge field syntax to embed the record ID: `https://external-tool.example.com/quote?sfQuoteId={!SBQQ__Quote__c}&sfLineId={!Id}`. The `{!Id}` token resolves to the current line item record ID when `Location__c = Line Item`.
3. Set `SBQQ__Location__c = Line Item` if the external tool is line-specific, or `Global` if it operates at the quote level.
4. Verify the URL is added to the org's Content Security Policy (CSP) trusted sites if it opens in a Lightning iframe context.

**Why not the alternative:** Visualforce pages embedded in the QLE introduce complexity and session context issues. A URL action that opens in a new browser tab is simpler, avoids CSP complications, and works with any external tool.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to execute Apex logic from a QLE button | Flow action type with an Apex invocable method inside the Flow | Custom actions have no Apex type; Flow is the supported bridge |
| Need to open an external tool in context | URL action type with CPQ merge field tokens in the URL | Simplest path; no managed package extension needed |
| Need to trigger standard CPQ recalculation on demand | `Calculate` action type | Purpose-built; no custom code required |
| Need conditional button visibility | CPQ condition records on the action (SBQQ__CustomActionCondition__c) | CPQ rendering evaluates its own condition engine; Flow/Apex are not evaluated at render time |
| At or near the 5-action limit per context | Consolidate actions into a single Flow with a choice screen | The 5-action limit is hard; the Flow can branch to multiple logical operations |
| Need a button per line row vs. per quote | Line Item location for per-row, Global location for per-quote | Location field controls rendering granularity |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Audit existing custom actions** — Query `SBQQ__CustomAction__c` filtered by the target `SBQQ__Location__c` and `SBQQ__Active__c = true`. Count records. If already at 5, the new action must replace an existing one or be consolidated into a Flow with branching logic before proceeding.
2. **Determine action type** — Decide whether the button should navigate to a URL, launch a Flow, or trigger a standard CPQ operation (Save, Calculate, Add Group). If Apex logic is required, plan the Flow-as-bridge or Visualforce-URL workaround at this step.
3. **Build the Flow or Visualforce page if needed** — For Flow-backed actions, build and activate the Flow first. Confirm the Flow API name. For URL actions pointing to an org page, create and deploy the Visualforce page before creating the action record.
4. **Create the SBQQ__CustomAction__c record** — Set `SBQQ__Type__c`, `SBQQ__Location__c`, `SBQQ__FlowName__c` or `SBQQ__URL__c`, `SBQQ__DisplayOrder__c`, and `SBQQ__Active__c = true`. Use a meaningful label in `Name` — this appears as the button label in the QLE.
5. **Configure conditional visibility if required** — Create `SBQQ__CustomActionCondition__c` records referencing the parent action. Set the `SBQQ__ConditionsMet__c` field on the action to `All`, `Any`, or `Formula`. Test by loading the QLE with a quote that meets and does not meet the conditions.
6. **Test end-to-end in the QLE** — Open a test quote in the QLE. Verify the button renders at the correct location, the label is correct, the action fires correctly, and conditional visibility behaves as expected. Check browser console for JavaScript errors if the button does not appear.
7. **Review checklist before deploying to production** — Confirm the 5-action limit is not exceeded, Flow is activated, URL CSP trusted sites are configured, and the action is tested on both new and amendment quotes if applicable.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Active custom action count for the target location is 5 or fewer
- [ ] Flow is activated (not Draft) before the custom action record is created
- [ ] For URL actions, the target URL domain is added to CSP Trusted Sites if it opens in a Lightning context
- [ ] Conditional visibility is configured via CPQ condition records, not via Flow decisions or Apex
- [ ] The action has been tested on both the target CPQ screen and, if applicable, on amendment/renewal quotes
- [ ] Button label in `Name` field is clear and rep-facing (not an internal API name)
- [ ] `SBQQ__DisplayOrder__c` is set to avoid collisions with existing actions

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Five-action limit is silent, not an error** — When more than five active custom actions exist for a location, CPQ does not throw an error. It silently drops actions beyond the limit. Reps report "missing buttons" with no error in the logs. Always query the count before adding.
2. **Flow must be Activated before the action fires** — A Flow in Draft status will cause the custom action to fail at runtime with a generic error. CPQ does not validate the Flow status when the `SBQQ__CustomAction__c` record is saved — the failure only surfaces when a rep clicks the button.
3. **Conditional visibility is evaluated at page load, not on field edit** — CPQ reads custom action conditions when the QLE renders. If a rep changes a quote field that would meet a condition, the button does not appear until the page reloads. This surprises stakeholders who expect real-time button visibility toggling.
4. **URL merge fields only resolve for the record type matching the Location** — The `{!Id}` token in a URL action resolves to the line item ID when `Location__c = Line Item`, and to the quote ID when `Location__c = Global`. Mixing up location and expected merge field values produces broken URLs.
5. **Custom actions do not appear on the Lightning record page — only in the CPQ screens** — Practitioners sometimes create `SBQQ__CustomAction__c` records and then look for the button on the Quote object's Lightning record page. Custom actions only render inside the QLE, configurator, and amendment screens launched by the CPQ package — not on standard Lightning record pages.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| SBQQ__CustomAction__c record | The configured custom action button record in the CPQ org |
| Flow (if type = Flow) | The activated Flow wired to the action, optionally containing an Apex invocable action |
| SBQQ__CustomActionCondition__c records | Condition records controlling button visibility (if conditional behavior required) |
| Visualforce page (if type = URL to VF) | Page wired to an Apex controller for Apex-execution workaround via URL action |
| Audit query results | SOQL results confirming action count per location is within the 5-action limit |

---

## Related Skills

- `cpq-architecture-patterns` — Covers QLE performance limits, Large Quote Mode, and bundle design patterns that interact with custom action placement
- `apex-invocable-actions` — Use alongside this skill when a Flow-backed custom action needs to call an Apex invocable method
