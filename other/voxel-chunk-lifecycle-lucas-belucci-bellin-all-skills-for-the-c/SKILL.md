---
name: voxel-chunk-lifecycle
description: "Models the lifecycle of streamed voxel chunks and their ownership. Use when adding chunk loading, generation, meshing, GPU upload, eviction, or cancellation."
---

# Voxel Chunk Lifecycle

## Use when
Chunks appear twice, disappear during reload, keep stale meshes, or finish asynchronous work after they have been unloaded.

## Workflow
1. Define explicit states such as absent, requested, generating, generated, meshing, ready-to-upload, resident, and evicting.
2. Assign each request a chunk key plus generation/version token so stale async completions can be rejected.
3. Specify ownership for voxel data, mesh data, GPU resources, and neighbor dependencies; define cancellation and eviction rules.
4. Test every transition, including unload/reload during generation, neighbor edits, world shutdown, and repeated requests.

## Required output
A state-transition table, ownership diagram, cancellation contract, and lifecycle regression cases.

## Validation
- Every async result checks that its token still matches the current chunk generation.
- Resources are freed exactly once and stale meshes cannot replace newer ones.
- Boundary and shutdown transitions are covered.

## Guardrails
Do not rely on timing delays or arbitrary sleeps to hide lifecycle races; expose state and make transitions testable.
