---
name: hypothesis-evolve-feasibility
description: Generate exactly one child hypothesis that is more experimentally and operationally feasible than its parent.
---

# hypothesis-evolve-feasibility

Goal:

- Generate exactly one child hypothesis that is more experimentally and operationally feasible than its parent.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- selected parent `hypotheses/<id>/HYPOTHESIS.json` artifacts
- parent review artifacts
- active `state/STRATEGY_PLAN.json`

Outputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- `hypotheses/<id>/HYPOTHESIS.md`
- `hypotheses/<id>/ORIGIN.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/hypothesis.py` and confirm the exact `HypothesisContract` shape before writing `hypotheses/<id>/HYPOTHESIS.json`.
- Read `research_plan/RESEARCH_PLAN.json`.
- Read `state/STRATEGY_PLAN.json`.
- Read each selected parent hypothesis and its review bundle.
- Confirm that the round selected `feasibility_evolution`.

Execution Prompt Contract:

- System Intent:
  - You are making the hypothesis more implementable with available methods, reagents, instrumentation, and timelines.
- Required Reasoning Focus:
  - Reduce experimental fragility.
  - Replace unrealistic requirements with practical alternatives.
  - Keep the core mechanism testable.
- Do Not Do:
  - Do not strip the hypothesis into a trivial claim.
  - Do not output implementation notes without a full child hypothesis artifact.
- Quality Floor:
  - The child must directly address at least one specific weakness from the parent review bundle.
  - `origin.content.statement` must name concrete materials, catalysts, reaction conditions, mechanistic variables, or experimental targets from the parent and research goal.
  - `origin.content.mechanism` must explain a causal chain; do not write only generic phrases such as `improved mechanism`, `targeted improvement`, or `review-identified weaknesses`.
  - `origin.content.experimental_design` must include 3-6 numbered steps with measurable readouts, controls, or decision thresholds.
  - Do not use generic refinement placeholder steps such as `Apply targeted improvement`, `Characterize with standard techniques`, `Benchmark against parent`, or `Validate improvement quantitatively`.
  - If the research plan, parent hypothesis, or parent review bundle is missing, stop and report the missing artifact instead of guessing.
- Output Shape:
  - Emit the canonical `HypothesisContract`.
  - `origin.strategy`: `feasibility_evolution`
  - Keep `experimental_design` concrete and operational.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Identify feasibility risks in the parent set.
3. Produce exactly one more implementable child hypothesis.
4. Persist canonical `HYPOTHESIS.json`, `HYPOTHESIS.md`, and `ORIGIN.json`.
5. Validate the emitted hypothesis artifact.

Completion Rule:

- This skill is complete only when one feasibility-improved child hypothesis has been written in canonical form.
