---
name: swiftui-lazy-stack-benefit-gate
description: "Use when a task involves deciding whether a SwiftUI lazy stack improves a measured workload to record Swift, Xcode, operating-system, build, and target versions; reproduction steps; data sensitivity; and the permission boundary before acting. Check current Apple or Swift documentation, preserve source and trace provenance, and verify on an owned test target. Do not change signing credentials, publish, notarize, or operate production systems without explicit approval."
---

# SwiftUI Lazy Stack Benefit Gate

## Overview

This skill applies when a task involves deciding whether a SwiftUI lazy stack improves a measured workload. Its intended outcome is to record Swift, Xcode, operating-system, build, and target versions; reproduction steps; data sensitivity; and the permission boundary before acting.

## When to Use

### Preserved source section: When to Use

Use this skill when deciding whether a SwiftUI lazy stack improves a measured workload. It is a focused engineering workflow for an authorized Apple-platform codebase or test environment; it does not itself authorize access to devices, credentials, accounts, signing infrastructure, or production systems.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

Do not assume lazy stacks are universally faster or preserve identical layout behavior for every view.
- Never expose signing keys, authentication tokens, private crash data, or user content in logs, prompts, or external services.
- Do not publish, notarize, submit, sign, install persistent helpers, change security permissions, or alter remote build infrastructure without explicit authorization from the owner.
- Do not bypass Gatekeeper, TCC, App Sandbox, code-signing validation, or user consent to make a test pass.
- Stop and ask when ownership, license, data handling, deployment target, or release authority is unclear.

### Source boundary statements from: Topic Provenance

This skill is independently authored for this repository. The linked public catalog was used only as a topic-discovery seed; its root LICENSE was reviewed as MIT, but no upstream prose, code, commands, examples, prompts, scripts, or assets were copied. Some entries in that repository are symlinks or carry separate attributions, so no license permission is inferred for those targets. The linked Apple or Swift documentation is a version-sensitive reference, not a substitute for current project policy or independent testing.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs and Boundaries

Record repository and source revision, Swift and Xcode versions, OS and SDK, target and build configuration, device or simulator, reproduction steps, expected behavior, data sensitivity, and the accountable owner. Identify whether the work is analysis, a local change, CI configuration, or a release-facing action. Use test accounts and synthetic fixtures when possible.

## Instructions

### Preserved source section: Workflow

1. **Set the boundary.** State the technical question, affected target, intended output, source revision, environment, permission scope, and stop condition. Separate an engineering assessment from an authorized code or release change.
2. **Establish evidence.** Capture the relevant build settings, diagnostics, trace, test result, or signed artifact identity. Pin toolchain and target versions; redact credentials, user content, and private paths from shared artifacts.
3. **Apply the focused method.** Start from the current container, record initial render, scrolling, memory, and layout behavior, then compare the lazy alternative against the same dataset and device conditions.
4. **Verify a bounded result.** Check view realization count, estimated versus resolved geometry, scroll jumps, accessibility traversal, and memory. Compare against a reproducible baseline or an independent test when feasible; report what the evidence does and does not show.
5. **Hand off safely.** Record findings, versions, artifacts, uncertainties, remaining tests, and decision owner. Keep proposed changes separate from applied changes and preserve a recovery path.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Inputs and Boundaries

Record repository and source revision, Swift and Xcode versions, OS and SDK, target and build configuration, device or simulator, reproduction steps, expected behavior, data sensitivity, and the accountable owner. Identify whether the work is analysis, a local change, CI configuration, or a release-facing action. Use test accounts and synthetic fixtures when possible.

### Source conditional guidance from: Workflow

4. **Verify a bounded result.** Check view realization count, estimated versus resolved geometry, scroll jumps, accessibility traversal, and memory. Compare against a reproducible baseline or an independent test when feasible; report what the evidence does and does not show.

### Source conditional guidance from: Apple-Platform Checks

- Verify the exact Swift compiler, language mode, SDK, OS, target, architecture, and build configuration when behavior depends on them.

### Source conditional guidance from: Guardrails

- Stop and ask when ownership, license, data handling, deployment target, or release authority is unclear.

## Tools and Resources

### Preserved source section: Topic Provenance

This skill is independently authored for this repository. The linked public catalog was used only as a topic-discovery seed; its root LICENSE was reviewed as MIT, but no upstream prose, code, commands, examples, prompts, scripts, or assets were copied. Some entries in that repository are symlinks or carry separate attributions, so no license permission is inferred for those targets. The linked Apple or Swift documentation is a version-sensitive reference, not a substitute for current project policy or independent testing.

Topic source: [steipete agent-scripts topic catalog](https://github.com/steipete/agent-scripts)
Technical reference: [Apple SwiftUI performance documentation](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance)

## Output Format

Not specified in source skill.

## Validation Checklist

### Preserved source section: Apple-Platform Checks

- Verify the exact Swift compiler, language mode, SDK, OS, target, architecture, and build configuration when behavior depends on them.
- Distinguish source-level reasoning, static compiler checks, simulator behavior, physical-device measurements, and production observations.
- Treat traces, crash reports, test bundles, screenshots, archives, and symbols as potentially sensitive; minimize and redact before sharing.
- Recheck current Apple or Swift primary documentation for tool flags, platform requirements, entitlements, and distribution policy.

**Unchecked checklist derived from source criteria (not test evidence):**

- [ ] Verify the exact Swift compiler, language mode, SDK, OS, target, architecture, and build configuration when behavior depends on them.
- [ ] Distinguish source-level reasoning, static compiler checks, simulator behavior, physical-device measurements, and production observations.
- [ ] Treat traces, crash reports, test bundles, screenshots, archives, and symbols as potentially sensitive; minimize and redact before sharing.
- [ ] Recheck current Apple or Swift primary documentation for tool flags, platform requirements, entitlements, and distribution policy.

## Edge Cases and Recovery

### Source edge/failure guidance from: Workflow

5. **Hand off safely.** Record findings, versions, artifacts, uncertainties, remaining tests, and decision owner. Keep proposed changes separate from applied changes and preserve a recovery path.

## Stop Conditions

### Source stop-related guidance from: Workflow

1. **Set the boundary.** State the technical question, affected target, intended output, source revision, environment, permission scope, and stop condition. Separate an engineering assessment from an authorized code or release change.

### Source stop-related guidance from: Guardrails

- Stop and ask when ownership, license, data handling, deployment target, or release authority is unclear.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Acceptance

The result answers the stated engineering question, identifies source and tool versions, includes reproducible evidence and limitations, and names any required owner approval. It makes no unsupported claim of platform compatibility, security, performance, or release readiness.
