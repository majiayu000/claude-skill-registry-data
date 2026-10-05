---
name: hypothesis-evolve-inspiration
description: Generate exactly one cross-parent child hypothesis by transferring a useful principle from one parent context into another.
---

# hypothesis-evolve-inspiration

Goal:

- Generate exactly one cross-parent child hypothesis by transferring a useful principle from one parent context into another.

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
- Confirm that the round selected `inspiration_evolution`.

Execution Prompt Contract:

- System Intent:
  - You are producing one novel child hypothesis by transferring a principle from one parent into another domain or mechanism context.
- Required Reasoning Focus:
  - Name the borrowed principle.
  - Keep the analogical leap explicit and testable.
  - Produce a child that is genuinely new, not just a stitched paraphrase.
- Do Not Do:
  - Do not copy one parent with cosmetic changes.
  - Do not emit more than one child.
- Quality Floor:
  - The child must directly address at least one specific weakness from the parent review bundle.
  - `origin.content.statement` must name concrete materials, catalysts, reaction conditions, mechanistic variables, or experimental targets from the parent and research goal.
  - `origin.content.mechanism` must explain a causal chain; do not write only generic phrases such as `improved mechanism`, `targeted improvement`, or `review-identified weaknesses`.
  - `origin.content.experimental_design` must include 3-6 numbered steps with measurable readouts, controls, or decision thresholds.
  - Do not use generic refinement placeholder steps such as `Apply targeted improvement`, `Characterize with standard techniques`, `Benchmark against parent`, or `Validate improvement quantitatively`.
  - If the research plan, parent hypothesis, or parent review bundle is missing, stop and report the missing artifact instead of guessing.
- Output Shape:
  - Emit the canonical `HypothesisContract`.
  - `origin.strategy`: `inspiration_evolution`
  - Keep `summary` and `category` specific to the new cross-parent insight.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Identify the transferable principle across the parent set.
3. Produce exactly one inspired child hypothesis.
4. Persist canonical `HYPOTHESIS.json`, `HYPOTHESIS.md`, and `ORIGIN.json`.
5. Validate the emitted hypothesis artifact.

Completion Rule:

- This skill is complete only when one inspired cross-parent child hypothesis has been written in canonical form.
