---
name: unity-client-offline-debugging
description: Use when a Unity client cannot enter offline gameplay because login, bootstrap, disconnected server handling, local mock data, network fallback, or scene startup paths fail.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [unity]
  versions: [2019.4+, 2021.3+, 6000+]
  platforms: [windows]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [unity]
    side_effects: none
    artifact: unity-offline-debug-report.md
    required_evidence: [reproduction, log-paths, bootstrap-trace]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [Hermes promotion source unavailable locally BLOCKED, independently authored workflow]
      copied_text: none
---
# Unity Client Offline Debugging

## Overview
Trace offline startup from entry scene through configuration, authentication bypass, local data, network fallback, and gameplay scene activation without editing Unity assets first.

## When to use
Use when offline mode hangs, redirects to login, waits for a disconnected server, lacks mock data, fails bootstrap, or enters the wrong scene.

## When NOT to use
Do not use when the client enters offline mode but a widget, canvas, NGUI item, prefab, atlas, or draw order is wrong.

## Required inputs and context discovery
Collect Unity version, entry scene, offline flag source, bootstrap components, login/network path, local data path, expected scene, logs, reproducible steps, and asset or scene no-touch rules.

## Safety and risk level
Read-only diagnosis first. Do not open or save scenes/prefabs, regenerate project files, upgrade packages, or change serialization without explicit mutation scope and backup.

## Workflow
1. Reproduce the offline failure and capture the first divergent log or state.
   Completion criterion: expected and observed startup paths are documented.
2. Trace how the offline flag is sourced and propagated through bootstrap.
   Completion criterion: the first missing or overwritten state is identified.
3. Inspect authentication bypass, network timeout/fallback, and local mock data contracts.
   Completion criterion: offline dependencies are classified as present, missing, stale, or BLOCKED.
4. Trace scene activation and required managers without saving Unity assets.
   Completion criterion: the failing code/data boundary is narrowed.
5. Hand a minimal failing test or instrumentation plan to `evidence-first-debugging`.
   Completion criterion: no speculative asset edits occurred.

## Evidence and output contract
Produce reproduction steps, Unity/version snapshot, log paths, bootstrap trace, offline flag source, dependency state, suspect paths, verdict, and next experiment.

## Handoff contract
Record entry scene, expected scene, offline flag source, network behavior, local data dependencies, logs, asset no-touch paths, and the next discriminating check.

## Pitfalls and anti-rationalization
- Do not assume “offline” means every network call is bypassed.
- Do not fix UI rendering when startup never reaches the UI state.
- Do not save scenes or prefabs during read-only diagnosis.
- Missing Unity Editor access is BLOCKED for live reproduction.

## Verification checklist
- [ ] Failure was reproduced or BLOCKED.
- [ ] Offline flag propagation was traced.
- [ ] Network and local data dependencies were separated.
- [ ] Scene activation path was inspected.
- [ ] No Unity asset was mutated during diagnosis.

## References and scripts
Read [references/commands.md](references/commands.md) for offline flag precedence, bootstrap ordering, player-log paths, network timeout inspection, and the startup-versus-UI boundary check. Use Unity logs, project bootstrap code, configuration sources, and project-local offline run guides. No generic script can replace project-specific startup tracing.
