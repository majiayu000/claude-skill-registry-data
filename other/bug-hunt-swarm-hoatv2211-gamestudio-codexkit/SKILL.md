---
name: bug-hunt-swarm
description: Use when an unknown crash, intermittent failure, or cross-subsystem bug needs parallel read-only reproduction lanes, ranked hypotheses, suspect paths, and an integrator root-cause plan.
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
    lifecycle_stage: verify
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: bug-packets.json
    required_evidence: [reproduction, ranked-hypotheses, suspect-paths]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from:
        repo: Dimillian/Skills
        path: bug-hunt-swarm/SKILL.md
        commit: 05ba982bfeb0d77d3c97d4542b0ee15034d05f84
        license: MIT
      patterns_from: [evidence-first-debugging hypothesis ranking]
      copied_text: none
---
# Bug Hunt Swarm

## Overview
Explore an unknown failure through independent read-only hypotheses, then converge on the smallest discriminating reproduction or instrumentation plan.

## When to use
Use for intermittent crashes, unclear subsystem ownership, multi-service failures, race conditions, protocol mismatches, or symptoms with several plausible root causes.

## When NOT to use
Do not use for reviewing an already known patch, implementing fixes, or parallel lanes that would need to mutate the same environment.

## Required inputs and context discovery
Collect symptom, expected behavior, frequency, environment, timeline, known-good snapshot, logs, subsystem map, active processes, safe read-only commands, and integrator owner.

## Safety and risk level
Lanes are read-only. They may propose instrumentation but cannot patch files, start or stop services, change databases, or modify shared fixtures.

## Workflow
1. Freeze one symptom statement and shared evidence packet.
   Completion criterion: all lanes investigate the same observable failure.
2. Assign disjoint hypotheses such as data, timing, config, protocol, rendering, or environment.
   Completion criterion: each lane has a falsifiable question and suspect paths.
3. Run independent read-only inspection and reproduction attempts.
   Completion criterion: each lane returns evidence, counterevidence, and confidence.
4. Rank hypotheses by explanatory power and cost of the next experiment.
   Completion criterion: the integrator selects one discriminating action.
5. Hand the selected action to `evidence-first-debugging` for mutation or instrumentation.
   Completion criterion: the swarm ends before any lane writes files.

## Evidence and output contract
Produce bug packets containing hypothesis, evidence, counterevidence, reproduction status, suspect paths, proposed experiment, confidence, and integrator rank.

## Handoff contract
Record symptom, shared snapshot, lanes, commands, ranked hypotheses, unresolved evidence, and the next single experiment with its owner.

## Pitfalls and anti-rationalization
- Lanes may not patch “obvious” suspects.
- Multiple opinions without falsifiable experiments are not evidence.
- Intermittent reproduction remains Unverified or BLOCKED.
- Do not let every lane inspect the same logs with the same hypothesis.

## Verification checklist
- [ ] Symptom and snapshot are shared.
- [ ] Lanes are disjoint and read-only.
- [ ] Hypotheses are ranked with counterevidence.
- [ ] A single next experiment is selected.
- [ ] No lane mutated the repository or environment.

## References and scripts
Pair the output with `evidence-first-debugging`. Use project logs and process/port inspection only when those commands are read-only.
