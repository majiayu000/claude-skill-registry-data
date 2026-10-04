---
name: fleet-regression-testing
description: How QA identifies what needs re-testing when code changes — impact analysis, test selection, and the regression-checker sub-agent for targeted verification.
---

# Regression Testing — QA's Change Impact Skill

When code changes, tests that passed before might break. Your job isn't to re-run everything — it's to identify WHAT might break and target your verification. The `regression-checker` sub-agent handles the mechanical part. You handle the judgment.

## When Regression Testing Applies

- **Fix tasks:** Engineer fixed a rejected task. What else might their fix have broken?
- **Refactoring:** Code restructured without behavior change — but did behavior actually stay the same?
- **Dependency updates:** Library version changed — what consumes that library?
- **Configuration changes:** YAML changed — what reads that config?

## The Impact Analysis Framework

### Step 1: Identify What Changed

Read the PR diff or commit history. Categorize changes:

| Change Type | Impact Radius | What to Re-test |
|------------|--------------|-----------------|
| Function signature changed | All callers of that function | Import grep + caller tests |
| Return value changed | All consumers of that return | Downstream tests |
| Config key renamed | All readers of that config | Config loading tests |
| Exception type changed | All catch blocks for that exception | Error handling tests |
| Module moved/renamed | All importers | Import resolution |
| Default value changed | All code that relies on the default | Boundary tests |

### Step 2: Map the Dependency Chain

A change in `fleet/core/model_selection.py` affects:
- Direct callers: `fleet/cli/dispatch.py` (imports select_model_for_task)
- Indirect users: `fleet/cli/orchestrator.py` (calls dispatch)
- Config consumers: any test that mocks model_selection behavior
- Chain effects: dispatch records, labor stamps (downstream data)

Use the `regression-checker` sub-agent for mechanical tracing:
```
Agent: regression-checker
Prompt: "Given changes to fleet/core/model_selection.py (functions: 
        select_model_for_task, _apply_stage_adjustment), identify 
        all test files that should be re-run and explain why."
```

### Step 3: Select Tests

Don't re-run everything. Target:

1. **Direct tests** — tests for the changed module itself
2. **Caller tests** — tests for modules that call the changed functions
3. **Integration tests** — tests that exercise the changed flow end-to-end
4. **Boundary tests** — tests at the edges of the changed behavior

```bash
# Direct tests for the module
.venv/bin/python -m pytest fleet/tests/core/test_model_selection.py -v

# Tests that import from the changed module
grep -rl "model_selection" fleet/tests/ | xargs .venv/bin/python -m pytest -v

# Integration flow tests
.venv/bin/python -m pytest fleet/tests/integration/test_flow_dispatch.py -v
```

### Step 4: Verify and Report

After running targeted tests:
- All pass? → Report "Regression check: {N} targeted tests, all pass. Change is safe."
- Failures? → Classify: regression (test was passing, now fails) vs pre-existing vs test-needs-update

Post as typed comment on the task:
```
Regression Check: {task_title}
Changed: {files}
Tests targeted: {N} across {M} test files
Result: {pass/fail}
- Direct: {N} pass
- Callers: {N} pass
- Integration: {N} pass
- Regression found: {details if any}
```

## What Regression Testing is NOT

- NOT running the full test suite blindly (that's CI's job)
- NOT writing new tests (that's predefinition's job)
- NOT validating against TC-XXX criteria (that's test validation's job)

Regression testing is IMPACT ANALYSIS + TARGETED VERIFICATION. You determine what COULD break and verify it didn't.

## Phase-Appropriate Depth

| Phase | Regression Scope |
|-------|-----------------|
| poc | Direct tests only — just verify the change works |
| mvp | Direct + caller tests |
| staging | Direct + callers + integration |
| production | Full regression: direct + callers + integration + performance |
