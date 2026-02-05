---
name: google-sheets-progress
version: 1.0.0
category: coordination
tags: [google-sheets, progress-tracking, micro-sprint, state-management]
status: approved
author: CFN Team
description: Tracks micro-sprint completion state and progress for Google Sheets operations
dependencies: [jq, bash]
created: 2025-11-18
updated: 2025-11-18
complexity: Low
keywords: [google-sheets, sprint-tracking, state-persistence, json]
triggers: [cfn-loop-micro-sprint, progress-monitoring]
performance_targets:
  execution_time_ms: 500
  success_rate: 0.99
---

# Google Sheets Progress Tracking Skill

## Purpose

Tracks and manages micro-sprint completion state for Google Sheets operations within CFN Loop iterations. Provides persistent state management enabling agents to resume operations after interruptions and coordinate work across multiple sprint phases.

## Problem Solved

Google Sheets operations often require multiple sequential steps (schema creation, data population, formula application). Without persistent progress tracking, agents cannot resume after failures or coordinate work between sprints. This skill enables micro-sprint checkpointing with recovery capabilities.

## When to Use

- After completing each micro-sprint phase (schema, data, formulas)
- When resuming interrupted work across CFN Loop iterations
- For progress reporting in Loop 2 validators
- When coordinating multi-phase operations across agents
- For audit trails showing which sprints completed successfully

## Interface

### Primary Script: `track-progress.sh`

**Required Parameters:**
- `--action`: `read`, `write`, `update`, `reset` (default: read)
- `--state-file`: Path to progress state file (default: `.claude/cfn-extras/.gs-progress-state.json`)

**Optional Parameters (for write/update):**
- `--completed`: JSON array of completed sprints, e.g., `["schema_001","data_001"]`
- `--current`: Current active sprint identifier, e.g., `formula_001`
- `--remaining`: JSON array of remaining sprints, e.g., `["formula_002"]`
- `--status`: State status (in_progress, completed, blocked, paused)
- `--metadata`: Additional JSON metadata to track
- `--task-id`: Task ID for coordination context

**Usage:**

```bash
# Read current progress state
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action read

# Initialize new sprint tracking
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action write \
  --completed '[]' \
  --current schema_001 \
  --remaining '["data_001","formula_001"]' \
  --status in_progress

# Update after completing a sprint
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action update \
  --completed '["schema_001"]' \
  --current data_001 \
  --remaining '["formula_001"]'

# Reset state for retry
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action reset
```

## Progress State Format

JSON structure managed by skill:

```json
{
  "task_id": "cfn-task-20251118-001",
  "sprint_sequence": [
    "schema_001",
    "data_001",
    "formula_001"
  ],
  "completed": ["schema_001"],
  "current": "data_001",
  "remaining": ["formula_001"],
  "status": "in_progress",
  "timestamps": {
    "created": "2025-11-18T10:30:00Z",
    "last_updated": "2025-11-18T10:45:30Z",
    "started": "2025-11-18T10:30:00Z",
    "completed": null
  },
  "metrics": {
    "total_sprints": 3,
    "completed_count": 1,
    "remaining_count": 1,
    "progress_percentage": 33.33,
    "estimated_completion": "2025-11-18T11:15:00Z"
  },
  "metadata": {
    "spreadsheet_id": "abc123def456",
    "sheet_name": "Operations",
    "retry_count": 0,
    "last_error": null
  }
}
```

## Validation Rules

The skill enforces:

1. **Valid JSON structure** - All state files are valid JSON
2. **Sprint identifier format** - Matches pattern: `[a-z]+_[0-9]{3}`
3. **Status enum validation** - Must be: `in_progress`, `completed`, `blocked`, `paused`
4. **Array consistency** - No duplicates between completed/current/remaining
5. **Chronological order** - Timestamps are monotonically increasing
6. **Atomic writes** - State files written atomically with backup

## Integration with CFN Loop

### Loop 3 Agents (Implementers)

After each micro-sprint completes:

```bash
# Initialize progress for 3-phase operation
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action write \
  --completed '[]' \
  --current schema_001 \
  --remaining '["data_001","formula_001"]' \
  --status in_progress \
  --task-id "$TASK_ID" \
  --metadata "{\"spreadsheet_id\": \"$SHEET_ID\", \"source\": \"loop3_agent\"}"

# After schema phase completes
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action update \
  --completed '["schema_001"]' \
  --current data_001 \
  --remaining '["formula_001"]'

# After data phase completes
./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh \
  --action update \
  --completed '["schema_001","data_001"]' \
  --current formula_001 \
  --remaining '[]'
```

### Loop 2 Validators

Read progress for validation context:

```bash
# Check what phases are complete
PROGRESS=$(./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh --action read)

COMPLETED=$(echo "$PROGRESS" | jq -r '.completed | length')
TOTAL=$(echo "$PROGRESS" | jq -r '.metrics.total_sprints')

echo "Validator inspecting: $COMPLETED of $TOTAL sprints completed"
```

### Coordinator Context

Use progress to determine which Loop 3 agents to spawn:

```bash
# Get current progress
PROGRESS=$(./.claude/cfn-extras/skills/google-sheets-progress/track-progress.sh --action read)
CURRENT_SPRINT=$(echo "$PROGRESS" | jq -r '.current')
REMAINING=$(echo "$PROGRESS" | jq -r '.remaining | length')

# Only spawn agents if there's remaining work
if [ "$REMAINING" -gt 0 ]; then
  echo "Spawning agents for remaining $REMAINING sprints"
  # Coordinator logic
fi
```

## Output Format

The script outputs structured JSON:

```json
{
  "success": true,
  "action": "read",
  "confidence": 0.98,
  "state": {
    "completed": ["schema_001"],
    "current": "data_001",
    "remaining": ["formula_001"],
    "status": "in_progress"
  },
  "metrics": {
    "progress_percentage": 33.33,
    "execution_time_ms": 45
  },
  "deliverables": [".claude/cfn-extras/.gs-progress-state.json"],
  "errors": []
}
```

## Error Handling

Skill handles these error scenarios:

1. **Invalid JSON in state file** - Backs up corrupted file, returns error with rollback option
2. **Missing state file** - Creates new state file with initialization defaults
3. **Lock contention** - Implements exponential backoff (100ms, 200ms, 400ms)
4. **Atomic write failures** - Uses temp file + mv pattern for safety
5. **Validation failures** - Returns detailed validation errors with suggestions

## State File Locations

State files are stored in:

- **Default**: `.claude/cfn-extras/.gs-progress-state.json`
- **Task-scoped**: `.claude/cfn-extras/.gs-progress-${TASK_ID}.json`
- **Backup location**: `.backups/gs-progress/[timestamp]_[hash].json`

## Best Practices

1. **Initialize on loop start**: Write initial state before spawning agents
2. **Atomic updates**: Use `--action update` for multi-field changes
3. **Regular reads**: Loop 2 validators should read at least once per iteration
4. **Task isolation**: Use `--task-id` to scope state to specific tasks
5. **Cleanup**: Call `--action reset` at completion to prepare for next task

## Anti-Patterns

❌ **Partial state updates**: Updating only some fields manually
❌ **File direct manipulation**: Editing JSON file directly instead of using script
❌ **Stale state assumptions**: Not reading current state before updating
❌ **Missing task context**: Not including task-id for multi-task scenarios
❌ **No validation**: Assuming state is always well-formed

## Testing

The skill includes comprehensive test coverage:

```bash
# Run all tests
./.claude/cfn-extras/skills/google-sheets-progress/test.sh

# Run specific test
./.claude/cfn-extras/skills/google-sheets-progress/test.sh --test write_action

# Validate dependencies
./.claude/cfn-extras/skills/google-sheets-progress/validate.sh
```

### Test Categories

1. **Initialization tests** - Create, read, verify state
2. **Update tests** - Modify state atomically
3. **Edge cases** - Missing file, corrupted JSON, concurrent access
4. **Validation tests** - Invalid enums, malformed arrays
5. **Performance tests** - Execution time within targets

## Success Criteria

- **Pass rate**: ≥0.95 (standard mode)
- **State consistency**: 0 consistency errors in concurrent access patterns
- **Recovery capability**: Failed operations recoverable via reset
- **Performance**: All operations complete within 500ms
- **Backward compatibility**: State files from v1.0.0 remain compatible

## References

- **CFN Loop Documentation**: `.claude/commands/CFN_LOOP_TASK_MODE.md`
- **State Management Pattern**: `.claude/skills/cfn-automatic-memory-persistence/SKILL.md`
- **Coordination Protocols**: `.claude/skills/cfn-coordination/SKILL.md`
- **Agent Output Standards**: `docs/AGENT_OUTPUT_STANDARDS.md`
