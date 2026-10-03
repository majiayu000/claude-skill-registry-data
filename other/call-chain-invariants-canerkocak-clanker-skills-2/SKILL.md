---
name: call-chain-invariants
description: >
  Classify which discovered product surfaces actually share an invariant before
  claiming a fix is complete. Use for multi-rail, admin/app, API/UI, lifecycle,
  explorer, fee, status, or repeated-state bugs where a one-surface patch may
  leave a reachable sibling broken. Consume the semantic blast-radius graph;
  do not assume a hard-coded chain or UI matrix applies.
---

# Call-chain invariants

A structural sibling is not automatically a semantic sibling. This skill takes
the canonical impact graph from `semantic-blast-radius` and answers one question:
which reachable product surfaces are governed by the same invariant?

It does not rediscover definitions and callers; that belongs to
`semantic-blast-radius` and `ast-grep-callchain-audit`.

## 1. Name the invariant and its owner

Write one falsifiable product sentence and identify the canonical owner or
oracle. Include units, state, direction, rail, authorization, or time basis when
those distinguish behavior.

Example:

> An external transaction link uses the row's authoritative network; a
> transaction-id shape never selects the network.

## 2. Derive product axes from evidence

Do not start from a fixed Eth/Solana/TRON/Canton or admin/app checklist. Inspect
the product model, route registrations, enums, state machines, API contracts,
workers, and runtime inventory. Derive only axes that can change the invariant,
such as:

- network or execution rail;
- operation or direction;
- lifecycle state and recovery path;
- user, admin, API, worker, or exported-library surface;
- current, legacy, migration, replay, or manually triggered producer;
- asset, currency, unit, valuation basis, or permission class.

An axis value is applicable only when source or runtime evidence shows a
reachable instance. Preserve `unknown` when access is missing.

## 3. Classify graph nodes

For every candidate surface returned by the impact graph, assign one status:

| Status | Meaning |
|---|---|
| **APPLIES** | The same owner, semantics, and harmful counterexample are reachable here. |
| **DIFFERENT CONTRACT** | It looks similar but has a different owner, unit, lifecycle, authority, or product rule. |
| **N/A** | The axis or surface does not exist for this product state; cite the evidence. |
| **UNKNOWN** | The surface may apply, but a dynamic edge, runtime inventory, or inaccessible source prevents classification. |

Do not turn `UNKNOWN` into `N/A`. Do not expand the user's scope merely because
a similarly named helper exists.

## 4. Build the smallest useful matrix

Rows and columns come from the applicable axes discovered above. A matrix is
useful only when two or more axes interact; otherwise a short list is clearer.

Mark each cell:

- `done` — applicable and covered by implementation plus evidence;
- `open` — applicable and not covered;
- `different` — verified different contract;
- `n/a` — verified absent;
- `unknown` — unresolved evidence gap.

Any acceptance-relevant `open` blocks completion. `Unknown` makes the result
`partial` unless the user explicitly accepts that limitation.

## 5. Decide whether logic should be shared

Two copies do not automatically justify a helper. Extract or reuse a shared
owner only when the copies have:

1. the same semantic contract;
2. the same owning layer;
3. compatible inputs, units, and failure behavior;
4. a reason to change together over time.

If those differ, keep the boundary explicit. If they match, prefer an existing
canonical helper and pass authoritative fields instead of guessing from shape.
Do not create a shared abstraction merely to make the matrix look symmetrical.

## 6. Return a graph delta

Return applicability evidence to the canonical impact graph:

```markdown
## Invariant surface classification
**Invariant and owner:** …
**Derived axes:** …
**Applies:** <surface — evidence>
**Different contract / N/A:** <surface — evidence>
**Open / unknown:** <surface — exact gap>
**Matrix:** <only when interacting axes make it useful>
**Shared owner decision:** reuse | extract | keep separate — <why>
**Coverage:** verified | partial
```

Do not present this as a second call-chain inventory. The completion claim is
made from the merged impact graph, focused tests, and applicable runtime
evidence.
