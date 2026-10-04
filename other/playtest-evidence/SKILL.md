---
name: playtest-evidence
description: Use when planning or reviewing game playtests that need structured scenarios, participant context, observations, reproduction evidence, severity, and honest separation of observed findings from conclusions.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, macos, linux, console, mobile]
metadata:
  studio:
    type: workflow
    lifecycle_stage: verify
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: playtest-evidence.json
    required_evidence: [test-scenario, participant-context, observations, limitations]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, evidence-first-debugging]
      copied_text: none
---
# Playtest Evidence

## Overview
Convert playtest notes into traceable evidence without turning opinions, memories, or small samples into invented metrics.

## When to use
Use for usability sessions, mechanic validation, onboarding tests, combat feel reviews, retention hypotheses, and regression playtests.

## When NOT to use
Do not use as a substitute for automated correctness tests, production analytics, or statistically representative research.

## Required inputs and context discovery
Collect build identity, feature hypothesis, participant context, scenario, environment, session method, consent constraints, observation timestamps, issue reproduction, and protected personal data rules.

## Safety and risk level
Read-only evidence synthesis. Remove personal data, do not record participants without consent, and label missing builds, recordings, or reproduction artifacts as `BLOCKED` or `Unverified`.

## Workflow
1. Bind the session to an exact build, feature hypothesis, and scenario.
   Completion criterion: the tested state and intended question are explicit.
2. Separate direct observation, participant quote, facilitator interpretation, and proposed fix.
   Completion criterion: every finding has one evidence class and source reference.
3. Normalize issues by reproduction, severity, frequency within the observed sample, and affected experience.
   Completion criterion: no issue uses unsupported population-level claims.
4. Compare results with the playtest criteria from the feature specification.
   Completion criterion: each criterion is Verified, Unverified, FAIL, or BLOCKED with a reason.
5. Produce follow-up experiments and regression checks.
   Completion criterion: each next step has an owner, artifact, and stopping condition.

## Evidence and output contract
Produce `playtest-evidence.json` with build identity, scenarios, participant context, observations, issues, criteria verdicts, limitations, and follow-up experiments.

## Handoff contract
Record session artifacts, privacy redactions, reproduced issues, unresolved disagreements, test gaps, next owners, and the build required for follow-up.

## Pitfalls and anti-rationalization
- A participant opinion is not an observed behavior metric.
- A small sample cannot justify a population percentage.
- Facilitator interpretation must not be rewritten as a participant quote.
- Missing recordings or builds remain explicit limitations.

## Verification checklist
- [ ] Build and scenario identities are recorded.
- [ ] Observations and interpretations are separate.
- [ ] Severity and frequency refer only to observed sessions.
- [ ] Privacy-sensitive data is removed.
- [ ] Conclusions cite evidence and limitations.

## References and scripts
Use the feature specification and project playtest artifacts. No live session runner is bundled; unavailable recordings or builds remain `BLOCKED`.
