---
name: chaos-experiment-designer
description: Design DSDS chaos experiments with deterministic setup, explicit hypotheses, and measurable outcomes. Use when planning failure drills, resilience validation, pre-production risk exercises, and repeatable chaos scenarios for regression testing.
---

# Chaos Experiment Designer

## Overview
Create focused chaos experiments that test one resilience claim at a time. Ensure each experiment is reproducible and has clear pass/fail criteria.

## Workflow

1. Define the hypothesis
- State one reliability claim in measurable form.
- Identify target metrics and acceptable bounds.

2. Define steady state
- Specify baseline workload and expected healthy metric band.
- Establish pre-fault observation window.

3. Design fault injection
- Pick minimal fault set to test the hypothesis.
- Set trigger timing and fault duration explicitly.

4. Define safeguards
- Add blast radius limits and abort conditions.
- Identify critical user journeys that must stay protected.

5. Define evaluation plan
- Add pass/fail rules tied to SLOs and invariants.
- Include recovery expectations (`MTTR`, error decay, queue normalization).

6. Package experiment
- Return experiment spec, run steps, success criteria, and follow-up checks.

## Output format
1. `Hypothesis`
2. `Steady-state definition`
3. `Fault plan`
4. `Safety and abort rules`
5. `Pass/fail criteria`
6. `Follow-up actions`

## References
- Read `references/chaos-experiment-template.md` for reusable experiment skeletons.
- Use these repo sources:
- `docs/05-devs-chaos-and-analysis.md` (Chapter 27)
- `canonical-catalogue/DSDS Canonical Catalogue - scenarios to ship.csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Failure modes & propagation semantics.csv`
