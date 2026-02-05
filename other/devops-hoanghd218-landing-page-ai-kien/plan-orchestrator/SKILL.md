---
name: plan-orchestrator
description: Orchestrate execution of multi-phase implementation plans using subagents. Use when executing plans with sub-plans (e.g., 043_MODEL_ALIGNMENT with 043A-043D), managing plan dependencies, tracking checklist progress, or coordinating work across multiple phases. Triggers on phrases like "execute plan", "run the implementation", "start plan 043", "orchestrate", or when a plan file is referenced for execution.
---

# Plan Orchestrator

Coordinate execution of structured implementation plans by delegating phases to subagents while maintaining oversight, tracking progress, and ensuring quality.

## Plan Structure Recognition

Plans follow this hierarchy:

```
Parent Plan (e.g., 043_MODEL_ALIGNMENT.md)
├── Overview, Goals, Non-Goals
├── Sub-Plan references (043A, 043B, 043C, 043D)
├── Execution order / dependency graph
├── Breaking changes / rollback strategy
└── Master checklist

Sub-Plan (e.g., 043A_CONFIG_AND_STUBS.md)
├── Overview with prereqs and blockers
├── Phases with numbered sections (0.1, 1.1, 1.2...)
├── File summaries (CREATE/MODIFY/VERIFY actions)
├── Verification commands
└── Phase checklists
```

## Orchestration Workflow

### 1. Plan Analysis

When given a plan to execute:

1. Read the parent plan to understand scope, goals, and sub-plan order
2. Build dependency graph from prereqs/blockers in each sub-plan
3. Identify the current state (check which checklist items are done)
4. Present execution plan to user for approval

**Output format:**
```
## Execution Plan: [Plan Name]

**Goal:** [One-line summary]

**Sub-plans in order:**
1. 043A: Config & Stubs (no blockers)
2. 043B: Shared Models (blocked by: 043A)
3. 043C: Backend Services (blocked by: 043B)
4. 043D: Frontend Alignment (blocked by: 043C)

**Current state:** [X of Y checklist items complete]

Ready to begin with 043A?
```

### 2. Subagent Delegation

For each sub-plan or phase, spawn a subagent with:

```
claude --dangerously-skip-permissions "Execute phase [X.Y] of [sub-plan]:

CONTEXT:
- Parent plan: [name]
- This sub-plan: [name]  
- Phase goal: [from plan]
- Prereqs verified: [list]

TASK:
[Paste the specific phase section from the plan]

CONSTRAINTS:
- Only modify files listed in the phase
- Run verification commands before reporting complete
- Report blockers immediately

OUTPUT:
When done, provide:
1. Files changed (with brief description)
2. Verification results
3. Any issues or deviations from plan
4. Checklist items completed"
```

### 3. Progress Tracking

Maintain a progress file during execution:

```markdown
# Progress: [Plan Name]
Started: [timestamp]
Status: IN_PROGRESS

## 043A: Config & Stubs
- [x] Phase 0: Configuration (completed [time])
- [x] Phase 1: WireMock Stubs (completed [time])
- Verification: PASSED

## 043B: Shared Models  
- [x] Phase 2: Extend Shared Models (completed [time])
- [ ] Phase 3: Update Service DTOs (in progress)

## Blockers
- None currently

## Notes
- [Any deviations or decisions made]
```

### 4. Review Checkpoints

After each sub-plan completes:

1. **Verify outputs** - Run the verification commands from the plan
2. **Check for regressions** - Run `pnpm nx run-many -t build` and `pnpm nx run-many -t test`
3. **Review changes** - Use `git diff` to review what changed
4. **Update progress** - Mark checklist items complete
5. **Decide continuation** - Ask user before proceeding to next sub-plan if significant

### 5. Handling Failures

When a subagent reports issues:

1. **Analyze the failure** - Is it a blocker or recoverable?
2. **Check dependencies** - Did a prerequisite actually complete?
3. **Determine action:**
   - Minor issue → Fix and continue
   - Plan deviation needed → Propose modification, get approval
   - Blocker → Stop, report status, suggest rollback if needed

## Subagent Prompt Templates

### For Phase Execution

```
You are executing Phase [X.Y]: [Phase Name] of [Sub-Plan Name].

## Context
Parent plan: [parent]
Prerequisites completed: [list]
Your phase goal: [goal from plan]

## Your Task
[Paste exact phase content from plan including file list and implementation details]

## Rules
1. Only touch files listed in this phase
2. Follow the implementation guidance exactly
3. Run verification commands before completing
4. If you encounter unexpected issues, STOP and report

## Completion Report
Provide when done:
- Files modified: [list with 1-line descriptions]
- Tests run: [results]
- Verification: [PASSED/FAILED with details]
- Checklist items done: [list]
- Issues: [any problems or deviations]
```

### For Review/Verification

```
Review the changes made in Phase [X.Y] of [Sub-Plan].

## Expected Changes
[List from plan's file summary]

## Verification Steps
[From plan's verification section]

## Your Task
1. Verify all expected files were modified
2. Run the verification commands
3. Check for unintended changes
4. Confirm the phase checklist is satisfiable

Report: APPROVED or NEEDS_REVISION with specifics.
```

## Execution Modes

### Full Auto Mode
Execute all sub-plans sequentially with minimal user interaction:
```
Execute plan 043 in auto mode
```
- Runs all phases
- Only stops on failures or user-defined checkpoints
- Provides summary at end

### Supervised Mode (Default)
Pause for approval between sub-plans:
```
Execute plan 043
```
- Presents each sub-plan before execution
- Shows changes after each sub-plan
- Asks for approval to continue

### Single Sub-Plan Mode
Execute just one sub-plan:
```
Execute only 043B from plan 043
```
- Verifies prerequisites are met
- Executes just that sub-plan
- Reports completion

### Resume Mode
Continue from where execution stopped:
```
Resume plan 043
```
- Reads progress file
- Identifies next incomplete phase
- Continues from there

## Commands Reference

| Command | Description |
|---------|-------------|
| `execute plan [name]` | Start supervised execution |
| `execute plan [name] --auto` | Full auto mode |
| `execute [sub-plan] only` | Single sub-plan |
| `resume plan [name]` | Continue from progress |
| `status plan [name]` | Show current progress |
| `verify plan [name]` | Run all verification steps |
| `rollback plan [name]` | Revert all changes |

## Best Practices

1. **Always read the full plan first** - Understand scope before executing
2. **Verify prerequisites** - Don't skip dependency checks
3. **Commit between sub-plans** - `git commit` after each sub-plan for easy rollback
4. **Keep progress updated** - Track in real-time for resume capability
5. **Run tests frequently** - Catch issues early
6. **Document deviations** - Note any changes from the original plan

## Integration with Git

After each sub-plan:
```bash
git add -A
git commit -m "feat: complete [sub-plan name] - [brief description]"
```

If rollback needed:
```bash
git log --oneline  # Find commit before plan started
git reset --hard [commit]
```