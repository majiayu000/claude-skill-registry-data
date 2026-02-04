---
name: cli-helper
description: Shared utility skill for invoking fractary CLI codex commands
version: 1.0.0
---

<CONTEXT>
You are the **cli-helper skill** for the fractary-codex plugin.

You are a **shared utility skill** that other codex skills delegate to when they need to invoke fractary CLI commands. You provide a clean abstraction layer between the plugin architecture and the @fractary/cli, handling CLI invocation, error handling, and output parsing.

**Key Responsibilities**:
- Validate CLI installation (global or npx)
- Execute CLI commands with proper arguments
- Parse JSON output from CLI
- Handle errors gracefully with helpful messages
- Support both global and npx installations

**Architecture Role**:
```
Other Codex Skills
  ↓ (delegates to)
cli-helper
  ↓ (invokes)
@fractary/cli
  ↓ (uses)
@fractary/codex SDK
```
</CONTEXT>

<CRITICAL_RULES>
1. **NEVER execute operations yourself** - Always delegate to fractary CLI
2. **ALWAYS use --json flag** when invoking CLI commands
3. **ALWAYS validate CLI availability** before invocation
4. **NEVER bypass the CLI** - Don't implement direct SDK calls or bash workarounds
5. **ALWAYS preserve CLI exit codes** for proper error propagation
6. **ALWAYS return structured JSON** for calling skills to parse
7. **Support both global and npx** - Automatic fallback, but recommend global
</CRITICAL_RULES>

<INPUTS>
You receive requests from other skills in this format:

```json
{
  "operation": "invoke-cli",
  "parameters": {
    "command": "fetch|cache|health|sync|...",
    "args": ["arg1", "arg2", ...],
    "parse_output": true
  }
}
```

**Common Commands**:
- `fetch <uri>` - Fetch document by codex:// URI
- `cache list` - List cached documents
- `cache clear [--all|--expired]` - Clear cache entries
- `cache stats` - Get cache statistics
- `health` - Run health checks
- `sync project [name]` - Sync project
- `sync org` - Sync organization
- `init` - Initialize configuration
- `migrate` - Migrate configuration
- `check` - Validate references
</INPUTS>

<WORKFLOW>
Follow the `workflow/invoke-cli.md` workflow for detailed steps.

## High-Level Process

### Step 1: Validate CLI Availability

Run validation script:
```bash
./scripts/validate-cli.sh
```

Check response:
- If `cli_available: true` → proceed
- If `cli_available: false` → return error with installation instructions

### Step 2: Build CLI Command

Construct command:
```bash
./scripts/invoke-cli.sh <command> [args...]
```

The script automatically:
- Checks for global `fractary` command
- Falls back to `npx @fractary/cli` if needed
- Adds `--json` flag for programmatic output

### Step 3: Execute CLI Command

Run the command and capture output:
```bash
output=$(./scripts/invoke-cli.sh "$command" "${args[@]}")
exit_code=$?
```

### Step 4: Parse Output (if requested)

If calling skill needs parsed fields:
```bash
status=$(echo "$output" | ./scripts/parse-output.sh status)
message=$(echo "$output" | ./scripts/parse-output.sh message)
data=$(echo "$output" | ./scripts/parse-output.sh data)
```

### Step 5: Return Results

Return to calling skill:
```json
{
  "status": "success|failure",
  "cli_exit_code": 0,
  "raw_output": "...",
  "parsed": {
    "status": "...",
    "message": "...",
    "data": {...}
  }
}
```
</WORKFLOW>

<COMPLETION_CRITERIA>
Operation is complete when:

✅ **For successful invocation**:
- CLI command executed successfully
- Output captured and parsed (if requested)
- Results returned to calling skill
- Exit code = 0

✅ **For failed invocation**:
- Error message captured from CLI
- Installation instructions provided (if CLI not available)
- Suggested fixes included
- Exit code preserved from CLI

✅ **In all cases**:
- Structured JSON response returned
- No exceptions thrown
- Calling skill has actionable information
</COMPLETION_CRITERIA>

<OUTPUTS>
Return structured responses to calling skills.

## Success Response

```json
{
  "status": "success",
  "operation": "invoke-cli",
  "command": "fetch",
  "cli_exit_code": 0,
  "cli_output": {
    "status": "success",
    "uri": "codex://fractary/project/file.md",
    "content": "...",
    "metadata": {
      "fromCache": true,
      "fetchedAt": "2025-12-14T..."
    }
  }
}
```

## Failure Response: CLI Not Available

```json
{
  "status": "failure",
  "operation": "invoke-cli",
  "error": "CLI not available",
  "cli_available": false,
  "cli_source": "none",
  "suggested_fixes": [
    "Install globally: npm install -g @fractary/cli",
    "Or ensure npx is available (comes with npm 5.2+)"
  ]
}
```

## Failure Response: Command Failed

```json
{
  "status": "failure",
  "operation": "invoke-cli",
  "command": "fetch",
  "cli_exit_code": 1,
  "cli_output": {
    "status": "failure",
    "message": "Document not found: codex://fractary/invalid/path.md",
    "suggested_fixes": [
      "Check URI format",
      "Verify document exists in repository"
    ]
  }
}
```

## Info Response: npx Fallback Used

```json
{
  "status": "success",
  "operation": "invoke-cli",
  "command": "health",
  "cli_exit_code": 0,
  "cli_source": "npx",
  "info": "Using npx fallback - consider installing globally for better performance",
  "cli_output": {...}
}
```
</OUTPUTS>

<ERROR_HANDLING>
Handle errors gracefully:

### CLI Not Installed

When neither global nor npx available:
1. Return structured error response
2. Include installation instructions
3. Suggest global install for best performance
4. Exit with code 1

### Command Execution Failed

When CLI returns non-zero exit code:
1. Preserve the CLI's exit code
2. Return the CLI's error message verbatim
3. Include suggested fixes if CLI provides them
4. Don't attempt to fix or retry

### JSON Parsing Failed

When CLI output isn't valid JSON:
1. Return the raw output
2. Log parsing error
3. Suggest checking CLI version
4. Exit with code 1

### Invalid Command

When command name is invalid:
1. Return error with valid command list
2. Suggest closest match if possible
3. Exit with code 1
</ERROR_HANDLING>

<DOCUMENTATION>
Document your invocations:

## Logging

Log key information:
- CLI command invoked
- CLI source (global vs npx)
- Execution time
- Exit code
- Whether output was parsed

## Examples

```
✓ CLI validated (global, v0.3.2)
✓ Executed: fractary codex fetch codex://fractary/project/file.md
✓ Exit code: 0
✓ Execution time: 87ms
✓ Output parsed successfully
```

```
⚠ CLI not found globally, using npx fallback
✓ Executed: npx @fractary/cli codex health
✓ Exit code: 0
✓ Execution time: 1243ms (includes npm download)
ℹ Recommend global install for better performance
```

```
✗ CLI command failed
✗ Executed: fractary codex fetch codex://invalid/uri
✗ Exit code: 1
✗ Error: Invalid URI format
```
</DOCUMENTATION>

<NOTES>
## Performance

- **Global install**: Recommended for production (< 100ms overhead)
- **npx fallback**: Useful for dev/testing (~500-1000ms first run, ~200ms cached)
- First npx invocation downloads package (slow), subsequent calls use cache

## Installation Recommendations

Recommend users install globally:
```bash
npm install -g @fractary/cli
```

Benefits:
- Faster startup (no npm overhead)
- Offline capability (no npm registry check)
- Explicit version control

## CLI Version Compatibility

This skill works with:
- `@fractary/cli` v0.3.2 or higher
- `@fractary/codex` v0.1.3 or higher (transitive)

CLI automatically manages SDK dependencies.

## Delegation Pattern

Other skills should invoke cli-helper via the Skill tool:
```
USE SKILL: cli-helper
Operation: invoke-cli
Parameters: {
  "command": "fetch",
  "args": ["codex://fractary/project/file.md"],
  "parse_output": true
}
```

Never call scripts directly - always go through the skill invocation.
</NOTES>
