---
name: lwc-performance
description: "Use when designing or reviewing Lightning Web Components for slow initial load, heavy rerenders, large-list rendering, payload reduction, and lazy instantiation choices such as `lwc:if`, tabs, or dynamic components. Triggers: 'slow lwc', 'rerenders too much', 'key index', 'dynamic import', 'large list lag'. NOT for wire-service data-source selection when provisioning strategy is the only question or for mobile/offline-specific tuning."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
triggers:
  - "lwc component rerenders too often and feels slow"
  - "large list in lwc lags when records load"
  - "should i use dynamic import or lazy instantiation in lwc"
  - "if:true versus lwc:if performance problem"
  - "getrecord layout fetch makes my component slow"
  - "need to optimize a heavy lightning page component"
tags:
  - lwc-performance
  - lazy-instantiation
  - list-rendering
  - payload-reduction
  - dynamic-components
  - render-optimization
inputs:
  - "where the slowness appears: first load, interaction, rerender, or large data set"
  - "current data path such as LDS base components, UI API, GraphQL, or Apex"
  - "component hierarchy, optional UI sections, and expected list sizes"
  - "target runtime such as Lightning Experience, Experience Cloud, or managed package constraints"
outputs:
  - "performance review findings with prioritized bottlenecks"
  - "refactor guidance for payload, rendering, and lazy-loading decisions"
  - "checker output for list, directive, and dynamic-component smells"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

# LWC Performance

Use this skill when the LWC works functionally but costs too much: slow first paint, laggy filters, expensive list rerenders, or optional UI that loads before the user asks for it. Optimize payload size, component instantiation, and DOM churn before reaching for micro-optimizations.

---

## Before Starting

Gather this context first:

- Is the pain on initial page load, after a user interaction, or only when the data set grows?
- Is the component using LDS base components, UI API wire adapters, the GraphQL wire adapter, or Apex, and how much data is being requested?
- Which UI sections are always needed, and which sections could be deferred behind tabs, disclosure, or conditional rendering?
- If dynamic components are being considered, is Lightning Web Security enabled and is the package model compatible with `lightning__dynamicComponent`?

---

## Core Concepts

Performance problems in LWC usually come from one of four places: too much data, too many component instances, unstable list identity, or reactivity that causes more rerendering than the user actually needs.

### Start With The Cheapest Data Path

Salesforce’s own guidance is to prefer base components built on Lightning Data Service, then LDS/UI API wire adapters, then GraphQL for multi-entity reads, and Apex only when those options do not fit. That order matters for performance because LDS shares cache, security checks, and refresh behavior across components. It is also why layout-based record fetches are a red flag for narrow UIs: you often pay for hundreds of fields when the component needs five.

### Reactivity Controls Rerender Cost

Primitive fields rerender when their value identity changes. Objects and arrays rerender when you assign a new value, and `@track` is only the deep-observation tool for plain objects and arrays. It does not make `Date`, `Set`, or `Map` mutations observable. Another important nuance from the docs: even with `@track`, LWC rerenders only when properties accessed during the previous render change. That is good for performance, but it surprises teams that mutate an object in place and expect broad UI refreshes.

### Template Directives Affect Instantiation And Evaluation

`lwc:if`, `lwc:elseif`, and `lwc:else` are the current conditional-rendering primitives. Salesforce explicitly says `if:true` and `if:false` are no longer recommended, may be removed in the future, and are less performant in chained conditions. Use getters for computed conditions and treat conditional rendering as a performance tool: if a section is not needed yet, avoid instantiating it yet.

### Lists Need Stable Identity And Bounded Size

When a list changes, the framework uses `key` to rerender only the affected items. The key must be stable, unique, and not the loop index. Stable keys reduce DOM churn; bounded list size reduces the absolute amount of DOM to diff. For large datasets, paginate, virtualize, or progressively reveal more rows rather than rendering every record at once.

### Dynamic Import Is Specialized, Not The Default

Dynamic components can help avoid loading large modules that are not always needed, but Salesforce’s current documentation is explicit about the tradeoff: dynamic import adds runtime overhead, requires Lightning Web Security, and dynamic components are supported only in managed packages, not unlocked packages. Start with static imports. Move to dynamic import only when the deferred component is genuinely heavy or unknown until runtime.

---

## Common Patterns

These patterns solve most real LWC performance issues without adding brittle complexity.

### Data-Minimized Read Model

**When to use:** The UI reads Salesforce data and feels slow because it requests full layouts, multiple overlapping calls, or Apex for standard CRUD-shaped reads.

**How it works:** Prefer LDS base components for standard record UI, LDS/UI API wire adapters for focused reads, and the GraphQL wire adapter when one query can replace multiple requests. Request only the fields and rows you need. If Apex remains necessary, make the caching and refresh behavior explicit.

**Why not the alternative:** Layout-based fetches and generic Apex wrappers often inflate payload size, bypass shared cache advantages, and create unnecessary refresh work.

### Progressive Disclosure And Lazy Instantiation

**When to use:** The component contains analytics panels, secondary tabs, modals, or rarely used renderers that do not need to exist on first paint.

**How it works:** Use `lwc:if`, App Builder visibility, or lazy tab/content patterns so the expensive child component is created only when the user asks for it. Use dynamic components only when the constructor is optional at runtime and the package and LWS constraints are satisfied.

**Why not the alternative:** Rendering every optional child up front increases bundle cost, component creation time, and server work before the user has expressed intent.

### Bounded Lists With Stable Keys

**When to use:** Search results, dashboards, or custom data tables render dozens or hundreds of repeated child rows.

**How it works:** Page or virtualize the collection, use a unique key from the incoming dataset, and prefer event delegation on the list container instead of one listener per row.

**Why not the alternative:** `key={index}` and unlimited list rendering cause row identity bugs, listener bloat, and full-list rerender churn when only one row changed.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard record view or edit UI | Use LDS base components first | Built-in caching and security with less custom code |
| Component needs a narrow read model | Use UI API or GraphQL and request exact fields | Smaller payload and fewer calls |
| Optional heavy panel or tab | Gate it with `lwc:if` or lazy tab activation | Avoid up-front instantiation cost |
| Renderer is chosen from metadata at runtime in a managed package | Use dynamic components with a statically analyzable import map | Deferred loading is justified and platform constraints are met |
| Large result set or custom table | Paginate or virtualize and use stable row keys | Reduces DOM size and preserves row identity |

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

- [ ] The component uses the cheapest viable data path before custom Apex is introduced.
- [ ] Record reads request explicit fields instead of layout-based payloads.
- [ ] Nonessential panels, tabs, or child components are deferred intentionally.
- [ ] Lists use stable non-index keys and do not render an unbounded number of rows.
- [ ] Conditional rendering uses `lwc:if` chains instead of legacy `if:true` or `if:false`.
- [ ] Object and array state updates rely on reassignment or intentional `@track` usage.
- [ ] Any dynamic import has a clear benefit and satisfies LWS plus managed-package constraints.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **`if:true` and `if:false` still work, but they are the slower legacy path** — Salesforce now recommends `lwc:if` and notes that chained `if:true` or `if:false` checks are not as performant and may be removed in the future.
2. **`@track` is not a general deep-reactivity switch** — it observes plain objects and arrays, but not internal mutations to `Date`, `Set`, `Map`, or class instances.
3. **The list key is part of the rendering contract** — missing keys or `key={index}` force more DOM churn and can scramble row-specific UI state.
4. **Dynamic components are not a universal lazy-loading trick** — they require LWS, `lightning__dynamicComponent`, and managed-package support, and they are not prefetched automatically.
5. **Layout-shaped record fetches are expensive by default** — a simple card can become slow because the payload includes far more data than the UI renders.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Performance review | Prioritized findings on payload size, rerendering, list scale, and deferred UI opportunities |
| Refactor plan | Concrete steps to reduce data, delay instantiation, or stabilize list rendering |
| Checker report | File-level findings for deprecated directives, list keys, layout fetches, and dynamic-component setup |

---

## Related Skills

- `lwc/wire-service-patterns` — use when the core decision is which data provisioning model to choose rather than UI rendering cost.
- `lwc/lifecycle-hooks` — use when the main problem is `renderedCallback`, listener cleanup, or lifecycle-driven rerender bugs.
- `lwc/lwc-offline-and-mobile` — use when the performance issue is specific to mobile containers, connectivity, or device constraints.
