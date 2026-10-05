---
name: hypothesis-review-pipeline
description: Run the decomposed review pipeline for a single hypothesis and persist each review stage as a structured artifact.
---

# hypothesis-review-pipeline

Goal:

- Run the decomposed review pipeline for a single hypothesis and persist each review stage as a structured artifact.

Inputs:

- `ResearchPlan`
- `MetaReview`
- `Hypothesis`
- optional resume context from `state/PIPELINE_STATE.json`

Outputs:

- `hypotheses/<id>/REVIEW/INITIAL_REVIEW.json`
- `hypotheses/<id>/REVIEW/FULL_REVIEW.json`
- `hypotheses/<id>/REVIEW/DEEP_VERIFICATION.json`
- `hypotheses/<id>/REVIEW/OBSERVATION_REVIEW.json`
- `hypotheses/<id>/REVIEW/SIMULATION_REVIEW.json`
- `hypotheses/<id>/REVIEW/REVIEW_SUMMARY.json`
- `literature/queries/<query_id>/*` when full review or deep verification needs external literature evidence
- updated `hypotheses/<id>/HYPOTHESIS.json`
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Sub-skills:

- `hypothesis-initial-review`
- `literature-search`
- `hypothesis-full-review`
- `hypothesis-deep-verification`
- `hypothesis-observation-review`
- `hypothesis-simulation-review`
- `hypothesis-review-summary`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/review.py` before writing any per-stage review artifact under `hypotheses/<id>/REVIEW/`.
- Read `packages/agent_contracts/hypothesis.py` before updating the embedded review payload inside `hypotheses/<id>/HYPOTHESIS.json`.
- Read `packages/agent_contracts/literature.py` and `skills/shared-references/literature-search-contract.md` before dispatching `hypothesis-full-review` or `hypothesis-deep-verification`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Read `skills/shared-references/codex-reviewer-routing.md` before using any optional Codex reviewer subagent route.
- Read `RUN_POLICY.yaml` before dispatching review work so the active `review_rigor` setting is honored.
- Read the current hypothesis, research plan, and any optional run-level review guidance before starting the stage sequence.

Execution Contract:

- This pipeline skill does not own hidden prompt templates.
- It orchestrates atomic review skills so the runtime can trace each review stage independently.
- Downstream atomic review skills remain responsible for the exact field-level contents of each standalone review artifact.
- The canonical `hypotheses/<id>/HYPOTHESIS.json` artifact must be updated after every review stage so the embedded `review` payload stays in sync with the per-stage review files.
- Use `from tools import sync_hypothesis_review` after each stage artifact write. The canonical synchronization helper is implemented in `packages/run_artifacts/review_sync.py`; do not hand-edit embedded review JSON.
- Use `from tools import sync_pipeline_stage_artifacts` as the canonical paired write surface for entering the `Reflection` substage.
- Treat `tools.sync_hypothesis_review(run_dir, hypothesis_id)` as a hard gate. If it fails, stop the review sequence immediately instead of continuing with later stages.
- On entry, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Reflection", current_skill="hypothesis-review-pipeline")` before starting the review sequence.
- When consumed by a host agent, validate both the embedded hypothesis review payload and the per-stage review artifacts. If validation fails, stop and repair the review bundle before running the next stage or returning control.
- Full review and deep verification must use `tools.search_literature(run_dir, request)` or an existing matching `EvidenceBundleContract` before making external literature support claims.
- The review pipeline must not accept prompt-invented paper metadata or model-memory citations as formal evidence.
- The review pipeline must not accept empty completed review artifacts. A completed or passing stage must contain concrete, hypothesis-specific findings that downstream evolution and ranking can use.
- Do not use placeholder review phrases such as `Viable evolved hypothesis`, `Refined from parent`, `Must outperform parent`, `Synthesize evolved catalyst`, or `Benchmark against parent` as the substantive content of any completed review artifact.
- Codex reviewer subagents are optional. If unavailable, run the same review contract in the main thread and record `reviewerRoute = local_main_thread` in the trace.
- If a Codex reviewer subagent is used, record `state/agent_traces/codex/<skill>/<timestamp>.json`; the trace is audit evidence and must not replace canonical review artifacts.
- Reviewer subagents must not write deterministic mechanics artifacts or bypass `tools.sync_hypothesis_review` and schema validation.
- Regardless of `review_rigor`, run the full review stack for every hypothesis:
  - `hypothesis-full-review`
  - `hypothesis-deep-verification`
  - `hypothesis-observation-review`
  - `hypothesis-simulation-review`
- `review_rigor` may shorten or deepen the reasoning inside those stages, but it must not disable any review artifact.

Execution Steps:

1. Open `skills/shared-references/schema-index.md` and `skills/shared-references/codex-reviewer-routing.md`, then read `packages/agent_contracts/review.py`, `packages/agent_contracts/hypothesis.py`, `packages/agent_contracts/literature.py`, and `packages/agent_contracts/pipeline_runtime.py` before writing any per-stage review artifact, embedded review state, literature evidence artifact, reviewer trace, or run-level stage artifact.
2. Read the research plan, current hypothesis, optional meta-review guidance, and active `RUN_POLICY.yaml`.
3. Before dispatching atomic review work, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Reflection", current_skill="hypothesis-review-pipeline")`.
4. Run `hypothesis-initial-review` and persist the resulting stage artifact.
5. Immediately call `tools.sync_hypothesis_review(run_dir, hypothesis_id)` to synchronize `review.initial_review` back into `hypotheses/<id>/HYPOTHESIS.json`. If sync fails, stop here and repair the artifact instead of continuing.
6. Determine the required reasoning depth from `review_rigor`, then run the full remaining atomic review stack for the hypothesis. When `hypothesis-full-review` or `hypothesis-deep-verification` needs external literature evidence, require those skills to call `tools.search_literature(run_dir, request)` or consume an existing matching evidence bundle.
7. After each later review stage, call `tools.sync_hypothesis_review(run_dir, hypothesis_id)` again so the standalone stage artifact and aggregate hypothesis artifact remain consistent. If sync fails, stop before the next stage.
8. Run `hypothesis-review-summary` after the required review stages finish.
9. Run `python -m tools.validation.contract_validation <run_dir> --skill hypothesis-review-pipeline`. If validation fails, stop and repair the review bundle before declaring completion or returning control.

Completion Rule:

- This skill is complete only when all review-stage artifacts exist, the embedded review payload in `hypotheses/<id>/HYPOTHESIS.json` matches those stage artifacts, and the resulting files validate for downstream routing.
