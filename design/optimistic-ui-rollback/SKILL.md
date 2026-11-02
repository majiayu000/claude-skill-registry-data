---
name: optimistic-ui-rollback
description: Design optimistic UI updates with rollback, conflict reconciliation, and safe handling of overlapping mutations.
---

# Optimistic Ui Rollback

## Goal

Keep UI responsive without leaving local state inconsistent after failures or concurrent edits.

## Inputs to inspect

Mutation handlers, cache/state store, server concurrency model, optimistic paths, and error UI.

## Workflow

1. Classify the action as reversible, idempotent, or consequential; decide whether prediction is safe before server confirmation.
2. Define the optimistic transform and capture the minimal prior state/version required to restore or reconcile it.
3. Handle overlapping mutations by serializing, versioning, rebasing, or reconciling instead of restoring an outdated snapshot blindly.
4. Define behavior for timeout, permission change, validation failure, conflict, and ambiguous server outcome; refetch canonical state as needed.
5. Test rapid repeated actions, offline transitions, reversed responses, two-tab edits, and rollback after a later successful mutation.

## Validation checklist

- [ ] Failed mutations cannot undo newer successful state.
- [ ] Concurrent updates have an explicit conflict policy.
- [ ] Network ambiguity does not automatically imply the server rejected a mutation.
- [ ] Optimism is limited for high-consequence operations.
- [ ] Tests assert canonical final state under different response orders.

## Required output

Deliver a mutation state machine, snapshot/version model, conflict policy, and failure-sequence tests.

## Boundaries and failure handling

Do not restore the entire cache when unrelated changes may exist; do not announce irreversible success before confirmation.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
