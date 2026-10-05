---
name: hypothesis-evolve-combination
description: Generate exactly one child hypothesis by combining complementary strengths from multiple parent hypotheses.
---

# hypothesis-evolve-combination

Goal:

- Generate exactly one child hypothesis by combining complementary strengths from multiple parent hypotheses.

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
- Read the selected parent hypotheses and their review bundles.
- Confirm that the round selected `combination_evolution`.

Execution Prompt Contract:

- System Intent:
  - You are synthesizing one stronger child hypothesis from the complementary strengths of multiple parents.
- Required Reasoning Focus:
  - Preserve the strongest pieces from each parent.
  - Resolve contradictions instead of ignoring them.
  - The child must be stronger than any single parent on at least two meaningful dimensions.
- Do Not Do:
  - Do not concatenate parent text.
  - Do not leave contradictions unresolved.
- Quality Floor:
  - The child must directly address at least one specific weakness from the parent review bundle.
  - `origin.content.statement` must name concrete materials, catalysts, reaction conditions, mechanistic variables, or experimental targets from the parent and research goal.
  - `origin.content.mechanism` must explain a causal chain; do not write only generic phrases such as `improved mechanism`, `targeted improvement`, or `review-identified weaknesses`.
  - `origin.content.experimental_design` must include 3-6 numbered steps with measurable readouts, controls, or decision thresholds.
  - Do not use generic refinement placeholder steps such as `Apply targeted improvement`, `Characterize with standard techniques`, `Benchmark against parent`, or `Validate improvement quantitatively`.
  - If the research plan, parent hypothesis, or parent review bundle is missing, stop and report the missing artifact instead of guessing.
- Output Shape:
  - Emit the canonical `HypothesisContract`.
  - `origin.strategy`: `combination_evolution`
  - Keep the statement, mechanism, and experimental design unified rather than parent-segmented.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Identify the complementary strengths and contradictions across the parent set.
3. Produce exactly one combined child hypothesis.
4. Persist canonical `HYPOTHESIS.json`, `HYPOTHESIS.md`, and `ORIGIN.json`.
5. Validate the emitted hypothesis artifact.

Completion Rule:

- This skill is complete only when one combined child hypothesis has been written in canonical form.
