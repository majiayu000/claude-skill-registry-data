---
name: review-loop
description: Use when code changes need multi-pass automated review before merge. Use when preparing branch for PR. Use when thorough code quality check needed.
---

# MANDATORY FIRST ACTION

**STOP. Before ANY other tool call, you MUST call TaskCreate.**

If you're about to:
- Run setup.sh → STOP. TaskCreate first.
- Dispatch reviewer → STOP. TaskCreate first.
- Read any file → STOP. TaskCreate first.

## Step 1: Create Tasks

First, check if `code-simplifier:code-simplifier` subagent is available in your Task tool's subagent_type list.

**If code-simplifier IS available:**
```
TaskCreate(subject: "Simplify code", description: "Run code-simplifier before review", activeForm: "Simplifying code")
TaskCreate(subject: "Iteration 1: Review", description: "Review and fix", activeForm: "Running iteration 1")
TaskCreate(subject: "Iteration 2: Review", description: "Review and fix", activeForm: "Running iteration 2")
TaskCreate(subject: "Iteration 3: Review", description: "Review and fix", activeForm: "Running iteration 3")
TaskCreate(subject: "Iteration 4: Review", description: "Review and fix", activeForm: "Running iteration 4")
```

Then set dependencies (ITER1 blocked by SIMPLIFY):
```
TaskUpdate(taskId: ITER1, addBlockedBy: [SIMPLIFY])
TaskUpdate(taskId: ITER2, addBlockedBy: [ITER1])
TaskUpdate(taskId: ITER3, addBlockedBy: [ITER2])
TaskUpdate(taskId: ITER4, addBlockedBy: [ITER3])
TaskUpdate(taskId: SIMPLIFY, status: "in_progress")
```

**If code-simplifier is NOT available:**
```
TaskCreate(subject: "Iteration 1: Review", description: "Review and fix", activeForm: "Running iteration 1")
TaskCreate(subject: "Iteration 2: Review", description: "Review and fix", activeForm: "Running iteration 2")
TaskCreate(subject: "Iteration 3: Review", description: "Review and fix", activeForm: "Running iteration 3")
TaskCreate(subject: "Iteration 4: Review", description: "Review and fix", activeForm: "Running iteration 4")
```

Then set dependencies and start:
```
TaskUpdate(taskId: ITER2, addBlockedBy: [ITER1])
TaskUpdate(taskId: ITER3, addBlockedBy: [ITER2])
TaskUpdate(taskId: ITER4, addBlockedBy: [ITER3])
TaskUpdate(taskId: ITER1, status: "in_progress")
```

**Report to user:** "code-simplifier plugin not installed. Recommended: `claude plugin install code-simplifier@anthropic-official` from https://github.com/anthropics/claude-plugins-official"

**CHECKPOINT: Have you created tasks? If NO → do it now. If YES → continue.**

---

# Review Loop

You are an ORCHESTRATOR. You dispatch subagents. You do NOT touch code.

## Process

```dot
digraph review_loop {
    rankdir=TB;
    "TaskCreate" [shape=box, style=bold];
    "Get REVIEW_DIR/TARGET_BRANCH" [shape=box];
    "code-simplifier available?" [shape=diamond];
    "Dispatch code-simplifier" [shape=box];
    "TaskList → find unblocked" [shape=box];
    "Dispatch reviewer" [shape=box];
    "Invoke /fix skill" [shape=box];
    "TaskUpdate completed" [shape=box];
    "Iteration < 4?" [shape=diamond];
    "Commit" [shape=box];

    "TaskCreate" -> "Get REVIEW_DIR/TARGET_BRANCH";
    "Get REVIEW_DIR/TARGET_BRANCH" -> "code-simplifier available?";
    "code-simplifier available?" -> "Dispatch code-simplifier" [label="yes"];
    "code-simplifier available?" -> "TaskList → find unblocked" [label="no"];
    "Dispatch code-simplifier" -> "TaskList → find unblocked";
    "TaskList → find unblocked" -> "Dispatch reviewer";
    "Dispatch reviewer" -> "Invoke /fix skill";
    "Invoke /fix skill" -> "TaskUpdate completed";
    "TaskUpdate completed" -> "Iteration < 4?";
    "Iteration < 4?" -> "TaskList → find unblocked" [label="yes"];
    "Iteration < 4?" -> "Commit" [label="no"];
}
```

## Step 2: Get Config

If args provided, use them. Otherwise:
```
~/.claude/plugins/cache/onsails-cc/review-loop/*/skills/review-loop/scripts/setup.sh
```

## Step 2.5: Code Simplification (if available)

If `code-simplifier:code-simplifier` subagent is available, dispatch it to simplify code changes between current branch and TARGET_BRANCH:
```
Task(subagent_type: "code-simplifier:code-simplifier",
     prompt: "Simplify code changes between HEAD and ${TARGET_BRANCH}. Focus only on files modified in this branch.")
TaskUpdate(taskId: SIMPLIFY, status: "completed")
```

## Step 3: Each Iteration

1. `TaskList` → find first unblocked task
2. Dispatch reviewer:
   ```
   Task(subagent_type: "review-loop:local-reviewer",
        prompt: "OUTPUT: ${REVIEW_DIR}/iterN.md\nTARGET: ${TARGET_BRANCH}")
   ```
3. Invoke fix: `Skill(skill: "review-loop:fix", args: "${REVIEW_DIR}/iterN.md")`
4. `TaskUpdate(taskId: CURRENT, status: "completed")`
5. Repeat

## Step 4: Completion

After 4+ iterations with no critical/major:
```bash
git add -A && git commit -m "fix: address review issues (N iterations)"
```

---

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I know what review-loop does" | You pattern-matched. Read the skill. TaskCreate FIRST. |
| "Let me run setup first" | NO. TaskCreate comes before setup.sh |
| "I'll create tasks after starting" | NO. Tasks FIRST, always. |
| "Two iterations enough" | NO. Minimum 4. |
| "I'll fix this quickly" | NO. /fix skill does fixes. |
| "Would you like me to..." | NO. Never ask. Execute. |
| "Skip code-simplifier, it's optional" | Check availability first. If available, run it. |

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Dispatching reviewer without tasks created → STOP
- Running setup.sh as first action → STOP
- Using Read/Edit/Grep on code → STOP
- Fixing issues directly → STOP
- Asking permission → STOP
- Skipping code-simplifier without checking availability → STOP

**All mean: You skipped TaskCreate. Go back to MANDATORY FIRST ACTION.**

## Iron Rules

1. TaskCreate BEFORE anything else
2. Check code-simplifier availability, run if present
3. MINIMUM 4 review iterations
4. ONLY Task and Skill tools on code
5. SEQUENTIAL iterations
6. /fix skill does fixes, not you
7. Never ask permission
