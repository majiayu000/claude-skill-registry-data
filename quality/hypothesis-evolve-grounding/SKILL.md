---
name: hypothesis-evolve-grounding
description: Generate exactly one grounded child hypothesis by strengthening evidence, specificity, and literature support.
---

# hypothesis-evolve-grounding

Goal:

- Generate exactly one grounded child hypothesis by strengthening evidence, specificity, and literature support.

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
- Confirm that the round selected `grounding_evolution`.

Execution Prompt Contract:

- System Intent:
  - You are refining the parent hypothesis by replacing weakly supported claims with better-grounded, more specific, and more internally consistent ones.
- Required Reasoning Focus:
  - Preserve the strongest core insight from the parent.
  - Use review findings to identify unsupported leaps, vague mechanisms, or weak evidence.
  - Strengthen the mechanism and experiment path without bloating the claim.
- Do Not Do:
  - Do not merely paraphrase the parent.
  - Do not emit multiple children.
  - Do not drop the parent linkage.
- Quality Floor:
  - The child must directly address at least one specific weakness from the parent review bundle.
  - `origin.content.statement` must name concrete materials, catalysts, reaction conditions, mechanistic variables, or experimental targets from the parent and research goal.
  - `origin.content.mechanism` must explain a causal chain; do not write only generic phrases such as `improved mechanism`, `targeted improvement`, or `review-identified weaknesses`.
  - `origin.content.experimental_design` must include 3-6 numbered steps with measurable readouts, controls, or decision thresholds.
  - Do not use generic refinement placeholder steps such as `Apply targeted improvement`, `Characterize with standard techniques`, `Benchmark against parent`, or `Validate improvement quantitatively`.
  - If the research plan, parent hypothesis, or parent review bundle is missing, stop and report the missing artifact instead of guessing.
- Output Shape:
  - Emit the canonical `HypothesisContract`.
  - `origin.strategy`: `grounding_evolution`
  - `origin.content.statement`: 2-3 sentences.
  - `origin.content.mechanism`: 2-3 sentences.
  - `origin.content.experimental_design`: one concise multiline string with 3-6 numbered steps.
  - `origin.content.experimental_design` must remain one string field containing embedded line breaks; do not emit it as a list, array, or nested object.
  - `origin.content.summary`: one sentence.
  - `origin.content.category`: 1-5 words.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/hypothesis.py` before writing `hypotheses/<id>/HYPOTHESIS.json`.
2. Identify the parent weaknesses that must be corrected by grounding.
3. Produce exactly one improved child hypothesis.
4. Persist canonical `HYPOTHESIS.json`, `HYPOTHESIS.md`, and `ORIGIN.json`.
5. Validate the emitted hypothesis artifact.

Completion Rule:

- This skill is complete only when one valid grounded child hypothesis has been written in canonical form.
