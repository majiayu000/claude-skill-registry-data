---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before writing code or executing experiments
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the executor has zero context for our project and questionable taste. Document everything they need to know: which files to touch for each task, code or protocols, testing or validation, docs they might need to check, how to verify it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. Validation-first. Frequent checkpoints.

Assume they are skilled, but know almost nothing about our toolset or problem domain. Assume they don't know good test/validation design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

**For software:**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

**For research/experiments:**
- "Define the expected result and validation criteria" - step
- "Verify data/resources are available" - step
- "Execute the minimal procedure/analysis" - step
- "Check output against expected criteria" - step
- "Checkpoint (save state, commit notebook)" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature/Experiment Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds/tests/answers]

**Architecture/Approach:** [2-3 sentences about approach]

**Tech Stack/Methods:** [Key technologies, libraries, methods, or protocols]

---
```

## Task Structure

**For Software Tasks:**

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

**For Research/Experiment Tasks:**

```markdown
### Task N: [Analysis/Experiment Name]

**Resources:**
- Data: `exact/path/to/data.csv` or `data source description`
- Script: `analysis/exact/path/to/script.py`
- Output: `results/exact/path/to/output.csv`
- Notebook: `notebooks/exact/path/to/analysis.ipynb`

**Step 1: Define expected outcome**

Success criteria: [Specific measurable outcome]
- Expected range/value: [e.g., "p < 0.05", "AUC > 0.8", "correlation positive"]
- Failure looks like: [e.g., "no significant effect", "data quality issues"]

**Step 2: Verify prerequisites**

Check: Data exists and is valid
Run: `head -5 data/path/file.csv && wc -l data/path/file.csv`
Expected: [N rows, correct columns]

**Step 3: Execute analysis**

```python
# Minimal analysis code
df = pd.read_csv("data/path/file.csv")
result = statistical_test(df["column"])
print(f"Result: {result}")
```

**Step 4: Validate result**

Run analysis and check:
- Does result match expected criteria?
- Are there any warnings or anomalies?
- Is output in expected format?

**Step 5: Checkpoint**

```bash
git add analysis/script.py results/output.csv
git commit -m "analysis: complete [specific analysis]"
```
Or for notebooks: Save notebook, export key results
```

## Remember

- Exact file/data paths always
- Complete code/commands in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, validation-first, frequent checkpoints
- For experiments: include expected ranges and failure criteria

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans
