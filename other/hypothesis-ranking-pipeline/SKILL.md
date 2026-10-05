---
name: hypothesis-ranking-pipeline
description: Update ranking artifacts for one reviewed hypothesis using canonical placement-opponent selection, ranked-frontier selection, tournament judgments, and Elo updates.
---

# hypothesis-ranking-pipeline

Goal:

- Update ranking artifacts for one reviewed hypothesis using canonical placement-opponent selection, ranked-frontier selection, tournament judgments, and Elo updates.

Inputs:

- candidate `hypotheses/<id>/HYPOTHESIS.json`
- current viable hypothesis frontier
- optional `state/PROXIMITY_GRAPH.json`
- current tournament artifacts
- numeric ranking settings from `state/RESOLVED_RUN_CONFIG.json`

Outputs:

- updated `tournaments/*.json`
- updated candidate and opponent `hypotheses/<id>/HYPOTHESIS.json` artifacts with Elo and match references
- updated `state/PIPELINE_STATE.json`
- updated `state/CURRENT_STAGE.json`

Sub-skills:

- `hypothesis-placement-tournament`
- `hypothesis-ranked-tournament`
- `ranking-elo-update`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/hypothesis.py` and confirm the exact `HypothesisContract` shape before writing any touched `HYPOTHESIS.json` artifact.
- Read `packages/agent_contracts/ranking.py` and confirm the exact `TournamentMatchContract` plus `HypothesisMatchupContract` shapes.
- Read `packages/agent_contracts/resolved_config.py` for `placement_match_count` and `tournament_top_k`.
- Read `packages/agent_contracts/pipeline_runtime.py` before updating `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- If `state/PROXIMITY_GRAPH.json` exists, read `packages/agent_contracts/state.py` and load the exact `ProximityGraphContract`.
- Read `packages/agent_contracts/proximity.py` before interpreting `state/proximity_receipts/<hypothesis_id>.json` or `state/PROXIMITY_STATUS.json`.
- Treat a missing or candidate-incomplete proximity graph as a valid upstream state only when the candidate has a bridge receipt/status proving that the embedding provider was skipped, disabled, unavailable, invalid, or failed. Do not interpret graph absence as permission to fabricate similarity state.

Execution Contract:

- This pipeline skill may orchestrate LLM tournament judgments, but all frontier-selection mechanics must use the canonical deterministic helper surface from `tools`.
- Use `from tools import sync_pipeline_stage_artifacts` as the canonical paired write surface for entering the `Ranking` substage.
- On entry, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Ranking", current_skill="hypothesis-ranking-pipeline")`.
- Use `from tools import select_placement_opponents` as the canonical placement-opponent selector when `state/PROXIMITY_GRAPH.json` is available.
- Use `from tools import select_fallback_placement_opponents` only for receipt-gated placement fallback when usable proximity state is unavailable.
- Use `from tools import get_top_k_hypotheses` to derive the canonical current top-k frontier.
- Use `from tools import should_run_ranked_tournament` to decide whether the candidate must enter ranked play.
- Use `from tools import select_ranked_opponents` to derive the canonical ranked-tournament opponents when ranked play is warranted.
- The helper implementations live in `packages/agent_mechanics/top_k_select.py`.
- Use `ranking-elo-update` after tournament winners are already decided. It is the canonical Elo and match-reference update step.
- Apply the placement batch Elo update before ranked-top-k gating; ranked tournament eligibility must be computed from the post-placement frontier, not stale pre-placement ratings.
- `ranking-elo-update` must close the batch by calling `tools.apply_and_persist_elo_updates(...)` before convergence or downstream routing reads the frontier again.
- The ranking closeout helper updates touched canonical hypothesis artifacts without rewriting standalone `REVIEW/*.json` stage artifacts and writes a `RankingUpdateReceiptContract`.
- Match refs are not sufficient closeout proof; each completed placement or ranked batch must have a persisted ranking update receipt.
- Ranking closeout must use the receipt-writing helper exactly once per completed batch. If the same stable receipt already exists, treat the helper's returned persisted receipt as the closeout proof and do not reapply Elo deltas or append duplicate match refs.
- Do not replace the helper logic with ad hoc manual opponent choice when the canonical artifacts needed by the helpers are available.
- If `state/PROXIMITY_GRAPH.json` is missing, invalid, or does not contain usable state for the candidate, first check `state/proximity_receipts/<candidate_id>.json` and `state/PROXIMITY_STATUS.json`.
- Receipt-gated placement fallback is allowed only when those bridge artifacts explicitly record a skipped, disabled, failed, or provider-unavailable proximity outcome for the candidate. If no such receipt/status exists, return to `hypothesis-proximity-update` instead of choosing opponents manually.
- When receipt-gated placement fallback is used, call `tools.select_fallback_placement_opponents(candidate, hypotheses, placement_match_count)` and write an explicit trace/rationale that names the candidate receipt status and states that placement was not embedding-, proximity-, or similarity-informed.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read the exact ranking, hypothesis, resolved-config, optional proximity, and pipeline-runtime contracts before writing artifacts.
2. Before selecting opponents or running tournaments, call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Ranking", current_skill="hypothesis-ranking-pipeline")`.
3. Load the candidate hypothesis, the current viable frontier, and `state/RESOLVED_RUN_CONFIG.json`.
4. If `state/PROXIMITY_GRAPH.json` is available and contains usable proximity state for the candidate, call `tools.select_placement_opponents(graph, candidate, hypotheses, placement_match_count)` to derive the placement opponents.
5. If `state/PROXIMITY_GRAPH.json` is unavailable, invalid, or candidate-incomplete, inspect the candidate proximity receipt/status. If the bridge artifacts record a skipped, disabled, failed, or provider-unavailable outcome, record an explicit receipt-gated fallback rationale in the trace, name the fallback status, state that placement was not embedding-, proximity-, or similarity-informed, and call `tools.select_fallback_placement_opponents(candidate, hypotheses, placement_match_count)`. If no such bridge artifact exists, stop ranking and return to `hypothesis-proximity-update`. Do not treat fallback selection as equivalent to `tools.select_placement_opponents(...)` when the graph exists.
6. Run `hypothesis-placement-tournament` for each placement matchup and persist the resulting `TournamentMatchContract` artifacts.
7. Run `ranking-elo-update` exactly once for the placement batch immediately after placement winners are decided, and confirm it writes every touched `hypotheses/<id>/HYPOTHESIS.json` artifact plus a ranking update receipt before ranked gating. Match ref arrays must remain duplicate-free.
8. Reload the candidate and viable frontier from the persisted hypothesis artifacts.
9. Call `tools.get_top_k_hypotheses(hypotheses, tournament_top_k)` to derive the post-placement frontier and `tools.should_run_ranked_tournament(candidate, top_k_hypotheses, tournament_top_k)` to decide whether ranked play is required.
10. If ranked play is required, call `tools.select_ranked_opponents(candidate, hypotheses, tournament_top_k)` and run `hypothesis-ranked-tournament` for each resulting matchup. If ranked play is required but no ranked opponents exist because the frontier has no other viable hypotheses, record that as a traceable no-op.
11. If ranked tournament matches were created, run `ranking-elo-update` exactly once for the ranked batch and confirm it writes every touched `hypotheses/<id>/HYPOTHESIS.json` artifact plus a ranking update receipt again. Do not copy opponent-side ranked refs into the current child's evolution-round receipt unless the child was `hypothesis_1_id` for that ranked match.
12. Persist the touched tournament artifacts and touched `hypotheses/<id>/HYPOTHESIS.json` artifacts.
13. Validate the updated ranking artifacts before declaring completion.

Artifact Rules:

- `packages/agent_mechanics/top_k_select.py` is the canonical frontier-selection implementation; the pipeline skill must not fork its semantics in prompt prose.
- Placement-opponent choice, ranked-entry gating, and ranked-opponent choice are deterministic mechanics, not freeform policy decisions.
- When canonical similarity state exists, placement opponents must come from `tools.select_placement_opponents(...)`.
- When canonical similarity state is unavailable and a receipt-gated fallback is used, placement opponents must come from `tools.select_fallback_placement_opponents(...)`, and ranking artifacts and traces must describe the fallback as receipt-gated deterministic placement, not as proximity-informed ranking.
- Ranked-tournament entry must come from `tools.should_run_ranked_tournament(...)`, not from an ad hoc narrative threshold.
- Ranked opponents must come from `tools.select_ranked_opponents(...)`, not from a manually re-sorted custom frontier.

Completion Rule:

- This skill is complete only when the canonical selection helpers have been applied where their required artifacts exist, all resulting tournament winners have been serialized, `ranking-elo-update` has persisted the touched hypothesis artifacts and ranking update receipt, and the run validates for downstream evolution or overview work.
