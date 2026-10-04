---
name: studio-project-intake
description: Use when collecting a game project goal, scope, risk tier, engine and version, subsystem ownership, constraints, and do-not-touch paths into an actionable intake task packet.
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
    artifact: task-packet.json
    required_evidence: [file-list, git-status]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [sanitized ownership preflight, sanitized project map]
      copied_text: none
---
# Studio Project Intake

## Overview
Turn an ambiguous game-studio request into a bounded task packet before implementation or diagnosis begins.

## When to use
Use for new repositories, new sessions, cross-subsystem work, unclear ownership, risky changes, or tasks mentioning Unity, Lua, C++, services, databases, generated data, or external projects.

## When NOT to use
Do not repeat full intake when a current task packet already has verified scope and the request is a micro-change inside that scope.

## Required inputs and context discovery
Collect goal, user-visible success, workspace and nested Git roots, branch and dirty state per repository, engine/version, runtime topology, exact subsystem, risk tier, owners, dependencies, generated and excluded paths, do-not-touch paths, available commands, optional code-intelligence provider/version/index freshness, and blocked capabilities. For that optional lane, record provider/version, repository/revision/worktree binding, index state, capability, required languages, artifacts, side effects, and blocker.

## Safety and risk level
Intake is read-only. Inspect status and structure without starting services, opening editors, importing databases, or modifying project files.

## Workflow
1. Identify the requested outcome and the smallest repository boundary that can deliver it.
   Completion criterion: the goal and excluded scope are one sentence each.
2. Inspect Git status, applicable instructions, project maps, manifests, and relevant subsystem entry points.
   Completion criterion: current state and ownership risks are captured without mutation.
3. Classify risk as read-only, low, medium, or high and list forbidden actions.
   Completion criterion: each planned side effect has an approval and rollback requirement.
4. Record engine/version, services, ports, database/schema, generated-source relationships, and test commands only when verified.
   Completion criterion: snapshots are separated from hypotheses.
5. Select the next workflow skill and, for verified multi-repository work, include a conservative project-profile draft with unknown owners and commands labeled.
   Completion criterion: the task packet is executable without rediscovery and routes through `studio-workspace-routing` when applicable.
6. The graph lane is optional. Apply `code-intelligence-contract` only when graph context or capability is requested or materially useful for scoped intake; provider existence alone never triggers it. Pure intake remains intake, and the optional graph lane may stay absent or BLOCKED without failing intake; intake may still succeed when the graph lane is BLOCKED because intake owns scope discovery, not a graph verdict.
   Completion criterion: the packet records provider/version, repository/revision/worktree binding, index state, capability, required languages, artifacts, side effects, and blocker while keeping graph extraction separate from source/runtime verification.

## Evidence and output contract
Produce `task-packet.json` with goal, scope, risk, repository snapshot, owners, do-not-touch paths, dependencies, verification commands, expected artifacts, optional graph-lane state, and BLOCKED items.

## Handoff contract
If intake cannot resolve a required fact, hand off the exact question, inspected paths, evidence label, and the safest next read-only action.

## Pitfalls and anti-rationalization
- Do not infer engine or server versions from folder names alone.
- Do not treat credentials, ports, or DB names in old docs as current facts.
- Do not expand scope because adjacent cleanup looks useful.

## Verification checklist
- [ ] Goal and excluded scope are explicit.
- [ ] Owners and do-not-touch paths are listed.
- [ ] Risk and rollback expectations are assigned.
- [ ] Snapshot facts cite inspected paths or commands.
- [ ] The next workflow skill is named.

## References and scripts
Use project-local `AGENTS.md`, `HANDOFF.md`, `.agents/CONTRACT.md`, project maps, and `registry/capabilities.yaml` when present.
