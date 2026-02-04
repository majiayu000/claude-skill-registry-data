---
name: checkpoint-approval
description: Manage user approval checkpoints with proper waiting and flag creation
allowed-tools: Bash, Write, Read
---

# Checkpoint Approval Skill

**Purpose**: Enforce user approval checkpoints with proper presentation, waiting, flag creation, and state transitions.

**Performance**: Prevents checkpoint bypasses, ensures user control over critical transitions

## When to Use This Skill

### ✅ Use checkpoint-approval When:

- Transitioning from SYNTHESIS → IMPLEMENTATION (plan approval)
- Transitioning from AWAITING_USER_APPROVAL → COMPLETE (change approval)
- Need to present plan/changes and wait for explicit approval
- Want to enforce mandatory checkpoint protocol

### ❌ Do NOT Use When:

- User already approved (flag exists)
- In bypass mode (user explicitly requested skip)
- Simple clarification questions (use AskUserQuestion)
- Not at a checkpoint transition

## What This Skill Does

### 1. Presents Information

**For Plan Approval (SYNTHESIS → IMPLEMENTATION)**:
```markdown
## Implementation Plan

[Shows synthesized plan from task.md]

### Stakeholder Requirements Summary:
- Architect: [key points]
- Tester: [key points]
- Formatter: [key points]

### Implementation Approach:
[planned approach]

### Agents to Invoke:
- architect (code implementation)
- tester (test creation)
- formatter (documentation/style)

⚠️ **APPROVAL REQUIRED**: Please review and approve to proceed.
```

**For Change Approval (AWAITING_USER_APPROVAL → COMPLETE)**:
```markdown
## Changes Ready for Merge

### Commit SHA: abc1234

### Changes Summary:
```bash
git diff --stat main...{task-branch}
```

### Files Modified:
[list of changed files]

### Validation Results:
- ✅ Build: PASSED
- ✅ Tests: PASSED
- ✅ Checkstyle: PASSED
- ✅ PMD: PASSED

⚠️ **APPROVAL REQUIRED**: Please review changes and approve merge to main.
```

### 2. Waits for Approval

```bash
# Skill STOPS and waits for user to respond with:
- "approved"
- "proceed"
- "looks good"
- "LGTM"
- "merge it"

# Does NOT proceed on:
- Silence
- Ambiguous responses
- Questions
```

### 3. Creates Approval Flag

**After explicit approval**:
```bash
# For plan approval:
touch /workspace/tasks/{task-name}/user-approved-synthesis.flag

# For change approval:
touch /workspace/tasks/{task-name}/user-approved-changes.flag
```

### 4. Transitions State

```bash
# For plan approval:
jq '.state = "IMPLEMENTATION"' task.json > tmp.json
mv tmp.json task.json

# For change approval:
jq '.state = "COMPLETE"' task.json > tmp.json
mv tmp.json task.json
```

## Usage

### Plan Approval Checkpoint

```bash
# After SYNTHESIS phase completes
TASK_NAME="implement-formatter-api"

# Invoke checkpoint-approval skill with plan type
/workspace/main/.claude/scripts/checkpoint-approval.sh \
  --task "$TASK_NAME" \
  --type "plan" \
  --plan-file "/workspace/tasks/$TASK_NAME/task.md"
```

### Change Approval Checkpoint

```bash
# After VALIDATION phase passes
TASK_NAME="implement-formatter-api"

# Invoke checkpoint-approval skill with changes type
/workspace/main/.claude/scripts/checkpoint-approval.sh \
  --task "$TASK_NAME" \
  --type "changes" \
  --branch "{task-name}"
```

## Approval Detection

### Valid Approval Phrases

**Affirmative**:
- "approved"
- "proceed"
- "looks good"
- "LGTM"
- "merge it"
- "go ahead"
- "approve"
- "yes"

**NOT Valid**:
- Silence (no response)
- "ok" (too ambiguous)
- Questions about the plan
- Requests for changes
- Partial approval ("mostly good but...")

## Safety Features

### Prevents Bypass

- ✅ Blocks state transition without flag
- ✅ Hook enforces flag presence
- ✅ No timeout (waits indefinitely)
- ✅ No assumption of approval

### Clear Communication

- ✅ Explicitly states "APPROVAL REQUIRED"
- ✅ Shows what user is approving
- ✅ Waits for clear affirmative response
- ✅ Confirms approval received

### State Machine Integration

- ✅ Validates current state before checkpoint
- ✅ Creates flag before transition
- ✅ Transitions state after flag created
- ✅ Hook validates flag exists

## Workflow Integration

### Checkpoint 1: Plan Approval

```markdown
CLASSIFIED state
  ↓
Requirements gathered (3 agent reports)
  ↓
SYNTHESIS state: Plan created in task.md
  ↓
[checkpoint-approval skill invoked] ← STOPS HERE
  ↓
Present plan to user
  ↓
Wait for explicit approval
  ↓
User says "approved"
  ↓
Create user-approved-synthesis.flag
  ↓
Transition to IMPLEMENTATION state
  ↓
Invoke implementation agents
```

### Checkpoint 2: Change Approval

```markdown
IMPLEMENTATION state
  ↓
Agents implement, merge to task branch
  ↓
VALIDATION state: Build and test
  ↓
All validation passes
  ↓
AWAITING_USER_APPROVAL state
  ↓
[checkpoint-approval skill invoked] ← STOPS HERE
  ↓
Present changes to user (diff, commit SHA)
  ↓
Wait for explicit approval
  ↓
User says "approved"
  ↓
Create user-approved-changes.flag
  ↓
Transition to COMPLETE state
  ↓
Squash and merge to main
```

## Output Format

Skill returns JSON after approval received:

```json
{
  "status": "approved",
  "checkpoint_type": "plan",
  "task_name": "implement-formatter-api",
  "flag_created": "/workspace/tasks/implement-formatter-api/user-approved-synthesis.flag",
  "state_transition": "SYNTHESIS → IMPLEMENTATION",
  "approval_phrase": "approved",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Related Skills

- **gather-requirements**: Precedes plan approval checkpoint
- **task-cleanup**: Follows change approval checkpoint
- **git-merge-linear**: Executes after change approval

## Troubleshooting

### User Says "ok" Instead of "approved"

```bash
# "ok" is too ambiguous, re-prompt:
"I need explicit approval to proceed. Please respond with
'approved', 'proceed', or 'looks good' if you approve the plan."
```

### User Asks Question Instead of Approving

```bash
# Answer question, then re-prompt for approval:
"[Answer to question]

Does this address your concern? If so, please approve with
'approved' or 'proceed' to continue."
```

### User Silent (No Response)

```bash
# DO NOT proceed, wait indefinitely
# After reasonable time (5+ minutes), prompt:
"Waiting for approval to proceed. Please review the plan above
and respond with 'approved' if you'd like to proceed."
```

### Hook Blocks Despite Flag Present

```bash
# Verify flag exists:
ls -la /workspace/tasks/{task-name}/*-flag

# Check flag permissions:
test -r /workspace/tasks/{task-name}/user-approved-synthesis.flag
echo $? # Should be 0

# Verify state matches:
jq -r '.state' /workspace/tasks/{task-name}/task.json
```

## Common Mistakes to Avoid

### ❌ Assuming Silence = Approval

```bash
# WRONG:
"User hasn't objected, proceeding with implementation..."

# CORRECT:
"Waiting for user approval. No response yet, continuing to wait..."
```

### ❌ Proceeding on Ambiguous Response

```bash
# WRONG:
User: "sure"
Agent: [Creates flag and proceeds]

# CORRECT:
User: "sure"
Agent: "To confirm, are you approving the plan? Please respond
with 'approved' or 'proceed' to continue."
```

### ❌ Creating Flag Before Presenting

```bash
# WRONG:
1. Create flag
2. Transition state
3. Present plan to user

# CORRECT:
1. Present plan to user
2. Wait for approval
3. Create flag
4. Transition state
```

### ❌ Skipping Checkpoint for "Simple" Tasks

```bash
# WRONG:
"This is a straightforward task, skipping approval..."

# CORRECT:
"Presenting plan for approval (required for all tasks)..."
```

## Implementation Notes

The checkpoint-approval script performs:

1. **Presentation Phase**
   - Load plan/changes from appropriate source
   - Format for user review
   - Display with clear approval request

2. **Waiting Phase**
   - Block execution (no timeout)
   - Monitor for user response
   - Validate response is affirmative

3. **Approval Phase**
   - Create flag file
   - Update task.json state
   - Return success status

4. **Verification Phase**
   - Confirm flag readable
   - Confirm state updated
   - Log approval event
