---
name: unity-batchmode-build-verification
description: Use when a Unity batch or batchmode, BuildPipeline, Editor.log, PlayerSettings, or Unity CI job is involved.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [unity]
  versions: [2019.4+, 2021.3+, 6000+]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: gate
    lifecycle_stage: verify
    risk_level: low
    packs: [unity]
    side_effects: files
    artifact: unity-build-verdict.json
    required_evidence: [command-output, exit-code, build-log, artifact-path]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [build-and-runtime-verification, registry/capabilities.yaml domain catalog]
      copied_text: none
---
# Unity Batchmode Build Verification

## Overview
Verify Unity batch builds by command, environment, log, exit code, and observable artifact rather than treating process success as a complete build verdict.

## When to use
Use for Unity CI, local batchmode builds, platform player generation, build-script regressions, or missing output despite exit code zero.

## When NOT to use
Do not use to claim gameplay, visual, performance, store, or network correctness that the batch build did not exercise.

## Required inputs and context discovery
Collect Unity executable/version, project path, build method, target platform, output path, log path, timeout, package snapshot, expected artifact properties, and safe cache policy.

## Safety and risk level
Build outputs and caches are low-risk file side effects. Do not upgrade packages, save scenes, modify project settings, or overwrite release artifacts without approved scope.

## Workflow
1. Define the build claim, command, target, and expected artifact before execution.
   Completion criterion: success and failure signals are explicit.
2. Verify Unity version, license availability, project lock state, and output ownership.
   Completion criterion: unavailable prerequisites are BLOCKED.
3. Run the narrowest batchmode build and capture complete output.
   Completion criterion: exit code, duration, stdout/stderr, and log path are recorded.
4. Inspect the expected artifact and relevant log errors or warnings.
   Completion criterion: exit zero without the artifact is FAIL.
5. Issue PASS, FAIL, or BLOCKED with limitations and cleanup information.
   Completion criterion: the verdict does not imply untested runtime behavior.

## Evidence and output contract
Produce `unity-build-verdict.json` with command, Unity version, target, exit code, log, artifact path/properties, verdict, limitations, and generated side effects.

## Handoff contract
Record the failing command, first actionable log error, Unity/package snapshot, output path, generated caches, and next verification action.

## Pitfalls and anti-rationalization
- Exit code zero without the expected player is FAIL.
- A player artifact does not prove playmode behavior.
- Do not retry with package upgrades as a diagnostic shortcut.
- License or Unity runner absence is BLOCKED.

## Verification checklist
- [ ] Exact Unity command and version are recorded.
- [ ] Exit code and full log are captured.
- [ ] Expected artifact is inspected.
- [ ] Generated side effects are known.
- [ ] Limitations are explicit.

## References and scripts
Read [references/commands.md](references/commands.md) before constructing a Unity command. Use the bundled [scripts/build_evidence.py](scripts/build_evidence.py) to validate normalized build evidence and project-native Unity build methods for execution.
