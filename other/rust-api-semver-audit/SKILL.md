---
name: rust-api-semver-audit
description: Audit Rust library changes for semantic-versioning impact on public types, traits, features, and downstream compilation.
---

# Rust Api Semver Audit

## Goal

Prevent accidental breaking changes and choose a release version consistent with the library's published compatibility promise.

## Inputs to inspect

Public crate API, prior/current release diff, Cargo features, rustdoc output, and declared MSRV.

## Workflow

1. Enumerate public exports and compare function signatures, trait requirements, struct fields, enum variants, visibility, feature flags, and minimum supported Rust version.
2. Identify source, type-inference, behavior, and feature-activation breaks, including implementations downstream crates must provide.
3. Review default-feature changes, dependency type exposure, error variants, and auto-trait/Send/Sync changes that may affect consumers.
4. Compile representative downstream fixtures against the candidate version and prior baseline; use API diff tools if available.
5. Classify every finding as breaking, additive, behavioral, or policy-sensitive and recommend version/deprecation/migration notes.

## Validation checklist

- [ ] Public API changes are compared against a specific released baseline.
- [ ] Semver impact includes trait implementations and feature behavior, not just function names.
- [ ] MSRV and target support changes are explicit.
- [ ] Downstream compile fixtures include common external usage patterns.
- [ ] Uncertain behavioral compatibility is documented rather than assumed.

## Required output

Produce a public API diff, compatibility findings, versioning recommendation, downstream fixture results, and migration notes.

## Boundaries and failure handling

Do not claim semver compatibility solely because internal tests pass; do not remove deprecated APIs before the published support policy allows it.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
