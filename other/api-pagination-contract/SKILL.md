---
name: api-pagination-contract
description: Design pagination contracts that remain stable under concurrent inserts, updates, deletes, and changing sort order.
---

# Api Pagination Contract

## Goal

Prevent clients from skipping or duplicating records when navigating large or changing result sets.

## Inputs to inspect

List endpoint, sort keys, filters, data volume, update rate, database query, and client navigation needs.

## Workflow

1. Document default and supported sort order, stable tie-breaker, page-size bounds, filter semantics, and whether total counts are exact, estimated, or omitted.
2. Choose offset or cursor pagination based on data size and mutation frequency; define opaque cursor contents, signing, expiry, and filter binding when needed.
3. Ensure sort fields establish a deterministic total order, including nulls and equal timestamps, and match indexes where required.
4. Test concurrent inserts/deletes, edits to sort keys, repeated cursors, invalid/expired cursors, and pages at result boundaries.
5. Specify next/previous links, empty-page behavior, backward compatibility, and safeguards against unbounded page sizes or expensive arbitrary sorts.

## Validation checklist

- [ ] Every page has deterministic order for a given snapshot/contract.
- [ ] Cursor reuse with different filters or sort parameters is rejected or explicitly supported.
- [ ] Pagination limits protect resource budgets.
- [ ] Concurrent mutation behavior is documented and tested.
- [ ] API docs define whether traversal is a live view or a consistent snapshot.

## Required output

Produce a pagination schema, cursor rules, query/index notes, mutation test matrix, and client integration examples.

## Boundaries and failure handling

Do not use an unstable timestamp without a unique tie-breaker; do not advertise snapshot consistency if the implementation provides a live changing view.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
