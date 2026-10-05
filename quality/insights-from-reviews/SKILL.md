---
name: insights-from-reviews
description: Extract recurring critique patterns from the completed review of a hypothesis.
---

# insights-from-reviews

Goal:

- Extract recurring critique patterns from the completed review of a hypothesis.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- `hypotheses/<id>/HYPOTHESIS.json`
- existing `meta/INSIGHTS_FROM_REVIEWS.json` when present

Outputs:

- `meta/INSIGHTS_FROM_REVIEWS.json`
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/meta_review.py` before writing `meta/INSIGHTS_FROM_REVIEWS.json`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Read `research_plan/RESEARCH_PLAN.json` for the active goal and evaluation boundaries.
- Read the current hypothesis together with its completed review stack.
- If `meta/INSIGHTS_FROM_REVIEWS.json` already exists, treat it as the current accumulated insight set that must be revised rather than appended to blindly.

Execution Prompt Contract:

- System Intent:
  - You are the run-level critique-pattern aggregator.
- Required Reasoning Focus:
  - Compare the current hypothesis review against existing accumulated insights.
  - Keep, strengthen, refine, merge, split, or remove insight statements based on the new evidence.
  - Maintain a complete self-contained insight list rather than incremental append-only notes.
  - Prefer concise, actionable critique patterns over vague thematic summaries.
- Do Not Do:
  - Do not output only the delta from the previous insight set.
  - Do not preserve unsupported or redundant insights just because they already exist.
  - Do not turn one hypothesis review into a run-level generalization without enough evidence.
- Output Shape:
  - Produce the exact `InsightsFromReviewsContract` from `packages/agent_contracts/meta_review.py`.
  - When consumed inside the run pipeline, use `from tools import sync_pipeline_stage_artifacts` so `currentPhase = Insights from Reviews`, `currentSkill = insights-from-reviews`, and `stageTrail` stay aligned across both state artifacts.
  - Keep each insight short and actionable.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/meta_review.py` and `packages/agent_contracts/pipeline_runtime.py` before writing `meta/INSIGHTS_FROM_REVIEWS.json` or updating run-level stage artifacts.
2. Before aggregating the new insight set, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Insights from Reviews", current_skill="insights-from-reviews")`.
3. Read the research plan, current hypothesis, and its completed review artifacts.
4. Read prior insights if they exist.
5. Compare the new review evidence against the prior insight set.
6. Produce a revised complete insight list.
7. Write `meta/INSIGHTS_FROM_REVIEWS.json`.
8. Validate before declaring completion.

Artifact Rules:

- `INSIGHTS_FROM_REVIEWS.json` must contain a complete revised insight set, not an append-only patch.
- The artifact should stay concise enough to guide later stages without becoming a second full review archive.

Completion Rule:

- This skill is complete only when `meta/INSIGHTS_FROM_REVIEWS.json` exists and is valid for downstream consumption.
