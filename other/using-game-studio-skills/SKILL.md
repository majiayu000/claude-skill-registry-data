---
name: using-game-studio-skills
description: Use when starting any GameStudio-CodexKIT task or when a model runner is unavailable and someone requests a confidence-based PASS.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: root
    lifecycle_stage: discover
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: operating-contract.md
    required_evidence: [task-packet, verdict]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-09-03
    provenance:
      derived_from: none
      patterns_from: [AGENTS.md evidence labels, sanitized studio operating contract]
      copied_text: none
---
# Using Game Studio Skills

## Overview
Apply the kit as a workflow router: inspect context, select the narrowest skill, preserve safety gates, and label every claim honestly.

## When to use
Use at the start of every kit-guided task and whenever a task changes scope, risk, owner, or verification strategy.

## When NOT to use
Do not use this root contract as a substitute for intake, debugging, mutation, review, build verification, or handoff workflows.

## Required inputs and context discovery
Collect the workspace and repository paths, current branch or snapshot, user goal, explicit constraints, available tools, project-profile path when present, and any do-not-touch paths.

## Safety and risk level
This skill is read-only. It classifies work and routes it; it never authorizes mutation, service control, database changes, publishing, credentials, or destructive cleanup.

## Repeated work strategy gate
Before execution, assess whether the selected workflow repeats the same action across records, files, or assets. Three or more similar records, files, or assets, or any high-volume set, requires an explicit choice among manual, reuse, extend, or create-tool. This threshold requires assessment; it does not justify a new tool by itself.

Prefer reuse or extension of an existing tool, converter, validator, or batch workflow. Keep a small one-off task manual when direct handling is clearer and lower risk. A new or extended tool must be deterministic, use bounded scope and bounded output, emit a manifest or structured log, validate results, and quarantine recoverable per-item failures. Mutating tools require report-only or dry-run behavior. Long-running pipelines must be resumable, and repeated operations must be idempotent or detect already completed state. Fail fast instead of quarantining when a failure invalidates shared integrity.

Group failures into a failure cluster by common cause. Repair the owning rule, converter, or pipeline and rerun the affected cluster instead of defaulting to individual record edits. Tool use does not expand authority: commit, service control, database actions, Unity mutation, publishing, credentials, and destructive actions retain the selected workflow's approval gates.

## Three-stage output contract

### Stage 1 - task packet
The report-only router or `gamestudio guide` produces a task packet with the planning status `READY`, `AMBIGUOUS`, or `BLOCKED`; that status is never a runtime `PASS`. `READY` authorizes no execution or mutation. It only means that current project evidence selected one canonical workflow.

The public intent vocabulary is Diagnose, Verify, Plan Change, Ship, and Handle Incident across eight Golden Path families: project adoption and routing, local environment recovery, Unity client entry recovery, C++ server failure recovery, Unity UI and localization, Unity build and asset integrity, Lua contract and server authority, and data and live release safety. Current unsupported role, intent, project, or installed-capability combinations return a task-packet `BLOCKED` with `selected_workflow: null`. The operator may run `studio-project-intake` or select a canonical skill directly outside `gamestudio guide`.

### Stage 2 - canonical workflow
When the packet is `READY`, only the selected canonical workflow executes or reviews its own actions and emits its workflow-specific artifact. The router does not inherit, weaken, or impersonate that workflow's execution, review, mutation, approval, or evidence contract.

### Stage 3 - normalized evidence card
After the workflow acts, its observed result is summarized by a normalized evidence card with a runtime verdict of `PASS`, `BLOCKED`, or `FAIL` as applicable. For an unsupported router outcome, the root skill may issue a normalized `BLOCKED` evidence card without a workflow artifact. The router cannot fabricate the final runtime verdict.

## Explicit KIT Goal participation
Ordinary tasks keep the three-stage contract unchanged and do not acquire progress files. When the operator explicitly opts the current long-running task into a KIT-managed Goal, route Goal preflight and initialization, meaningful-boundary event submission, state recovery, and `Open Progress` to `studio-goal-progress`. The active workflow remains authority for packet completion and evidence truth. If that capability is absent, invalid, or unavailable, Goal progress is `BLOCKED`; never simulate percentage, ETA, events, or a GUI from commentary or elapsed wall time.

## Workflow
1. Collect the repository path, project profile, goal, constraints, available tools, do-not-touch paths, and any explicit role, intent, or mode.
   Completion criterion: request context is bounded and unknowns are labeled.
2. When role or mode is absent, use the project profile's `studio_experience` defaults. Infer one intent from Diagnose, Verify, Plan Change, Ship, or Handle Incident; if the top Golden Paths remain ambiguous, ask one question.
   Completion criterion: role, intent, mode, and candidate Golden Paths are explicit.
3. Assess repeated work and record the strategy as manual, reuse, extend, or create-tool before item-by-item processing begins.
   Completion criterion: three-or-more or high-volume scopes have an explicit tool assessment, tool contracts match the repeated work strategy gate, and one-off work is not over-engineered.
4. Select the narrowest canonical workflow. A role preset is advisory and cannot override repository evidence, missing capabilities, or risk gates.
   Completion criterion: the normalized task packet names the selected workflow or reports `BLOCKED` with the missing prerequisite.
5. If the task explicitly opted into a KIT-managed Goal, require `studio-goal-progress` preflight before initialization and emit only start, packet transition, evidence observation, plan revision, context refresh, terminal, or explicitly bounded heartbeat events.
   Completion criterion: ordinary tasks remain unchanged, ordinary commentary and raw tool output do not become progress events, and missing progress capability remains `BLOCKED`.
6. Preserve the selected workflow's evidence and mutation contracts without weakening them in Basic mode; the selected workflow, not this router, executes or authorizes its work.
   Completion criterion: Basic and Advanced modes differ only in presentation and explicit controls.
7. If a workflow was selected, require it to return its workflow-specific artifact, a normalized evidence card, and one next action. If routing is unsupported, return no workflow artifact and preserve the task-packet and evidence-card `BLOCKED` state.
   Completion criterion: commands, exit codes, artifacts, limitations, restore information, and blockers remain available without an invented workflow result.

## Evidence and output contract
Return the planning task packet first. Only a selected canonical workflow may add its native artifact. Return the normalized evidence card last, with a runtime verdict backed by that workflow's observed evidence or by the root router's explicit unsupported blocker. `BLOCKED` is a valid outcome; fabricated PASS is not.

## Handoff contract
Record repository/path, branch, goal, owned scope, do-not-touch paths, files touched, commands, verified results, snapshots, hypotheses, failures, decisions, next actions, and a reactivation prompt.

## Pitfalls and anti-rationalization
- “The change is small” does not waive intake or verification.
- “It compiled” does not prove runtime or regression safety.
- “The runner is unavailable” means `BLOCKED`, never PASS.
- “Another project uses this pattern” is a snapshot until this repository is inspected.
- “Automation is faster” does not justify a new tool or waive mutation and approval gates.

## Verification checklist
- [ ] The primary workflow skill is explicit.
- [ ] KIT Goal participation is explicit or ordinary task behavior remains unchanged.
- [ ] Repeated work has an explicit manual, reuse, extend, or create-tool decision.
- [ ] Every material claim has an evidence label.
- [ ] Side effects match the declared risk gate.
- [ ] Unavailable live operations are `BLOCKED`.
- [ ] Final verification is fresh.

## References and scripts
Use the active project's `AGENTS.md` when present and route through the installed skill catalog. Use the bundled [scripts/studio_experience.py](scripts/studio_experience.py) planner with the normalized [task-packet](schemas/studio-task-packet.schema.json) and [evidence-card](schemas/studio-evidence-card.schema.json) schemas for role-aware routing output. The planner selects routes but never executes or authorizes the selected workflow. Architecture, registry, and `scripts/doctor.py` maintenance checks are available only in a full repository clone.

## Negative scope
This root skill does not debug failures, mutate files, run database migrations, start or stop services, replace project intake, perform review lanes, generate adapters, or claim verification for commands it did not run.
