---
name: co-scientist-pipeline
description: Run the full Co-Scientist pipeline for one research run.
---

# co-scientist-pipeline

Goal:

- Run the full Co-Scientist pipeline for one research run.

Inputs:

- one run directory root
- run-local `input.md`
- optional compatibility `config.yaml`
- optional `resume` flag
- existing run artifacts when resuming

Outputs:

- updated run artifacts
- `RUN_POLICY.yaml`
- `state/POLICY_DECISION.json`
- `state/RESOLVED_RUN_CONFIG.json`
- `state/STRATEGY_PLAN.json`
- `state/STRATEGY_DECISIONS.jsonl`
- `state/EVOLUTION_ROUNDS.jsonl`
- `state/PIPELINE_STATE.json`
- `state/CURRENT_STAGE.json`
- `state/HOST_AGENT_HANDOFF.json` when a host-agent handoff is prepared
- final research overview when convergence is reached

Sub-skills:

- `research-config`
- `hypothesis-generation-pipeline`
- `hypothesis-evolution-loop`
- `research-overview-pipeline`

Required shared references:

- `../shared-references/artifact-contract.md`
- `../shared-references/completion-contract.md`
- `../shared-references/policy-contract.md`
- `../shared-references/resolved-config-contract.md`
- `../shared-references/strategy-contract.md`
- `../shared-references/state-contract.md`
- `../shared-references/integration-contract.md`
- `../shared-references/execution-modes.md`
- `../shared-references/schema-index.md`

Context Loading:

- Open `../shared-references/integration-contract.md`, `../shared-references/strategy-contract.md`, `../shared-references/completion-contract.md`, and `../shared-references/schema-index.md` before dispatching any sub-skill.
- Before writing top-level control-plane artifacts, read the exact Python contracts for:
  - `RUN_POLICY.yaml` and `state/POLICY_DECISION.json` from `packages/agent_contracts/policy.py`
  - `research_plan/RESEARCH_PLAN.json` from `packages/agent_contracts/research_plan.py` when dispatching `research-config`
  - `state/RESOLVED_RUN_CONFIG.json` from `packages/agent_contracts/resolved_config.py`
  - `state/STRATEGY_PLAN.json` and `state/STRATEGY_DECISIONS.jsonl` from `packages/agent_contracts/strategy_plan.py`
  - `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` from `packages/agent_contracts/pipeline_runtime.py`
  - `state/EVOLUTION_STATE.json` and `state/COMPLETION_DECISION.json` from `packages/agent_contracts/pipeline_control.py`
- If `resume` is `true`, inspect `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` before dispatching any sub-skill.
- Preserve existing dashboard links, handoff artifacts, and manifest history during resume work.

Execution Contract:

- Host-agent mode should consume this skill directly from the repository-local `skills/` tree.
- This top-level skill owns run-level orchestration and control-plane sequencing. It should not manually re-specify field-level hypothesis, review, ranking, or overview payloads that are already owned by downstream skills plus their exact Python contracts.
- Resume and routing decisions must come from persisted artifacts, not hidden process memory.
- Fresh bootstrap may materialize missing control-plane artifacts, but resumed work must preserve existing valid control-plane artifacts and rebuild only the missing ones.
- Before dispatching generation, review, insights, proximity, ranking, or evolution work, refresh `state/STRATEGY_PLAN.json`.
- Refresh `state/STRATEGY_PLAN.json` through `python -m tools.policy.plan_strategy <run_dir>` when resuming persisted routing state for the active round or substage.
- Use `python -m tools.policy.plan_strategy <run_dir>` when restoring persisted routing state. Add an explicit phase override such as `--phase Configuration`, `--phase Generation`, or `--phase Evolution` only when the top-level workflow is intentionally forcing a new stage transition rather than restoring the persisted one.
- Use `from tools import sync_pipeline_stage_artifacts` as the canonical paired write surface when entering any active substage.
- The stage-sync helper is implemented in `packages/run_artifacts/stage_sync.py`.
- Before dispatching any sub-skill, call `tools.sync_pipeline_stage_artifacts(...)` so `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json` stay aligned.
- When a substage is active, `state/PIPELINE_STATE.json currentSkill` must match the canonical skill for that `currentPhase`.
- When a substage is an active runtime phase (`Generation`, `Evolution`, `Reflection`, `Insights from Reviews`, `Proximity`, `Ranking`, or `Research Overview`), `state/PIPELINE_STATE.json status` must be `running` unless the run is terminal. Do not leave active work as `not_started`.
- `run_configuration` is the explicit routing action for preparing or repairing `research_plan/RESEARCH_PLAN.json`. Do not treat configuration as an implicit bootstrap side effect.
- `inspect_state` is a blocked control-plane action. Do not continue automatic generation, review, or evolution work until the persisted routing artifacts are inspected or repaired.
- Do not synthesize placeholder hypotheses, reviews, tournaments, proximity receipts, embeddings, or evolution-round receipts to make progress.
- If the required sub-skill or canonical tool cannot be executed, stop and report a resumable blocked state instead of writing low-information artifacts.
- Do not dispatch `hypothesis-generation-pipeline` until `research_plan/RESEARCH_PLAN.json` exists and validates through the canonical `ResearchPlanContract`.
- Generation seeding must follow the active `state/STRATEGY_PLAN.json` exactly. On a fresh run, execute one generated hypothesis per selected generation strategy instead of collapsing the seed frontier into a single batch summary.
- Evolution must remain round-based: one refreshed routing plan, one chosen parent set, one chosen concrete evolution strategy, and at most one new child hypothesis per round.
- A completed evolution round must be replayable from exactly one router decision, one evolved child, one review bundle, one proximity receipt, completed ranking artifacts with ranking update receipt coverage, one convergence update, and one appended round receipt.
- The appended round receipt must include only child-owned, duplicate-free placement/ranked match IDs for that round; do not copy later opponent-side lifetime refs from `HYPOTHESIS.json` into an earlier `EVOLUTION_ROUNDS.jsonl` record.
- Evolution safety metadata must come from `state/RESOLVED_RUN_CONFIG.json`; do not rewrite `EVOLUTION_STATE.safetyMaxIterations` from the current iteration count or from prompt memory.
- `safety_iteration_limit_reached` is valid only when `iterationCount >= RESOLVED_RUN_CONFIG.convergence.safety_max_iterations` and `safetyLimitHit` is `true`.
- `completion_driven` controls stop semantics, while `human_checkpoint` controls where the host agent may pause for the user. Do not conflate them.
- When the effective policy is `iteration_policy = completion_driven` and `human_checkpoint = auto`, keep executing generation and evolution work autonomously until the routing plan reaches `generate_overview` or `inspect_state`, or until validation / safety ceilings block further work.
- Treat `complete` as a completion-verifier outcome, not as a `state/STRATEGY_PLAN.json next_action`.
- In that autonomous mode, do not ask the user whether to continue after each evolution round or each new child hypothesis.
- If the host-agent turn must stop before a terminal route is reached, say explicitly that the run is paused, convergence has not been reached, persisted state is resumable, and the next recommended action is continue evolution via resume or an explicit continue request.
- When `human_checkpoint = before_overview`, pause only after evolution reaches an overview-ready routing state and before `research-overview-pipeline`.
- When `human_checkpoint = before_completion`, pause only after overview work is complete and before final completion writeback.
- When `human_checkpoint = every_major_stage`, pause only at major stage boundaries and not merely because one evolution child finished.

Execution Steps:

1. Open the required shared references, then open `skills/shared-references/schema-index.md` and the exact Python contracts for any top-level control-plane artifact this run will write or update.
2. If the run is fresh, materialize the initial control-plane artifacts in canonical form:
   - `RUN_POLICY.yaml`
   - `state/POLICY_DECISION.json`
   - `state/RESOLVED_RUN_CONFIG.json`
   - `state/STRATEGY_PLAN.json`
3. If the run is resuming, inspect `state/PIPELINE_STATE.json` and `state/CURRENT_STAGE.json`, preserve existing valid control-plane artifacts, and rebuild only the missing artifacts needed to continue safely.
4. Skip already completed phases listed in `completedSkills` only when the required artifacts for that phase are present and valid.
5. Before each configuration dispatch, generation batch, or evolution round, refresh `state/STRATEGY_PLAN.json` through `python -m tools.policy.plan_strategy <run_dir>` for persisted-state refreshes, or add `--phase <...>` only when explicitly forcing a new stage route.
6. If `next_action` is `run_configuration`, first call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Configuration", current_skill="research-config")`, then execute `research-config`, validate `research_plan/RESEARCH_PLAN.json`, and refresh the strategy plan again before any generation work.
7. If `next_action` is `inspect_state`, pause automatic execution and inspect or repair the persisted routing artifacts before continuing.
8. If `next_action` is `run_generation` or `return_to_generation`, first call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Generation", current_skill="hypothesis-generation-pipeline")`, then execute `hypothesis-generation-pipeline` once per selected generation strategy, validate the writes, and refresh the strategy plan again.
9. If `next_action` is `run_review`, `run_insights`, `run_proximity`, or `run_ranking`, first call `tools.sync_pipeline_stage_artifacts(...)` for the exact resumed substage so both state artifacts stay aligned, then execute that substage before attempting any new evolution child.
10. If `next_action` is `continue_evolution`, first call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Evolution", current_skill="hypothesis-evolution-loop")`, then run `evolution-strategy-supervisor` to choose exactly one concrete evolution strategy from `selected_evolution_strategies`, create exactly one new child hypothesis from `signals.selected_parent_ids`, and run the downstream child substage work before closing the round.
    - Treat `state/STRATEGY_DECISIONS.jsonl` as canonical router-planning audit only.
    - Do not add child hypothesis IDs, chosen concrete strategies, proximity statuses, tournament match IDs, top-k entry results, or convergence transitions to strategy decisions; write those through `state/EVOLUTION_ROUNDS.jsonl`.
    - If an evolve, review, proximity, ranking, convergence, or round-receipt substage cannot run through its canonical skill or tool, pause in a resumable blocked state instead of fabricating the missing artifact.
11. After each closed evolution round, refresh `state/STRATEGY_PLAN.json` again. When the effective policy is `completion_driven` with `human_checkpoint = auto`, continue automatically into the next round unless the refreshed plan now requires `generate_overview` or `inspect_state`.
12. If the effective `human_checkpoint` requests a pause (`before_overview`, `before_completion`, or `every_major_stage`), stop only at that configured checkpoint boundary and record enough state for a clean resume. Do not introduce per-round confirmation prompts in `auto` mode.
13. If execution stops for any other reason before convergence or a terminal route, produce a paused handoff: current convergence has not been reached, state has been persisted, and the next action is continue evolution through resume or an explicit continue request.
14. After each major phase write, run `python -m tools.validation.contract_validation <run_dir> --skill co-scientist-pipeline`.
15. After the evolution loop reports a terminal stop reason, run `python -m tools.validation.verify_pipeline_completion <run_dir> --skill co-scientist-pipeline`.
16. If overview generation is recommended, first call `tools.sync_pipeline_stage_artifacts(run_dir, current_phase="Research Overview", current_skill="research-overview-pipeline")`, then run `research-overview-pipeline`. After overview generation, run `python -m tools.validation.verify_pipeline_completion <run_dir> --skill co-scientist-pipeline` again and record `state/COMPLETION_DECISION.json` only when the verifier now recommends `complete` or an explicit override rationale is supplied.
17. Do not mark the pipeline complete after refining each seed hypothesis only once. Completion requires a replayable round history in `state/STRATEGY_DECISIONS.jsonl` and completed round receipts in `state/EVOLUTION_ROUNDS.jsonl`.

Completion Rule:

- This skill is complete only when the required top-level control-plane artifacts are valid, downstream phase work has been dispatched according to the refreshed routing plan, and any final completion or overview transition has been recorded in canonical form.
