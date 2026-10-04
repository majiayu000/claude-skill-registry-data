---
name: planupdate
description: Use when the user asks to "update the plan", "sync the plan with the code", "/ar:planupdate", or "/ar:pu". Reconciles an existing plan with the current codebase and marks what already shipped.
aliases: [pu]
argument-hint: [plan file]
---

# Quick Plan Update (/ar:planupdate)

<purpose>

The user's request is the task description for everything below.

## Harness-specific plan lifecycle

- **Claude Code:** Use `EnterPlanMode` and `ExitPlanMode` where this skill instructs; `ExitPlanMode` is the approval boundary.
- **Pi:** Do not call `EnterPlanMode` or `ExitPlanMode` on Pi because Pi exposes neither tool. Write or refine the durable plan note directly, report its exact path for approval, and after approval start execution with `/ar pp <path>`.
- **Native task tracking is conditional:** Before following any task-operation instruction below, use only a mutation tool that the current session actually exposes. Claude uses `TaskCreate`/`TaskUpdate`; Pi and Prime use those tools only when the autorun extension registered them; Codex uses the flat `update_plan` checklist only when exposed (`update_plan` is unavailable in Codex Plan mode). If no native task mutation tool is available, keep progress in the durable Markdown checklist, do not call or retry an unavailable task tool, and report that native task state was not updated. Every unqualified `TaskCreate`, `TaskUpdate`, dependency, and `TaskList` instruction below is conditional on those capabilities.
- **Other harnesses:** Use a native plan-mode boundary and native task tracking only when those tools actually exist; otherwise use the same durable-note approval and checklist workflow as Pi with that harness's documented autorun command spelling.

</purpose>

---

<requirements>

## CRITICAL RULES — SURVIVE COMPACTION

If this session was compacted, these rules STILL apply without exception:

1. **On Claude Code, call ExitPlanMode when ALL planning tasks are complete** — this is Claude Code’s approval boundary. On Pi, report the durable plan note path and wait for explicit user approval.
2. **When TaskCreate is exposed, ALL plan steps require TaskCreate.** If another native checklist mutation tool is exposed, track every step with that tool instead. Otherwise, use the durable Markdown checklist as required by the capability rule above.
3. **ALL user instructions must be directly quoted as a numbered list** at the top of the plan file. Every distinct message, with sub-items for context if needed.
4. **NEVER delete content from plan files.** Only add or make micro-edits. Read before editing. Verify after.
5. **Keep tasks updated:** Before starting any step, `TaskUpdate(status="in_progress")`. When done, `TaskUpdate(status="completed")`.

---

## 1. Foundation (Reference)

### 1.1 Key Principles

| Acronym | Meaning |
|---------|---------|
| TDD | Test-Driven Development |
| DRY | Don't Repeat Yourself |
| OODA | Observe-Orient-Decide-Act |
| KISS | Keep It Simple |
| YAGNI | You Aren't Gonna Need It |
| SOLID | Single responsibility, Open/closed, Liskov, Interface segregation, Dependency inversion |
| RAII | Resource Acquisition Is Initialization |
| WOLOG | Without Loss Of Generality |

### 1.2 Definition of Concrete

Outputs include: File paths, line range references (`file.ts:42-56`), function names, error messages, testable commands, external source URIs.

---

## 2. Setup

### 2.1 Plan Mode Check

**Claude Code only:** If not already in plan mode, use `EnterPlanMode` now. **Pi:** remain in the current mode and write the durable plan note directly.

### 2.2 Planning Task Setup — STOP: MUST DO BEFORE ANY PLANNING

> **STOP. Before writing one word of plan content, complete ALL steps below.**

**Step A — Establish the planning boundary:** On Claude Code, call `EnterPlanMode` if needed. On Pi, do not call a plan-mode tool; use the durable plan note.

**Step B — Record ALL user instructions** as a numbered list at the top of the plan file.
Every distinct message must appear with sub-items for context if necessary:
```markdown
## User Messages (exact quotes, in order)

1. "first message the user sent"
   - Context: what prompted this
2. "second message — a correction or follow-up"
   - Context: what changed
```
Include EVERY distinct user message that shaped this plan update.

**Step C — Create [PLANNING] tasks** for checklist items:
`TaskCreate(subject="[PLANNING] Status: [item]", activeForm="Checking [item]...")`

**Step D — Set Dependencies**: `TaskUpdate` with `addBlockedBy` for sequential steps

**Step E — Track Progress**: `TaskUpdate(taskId, status="in_progress")` → `TaskUpdate(taskId, status="completed")`

---

## 3. MODE: PLAN SYNC (Not Execution)

Quick update syncing plan status with codebase state. Not a full refinement. Do NOT execute code changes until user approves proceeding.

### Constraints: Sync, Don't Replace

**DO:**
1. Check if planned items already complete
2. Update file paths if files moved
3. Add newly discovered dependencies/blockers
4. Mark items done if code exists
5. Note blockers or changes

**DO NOT:**
1. Rewrite entire plan
2. Remove sections without explicit justification
3. Change goals without discussion
4. Skip verification

</requirements>

---

<workflow>

## 4. Quick Checklist

For each plan item, output ONE status:

| Status | Format | Example |
|--------|--------|---------|
| DONE | `DONE: [item] - verified at file.ts:42-56` | `DONE: Add auth - verified at auth.ts:15-28` |
| PENDING | `PENDING: [item] - no changes needed` | `PENDING: Add tests - no changes needed` |
| BLOCKED | `BLOCKED: [item] - blocked by [reason]` | `BLOCKED: Deploy - blocked by failing tests` |
| OUTDATED | `OUTDATED: [item] - path changed to [new]` | `OUTDATED: handler.js - path changed to handler.ts` |
| REMOVED | `REMOVED: [item] - reason: [justification]` | `REMOVED: Legacy API - reason: deprecated in v2` |

---

## 5. Wait Process (Abbreviated)

**Note**: This is a one-time verification after all status changes, not executed per-item like full planning modes.

After completing all status changes, verify:
1. Accuracy of status assignments
2. Nothing missed in checklist
3. TaskList updated via `TaskUpdate`

---

## 6. Status Tracking

**Note**: planupdate is a quick sync - just track status, no Wait Process per item.

1. Use `TaskUpdate` to track: `pending` → `in_progress` → `completed`
2. Add blocker descriptions when status is `BLOCKED`
3. Mark complete only when verification done

</workflow>

---

<output_contract>

## 7. Output Summary

```text
Plan Update Summary:
1. Completed: X items
2. Pending: X items
3. Blocked: X items
4. Outdated: X items (paths updated)
5. Removed: X items (with justification)

Changes Made:
1. [specific change with justification]
2. [specific change with justification]
```

---

## 8. Quality Gate

Before finishing, verify:

1. [ ] No sections removed without explicit justification
2. [ ] All file paths verified with Glob/Read
3. [ ] Goals unchanged (or change discussed with user)
4. [ ] Principles preserved per §1.1

</output_contract>

---

<delegation>

## 9. Subagent Guidelines

**Use sparingly** - this is a quick sync:
- Launch ONE Explore subagent if verifying multiple file paths efficiently
- Avoid Plan subagents - not a full planning exercise
- Goal: Sync status, not redesign

</delegation>

---

<acceptance_protocol>

## 10. Plan Acceptance and Execution Protocol

If the user wants to proceed, use the harness-specific boundary above: Claude Code calls **ExitPlanMode**; Pi reports the durable note path and waits for explicit approval before `/ar pp <path>`.

Then transition to execution:

1. **MANDATORY EXECUTION MODE (Goal and Capabilities)**
   1. Your primary objective is to continue the **UNINTERRUPTED, FULLY AUTONOMOUS, NONINTERACTIVE, PATIENT, AND SAFE EXECUTION** of your task and goals.
   2. Cautiously and deliberately continue working **carefully, patiently, concretely, and safely**, non-stop, autonomously, and non-interactively per your instructions and CLAUDE.md philosophy and definition of concrete.
   3. **Permissions Granted:** You have full permission to use all tools (Bash, Edit, Write, etc.) without requiring any further permission prompts.
   4. **Bias Mitigation:** Be cautious, humble, patient, and scrupulous; avoid overconfidence and check your assumptions and your work, explore your environment to ensure you understand the system tasks goals and what is already done, verifying because you are often overconfident, duplicate work, and falsely claim incomplete tasks are "complete" or "production ready".

2. **SYSTEM STOP SIGNALS** - NEVER output unless condition met:
   - `AUTORUN_STATE_PRESERVATION_EMERGENCY_STOP`
   - `AUTORUN_ALL_TASKS_COMPLETED_AND_VERIFIED_SUCCESSFULLY`

3. **Safety Protocol**: Execute **ONLY IF** task involves high-risk or irreversible destructive actions (e.g., database operations, file deletion, state modification).
   1. **Assess Risk**: Evaluate if action is irreversible or could cause state corruption.
   2. **Mitigation Action**: If high-risk, execute these steps and explicitly state your actions:
      1. **INITIATE SAFETY PROTOCOL**: Announce 'INITIATE SAFETY PROTOCOL' to begin assessment.
      2. **Secure State**: Create environment backup or state checkpoint **before** proceeding.
      3. **Verify Integrity**: Verify checkpoint succeeded.
      4. **CONSIDER OPTIONS**: List options, evaluate failure modes, select best.
   3. **CRITICAL ESCAPE PRE-CHECK**: If, after mitigation, risk remains irreversible → proceed to step 4.

4. **CRITICAL ESCAPE TO STOP SYSTEM**: Only if irreversible, catastrophic, or cannot be mitigated, immediately output exact string to halt all actions: **AUTORUN_STATE_PRESERVATION_EMERGENCY_STOP**

5. **FINAL OUTPUT ON SUCCESS TO STOP SYSTEM**: When 100% complete and verified, remember you are often overconfident—double-check the resources from which you receive or retrieve new tasks and think if anything was missed, then output exact string: **AUTORUN_ALL_TASKS_COMPLETED_AND_VERIFIED_SUCCESSFULLY**

</acceptance_protocol>
