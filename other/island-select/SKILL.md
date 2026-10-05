---
name: island-select
description: Select the next island strategy and parent hypothesis set for one evolution round.
---

# island-select

Goal:

- Select the next island strategy and parent hypothesis set for one evolution round.

Inputs:

- `islands/ISLANDS.json`
- current viable `hypotheses/<id>/HYPOTHESIS.json` frontier
- `iteration_count`
- numeric island-selection settings from `state/RESOLVED_RUN_CONFIG.json`

Outputs:

- deterministic `SelectionResult`
- selection strategy
- selected parent hypotheses
- when consumed by routing, updated `state/STRATEGY_PLAN.json` signals

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/state.py` and confirm the exact `IslandStateContract` shape used inside `islands/ISLANDS.json`.
- Read `packages/agent_contracts/hypothesis.py` for the exact `HypothesisContract` shape.
- Read `packages/agent_contracts/resolved_config.py` for the island numeric settings.
- When the result is persisted into routing state, also read `packages/agent_contracts/strategy_plan.py`.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- Use `from tools import select_island_hypotheses` as the stable invocation surface.
- The exported helper is implemented in `packages/agent_mechanics/island_select.py`.
- The helper signature is `select_island_hypotheses(islands, hypotheses, iteration_count, ucb_exploration_constant=..., softmax_temperature=..., stagnation_epsilon=...) -> SelectionResult`.
- The helper is the canonical implementation of UCB island selection, stagnation-triggered multi-island fallback, and Elo-softmax parent sampling.
- `islands/ISLANDS.json` is the only canonical persisted island source for this skill. Do not read, repair from, or write `state/ISLANDS.json`.
- If `islands/ISLANDS.json` is missing, invalid, or uses deprecated item keys such as `island_id`, `reward`, `stagnation_count`, or `last_updated`, stop and report an invalid canonical island artifact instead of selecting parents.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/state.py`, `packages/agent_contracts/hypothesis.py`, and `packages/agent_contracts/resolved_config.py`.
2. Load island state from `islands/ISLANDS.json` and the current viable hypotheses from their canonical `HYPOTHESIS.json` artifacts. Reject `state/ISLANDS.json` as a non-canonical legacy path.
3. Read `iteration_count` and the island numeric settings from `state/RESOLVED_RUN_CONFIG.json`.
4. Call `tools.select_island_hypotheses(...)` with the canonical inputs.
5. Return the `SelectionResult` to the caller. When used by routing, persist:
   - `signals.selection_strategy`
   - `signals.selected_parent_ids`
   - `signals.selected_island_ids`
6. Validate any updated `state/STRATEGY_PLAN.json` artifact before declaring completion.

Artifact Rules:

- Do not replace the helper with ad hoc manual parent choice when the canonical artifacts are available.
- When routing persists the result, the selected parent set becomes the only valid parent set for the next child hypothesis in that round.
- `islands/ISLANDS.json` remains the canonical source of island reward and visit statistics; this skill reads it but does not mutate it.
- Canonical island items must use `id`, `decayed_reward`, `decayed_visits`, and `visit_count`. Deprecated aliases are not accepted as selection inputs.

Completion Rule:

- This skill is complete only when the deterministic selection result has been produced and any caller-owned routing artifact has been updated consistently with that result.
