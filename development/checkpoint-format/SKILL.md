---
name: checkpoint-format
description: Interactive checkpoint format for orchestrator pause points
---

# Checkpoint Format Skill

Use this format when orchestrators need to pause for user approval.

## Standard Checkpoint Template

```
★ CHECKPOINT: [Name]

[Summary of current state]

Options:
- A) [Primary action]
- B) [Alternative]
- C) [Abort]
```

**IMPORTANT:** Wait for user to select an option before proceeding.

## Error Recovery Checkpoint

When a sub-agent fails:

```
★ CHECKPOINT: Sub-Agent Error

**Failed Agent:** {agent_name}
**Task:** {task_description}
**Error:** {error_message}

### Partial Progress
{list of completed steps before failure}

### Options
- **R) Retry** - Attempt {agent_name} again
- **S) Skip** - Continue to next step (may cause issues)
- **A) Abort** - Stop workflow, state saved to 00-index.md
- **D) Debug** - Launch debug-analyst to investigate

**[WAIT FOR USER INPUT]**
```

## Depth Limit Checkpoint

When spawning depth limit is reached:

```
★ CHECKPOINT: Depth Limit Reached

**Current Depth:** 5/5
**Attempted Spawn:** {agent_name}
**Reason:** {why spawn was needed}

This may indicate a recursive workflow or overly complex task.

### Options
- **I) Increase** - Raise limit to 7 and continue
- **S) Simplify** - Break task into smaller pieces
- **A) Abort** - Stop and review workflow design

**[WAIT FOR USER INPUT]**
```

## Orchestrator-Specific Checkpoints

| Orchestrator | Checkpoint Points |
|--------------|-------------------|
| `pr-review-manager` | After review, Before implement, Before merge |
| `architecture-lead` | After analysis, After design options |
| `implementation-manager` | After decomposition, Before each task |
