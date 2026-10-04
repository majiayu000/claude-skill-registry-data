---
name: lwc-graphql-wire
description: "Use when an LWC needs to read related records across multiple sObjects in one request, paginate a related list with cursors, or replace several overlapping `@wire(getRecord)` calls with a single shared-cache query. Covers both. NOT for single-record reads where `getRecord` from `lightning/uiRecordApi` already fits — use lwc/wire-service-patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Security
  - Reliability
triggers:
  - "need to read account and related contacts in one request"
  - "how to paginate a graphql wire with cursors"
  - "graphql wire not refreshing after an imperative apex mutation"
  - "too many @wire(getRecord) calls for parent plus related list"
  - "what fields does ui api graphql support and how do i filter"
  - "why does my graphql field value come back as an object with value and displayValue"
  - "how do i pass a reactive variable into a gql template literal"
  - "migrate lightning/uiGraphQLApi to lightning/graphql v2"
  - "create or update a record from an lwc graphql mutation without apex"
  - "mark a graphql field optional so the query survives an fls restriction"
tags:
  - lwc-graphql-wire
  - graphql
  - ui-api
  - multi-entity-reads
  - cursor-pagination
  - refresh-graphql
  - reactive-variables
  - lightning-graphql-v2
  - execute-mutation
  - optional-fields
inputs:
  - "target sObjects and the relationship shape (parent-to-child, child-to-parent, polymorphic)"
  - "field selection the UI actually renders — not the full layout"
  - "pagination strategy: page size, starting cursor, and how 'load more' or filter changes reset state"
  - "filter and sort shape, including any reactive variables that change at runtime"
  - "refresh triggers — which imperative writes or platform events should invalidate the cache"
outputs:
  - "gql query template sized to the rendered UI with stable variable shape"
  - "cursor paginator pattern using `edges`, `node`, and `pageInfo.endCursor` / `hasNextPage`"
  - "refresh hook plan that calls `refreshGraphQL(this.wiredResult)` after mutations"
  - "review notes on cache sharing with LDS and FLS-trimmed field handling"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-07-07
---

# LWC GraphQL Wire

Use this skill when an LWC needs to read across more than one sObject or more than one related list in a single request, or when a component currently runs three or four overlapping `@wire(getRecord)` calls that could collapse into one cache-shared query. The GraphQL wire adapter shares the Lightning Data Service cache, enforces field-level security, and returns a structured response shaped around the `uiapi` root, `edges`, and `node`.

Two modules ship this adapter. Read the section below to pick the right one before writing any query — the response shape, cache behavior, and pagination model are the same, but the newer module adds optional fields, dynamic queries, and write support.

---

## Which Module: `lightning/graphql` (v2) vs `lightning/uiGraphQLApi` (v1)

Salesforce introduced `lightning/graphql` (v2) in Winter '26. Per the official reference, "`lightning/graphql` (v2) supersedes the `lightning/uiGraphQLApi` (v1) module," and Salesforce states: "We recommend that you use `lightning/graphql` (v2) where possible." Reach for v2 for all new GraphQL-wire work.

- **`lightning/graphql` (v2)** — the recommended module. Adds three capabilities v1 lacks: **optional fields** (mark a field so the query still succeeds when the user lacks FLS to it), **dynamic query construction** (build parts of the query at runtime with JS string interpolation inside the `gql` literal), and, since Spring '26, **mutations** — `executeMutation` for create/update/delete without Apex. It refreshes by calling a `refresh` method on the emitted wire result. It does **not** currently support Mobile Offline.
- **`lightning/uiGraphQLApi` (v1)** — retained specifically because it "supports Mobile Offline use cases, but it doesn't support newer features, such as optional fields and dynamic query construction." Use v1 only when the component must run in a Mobile Offline context. It refreshes with the standalone `refreshGraphQL(result)` helper.

The rest of this skill's read patterns (query shape, `edges`/`node`, cursor pagination, stable variables) apply identically to both modules. Where behavior diverges — string interpolation, optional fields, mutations, and the refresh call — the version is called out explicitly.

---

## Before Starting

Gather this context before authoring the component:

- Which sObjects and relationships does the UI render, and which fields are actually displayed? GraphQL is a shape-matching tool — over-selection here negates the payload win.
- Is the component read-only, or does it also create/update/delete? The GraphQL *wire* is read-only in both modules. On v2, writes can stay on GraphQL via `executeMutation` (create/update/delete, no Apex); on v1 they must go through UI API or imperative Apex.
- Which module will this run under? If the component ships to Mobile Offline, you are on v1 and lose optional fields, dynamic queries, and `executeMutation`. Otherwise default to v2.
- Is pagination needed, and if so, is a cursor-based model acceptable? The connection pattern exposes `pageInfo.endCursor` and `hasNextPage`; classic offset pagination is not the first-class model.
- What invalidates the view? A PE, a CDC event, an imperative Apex mutation — each implies a different refresh strategy built around `refreshGraphQL(this.wiredResult)`.

---

## Core Concepts

Three ideas carry most GraphQL-wire *reads*: the adapter response shape, reactive variables, and the connection-based pagination model. Two more apply on `lightning/graphql` (v2): optional fields and `executeMutation` writes.

### Adapter Shape And The `uiapi` Root

Importing `{ gql, graphql }` from `lightning/uiGraphQLApi` and wiring `@wire(graphql, { query, variables, operationName })` gives you a provisioned result whose `data` is rooted at `uiapi`. Field scalar values are returned as `{ value, displayValue }` objects, not bare primitives, because Salesforce exposes both raw storage values and locale-formatted display values. Templates must render `{record.Name.value}` or `{record.Name.displayValue}`, not `{record.Name}`. The adapter shares the LDS cache: if another component has already fetched the same record and fields, this wire is a cache hit.

### Reactive Variables And The `gql` Template Literal

`gql` is a tagged template literal that parses the query at module load. **Reactive** runtime values must be declared in the `query` block (for example `query ($id: ID) { ... }`) and passed through the wire config as a plain object referenced with a leading `$` (for example `variables: '$vars'`). Rebuilding the variables object on every render creates a new identity and defeats cache dedup; stabilize it in a getter or derive it from tracked fields so identity only changes when a value actually changes.

Note the version split on interpolation. On **v1**, `${jsValue}` inside the literal is an anti-pattern: it bakes a frozen value into the query text and never re-fires. On **v2**, dynamic query *construction* via JS string interpolation is a first-class feature — you can vary the query structure (an object name, a field set) at runtime. Even on v2, still route *reactive per-record filter values* (a record id that changes) through declared `$` variables; use interpolation to shape the query, not to smuggle in reactive data.

### Optional Fields (v2)

On v2 you can mark a field as optional so field-level security no longer breaks the whole query: when a field is marked optional, the query still succeeds even if the user lacks permission to see it. This is a different failure mode from the silent-`null` behavior of an ordinary field — a normal FLS-trimmed field comes back `null`, but a field the user cannot see that is *not* marked optional can fault the query. Mark fields optional when a subset of users legitimately lacks access and the UI can render without them.

### Mutations Via `executeMutation` (v2)

Since Spring '26, v2 exposes `executeMutation` for create/update/delete without Apex. Import it from `lightning/graphql` and call it with the same `{ query, variables, operationName }` shape as the wire. Refresh behavior is asymmetric and matters: **deletes** are removed from LDS wire results automatically ("Refreshes are not required for delete operations"), but **newly created records** "will not appear in existing GraphQL query results until the query is refreshed," and updates only propagate where cached data overlaps. So plan an explicit refresh after create/update, and skip it after delete.

### Connection Pagination Via `edges`, `node`, `pageInfo`

List queries return a connection: `edges { node { ... } cursor } pageInfo { endCursor hasNextPage startCursor hasPreviousPage }`. To implement "Load more", pass `first: N` and `after: $cursor` into the query and append new `node` values into a local array keyed by `Id.value`. The wire fires for each cursor change; accumulate rather than replace to preserve already-rendered rows. Offset pagination is not the adapter's native model — emulating it forces the adapter to discard cache benefits.

---

## Common Patterns

### Single-Query Replacement For Overlapping `getRecord` Calls

**When to use:** The component currently runs a parent `getRecord` plus one or more related-list or parent-of-parent wires, and the combined payload is still small enough to fit a single query.

**How it works:** Write one `gql` query that selects only the fields the UI renders, wire it once, and destructure in getters. The LDS cache still de-dupes parent-record access for other components on the page.

**Why not the alternative:** Multiple independent wires each have their own provisioning lifecycle, refresh hooks, and identity. They rerender independently, multiplying the surface area of cache-miss bugs.

### Cursor-Paginated "Load More"

**When to use:** The UI shows a related list that can grow beyond a reasonable first-paint size (typically >20 rows).

**How it works:** Track `cursor` as a reactive variable, bind it into `after: $cursor` in the query, and in the wire handler append `data.uiapi.query.<Entity>.edges` into a tracked array. Update `cursor` from `pageInfo.endCursor` only when the user clicks "Load more".

**Why not the alternative:** Replacing the accumulator on each wire fire causes list flicker and scroll-position loss. Treating `hasNextPage` as implicit from `edges.length` is unreliable because server-side filters may return a short page that is still not the last one.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Single record, id already known, UI renders a handful of fields | `@wire(getRecord)` from `lightning/uiRecordApi` | Simpler config, full LDS cache hit, no query parsing cost |
| Parent record plus one or more related lists in the same UI | GraphQL wire with a single `gql` query | One round trip, shared cache, consistent refresh handle |
| Component needs to write (create/update/delete) on v2 | `executeMutation` from `lightning/graphql` | Keeps the write on the same GraphQL/LDS path; no Apex needed (Spring '26+) |
| Component needs to write and must run Mobile Offline (v1) | UI API (`createRecord`, `updateRecord`, `deleteRecord`) or imperative Apex | The v1 wire is read-only and has no `executeMutation` |
| Query must survive users who lack FLS on a subset of fields | v2 optional fields | Query succeeds without the field instead of faulting |
| Query structure varies at runtime (object name, field set) | v2 dynamic query construction | v1 cannot build query text at runtime; v2 supports interpolation in `gql` |
| List that grows and needs "Load more" or infinite scroll | GraphQL wire with cursor pagination via `pageInfo` | Native shape of the connection pattern |
| Complex server-side aggregation or cross-org joins | Imperative Apex returning a DTO | GraphQL wire does not cover arbitrary aggregation or callouts |
| Single sObject list with standard filters rendered in a simple card | `@wire(getListRecords)` or `lightning-datatable` with LDS | Less boilerplate; GraphQL is overkill |

---

## Recommended Workflow

1. Pick the module — `lightning/graphql` (v2) for new work; `lightning/uiGraphQLApi` (v1) only if the component must run Mobile Offline. This decides which refresh call, whether `executeMutation` is available, and whether optional fields / dynamic queries are on the table.
2. Confirm scope — read-only, or does it also write? On v2, writes can stay on GraphQL via `executeMutation`; on v1 they disqualify the adapter and route to UI API / Apex.
3. Enumerate the minimal field list the UI actually renders and the relationships that join them; mark fields optional (v2) where a subset of users lacks FLS.
4. Draft the `gql` query with a `query ($vars: ...)` signature, validate it against the official UI API GraphQL examples, and stabilize the variables object in a getter so its identity only changes when a value changes; reference it as `$vars`.
5. Store the wired result in the handler and plan the refresh: on v2 call `result.refresh()`; on v1 call `refreshGraphQL(this.wiredResult)`. After a v2 `executeMutation` delete, skip the refresh (LDS auto-removes); after create/update, refresh.
6. Add cursor-paginated accumulation only if the list can grow; key accumulated rows by `Id.value`.
7. Run `scripts/check_lwc_graphql_wire.py --manifest-dir force-app/main/default/lwc` and resolve every finding.

---

## Review Checklist

- [ ] The module choice is deliberate: `lightning/graphql` (v2) unless the component must run Mobile Offline (v1).
- [ ] On v1, the component reads only and all writes go through UI API or imperative Apex; on v2, writes use `executeMutation`.
- [ ] Every scalar access in the template uses `.value` or `.displayValue`; no bare `{record.Field}` reads.
- [ ] Reactive per-record filter values flow through declared `$` variables, not `${...}` interpolation. (v2 interpolation is reserved for shaping query structure, not smuggling reactive data.)
- [ ] Variables object identity is stable across renders; it is not rebuilt in the template or in `renderedCallback`.
- [ ] Pagination uses `pageInfo.endCursor` and `hasNextPage`; "Load more" appends instead of replaces.
- [ ] The correct refresh is called after mutations that change queried data: `result.refresh()` on v2, `refreshGraphQL(this.wiredResult)` on v1 — and no refresh after a v2 delete.
- [ ] Fields that a subset of users may lack FLS on are marked optional (v2) so the query does not fault.
- [ ] The query selects only the fields the UI renders; no speculative "include everything we might need" selection.

---

## Salesforce-Specific Gotchas

1. **`${jsValue}` for reactive data is a v1 anti-pattern, not a universal one** — on v1 it bakes a frozen value into the query and never re-fires; route reactive values through declared `$` variables. On v2, interpolation *is* supported for dynamic query construction (varying the query structure), so scope this rule by module and by intent.
2. **Scalars are wrapped objects** — `Name` comes back as `{ value, displayValue }`. Forgetting `.value` in the template silently renders `[object Object]`.
3. **v2 and v1 refresh differently** — v2 calls a `refresh` method on the emitted wire result (`result.refresh()`); v1 calls the standalone `refreshGraphQL(this.wiredResult)`. Neither is `refreshApex` (that is for `@wire(<apexMethod>)` only).
4. **Pagination is cursor-based** — the connection shape exposes `pageInfo.endCursor`/`hasNextPage`. Emulating offset pagination defeats caching and drifts on inserts.
5. **FLS is enforced silently** — inaccessible fields return `null` without an error; tests on a privileged admin user can mask data loss that production users will hit. On v2, mark such fields optional so a missing permission does not fault the whole query.
6. **Unstable variables thrash the cache** — rebuilding `{ ids: [...], limit: 25 }` on every getter call creates a new identity each render; memoize it.
7. **The *wire* is read-only; on v2 writes go through `executeMutation`** — you cannot embed a `mutation { ... }` block in the wired `gql` query. On v2, create/update/delete run through `executeMutation` from `lightning/graphql` (Spring '26+); on v1 there is no write path and mutations must use UI API or Apex. After a v2 create/update, refresh; after a v2 delete, LDS auto-removes the record.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `gql` query template | A minimal query sized to the rendered UI, with declared variables and an `operationName` for telemetry |
| Paginator pattern | A `loadMore()` handler that appends new `edges` and advances the cursor from `pageInfo.endCursor` |
| Refresh hook plan | A documented list of imperative mutations paired with `refreshGraphQL(this.wiredResult)` calls |
| Checker report | Line-numbered findings for JS interpolation inside `gql`, wrong refresh helper, missing `pageInfo`, and mutation attempts |

---

## Related Skills

- `lwc/wire-service-patterns` — use when the decision is how to provision data generally; this skill is the GraphQL-specific deep dive.
- `lwc/lwc-imperative-apex` — use when writes or complex server-side logic disqualify the GraphQL wire.
- `lwc/lwc-wire-refresh-patterns` — use when the core problem is invalidating cached data after a mutation across wire types.
