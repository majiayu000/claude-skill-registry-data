---
name: failure-propagation-analyzer
description: Analyze likely cascade paths and propagation semantics in DSDS architectures. Use when estimating blast radius, diagnosing multi-hop degradation, validating containment strategies, or explaining how a localized failure can become systemic.
---

# Failure Propagation Analyzer

## Overview
Model how failures spread through dependencies and identify where containment should happen. Produce an explicit trigger-to-impact chain with mitigation points.

## Workflow

1. Build dependency view
- Identify upstream/downstream relationships and critical dependencies.
- Mark optional fallbacks and graceful degradation paths.

2. Define trigger failure
- Choose initiating failure type and target component.
- Record timing and intensity assumptions.

3. Apply propagation semantics
- Evaluate timeouts, retries, queue growth, resource exhaustion, and split-brain risks.
- Track each hop with expected delay and effect.

4. Estimate blast radius
- Identify directly affected components, second-order impacts, and user-facing outcomes.
- Distinguish local degradation from system-wide risk.

5. Propose containment
- Recommend controls: bulkheads, breakers, timeouts, backpressure, and load shedding.
- Prioritize controls by impact reduction and implementation effort.

## Output format
1. `Trigger definition`
2. `Propagation chain`
3. `Blast radius summary`
4. `Containment recommendations`
5. `Confidence and assumptions`

## References
- Read `references/propagation-modeling-checklist.md` for analysis checklist.
- Use these repo sources:
- `canonical-catalogue/DSDS Canonical Catalogue - Failure modes & propagation semantics.csv`
- `docs/04-distributed-systems-and-failures.md` (Chapters 22-24)
- `planning/IMPLEMENTATION_PLAN.md` (Phase 4)
