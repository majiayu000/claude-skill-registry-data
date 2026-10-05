---
name: u0947-infra-a-b-rollout-governor
description: Build and operate the "Infra A/B Rollout Governor" capability for Infrastructure and Sustainability. Trigger when this exact capability is needed in mission execution.
---

# Infra A/B Rollout Governor

## Why This Skill Exists
We need this skill because long-term scale depends on resilient and sustainable infrastructure choices. This specific skill controls production risk during behavioral changes.

## When To Use
Use this skill when the request explicitly needs "Infra A/B Rollout Governor" outcomes in the Infrastructure and Sustainability domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Infra A/B Rollout Governor`, including at least three measurable KPIs tied to capacity collapse and environmental debt.
2. Design and version the input/output contract for capacity forecasts, energy usage, and sustainability metrics, then add schema validation and failure-mode handling.
3. Implement the core capability using staged rollout policies, and produce safe rollout decisions with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover capacity collapse and environmental debt, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: general-capability using staged rollout policies to produce safe rollout decisions.
- Orchestration integration: infrastructure-and-sustainability:general-capability routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Infra A/B Rollout Governor request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0947_infra-a-b-rollout-governor, approval gates, and rollback owner before autonomous use.

### Execution
- Execute staged rollout policies with deterministic scoring and reproducible trace capture.
- Produce safe rollout decisions plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish safe rollout decisions, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
