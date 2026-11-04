---
name: subagent-execution
description: "Execute implementation plans using subagents. Three modes: single task, batch (sequential), parallel. Two-stage review for every task."
---

# Subagent Execution

## Overview

Execute implementation plans using fresh subagents. Each task gets a new session. Every task goes through two-stage review (spec compliance + code quality).

**Core principle:** One subagent per task + two-stage review = high quality, fast iteration.

## 3 Execution Modes

### Mode A -- Single Task Execution

Delegate a single task to a subagent.

```
1. Prepare task text (full context + requirements)
2. Spawn an implementer subagent
3. When subagent completes, run spec review
4. When spec passes, run code quality review
5. Update task status
```

### Mode B -- Batch (Sequential Execution)

Execute tasks from a plan file in order. Checkpoint between each task.

```
1. Read the plan file, extract all tasks
2. Create $AEK_HOME/tasks/current-plan.md (for tracking)
3. Apply Mode A for each task
4. Update task status after each task
5. Run final review when all tasks complete
```

### Mode C -- Parallel Execution

Run 2+ independent tasks simultaneously.

```
1. Verify independence (no shared files/state)
2. Spawn separate subagent for each task
3. Collect results when all subagents complete
4. Run spec + quality review for each
5. Resolve merge conflicts if any
```

**Do NOT use parallel when:**
- Tasks modify the same files
- Tasks have sequential dependencies
- Task outputs depend on each other

## Task Tracking

Use `$AEK_HOME/tasks/current-plan.md` for plan tracking:

```markdown
# Plan: [Feature Name]
Date: YYYY-MM-DD
Source: [plan file path]

## Task 1: [Name] -- COMPLETED
- Implementer: session_xxx
- Review: PASSED
- Commit: abc1234

## Task 2: [Name] -- IN PROGRESS
- Implementer: session_yyy

## Task 3: [Name] -- PENDING
```

## Process Flow (Mode B -- Detailed)

```
Read plan file
       |
       v
Extract all tasks (full text + context)
       |
       v
Create current-plan.md
       |
       v
[For each task]
       |
       v
Spawn implementer subagent
       |
       v
Subagent asking questions? --YES--> Answer, provide context
       |                                    |
       NO                                   v
       |                         Subagent implements
       v                                    |
Subagent implements <----------------------+
       |
       v
Spawn spec reviewer subagent
       |
       v
Spec compliant? --NO--> Implementer fixes --> re-run spec review
       |
       YES
       |
       v
Spawn code quality reviewer subagent
       |
       v
Quality approved? --NO--> Implementer fixes --> re-run quality review
       |
       YES
       |
       v
Mark task as COMPLETED
       |
       v
More tasks? --YES--> Next task
       |
       NO
       |
       v
Final code review (entire implementation)
       |
       v
Pass through verification-gate
```

## Subagent Prompts

### Implementer Subagent

```
[spawn subagent]:

task="Implement Task N: [task name]

[FULL task text -- do not make the subagent read files, provide everything]

## Context
[Where this task fits, dependencies, architecture]

## Before You Start
If you have questions about requirements or approach, ASK FIRST.

## Task
1. Implement exactly what the spec says
2. Write tests (TDD)
3. Verify
4. Commit
5. Self-review
6. Report what was done"

model="[your model]"
```

### Spec Reviewer Subagent

```
[spawn subagent]:

task="Spec Compliance Review -- Task N

## What Was Requested
[FULL task requirements]

## Implementer's Claim
[From their report]

## CRITICAL: Do NOT Trust the Report
The implementer may have rushed. Verify everything INDEPENDENTLY.
- Do not accept their claims at face value
- Read the actual code
- Compare requirements line by line
- Look for missing parts, look for extra features

Report: PASS -- Spec compliant OR FAIL -- Issues [list]"

model="[your model]"
```

### Code Quality Reviewer Subagent

```
[spawn subagent]:

task="Code Quality Review -- Task N

## What Was Implemented
[Summary]

## Checklist
- OWASP Top 10 security
- Clean code principles
- Test quality (tests real behavior, not mocks)
- Error handling appropriateness
- Naming conventions
- YAGNI -- any unnecessary complexity?

Report: Strengths, Issues (Critical/Important/Minor), Verdict"

model="[your model]"
```

## When a Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Do not rush them -- good questions lead to good results

## When a Reviewer Finds Issues

1. The implementer (same subagent) fixes the issues
2. The reviewer reviews again
3. Repeat until approved
4. Do NOT skip the re-review

## Red Flags

**Never:**
- Skip reviews (spec OR quality)
- Proceed with unfixed issues
- Run multiple implementer subagents in parallel on dependent tasks
- Make the subagent read the plan file (PROVIDE the full text)
- Send a subagent without context
- Ignore subagent questions
- Accept "approximately compliant" (reviewer found issues = not done)
- **Start code quality review before spec review passes** (wrong order)
- Move to the next task while the current review has open issues

## Integration

**Required skills:**
- **`structured-brainstorming`** -- Creates the plan that this skill executes
- **`tdd-workflow`** -- Subagents follow TDD
- **`verification-gate`** -- Final verification when all tasks complete
- **`systematic-debugging`** -- When a subagent hits an error
