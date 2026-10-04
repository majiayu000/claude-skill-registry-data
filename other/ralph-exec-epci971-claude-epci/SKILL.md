---
name: epci:ralph-exec
description: >-
  Executes a single user story from PRD.json with TDD Red-Green cycle.
  Selects next pending story respecting dependencies, implements via @implementer,
  updates PRD with results, and emits RALPH_STATUS block for shell detection.
  Use when: Ralph autonomous loop, story-by-story execution, overnight batch runs.
  Triggers: ralph-exec, execute story, run next story, ralph execute.
  Not for: batch story execution, debugging (use /debug), full features (use /implement).
user-invocable: true
argument-hint: "--prd <path>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Ralph Exec

Execute a single user story from PRD.json with TDD workflow.

## Quick Start

```
/ralph-exec --prd .ralph/my-feature/prd.json
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER execute multiple stories in one invocation
- 🔴 NEVER skip TDD cycle (Red-Green required)
- 🔴 NEVER proceed without valid PRD.json
- 🔴 NEVER modify PRD without RALPH_STATUS emission
- ✅ ALWAYS start with step-00-init.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS emit RALPH_STATUS block at end
- ✅ ALWAYS respect story dependency order
- ⛔ FORBIDDEN skipping the RALPH_STATUS emission
- 🔵 YOU ARE A DISCIPLINED SINGLE-STORY EXECUTOR

## EXECUTION PROTOCOLS:

1. **Load** step-00-init.md
2. **Execute** current step protocols completely
3. **Proceed** to next_step
4. **Complete** until step-02-report.md with RALPH_STATUS

## CONTEXT BOUNDARIES:

- IN scope: Single story execution, TDD cycle, PRD update, status emission
- OUT scope: Multiple stories, debugging, circuit breaker logic, rollback

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    RALPH-EXEC WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 00: INIT                                                   │
│  ├─ Parse --prd argument                                        │
│  ├─ Load and validate PRD.json                                  │
│  └─ Select next story (pending + !passes + deps OK)             │
│     └─ If no story → ABORT with ALL_DONE status                 │
│                                                                  │
│  Step 01: EXECUTE                                                │
│  ├─ Load story context (AC, tasks)                              │
│  ├─ TDD Red-Green cycle via @implementer                        │
│  │   ├─ RED: Write failing test                                 │
│  │   └─ GREEN: Implement to pass                                │
│  └─ Track files_modified                                        │
│                                                                  │
│  Step 02: REPORT                                                 │
│  ├─ Update PRD.json                                             │
│  │   ├─ status, passes, attempts++                              │
│  │   └─ files_modified[], completed_at                          │
│  └─ Emit RALPH_STATUS block                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Steps

| Step | Name | Description | Skippable |
|------|------|-------------|-----------|
| 00 | init | Parse PRD, validate, select next story | No |
| 01 | execute | TDD Red-Green implementation | No |
| 02 | report | Update PRD, emit RALPH_STATUS | No |

## Step Files

- [steps/step-00-init.md](steps/step-00-init.md) — Initialization
- [steps/step-01-execute.md](steps/step-01-execute.md) — TDD Execution
- [steps/step-02-report.md](steps/step-02-report.md) — Report & Status

## Reference Files

- [references/status-block.md](references/status-block.md) — RALPH_STATUS format

## Shared Components Used

- `epci:tdd-enforcer` — TDD cycle enforcement (Red-Green mode)

## Story Selection Algorithm

```
FOR each story IN prd.userStories ORDER BY id:
  IF story.status == "pending" AND story.passes == false:
    deps_satisfied = ALL(dep.passes == true FOR dep IN story.dependencies.depends_on)
    IF deps_satisfied:
      RETURN story
RETURN null  # No story available
```

## RALPH_STATUS Format (Summary)

```
<<<RALPH_STATUS>>>
story_id: {US1}
status: {SUCCESS|FAILURE|BLOCKED|ALL_DONE}
passes: {true|false}
error: {null|"error message"}
files_modified: [{list}]
next_story: {US2|null}
timestamp: {ISO-8601}
<<<END_RALPH_STATUS>>>
```

See [references/status-block.md](references/status-block.md) for complete specification.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| PRD not found | Invalid --prd path | RALPH_STATUS with FAILURE |
| PRD invalid | Schema validation fails | RALPH_STATUS with FAILURE |
| No story available | All done or blocked | RALPH_STATUS with ALL_DONE or BLOCKED |
| Test fails 2x | Implementation issue | RALPH_STATUS with FAILURE |
| Dependency missing | Story blocked | Skip and emit BLOCKED |

## Limitations

This skill does NOT:
- Execute multiple stories at once
- Handle circuit breaker logic (done by ralph.sh)
- Perform rollback on failure
- Run code review or security audit (speed priority)
- Create Feature Documents (handled by /spec)
