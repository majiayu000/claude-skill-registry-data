---
name: hypothesis-simulation-review
description: Simulate the hypothesis mechanism and identify failure scenarios.
---

# hypothesis-simulation-review

Goal:

- Simulate the hypothesis mechanism and identify failure scenarios.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- optional prior review artifacts for calibration

Outputs:

- `hypotheses/<id>/REVIEW/SIMULATION_REVIEW.json`

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Read `hypotheses/<id>/HYPOTHESIS.json`.
- Use prior reviews only as hints for likely weak spots; the simulation should still be an independent walk-through of the mechanism and validation path.

Execution Prompt Contract:

- System Intent:
  - You are mentally simulating the hypothesis mechanism and proposed validation path step by step.
- Required Reasoning Focus:
  - Break the mechanism into an ordered process.
  - Identify where the process could fail and why.
  - Distinguish inherent failures from contingent implementation issues where possible.
  - Prioritize likely and fundamental failure scenarios over edge cases.
- Do Not Do:
  - Do not generate abstract critique without a concrete simulated step.
  - Do not flood the artifact with low-value edge cases.
  - Do not replace the structured review with narrative prose.
- Review Quality Floor:
  - A `status = completed` simulation review must include concrete mechanism or validation steps and concrete failure scenarios.
  - Steps must name hypothesis-specific materials, mechanisms, measurements, conditions, controls, or decision points.
  - Do not use placeholder simulation steps such as `Synthesize evolved catalyst`, `Characterize structure`, `Test activity`, or `Benchmark against parent` as substantive review content.
- Output Shape:
  - Produce the exact `SimulationReviewContract` from `packages/agent_contracts/review.py` with:
    - `steps`
    - `failure_scenarios`
  - Keep each step and failure scenario concise and concrete.
  - Each item in `steps` must be a plain string, not an object with nested keys such as `step`, `description`, or `expected_outcome`.
  - Each item in `failure_scenarios` must be a plain string, not an object with nested keys such as `scenario`, `likelihood`, or `mitigation`.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/review.py` and confirm the exact `SimulationReviewContract` shape before writing `SIMULATION_REVIEW.json`.
2. Read the research plan and hypothesis.
3. Simulate the key mechanism or validation path step by step.
4. Record the major steps.
5. Identify likely and fundamental failure scenarios.
6. Write `hypotheses/<id>/REVIEW/SIMULATION_REVIEW.json`.
7. Validate before declaring completion.

Artifact Rules:

- `SIMULATION_REVIEW.json` should focus on the highest-signal failure modes.
- The artifact should remain short enough for downstream summarization but concrete enough to guide revision.

Completion Rule:

- This skill is complete only when `SIMULATION_REVIEW.json` exists and is valid for downstream synthesis.
