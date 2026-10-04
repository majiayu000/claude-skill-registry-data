---
name: virtualized-lists
description: "Render only visible rows for long lists (1k+ rows) using intersection observer or lightning-datatable virtual scroll. Triggers: virtual scroll, long list LWC. NOT for hand-built windowed rendering past datatable limits — use lwc/lwc-virtualized-lists."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - User Experience
triggers:
  - "lwc slow list 10000 rows"
  - "virtualize lwc"
  - "lightning datatable performance"
  - "infinite scroll lwc"
tags:
  - performance
  - virtualization
  - datatable
inputs:
  - "row count"
  - "row height (fixed or variable)"
outputs:
  - "virtualized component or datatable config"
dependencies: []
version: 1.0.1
author: Pranav Nagrecha
updated: 2026-08-14
---

# LWC Virtualized Lists

Rendering 10,000 DOM nodes crashes mobile and lags desktop. This skill covers
the two paths that get you to a working long list: `lightning-datatable` with
infinite loading, and an `IntersectionObserver` sentinel for non-tabular
content. Hand-built windowed rendering — computing a visible slice from scroll
offset, spacer sizing, height measurement — is `lwc/lwc-virtualized-lists`.

**The distinction is not stylistic.** Infinite loading bounds the *network* work
by fetching in pages; loaded rows stay in the DOM, so memory grows monotonically.
Windowing bounds the *DOM* and is a harder build. Most Salesforce lists need only
the first, plus a stated ceiling.

## The Published Budget

From [Improve Datatable
Performance](https://developer.salesforce.com/docs/platform/lwc/guide/data-table-performance.html):

| Guidance | Value |
|---|---|
| Best performance | **1,000 rows and 5 columns** |
| Past 250 rows | fewer than **20 columns** |
| Per request | maximum **50 rows** via `LIMIT` |
| Inline editing | critical fields only — it costs performance |

Columns are a budget line, not a requirement. Row count is what teams manage;
column count is what they add without noticing.

## The Platform Ceiling That Shapes The Query

**`OFFSET` cannot skip more than 2,000 records**
([OFFSET](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_offset.htm)).
Page-number pagination therefore has a hard ceiling at `2000 / pageSize`, and
degrades before reaching it because the database scans and discards every skipped
row. Use **keyset pagination** — carry the last row's sort key as a cursor — with
a unique tiebreak:

```apex
WHERE CreatedDate < :cursorDate
   OR (CreatedDate = :cursorDate AND Id < :cursorId)
ORDER BY CreatedDate DESC, Id DESC
```

Without the tiebreak, rows sharing a timestamp are dropped or duplicated at page
boundaries — intermittently, which reads as a data bug.

## Adoption Signals

Lists beyond 500 rows or tables beyond 1,000. Not for short lists, and not
before measuring.

## Recommended Workflow

1. **Measure first.** Chrome DevTools Performance with 4× CPU throttling. Under
   ~100 ms first render and smooth scrolling there, stop — the complexity costs a
   class of bugs a plain list does not have.
2. **Datatable path:** `enable-infinite-loading` + `onloadmore`, inside a
   container with an **explicit height** — the table needs it to know where its
   bottom is, and the documentation ties it to preventing infinite looping. Raise
   `load-more-offset` above its 20px default so fetching starts before the user
   reaches blank space.
3. **Guard `loadmore`.** It fires repeatedly while the trigger zone is visible,
   so an in-flight boolean is required — and set `enableInfiniteLoading = false`
   on an empty page, or the table asks forever at the bottom of a complete list.
4. **Custom path:** one `IntersectionObserver`, created once (not per
   `renderedCallback`), with `root` set to the scrolling element via `lwc:ref` —
   the default `root: null` observes the viewport and fires continuously for a
   list scrolling inside its own container. `disconnect()` in
   `disconnectedCallback`.
5. **Filter on the server, debounced (~300 ms), and reset the cursor** on every
   filter or sort change. A client-side filter over a paginated list cannot see
   unloaded rows — a correctness bug that presents as missing data.
6. **State a ceiling with an escape hatch.** Past ~1,000 client rows, "showing
   the first 1,000 — narrow your filter or export" is a better product than a
   list that degrades silently.

## Key Considerations

- `aria-setsize="-1"` means "size unknown" and is the honest value for a
  progressively-loaded list. Reporting the loaded count as the total tells a
  screen-reader user the list is finished when it is not.
- Announce loading and completion in a polite live region. For
  `lightning-datatable`, do not hand-roll `aria-rowcount` — the base component
  owns its grid semantics.
- A keyboard user must never have to tab through 4,000 items to reach the footer.
- Variable row heights are not a problem for infinite loading (nothing is
  removed) and are the central problem for windowing.
- Custom cell types multiply their cost by every rendered row — minimise
  `setTimeout()`, promises, and DOM nesting inside them.

## Worked Examples (see `references/examples.md`)

- *10k-row audit log* — the wrong version and the right one, with the in-flight
  guard, the fixed-height container, and a stated ceiling.
- *Activity feed with `IntersectionObserver`* — correct `root`, single creation,
  teardown.
- *Keyset pagination in Apex* — cursor with a unique tiebreak, and the tradeoff
  table against `OFFSET`.
- *Debounced server-side filtering* — including the cursor reset everyone omits.

## Common Gotchas (see `references/gotchas.md`)

- **No fixed-height container** — `enable-infinite-loading` cannot function.
- **`loadmore` fires repeatedly** — one scroll gesture, four identical requests.
- **`OFFSET` caps at 2,000** — and degrades before it.
- **Observer with the default `root`** — fires continuously inside a scrolling
  container.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- `OFFSET` pagination past the 2,000-record platform ceiling.
- Keyset pagination with no unique tiebreak.
- Client-side filtering over a paginated list — a correctness bug, not a
  performance choice.
- `aria-setsize` set to the loaded count, telling a screen reader the list is
  complete.

## Official Sources Used

- Improve Datatable Performance — https://developer.salesforce.com/docs/platform/lwc/guide/data-table-performance.html
- lightning-datatable (Component Reference) — https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-datatable.html
- OFFSET (SOQL and SOSL Reference) — https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_offset.htm
- Access Elements the Component Owns (`lwc:ref`) — https://developer.salesforce.com/docs/platform/lwc/guide/create-components-dom-work.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
