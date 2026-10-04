---
name: feature-to-work-packets
description: Use when decomposing an approved specification into ordered work packets with a file owner, exact paths, single-writer ownership, dependencies, risks, evidence, and verification commands.
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
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: work-packets.yaml
    required_evidence: [approved-spec, ownership-map, verification-plan]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [sanitized multi-project subsystem registries, AGENTS.md ownership waves]
      copied_text: none
---
# Feature to Work Packets

## Overview
Turn a testable feature spec into implementation units that can be owned, sequenced, reviewed, and verified without overlapping writes.

## When to use
Use before multi-file, multi-subsystem, or multi-agent implementation when the specification is approved and dependency order matters.

## When NOT to use
Do not use when the feature direction or specification remains unresolved, or when the task is a single-file micro-change.

## Required inputs and context discovery
Require approved spec, repository map, generated/source relationships, subsystem owners, applicable instructions, dependency graph, risky files, verification commands, and unavailable tools.

## Safety and risk level
Packet authoring is low-risk. Packets cannot grant destructive actions or overlapping write ownership, and they must preserve external and generated no-touch rules.

## Workflow
1. Map specification requirements to concrete subsystems and source-of-truth files.
   Completion criterion: generated outputs and external dependencies are distinguished from editable sources.
2. Build the dependency graph and identify immediate blockers versus parallel sidecars.
   Completion criterion: ordering is based on real interfaces, not team preference.
3. Create packets with one objective, `workflow_id`, owner, repository phase, exact owned files, excluded files, inputs, outputs, authority handoff, and risks. For a progress-enabled KIT Goal, also require positive integer `progress_weight`, required evidence kinds, optional or null `estimate_seconds: {low, high}`, and timing policy `max_active_timed_packets: 1`.
   Completion criterion: no two concurrent packets own the same path or generated target, cross-project phases have one integration owner, and every opted-in progress packet has complete fields without inferred equal weights.
4. Attach focused and broader verification commands plus expected artifacts.
   Completion criterion: each packet has an objective completion check.
5. Define integration and review packets owned by the orchestrator or reviewer.
   Completion criterion: shared registries and final verdict have a single owner.

## Evidence and output contract
Produce `work-packets.yaml` with packet ID, objective, `workflow_id`, owner, paths, do-not-touch, dependencies, risk, steps, completion criteria, commands, artifacts, and handoff requirements. When the plan explicitly opts into KIT Goal progress, add positive integer `progress_weight`, required evidence kinds, optional or null `estimate_seconds` with low/high seconds, and `timing_policy.max_active_timed_packets: 1`. Existing plans without Goal opt-in remain valid without progress fields.

## Handoff contract
Record packet status, dependency changes, ownership transfers, commands, artifacts, blockers, and the next runnable packet.

## Pitfalls and anti-rationalization
- Do not create packets by role name without path ownership.
- Do not parallelize shared registries, scenes, prefabs, or generators.
- Do not omit integration and verification work.
- Do not treat “independent conceptually” as independent in the filesystem.

## Verification checklist
- [ ] Spec requirements map to packets.
- [ ] Dependencies and blockers are explicit.
- [ ] Concurrent write scopes are disjoint.
- [ ] Every packet has commands and artifacts.
- [ ] Progress-enabled packets have workflow, owner, positive weight, evidence kinds, optional bounded estimates, and single active timing policy.
- [ ] Integration and final review have owners.

## References and scripts
Use repository project maps, `AGENTS.md`, generated-file headers, and installed skill descriptions to resolve boundaries. In a full repository clone, `registry/capabilities.yaml` is an optional maintained index.
