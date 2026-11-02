---
name: engine-asset-hot-reload
description: Design safe development-time asset hot reload with dependency tracking, atomic replacement, and runtime resource lifetime rules.
---

# Engine Asset Hot Reload

## Goal

Allow assets to change during development without stale dependencies, partial loads, dangling GPU handles, or inconsistent runtime state.

## Inputs to inspect

Asset loader, dependency graph, resource handles, import pipeline, renderer ownership, filesystem watcher, and current reload limitations.

## Workflow

1. Map the flow from source file through import, validation, CPU-side resource construction, GPU upload, dependency notification, and consumer update.
2. Assign stable asset identifiers and track reverse dependencies so a changed texture, shader, model, or material triggers only the affected resources.
3. Load and validate a replacement off to the side, then publish it atomically at a safe synchronization point. Keep the last known-good resource if parsing or upload fails.
4. Define ownership and retirement for old GPU resources so in-flight frames cannot reference released data. Avoid mutating shared resources halfway through a render or simulation phase.
5. Test rapid repeated edits, rename/delete events, partial writes, invalid assets, cyclic dependencies, and app shutdown during a pending reload.

## Validation checklist

- [ ] A failed reload leaves the last known-good resource usable and provides an actionable error.
- [ ] Resource swaps occur at a defined safe point and old resources are retired only after last use.
- [ ] Dependency invalidation is targeted and cannot silently miss transitive consumers.
- [ ] Filesystem events are debounced/coalesced without losing the final file state.
- [ ] Release builds can disable or restrict hot reload without changing asset identity semantics.

## Required output

Deliver a reload lifecycle diagram, asset dependency rules, failure behavior, resource lifetime strategy, and an acceptance test matrix.

## Boundaries and failure handling

Do not treat filesystem notifications as reliable final writes; do not free GPU resources immediately after replacing a handle.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
