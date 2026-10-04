---
name: studio-agent-orchestration
description: Use when selecting project investigator, implementer, independent verifier, or profile specialist roles with expected output, do-not-touch scope, critical-path ownership, disjoint writers, concurrency limits, or no child agents.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: plan
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: agent-plan.yaml
    required_evidence: [critical-path, ownership-map, role-contracts]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-09-07
    provenance:
      derived_from: none
      patterns_from: [sanitized bounded investigator implementer verifier roles]
      copied_text: none
---
# Studio Agent Orchestration

## Overview
Choose agent roles only where parallelism creates leverage. Keep the immediate critical path on the main thread and make every sidecar contract independently verifiable.

## When to use
Use when two or more independent workstreams exist, repeated discovery can be partitioned, a stable slice needs independent verification, or a project profile declares a specialist role.

## When NOT to use
Do not delegate small one-file work, immediate blockers, overlapping writes, shared unstable contracts, or tightly coupled edit-test iteration. Do not use a specialist outside its declared repository.

## Required inputs and context discovery
Collect the workspace route, immediate critical-path action, candidate workstreams, resolved profile and inferred role templates, capability scopes, exact active file assignments, read-only scopes, expected outputs, concurrency limit, available role definitions, and validation requirements.

## Safety and risk level
Planning is read-only. Agent role selection never expands mutation permissions. Investigator and review lanes remain read-only; implementers own exact disjoint paths; verifiers may write only normal test/build artifacts.

## Workflow
1. Identify the immediate critical-path action and keep it on the main thread.
   Completion criterion: no sidecar blocks the next local action.
2. Resolve profile specialists, inferred specialists, and canonical templates before reviewing effective owned scopes. Record broad scope intersections as `capability-overlap`; they describe what roles can own and do not by themselves block activation.
   Completion criterion: the review distinguishes effective capability patterns from exact files assigned in the current work packet.
3. Reject an active assignment outside its role's effective scope or any exact file assigned to more than one simultaneous writer. Also reject generated targets or unstable shared interfaces that lack one owner.
   Completion criterion: every concurrent writer has a disjoint exact write set, while disjoint assignments remain allowed even when role capabilities overlap.
4. Select the narrowest role: investigator for ownership discovery, implementer for bounded writes, verifier for independent checks, or a profile-declared specialist for difficult domain work.
   Completion criterion: role choice is justified by scope rather than prestige.
5. Bound concurrency by project profile and available independent work.
   Completion criterion: concurrency never exceeds three and may be zero.
6. Give each sidecar ownership, do-not-touch scope, expected output, and verification contract.
   Completion criterion: sidecars cannot create child agents and the main thread owns integration.

## Evidence and output contract
Produce `agent-plan.yaml` with critical path, role, owner, resolved scopes, advisory capability overlaps, exact active assignments, paths, do-not-touch, expected output, validation, concurrency, delegation reason, integration owner, and rejected parallelism.

## Handoff contract
Record active roles, ownership transfers, completed outputs, conflicts, commands, remaining verification, integration decisions, and the next main-thread action.

## Pitfalls and anti-rationalization
- More agents do not make coupled work independent.
- Broad capability overlap is not proof that two agents will write the same file; inspect the active exact assignments.
- Different disciplines are not permission to assign the same file to concurrent writers.
- A verifier does not become a source writer because a test fails.
- Specialist knowledge does not grant sibling-repository ownership.
- Waiting for a sidecar while local work is available wastes the critical path.

## Verification checklist
- [ ] The main thread retains the critical path.
- [ ] Resolved profile, inferred, and template scopes were reviewed.
- [ ] Concurrent exact file assignments are disjoint and within each role's effective owned scope.
- [ ] Role selection matches the task contract.
- [ ] Concurrency respects the profile and never exceeds three.
- [ ] Sidecars have expected outputs and cannot delegate.

## References and scripts
Use `registry/agent-roles.yaml` in a full repository clone and project-local `.codex/agents.generated.toml` only as an activation snippet. Full-clone and bundled scaffold planners expose `scope_review`; callers may pass current `active_assignments` as role IDs plus exact relative write paths. Use `studio-workspace-routing` before selecting project specialists.
