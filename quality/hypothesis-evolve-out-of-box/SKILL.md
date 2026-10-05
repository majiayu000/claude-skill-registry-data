---
name: hypothesis-evolve-out-of-box
description: Generate exactly one divergent but still testable child hypothesis that challenges the shared assumptions of the parent set.
---

# hypothesis-evolve-out-of-box

Goal:

- Generate exactly one divergent but still testable child hypothesis that challenges the shared assumptions of the parent set.

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
- Confirm that the round selected `out_of_box_evolution`.

Execution Prompt Contract:

- System Intent:
  - You are deliberately leaving the parents' default reasoning path while staying scientifically grounded and testable.
- Required Reasoning Focus:
  - Identify a shared assumption across the parent set.
  - Challenge that assumption with a concrete alternative mechanism.
  - Keep the child falsifiable and experimentally actionable.
- Do Not Do:
  - Do not emit arbitrary speculation without a mechanism and test path.
  - Do not produce a child that is just a noisier parent variant.
- Quality Floor:
  - The child must directly address at least one specific weakness from the parent review bundle.
  - `origin.content.statement` must name concrete materials, catalysts, reaction conditions, mechanistic variables, or experimental targets from the parent and research goal.
  - `origin.content.mechanism` must explain a causal chain; do not write only generic phrases such as `improved mechanism`, `targeted improvement`, or `review-identified weaknesses`.
  - `origin.content.experimental_design` must include 3-6 numbered steps with measurable readouts, controls, or decision thresholds.
  - Do not use generic refinement placeholder steps such as `Apply targeted improvement`, `Characterize with standard techniques`, `Benchmark against parent`, or `Validate improvement quantitatively`.
  - If the research plan, parent hypothesis, or parent review bundle is missing, stop and report the missing artifact instead of guessing.
- Output Shape:
  - Emit the canonical `HypothesisContract`.
  - `origin.strategy`: `out_of_box_evolution`
  - Keep `summary` explicit about the divergent mechanism.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Identify the shared parent assumption that should be challenged.
3. Produce exactly one divergent but testable child hypothesis.
4. Persist canonical `HYPOTHESIS.json`, `HYPOTHESIS.md`, and `ORIGIN.json`.
5. Validate the emitted hypothesis artifact.

Completion Rule:

- This skill is complete only when one divergent child hypothesis has been written in canonical form.
