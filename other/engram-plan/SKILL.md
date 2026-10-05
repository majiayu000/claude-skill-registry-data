---
name: engram-plan
description: Plan engram implementation work from the architecture and contract docs. Use when sequencing Rust crates, TypeScript packages, storage adapters, retrieval pipelines, bindings, evaluation milestones, or future code/document knowledge-source extensions.
---

# Engram Plan

Use this skill when turning the engram architecture into implementation slices. Plans should stay modular, composable, and contract-backed: Rust owns the deterministic core, TypeScript owns integration ergonomics, and adapters sit behind stable ports.

## Required Context

Read these files before planning implementation:

- `docs/domain-data-model.md`
- `docs/architecture.md`
- `docs/research/synthesis.md`
- `docs/rfcs/0001-memory-layer-scope.md`
- `docs/rfcs/0002-knowledge-source-extension.md`
- `references/crate-map.md`

## Planning Rules

- Treat the accepted domain model as the source of truth.
- Keep SQL, vector stores, model providers, and Node runtimes outside the Rust core domain crate.
- Prefer ports and adapters over baked-in infrastructure.
- Plan vertical slices that can be tested with in-memory adapters before persistent storage.
- Make evaluation part of each milestone instead of a separate late-stage project.
- Call out contract risks before implementation risks.

## Default Build Order

1. Contract freeze review and implementation stack ADR.
2. Rust domain crate with serde-compatible types and invariants.
3. Rust engine crate with ports, in-memory store, policy gate, and retrieval pipeline skeleton.
4. Evaluation fixtures and deterministic regression harness.
5. Adapter crates for SQL/vector/object storage.
6. N-API TypeScript package and generated TypeScript contract types.
7. Ingestion extensions for code and unstructured documents.
8. Background consolidation, belief derivation, hierarchy maintenance, and observability.

## Output

Plans should include:

- Crates and packages affected.
- Contract surfaces involved.
- First testable slice.
- Explicit deferrals.
- Verification commands.
