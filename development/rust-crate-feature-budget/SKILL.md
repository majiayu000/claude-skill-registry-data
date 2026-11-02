---
name: rust-crate-feature-budget
description: Set and audit budgets for Rust crate features and optional dependencies to limit compile time, binary size, and accidental feature activation.
---

# Rust Crate Feature Budget

## Goal

Keep Cargo feature surfaces intentional as a workspace grows across library, server, client and platform-specific builds.

## Inputs to inspect

Cargo manifests and lockfile, cargo tree feature output, optional dependencies, target matrix, build timings and binary-size reports.

## Workflow

1. Inventory each crate's default/public features, optional dependencies, forwarded features and target-specific activation rules.
2. Measure clean and incremental compile time, dependency graph size and artifact size for a representative feature matrix.
3. Flag features that pull in heavy dependency trees, duplicate functionality, overlap semantically or are never exercised by supported consumers.
4. Propose a small public feature contract with clear defaults and independent optional capabilities; preserve compatibility when changing published crate behavior.
5. Add CI checks or periodic reports for feature-count/dependency/size growth, and verify minimum, default and maximum supported configurations.

## Validation checklist

- [ ] Each public feature has a defined user-visible capability and tested dependency forwarding.
- [ ] Default features avoid activating unrelated platform or runtime stacks.
- [ ] Published compatibility changes are assessed against downstream semver expectations.
- [ ] Budget alerts are based on measured growth and do not block intentional, documented changes without review.

## Required output

A crate feature matrix, dependency and build-cost baseline, budget thresholds, and compatibility-aware cleanup plan.

## Boundaries and failure handling

Do not remove a feature or alter defaults in a public crate without checking downstream users and semver implications.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
