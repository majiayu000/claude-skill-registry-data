---
name: skill-authoring-and-audit
description: Use when creating or revising a GameStudio-CodexKIT skill, resolving ambiguous skill triggers, auditing provenance or lifecycle maturity, or deriving reusable capabilities from session history.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: governance
    lifecycle_stage: operate
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: skill-audit.json
    required_evidence: [catalog-scan, routing-results, provenance-check]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-09-07
    provenance:
      derived_from:
        repo: Dimillian/Skills
        path: project-skill-audit/SKILL.md
        commit: 05ba982bfeb0d77d3c97d4542b0ee15034d05f84
        license: MIT
      patterns_from: [skill-creator concise authoring, docs/authoring/skills.md update-first and provenance rules]
      copied_text: none
---
# Skill Authoring and Audit

## Overview
One governance skill supports two modes: `author` creates or updates a needed workflow; `audit` detects gaps, collisions, stale maturity, and unsupported claims. Update-first is mandatory.

## When to use
Use when a recurring workflow needs codification, a skill trigger is ambiguous, session history reveals repeated failures, or catalog lifecycle and provenance need review.

## When NOT to use
Do not use this skill merely to execute or report an existing evaluation, and do not author a skill for a one-off task, duplicate an existing capability, copy noncommercial content, or promote maturity without eval and dogfood evidence.

## Required inputs and context discovery
Collect requested mode, catalog and registries, existing descriptions, project-local skills and agent roles, routing cases, session or issue evidence, provenance source/license/SHA, owner, reviewer, risk, and target pack.

## Safety and risk level
Writes are limited to owned skill, eval, registry, and documentation paths. Never mutate `.research` sources, external projects, generated adapters, or copied NC content.

## Workflow
1. Scan the catalog and bundled helpers for exact, neighboring, deprecated, reusable, or updateable capabilities.
   Completion criterion: the decision is reuse, update, new skill or tool, backlog, or no action, with existing workflows and tools preferred.
2. In `author` mode, create failing routing, behavior, or pressure cases from observed needs before editing the skill.
   Completion criterion: the gap is reproducible and not a hypothetical preference.
3. Write the smallest complete skill with closed schema, provenance, safety, evidence, workflow criteria, and concise triggers.
   Completion criterion: structural validation passes for the skill.
4. Run deterministic routing, behavior, pressure, originality, and safety checks.
   For a governed Tier-B, behavior, or pressure run, capture `python -B scripts/catalog_audit.py . --input-digest` immediately before invoking the model and store that value as `input_digest` in the runner status. Run the catalog audit afterward so it compares the recorded digest with the then-current inputs.
   Completion criterion: failures are repaired without weakening cases, and accepted runner evidence has one uniquely newest timezone-aware timestamp, is no older than 90 days, and matches current catalog, shipped-skill, evaluator, and eval inputs.
5. In `audit` mode, scan catalog, project overlays, agent-role IDs, and session history for stale skills, repeated manual workflows, trigger or role collisions, missing owners, and observed-versus-target KPI gaps.
   Completion criterion: findings have evidence, owner, severity, and update-first recommendation.
6. Apply lifecycle promotion or demotion only when prerequisites are observed.
   Completion criterion: registry maturity matches evidence rather than aspiration.

## Evidence and output contract
Produce `skill-audit.json` with mode, findings, overlap, routing/behavior/pressure results, provenance, lifecycle recommendation, observed metrics, target metrics, and changed paths.

## Handoff contract
Record requested mode, preflight decision, skill/eval files, provenance source, commands, failures, lifecycle status, and next audit or dogfood action.

## Pitfalls and anti-rationalization
- “A new skill would be cleaner” does not beat updating an existing one.
- “Several items need the same edit” requires a tool assessment, not automatic tool creation or manual per-item repair.
- A small one-off task does not justify a reusable helper without evidence of future value.
- High overlap with undeclared provenance is a Gate 10 failure.
- Target metrics are never observed metrics.
- Missing live dogfood is BLOCKED, not a maturity PASS.
- Never add a current digest to historical runner output after the fact. Missing, stale, future-dated, tied, unreadable, or input-drifted evidence remains `BLOCKED`.

## Verification checklist
- [ ] Update-first preflight was performed.
- [ ] Existing tools were assessed before a new helper was proposed.
- [ ] New behavior had a failing case first.
- [ ] Provenance and license are complete.
- [ ] Routing, behavior, pressure, and safety gates ran.
- [ ] Governed runner status was bound before execution and rechecked afterward; no historical result was retroactively bound.
- [ ] Lifecycle uses observed evidence.

## References and scripts
When maintaining this kit from a full repository clone, use `scripts/validate.py`, `scripts/route_eval.py`, `scripts/check_originality.py`, `scripts/catalog_audit.py`, and the eval directories. Standalone skill installs do not include repository governance tooling.
