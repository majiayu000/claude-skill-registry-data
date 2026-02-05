---
name: state-transition
description: Safely transition task state with validation and prerequisite checks
allowed-tools: Bash, Read, Write
---

# State Transition Skill

**Purpose**: Safely transition task.json state with automatic prerequisite validation and proper timestamp tracking.

**Performance**: Reduces state transition errors, ensures prerequisites met

## When to Use This Skill

### ✅ Use state-transition When:

- Need to transition task to new state
- Want automatic prerequisite validation
- Ensuring state machine compliance
- Recording state transition timestamps

### ❌ Do NOT Use When:

- State already correct
- Prerequisites not yet met (will fail validation)
- Task doesn't exist yet
- Working outside task protocol

## What This Skill Does

### 1. Validates Current State

```bash
# Checks task in expected current state
# Prevents invalid transitions (e.g., INIT → VALIDATION)
```

### 2. Checks Prerequisites

```bash
# For each state transition, validates:
- Required files exist
- Required flags present
- Required conditions met
```

### 3. Updates State

```bash
# Updates task.json:
jq '.state = "NEW_STATE" | .transitions += [{
  "from": "OLD_STATE",
  "to": "NEW_STATE",
  "timestamp": "2025-11-11T12:34:56-05:00"
}]' task.json > tmp.json
mv tmp.json task.json
```

### 4. Records Transition

```bash
# Logs transition history
# Tracks timestamps for metrics
# Enables state machine audit
```

## Usage

### Basic State Transition

```bash
# Transition from INIT to CLASSIFIED
TASK_NAME="implement-formatter-api"
FROM_STATE="INIT"
TO_STATE="CLASSIFIED"

/workspace/main/.claude/scripts/state-transition.sh \
  --task "$TASK_NAME" \
  --from "$FROM_STATE" \
  --to "$TO_STATE"
```

### With Automatic Validation

```bash
# Skill automatically validates prerequisites
TASK_NAME="implement-formatter-api"
TO_STATE="SYNTHESIS"

/workspace/main/.claude/scripts/state-transition.sh \
  --task "$TASK_NAME" \
  --to "$TO_STATE" \
  --auto-validate true
```

## State Machine

### Valid State Flow

```
INIT
  ↓
CLASSIFIED
  ↓
REQUIREMENTS
  ↓
SYNTHESIS
  ↓
IMPLEMENTATION
  ↓
VALIDATION
  ↓
AWAITING_USER_APPROVAL
  ↓
COMPLETE
  ↓
CLEANUP
```

### State Descriptions

**INIT**: Task initialized, worktrees created
**CLASSIFIED**: Task categorized, ready for requirements
**REQUIREMENTS**: Stakeholder agents gathering requirements
**SYNTHESIS**: Main agent synthesizing implementation plan
**IMPLEMENTATION**: Stakeholder agents implementing features
**VALIDATION**: Running build/tests/checks
**AWAITING_USER_APPROVAL**: Waiting for user to approve changes
**COMPLETE**: Merged to main, ready for cleanup
**CLEANUP**: Branches/worktrees removed, task archived

## Prerequisites by Transition

### INIT → CLASSIFIED

```bash
Prerequisites:
- task.json exists
- task.md exists
- All worktrees created
- All branches created

Validation:
ls /workspace/tasks/{task}/task.json
ls /workspace/tasks/{task}/task.md
git worktree list | grep {task}
```

### CLASSIFIED → REQUIREMENTS

```bash
Prerequisites:
- Task classified (task.md has description)
- All stakeholder agents invoked

Validation:
grep -q "## Requirements" /workspace/tasks/{task}/task.md
```

### REQUIREMENTS → SYNTHESIS

```bash
Prerequisites:
- All 3 requirement reports exist:
  * {task}-architect-requirements.md
  * {task}-tester-requirements.md
  * {task}-formatter-requirements.md
- All agents completed successfully

Validation:
verify-requirements-complete skill
```

### SYNTHESIS → IMPLEMENTATION

```bash
Prerequisites:
- Implementation plan in task.md
- User approval flag exists:
  * user-approved-synthesis.flag

Validation:
grep -q "## Implementation Plan" /workspace/tasks/{task}/task.md
test -f /workspace/tasks/{task}/user-approved-synthesis.flag
```

### IMPLEMENTATION → VALIDATION

```bash
Prerequisites:
- All agents completed implementation
- All agent work merged to task branch

Validation:
jq -r '.agents | to_entries | .[] | select(.value.merged == false)' task.json
# Should return empty
```

### VALIDATION → AWAITING_USER_APPROVAL

```bash
Prerequisites:
- Build succeeds
- All tests pass
- No Checkstyle violations
- No PMD violations

Validation:
mvn clean verify
```

### AWAITING_USER_APPROVAL → COMPLETE

```bash
Prerequisites:
- User approval flag exists:
  * user-approved-changes.flag
- Changes merged to main

Validation:
test -f /workspace/tasks/{task}/user-approved-changes.flag
git log main --oneline | grep -q {task}
```

### COMPLETE → CLEANUP

```bash
Prerequisites:
- Task merged to main
- todo.md updated (task marked complete)
- changelog.md updated

Validation:
git log main -1 --grep={task}
grep -q "\[x\] {task}" /workspace/main/todo.md
grep -q "{task}" /workspace/main/changelog.md
```

## Workflow Integration

### Typical State Progression

```markdown
1. Task initialization
   [task-init skill]
   → INIT state

2. Classify task
   [state-transition: INIT → CLASSIFIED]

3. Gather requirements
   [gather-requirements skill]
   → REQUIREMENTS state

4. Verify requirements
   [verify-requirements-complete skill]

5. Synthesize plan
   [synthesize-plan skill]
   → SYNTHESIS state

6. Get approval
   [checkpoint-approval skill]
   [state-transition: SYNTHESIS → IMPLEMENTATION]

7. Implement features
   [Invoke agents]
   → IMPLEMENTATION state

8. Validate implementation
   [Run build/tests]
   → VALIDATION state

9. Get approval
   [checkpoint-approval skill]
   [state-transition: AWAITING_USER_APPROVAL → COMPLETE]

10. Archive task
    [archive-task skill]
    [state-transition: COMPLETE → CLEANUP]

11. Cleanup
    [task-cleanup skill]
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "State transition successful",
  "task_name": "implement-formatter-api",
  "from_state": "SYNTHESIS",
  "to_state": "IMPLEMENTATION",
  "prerequisites_met": true,
  "transition_timestamp": "2025-11-11T12:34:56-05:00",
  "duration_in_state": "PT15M30S",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

**Or if prerequisites not met**:

```json
{
  "status": "failed",
  "message": "Prerequisites not met for transition",
  "task_name": "implement-formatter-api",
  "from_state": "SYNTHESIS",
  "to_state": "IMPLEMENTATION",
  "prerequisites_met": false,
  "missing_prerequisites": [
    "user-approved-synthesis.flag not found"
  ],
  "error": "Cannot transition without user approval",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Invalid Transitions

### Skipping States

```bash
❌ INVALID: INIT → SYNTHESIS
Reason: Must go through CLASSIFIED, REQUIREMENTS first

✅ VALID: INIT → CLASSIFIED → REQUIREMENTS → SYNTHESIS
```

### Backward Transitions

```bash
❌ INVALID: VALIDATION → IMPLEMENTATION
Reason: Cannot go backward (use re-invoke agents instead)

✅ VALID: Stay in VALIDATION, re-invoke agents for fixes
```

### Duplicate Transitions

```bash
❌ WARNING: SYNTHESIS → SYNTHESIS
Reason: Already in target state (no-op)

✅ VALID: Check current state before transitioning
```

## Safety Features

### Precondition Validation

- ✅ Verifies task exists
- ✅ Checks task.json readable/writable
- ✅ Validates from_state matches current
- ✅ Confirms to_state is valid next state

### Prerequisite Enforcement

- ✅ Checks all required files exist
- ✅ Validates all required flags present
- ✅ Confirms all required conditions met
- ✅ Blocks transition if prerequisites missing

### State History Tracking

- ✅ Records all transitions
- ✅ Timestamps each transition
- ✅ Tracks duration in each state
- ✅ Enables metrics and auditing

### Error Handling

On any error:
- Does not modify task.json
- Reports specific prerequisite failures
- Returns JSON with error details
- Provides recovery actions

## Metrics Tracking

### State Duration Metrics

```json
{
  "task_name": "implement-formatter-api",
  "transitions": [
    {"from": "INIT", "to": "CLASSIFIED", "timestamp": "...", "duration": "PT2M"},
    {"from": "CLASSIFIED", "to": "REQUIREMENTS", "timestamp": "...", "duration": "PT45M"},
    {"from": "REQUIREMENTS", "to": "SYNTHESIS", "timestamp": "...", "duration": "PT10M"},
    ...
  ],
  "total_duration": "PT2H15M"
}
```

### Phase Metrics

```bash
# Time in each phase:
- REQUIREMENTS: 45 minutes (agents working)
- SYNTHESIS: 10 minutes (planning)
- IMPLEMENTATION: 1 hour (agents implementing)
- VALIDATION: 15 minutes (testing)
- Total: 2 hours 15 minutes
```

## Related Skills

- **task-init**: Creates task in INIT state
- **verify-requirements-complete**: Validates REQUIREMENTS → SYNTHESIS
- **checkpoint-approval**: Manages approval prerequisites
- **task-cleanup**: Final transition to CLEANUP

## Troubleshooting

### Error: "Invalid state transition"

```bash
# Trying to skip states
From: INIT
To: SYNTHESIS

Fix: Go through intermediate states:
1. INIT → CLASSIFIED
2. CLASSIFIED → REQUIREMENTS
3. REQUIREMENTS → SYNTHESIS
```

### Error: "Prerequisites not met"

```bash
# Missing required files/flags
Missing: user-approved-synthesis.flag

Fix:
1. Complete prerequisite step (get user approval)
2. Create required flag
3. Retry transition
```

### Error: "Task not in expected state"

```bash
# from_state doesn't match actual state
Expected: SYNTHESIS
Actual: REQUIREMENTS

Fix:
1. Check current state: jq -r '.state' task.json
2. Update from_state parameter
3. Or complete missing state transition
```

### State Stuck (Cannot Progress)

```bash
# Prerequisites can't be met
State: SYNTHESIS → IMPLEMENTATION
Blocker: User approval not obtained

Fix:
1. Present plan to user
2. Wait for explicit approval
3. Create approval flag
4. Retry transition
```

## Common Transition Patterns

### Pattern 1: Sequential (Normal Flow)

```bash
# Follow state machine exactly
INIT → CLASSIFIED → REQUIREMENTS → SYNTHESIS →
IMPLEMENTATION → VALIDATION → AWAITING_USER_APPROVAL →
COMPLETE → CLEANUP
```

### Pattern 2: Iteration (Fix Loop)

```bash
# Stay in VALIDATION, re-invoke agents
VALIDATION (fails) → re-invoke agents → VALIDATION (retry)
# Don't transition backward, fix in place
```

### Pattern 3: Fast-Forward (Skip Optional States)

```bash
# Some states optional for simple tasks
❌ Cannot skip: REQUIREMENTS, SYNTHESIS (mandatory)
⚠️  Cannot skip checkpoints (approval required)
```

## Implementation Notes

The state-transition script performs:

1. **Validation Phase**
   - Check task exists
   - Verify task.json readable
   - Validate from_state matches current
   - Confirm to_state is valid

2. **Prerequisite Check Phase**
   - Load prerequisites for transition
   - Check each prerequisite
   - Report missing prerequisites
   - Block if any missing

3. **Transition Phase**
   - Calculate duration in current state
   - Update state field
   - Append transition record
   - Update timestamp

4. **Persistence Phase**
   - Write updated task.json
   - Verify write successful
   - Validate JSON structure

5. **Verification Phase**
   - Read task.json back
   - Confirm state updated
   - Validate transition recorded
   - Return success status

6. **Metrics Phase**
   - Calculate phase duration
   - Update metrics
   - Log transition
   - Return detailed results
