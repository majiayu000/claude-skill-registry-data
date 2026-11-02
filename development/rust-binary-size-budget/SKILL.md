---
name: rust-binary-size-budget
description: Track Rust executable and WASM artifact size by section, feature, dependency, and build profile.
---

# Rust Binary Size Budget

## Goal

Keep startup, download, disk, and memory costs within targets without deleting required functionality blindly.

## Inputs to inspect

Release artifacts, linker maps, cargo feature tree, target triple, build flags, and size goals.

## Workflow

1. Record exact compiler, target, profile, LTO/strip settings, enabled features, and artifact formats; measure compressed and uncompressed sizes separately.
2. Break down code, data, debug symbols, embedded resources, and dependency contributions using available tooling.
3. Inspect feature activation and duplicate implementation paths; identify optional capabilities that are pulled into default builds unintentionally.
4. Try one change at a time—feature gating, dead-code removal, dependency replacement, or resource compression—and measure size plus runtime impact.
5. Add a repeatable size report and threshold with an intentional exception mechanism for justified growth.

## Validation checklist

- [ ] Measurements use the same target and build settings.
- [ ] Debug symbols and production payload are not confused.
- [ ] Dependency/feature changes preserve required runtime behavior and licenses.
- [ ] Size thresholds are tied to a delivery or runtime constraint.
- [ ] Size improvement is not accepted if it breaks startup, performance, or required functionality.

## Required output

Produce a size baseline, section/dependency breakdown, tested reduction opportunities, and a CI size-regression threshold.

## Boundaries and failure handling

Do not compare debug builds with release builds; do not remove safety checks or required features solely to hit an arbitrary byte count.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
