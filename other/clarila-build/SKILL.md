---
name: clarila-build
description: "Produce or inspect a source-bound build artifact for a requested candidate. Use for artifact preparation and inclusion evidence, not automatic distribution or store submission."
---

# Produce an attributable artifact

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve repository, full source SHA, clean/dirty state, intended platform, build profile, runtime and target environment.
2. Inspect the actual build command and CI auto-submit/distribution triggers before running it. Build permission does not imply permission for user-affecting routing or new spend.
3. Use project tooling and official provider CLIs. For Expo verify the current project configuration and use eas; use Bun in HeyAmara mobile.
4. Retain actual build receipt, artifact identity/hash when available, source/runtime/profile mapping and build logs. A successful job without an artifact is an acquisition gap.
5. Hand off the exact artifact to Verify/Capture or Release. Do not call an upload or build completion delivered.

## Acquire the artifact being verified

Follow the chosen command's actual trigger chain, including post-build hooks, auto-submit settings and destination routing, before starting it. Match the returned build to the requested source, profile and runtime using provider metadata and available artifact metadata.

Retain one build identity through polling, download and handoff. An interrupted read resumes acquisition of that build within the current retry budget. Record artifact location and digest when acquired, the inclusion evidence, and the exact remaining prerequisite when acquisition or installation is unavailable.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return artifact/source/platform identity, actual build result and downstream acquisition or verification gaps.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
