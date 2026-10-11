---
name: lwc-data-table
description: "Use when designing or reviewing `lightning-datatable` usage in Lightning Web Components, including column configuration, stable `key-field` values, inline editing, row actions, infinite loading, and custom cell types. Triggers: 'lightning datatable inline edit', 'row actions in lwc datatable', 'key field missing', 'infinite loading in datatable'. NOT for highly custom virtualized grids or broad page-performance work outside the datatable boundary."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Performance
  - User Experience
tags:
  - lwc-data-table
  - lightning-datatable
  - inline-edit
  - row-actions
  - infinite-loading
triggers:
  - "lightning datatable inline edit save pattern"
  - "row actions are not working in lwc datatable"
  - "what should key field be in datatable"
  - "how do i do infinite loading in lightning datatable"
  - "custom cell type in lwc datatable"
inputs:
  - "row count, data source, and whether the table needs inline edit or row actions"
  - "how rows are keyed and whether selection state must survive pagination"
  - "whether the use case needs standard types, custom cell rendering, or infinite loading"
outputs:
  - "datatable design recommendation for columns, save flow, and loading strategy"
  - "review findings for key-field, selection, and edit-state issues"
  - "implementation guidance for inline edit, row actions, or bounded infinite loading"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-15
---

Use this skill when a table is becoming the center of the LWC experience and small design mistakes are turning into fragile state management. `lightning-datatable` is powerful when the component keeps row identity, edit lifecycle, and loading strategy explicit; it becomes unstable when those concerns are improvised in the UI layer.

---

## Before Starting

Gather this context before working on anything in this domain:

- How many rows should the user ever see at once, and is the dataset naturally page-sized or effectively unbounded?
- Does the grid need inline edit, row-level actions, mass selection, or only read-only browsing?
- What stable unique value can serve as `key-field`, and will selection or draft state need to survive refreshes?

---

## Core Concepts

The single most important idea in `lightning-datatable` work is row identity. If the table cannot map a row to a stable key, selection, edit state, rerender behavior, and event handling all become unreliable. Many table bugs that look like random UI glitches are actually identity or data-shaping mistakes upstream.

### `key-field` Is A Contract, Not Decoration

Every row must expose a stable, unique field that the table can use as `key-field`. The value should survive sorting, refreshes, and pagination. Index-based identity is not durable enough. When the key is wrong, selected rows jump unexpectedly, inline edits attach to the wrong record, and rerenders behave inconsistently.

### Column Definitions Are Part Of Data Shaping

`lightning-datatable` expects columns and rows to agree on field names, types, and type attributes. That means the component often needs a shaping layer that converts raw Apex or UI API data into a table-specific model. This is especially important for row actions, URL cells, and formatted numeric or currency columns.

### Inline Edit Has A Real Save Lifecycle

Inline editing is not just a visual flag. Draft values appear in `draft-values`, the user triggers `onsave`, the component persists the changes, and only then should draft state be cleared. Teams often forget that failure handling and optimistic UI rules must be explicit or the grid will feel unreliable.

### Infinite Loading Must Stay Bounded

Infinite loading is useful for progressive browsing, not an excuse to push an unbounded dataset into the browser. Each load step still needs server-side filters, stable sort behavior, and a deliberate stop condition.

---

## Common Patterns

### Read-Only Grid With Typed Columns And Row Actions

**When to use:** Users primarily browse records but need targeted row actions such as View, Edit, or Assign.

**How it works:** Shape rows into a stable view model, define typed columns once, and attach a single `onrowaction` handler that dispatches based on action name.

**Why not the alternative:** Embedding ad hoc action logic directly into the data shape makes the component harder to maintain and test.

### Inline Edit With Explicit Save Pipeline

**When to use:** Users need quick in-grid edits for a narrow set of fields.

**How it works:** Mark the supported columns `editable: true`, handle `onsave`, persist the `draftValues`, refresh the backing data, and clear draft state only after the save succeeds.

**Why not the alternative:** Clearing drafts early or mutating rows in place without a save contract leads to mismatched UI and server state.

### Bounded Infinite Loading

**When to use:** The table is browse-oriented and the next page is meaningful, but the full result set is too large for first render.

**How it works:** Use `enable-infinite-loading` with `onloadmore`, fetch the next bounded page from the server, append rows by stable key, and stop loading when the server signals exhaustion.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard browse table with a modest row count | `lightning-datatable` with typed columns | Fastest supported grid with strong platform behavior |
| Need quick edits to a few fields | Inline edit with explicit `onsave` pipeline | Keeps draft state and persistence aligned |
| Need row-specific actions | Use action columns and `onrowaction` | Clear separation between data and commands |
| Need to browse large but bounded datasets | Paginate or use infinite loading with a stop condition | Prevents a runaway browser-side dataset |
| Need spreadsheet-like behavior or deep virtualization | Consider a different architecture | Base datatable is not a replacement for a full grid framework |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `key-field` is stable, unique, and not derived from array position.
- [ ] Column definitions match the actual row shape and type attributes intentionally.
- [ ] Inline edit uses `draft-values`, `onsave`, and a clear refresh strategy.
- [ ] Selection state is tested across sorting, refresh, or pagination.
- [ ] Infinite loading has bounded server queries and a stop condition.
- [ ] The component stays within a realistic row count for browser usability.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Bad `key-field` values look like random UI bugs** - row selection, expansion, and draft state become unstable when identity is not durable.
2. **`draft-values` persists until you clear it** - a save success should reset the edit state intentionally rather than assuming the table will do it.
3. **Type attributes use JavaScript-style names** - column config often fails because the component uses HTML-style names instead of the expected camelCase values.
4. **Infinite loading still needs server discipline** - appending page after page without filters or a stop rule becomes a performance problem quickly.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Datatable design | Recommendation for columns, identity, actions, and edit strategy |
| Save-flow review | Findings on draft handling, refresh, and failure behavior |
| Loading strategy | Guidance for paging or infinite loading without runaway state |

---

## Related Skills

- `lwc/lwc-performance` - use when the table issue is part of a wider rendering or data-fetch scale problem.
- `lwc/wire-service-patterns` - use when the table's row model is unstable because the data contract is wrong.
- `lwc/lwc-forms-and-validation` - use alongside this skill when inline edit should be escalated into a real form UX instead of remaining in-grid.
