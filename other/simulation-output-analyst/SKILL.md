---
name: simulation-output-analyst
description: Interpret DSDS simulation outputs including summary metrics, per-node time series, traces, causal graphs, and invariant breaches. Use when reviewing run results, comparing design alternatives, diagnosing bottlenecks, and proposing mitigation steps.
---

# Simulation Output Analyst

## Overview

Analyze DSDS run outputs to identify bottlenecks, cascade roots, and mitigation priority. Produce evidence-backed findings from summary metrics, time series, traces, and causal artifacts.

## Workflow

1. Verify run context
- Record scenario name, seed, duration, workload shape, and injected faults.
- Confirm comparison baseline before judging regressions.

2. Triage global health
- Check throughput, error rate, and latency percentiles first.
- Flag immediate SLO and invariant violations.

3. Localize bottlenecks
- Rank nodes by utilization, queue depth, rejection rate, and service-time inflation.
- Rank edges by latency growth, packet loss, and concurrency saturation.

4. Reconstruct failure chain
- Use traces and causal graph to determine trigger, first-order impact, and propagation path.
- Distinguish root cause from secondary symptoms (for example retry amplification).

5. Recommend mitigations
- Provide prioritized actions:
- `Now`: stop-the-bleed changes.
- `Next`: structural fixes.
- `Later`: optimization and cost tuning.
- Tie each action to the metric or failure mode it addresses.

6. Produce report
- Include findings by severity, evidence table, confidence level, unknowns, and next scenarios to verify fixes.

## Analysis guardrails

- Do not claim causality without time-ordered evidence.
- Separate observed facts from inference.
- Call out missing telemetry explicitly.

## References

- Read `references/output-analysis-playbook.md` for checklist and report template.
- Use these repo sources:
- `docs/SYSTEM_OVERVIEW.md` (analysis layer expectations)
- `canonical-catalogue/DSDS Canonical Catalogue - Metrics & SLIs.csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Simulation outputs.csv`
- `planning/IMPLEMENTATION_PLAN.md` (Phase 6)
