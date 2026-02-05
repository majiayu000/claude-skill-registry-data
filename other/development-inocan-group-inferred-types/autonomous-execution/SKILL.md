---
name: autonomous-execution
description: Execute implementation plans or backlog items autonomously with shared-context architecture for maximum accuracy
---

# Autonomous Execution

Execute implementation plans or backlog items to completion without human intervention, using a shared-context architecture that keeps requirements fresh in the main agent's mind.

## Core Principle

**Use context budget for accuracy, not efficiency.**

The main agent maintains full context (requirements + execution history + code) throughout execution. This prevents requirement fragmentation and enables immediate verification against original requirements.

**Context budget per task:** ~10k tokens (requirement doc + execution log + changed code)
**Typical execution:** 7 tasks = 70k tokens, well under 200k budget

## When to Use

**Use for:**
- Implementation plans with 5+ tasks
- Backlog items with multiple steps
- Multi-hour implementations
- Work when human review isn't available

**Don't use for:**
- Single tasks (just implement directly)
- Exploratory work without clear requirements
- Work needing real-time human oversight
- Ambiguous requirements

## Prerequisites

- Dedicated worktree (isolated environment)
- Requirement document (design doc or backlog item)
- Implementation plan OR backlog item with Proposed Solution section

## Process Overview

```
Setup:
1. Verify isolation, load requirements
2. Create state file + execution log
3. Extract tasks, create TodoWrite

Main Loop (per task):
1. Re-read requirement doc (keep fresh)
2. Dispatch implementation subagent (with full requirement)
3. Main agent reads changed code
4. Main agent verifies against requirement
5. Loop back for fixes if needed
6. Update logs, mark complete

Completion:
1. Write final report with requirements traceability
2. Commit and cleanup
```

## Setup Phase

### 1. Verify Worktree Isolation

```bash
git branch --show-current  # Must NOT be main/master
```

### 2. Load Requirement Document

**For backlog items:**
- Read `docs/backlog/BX-name.md`
- Problem section = WHY (design intent)
- Proposed Solution section = requirements

**For implementation plans:**
- Read design doc (WHY)
- Read implementation plan (tasks)

**Store paths:**
- `REQUIREMENT_DOC` = path to requirement source
- `IMPLEMENTATION_PLAN` = path to plan (same as requirement for backlog items)

### 3. Create State File

```bash
mkdir -p tmp
cat > tmp/.autonomous-execution-state.json << EOF
{
  "skill": "autonomous-execution",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "requirement_doc": "${REQUIREMENT_DOC}",
  "implementation_plan": "${IMPLEMENTATION_PLAN}",
  "current_task": 1,
  "total_tasks": ${TOTAL_TASKS},
  "status": "in_progress"
}
EOF
```

### 4. Create Execution Log

```bash
cat > tmp/execution-log.md << EOF
# Execution Log: [Feature Name]

**Started:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Requirement:** ${REQUIREMENT_DOC}
**Plan:** ${IMPLEMENTATION_PLAN}

## Context
[Brief summary of what we're building and why]

## Task 1: [Name] - PENDING
EOF
```

### 5. Create TodoWrite

Extract tasks from plan/backlog item, create TodoWrite with all tasks.

## Main Execution Loop

### Step 1: Re-Read Requirement (Every Task)

**Before EVERY task, re-read the requirement document.**

```bash
# Main agent: Read ${REQUIREMENT_DOC} to refresh context
# Focus on requirements relevant to this task
```

**Why:** Prevents requirement fragmentation. Original requirement stays fresh in main agent's mind.

**Context cost:** 1-3k tokens per task

### Step 2: Dispatch Implementation Subagent

**Main agent provides FULL requirement + task context:**

```
Task tool with general-purpose agent:

description: "Implement Task N: [name]"

prompt: |
  Implement Task N: [task description from plan]

  **REQUIREMENT DOCUMENT:**
  Read: ${REQUIREMENT_DOC}

  This is the source of truth. Your task implements part of these requirements.

  **TASK CONTEXT:**
  - Prior work: [summary from execution log]
  - Your task: [task description]
  - Connection to requirement: [why this task matters]

  **YOUR JOB:**
  1. Read requirement document for full context
  2. Implement your task
  3. Follow TDD if specified
  4. Commit your work
  5. Report back:
     - What you implemented (1-2 sentences)
     - Files changed (with line counts)
     - Tests added/modified
     - Any issues

  **CRITICAL:**
  - If requirement conflicts with task, requirement wins
  - Document deviations in commit message
  - Commit working code even if incomplete

  Context:
  - Requirement: ${REQUIREMENT_DOC}
  - Execution log: tmp/execution-log.md
```

**Key point:** Subagent gets requirement doc path and explicit instruction to read it.

### Step 3: Main Agent Reads Changed Code

**After implementation subagent reports:**

```bash
# Main agent:
# 1. Read implementation report
# 2. Read files that were changed (Use Read tool)
# 3. Load changed code into context
```

**Example:**
```
Report says changed:
- tg_bot/parser.py
- tests/test_parser.py

Main agent:
- Read tg_bot/parser.py (scan implementation)
- Read tests/test_parser.py (verify coverage)
```

**Context cost:** 2-10k tokens per task

**Why this matters:** Main agent holds requirement + code in same context. Can directly verify match.

### Step 4: Main Agent Verifies Against Requirement

**Main agent has in context:**
- Requirement document (from step 1)
- Changed code (from step 3)
- Task description

**Verification checklist:**

```markdown
## 1. TESTS
- Run test suite: `pytest -q` (or project command)
- Check pass/fail counts
- Verify test coverage increased for new features

## 2. REQUIREMENT MATCH
- Does code implement what requirement specifies?
- Compare specific requirement text to code implementation
- Example: Requirement: "filter by status='ready'"
          Code: WHERE status = 'ready' ✓
- Any requirement details missing?

## 3. INTEGRATION
- Connects to previous tasks?
- Provides what future tasks need?
- Can trace execution end-to-end?

## 4. COMPLETENESS
- Error handling present?
- Edge cases covered?
- Not just happy path?

## 5. CODE QUALITY
- Follows project conventions?
- Clear and maintainable?
- Any obvious issues?
```

**If all checks pass:** → Step 6 (update logs)

**If any check fails:** → Step 5 (create feedback, loop back)

### Step 5: Loop Back for Fixes (If Needed)

**Main agent creates specific feedback:**

```markdown
Issues found in Task N:

1. Tests: [X passed, Y failed - paste failures]
2. Requirement mismatch:
   - Requirement says: "[quote exact text]"
   - Code does: "[what's actually implemented]"
   - Missing: "[specific gap]"
3. Integration gap: "[specific missing connection]"
4. Completeness: "[missing error handling]"
5. Code quality: "[issues with file:line]"
```

**Dispatch fix subagent:**

```
Task tool:

description: "Fix issues in Task N"

prompt: |
  Fix issues in Task N: [name]

  **ISSUES TO FIX:**
  [Paste main agent's feedback above]

  **REQUIREMENT CONTEXT:**
  The requirement at ${REQUIREMENT_DOC} specifies:
  [Quote relevant requirement that was missed]

  Your implementation needs to match this exactly.

  **YOUR JOB:**
  1. Fix ALL issues listed
  2. Priority: tests → requirements → integration → completeness → quality
  3. Commit fixes
  4. Report what was fixed

  Context:
  - Requirement: ${REQUIREMENT_DOC}
  - Execution log: tmp/execution-log.md
```

**After fix:** Loop back to step 3 (read code, verify again)

### Step 6: Update Logs and Mark Complete

**Main agent updates execution log:**

```bash
cat >> tmp/execution-log.md << EOF

**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Status:** ✅ Complete
**Files changed:** [list]
**Tests:** [X passed, Y failed]
**Verification:**
- Requirement match: ✓
- Integration: ✓
- Completeness: ✓
**Iterations:** [1 = clean, 2+ = fixes needed]
**Key decisions:** [if any]

## Task $((N+1)): [Name] - PENDING
EOF
```

**Update state file:**
```bash
jq '.current_task += 1' tmp/.autonomous-execution-state.json > tmp/.state.tmp
mv tmp/.state.tmp tmp/.autonomous-execution-state.json
```

**Mark TodoWrite task complete**

**Verify commit exists** (subagent should have committed)

### Step 7: Continue

Increment state, repeat from step 1 for next task.

## Completion Phase

### 1. Write Final Report

**Main agent creates final report:**

```markdown
# [Feature Name] - Final Report

**Completed:** [timestamp]
**Requirement:** ${REQUIREMENT_DOC}
**Duration:** [time]
**Tasks:** [X completed]
**Test progression:** [baseline → final]

## Summary
[What was built, key decisions, outcome]

## Requirements Verification

| Requirement | Implementation | Evidence |
|-------------|----------------|----------|
| [Req text] | ✅ Complete | [file:line] |
| [Req text] | ✅ Complete | [file:line] |

## Key Decisions
1. **[Decision]:** [rationale]

## Task Completion

| Task | Status | Files | Tests | Iterations |
|------|--------|-------|-------|------------|
| 1. [Name] | ✅ | [count] | [pass] | 1 |

## Recommendations
- [Future work or monitoring]
```

**Location:** `docs/plans/YYYY-MM-DD-[feature]-final-report.md`

### 2. Commit and Cleanup

```bash
# Commit final report (permanent deliverable)
git add docs/plans/*-final-report.md
git commit -m "docs: [feature] autonomous execution final report"

# Cleanup tmp/ (gitignored, ephemeral)
rm -rf tmp/
```

## Resume Capability

**If interrupted:**

1. Check for `tmp/.autonomous-execution-state.json`
2. Read `current_task` number
3. Read `tmp/execution-log.md` for context
4. Continue from current task

**State file provides:** Current position, requirement/plan paths, start time

**Execution log provides:** What's complete, decisions made, context for next task

## Why This Architecture Works

### Shared Context Pattern

```
Main Agent Context:
├── Requirement document (re-read each task)
├── Execution log (growing history)
├── Changed code (after implementation)
└── Verification (against requirement)

Result: Direct requirement → code verification, no fragmentation
```

### Compared to Alternative Approaches

**Minimal main agent (failed approach):**
- Main agent summarizes requirements once
- Subagents work from task summaries
- Verification subagent compares to task (not requirement)
- Result: Requirement details lost through 3-4 hops

**Shared context (this approach):**
- Main agent keeps requirement loaded
- Implementation subagent gets full requirement
- Main agent verifies code directly against requirement
- Result: Requirement stays fresh, immediate verification

### Context Budget

**Per task (typical):**
- Requirement doc: 2k
- Execution log: 3k
- Changed code: 5k
- **Total: ~10k tokens**

**For 7 tasks:** 70k tokens (leaves 130k available)

**What the 70k buys:**
- ✅ Requirements don't fragment
- ✅ Direct verification (requirement + code in same context)
- ✅ Immediate mismatch detection
- ✅ Faster (no verification subagent overhead)

## Common Pitfalls

**Don't:**
- Skip re-reading requirement ("I remember it")
- Let subagent verify (they lack requirement context)
- Optimize for context efficiency over accuracy
- Summarize requirements to save tokens

**Do:**
- Re-read requirement before each task
- Read code after implementation
- Hold requirement + code in same context
- Use the 200k token budget for accuracy

## Success Metrics

**Expected outcomes:**
- Zero requirement misses (requirement in context during verification)
- Faster iteration (direct verify, no verification subagent)
- Clean requirements traceability (each requirement → code evidence)

**Red flags:**
- Still missing requirements (means verification process broken)
- Context exhaustion (200k wasn't enough - very rare)
- Slower than manual (means overhead isn't justified)

## Related Skills

- **using-git-worktrees** - Create isolated workspace (prerequisite)
- **writing-plans** - Create implementation plans this skill executes
- **systematic-debugging** - When implementation subagent gets stuck
- **requesting-code-review** - After autonomous execution completes

---

**Remember:** Accuracy > efficiency. Use context to keep requirements fresh. Verify directly with requirement in hand.
