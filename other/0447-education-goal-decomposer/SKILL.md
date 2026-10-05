---
name: u0447-education-goal-decomposer
description: Build and operate the "Education Goal Decomposer" capability for Education and Upskilling. Trigger when this exact capability is needed in mission execution.
---

# Education Goal Decomposer

## Why This Skill Exists
We need this skill because human capability growth requires targeted planning under constraints. This specific skill breaks ambiguous missions into executable units.

## When To Use
Use this skill when the request explicitly needs "Education Goal Decomposer" outcomes in the Education and Upskilling domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Education Goal Decomposer`, including at least three measurable KPIs tied to persistent skill gaps and poor learning outcomes.
2. Design and version the input/output contract for skill profiles, learning paths, and support resources, then add schema validation and failure-mode handling.
3. Implement the core capability using hierarchical decomposition, and produce atomic task trees with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover persistent skill gaps and poor learning outcomes, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: planning-router using hierarchical decomposition to produce atomic task trees.
- Orchestration integration: education-and-upskilling:planning-router routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Education Goal Decomposer request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0447_education-goal-decomposer, approval gates, and rollback owner before autonomous use.

### Execution
- Execute hierarchical decomposition with deterministic scoring and reproducible trace capture.
- Produce atomic task trees plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish atomic task trees, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
