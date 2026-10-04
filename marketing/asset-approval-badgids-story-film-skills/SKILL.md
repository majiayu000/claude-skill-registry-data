---
name: asset-approval
description: Register and approve generated or imported media across reference, voice, dialogue, music, SFX, video, master, trailer, social, artwork, and release groups with one durable primary/alternate/reject state model.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Asset Approval

## Workflow

1. Read `../../references/MEDIA_REGISTRY.md`, project dependencies, and the relevant source artifact.
2. Register each concrete media candidate in `00_project/media_registry.jsonl` with a new `MEDIA-###` ID.
3. Preserve the domain source ID such as `TAKE-###`, `VOICE-###`, `MUS-###`, `SFX-###`, `REF-###`, `TRL-###`, or `SOC-###`.
4. Use one approval group per decision scope.
5. Inspect media and relevant QC before selecting a primary.
6. Keep useful alternates. Keep rejected and superseded history. Rejection changes state; it does not physically delete a file.
7. Never select a QC-failed candidate without explicit `qc_override: true` and a concrete user-approved reason.
8. Use `scripts/media_registry.py` for deterministic state changes when available. Use `scripts/media_lifecycle.py` only after an explicit deletion or runtime-copy-repair request; it may delete only an exact eligible registered path and records the cleanup operation.
9. If a primary replacement affects downstream timing, identity, content, or continuity, run `project-impact`.

## Weak-model rule

Never infer approval from filename order, newest timestamp, highest seed, or generation success. Only `media_approvals.json` determines the current primary.

## Done

Every reviewed media group has zero or one primary, explicit alternates, preserved rejected history, and project-relative paths.
