---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks — dispatches fresh subagents per task with two-stage review (spec compliance, then code quality)
user-invocable: true
disable-model-invocation: true
---

# Subagent-Driven Development

Execute a plan by dispatching a fresh subagent per task, with two-stage review after each: spec compliance first, then code quality.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

**Why subagents:** Isolated context per task — subagents never inherit your session history. You construct exactly what they need. This keeps the coordinator context clean for orchestration work.

## When to Use

Use this after `/squad-plan` generates a parallel workstream plan, OR when you have any plan document with independent tasks.

**vs. dispatching subagents manually:** This enforces the two-stage review loop automatically — no skipping spec compliance to jump to quality.

**Not suitable when tasks are tightly coupled** — if task B depends on task A's exact output, execute sequentially in the main context instead.

## The Process

**Setup:**

1. Read plan file once — extract ALL tasks with full text and context
2. Create tasks in `claude/tasks/todo.md` with all task titles

**Per task loop:**

1. Dispatch **implementer subagent** with: full task text + relevant file context (do NOT make subagent read the plan — provide it directly)
2. If subagent asks questions → answer completely before letting them proceed
3. Implementer implements, tests, commits, self-reviews → reports status
4. Dispatch **spec compliance reviewer** (bootstrap `reviewer` subagent type) → does code match the spec?
   - Issues found → implementer fixes → spec reviewer re-reviews → repeat until ✅
5. Dispatch **code quality reviewer** (bootstrap `reviewer` subagent type) → is code clean, tested, production-ready?
   - Issues found → implementer fixes → quality reviewer re-reviews → repeat until ✅
6. Mark task complete in `claude/tasks/todo.md`

**After all tasks:**

- Dispatch final reviewer across entire implementation
- Run `/mr` to finalize the branch

## Handling Implementer Status

| Status               | Action                                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DONE`               | Proceed to spec compliance review                                                                                                                                                           |
| `DONE_WITH_CONCERNS` | Read concerns first — address correctness/scope concerns before review, note observations and proceed                                                                                       |
| `NEEDS_CONTEXT`      | Provide missing context, re-dispatch                                                                                                                                                        |
| `BLOCKED`            | Diagnose: context problem → provide context + re-dispatch; needs more reasoning → re-dispatch with opus model; task too large → break into smaller pieces; plan is wrong → escalate to user |

**Never** ignore an escalation or force the same model to retry without changes.

## Model Selection

| Task                                     | Model  |
| ---------------------------------------- | ------ |
| Isolated function, clear spec, 1-2 files | haiku  |
| Multi-file, integration concerns         | sonnet |
| Architecture, design, review             | opus   |

## Implementer Prompt Template

```
You are implementing Task N of M in a subagent-driven development session.

**Task:** [full task text from plan]

**Context:**
- Branch: [current branch]
- Plan: [plan file path]
- Relevant files: [list key files — provide content, don't make them read]
- Constraints: [any architectural constraints]

**Requirements:**
1. Follow TDD — write failing test first, then implement
2. Run tests and verify they pass
3. Commit with a clear message
4. Self-review: check for missed requirements, edge cases, quality issues

**Report status as one of:**
- DONE: completed and committed
- DONE_WITH_CONCERNS: done but flagging [specific concern]
- NEEDS_CONTEXT: blocked on [specific missing info]
- BLOCKED: cannot proceed because [specific reason]
```

## Spec Reviewer Prompt Template

```
You are a spec compliance reviewer. Your ONLY job: does the implementation match the spec?

**Spec for this task:** [full task text]
**Implementation:** [git diff or file content]

Check:
1. Does the code implement EVERYTHING the spec requires?
2. Does the code implement NOTHING the spec did not ask for?

Report:
- ✅ COMPLIANT: all spec requirements met, no extras
- ❌ ISSUES: [list each gap or extra feature]
```

## Quality Reviewer Prompt Template

```
You are a code quality reviewer. The spec compliance gate has already passed.

**Implementation:** [git diff or file content]

Check:
1. Tests cover all branches and edge cases?
2. No magic numbers, unclear names, dead code?
3. Error handling appropriate to criticality?
4. File/function size within project limits (400 lines/file, 50 lines/function)?

Report:
- ✅ APPROVED
- ❌ ISSUES (Critical | Important | Minor): [list each issue]
```

## Red Flags — Never Do These

- Start implementation on main branch without explicit user consent
- Skip either review stage (spec compliance AND quality both required)
- Proceed with unfixed issues from a review
- Make subagent read the plan file — provide full text directly
- Accept "close enough" on spec compliance
- Start quality review before spec compliance is ✅
- Move to next task while any review has open issues
- Dispatch multiple implementer subagents in parallel (causes conflicts)
