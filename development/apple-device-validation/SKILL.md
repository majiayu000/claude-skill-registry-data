---
name: apple-device-validation
description: "Build, install, run, render, and validate Apple apps on the correct destination. Use for simulator/device evidence, screenshots, hardware, paired devices, and infrastructure triage."
---

# Apple runtime and device validation

## Inputs

Define the exact claim, authorized actions, source state, project/workspace, scheme, configuration, bundle, destination, required app state, and available tools. Discover current destinations instead of remembering device identifiers.

## Rules

- **PROOF-001 — Match evidence to claim.** Source, compile, tests, install, launch, rendering, interaction, hardware, and cross-device proof are distinct.
- **PROOF-002 — Respect action boundaries.** Installation does not authorize uninstall, data reset, account changes, or unrelated source edits. Advance only as the requested validation requires.
- **PROOF-003 — Reproduce the environment.** Record exact source, toolchain, destination/runtime, fixture state, commands, exit status, and relevant artifacts.
- **PROOF-004 — Classify infrastructure first.** Separate unavailable runtimes, pairing, service health, provisioning, installation, and application defects before changing code.
- **PROOF-005 — Validate the current candidate.** Repeat affected checks after changes; reconcile superseded receipts before reporting a blocker. Remove temporary harness state unless it is an intentional maintained test facility.

## Workflow

1. Set the minimum sufficient proof contract and inspect environment readiness.
2. Run the narrow build/test prerequisite for the selected destination.
3. Install, launch, interact, and capture evidence only within the authorized scope.
4. Exercise relevant lifecycle, failure, persistence, and system-boundary transitions.
5. Report the strongest supported claim and every blocked or unverified gate.

## Verify

For layout, inspect rendered output at risky sizes and accessibility settings. For persistence, prove store readiness, mutation, and relaunch. For hardware or paired-device claims, test the real boundary rather than substituting simulator success.

## Output

Return a compact evidence matrix with pass/fail/blocked/not-run, exact candidate and environment, artifacts, failure classification, and remaining device gates.

## References

Read the [playbook](references/device-validation-patterns.md) for decisions, failure cases, and source links. For a whole-app review or batch feedback, use the [screen review workflow](references/screen-review.md).

For debugger, simulator, and evidence integrity, read the [focused reference](references/debugger-and-simulator-evidence.md).
