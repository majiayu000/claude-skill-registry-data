---
name: safe-project-mutation
description: Use when changing project files or generated state requires a report-only dry run, exact scope, backup manifest, apply verification, and a tested restore path.
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
    risk_level: medium
    packs: [studio-core]
    side_effects: files
    artifact: mutation-manifest.json
    required_evidence: [dry-run-report, backup-manifest, verification-output, restore-path]
    owner: HoaTV Studio
    reviewer: QA Lead
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from:
        repo: vibeforge1111/keep-codex-fast
        path: SKILL.md
        commit: e74c4496aca550c54228740fcc144372308da529
        license: MIT
      patterns_from: [sanitized ownership preflight, AGENTS.md mutation policy]
      copied_text: none
---
# Safe Project Mutation

## Overview
Separate inspection from mutation. Every applied file change must be scoped, reviewable, restorable, and verified.

## When to use
Use for scripted edits, bulk normalization, generated files, project scaffolding, config rewrites, asset metadata operations, or any medium-risk file mutation.

## When NOT to use
Do not use this skill as the primary owner for a scaffold or per-project adapter; use `studio-project-scaffold` and keep mutation safety as its dependency. Do not use it to authorize database writes, service control, publishing, credential changes, destructive cleanup, or edits outside the user-approved repository.

## Required inputs and context discovery
Require repository root, exact operations, owned paths, excluded paths, expected before/after state, process/editor locks, reviewer, verification command, backup location, and restore objective.

## Safety and risk level
Default to report-only. Reject path traversal, source deletion, out-of-scope writes, unknown generated ownership, active editor/build/server conflicts, missing reviewer, or missing restore information.

## Workflow
1. Normalize every target path and prove it remains inside the approved root. Require a pre-change impact query under `code-intelligence-contract` before non-trivial code edits; do not expand write scope automatically.
   Completion criterion: affected paths, source owners, generated authorities, and approved write scope are explicit, or the graph lane is BLOCKED.
2. If the graph lane is BLOCKED, mutation may proceed only with Decision: `REVIEWER_ACKNOWLEDGED_FALLBACK`. Record explicit missing graph coverage/blocker, authoritative source owners, known callers/consumers, generated authorities or exact `NOT_APPLICABLE`, focused test commands, named reviewer, and residual risk. Preserve existing risk, approval, backup, and restore gates; any unresolved generated, cross-repository, or dynamic boundary remains BLOCKED, and graph verdict stays BLOCKED.
   Completion criterion: fallback fields are complete and approved write scope remains unchanged.
3. Run report-only mode and calculate proposed changes without writing files.
   Completion criterion: hashes and diff intent exist while source state is unchanged.
4. Create backups for existing targets and a manifest for creates, updates, and restore actions.
   Completion criterion: each operation has a backup or an explicit “created file; remove on restore” action.
5. Apply only the reviewed manifest.
   Completion criterion: actual hashes match the manifest’s expected outputs.
6. Run the declared verification command and capture exit code and artifacts.
   Completion criterion: success is supported by fresh output or labeled BLOCKED.
7. Exercise restore in a fixture or provide a verified restore command for the real scope.
   Completion criterion: the original hashes can be reproduced.

## Evidence and output contract
Produce a report-only plan, `mutation-manifest.json`, backup paths, before/after hashes, verification output, reviewer, and restore instructions.

## Handoff contract
Record pending versus applied operations, manifest path, backup root, verification state, restore command, and any process locks that must remain closed.

## Pitfalls and anti-rationalization
- Never skip report-only because an operation is “just formatting.”
- Never back up after mutation.
- Never delete source assets; archive or leave BLOCKED.
- Never hand-edit generated outputs without changing their source.
- Stale, broken, partial, unavailable, disabled, or unsupported graph state is BLOCKED graph evidence, not permission to assume a small blast radius.
- A reviewer fallback never converts graph BLOCKED into PASS or widens file ownership.

## Verification checklist
- [ ] Report-only mode did not mutate the fixture.
- [ ] Every path is inside approved scope.
- [ ] Backup and manifest predate apply.
- [ ] Verification output is fresh.
- [ ] Restore reproduces original state.

## References and scripts
Use the bundled [scripts/safe_mutation.py](scripts/safe_mutation.py) for deterministic file operations and the active project's `AGENTS.md` for repository-wide mutation rules when present.
