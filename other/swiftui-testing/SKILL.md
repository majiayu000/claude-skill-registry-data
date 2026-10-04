---
name: swiftui-testing
description: "Design Swift Testing, XCTest, UI automation, preview fixtures, accessibility checks, and deterministic regression tests for SwiftUI features."
---

# Behavior tests, previews, and evidence

## Inputs

Identify the behavior contract, failure reproduction, test target/toolchain, injectable dependencies, current fixtures, and evidence level required.

## Rules

- **TEST-001 — Test observable behavior.** Assert state transitions and user outcomes; source-text assertions are secondary checks, not substitutes for execution.
- **TEST-002 — Make time and I/O controllable.** Inject clocks, clients, storage, IDs, and completion order where the behavior depends on them. Avoid arbitrary sleeps.
- **TEST-003 — Isolate fixtures.** Tests may run concurrently; avoid shared mutable globals, shared files, production accounts, and ordering assumptions.
- **TEST-004 — Match tool to claim.** Use Swift Testing or XCTest for appropriate behavior tests, UI automation for interaction, and rendered inspection for visual claims.
- **TEST-005 — Report exact proof.** A preview is not a test run, a snapshot is not accessibility proof, and a green mocked test is not a real-service result.

## Workflow

1. Reproduce the defect and write the smallest failing behavioral test when feasible.
2. Cover normal, boundary, failure, cancellation, and restoration paths relevant to the change.
3. Add deterministic previews for the important visual states without invoking production services.
4. Run targeted tests, then affected broader suites and destination builds.
5. Review failures before updating baselines or disabling checks; a replaced test must preserve its distinct proof claim.

## Verify

Run from a clean reproducible source state; record commands, toolchain, destination, pass/fail, and skipped gates. Repeat asynchronous tests under varied controlled completion orders.

## Output

Return the test matrix, results, artifact locations, and explicitly untested claims.

## References

Read the [playbook](references/testing-patterns.md) for decisions, failure cases, and source links.

For async tests, parameterization, and framework coexistence, read the [focused reference](references/async-and-migration-tests.md).
