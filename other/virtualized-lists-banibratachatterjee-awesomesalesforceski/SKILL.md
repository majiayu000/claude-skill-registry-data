---
name: virtualized-lists
description: "Render only visible rows for long lists (1k+ rows) using intersection observer or lightning-datatable virtual scroll. NOT for simple lists under 100 rows."
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
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# LWC Virtualized Lists

Rendering 10,000 DOM nodes crashes mobile and lags desktop. Virtualization renders only ~2 screens worth of rows and swaps them as the viewport scrolls. `lightning-datatable` has built-in infinite scroll; for custom layouts use an IntersectionObserver-based pattern with fixed row height. This skill covers both paths plus the accessibility requirements (aria-rowcount, keyboard reachability) that are easy to miss when optimizing for performance.

## When to Use

Lists beyond 500 rows or tables beyond 1000. Not for simple short lists.

Typical trigger phrases that should route to this skill: `lwc slow list 10000 rows`, `virtualize lwc`, `lightning datatable performance`, `infinite scroll lwc`.

## Recommended Workflow

1. Measure: if first render <100ms, skip virtualization.
2. `lightning-datatable enable-infinite-loading` + `onloadmore` handler that paginates server-side.
3. Custom: fixed row height + IntersectionObserver sentinels + windowed render of visible + buffer rows.
4. Cache row data client-side; server returns pages of 50–200.
5. Test with 10,000-row fixture to measure FPS and memory.

## Key Considerations

- Variable row heights break naive virtualization; use a measured-height library or fix the height.
- Screen readers must see a meaningful row count (`aria-rowcount`).
- Keyboard navigation must still reach off-screen rows logically.
- Server pagination > client-side filtering for 10k+ datasets.

## Worked Examples (see `references/examples.md`)

- *10k-row datatable* — Audit log viewer
- *Custom list with IO* — Activity feed

## Common Gotchas (see `references/gotchas.md`)

- **Variable row height** — Items jump around on scroll.
- **aria-rowcount missing** — Screen reader reports 'list with 20 items' on a 10k list.
- **Client-side filter on big list** — Re-filters 10k rows on each keystroke; jank.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Rendering 10k rows directly
- Client-side filter on huge datasets
- Missing aria-rowcount

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-wire-service-about.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
- SLDS 2 — https://www.lightningdesignsystem.com/2e/
