---
name: clarila-mobile
description: "Investigate and implement a scoped iOS, Android or Expo issue in its verified worktree. Use for mobile behavior and for checking whether the configured Expo project, reported source, native artifact and device evidence apply to a mobile issue."
---

# Repair or implement mobile behavior

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the original issue, repository rules and accepted device/artifact evidence. Resolve the current worktree and inspect the native/JavaScript boundary.
2. For HeyAmara use Bun for installation, project-local bunx expo, expo-doctor and official eas commands. Read actual app configuration and cross-check its project identity against 4349641f-937e-4fa9-b5a7-43550301f065 before relying on project-scoped service data. If they differ, inspect repository/worktree identity and current project/account metadata read-only, record both IDs and resolve which belongs to this task from current owner/repository evidence. Do not repoint configuration or query the historical project as if it were current. Continue independent source work while an unresolved identity blocks dependent artifact conclusions. Use sentry for heyamara/ats-mobile and sentry-cli for artifacts, never service MCP tools.
3. Reproduce on a permitted simulator/device at identified source/artifact. Inspect and plan before edits. Capture original visible behavior before changing UI when required, using the [iOS/Android capture reference](../clarila-capture/references/mobile.md) for native screenshots and finalized recordings.
4. Implement the supported fix and run focused checks plus the affected device flow when the environment permits. Use clarila-test for automated test strategy/writing/maintenance and its [mobile checks](../clarila-test/references/mobile.md) to separate JavaScript test results from source-bound device evidence. Native byte changes need a compatible rebuilt artifact; OTA cannot establish native inclusion.
5. Hand off full source identity, build/runtime/update coordinates, device, executed checks and remaining independent verification.

## Verify the installed execution path

Trace the original action across JavaScript state, native modules and provider calls only where the failure crosses those boundaries. Select an artifact capable of exercising that path. Record the installed build/runtime/update coordinates and check which JavaScript source it actually runs.

For data-driven screens, exercise the relevant hydration, initial-load, refresh, offline and failed-save states. Preserve usable data and drafts through recoverable errors. Tie the observed device result to the current candidate, and retain any missing build or device prerequisite alongside completed local checks.

Discover and reuse the repository's maintained verifier and feature map before creating another launch/device driver. When a compatible artifact and task-owned device are available, drive one bounded native journey and retain the actual artifact/source and device evidence. A sanitized CLI-output fixture tests parsing and applicability only; keep that result separate from JavaScript tests, observed native behavior and live provider state.

For hydration, offline recovery, navigation or uncertain native inclusion, read [runtime and data decisions](references/runtime-data.md). Resolve only the relevant `expo-data`, `expo-sdk` or `apple-ui` expert through the [expert catalog](../clarila/references/expertise.md), checking installed versions and artifact needs before applying its examples.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return mobile source changes, artifact/device identity, scenario evidence and remaining build or acceptance requirements.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
