---
name: lwc-data-table
description: "First-time lightning-datatable setup — columns, key-field, basic sort, row actions. Triggers: lightning-datatable basics, datatable columns, key-field, fieldName, draft-values, onsave, onsort, onrowaction, customTypes, LightningDatatable, refreshApex after save. NOT for inline edit, custom types, infinite scroll — use lwc/lwc-datatable-advanced. NOT for datasets too large for datatable — use lwc/lwc-virtualized-lists."
category: lwc
salesforce-version: "Spring '25+"
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
  - "lwc data table isn't working"
  - "build a lightning datatable from an apex wire method"
  - "sort lightning datatable columns in javascript"
  - "save datatable draft values through an apex controller"
  - "add a custom column type to lightning datatable"
  - "datatable does not refresh after saving inline edits"
  - "datatable column is blank even though apex returns the field"
  - "datatable rows do not rerender after i sort them"
  - "handle onrowaction and dispatch a custom event from a datatable"
  - "write a jest test for a lightning datatable component"
  - "limit how many rows a lightning datatable loads"
  - "datatable not rerendering after the data array changes"
inputs:
  - "row count, data source, and whether the table needs inline edit or row actions"
  - "how rows are keyed and whether selection state must survive pagination"
  - "whether the use case needs standard types, custom cell rendering, or infinite loading"
outputs:
  - "datatable design recommendation for columns, save flow, and loading strategy"
  - "review findings for key-field, selection, and edit-state issues"
  - "implementation guidance for inline edit, row actions, or bounded infinite loading"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when a table is becoming the center of the LWC experience and small design mistakes are turning into fragile state management. `lightning-datatable` is powerful when the component keeps row identity, edit lifecycle, and loading strategy explicit; it becomes unstable when those concerns are improvised in the UI layer.

---

## Before Starting

Gather this context before working on anything in this domain:

- How many rows should the user ever see at once, and is the dataset naturally page-sized or effectively unbounded?
- Does the grid need inline edit, row-level actions, mass selection, or only read-only browsing?
- What stable unique value can serve as `key-field`, and will selection or draft state need to survive refreshes?

---

## Questions to Ask Before Configuring

Ask these before writing the column array. Each one closes a failure that the datatable reports as a rendering bug rather than an error, and each maps to a gotcha in `references/gotchas.md`.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "What is the stable unique key on every row, and does it survive sort, refresh, and the next page?" | `key-field` is required and is what associates a row with a record; anything the shaping layer derives is re-derived on every load | The `key-field` value, and the confirmation that the query actually selects it |
| "For each column, what is the exact key on the row object — not the field label, not the relationship path?" | `fieldName` names a key on the provisioned row; `SELECT Account.Name` arrives as a nested object, not a flat string | The shaping-layer spec: which keys are flattened, which are derived |
| "Which fields genuinely need inline edit, and which are read-only?" | Every editable column costs performance, and compound fields such as `Name` cannot be edited at all | A short editable list and the component fields that replace any compound one |
| "If a save fails, may the user's typing be discarded?" | Clearing `draftValues` is what hides the Cancel/Save footer, so *when* you clear it is a UX decision, not a formality | The clear-early vs clear-on-success choice, written into the `onsave` handler |
| "Do other components on the same page have to see the edit immediately?" | Apex writes bypass Lightning Data Service — `refreshApex` fixes this table, `notifyRecordUpdateAvailable` fixes the rest of the page | Whether the save path needs one refresh call or both |
| "How many rows and columns will this table hold on its worst day?" | Salesforce testing puts best performance at 1,000 rows and 5 columns; past 250 rows the guidance is fewer than 20 columns | A bounded page size and a decision between pagination, infinite loading, and a different component |
| "Will any user open this on mobile?" | `lightning-datatable` is not supported on mobile devices, and `lightning-tree-grid` supports neither sorting, inline editing, nor infinite scrolling | A separate mobile design, or a documented desktop-only scope in the `-meta.xml` targets |

What a proper configuration adds over just dropping a datatable on the page: row identity survives every sort and refresh, columns resolve because the shaping layer put the keys there, a failed save leaves the user's edits intact, and the row count is bounded by a number someone chose rather than by whatever the query happened to return.

---

## Core Concepts

The single most important idea in `lightning-datatable` work is row identity. If the table cannot map a row to a stable key, selection, edit state, rerender behavior, and event handling all become unreliable. Many table bugs that look like random UI glitches are actually identity or data-shaping mistakes upstream.

### `key-field` Is A Contract, Not Decoration

Every row must expose a stable, unique field that the table can use as `key-field`. The value should survive sorting, refreshes, and pagination. Index-based identity is not durable enough. When the key is wrong, selected rows jump unexpectedly, inline edits attach to the wrong record, and rerenders behave inconsistently.

### Column Definitions Are Part Of Data Shaping

`lightning-datatable` expects columns and rows to agree on field names, types, and type attributes. That means the component often needs a shaping layer that converts raw Apex or UI API data into a table-specific model. This is especially important for row actions, URL cells, and formatted numeric or currency columns.

### Two Naming Worlds Meet On One Component

The element's attributes are kebab-case (`key-field`, `draft-values`, `enable-infinite-loading`); everything inside the `columns` array is a JavaScript object and therefore camelCase (`fieldName`, `typeAttributes`, `cellAttributes`, `standardCellLayout`, `editTemplate`). A key from the wrong world is an unrecognised property, not an error.

### The Table Only Rerenders On A New Array Reference

LWC compares field values with `===`. Sorting, appending, or patching `this.rows` in place changes nothing the framework can see, so the table keeps rendering the old rows. Every mutation has to produce a new array of new objects.

### Inline Edit Has A Real Save Lifecycle

Inline editing is not just a visual flag. Draft values appear in `draft-values`, the user triggers `onsave`, the component persists the changes, and only then should draft state be cleared. Teams often forget that failure handling and optimistic UI rules must be explicit or the grid will feel unreliable.

### Custom Types Are A Subclass, Not A Column Option

A custom cell type means a second component that extends `LightningDatatable` and registers the type in `static customTypes` with a `template`, its `typeAttributes`, and — for anything editable or interactive — `standardCellLayout: true`. Extending `LightningDatatable` is allowed *only* for this purpose.

### Infinite Loading Must Stay Bounded

Infinite loading is useful for progressive browsing, not an excuse to push an unbounded dataset into the browser. Each load step still needs server-side filters, stable sort behavior, and a deliberate stop condition.

---

## Common Patterns

### Read-Only Grid With Typed Columns And Row Actions

**When to use:** Users primarily browse records but need targeted row actions such as View, Edit, or Assign.

**How it works:** Shape rows into a stable view model, define typed columns once, and attach a single `onrowaction` handler that reads `event.detail.action` and `event.detail.row` and re-dispatches a `CustomEvent` for the parent.

**Why not the alternative:** Embedding ad hoc action logic directly into the data shape makes the component harder to maintain and test.

### Inline Edit With Explicit Save Pipeline

**When to use:** Users need quick in-grid edits for a narrow set of fields.

**How it works:** Mark the supported columns `editable: true`, handle `onsave`, persist the `draftValues`, refresh the backing data, and clear draft state on the branch your failure policy says.

**Why not the alternative:** Clearing drafts early or mutating rows in place without a save contract leads to mismatched UI and server state.

### Custom Cell Type Extending `LightningDatatable`

**When to use:** No standard type (`action`, `boolean`, `button`, `button-icon`, `currency`, `date`, `date-local`, `email`, `location`, `number`, `percent`, `phone`, `text`, `url`) renders the cell you need.

**How it works:** A second bundle extends `LightningDatatable`, registers the type in `static customTypes`, and points at a cell template; the wrapper component uses `<c-my-datatable>` instead of `<lightning-datatable>`.

**Why not the alternative:** `cellAttributes` and SLDS styling hooks cover most styling needs without a subclass — reach for the subclass only when the cell's *markup* has to change.

### Bounded Infinite Loading

**When to use:** The table is browse-oriented and the next page is meaningful, but the full result set is too large for first render.

**How it works:** Use `enable-infinite-loading` with `onloadmore`, fetch the next bounded page from the server, append rows by stable key into a new array, and stop loading when the server signals exhaustion.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard browse table with a modest row count | `lightning-datatable` with typed columns | Fastest supported grid with strong platform behavior |
| Need quick edits to a few fields | Inline edit with explicit `onsave` pipeline | Keeps draft state and persistence aligned |
| Saving more than a handful of rows at once | One Apex DML, not N calls to `updateRecord()` | `updateRecord()` takes a single record; Apex is the documented bulk path |
| Need row-specific actions | Use action columns and `onrowaction` | Clear separation between data and commands |
| Need a cell the standard types cannot render | Extend `LightningDatatable` with a registered custom type | The only supported way to change cell markup |
| Need to browse large but bounded datasets | Paginate or use infinite loading with a stop condition | Prevents a runaway browser-side dataset |
| Any mobile access at all | A different component or layout | `lightning-datatable` is not supported on mobile |
| Need spreadsheet-like behavior or deep virtualization | Consider a different architecture | Base datatable is not a replacement for a full grid framework |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. **Answer the seven questions above**, then write the row contract down: the `key-field`, the exact key each column's `fieldName` will read, and which of those keys the Apex query returns versus which the shaping layer must derive.
2. **Write the Apex read and write halves separately.** The read is `@AuraEnabled(cacheable=true)` and bounded (`LIMIT`, or `LIMIT`/`OFFSET`); the write is a plain `@AuraEnabled` method taking the whole draft batch. Copy the shapes from `references/code-examples.md` §1.
3. **Build the bundle** — wrapper component, and a `LightningDatatable` subclass only if a standard type will not do. Wire a *function*, not a property, so `refreshApex` has the object it requires. `references/code-examples.md` §2–§3 is the reference implementation; `templates/lwc/patterns/datatableCustomTypePattern.html` is the canonical cell template and `templates/lwc/component-skeleton/` the bundle skeleton.
4. **Write the Jest test before the deploy** — assert that rows render keyed by `key-field`, that the sort handler reorders *and* hands back a new array reference, and that a row action dispatches its `CustomEvent`. `references/code-examples.md` §4 and `templates/lwc/jest.config.js`.
5. **Run the checker**: `python3 skills/lwc/lwc-data-table/scripts/check_lwc_data_table.py --manifest-dir force-app/main/default`. It flags a datatable with no `key-field`, columns whose `fieldName` has no matching key in the Apex return shape, `draft-values` with no `onsave`, in-place mutation of the wired array, a `LightningDatatable` subclass with no `static customTypes`, and a bundle with no `__tests__`.
6. **Deploy and verify in the org** using the sequence in `references/code-examples.md` §7 — edit two rows, save, and confirm the footer clears, the toast counts the rows, and the related lists on the same page update without a browser refresh.
7. **Fill in `templates/lwc-data-table-template.md`** with the decisions you actually made, and record anything you deviated from — especially a row count above the documented performance envelope.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `key-field` is stable, unique, selected by the query, and not derived from array position.
- [ ] Every column `fieldName` resolves to a key that exists on the provisioned row.
- [ ] Column config uses camelCase keys; only the element's attributes are kebab-case.
- [ ] Inline edit uses `draft-values`, `onsave`, and a stated clear-on-success or clear-early policy.
- [ ] Rows are replaced with a new array reference on every sort, append, and patch.
- [ ] An Apex save calls `notifyRecordUpdateAvailable` and `refreshApex`, in that order, after the `await`.
- [ ] Any custom type sets `standardCellLayout: true` and calls `super.connectedCallback()` in any override.
- [ ] Selection state is tested across sorting, refresh, or pagination.
- [ ] Infinite loading has bounded server queries and a stop condition.
- [ ] Row and column counts sit inside the documented performance envelope, and mobile is out of scope or separately designed.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems. Full detail, with guide line citations, in `references/gotchas.md`.

1. **Bad `key-field` values look like random UI bugs** - row selection, expansion, and draft state become unstable when identity is not durable.
2. **Clearing `draftValues` is what hides the footer** - the two documented recipes clear it at different moments, so the timing is a deliberate failure-policy choice.
3. **Column keys are camelCase, element attributes are kebab-case** - a key from the wrong world is ignored silently.
4. **`fieldName` reads the row object, not the sObject** - a relationship field arrives nested, so a blank column is usually a shaping bug.
5. **In-place array mutation never rerenders** - `sort`, `push`, and cell patches all need a fresh array reference.
6. **`event.detail.fieldName` is `undefined` when sorting a custom type** - pass the field name into the sort function instead.
7. **`standardCellLayout` defaults to `false`** - the bare layout drops padding and keyboard access for editable custom types.
8. **A `connectedCallback` override without `super` breaks the subclass** - and a nested datatable inside a custom cell is unsupported.
9. **An Apex save needs two refresh calls** - `refreshApex` for this wire, `notifyRecordUpdateAvailable` for the rest of the page.
10. **Server-side validation rules never fire for custom data types** - and `lightning-input-field` is rejected inside a datatable.
11. **Infinite loading still needs server discipline** - appending page after page without filters or a stop rule becomes a performance problem quickly.
12. **The component is desktop-only** - and tree-grid is not a drop-in fallback, since it has no sorting, inline edit, or infinite scroll.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Component bundle | Wrapper LWC, optional `LightningDatatable` subclass, `-meta.xml`, and `package.xml` |
| Apex controller + test | Bounded cacheable read and a bulk-safe non-cacheable write, with a 200-row test |
| Jest test | Assertions on row rendering, sort reordering, row-action events, and the wire error path |
| Datatable design | Recommendation for columns, identity, actions, and edit strategy |
| Save-flow review | Findings on draft handling, refresh, and failure behavior |
| Loading strategy | Guidance for paging or infinite loading without runaway state |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are building the thing — the full bundle, Apex controller and test, `-meta.xml`, `package.xml`, Jest test, and the deploy/verify sequence |
| `references/gotchas.md` | A table behaves strangely and you need the grounded platform behaviour behind it |
| `references/llm-anti-patterns.md` | Reviewing datatable code an assistant generated, before it reaches a PR |
| `references/examples.md` | You want worked scenarios — inline edit, bounded infinite loading, custom-type sorting — with the reasoning attached |
| `references/well-architected.md` | Justifying the design trade-offs, or you need the official sources behind a claim |
| `templates/lwc-data-table-template.md` | Recording the identity, interaction, and loading decisions for this specific table |

---

## Related Skills

- `lwc/lwc-datatable-advanced` - use when the table needs row-level errors, richer inline-edit variants, or infinite scroll beyond the bounded pattern here.
- `lwc/lwc-custom-datatable-types` - use when the work is mostly about the custom cell itself: progress bars, pickers, image columns, editable picklists.
- `lwc/lwc-accessibility` - use for the datatable's navigation-mode / action-mode keyboard contract and for making custom cell types reachable.
- `lwc/lwc-wire-refresh-patterns` - use when the question is which refresh call to make after a write, or why the wire will not re-provision.
- `lwc/lwc-performance` - use when the table issue is part of a wider rendering or data-fetch scale problem.
- `lwc/lwc-virtualized-lists` - use when the row count is past what `lightning-datatable` should hold at all.
- `lwc/wire-service-patterns` - use when the table's row model is unstable because the data contract is wrong.
- `lwc/lwc-forms-and-validation` - use alongside this skill when inline edit should be escalated into a real form UX instead of remaining in-grid.
