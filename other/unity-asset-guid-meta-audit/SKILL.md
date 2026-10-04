---
name: unity-asset-guid-meta-audit
description: Use when auditing Unity asset GUID and meta consistency, duplicate GUIDs, missing meta files, stale references, or import and prefab reference failures without editing assets.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [unity]
  versions: [2019.4+, 2021.3+, 6000+]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [unity]
    side_effects: none
    artifact: unity-guid-meta-audit.json
    required_evidence: [asset-list, guid-map, reference-map]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml domain catalog, Unity source-to-generated ownership]
      copied_text: none
---
# Unity Asset GUID Meta Audit

## Overview
Build a read-only map of Unity assets, `.meta` files, GUIDs, and serialized references before any import, regeneration, or asset edit.

## When to use
Use for duplicate GUID warnings, missing `.meta` files, broken prefab or scene references, stale GUIDs, merge damage, or unexplained import failures.

## When NOT to use
Do not use for draw order, clipping, runtime UI state, or broad asset reimport. Route those cases to the narrower Unity workflow.

## Required inputs and context discovery
Collect Unity version, project root, asset paths, meta paths, serialized reference sources, generated/vendor exclusions, version-control state, and no-touch asset rules.

## Safety and risk level
Read-only only. Never create, delete, copy, or regenerate `.meta` files during diagnosis. Any repair requires exact ownership, backup, and `safe-project-mutation`.

## Workflow
1. Inventory assets and their adjacent `.meta` files without opening or saving Unity.
   Completion criterion: every inspected asset is classified as paired, missing-meta, generated, vendor, or excluded.
2. Normalize GUID ownership into a deterministic map.
   Completion criterion: duplicate GUIDs cite every owning path.
3. Extract serialized GUID references from scoped text assets.
   Completion criterion: stale references cite source path and missing GUID.
4. Trace the editable source for generated or copied assets.
   Completion criterion: no generated destination is proposed as the repair source.
5. Produce a source-first repair plan and verification fixture.
   Completion criterion: proposed changes are reversible or remain BLOCKED.

## Evidence and output contract
Produce `unity-guid-meta-audit.json` with asset/meta pairs, duplicate GUIDs, missing meta, stale references, exclusions, limitations, and source-first recommendations.

## Handoff contract
Record Unity version, inspected roots, duplicate/stale GUIDs, protected paths, generated ownership, and the next safe repair experiment.

## Pitfalls and anti-rationalization
- Never generate a new `.meta` merely because one is missing.
- A text search result is not proof Unity imported the asset.
- Do not rewrite GUIDs across the project to silence one error.
- Missing Editor access is BLOCKED for live import confirmation.

## Verification checklist
- [ ] Asset and meta inventories are scoped.
- [ ] Duplicate GUIDs cite all paths.
- [ ] Stale references cite their sources.
- [ ] Generated/vendor paths remain untouched.
- [ ] Repair work is routed through safe mutation.

## References and scripts
Use the bundled [scripts/unity_guid_audit.py](scripts/unity_guid_audit.py) on normalized manifests and project-local Unity serialization rules.
