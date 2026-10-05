---
name: strategy-router
description: Produce the current `state/STRATEGY_PLAN.json` bundle for configuration, generation, review, evolution, or overview routing.
---

# strategy-router

Goal:

- Produce the current `state/STRATEGY_PLAN.json` bundle for configuration, generation, review, evolution, or overview routing.

Inputs:

- current run-local artifacts
- `RUN_POLICY.yaml`
- `state/RESOLVED_RUN_CONFIG.json`
- optional `state/PIPELINE_STATE.json`
- optional `state/CURRENT_STAGE.json`
- optional `state/EVOLUTION_STATE.json`
- optional `state/COMPLETION_DECISION.json`

Outputs:

- updated `state/STRATEGY_PLAN.json`
- appended `state/STRATEGY_DECISIONS.jsonl`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/strategy_plan.py` and confirm the exact `StrategyPlanContract` shape before writing `state/STRATEGY_PLAN.json`.
- Read `packages/agent_contracts/pipeline_control.py` when completion or evolution signals are present.
- Read persisted stage information from `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` before inferring a route.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- Use `python -m tools.policy.plan_strategy <run_dir> [--phase <Configuration|Generation|Evolution|Insights from Reviews|Proximity|Ranking|Research Overview>]` as the canonical invocation surface.
- The underlying implementation lives in `tools/policy/plan_strategy.py`.
- The router must honor the effective run policy, resolved numeric config, persisted stage artifacts, and completion advisories while still emitting one explicit next-action artifact.
- When `research_plan/RESEARCH_PLAN.json` is missing or invalid, the router must emit `next_action = run_configuration` before any generation or evolution work.
- Omit `--phase` when refreshing routing from persisted `state/PIPELINE_STATE.json` or `state/CURRENT_STAGE.json`.
- Use an explicit `--phase` override only when the caller is intentionally forcing a fresh stage transition instead of resuming the persisted one.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/strategy_plan.py` before writing `state/STRATEGY_PLAN.json`.
2. Read `RUN_POLICY.yaml`, `state/RESOLVED_RUN_CONFIG.json`, and the current persisted run-state artifacts.
3. Run `python -m tools.policy.plan_strategy <run_dir>` for persisted-state refreshes, or add `--phase <...>` only when explicitly forcing a new stage route.
4. Persist the returned `StrategyPlanContract` to `state/STRATEGY_PLAN.json`.
5. Append the matching decision record to `state/STRATEGY_DECISIONS.jsonl`, unless the canonical router detects an equivalent unconsumed open `continue_evolution` decision and only refreshes `state/STRATEGY_PLAN.json`.
6. Validate both artifacts before declaring completion.

Artifact Rules:

- The strategy audit log is append-only and must preserve prior decisions for replay and debugging.
- Call this skill before every generation batch and before every individual evolution round rather than only once at bootstrap.
- When the returned plan is `run_configuration`, configuration must write and validate `research_plan/RESEARCH_PLAN.json` before the caller refreshes routing again.
- When the returned plan stays in `continue_evolution`, the selected parent set in `signals.selected_parent_ids` is the only valid parent set for the next child hypothesis in that round.
- Repeated refreshes of the same unconsumed `continue_evolution` route must not create duplicate open decisions. A new decision is valid only when the pre-round state changed or the earlier equivalent decision has already been consumed by a completed `EVOLUTION_ROUNDS.jsonl` receipt.
- The router must preserve the island-selection outcome for the round:
  - `signals.selection_strategy`
  - `signals.selected_parent_ids`
  - `signals.selected_island_ids`
- For `next_action = continue_evolution`, all router signals must describe the state immediately before the next child is created:
  - `signals.hypothesis_count` and `signals.viable_hypothesis_count` come from currently persisted hypothesis artifacts.
  - `signals.convergence_count` and `signals.entered_top_k_last_round` come from `state/EVOLUTION_STATE.json`.
  - `signals.top_hypothesis_ids` comes from the current persisted top-k frontier.
  - `signals.selected_parent_ids` must only select viable hypotheses that already exist.
  - `signals.selected_island_ids` must match the selected parents' persisted `island_id` values.
  - Do not set `signals.entered_top_k_last_round = true` while `signals.convergence_count` is positive.
- The router does not finalize the concrete evolution strategy itself. It emits the allowed bundle, and `evolution-strategy-supervisor` must choose one strategy from that bundle before child generation.

Completion Rule:

- This skill is complete only when `state/STRATEGY_PLAN.json` has been updated through the canonical router surface, any required new `state/STRATEGY_DECISIONS.jsonl` record has been appended by that surface, and both artifacts validate.
