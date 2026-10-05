---
name: hypothesis-observation-review
description: Evaluate a hypothesis against prior observations.
---

# hypothesis-observation-review

Goal:

- Evaluate a hypothesis against prior observations.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- optional review guidance from prior review artifacts

Outputs:

- `hypotheses/<id>/REVIEW/OBSERVATION_REVIEW.json`

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Read `hypotheses/<id>/HYPOTHESIS.json`.
- Use the current hypothesis mechanism and predictions as the reference point for comparing against known observations.
- If prior reviews exist, use them only to focus attention on disputed claims.

Execution Prompt Contract:

- System Intent:
  - You are evaluating whether the hypothesis meaningfully explains relevant observations.
- Required Reasoning Focus:
  - Look for observations that are causally relevant to the hypothesis domain.
  - Judge whether the hypothesis explains them, adds nothing, is contradicted by them, or is less plausible than existing explanations.
  - Prefer causal explanatory value over loose topical overlap.
- Do Not Do:
  - Do not list observations that have no material connection to the hypothesis.
  - Do not treat generic correlation as causal support.
  - Do not emit free-form prose instead of structured observation entries.
- Review Quality Floor:
  - A `status = completed` observation review must include concrete observations or retrieval results that are materially connected to the hypothesis mechanism or predicted behavior.
  - Each observation must explain why it supports, weakens, or remains neutral for the hypothesis rather than only naming a topic.
  - Do not use placeholder observation phrases such as `consistent with prior observations`, `needs validation`, or `benchmark against parent` as substantive review content.
- Output Shape:
  - Produce the exact `ObservationReviewContract` from `packages/agent_contracts/review.py`.
  - Each observation entry must contain:
    - `reasoning`
    - `conclusion`
  - Use the allowed conclusion categories only.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/review.py` and confirm the exact `ObservationReviewContract` shape before writing `OBSERVATION_REVIEW.json`.
2. Read the research plan and hypothesis.
3. Identify the most relevant observations for the hypothesis domain.
4. Evaluate whether the hypothesis explains, conflicts with, or adds little to each observation.
5. Write `hypotheses/<id>/REVIEW/OBSERVATION_REVIEW.json`.
6. Validate before declaring completion.

Artifact Rules:

- Limit the review to the strongest and most relevant observations rather than padding the artifact.
- Each observation entry must remain decision-oriented and concise.

Completion Rule:

- This skill is complete only when `OBSERVATION_REVIEW.json` exists and is valid for downstream synthesis.
