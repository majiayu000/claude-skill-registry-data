---

name: superpowers-writing-plans
description: >
  Use when you have an approved spec or requirements for a multi-step task, before touching code.
  Transforms an approved design into a detailed, file-level implementation plan with one action
  per task step (2–5 min each), exact file paths, and complete code blocks. Saves plans to
  docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md. Also for: breaking multi-subsystem specs
  into focused sub-plans, mapping file structure before task decomposition, triggering a
  plan-document-reviewer subagent for review, and choosing between subagent-driven versus inline
  execution on completion. Also for: decomposing large features into milestone sub-plans,
  aligning plan structure to existing project conventions, and handing off to a fresh agent
  with a complete, executable plan.
---


# Writing Plans Skill

**Purpose:** Transform an approved design into a detailed, bite-sized implementation plan.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

## Plan File Location

Save to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
(User preferences for plan location override this default.)

## Step 1: Scope Check

If the spec covers multiple independent subsystems, they should have been broken into sub-project specs during brainstorming. If not, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## Step 2: File Structure Mapping

Before defining tasks, map which files will be created or modified:

- Design units with clear boundaries and well-defined interfaces
- Each file has one clear responsibility
- Files that change together should live together
- Follow established patterns in existing codebases
- Prefer smaller, focused files over large ones

This structure informs task decomposition.

## Step 3: Plan Document Header

Every plan MUST start with this header.

Also reference any existing `{phase}-CONTEXT.md` from the project for
implementation constraints already captured.

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Step 4: Task Structure

**Each step is one action (2-5 minutes):**

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## Step 5: Plan Review Loop

After writing the complete plan:

1. Dispatch a single `plan-document-reviewer` subagent with precisely crafted review context — never your session history
2. Provide: path to the plan document, path to spec document
3. If issues found: fix the issues, re-dispatch reviewer for the whole plan
4. If approved: proceed to execution handoff
5. If loop exceeds 3 iterations: surface to human for guidance

Reviewers are advisory — explain disagreements if you believe feedback is incorrect.

## Step 6: Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved. Two execution options:**

**1. Subagent-Driven (recommended)** - Fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**

## Key Principles

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits
- One action per step (2-5 minutes)

## Integration

- **Required sub-skill:** `superpowers-subagent-driven-development` or `superpowers-executing-plans`
- **Called by:** `superpowers-brainstorming`
- **Creates:** plan document at `docs/superpowers/plans/`
- **Prerequisite:** approved design spec from brainstorming
