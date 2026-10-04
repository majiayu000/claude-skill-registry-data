---
name: save-data-schema-migration
description: Use when versioning or converting serialized player save files, profiles, checkpoints, or persistence payloads across recognized save-format versions with fixture compatibility and rollback.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: safety
    lifecycle_stage: build
    risk_level: high
    packs: [cpp-lua-mmorpg]
    side_effects: files
    artifact: save-migration-plan.json
    required_evidence: [schema-version, fixture-result, rollback-plan, reviewer-approval]
    owner: HoaTV Studio
    reviewer: QA Lead
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [safe-project-mutation, registry/capabilities.yaml domain catalog]
      copied_text: none
---
# Save Data Schema Migration

## Overview
Plan and test player-save migrations through an explicit version chain while preserving the original payload and refusing unknown or newer versions.

## When to use
Use for save field renames, defaults, removals, version upgrades, backward compatibility, import migrations, or player-data format changes.

## When NOT to use
Do not use for database schema migration, arbitrary config edits, or direct production player-save rewrites without a project runbook.

## Required inputs and context discovery
Require current and target versions, migration chain, save authority, fixture set, backup scope, rollback method, compatibility window, reviewer, human approval, privacy constraints, and validation checks.

## Safety and risk level
High-risk. Unknown versions, incomplete chains, missing backup, missing rollback, missing reviewer, live player data, or missing approval means BLOCKED.

## Workflow
1. Identify save authority, current version, target version, and supported compatibility range.
   Completion criterion: unknown or newer versions are BLOCKED.
2. Review each one-version migration step for rename, default, removal, and data loss.
   Completion criterion: irreversible transformations are explicit.
3. Preserve the original fixture and run migration on a copy.
   Completion criterion: fixture mutation cannot destroy rollback input.
4. Validate migrated semantics and backward/forward compatibility expectations.
   Completion criterion: expected fields and values are asserted.
5. Prepare exact backup, apply, rollback, reviewer, and approval evidence for real scope.
   Completion criterion: real player data remains untouched until authorized.

## Evidence and output contract
Produce `save-migration-plan.json` with versions, migration hashes, fixture results, compatibility, rollback, reviewer, approval, verdict, and limitations.

## Handoff contract
Record save authority, version chain, fixture paths, migration result, data-loss risks, backup/rollback, approval state, and next authorized action.

## Pitfalls and anti-rationalization
- Never guess an unknown save version.
- A successful JSON parse is not semantic compatibility.
- Do not test with the only copy of a player save.
- Database migration safety is a separate workflow.

## Verification checklist
- [ ] Version chain is complete.
- [ ] Original fixture is preserved.
- [ ] Migration and rollback are tested.
- [ ] Compatibility risks are explicit.
- [ ] Reviewer and human approval gate real apply.

## References and scripts
Use the bundled [scripts/save_migration.py](scripts/save_migration.py) for isolated fixtures and `safe-project-mutation` for authorized file application.
