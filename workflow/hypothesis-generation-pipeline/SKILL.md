---
name: hypothesis-generation-pipeline
description: Dispatch one enabled generation strategy for a given `ResearchPlan`.
---

# hypothesis-generation-pipeline

Goal:

- Dispatch one enabled generation strategy for a given `ResearchPlan`.

Inputs:

- `ResearchPlan`
- active `state/STRATEGY_PLAN.json`
- one enabled generation `strategy`
- optional resume context from `state/PIPELINE_STATE.json`

Outputs:

- `hypotheses/<id>/HYPOTHESIS.json`
- `hypotheses/<id>/HYPOTHESIS.md`
- `hypotheses/<id>/ORIGIN.json`
- `literature/queries/<query_id>/*` when `hypothesis-generate-literature` is selected
- `hypotheses/<id>/REVIEW/*.json`
- updated `meta/INSIGHTS_FROM_REVIEWS.json` when the hypothesis is viable
- updated proximity receipt/status artifacts, plus `state/PROXIMITY_GRAPH.json` when the embedding bridge succeeds
- updated `tournaments/*.json`
- updated `islands/ISLANDS.json`
- updated `state/PIPELINE_STATE.json`

Sub-skills:

- `hypothesis-generate-literature`
- `literature-search`
- `hypothesis-generate-debate`
- `hypothesis-generate-assumptions`
- `hypothesis-review-pipeline`
- `insights-from-reviews`
- `hypothesis-proximity-update`
- `hypothesis-ranking-pipeline`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/research_plan.py` before consuming `research_plan/RESEARCH_PLAN.json` as the canonical generation brief.
- Read `packages/agent_contracts/strategy_plan.py` before consuming `state/STRATEGY_PLAN.json` as the active generation-stage routing input.
- Read `packages/agent_contracts/hypothesis.py` before dispatching any atomic generation skill that will write `hypotheses/<id>/HYPOTHESIS.json`.
- Read `packages/agent_contracts/literature.py` and `skills/shared-references/literature-search-contract.md` before dispatching `hypothesis-generate-literature`.
- Read `packages/agent_contracts/state.py` before assigning or updating `islands/ISLANDS.json`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json`.
- Read `state/STRATEGY_PLAN.json` and confirm the current round permits the selected generation strategy.
- Read `RUN_POLICY.yaml` when review rigor or downstream optional review behavior depends on the effective run policy.

Execution Contract:

- This pipeline skill does not own hidden prompt templates.
- `state/STRATEGY_PLAN.json` is a routing input to this skill, not a generation-stage artifact that this skill may rewrite ad hoc.
- `research_plan/RESEARCH_PLAN.json` is a required canonical input. If it is missing or invalid, stop immediately and return control to the top-level workflow or configuration stage instead of attempting generation.
- Append-only routing audit artifacts such as `state/STRATEGY_DECISIONS.jsonl` remain owned by the top-level orchestration layer and the canonical router surface in `python -m tools.policy.plan_strategy <run_dir>`.
- It coordinates downstream generation, review, insights, proximity, and ranking skills; those downstream skills remain responsible for the field-level canonical shapes of the artifacts they write.
- The selected generation strategy must be consistent with `state/STRATEGY_PLAN.json`.
- When the selected generation strategy is `literature_exploration_generation`, the dispatched `hypothesis-generate-literature` skill must call `tools.search_literature(run_dir, request)` and consume a non-blocked `EvidenceBundleContract` before writing a literature-grounded hypothesis.
- The generation pipeline must not accept prompt-invented literature evidence in place of `literature/queries/<query_id>/EVIDENCE_BUNDLE.json`.
- On a fresh run, execute one generated hypothesis per selected generation strategy so the initial frontier mirrors the full seed set instead of collapsing to a single synthetic output.
- On a regeneration pass triggered from evolution, execute one generated hypothesis per selected generation strategy and then refresh the evolution plan before continuing.
- After each generated hypothesis is written, immediately run:
  - `hypothesis-review-pipeline`
  - `insights-from-reviews` when the hypothesis is viable
  - `hypothesis-proximity-update` for each viable hypothesis
  - `hypothesis-ranking-pipeline`
- The generation pipeline must not skip proximity because no embedding vector is already present. The bridge owns provider invocation and records a receipt/status when the provider is disabled, unavailable, invalid, or failed.
- Do not generate, infer, or fabricate embeddings in prompt output. Proceed to ranking through the documented receipt-gated fallback path only after `hypothesis-proximity-update` has recorded a skipped or failed receipt/status.
- For initial frontier seeding, assign one non-empty `island_id` to each viable generated hypothesis, then call `tools.ensure_run_islands_for_hypotheses(run_dir)` before the round is considered complete.
- Newly created seed islands are initialization records only: they must keep `decayed_reward = 0.0`, `decayed_visits = 0.0`, and `visit_count = 0`.
- Initial frontier island assignment is distinct from the later single-island reward / decay mechanics in `hypothesis-evolution-loop`; do not apply `tools.update_single_island_reward(...)`, `tools.update_run_single_island_reward(...)`, or any manual reward/visit increment during seeding.
- Persist only canonical island fields. Do not add dashboard-derived or router-derived fields such as `hypothesis_ids`, `ucb_score`, or `strategy_label` to `islands/ISLANDS.json`.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/research_plan.py`, `packages/agent_contracts/strategy_plan.py`, `packages/agent_contracts/hypothesis.py`, `packages/agent_contracts/literature.py`, `packages/agent_contracts/state.py`, and `packages/agent_contracts/pipeline_runtime.py` before consuming generation-stage routing state or performing any directly managed generation-stage write.
2. Read `research_plan/RESEARCH_PLAN.json`, active `state/STRATEGY_PLAN.json`, and relevant policy context.
3. If the research plan artifact is missing or invalid, stop immediately. Do not dispatch any generation strategy.
4. Confirm that the selected generation strategy is allowed for the active round.
5. Dispatch exactly one matching atomic generation skill for the current strategy and let that sub-skill write the canonical hypothesis and origin artifacts. For `literature_exploration_generation`, require the sub-skill to call `tools.search_literature(run_dir, request)` and preserve the resulting literature artifacts.
6. Run `hypothesis-review-pipeline` for the newly created hypothesis.
7. If the hypothesis remains viable, run `insights-from-reviews`.
8. Run `hypothesis-proximity-update` for each viable hypothesis by calling `tools.update_hypothesis_proximity(run_dir, hypothesis_id)` through that skill. If the bridge records a skipped, disabled, failed, or provider-unavailable receipt/status, preserve it and continue to ranking without fabricating placeholder embeddings.
9. Run `hypothesis-ranking-pipeline`.
10. For initial frontier seeding, assign exactly one non-empty `island_id` to each viable generated hypothesis, call `tools.ensure_run_islands_for_hypotheses(run_dir)`, and verify the resulting canonical `islands/ISLANDS.json` contains one unvisited island record per viable seed hypothesis.
11. Update `state/PIPELINE_STATE.json` as required by the top-level workflow and refreshed downstream status.
12. Do not append or rewrite `state/STRATEGY_DECISIONS.jsonl` from this skill. If the caller needs a routing refresh or new decision record, return control to the top-level orchestration layer or `strategy-router`.
13. Run `python -m tools.validation.contract_validation <run_dir> --skill hypothesis-generation-pipeline` before declaring completion.

Completion Rule:

- This skill is complete only when the selected generation strategy has produced exactly one canonical hypothesis candidate, required downstream review and frontier-upkeep work has been dispatched, and any directly managed state or island updates validate.
