---
name: fleet-implementation-planning
description: How engineers map a confirmed plan to specific files and changes — the bridge from reasoning stage to work stage. Target files, change sequence, acceptance criteria mapping.
---

# Implementation Planning — Engineer's Reasoning-to-Work Bridge

You have a confirmed plan. The architect gave you design_input. QA gave you test criteria. The PO approved. Now you need to turn that plan into a sequence of changes that satisfies every requirement. This is the last step before writing code.

## When This Skill Applies

- **Reasoning stage:** After reading contributions, before calling `fleet_task_accept`
- **Your plan IS your implementation plan** — `fleet_task_accept(plan=...)` commits you to this approach

## The Implementation Plan Structure

### 1. Requirement Grounding

Start by restating the verbatim requirement. Your plan MUST reference it. This is the anti-corruption anchor — everything you build traces back to this.

```
Requirement: "Add stage-aware effort to model selection"
```

### 2. Target File Map

List every file you'll touch and WHY:

```
Files to modify:
  fleet/core/model_selection.py — add _STAGE_EFFORT_FLOOR + _apply_stage_adjustment
  fleet/cli/dispatch.py — use model_config (stage-aware) for Claude backends
  fleet/tests/core/test_model_selection.py — add 10 stage-aware tests
  fleet/tests/integration/test_flow_dispatch.py — add 3 stage-dispatch tests
  fleet/tests/integration/conftest.py — add task_stage parameter to make_task

Files NOT touched (verified):
  fleet/core/context_assembly.py — already has stage field, no change needed
  config/methodology.yaml — stages defined, no change needed
```

The "NOT touched" list matters — it proves you examined the scope and ruled things out.

### 3. Change Sequence

Order matters. Dependencies between changes dictate the sequence:

```
Step 1: Add _STAGE_EFFORT_FLOOR dict to model_selection.py
  - Maps stage name → minimum effort level
  - No dependencies, can be tested in isolation

Step 2: Add _apply_stage_adjustment() to model_selection.py
  - Reads floor, compares to current effort, raises if needed
  - Depends on: Step 1 (floor dict)

Step 3: Wire into select_model_for_task()
  - Call _apply_stage_adjustment after unconstrained selection
  - Depends on: Step 2 (adjustment function)

Step 4: Fix dispatch.py to use model_config for Claude backends
  - Currently uses routing.effort (no stage awareness)
  - Depends on: Step 3 (model_config now stage-aware)

Step 5: Add tests
  - 10 unit tests for stage effort floors
  - 3 integration tests for dispatch + stage
  - Depends on: Steps 1-4 (code to test)
```

### 4. Acceptance Criteria Mapping

Map QA's TC-XXX criteria to your implementation steps:

```
TC-001: Investigation stage gets high effort → Step 2 (floor dict has investigation: high)
TC-002: Work stage doesn't inflate effort → Step 2 (floor dict has work: low)
TC-003: Dispatch uses stage-aware config → Step 4 (dispatch.py fix)
```

Every TC-XXX must map to at least one step. If a TC-XXX doesn't map, either your plan is incomplete or the criterion doesn't apply (flag to QA).

### 5. Contribution Compliance

Verify your plan follows all contributions:

```
design_input (architect): "Use floor dict + adjustment function" → Steps 1-2 follow this
security_requirement (devsecops): N/A for this task
qa_test_definition: TC-001 through TC-003 → mapped above
```

## Submitting the Plan

```
fleet_task_accept(plan="""
Implementation plan for: Add stage-aware effort to model selection

Requirement: "Add stage-aware effort to model selection"

Target files:
  fleet/core/model_selection.py — floor dict + adjustment function
  fleet/cli/dispatch.py — use model_config for Claude backends
  fleet/tests/ — 13 tests

Steps:
  1. Add _STAGE_EFFORT_FLOOR to model_selection.py
  2. Add _apply_stage_adjustment()
  3. Wire into select_model_for_task()
  4. Fix dispatch.py model_config usage
  5. Add 10 unit + 3 integration tests

TC mapping: TC-001→Step2, TC-002→Step2, TC-003→Step4

Follows architect design_input: floor dict + adjustment pattern.
""")
```

## During Work Stage

Follow your plan step by step. Each step = one logical commit:

```
fleet_commit(["fleet/core/model_selection.py"], "feat(model): add _STAGE_EFFORT_FLOOR dict [task:abc12345]")
fleet_commit(["fleet/core/model_selection.py"], "feat(model): add _apply_stage_adjustment [task:abc12345]")
fleet_commit(["fleet/cli/dispatch.py"], "fix(dispatch): use model_config for Claude backends [task:abc12345]")
fleet_commit(["fleet/tests/..."], "test(model): add 10 stage-aware effort tests [task:abc12345]")
```

Each commit traces to a plan step. The git log tells the story of your implementation.

## What Implementation Planning is NOT

- NOT designing the approach (architect does that via design_input)
- NOT defining test criteria (QA does that via qa_test_definition)
- NOT deciding security controls (devsecops does that via security_requirement)

You CONSUME all contributions and MAP them to a sequence of file changes. That's the plan.
