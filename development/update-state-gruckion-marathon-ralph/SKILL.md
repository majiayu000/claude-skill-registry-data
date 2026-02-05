---
name: update-state
description: Programmatically update marathon-ralph state file using deterministic jq commands. Use this instead of manually editing the JSON file.
allowed-tools: Bash
---

# Update Marathon State

This skill provides deterministic state file updates using jq. **Always use this skill instead of manually editing `.claude/marathon-ralph.json`.**

## Why Use This Skill

- **Deterministic**: jq commands are atomic and predictable
- **Zero token overhead**: Script executes without loading into context
- **Consistent**: Same operation always produces same result
- **Safe**: Prevents malformed JSON from manual edits

## Available Commands

### Complete an Issue

Marks an issue as done: increments completed count, decrements todo, clears current_issue.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" complete-issue
```

### Start an Issue

Sets the current issue being worked on.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" start-issue "<issue_id>" "<issue_title>"
```

### Set Phase

Updates the marathon phase (setup, init, coding, complete).

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" set-phase "<phase>"
```

### Mark Complete

Marks the entire marathon as complete (sets active=false, phase=complete).

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" mark-complete
```

### Update Stats

Manually update the stats object.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" update-stats <completed> <in_progress> <todo>
```

### Clear Session

Clears the session_id (used when --force takeover is needed).

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" clear-session
```

### Reset Iterations

Resets the stop_hook_iterations counter to 0.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" reset-iterations
```

## Failure Tracking Commands

These commands support the circuit breaker system that prevents infinite loops.

### Initialize Failure Tracking

Sets up the failure tracking structure with default limits.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" init-failure-tracking
```

### Increment Phase Attempt

Increments the attempt counter for a specific phase of an issue.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" increment-phase-attempt "<issue_id>" "<phase>"
```

Example:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" increment-phase-attempt "GRU-220" "qa"
```

### Get Phase Attempts

Returns the current attempt count for a phase.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" get-phase-attempts "<issue_id>" "<phase>"
```

Returns a number (e.g., "3").

### Record Error

Records an error with signature detection for repeated error tracking.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" record-error "<issue_id>" "<phase>" "[error_message]"
```

The script normalizes the error message and creates a signature to detect if the same error is repeating.

### Skip Phase

Marks a phase as skipped with a reason.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" skip-phase "<issue_id>" "<phase>" "[reason]"
```

Example:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" skip-phase "GRU-220" "qa" "oRPC detected - REST URL mocking incompatible"
```

### Skip Issue

Skips an entire issue with a reason.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" skip-issue "<issue_id>" "[reason]"
```

### Reset Issue Tracking

Resets all failure tracking for a specific issue.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" reset-issue-tracking "<issue_id>"
```

### Reset on Success

Resets global failure counters after successful issue completion.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" reset-on-success
```

This resets:

- consecutive_failures to 0
- repeated_error_count to 0
- last_failure_signature to null
- stop_hook_iterations to 0

### Get Skipped Phases

Returns the list of skipped phases for an issue.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" get-skipped-phases "<issue_id>"
```

Returns a JSON array like:

```json
[{"phase": "qa", "reason": "oRPC detected", "timestamp": "2024-01-15T10:30:00.000Z"}]
```

### Check Limits

Checks if any failure limits have been exceeded.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" check-limits "<issue_id>" "[phase]"
```

Returns JSON with limit status:

```json
{
  "issue_id": "GRU-220",
  "should_skip_issue": false,
  "should_abort": false,
  "same_error_repeating": false,
  "should_skip_phase": false,
  "phase_attempts": 2,
  "max_phase_attempts": 5,
  "issue_attempts": 3,
  "max_issue_attempts": 5,
  "consecutive_failures": 1,
  "repeated_errors": 1
}
```

## Default Failure Limits

| Limit | Default | Description |
|-------|---------|-------------|
| max_phase_attempts.verify | 3 | Max attempts for verify phase |
| max_phase_attempts.plan | 3 | Max attempts for plan phase |
| max_phase_attempts.code | 3 | Max attempts for code phase |
| max_phase_attempts.test | 5 | Max attempts for test phase |
| max_phase_attempts.qa | 5 | Max attempts for QA phase |
| max_issue_attempts | 5 | Max total attempts per issue |
| max_consecutive_failures | 5 | Max failures before aborting marathon |
| max_repeated_errors | 3 | Max same error before skipping |
| max_stop_hook_iterations | 25 | Max stop hook cycles |

## Usage Examples

After completing the verify-plan-code-test-qa cycle for an issue:

```bash
# Mark the issue complete in state file
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" complete-issue
```

When starting work on a new issue:

```bash
# Set current issue
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" start-issue "GRU-220" "Step 5: Toggle Completion"
```

When all issues are done:

```bash
# Mark marathon complete
bash "${CLAUDE_PLUGIN_ROOT}/skills/update-state/scripts/update-state.sh" mark-complete
```

## State File Location

The script uses `${CLAUDE_PROJECT_DIR:-.}/.claude/marathon-ralph.json`

## Exit Codes

- `0`: Success
- `1`: Invalid arguments or missing state file
- `2`: jq command failed
