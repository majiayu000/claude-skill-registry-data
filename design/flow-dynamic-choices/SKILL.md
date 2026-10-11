---
name: flow-dynamic-choices
description: "Build picklists and choice sets in Flow Builder sourced from records, picklist fields, or collections, including dependent choices. NOT for static hard-coded choice sets."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Reliability
triggers:
  - "dynamic choice flow"
  - "record choice set flow"
  - "dependent picklist flow"
  - "flow picklist from records"
tags:
  - flow
  - choices
  - screen-flow
inputs:
  - "picklist source (SObject query or picklist field)"
  - "filter criteria"
outputs:
  - "Choice configuration + fallback on empty results"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# Flow Dynamic Choices

Screen Flows often need choices that reflect current data — active Accounts, open Cases, active picklist values. Record Choice Sets pull from SOQL; Picklist Choice Sets pull from field metadata; Collection Choice Sets iterate a variable. This skill covers each plus dependent-picklist patterns and empty-state handling.

## When to Use

Any screen flow choice that should reflect org data at runtime.

Typical trigger phrases that should route to this skill: `dynamic choice flow`, `record choice set flow`, `dependent picklist flow`, `flow picklist from records`.

## Recommended Workflow

1. Pick source: Record Choice Set (SOQL), Picklist Choice Set (metadata), or Collection Choice Set (from a Get/Loop).
2. Constrain the query: filter active, limit rows, order for UX.
3. For dependent choices: second choice set filters on the first's stored value; use the reactive screen component.
4. Handle empty set: branch to a message screen or preselect a fallback.
5. Test with a user whose sharing hides the query results; verify graceful empty state.

## Key Considerations

- Record Choice Sets ignore sharing by default with admin-run flow; use `Run In` = 'System Context With Sharing' carefully.
- Large result sets (>200) should be filtered — UI becomes unusable.
- Picklist Choice Set uses active values only; inactive values don't appear.
- Dependent fields in metadata are honored by Record-Triggered paths but not always by Screen picklists — test.

## Worked Examples (see `references/examples.md`)

- *Active Account picker* — Case creation flow
- *Country → State dependent* — Address capture

## Common Gotchas (see `references/gotchas.md`)

- **Sharing mismatch** — User sees choices they can't open.
- **Empty state not handled** — User sees empty dropdown; stuck.
- **Inactive picklist values** — Historical values invisible.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Hard-coded choices that mirror records
- Unbounded SOQL in Choice Set
- No empty-state path

## Official Sources Used

- Flow Builder Guide — https://help.salesforce.com/s/articleView?id=sf.flow.htm
- Flow Best Practices — https://help.salesforce.com/s/articleView?id=sf.flow_best_practices.htm
- Reactive Screens — https://help.salesforce.com/s/articleView?id=sf.flow_ref_elements_screen_reactive.htm
- Flow HTTP Callout Action — https://help.salesforce.com/s/articleView?id=sf.flow_concepts_callout.htm
