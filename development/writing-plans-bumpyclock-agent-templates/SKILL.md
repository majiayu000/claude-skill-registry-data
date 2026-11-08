---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
source: https://github.com/obra/superpowers/tree/main/skills/writing-plans
license: MIT
---

# Writing Plans

Create implementation plans from approved specs/requirements before code. Plans must let skilled engineers/agents with near-zero repo context build safely.

## Local rules

- Follow stricter repo/user git policy.
- In dotfiles, no commits unless user explicitly asks.
- Use `subagent-driven-development` by default for approved controller-owned plans.
- SDD handoffs: run reviewer loops at aggregation boundaries, not per peer leaf task. Task with children → implement safe ready children first, integrate under parent/subtree, run one combined read-only `reviewer` for that subtree covering spec compliance + code quality. Recursive for nested trees, bottom-up. Dispatch leaf-level reviewers only when caller explicitly asks, risk requires isolation, or stricter repo policy requires it.
- Inline execution allowed for: tiny micro-flow fixes, urgent critical-path blockers, verification-only work, unavailable/forbidden subagents, explicit user request.
- Isolated worktree → follow local git workflow instructions.
- Referenced Superpowers skills unavailable → map locally: implementation/debugging → `programming`, frontend/web → `web-development`, git/GitHub → `git-workflow`.

## Scope check

Spec covers independent subsystems → suggest separate plans. Each plan produces working, testable software on its own. No decomposition buried inside mega-plans.

## Tasque source of truth

`tsq` is source of truth for SDD-backed or durable planning.

Controller-owned planned implementation:

1. Create or reuse `tsq` parent task.
2. Attach approved spec/requirements to parent.
3. Decompose into small atomic child tasks.
4. Encode readiness dependencies with `tsq block`.
5. Encode preferred sequencing with `tsq order`.
6. Attach final implementation plan to parent.
7. Mark parent planned.

Tiny micro-flow fixes, urgent blockers, one-off verification, child-planner drafts don't need new `tsq` tasks unless caller asks or passes parent ID.

Never claim path, task ID, dependency, or `tsq` state not actually created.

## Repo artifacts

`tsq` is canonical for implementation workflow state.

Repo plan/spec files are optional exports. Write only when:

- user asks for saved doc,
- repo convention requires one,
- `tsq` unavailable.

Product/API/user docs still required when behavior changes.

## File structure first

Before tasks, map files to create/modify + each file's responsibility.

Rules:

- Clear boundaries, clear interfaces.
- One file = one main responsibility where practical.
- Files that change together live together.
- Split by responsibility, not technical layer by default.
- Follow existing repo patterns.
- Touched file unwieldy → plan focused split only when it serves current goal.
- No unrelated refactors.

File map drives task decomposition.

## Atomic task decomposition

Decompose into small, atomic child tasks.

Each child task must have:

- one owned scope,
- clear files/modules,
- acceptance criteria,
- focused verification command,
- smoke/live verification when user-visible behavior changes,
- dependencies in `tsq`, not hidden in prose.

Prefer more small tasks over fewer large. Large one-shot tasks fail more often, reduce safe parallelism.

Parallelize ready tasks by default only when:

- `tsq block` dependencies clear,
- owned write sets disjoint,
- shared contracts stable,
- generated artifacts/config/migrations/global styles/snapshots cannot collide.

Use `tsq block` for readiness/safety dependencies. `tsq order` only for preferred sequencing.

## Task granularity

Each step ≈ 2-5 minutes, one small action.

Prefer TDD loop when possible:

- write failing test
- run, confirm failure
- implement minimum code
- run, confirm pass
- smoke/live verification when user-visible behavior changes
- commit only if requested

## Plan document header

Every plan MUST start with this header:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Execute approved controller-owned plans with `subagent-driven-development` by default. Task implementers own atomic leaf tasks; reviewer loops run at parent/subtree aggregation boundaries, not per peer leaf task, with one combined read-only reviewer checking spec compliance and code quality for the integrated subtree. Integration owner owns final root integration. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task structure

Use exact file paths, verified code shapes, exact commands, expected output. Include complete code only when verified from repo context or provided by caller. Otherwise exact patch-level instructions with named symbols, target behavior, assertions, investigation steps.

````markdown
### Task N: [Component Name]

**Tasque:** `<parent-id>` / `<child-id>` for SDD-backed or durable plans. For inline/non-durable plans, omit or write `Tasque: not used — <reason>`. Never fabricate IDs.

**Owned scope:**

- May edit: `exact/path/or/module`
- Must not edit: `exact/path/or/module`

**Files:**

- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Dependencies:**

- Blocks: `<none | child-id>`
- Blocked by: `<none | child-id>`
- Ordered after: `<none | child-id>`

**Acceptance criteria:**

- [Specific observable outcome]
- [Specific regression that must stay fixed]

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

- [ ] **Step 4: Run focused verification**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Run smoke/live verification when user-visible**

Run: `exact command or manual check`
Expected: PASS / observed expected behavior

- [ ] **Step 6: Commit if requested**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

Adjust steps to fit repo, keep each step one action.

## No placeholders

Plan failures. Never write:

- `TBD`, `TODO`, `implement later`, `fill in details`
- `Add appropriate error handling`
- `Add validation`
- `Handle edge cases`
- `Write tests for the above` without actual test intent and code shape
- `Similar to Task N` — repeat code; tasks may be read out of order
- Steps describing code changes without code or exact patch-level direction
- References to undefined types, functions, methods, props, commands, files
- Fabricated code blocks, commands, APIs, paths, or `tsq` IDs

## Required detail

Every plan needs:

- Exact file paths.
- Owned files/modules per child task.
- Complete code only when verified from repo context; otherwise exact patch-level direction.
- Exact commands with expected output.
- Tests/verification for each behavior, with enough test-design detail for someone weak at test design.
- Smoke/live verification for user-visible behavior.
- Docs/changelog steps when behavior/API/user flow changes.
- DRY, YAGNI, TDD where useful.
- Commits only when requested by user.

## Independent review

After writing plan, review against spec. Mandatory.

1. Spec coverage — every requirement maps to task(s). Add missing tasks.
2. Placeholder scan — remove failures listed above.
3. Type/signature consistency — names used later match definitions earlier.
4. Buildability — implementer can follow without repo lore or guessing.
5. Test coverage — every task has tests verifying its behavior.
6. Task decomposition — tasks small, focused, independently reviewable.
7. Atomicity — tasks small enough for one subagent to own safely.
8. Owned scope — every atomic child has clear may-edit and must-not-edit boundaries.
9. Dependencies — readiness blockers use `tsq block`; preference order uses `tsq order`.
10. Parallel safety — ready tasks have disjoint owned scopes and stable shared contracts.
11. Verification — focused checks and smoke/live checks present where needed.
12. Scope control — plan does not add unrequested behavior.

Fix issues inline. No need to re-review from scratch.

## Plan review gate

After writing plan into `tsq`, dispatch `plan-reviewer` for controller-owned planned implementation.

Pass:

- `tsq` parent task ID
- plan text/spec attached to parent
- child task list
- dependency graph
- constraints or ignored areas, if any

Iterate only on blocking issues. Re-run until `Status: Approved`.

Blocker needs product/API/scope decision, `tsq` state invalid, or reviewer cannot run → stop, ask caller/controller. Do not start implementation until approved or explicitly waived by controller.

Plan-reviewer must verify:

- task decomposition atomic enough,
- dependencies explicit in `tsq`,
- ready tasks parallelizable safely,
- owned scopes clear,
- review loops at parent/subtree aggregation boundaries instead of per peer leaf task, one combined reviewer pass covering both spec compliance + code quality per integrated subtree unless caller explicitly requested leaf-level or two-stage review,
- verification includes smoke/live checks where needed.

Inside `planner` subagent → do not dispatch review. Return plan, tell caller/controller to run `plan-reviewer`.

## Execution handoff

After plan-reviewer approves controller-owned planned implementation, invoke `subagent-driven-development` by default.

Inline execution allowed for:

- tiny micro-flow fixes,
- urgent critical-path blockers,
- verification-only work,
- unavailable/forbidden subagents,
- explicit user request.

No execution-choice prompt when SDD clearly applies. Start SDD with reviewer loops at aggregation boundaries. For each parent/subtree: dispatch safe ready leaf implementers, integrate outputs, run one combined reviewer over integrated subtree. Combined reviewer prompt: spec compliance first, then code quality, return one PASS/FAIL with evidence. Report:

```text
Plan-reviewer approved `tsq` parent `<id>`. Starting SDD: dispatching safe ready leaf tasks concurrently where write sets disjoint and shared contracts stable, then reviewing integrated parent/subtree boundaries with one combined reviewer per aggregation point.
```
