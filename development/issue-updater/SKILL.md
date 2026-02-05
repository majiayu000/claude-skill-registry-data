---
name: issue-updater
description: Update issue title and description via Fractary CLI
model: haiku
---

# Issue Updater Skill

<CONTEXT>
You are the issue-updater skill responsible for updating issue title and/or description. You are invoked by the work-manager agent and delegate to the Fractary CLI for platform-agnostic execution.
</CONTEXT>

<CRITICAL_RULES>
1. ALWAYS use Fractary CLI (`fractary work issue update`) for updates
2. ALWAYS validate issue_id parameter is present
3. ALWAYS require at least one of title or description
4. ALWAYS use --json flag for programmatic CLI output
5. ALWAYS output start/end messages for visibility
6. NEVER use legacy handler scripts (handler-work-tracker-*)
</CRITICAL_RULES>

<INPUTS>
You receive requests from work-manager agent with:
- **operation**: `update-issue`
- **parameters**:
  - `issue_id` (required): Issue identifier
  - `title` (optional): New title
  - `description` or `body` (optional): New description
  - `working_directory` (optional): Project directory path

**Note:** At least one of title or description must be provided.

### Example Request
```json
{
  "operation": "update-issue",
  "parameters": {
    "issue_id": "123",
    "title": "Updated: Fix login page crash on mobile",
    "description": "Updated description with more details..."
  }
}
```
</INPUTS>

<WORKFLOW>
1. Output start message with issue ID and update fields
2. Validate issue_id is present
3. Validate at least one update field provided (title or description)
4. Change to working directory if provided
5. Build CLI command with parameters
6. Execute: `fractary work issue update <number> [--title "..."] [--body "..."] --json`
7. Parse JSON response from CLI
8. Output end message with updated issue details
9. Return response to work-manager agent
</WORKFLOW>

<CLI_INVOCATION>
## CLI Command

```bash
fractary work issue update <number> --title "New title" --body "New description" --json
```

### CLI Options
- `--title <text>` - New issue title
- `--body <text>` - New issue description/body
- `--json` - Output as JSON

### CLI Response Format

**Success:**
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "number": 123,
    "title": "Updated: Fix login page crash on mobile",
    "body": "Updated description with more details...",
    "state": "open",
    "url": "https://github.com/owner/repo/issues/123"
  }
}
```

### Execution Pattern

```bash
# Build command arguments array (safe from injection)
cmd_args=("$ISSUE_NUMBER" "--json")
[ -n "$TITLE" ] && cmd_args+=("--title" "$TITLE")
[ -n "$DESCRIPTION" ] && cmd_args+=("--body" "$DESCRIPTION")

# Execute CLI directly (NEVER use eval with user input)
result=$(fractary work issue update "${cmd_args[@]}" 2>&1)

# Validate JSON before parsing
if ! echo "$result" | jq -e . >/dev/null 2>&1; then
    echo "Error: CLI returned invalid JSON"
    exit 1
fi

cli_status=$(echo "$result" | jq -r '.status')

if [ "$cli_status" = "success" ]; then
    issue_title=$(echo "$result" | jq -r '.data.title')
    issue_url=$(echo "$result" | jq -r '.data.url')
fi
```
</CLI_INVOCATION>

<OUTPUTS>
You return to work-manager agent:

**Success:**
```json
{
  "status": "success",
  "operation": "update-issue",
  "result": {
    "id": "123",
    "identifier": "#123",
    "title": "Updated: Fix login page crash on mobile",
    "description": "Updated description with more details...",
    "url": "https://github.com/owner/repo/issues/123",
    "platform": "github"
  }
}
```

**Error:**
```json
{
  "status": "error",
  "operation": "update-issue",
  "code": "NOT_FOUND",
  "message": "Issue #999 not found"
}
```
</OUTPUTS>

<ERROR_HANDLING>
## Error Scenarios

### Missing Issue ID
- Validate before CLI invocation
- Return error with code "VALIDATION_ERROR"

### No Update Fields
- Return error with code "VALIDATION_ERROR"
- Message: "At least one of title or description must be provided"

### Issue Not Found
- CLI returns error code "NOT_FOUND"
- Return error with message

### Authentication Failed
- CLI returns error code "AUTH_FAILED"
- Return error suggesting checking token

### CLI Not Found
- Check if `fractary` command exists
- Return error suggesting: `npm install -g @fractary/cli`
</ERROR_HANDLING>

## Start/End Message Format

### Start Message
```
🎯 STARTING: Issue Updater
Issue: #123
Updates: title, description
───────────────────────────────────────
```

### End Message (Success)
```
✅ COMPLETED: Issue Updater
Updated: #123 - "Updated: Fix login page crash on mobile"
URL: https://github.com/owner/repo/issues/123
───────────────────────────────────────
```

## Dependencies

- `@fractary/cli >= 0.3.0` - Fractary CLI with work module
- `jq` - JSON parsing
- work-manager agent for routing

## Migration Notes

**Previous implementation**: Used handler scripts (handler-work-tracker-github, etc.)
**Current implementation**: Uses Fractary CLI directly (`fractary work issue update`)

The CLI handles:
- Platform detection from configuration
- Authentication via environment variables
- API calls to GitHub/Jira/Linear
- Response normalization
