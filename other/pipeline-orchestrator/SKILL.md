---
name: pipeline-orchestrator
description: "Use when executing the multi-phase build pipeline. Triggers: 'run build pipeline', 'execute phases', 'build orchestration'."
---

## 1. Overview

Executes an 8-phase build pipeline delegating to specialized builder skills via `task()`. Validates each phase before proceeding.

## 2. Quick Reference

| Phase | Status | Skills Delegated |
|-------|--------|------------------|
| 0 | Resume check | — |
| 1 | Dependency check | — |
| 2 | Foundation (MANDATORY) | implement-event-bus, implement-ecs-systems, implement-state-machine, implement-save-system, implement-renderer |
| 3 | Logic (MANDATORY) | implement-behavior-tree, implement-input-handler |
| 4 | Asset & Localization (optional) | implement-asset-loader, implement-localization |
| 5 | Entry Point (MANDATORY) | implement-game-loop |
| 6 | Screen Management (MANDATORY) | implement-screen-manager, implement-scenes |

## 3. Core Pattern

### Phase 0: Resume Check

Read `.game-dev-config.json` for `target_folder`/`specs_dir` (abort if missing). Check `src/` for artifacts:
- **Phase 2**: `src/systems/`, `src/event_bus/`, `src/state_machine/`, `src/renderer/`
- **Phase 3**: `src/behavior_tree/`, `src/input_handler/`
- **Phase 4**: `src/asset_loader/`, `src/localization/`
- **Phase 5**: `src/main.*`, `src/game_loop.*`
- **Phase 6**: `src/screens/`
Ask to resume from earliest missing phase. On "no" or missing `src/`: full build.

### Phase 1: Dependency Check

Verify required specs exist; prepare source directories.

### Phase 2: Foundation (MANDATORY)

Delegate in sequence, validate, max 1 retry:

1. `implement-event-bus` from `events_spec.md`
2. `implement-ecs-systems` from `ecs_spec.md` — validate: `src/systems/` not empty, systems as files, factories present
3. `implement-state-machine` from `state_machine_spec.md`
4. `implement-save-system` from `state_machine_spec.md` + `ecs_spec.md`
5. `implement-renderer` from `renderer_spec.md` + `rendering_target.md` — validate: `src/renderer/` exists

### Phase 3: Logic (MANDATORY)

1. `implement-behavior-tree` from `behavior_tree_spec.md` — validate: BT definitions, AI factories, condition/action nodes
2. `implement-input-handler` from `input_mapping.md`
Max 1 retry.

### Phase 4: Asset & Localization (Non-Critical)

1. `implement-asset-loader` from `bundle_strategy.md`
2. `implement-localization` from `localization_keys.md`
Continue regardless of phase outcome.

### Phase 5: Entry Point (MANDATORY)

- `implement-game-loop` from `game_loop.md` + all specs — validate: ECS systems registered, BT initialized, factories used, `world.update(dt)`. Max 1 retry.

### Phase 6: Screen Management (MANDATORY)

1. `implement-screen-manager` from `screen_architecture_spec.md` + `rendering_target.md` — validate: `src/screens/` exists, screen manager class, base screen class, transition logic
2. `implement-scenes` from `screen_architecture_spec.md` + `rendering_target.md` + `events_spec.md` + `visual_style.md` — validate: `src/screens/scenes/` not empty, one file per screen definition
Max 1 retry.

## 3. Interaction Protocol

* **Orchestrate via `task()` only.** Use sub-skill output directly.

## 4. Final Integrity Audit
- [ ] All mandatory phases (1–3, 5–6) completed with SUCCESS status; no skipped dependencies
- [ ] Each phase output validated before advancing (directories exist, expected artifacts present)
- [ ] Atomic build state maintained — partial failures did not leave orphaned or half-written files
* **Continuous Execution**: Auto-advance phases on success. Report progress automatically.
* **Stop only for**: critical failures, unexpected dependency gaps, or final phase.

### Intercepts

* **Missing Config**: *"Run `/bootstrap-game-project` first."*
* **Phase Failure**: Abort with report.
* **Dependency Missing**: *"Cannot proceed — [Spec] is missing."*

## Golden Rules

* **Phase 0**: Always check existing progress first.
* **SEQUENTIAL**: Advance one phase at a time.
* **MANDATORY PHASES**: Foundation (2), Logic (3), Entry Point (5), Screen Management (6) must succeed.
* **Non-Critical**: Phase 4 (Asset/Localization) — continue regardless of phase outcome.
* **MUST use `task(load_skills=["..."], prompt="...")`** — delegate to sub-skill logic only.
* **MUST include `load_skills`** in every `task()` call.

## 5. Red Flags

Delegating exclusively via `task()` — never self-implementing sub-skill logic
Running resume check first, executing phases in topological order only
Honoring mandatory phase success (Foundation, Logic, Entry Point, Screen Management) before advancing
Checking all specs exist before cascading; aborting on missing dependencies
Including `load_skills` in every `task()` call

## 6. Execution Command

`/pipeline-orchestrator`
