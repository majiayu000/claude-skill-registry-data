---
name: hypothesis-initial-review
description: Run the initial review gate for a hypothesis.
---

# hypothesis-initial-review

Goal:

- Run the initial review gate for a hypothesis.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- optional `meta/INSIGHTS_FROM_REVIEWS.json` or other run-level review guidance when available

Outputs:

- `hypotheses/<id>/REVIEW/INITIAL_REVIEW.json`

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Treat `research_goal` as the target problem.
- Treat `preferences` as the main evaluation axes.
- Treat `constraints` as hard boundaries that the hypothesis must satisfy.
- Read `hypotheses/<id>/HYPOTHESIS.json`.
- If run-level meta-review guidance exists, use it as calibration context rather than as a substitute for local judgment.

Execution Prompt Contract:

- System Intent:
  - You are the rapid initial review gate for one hypothesis.
- Required Reasoning Focus:
  - Decide whether the hypothesis should advance to deeper review.
  - Judge it against the explicit preference axes and constraints.
  - Distinguish between fundamental flaws and refinable weaknesses.
  - Borderline but refinable hypotheses should usually pass.
- Do Not Do:
  - Do not perform a full literature-grounded review here.
  - Do not fail a hypothesis for minor polish issues alone.
  - Do not emit unstructured commentary in place of the review artifact.
- Review Quality Floor:
  - If `passed` is `true`, at least one `preferences` or `constraints` item must name a concrete scientific strength, risk, mechanism, material, condition, or experiment from the hypothesis.
  - Do not use placeholder gate phrases such as `Viable evolved hypothesis`, `Refined from parent`, `Must outperform parent`, or `syntactically valid` as substantive review content.
  - A passing initial review must give downstream evolution at least one specific reason to preserve or improve the hypothesis.
- Output Shape:
  - Produce the exact `InitialReviewContract` from `packages/agent_contracts/review.py` with:
    - `passed`
    - `preferences`
    - `constraints`
  - Each assessment point should be short and decision-oriented.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/review.py` and confirm the exact `InitialReviewContract` shape before writing `INITIAL_REVIEW.json`.
2. Read the research plan and current hypothesis.
3. Review the hypothesis against each preference axis.
4. Review the hypothesis against each constraint.
5. Make a pass/fail decision.
6. Write `hypotheses/<id>/REVIEW/INITIAL_REVIEW.json`.
7. Validate before declaring completion.

Artifact Rules:

- `INITIAL_REVIEW.json` must be a structured artifact, not a free-form memo.
- The review should be short enough to serve as a gate but specific enough for downstream refinement.

Completion Rule:

- This skill is complete only when `INITIAL_REVIEW.json` exists and is valid for downstream review routing.
