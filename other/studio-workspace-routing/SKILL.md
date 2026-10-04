---
name: studio-workspace-routing
description: Use when `.agents/project-profile.yaml`, nested Git roots, or cross-repository game work requires a profile-defined repository route, validation slice, or cross-project phase.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: router
    lifecycle_stage: discover
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: workspace-route.json
    required_evidence: [project-profile, repository-owner, validation-slice]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-09-07
    provenance:
      derived_from: none
      patterns_from: [sanitized multi-repository workspace routing]
      copied_text: none
---
# Studio Workspace Routing

## Overview
Route work through one project-profile seam so repository ownership, project-local facts, and verification stay local while reusable workflow logic stays in the kit.

## When to use
Use when `.agents/project-profile.yaml` exists, the workspace contains nested Git roots, ownership is unclear across client/server/services, or one feature crosses repositories.

## When NOT to use
Do not use for a single known repository and subsystem with an already selected owner skill. Do not replace project intake when the profile is missing or unverified.

## Required inputs and context discovery
Collect the workspace root, profile path, current repository snapshots, requested goal, candidate paths, cross-project contract, exclusions, owner skills, and declared validation commands.

## Safety and risk level
This skill is read-only. It selects scope and evidence; it does not authorize edits, builds, services, database operations, publishing, or agent activation.

## Workflow
1. Load and validate the project profile before routing.
   Completion criterion: invalid, missing, or stale ownership remains Unverified or BLOCKED. Overlapping declared capability patterns remain valid profile metadata; exact concurrent assignment conflicts are checked after agent templates and inferred roles resolve.
2. Select one repository and subsystem owner for repository-local work.
   Completion criterion: one owner skill, write scope, and do-not-touch scope are explicit.
3. Split cross-project contracts into ordered repository phases.
   Completion criterion: authority, interface handoffs, and integration ownership are named.
4. Choose the narrowest declared validation for each phase.
   Completion criterion: every phase has a command, risk level, expected artifact, or explicit BLOCKED state.
5. Hand the bounded route to the owning workflow and re-route if scope changes.
   Completion criterion: sibling repositories are not changed for convenience.

## Evidence and output contract
Produce `workspace-route.json` with profile snapshot, selected repository, subsystem, owner skill, phase, owned paths, exclusions, validation, authority, and evidence labels.

## Handoff contract
Record profile path, repository snapshots, selected route, unresolved ownership, phase order, commands, artifacts, blockers, and the prompt that resumes the next phase.

## Pitfalls and anti-rationalization
- Directory names alone do not prove ownership.
- Cross-project work is not one shared write scope.
- Capability scope overlap is not an active write collision; the current work packet still needs disjoint exact file assignments.
- A convenient command is not valid unless the profile or project evidence owns it.
- A stale profile is Snapshot evidence, not current truth.

## Verification checklist
- [ ] The profile is valid and current enough for the decision.
- [ ] One repository owner exists per phase.
- [ ] Cross-project authority and handoffs are explicit.
- [ ] Validation is the narrowest meaningful declared slice.
- [ ] Sibling repositories remain outside the active write scope.

## References and scripts
Use bundled `scripts/project_profile.py` to validate profiles and render workspace and validation references. Pair delegation decisions with `studio-agent-orchestration`.

