---
name: hypothesis-evolution-loop
description: Run the iterative evolution loop from the current persisted run state until convergence.
---

# hypothesis-evolution-loop

Goal:

- Run the iterative evolution loop from the current persisted run state until convergence.

Inputs:

- current persisted run artifacts
- active `state/STRATEGY_PLAN.json`
- optional `resume` flag

Outputs:

- updated hypotheses
- updated island statistics
- updated proximity receipt/status artifacts, plus `state/PROXIMITY_GRAPH.json` when the embedding bridge succeeds
- updated tournament artifacts
- updated convergence counters
- updated `state/EVOLUTION_STATE.json`
- appended `state/EVOLUTION_ROUNDS.jsonl`
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/pipeline_control.py` before updating `state/EVOLUTION_STATE.json` or `state/COMPLETION_DECISION.json`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Read `packages/agent_contracts/hypothesis.py` before writing any evolved `hypotheses/<id>/HYPOTHESIS.json` artifact.
- Read `packages/agent_contracts/state.py` before any island state validation, and read `packages/run_artifacts/island_state.py` before invoking the run-level island persistence helper.
- Read `packages/agent_contracts/ranking.py` when the round will write tournament artifacts through downstream ranking work.
- Read `packages/agent_contracts/evolution_round.py` before appending `state/EVOLUTION_ROUNDS.jsonl`.
- Read the active `state/STRATEGY_PLAN.json`, `state/PIPELINE_STATE.json`, `state/CURRENT_STAGE.json`, `state/EVOLUTION_STATE.json`, the selected parent hypotheses, and the latest parent review bundles before starting or resuming a round.

Execution Contract:

- Resume decisions must come from artifact state, not hidden process memory.
- The active evolution route must be consistent with `state/STRATEGY_PLAN.json`.
- Refresh `state/STRATEGY_PLAN.json` through `python -m tools.policy.plan_strategy <run_dir>` before every evolution round that is resuming from persisted state.
- Use an explicit phase override only when the caller is intentionally forcing a new stage transition instead of restoring the current persisted round or substage.
- Use `from tools import sync_pipeline_stage_artifacts` as the canonical paired write surface when entering `Evolution`, `Reflection`, `Insights from Reviews`, `Proximity`, or `Ranking`.
- The stage-sync helper is implemented in `packages/run_artifacts/stage_sync.py`.
- Before resuming or starting an evolution round, call `tools.sync_pipeline_stage_artifacts(...)` for `Evolution`.
- Before dispatching review, insights, proximity, or ranking work for the active child, call `tools.sync_pipeline_stage_artifacts(...)` for the exact substage being entered so dashboard state reflects the live round status.
- Read `state/RESOLVED_RUN_CONFIG.json` before deciding whether the loop is capped or completion-driven:
  - `convergence.max_iterations > 0` means a user-visible capped run.
  - `convergence.max_iterations == 0` means completion-driven mode; do not invent a small hard iteration cap.
  - `convergence.safety_max_iterations` is still a hard safety ceiling and must be recorded if reached.
  - Persist `EVOLUTION_STATE.safetyMaxIterations` exactly from `RESOLVED_RUN_CONFIG.convergence.safety_max_iterations`; never rewrite it from the current iteration count.
- Treat `iteration_policy = completion_driven` together with `human_checkpoint = auto` as an autonomous loop contract: after one round closes, refresh routing and continue automatically instead of returning to the user for per-round confirmation.
- `human_checkpoint` can still intentionally pause the loop, but only at the configured checkpoint boundary (`before_overview`, `before_completion`, or `every_major_stage`).
- If the host-agent turn stops before a terminal route is reached, the handoff must state that convergence has not been reached, state is persisted, and the recommended next action is continue evolution through resume or an explicit continue request.
- One evolution round may create only one new child hypothesis. Do not batch-refine every seed candidate once and then stop.
- Do not synthesize placeholder hypotheses, reviews, tournaments, proximity receipts, embeddings, or evolution-round receipts to make progress.
- If an evolve, review, proximity, ranking, convergence, or round-receipt substage cannot run through its canonical skill or tool, stop and report a resumable blocked state instead of writing low-information artifacts.
- When `state/STRATEGY_PLAN.json` reports `next_action: continue_evolution`, use `signals.selected_parent_ids` as the parent set for the next child hypothesis and persist the resulting parent linkage in `HYPOTHESIS.json` and `ORIGIN.json`.
- Before generating that child, run `evolution-strategy-supervisor` and choose exactly one concrete evolution strategy allowed by:
  - `signals.selection_strategy`
  - `selected_evolution_strategies`
  - the parent hypotheses and their latest review bundles
- For single-island rounds, use `from tools import update_run_single_island_reward` as the canonical run-level island reward / decay update and persistence surface after the child has finished review and ranking update receipt coverage.
- For seed island initialization and multi-island child island creation, use `from tools import ensure_run_islands_for_hypotheses` as the canonical run-level island initialization surface.
- The run-level helper is implemented in `packages/run_artifacts/island_state.py` and delegates the deterministic reward mechanics to `packages/agent_mechanics/island_reward_update.py`.
- Do not hand-edit `islands/ISLANDS.json`, and never write `state/ISLANDS.json`. The run-level helper must load hypotheses, apply decay/reward, and persist the canonical `islands/ISLANDS.json` artifact.
- After the run-level helper returns, reload canonical `islands/ISLANDS.json` and confirm the selected island now has nonzero `visit_count` and nonzero `decayed_visits`; the selected island `visit_count` must also cover the completed single-island round receipts that selected it.
- If the selected island metrics do not validate after a single-island closeout, stop before the next routing refresh, run `python -m tools.validation.contract_validation <run_dir> --skill hypothesis-evolution-loop`, and report a resumable blocked state instead of continuing on stale UCB state.
- Newly created islands must remain unvisited until they are later selected by a completed single-island round: verify `decayed_reward = 0.0`, `decayed_visits = 0.0`, and `visit_count = 0` after calling the initialization helper.
- Persist only canonical island fields. Do not add dashboard-derived or router-derived fields such as `hypothesis_ids`, `ucb_score`, or `strategy_label` to `islands/ISLANDS.json`.
- The lower-level `tools.update_single_island_reward(...)`, `tools.compute_single_island_reward(...)`, and `tools.apply_decayed_island_update(...)` surfaces are internal/testing fallbacks only for in-memory mechanics; do not use them as the host-agent evolution-loop persistence path.
- Use `from tools import evaluate_convergence` as the canonical convergence-counter update surface after the child's final top-k membership is known.
- The convergence helper is implemented in `packages/agent_mechanics/convergence_check.py`.
- Use `from tools import append_evolution_round_record` as the canonical append-only write surface for `state/EVOLUTION_ROUNDS.jsonl` after the child has completed review, proximity, ranking, and convergence updates.
- `state/EVOLUTION_ROUNDS.jsonl` is the completed round receipt. It does not replace `state/STRATEGY_DECISIONS.jsonl`, and it must not be used to rewrite prior routing decisions.
- The round receipt's `placement_match_ids` and `ranked_match_ids` must be child-owned closeout refs for that round only:
  - placement refs require `match_strategy = placement_tournament` and `hypothesis_1_id = child_hypothesis_id`
  - ranked refs require `match_strategy = ranked_tournament` and `hypothesis_1_id = child_hypothesis_id`
  - duplicate match IDs are invalid
  - later matches where the child appears as `hypothesis_2_id` may remain in the child's lifetime `HYPOTHESIS.json` refs, but they must not be copied into this earlier round receipt
- After appending a completed round receipt, update `state/EVOLUTION_STATE.json` from the same convergence helper output and refresh `state/STRATEGY_PLAN.json`; do not leave pre-round router signals as the current plan.
- The referenced `continue_evolution` decision must be a canonical router record from `python -m tools.policy.plan_strategy <run_dir>` with router-level signals. Do not add child IDs, chosen concrete strategies, proximity statuses, tournament IDs, top-k entry results, or convergence transitions to `state/STRATEGY_DECISIONS.jsonl`.
- Treat the referenced router signals as a replayable pre-round state contract:
  - `signals.hypothesis_count` and `signals.viable_hypothesis_count` are the counts before the child is created.
  - `signals.convergence_count` is the value before the child is created and must become the round receipt's `convergence_count_before`.
  - `signals.entered_top_k_last_round` must reflect the prior completed round when one exists.
  - `signals.top_hypothesis_ids` must become the round receipt's `previous_top_k_ids`.
  - `signals.selected_parent_ids` must reference viable hypotheses already persisted before the child is created.
  - `signals.selected_island_ids` must match the selected parents' persisted `island_id` values.
- A completed evolution round must be replayable from exactly one router decision, one evolved child, one review bundle, one proximity receipt, completed ranking artifacts with ranking update receipt coverage, one convergence update, and one appended round receipt.
- After emitting the child hypothesis, you must:
  - run `hypothesis-review-pipeline`
  - run `insights-from-reviews` when the child is viable
  - run `hypothesis-proximity-update` for each viable child hypothesis
  - run `hypothesis-ranking-pipeline`
  - for `signals.selection_strategy == single_island`, call `tools.update_run_single_island_reward(run_dir, selected_island_id, candidate_hypothesis.id, decay_factor)` exactly once after the child's final Elo and viability state are known, and use the helper-persisted canonical `islands/ISLANDS.json` artifact as the source of truth
  - after that single-island reward update, verify the helper-persisted selected island has nonzero `visit_count` and `decayed_visits`; do not append a completed round receipt or refresh routing if the selected island metrics are stale
  - for `signals.selection_strategy == multi_island`, assign the child a new non-empty `island_id`, call `tools.ensure_run_islands_for_hypotheses(run_dir, [candidate_hypothesis.id])`, verify the created island remains unvisited, and do not apply the single-island reward helper to that cross-island child
  - call `tools.evaluate_convergence(candidate_hypothesis.id, previous_top_k_ids, current_top_k_ids, current_convergence_count)` exactly once after the final ranked frontier is known, then persist both `enteredTopKLastRound` and `convergenceCount` exactly as returned
  - call `tools.append_evolution_round_record(run_dir, record)` exactly once with an `EvolutionRoundRecordContract` that records the decision index, selected parent IDs, selected island IDs, chosen concrete evolution strategy, child hypothesis ID, child island ID, proximity receipt status, child-owned placement/ranked tournament match IDs, previous/current top-k IDs, `entered_top_k`, and convergence counts before and after the round
  - update `state/EVOLUTION_STATE.json`
- When `next_action: return_to_generation`, leave the evolution loop, run the requested generation pass, then refresh the evolution plan again.
- Do not skip proximity because no embedding vector is already present. The bridge owns provider invocation and records a receipt/status when the provider is disabled, unavailable, invalid, or failed.
- Do not generate, infer, or fabricate embeddings in prompt output. Let ranking use its documented receipt-gated missing-graph fallback only after `hypothesis-proximity-update` has recorded a skipped or failed receipt/status.
- The evolution-round `proximity_receipt_status` must be copied from the persisted per-child `state/proximity_receipts/<child_hypothesis_id>.json` receipt. Do not infer this field from environment variables, provider availability, or dashboard state.
- The loop is complete only when `state/EVOLUTION_STATE.json` records a terminal stop reason and the routing audit log contains one decision record per evolved hypothesis.
- When writing `state/EVOLUTION_STATE.json`, persist the active `stopPolicy`, `iterationPolicy`, `iterationBand`, and `safetyMaxIterations` metadata from the effective run configuration and policy artifacts.
- Only record `stopReason: safety_iteration_limit_reached` when `iterationCount >= RESOLVED_RUN_CONFIG.convergence.safety_max_iterations` and `safetyLimitHit` is `true`.
- When consumed by a host agent, run `python -m tools.validation.contract_validation <run_dir> --skill hypothesis-evolution-loop` after each evolved hypothesis is persisted.
- When the loop reports `status: completed`, run `python -m tools.validation.verify_pipeline_completion <run_dir> --skill hypothesis-evolution-loop`.
- The final research overview remains a separate step in `research-overview-pipeline`.
- Treat `complete` as a completion-verifier outcome after overview, not as a `state/STRATEGY_PLAN.json` route.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read the exact Python contracts for the evolution, pipeline-state, hypothesis, island, and ranking artifacts that this round may write.
2. Load the persisted routing, pipeline-state, evolution-state, island, and parent-hypothesis artifacts for the active round or substage.
3. Refresh `state/STRATEGY_PLAN.json` through `python -m tools.policy.plan_strategy <run_dir>` before every evolution round that is resuming from persisted state, or use an explicit phase override only when intentionally forcing a new stage transition.
4. If `next_action` is `inspect_state`, pause automatic execution and inspect or repair the persisted routing artifacts before continuing.
5. If `next_action` is `run_review`, `run_insights`, `run_proximity`, or `run_ranking`, first update `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` to that exact substage, then resume it for the active round before attempting another child.
6. If `next_action` is `return_to_generation`, leave the evolution loop, run the requested generation pass, then refresh the evolution plan again.
7. If `next_action` is `continue_evolution`, first call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Evolution", current_skill="hypothesis-evolution-loop")`, then run `evolution-strategy-supervisor`, create exactly one new child hypothesis from `signals.selected_parent_ids`, and persist its canonical hypothesis and origin linkage artifacts.
   - Confirm the active strategy decision includes router signals for hypothesis counts, viable counts, convergence state, top-k IDs, research-plan status, island selection, and selected parents.
   - Keep child/result metadata out of `state/STRATEGY_DECISIONS.jsonl`; it is recorded later through `tools.append_evolution_round_record(...)`.
8. After the child is emitted, update the run-level stage artifacts before each downstream child substage:
   - `Reflection` / `hypothesis-review-pipeline`
   - `Insights from Reviews` / `insights-from-reviews` when viable
   - `Proximity` / `hypothesis-proximity-update` for each viable child
   - `Ranking` / `hypothesis-ranking-pipeline`
9. In the proximity substage, call `tools.update_hypothesis_proximity(run_dir, hypothesis_id)` exactly once through `hypothesis-proximity-update`. If the bridge records a skipped, disabled, failed, or provider-unavailable receipt/status, preserve the per-child receipt and continue to ranking without fabricating placeholder embeddings.
10. For `signals.selection_strategy == single_island`, call `tools.update_run_single_island_reward(run_dir, selected_island_id, candidate_hypothesis.id, decay_factor)` exactly once after the child's final Elo and viability state are known, then reload `islands/ISLANDS.json` and verify the selected island metrics before writing the completed round receipt or refreshing routing; for `signals.selection_strategy == multi_island`, assign the child a new non-empty `island_id`, call `tools.ensure_run_islands_for_hypotheses(run_dir, [candidate_hypothesis.id])`, verify the created island remains unvisited, and do not apply the single-island helper.
11. After the final ranked frontier is known, call `tools.evaluate_convergence(candidate_hypothesis.id, previous_top_k_ids, current_top_k_ids, current_convergence_count)` exactly once and persist the returned `entered_top_k` / `convergence_count` values into `state/EVOLUTION_STATE.json` without manual reinterpretation.
12. Append the completed round receipt through `tools.append_evolution_round_record(run_dir, record)`. The record must serialize `packages.agent_contracts.EvolutionRoundRecordContract`; copy `proximity_receipt_status` from the persisted per-child receipt when one is recorded, include only duplicate-free child-owned placement/ranked match IDs for this round, and do not infer or omit the child ID, chosen concrete strategy, or top-k entry result.
13. Update `state/EVOLUTION_STATE.json`, `state/PIPELINE_STATE.json`, and `state/CURRENT_STAGE.json` for the finished round or resumed substage. Keep `currentPhase`, `currentSkill`, and `stageTrail` aligned with the active substage being closed. Treat `max_iterations = 0` as completion-driven mode, reserve `max_iterations_reached` for user-visible capped runs only, and reserve `safety_iteration_limit_reached` for cases where the resolved safety ceiling has actually been reached.
14. After each finished round, refresh `state/STRATEGY_PLAN.json` again. In `completion_driven + human_checkpoint = auto` mode, keep looping until the refreshed plan reaches a terminal route (`generate_overview` or `inspect_state`) or a validator/safety block occurs.
15. If `human_checkpoint` requests a pause, stop only at that configured checkpoint boundary. Do not ask for user confirmation after every evolution child in `auto` mode.
16. If execution stops before a terminal route for any reason other than a configured checkpoint, produce a paused handoff that says convergence has not been reached and the next action is continue evolution via resume or an explicit continue request.
17. Run `python -m tools.validation.contract_validation <run_dir> --skill hypothesis-evolution-loop` after each evolved hypothesis is persisted. When the loop reports `status: completed`, run `python -m tools.validation.verify_pipeline_completion <run_dir> --skill hypothesis-evolution-loop`.

Completion Rule:

- This skill is complete only when the active round or restored substage has been executed according to the persisted routing plan, the completed child has a matching `state/EVOLUTION_ROUNDS.jsonl` receipt, required evolution-state updates validate, and any terminal completion signal has been checked through the completion verifier.
