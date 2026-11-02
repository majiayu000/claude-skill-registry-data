---
name: rust-crate-boundary-audit
description: "Audits Rust crate boundaries, public APIs, and dependency direction. Use when a workspace grows circular concepts, duplicated abstractions, or slow builds from excessive coupling."
---

# Rust Crate Boundary Audit

## Use when
Crates are split by folder rather than responsibility, and harmless changes trigger broad rebuilds or expose implementation details.

## Workflow
1. Map workspace members, dependency edges, public exports, feature flags, unsafe blocks, and target-specific code.
2. Group crates by stable domain responsibility and identify cycles, duplicate types, oversized facades, or shared crates with unrelated concepts.
3. Trace one representative feature through its API boundaries and estimate refactor risk before moving code.
4. Propose incremental boundary changes with compile/test checkpoints rather than a workspace-wide rewrite.

## Required output
A crate dependency graph, boundary findings ranked by impact, candidate API changes, and a staged refactor plan.

## Validation
- Public APIs expose only types consumers need.
- Dependency direction follows domain ownership and has no unintended cycles.
- Feature combinations and supported targets remain buildable.

## Guardrails
Do not split crates merely to maximize count; optimize for stable ownership, compilation cost, and understandable contracts.
