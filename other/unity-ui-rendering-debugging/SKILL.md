---
name: unity-ui-rendering-debugging
description: Use when a Unity UI, HUD, screen item, or NGUI widget is missing, clipped, behind another canvas, wrongly sorted, disconnected from a prefab or atlas, misanchored, or invisible despite correct gameplay state.
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
    artifact: unity-ui-debug-report.md
    required_evidence: [hierarchy-path, render-order, prefab-reference]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [Hermes NGUI promotion source unavailable locally BLOCKED, independently authored workflow]
      copied_text: none
---
# Unity UI Rendering Debugging

## Overview
Separate data/state problems from hierarchy, activation, geometry, clipping, material, atlas, camera, canvas, and NGUI depth problems before editing assets.

## When to use
Use when a known UI state should render but a widget, item, canvas, prefab, atlas sprite, anchor, mask, or sorting layer is wrong or invisible.

## When NOT to use
Do not use when the Unity client never reaches the offline/gameplay state, login/bootstrap fails, or network fallback is the primary symptom.

## Required inputs and context discovery
Collect Unity and UI framework versions, hierarchy path, prefab source, expected data/state, activation state, canvas/camera, layer, sorting order or NGUI depth, clipping/mask chain, material/atlas, anchors, and no-touch asset rules.

## Safety and risk level
Read-only diagnosis first. Do not save scenes or prefabs, reimport assets, change GUID/meta files, upgrade UI packages, or batch-reserialize without scoped mutation and backup.

## Workflow
1. Prove the underlying data and state say the item should exist.
   Completion criterion: rendering is isolated from business logic or routed elsewhere.
2. Trace hierarchy presence, active state, scale, position, and parent clipping.
   Completion criterion: the first invisible transform or activation condition is identified.
3. Inspect canvas/camera/layer/sorting or NGUI panel and widget depth.
   Completion criterion: render-order conflicts are supported by values, not screenshots alone.
4. Inspect prefab links, materials, atlases, sprite names, masks, and anchors.
   Completion criterion: missing or stale asset references are named with paths.
5. Define the smallest reversible change and verification scene or fixture.
   Completion criterion: any asset edit routes through `safe-project-mutation`.

## Evidence and output contract
Produce hierarchy path, state proof, render-order values, clipping chain, prefab/material/atlas references, suspect cause, proposed minimal change, and verification plan.

## Handoff contract
Record scene/prefab paths, hierarchy, framework version, expected state, inspected render values, asset references, no-touch paths, and the next reversible experiment.

## Pitfalls and anti-rationalization
- Do not blame draw order before proving the object exists and is active.
- Do not reimport or resave assets as a diagnostic shortcut.
- Do not change `.meta` or GUID files outside exact scope.
- Missing Unity Editor access is BLOCKED for visual confirmation.

## Verification checklist
- [ ] Data/state and rendering were separated.
- [ ] Hierarchy and activation were inspected.
- [ ] Canvas/NGUI order and clipping were measured.
- [ ] Prefab/material/atlas references were checked.
- [ ] Any proposed edit is reversible and scoped.

## References and scripts
Read [references/commands.md](references/commands.md) for stack detection markers, serialized-value inspection, runtime probes, camera culling checks, and the diagnostic order that avoids false draw-order root causes. Use project scenes, prefabs, UI framework docs already vendored in the project, and Unity logs. Avoid package upgrades during diagnosis.
