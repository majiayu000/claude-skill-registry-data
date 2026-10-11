---
name: flow-data-tables
description: "Use the Data Table screen component for selecting rows from collections in Screen Flows, including single/multi-select and inline actions. NOT for displaying read-only data outside flows."
category: flow
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Reliability
triggers:
  - "flow data table"
  - "flow collection screen selection"
  - "datatable in flow"
  - "flow select record from list"
tags:
  - flow
  - datatable
  - screen
inputs:
  - "collection to display"
  - "selection mode"
outputs:
  - "screen with Data Table configured"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# Flow Data Tables

The Data Table screen component (GA) displays a record collection and lets users select rows. It is the replacement for custom LWC datatables inside flows for 80% of cases. This skill configures columns, selection mode, and downstream consumption of the selected rows, and documents the row-count soft limit beyond which you should switch back to a custom LWC table with server-side paging rather than stretch the screen component into a role it wasn't designed for.

## When to Use

Screen flows that need row selection from a list. Not for inline edit use cases — use lightning-datatable LWC.

Typical trigger phrases that should route to this skill: `flow data table`, `flow collection screen selection`, `datatable in flow`, `flow select record from list`.

## Recommended Workflow

1. Get Records of the SObject into a collection variable.
2. Add Data Table component; bind Source Collection; configure columns (Label, Field Name, Type).
3. Pick selection mode: Single or Multiple.
4. Downstream: reference `{!DataTable.selectedRows}` or `.firstSelectedRow`.
5. Empty state: branch on collection size and show a message screen if zero.

## Key Considerations

- Column types inferred but can be overridden for currency/date/checkbox.
- Soft limit ~1500 rows; beyond that use pagination or refactor to LWC.
- Sort is per-column user action, not configurable default.
- Supports Lookup columns; Rich Text limited.

## Worked Examples (see `references/examples.md`)

- *Select Contact from list* — Case creation
- *Multi-select bulk update* — Update Cases

## Common Gotchas (see `references/gotchas.md`)

- **Huge collection** — Browser sluggish.
- **Missing empty state** — Empty screen with no action.
- **Lookup column confusion** — Shows Id not Name.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Custom LWC when Data Table suffices
- Unbounded collection
- Missing empty state

## Official Sources Used

- Flow Builder Guide — https://help.salesforce.com/s/articleView?id=sf.flow.htm
- Flow Best Practices — https://help.salesforce.com/s/articleView?id=sf.flow_best_practices.htm
- Reactive Screens — https://help.salesforce.com/s/articleView?id=sf.flow_ref_elements_screen_reactive.htm
- Flow HTTP Callout Action — https://help.salesforce.com/s/articleView?id=sf.flow_concepts_callout.htm
