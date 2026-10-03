---
name: cascade-compile
description: "Use when upstream game design specs changed and downstream specs need regeneration. Triggers: 'cascade compile', 'regenerate downstream', 'spec pipeline'."
---

## 1. Overview

Orchestrates downstream spec regeneration when upstream user specs change. Delegates all work via `task()` — uses sub-skill output only.

## 2. Quick Reference

| Upstream Spec Changed | Downstream Specs to Regenerate |
|-----------------------|--------------------------------|
| game_loop.md | raw_rules.md, system_roster.md |
| raw_rules.md | events_spec.md, ecs_spec.md, state_machine_spec.md, behavior_tree_spec.md |
| system_roster.md | ecs_spec.md |
| events_spec.md | state_machine_spec.md, behavior_tree_spec.md, ecs_spec.md |
| screen_flow.md | screen_architecture_spec.md |
| visual_style.md | asset_budget.md, bundle_strategy.md, network_test.md, renderer_spec.md |
| rendering_target.md | renderer_spec.md, screen_architecture_spec.md |

Rules: topological order only, all synchronous (`run_in_background=false`), abort on failure. Post-cascade alignment check mandatory.

## 3. Core Pattern

### Phase 0: Resume Check
Read `.game-dev-config.json` for `specs_dir` (abort if missing). Check existing specs + mtimes. Present resume prompt.

### Phase 1: Impact Analysis
Identify modified specs, calculate dependency chain.

### Phase 2: Sequential Execution
Regenerate downstream specs in topological order via synchronous `task()`.

### Phase 3: Alignment Check
Delegate `verify-spec-alignment` for final check.

### Phase 4: Completion + Handoff
Summarize results. Prompt `/pipeline-orchestrator` for approval before executing.

## 3. Dependency Graph

```
game_loop.md (root)
   ├-> raw_rules.md (depends on: 002)
   │   ├-> events_spec.md (depends on: 003)
   │   │   ├-> state_machine_spec.md (depends on: 101)
   │   │   └-> behavior_tree_spec.md (depends on: 003, 101)
   │   └-> ecs_spec.md (depends on: 004, 101)
   └-> system_roster.md (depends on: 002)

screen_flow.md (user spec, independent trigger)
   └-> screen_architecture_spec.md (depends on: 010, 008)

visual_style.md (independent)
   ├-> asset_budget.md (depends on: 004, 104)
   │   └-> bundle_strategy.md (depends on: 109)
   └-> network_test.md (depends on: 004, 101)

rendering_target.md (independent)
   ├-> renderer_spec.md (depends on: 008, 007)
   └-> screen_architecture_spec.md (depends on: 010, 008)
```

## 4. Cascade Execution Order

When cascade triggers, identify blast radius and delegate each downstream spec:

1. **`game_loop.md`** → `define-game-rules`, `define-game-systems`
2. **`raw_rules.md`** → `create-event-bus`, `create-behavior-tree`, `create-state-machine`, `design-ecs-architecture`
3. **`system_roster.md`** → `design-ecs-architecture`
4. **`events_spec.md`** → `create-state-machine`, `create-behavior-tree`, `design-ecs-architecture`
5. **`screen_flow.md`** → `design-screen-architecture` (if modified)
6. **`screen_architecture_spec.md`** → (auto-generated from `screen_flow.md` + `rendering_target.md` via `design-screen-architecture`)
7. **`visual_style.md`** → `audit-asset-budget`, `configure-asset-bundling`, `simulate-network-latency`, `design-rendering-architecture`
8. **`rendering_target.md`** → `design-rendering-architecture`, `design-screen-architecture` (if modified)

**Optional** (if relevant):
- `005` → `create-state-machine`/`create-behavior-tree`
- `105` → `simulate-economy-monte-carlo`
- `106` → `flatten-dialogue-tree`
- `107` → `plan-save-migration`
- `006` → `apply-input-bindings`
- `112` → `analyze-performance-profile`

**Rules**: Topological order only. ALL synchronous (`run_in_background=false`). On failure, abort.

### Post-Cascade Alignment (MANDATORY)
Delegate `verify-spec-alignment`. If ERRORs: abort. If WARNINGs: proceed and flag.

### Handoff
Success: *"✅ Cascade complete — [N] specs regenerated. Run `/pipeline-orchestrator`."*
Failure: *"Cascade failed. Fix upstream specs before `/pipeline-orchestrator`."*

## 5. Intercepts

- **Cascade Failure**: *"Critical error at [Spec]. Aborting."*
- **Dependency Gap**: *"Cannot regenerate [Downstream] — [Upstream] missing."*
- **Delegation Failure**: *"Cascade failure at [Skill] — [Error]. Aborting."*

## 6. Red Flags

Delegating exclusively via `task()` — never self-implementing sub-skill logic
Prompting `/pipeline-orchestrator` on success — never skipping handoff
Running resume check first, executing in topological order only
Honoring alignment failures, avoiding circular triggers

## 7. Execution Command

Command: `/cascade-compile`
