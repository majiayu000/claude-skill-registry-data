---
name: writing-plans
description: Use when turning an approved design into executable OpenSpec tasks or one bounded Beads work contract before touching code. Triggers on "implementation plan", "task breakdown", "engineer handoff", "spec-to-plan", "write a plan for this feature".
source: ~/.agents/skills@2026-07-13
---


# Writing Plans

## Overview

Write comprehensive execution contracts assuming the engineer has zero context for the codebase.
Document what they need to know: exact files, behavior, tests, references, commands, expected
results, and rollback concerns. Keep every durable task in the repository's canonical workflow
artifact.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to author the canonical execution tasks."

## Choose the Existing Workflow Lane

- **Proposal lane:** Work only inside the active `openspec/changes/<slug>/` change. Put the
  executable checklist in `openspec/changes/<slug>/tasks.md`; proposal, delta specs, and design
  remain the authority for intent and requirements.
- **Ad-hoc lane:** Enrich exactly one existing or newly claimed Beads issue with the goal, affected
  paths, constraints, acceptance criteria, steps, verification, and rollback notes where Beads is
  available.
- **No workflow authority:** Return the execution contract to the active semantic workflow binding
  without creating a persistent side ledger.

Do not create a standalone plan document, duplicate checklist, worktree-specific plan directory,
or alternative completion lifecycle. `feature` owns proposal authoring, Beads owns ad-hoc state,
and `apply`/`apply:all` own execution.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

Each step is one atomic action (2-5 minutes) — see Task Structure below for the canonical shape
(write test / verify fail / implement / verify pass / commit). The reason for this granularity
is not aesthetic: a subagent-driven or interrupted execution resumes at an arbitrary step with no
memory of what came before it. A step that silently depends on "remember what I did two steps
ago" breaks the resume contract — write every step so it stands alone.

## Canonical Artifact Header

For a proposal-lane change, retain the repository's OpenSpec task schema. When the schema permits
context before the checklist, include the following information in its required artifact rather
than inventing another document:

```markdown
# [Feature Name] Execution Contract

> **For agentic workers:** OpenSpec tasks are the only durable checklist. Claim work through the
> linked Beads state and follow the repository's dependency and concurrency rules.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
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
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Other Plan-Writing Anti-Patterns

Beyond placeholders, subtler failure modes exist where the plan *looks* complete but the gap only
surfaces once an engineer is implementing it — vague acceptance criteria, missing rollback notes
on schema/infra tasks, hidden reverse dependencies in task ordering, and test instructions that
name a framework not actually used in this codebase. Read
[`references/anti-patterns.md`](references/anti-patterns.md) for the full list with rationale
before running the Self-Review anti-pattern scan below.

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output

## Self-Review

After writing the complete plan, run a fresh-eyes check against the spec yourself — not a
subagent dispatch: spec coverage (can you point to a task for each requirement?), the anti-pattern
scan, and type consistency across tasks (a function called `clearLayers()` in Task 3 but
`clearFullLayers()` in Task 7 is a bug). Read
[`references/self-review-checklist.md`](references/self-review-checklist.md) for the full
three-step checklist before offering Execution Handoff. Fix issues inline as you find them — no
need to re-review, just fix and move on.

## Optional: Independent Subagent Review

The self-review above is a checklist you run yourself and is sufficient for most plans. For a
larger or higher-risk plan — many tasks, touches multiple subsystems, or the user asks for an
extra check before implementation starts — dispatch a fresh subagent as a second, independent
pass instead of (or in addition to) self-review: a subagent has no attachment to the plan it
didn't write and catches gaps self-review misses. Use the dispatch template in
[`plan-document-reviewer-prompt.md`](plan-document-reviewer-prompt.md) — it defines the review
checklist (completeness, spec alignment, task decomposition, buildability), calibration
guidance (flag only issues that would cause real implementation problems), and the expected
`Status: Approved | Issues Found` output format. Fix any reported issues inline, same as
self-review findings.

## Execution Handoff

After the canonical artifact passes self-review:

- Hand one ready named feature to `apply`.
- Hand an explicitly selected ordered queue to `apply:all`.
- For bounded ad-hoc work, leave exactly one claimed Beads issue ready for the repository's ad-hoc
  execution lane.
- Let the active harness decide whether safe independent tasks run inline or through parallel
  agents. Do not encode harness-specific dispatch mechanics or create checkpoint documents.

Report the canonical OpenSpec change slug or Beads issue ID and the verification commands the
executor must run. Do not offer a second execution-mode menu: authorization, dependencies,
concurrency, completion, archival, and persistence belong to `apply`, `apply:all`, and Beads.
