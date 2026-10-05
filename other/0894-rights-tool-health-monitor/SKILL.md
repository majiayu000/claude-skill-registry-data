---
name: u0894-rights-tool-health-monitor
description: Build and operate the "Rights Tool Health Monitor" capability for Legal, Rights, and Compliance. Trigger when this exact capability is needed in mission execution.
---

# Rights Tool Health Monitor

## Why This Skill Exists
We need this skill because operations must preserve rights and satisfy jurisdictional obligations. This specific skill detects tool flakiness before it impacts mission outcomes.

## When To Use
Use this skill when the request explicitly needs "Rights Tool Health Monitor" outcomes in the Legal, Rights, and Compliance domain.

## Step-by-Step Implementation Guide
1. Define the scope and success metrics for `Rights Tool Health Monitor`, including at least three measurable KPIs tied to rights violations and compliance penalties.
2. Design and version the input/output contract for requirements mappings, legal decisions, and evidence trails, then add schema validation and failure-mode handling.
3. Implement the core capability using telemetry aggregation and SLO checks, and produce tool reliability scores with deterministic scoring.
4. Integrate the skill into swarm orchestration: task routing, approval gates, retry strategy, and rollback controls.
5. Add unit, integration, and simulation tests that explicitly cover rights violations and compliance penalties, then run regression baselines.
6. Deploy behind a feature flag, monitor telemetry/alerts for two release cycles, and iterate thresholds based on observed outcomes.

## Required Deliverables
- Capability contract: input schema, deterministic scoring, output schema, and failure modes.
- Runtime profile: detection-guard using telemetry aggregation and SLO checks to produce tool reliability scores.
- Orchestration integration: legal-rights-and-compliance:detection-guard routing, approval gates, retries, and rollback controls.
- Validation evidence: unit, integration, simulation, regression-baseline suites and rollout telemetry.

## Operational Runbook
### Preflight
- Confirm the Rights Tool Health Monitor request scope, source evidence, and measurable success criteria before execution.
- Verify feature flag skill_0894_rights-tool-health-monitor, approval gates, and rollback owner before autonomous use.

### Execution
- Execute telemetry aggregation and SLO checks with deterministic scoring and reproducible trace capture.
- Produce tool reliability scores plus scorecard, assumptions, and unresolved-risk notes.

### Recovery
- Fail closed when required signals, evidence, or approval gates are missing.
- Rollback to the last stable baseline when posture is critical or validation fails.

### Handoff
- Publish tool reliability scores, validation evidence, and telemetry links to downstream owners.
- Queue follow-up tasks for unresolved risks, threshold tuning, or approval review.

## Guardrails
- [quality] Require deterministic scoring and validation evidence before promotion.
- [reliability] Preserve retries, rollback controls, and failure-mode evidence for every run.
- [safety] Route critical posture or missing approval gates to human review before autonomous action.
