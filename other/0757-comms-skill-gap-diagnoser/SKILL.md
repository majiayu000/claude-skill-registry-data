---
name: u0757-comms-skill-gap-diagnoser
description: Build and operate the "Comms Skill Gap Diagnoser" capability for Communication and Explainability. Trigger when this exact capability is needed in mission execution.
---

# Comms Skill Gap Diagnoser

## Why This Skill Exists
We need this skill because complex systems require explanations humans can act on quickly. This specific skill identifies where agents and humans need capability upgrades.

## When To Use
Use this skill when the request explicitly needs "Comms Skill Gap Diagnoser" outcomes in the Communication and Explainability domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Comms Skill Gap Diagnoser`, including at least three measurable KPIs tied to misinterpretation and trust erosion.
2. Design and version the input/output contract for decision factors, uncertainty markers, and audience summaries, then add schema validation and failure-mode handling.
3. Implement the core capability using competency coverage analysis, and produce skill gap reports with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover misinterpretation and trust erosion, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: general-capability using competency coverage analysis to produce skill gap reports.
- Orchestration integration: communication-and-explainability:general-capability routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Comms Skill Gap Diagnoser request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0757_comms-skill-gap-diagnoser, approval gates, and rollback owner before autonomous use.

### Execution
- Execute competency coverage analysis with deterministic scoring and reproducible trace capture.
- Produce skill gap reports plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish skill gap reports, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
