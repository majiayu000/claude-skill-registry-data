---
name: wire-service-patterns
description: "Use when designing or reviewing Lightning Web Components that use `@wire`, Lightning Data Service, UI API, or the GraphQL wire adapter, especially for reactive parameters, cache behavior, and refresh strategy. Triggers: 'wire service', 'refreshApex', 'reactive parameter', 'getRecord', 'wire vs imperative Apex'. NOT for component communication or generic lifecycle issues when data provisioning is not the main concern."
category: lwc
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Performance
  - Reliability
  - User Experience
tags:
  - wire-service
  - lightning-data-service
  - refreshapex
  - reactive-parameters
  - graphql-wire
triggers:
  - "when should i use wire vs imperative apex"
  - "refreshapex not updating my component"
  - "reactive wire parameter not firing"
  - "getrecord wire returns undefined"
  - "graphql wire uses errors instead of error"
  - "LWC not updating when data changes"
  - "component not updating when record changes"
inputs:
  - "data source such as UI API, Apex, or GraphQL"
  - "whether the component only reads data or also mutates it"
  - "what should trigger refresh or re-evaluation"
outputs:
  - "wire-service pattern recommendation"
  - "review findings for cache, reactive parameters, and refresh behavior"
  - "decision on wire adapters, LDS forms, or imperative Apex"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when the LWC data path needs to be intentional rather than incidental. The wire service is excellent for declarative, cache-aware reads, but only if the component understands immutability, reactive parameters, and when wire adapters will or will not re-evaluate. Use it when the LWC is not updating when data changes—often because the wire adapter isn't re-evaluating or a refresh wasn't triggered.

## Before Starting

- Is the component only reading Salesforce data, or does it also perform writes that should happen imperatively?
- Is the best data source a base component, a UI API wire adapter, an Apex wire adapter, or the GraphQL wire adapter?
- What event should actually refresh the data: parameter change, record change notification, or an explicit refresh call?

## Core Concepts

### Wire Is A Provisioning Model, Not A Lifecycle Hook

Wire adapters provision data when their configuration is complete and when Salesforce determines fresh data should be emitted. The component should not assume wire execution timing matches `connectedCallback()` or `renderedCallback()`. The framework owns when data arrives.

### Reactive Parameters Must Become Real Values

Dynamic wire parameters prefixed with `$` only work when the underlying values are defined. If a required reactive parameter is `undefined`, the wire adapter is not evaluated. This is one of the most common reasons a wire "doesn't fire."

### Wired Data Should Be Treated As Immutable Input

The wire service gives the component data to render, not mutable state to edit in place. Clone data before transforming it for UI use. Direct mutation of wired data leads to confusing bugs and stale state assumptions.

### Wire And Imperative Calls Solve Different Problems

Use wire for cache-aware reads and declarative reactivity. Use imperative Apex or LDS mutation APIs for creates, updates, deletes, and explicit user-triggered actions. If the component writes data, it also needs a clear refresh strategy for any wired reads that should update afterward.

## Common Patterns

### UI API Wire For Record Reads

**When to use:** The component reads record data and should inherit Lightning Data Service caching, sharing, CRUD, and FLS behavior.

**How it works:** Use adapters such as `getRecord` or object-info wires with schema imports and reactive record identifiers.

**Why not the alternative:** Custom Apex for standard record reads adds avoidable maintenance and can bypass built-in data protections.

### Imperative Mutation Plus Controlled Refresh

**When to use:** A user action updates data and the component must then refresh its wired state.

**How it works:** Perform the write imperatively, then use `refreshApex()` or the appropriate LDS notification pattern to refresh affected wired reads.

**Why not the alternative:** Expecting the wire adapter to notice every asynchronous server-side change leads to stale UI.

### GraphQL Wire For Multi-Entity Read Models

**When to use:** The component needs a richer read model than individual UI API wires can express cleanly.

**How it works:** Use the GraphQL wire adapter, remember that the response exposes `errors` instead of `error`, and keep the component read-focused.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Standard record read with strong platform security defaults | UI API wire adapter or LDS base component | Built-in cache plus sharing, CRUD, and FLS |
| User clicks Save or Submit and writes data | Imperative call | Writes are not a wire-service use case |
| Complex read model across related entities | GraphQL wire adapter | Cleaner multi-entity read shape |
| Wire depends on a value not available at first render | Use reactive parameters and guard for `undefined` | The wire only evaluates when config is complete |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] The component uses wire only for read/provisioning use cases.
- [ ] Reactive parameters are defined intentionally and not left `undefined` accidentally.
- [ ] Wired results are cloned before UI-specific mutation or sorting.
- [ ] Refresh behavior after writes is explicit, not assumed.
- [ ] Schema imports are used where referential integrity matters.
- [ ] GraphQL wire consumers handle `errors` rather than assuming `error`.

## Salesforce-Specific Gotchas

1. **A wire adapter does not guarantee when data arrives** — it can emit multiple times and is not tied to component lifecycle timing.
2. **Undefined reactive parameters stop evaluation** — many "wire isn't running" bugs are really incomplete configuration.
3. **GraphQL wire returns `errors`, not `error`** — assuming the standard wire error shape causes broken error handling.
4. **Async changes outside the adapter do not always auto-refresh** — Apex-triggered or Flow-triggered server updates often still need explicit refresh strategy.

## Output Artifacts

| Artifact | Description |
|---|---|
| Data-path recommendation | Decision on UI API, Apex wire, GraphQL wire, or imperative pattern |
| Wire-service review | Findings on reactive params, immutability, refresh, and cache usage |
| Refactor guidance | Concrete steps to fix stale data or misused wire patterns |

## Related Skills

- `lwc/lifecycle-hooks` — use when render timing or cleanup is the real problem rather than provisioning strategy.
- `apex/soql-security` — use when the component relies on custom Apex reads that need secure data access review.
- `lwc/lwc-offline-and-mobile` — use when the wire strategy must also account for mobile or offline behavior.
