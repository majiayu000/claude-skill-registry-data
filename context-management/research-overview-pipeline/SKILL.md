---
name: research-overview-pipeline
description: Generate the final research overview from the top-ranked hypotheses.
---

# research-overview-pipeline

Goal:

- Generate the final research overview from the top-ranked hypotheses.

Inputs:

- `research_plan/RESEARCH_PLAN.json`
- top-ranked `hypotheses/<id>/HYPOTHESIS.json` artifacts with completed review payloads
- optional `meta/INSIGHTS_FROM_REVIEWS.json`

Outputs:

- `meta/RESEARCH_OVERVIEW.json`
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Context Loading:

- Read `research_plan/RESEARCH_PLAN.json`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Read `state/EVOLUTION_STATE.json` before writing the overview.
- Read `literature/queries/*/EVIDENCE_BUNDLE.json` when literature artifacts exist and record whether any `retrieval_metadata.status` is `partial` or `blocked`.
- Read `state/PROXIMITY_STATUS.json` when it exists and record whether proximity was `succeeded` or degraded to a skipped/failed fallback state.
- Use `research_goal` as the synthesis anchor.
- Use `preferences` and `constraints` to frame which research directions are worth elevating.
- Read the current top-ranked hypothesis artifacts together with their embedded or adjacent review results.
- If `meta/INSIGHTS_FROM_REVIEWS.json` exists, use it to highlight recurring critique patterns and unresolved risks across the run.

Execution Prompt Contract:

- System Intent:
  - You are synthesizing the strongest current hypotheses into a final research overview.
- Required Reasoning Focus:
  - Group the strongest candidates into 3-5 coherent research directions or areas where possible.
  - Explain why each direction matters relative to the research goal.
  - Suggest concrete experiments or next steps for each direction.
  - Use review evidence and recurring critique patterns to keep the overview realistic rather than promotional.
  - Explain the actual run stop state from `state/EVOLUTION_STATE.json`.
  - When any evidence bundle is `partial` or `blocked`, include a concise literature retrieval limitation note; do not describe the run as having comprehensive literature coverage in that case.
  - When `PROXIMITY_STATUS.json` records a skipped or failed fallback, include a concise proximity embedding fallback limitation note; do not describe ranking as embedding-, proximity-, or similarity-informed in that case.
- Do Not Do:
  - Do not simply concatenate ranked hypotheses.
  - Do not ignore major recurring weaknesses surfaced by review.
  - Do not produce a vague essay without clear actionable research directions.
  - Do not claim that the frontier converged unless `EVOLUTION_STATE.stopReason` is exactly `convergence_reached`.
  - Do not describe a safety stop, capped stop, or paused state as scientific convergence.
  - Do not call partial or blocked literature retrieval comprehensive, complete, exhaustive, or full literature coverage.
  - Do not call receipt-gated manual placement embedding-informed, proximity-informed, or similarity-driven ranking.
  - Do not omit degraded literature or proximity bridge limitations from a completed overview.
- Output Shape:
  - Produce the exact `ResearchOverviewContract` from `packages/agent_contracts/meta_review.py`.
  - When updating `state/PIPELINE_STATE.json`, preserve the exact `PipelineStateContract` from `packages/agent_contracts/pipeline_runtime.py`.
  - When this synthesis step starts, use `from tools import sync_pipeline_stage_artifacts` so `currentPhase = Research Overview`, `currentSkill = research-overview-pipeline`, and `stageTrail` stay aligned across both state artifacts.
  - Use `##` sections for major directions and `###` subsections where helpful.
  - Keep the overview concise and decision-oriented.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/meta_review.py` and `packages/agent_contracts/pipeline_runtime.py` before writing `meta/RESEARCH_OVERVIEW.json` or updating run-level stage artifacts.
2. Before synthesizing the overview, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Research Overview", current_skill="research-overview-pipeline")`.
3. Read `state/EVOLUTION_STATE.json` and record whether the stop reason is `convergence_reached`, `max_iterations_reached`, `safety_iteration_limit_reached`, `no_viable_candidates`, or still empty.
4. Read the research plan and current top-ranked hypothesis artifacts.
5. Read run-level literature bundle statuses and proximity status when those artifacts exist.
6. Read run-level critique insights if they exist.
7. Group the strongest hypotheses into coherent directions.
8. Write one synthesized overview that explains importance, evidence, next experiments, and the real stop state. Use convergence language only for `stopReason=convergence_reached`; for safety stops use language such as "synthesis after the safety ceiling" rather than "frontier converged". When literature or proximity is degraded, include the limitation in plain language without overstating the pipeline evidence.
   - If literature retrieval is `partial` or `blocked`, state that external evidence coverage was partial, limited, blocked, or otherwise incomplete.
   - If proximity embedding is skipped or failed, state that proximity embedding was unavailable/skipped and ranking continued through documented fallback rather than true embedding/proximity-informed placement.
9. Write `meta/RESEARCH_OVERVIEW.json`.
10. Update `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` as required by the top-level workflow.
11. Validate the run artifacts before declaring completion.

Artifact Rules:

- `RESEARCH_OVERVIEW.json` is the canonical machine-consumable overview artifact.
- The overview should synthesize rather than repeat the underlying hypotheses.
- Any pipeline-state update must remain consistent with the completion and state contracts.
- Overview evidence claims must remain consistent with literature retrieval and proximity bridge status artifacts.

Completion Rule:

- This skill is complete only when `meta/RESEARCH_OVERVIEW.json` exists, required state updates have been written, and the run validates for downstream consumption.
