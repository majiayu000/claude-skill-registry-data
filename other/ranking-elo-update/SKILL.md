---
name: ranking-elo-update
description: Apply deterministic Elo updates for one completed tournament batch, persist touched hypotheses, and write the ranking update receipt.
---

# ranking-elo-update

Goal:

- Apply deterministic Elo updates for one completed tournament batch, persist the touched hypothesis artifacts, and write the ranking update receipt.

Inputs:

- completed tournament `matches`
- canonical `matchups`
- `strategy`
- `run_dir`
- optional `k_factor`
- optional `top_k_limit`

Outputs:

- updated in-memory hypothesis ratings and match references
- updated `hypotheses/<id>/HYPOTHESIS.json` artifacts for all touched hypotheses
- `state/ranking_update_receipts/<receipt_id>.json`
- `RankingUpdateReceiptContract`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/ranking.py` and confirm the exact `TournamentMatchContract` plus `HypothesisMatchupContract` shapes.
- Read `packages/agent_contracts/hypothesis.py` and confirm the exact `HypothesisContract` shape before writing any touched `HYPOTHESIS.json` artifact.
- Use only tournament artifacts whose winners have already been decided and serialized.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- Use `from tools import apply_and_persist_elo_updates` as the stable invocation surface.
- The exported closeout helper is implemented in `packages/run_artifacts/ranking_writeback.py`.
- The helper signature is `apply_and_persist_elo_updates(run_dir, matches, matchups, strategy, k_factor=..., top_k_limit=...) -> RankingUpdateReceiptContract`.
- The closeout helper internally calls the canonical Elo helper, persists touched hypotheses, and writes the ranking update receipt.
- The closeout helper is idempotent for the same stable receipt ID: if the receipt already exists, it returns the persisted receipt instead of reapplying Elo deltas or appending duplicate match refs.
- Accepted `strategy` values are `placement_tournament` and `ranked_tournament` only.
- The closeout helper updates canonical hypothesis bundle fields for touched hypotheses, but it must not rewrite standalone `REVIEW/*.json` stage artifacts.
- Match refs are not a ranking update receipt. Completion requires the persisted `RankingUpdateReceiptContract`.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/ranking.py` and `packages/agent_contracts/hypothesis.py` before writing any touched `HYPOTHESIS.json`.
2. Load the completed tournament matches as `TournamentMatchContract` payloads and the paired matchup payloads as `HypothesisMatchupContract`.
3. Confirm every match already has a decided `winner_id` and that the requested strategy is valid.
4. Call `tools.apply_and_persist_elo_updates(run_dir, matches, matchups, strategy, k_factor=..., top_k_limit=...)`.
5. Confirm the returned `RankingUpdateReceiptContract` names every completed match ID and touched hypothesis ID.
6. Validate the touched hypothesis artifacts and `state/ranking_update_receipts/<receipt_id>.json` before declaring completion.

Artifact Rules:

- This skill updates ratings only after the tournament winner artifacts are already finalized.
- Placement rounds update `placement_match_ids` for the challenger hypothesis and `ranked_match_ids` for the defender.
- Ranked rounds update `ranked_match_ids` for both participating hypotheses.
- Match ref arrays must remain duplicate-free. If a completed match ID is already recorded by both touched hypotheses for the same strategy, do not apply the Elo delta again.
- Do not invent extra ranking heuristics outside the helper; the helper is the canonical Elo update rule.
- Do not replace canonical ranking closeout with ad hoc file edits; use `tools.apply_and_persist_elo_updates(...)` after every Elo batch.
- Review-stage synchronization is a separate concern owned by `tools.sync_hypothesis_review(...)`; Elo writeback must not clobber those standalone review artifacts.
- Do not hand-write ranking update receipts. The closeout helper owns receipt creation.

Completion Rule:

- This skill is complete only when the closeout helper has been applied once to the finished batch, every touched `hypotheses/<id>/HYPOTHESIS.json` artifact has been rewritten in canonical contract form, and the corresponding ranking update receipt exists.
