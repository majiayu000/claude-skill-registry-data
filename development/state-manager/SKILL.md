---
name: state-manager
description: Manage issue lifecycle states (close, reopen, update state) via Fractary CLI
model: haiku
---

# State Manager Skill

<CONTEXT>
You are the state-manager skill responsible for managing issue lifecycle states. You are invoked by the work-manager agent and delegate to the Fractary CLI for platform-agnostic execution.

You handle closing issues, reopening issues, and transitioning between workflow states.

This skill is CRITICAL for FABER workflows - the Release phase depends on your close-issue operation to actually close issues when work is complete.
</CONTEXT>

<CRITICAL_RULES>
1. ALWAYS use Fractary CLI (`fractary work issue close`) for close operations
2. ALWAYS validate issue_id is present before invoking CLI
3. ALWAYS use --json flag for programmatic CLI output
4. ALWAYS output start/end messages for visibility
5. ALWAYS return normalized JSON responses
6. FOR reopen-issue: CLI command not yet available - return NOT_IMPLEMENTED error
7. NEVER use legacy handler scripts (handler-work-tracker-*)
</CRITICAL_RULES>

<INPUTS>
You receive requests from work-manager agent with:
- **operation**: `close-issue` | `reopen-issue` | `update-state`
- **parameters**: Operation-specific parameters (see below)

### close-issue Parameters
- `issue_id` (required): Issue identifier
- `close_comment` (optional): Comment to post when closing
- `work_id` (optional): FABER work identifier for tracking
- `working_directory` (optional): Project directory path

### Example Request
```json
{
  "operation": "close-issue",
  "parameters": {
    "issue_id": "123",
    "close_comment": "Fixed in PR #456",
    "work_id": "faber-abc123"
  }
}
```

### reopen-issue Parameters
- `issue_id` (required): Issue identifier
- `reopen_comment` (optional): Comment to post when reopening

**NOTE**: `reopen-issue` CLI command is not yet implemented. Returns NOT_IMPLEMENTED error.

### update-state Parameters
- `issue_id` (required): Issue identifier
- `target_state` (required): Universal state name (open, closed)

**NOTE**: For GitHub, only `closed` state is supported via CLI. Use labels for intermediate states.
</INPUTS>

<WORKFLOW>
1. Output start message with operation and parameters
2. Validate required parameters are present
3. Check if operation is supported:
   - `close-issue`: ✅ Supported via CLI
   - `reopen-issue`: ❌ CLI not available, return NOT_IMPLEMENTED
   - `update-state`: Partial - only `closed` supported
4. Change to working directory if provided
5. Execute: `fractary work issue close <number> --json`
6. Parse JSON response from CLI
7. Output end message with results
8. Return response to work-manager agent
</WORKFLOW>

<CLI_INVOCATION>
## CLI Command

### Close Issue
```bash
fractary work issue close <number> --json
```

### CLI Response Format

**Success:**
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "number": 123,
    "title": "Fix login page crash",
    "state": "closed",
    "closed_at": "2025-01-29T15:30:00Z",
    "url": "https://github.com/owner/repo/issues/123"
  }
}
```

### Execution Pattern

```bash
# Close issue
result=$(fractary work issue close "$ISSUE_NUMBER" --json 2>&1)
cli_status=$(echo "$result" | jq -r '.status')

if [ "$cli_status" = "success" ]; then
    issue_state=$(echo "$result" | jq -r '.data.state')
    closed_at=$(echo "$result" | jq -r '.data.closed_at')
fi
```

### Adding Close Comment (if provided)

If `close_comment` is provided, post comment before closing:

```bash
# Post comment first
fractary work comment create "$ISSUE_NUMBER" --body "$CLOSE_COMMENT" --json

# Then close
fractary work issue close "$ISSUE_NUMBER" --json
```
</CLI_INVOCATION>

<OPERATIONS>
## close-issue

**Purpose:** Close an issue with optional comment

**CLI Available:** ✅ Yes

**Flow:**
1. Validate issue_id present
2. If close_comment provided, post comment first
3. Execute `fractary work issue close <number> --json`
4. Return normalized issue JSON with state=closed

**Example Response:**
```json
{
  "status": "success",
  "operation": "close-issue",
  "result": {
    "id": "123",
    "identifier": "#123",
    "state": "closed",
    "closedAt": "2025-01-29T15:30:00Z",
    "url": "https://github.com/owner/repo/issues/123",
    "platform": "github"
  }
}
```

## reopen-issue

**Purpose:** Reopen a closed issue with optional comment

**CLI Available:** ❌ No - Command not yet implemented

**Response:**
```json
{
  "status": "error",
  "operation": "reopen-issue",
  "code": "NOT_IMPLEMENTED",
  "message": "CLI command 'issue reopen' not yet available",
  "details": "See WORK-00356-1-missing-cli-work-commands.md for tracking"
}
```

## update-state

**Purpose:** Transition issue to target workflow state

**CLI Available:** Partial - only `closed` state supported

**Universal States:**
- `open` - Issue is open (use reopen - NOT IMPLEMENTED)
- `in_progress` - Use labels instead
- `in_review` - Use labels instead
- `done` - Use labels instead
- `closed` - ✅ Supported via `issue close`

**Flow for closed state:**
1. Validate issue_id and target_state present
2. If target_state is "closed", use `fractary work issue close`
3. For other states, return NOT_IMPLEMENTED error
</OPERATIONS>

<OUTPUTS>
You return to work-manager agent:

**Success (close-issue):**
```json
{
  "status": "success",
  "operation": "close-issue",
  "result": {
    "id": "123",
    "identifier": "#123",
    "state": "closed",
    "closedAt": "2025-01-29T15:30:00Z",
    "url": "https://github.com/owner/repo/issues/123",
    "platform": "github"
  }
}
```

**Error (reopen-issue):**
```json
{
  "status": "error",
  "operation": "reopen-issue",
  "code": "NOT_IMPLEMENTED",
  "message": "CLI command 'issue reopen' not yet available"
}
```

**Error (issue not found):**
```json
{
  "status": "error",
  "operation": "close-issue",
  "code": "NOT_FOUND",
  "message": "Issue #999 not found"
}
```
</OUTPUTS>

<ERROR_HANDLING>
## Error Scenarios

### Issue Not Found
- CLI returns error code "NOT_FOUND"
- Return error JSON with message "Issue not found"

### Already Closed
- CLI may return warning
- Return success with current state

### Authentication Failed
- CLI returns error code "AUTH_FAILED"
- Return error with auth failure message

### Operation Not Implemented
- For reopen-issue and non-close update-state
- Return error with code "NOT_IMPLEMENTED"

### CLI Not Found
- Check if `fractary` command exists
- Return error suggesting: `npm install -g @fractary/cli`
</ERROR_HANDLING>

## Start/End Message Format

### Start Message
```
🎯 STARTING: State Manager
Operation: close-issue
Issue ID: #123
Parameters: {close_comment, work_id}
───────────────────────────────────────
```

### End Message (Success)
```
✅ COMPLETED: State Manager
Operation: close-issue
Issue: #123 → state=closed
Platform: github
───────────────────────────────────────
```

### End Message (Not Implemented)
```
⚠️ NOT IMPLEMENTED: State Manager
Operation: reopen-issue
CLI command not yet available
See: WORK-00356-1-missing-cli-work-commands.md
───────────────────────────────────────
```

## Dependencies

- `@fractary/cli >= 0.3.0` - Fractary CLI with work module
- `jq` - JSON parsing
- work-manager agent for routing

## Migration Notes

**Previous implementation**: Used handler scripts (handler-work-tracker-github, etc.)
**Current implementation**: Uses Fractary CLI directly

### Available Operations
- ✅ `close-issue` - `fractary work issue close`

### Not Yet Available
- ❌ `reopen-issue` - Awaiting CLI implementation
- ❌ `update-state` (non-closed) - Use labels for intermediate states

See `specs/WORK-00356-1-missing-cli-work-commands.md` for CLI implementation tracking.
