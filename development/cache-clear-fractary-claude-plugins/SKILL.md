---
name: cache-clear
model: claude-haiku-4-5
description: |
  Clear cache entries based on filters (all, expired, pattern).
  Delegates to fractary CLI for safe cache operations with dry-run support.
tools: Bash, Skill
version: 4.0.0
---

<CONTEXT>
You are the cache-clear skill for the Fractary codex plugin.

Your responsibility is to remove entries from the codex cache by delegating to the **cli-helper skill** which invokes the `fractary codex cache clear` CLI command.

**Architecture** (v4.0):
```
cache-clear skill
  ↓ (delegates to)
cli-helper skill
  ↓ (invokes)
fractary codex cache clear
  ↓ (uses)
@fractary/codex SDK (CacheManager)
```

This provides safe cache deletion with confirmation, dry-run previews, and atomic index updates via the TypeScript SDK.
</CONTEXT>

<CRITICAL_RULES>
1. **ALWAYS delegate to cli-helper** - Never execute operations directly
2. **NEVER invoke bash scripts** - The CLI handles all operations
3. **ALWAYS preserve CLI error messages** - Pass through verbatim
4. **NEVER bypass the CLI** - Don't implement custom cache deletion logic
5. **Safety first** - CLI enforces confirmation for destructive operations
6. **Support dry-run** - Always allow preview before deletion
</CRITICAL_RULES>

<INPUTS>
- **scope**: string - Type of deletion (required)
  - "all": Clear entire cache (requires confirmation)
  - "expired": Clear only expired entries
  - "pattern": Clear entries matching pattern
- **filter**: Object with scope-specific parameters (optional)
  - `pattern`: string - Glob pattern (when scope=pattern)
- **dry_run**: boolean - Preview mode (default: false)
- **confirmed**: boolean - User confirmation (for scope=all)
</INPUTS>

<WORKFLOW>

## Step 1: Validate Scope

Check that scope is one of: all, expired, pattern

IF scope is invalid:
  - Error: "Invalid scope"
  - List valid scopes: all, expired, pattern
  - STOP

IF scope == "all" AND confirmed != true:
  - Set dry_run = true (force preview first)
  - Continue to show what would be deleted
  - Then ask for confirmation

## Step 2: Build CLI Arguments

Construct arguments array from inputs:

```javascript
args = ["cache", "clear"]

// Add scope
if (scope === "all") args.push("--all")
if (scope === "expired") args.push("--expired")
if (scope === "pattern" && filter?.pattern) {
  args.push("--pattern", filter.pattern)
}

// Add dry-run flag if requested or scope=all without confirmation
if (dry_run || (scope === "all" && !confirmed)) {
  args.push("--dry-run")
}
```

## Step 3: Delegate to CLI Helper

USE SKILL: cli-helper
Operation: invoke-cli
Parameters:
```json
{
  "command": "cache",
  "args": ["clear", ...scope_flags, ...dry_run_flag],
  "parse_output": true
}
```

The cli-helper will:
1. Validate CLI installation
2. Execute: `fractary codex cache clear [--all|--expired|--pattern <p>] [--dry-run] --json`
3. Parse JSON output
4. Return results

## Step 4: Process CLI Response

The CLI returns JSON like:

**Dry-Run**:
```json
{
  "status": "success",
  "operation": "cache-clear",
  "dry_run": true,
  "would_delete": {
    "count": 4,
    "size_bytes": 8483,
    "entries": [
      {
        "uri": "codex://fractary/old-service/README.md",
        "size_bytes": 5242,
        "reason": "Expired 5 days ago"
      }
    ]
  }
}
```

**Actual Deletion**:
```json
{
  "status": "success",
  "operation": "cache-clear",
  "dry_run": false,
  "deleted": {
    "count": 4,
    "size_bytes": 8483,
    "entries": [...]
  },
  "cache_stats": {
    "before": {"total_entries": 42, "total_size_bytes": 3355443},
    "after": {"total_entries": 38, "total_size_bytes": 3347960}
  }
}
```

IF status == "success" AND dry_run == true:
  - Display preview (see OUTPUTS section)
  - IF scope == "all": Ask for confirmation
  - STOP (wait for user action)

IF status == "success" AND dry_run == false:
  - Display deletion results (see OUTPUTS section)
  - DONE ✅

IF status == "failure":
  - Extract error message from CLI
  - Return error to caller
  - DONE (with error)

## Step 5: Handle Confirmation (scope=all only)

IF scope == "all" AND dry_run preview shown:
  - Ask user: "Delete entire cache? This will remove {count} entries ({size})"
  - Options:
    - "Yes, delete all" → Retry with confirmed=true, dry_run=false
    - "Cancel" → STOP
  - STOP (wait for user choice)

## Step 6: Return Results

Display formatted output to user.

COMPLETION: Operation complete when results shown.

</WORKFLOW>

<COMPLETION_CRITERIA>
Operation is complete when:

✅ **For dry-run**:
- CLI invoked successfully
- Preview displayed to user
- User informed of next steps

✅ **For actual deletion**:
- CLI invoked successfully
- Entries deleted
- Cache index updated atomically
- Results displayed to user

✅ **For failed clear**:
- Error captured from CLI
- Error message clear and actionable
- Results returned to caller

✅ **In all cases**:
- No direct script execution
- CLI handles all operations
- Structured response provided
</COMPLETION_CRITERIA>

<OUTPUTS>
Return formatted cache clear results.

## Dry-Run Output

```
🔍 DRY-RUN: Cache Clear Preview
───────────────────────────────────────
Would delete 4 entries (8.3 KB):

⚠ codex://fractary/old-service/README.md (5.1 KB)
  Reason: Expired 5 days ago

⚠ codex://fractary/deprecated/guide.md (3.2 KB)
  Reason: Expired 7 days ago

Total to delete: 8.3 KB
───────────────────────────────────────
Run without --dry-run to execute
```

## Actual Deletion Output

```
🗑️  CACHE CLEAR COMPLETED
───────────────────────────────────────
Deleted 4 entries (8.3 KB):

✓ codex://fractary/old-service/README.md
✓ codex://fractary/deprecated/guide.md
✓ codex://fractary/temp-service/notes.md
✓ codex://fractary/archived/spec.md

Cache stats updated:
- Total entries: 38 (was 42)
- Total size: 3.1 MB (was 3.2 MB)
───────────────────────────────────────
Cache index updated automatically

Documents will be re-fetched when accessed.
```

## Confirmation Required (scope=all)

```
⚠️  CONFIRMATION REQUIRED: Delete entire cache

This will delete ALL cached documents:
- Total entries: 42
- Total size: 3.2 MB

Cache is regeneratable - source documents are not affected.
Deleted documents will be re-fetched automatically when accessed.

Delete entire cache?
[Yes, delete all] [Cancel]
```

## No Matches

```
ℹ️  CACHE CLEAR: No entries found

No entries matched the specified filter.

Filter: {filter description}
Current cache size: {count} entries ({size})
───────────────────────────────────────
Use /fractary-codex:cache-list to view cache
```

## Failure Response: CLI Error

```json
{
  "status": "failure",
  "operation": "cache-clear",
  "error": "Failed to delete cache entries",
  "cli_error": {
    "message": "Permission denied writing to cache index",
    "suggested_fixes": [
      "Check file permissions",
      "Ensure cache directory is writable"
    ]
  }
}
```

## Failure Response: CLI Not Available

```json
{
  "status": "failure",
  "operation": "cache-clear",
  "error": "CLI not available",
  "suggested_fixes": [
    "Install globally: npm install -g @fractary/cli",
    "Or ensure npx is available"
  ]
}
```

</OUTPUTS>

<ERROR_HANDLING>

### Index Missing

When CLI reports cache index doesn't exist:
1. Show "Cache is already empty" message
2. NOT an error condition
3. Explain this is normal for new installations

### Script Failure

When CLI returns error:
1. Preserve exact error message from CLI
2. Include suggested fixes if CLI provides them
3. Add context about what was being cleared
4. Return structured error

### Filesystem Error

When CLI reports file deletion failures:
1. Show CLI's error message
2. Explain which files failed
3. Note that CLI uses best-effort deletion
4. Index reflects actual state

### No Scope

When scope is missing or invalid:
1. Return error with valid scope list
2. Provide examples for each scope
3. Suggest using --dry-run to preview

### CLI Not Available

When cli-helper reports CLI unavailable:
1. Pass through installation instructions
2. Don't attempt workarounds
3. Return clear error to caller

</ERROR_HANDLING>

<DOCUMENTATION>
Upon completion, output:

**Success (Dry-Run)**:
```
🎯 STARTING: cache-clear
Scope: {scope}
Filter: {filter details}
Mode: DRY-RUN
───────────────────────────────────────

[Preview of entries to delete]

✅ COMPLETED: cache-clear (dry-run)
Would delete {count} entries ({size})
Source: CLI (via cli-helper)
───────────────────────────────────────
```

**Success (Actual Deletion)**:
```
🎯 STARTING: cache-clear
Scope: {scope}
Filter: {filter details}
Mode: EXECUTE
───────────────────────────────────────

[Deletion results]

✅ COMPLETED: cache-clear
Deleted {count} entries ({size})
Cache index updated
Source: CLI (via cli-helper)
───────────────────────────────────────
Documents will be re-fetched when accessed
```

**Failure**:
```
🎯 STARTING: cache-clear
───────────────────────────────────────

❌ FAILED: cache-clear
Error: {error_message}
Suggested fixes:
- {fix 1}
- {fix 2}
───────────────────────────────────────
```
</DOCUMENTATION>

<NOTES>

## Migration from v3.0

**v3.0 (bash scripts)**:
```
cache-clear
  └─ scripts/clear-cache.sh
      ├─ reads cache index
      ├─ deletes files
      ├─ updates index atomically
      └─ handles errors
```

**v4.0 (CLI delegation)**:
```
cache-clear
  └─ delegates to cli-helper
      └─ invokes: fractary codex cache clear
```

**Benefits**:
- ~95% code reduction in this skill
- TypeScript type safety from SDK
- Atomic index updates guaranteed by SDK
- Better error messages
- Built-in dry-run support
- Automatic confirmation handling

## CLI Command Used

This skill delegates to:
```bash
fractary codex cache clear [--all|--expired|--pattern <pattern>] [--dry-run] --json
```

## SDK Features Leveraged

Via the CLI, this skill benefits from:
- `CacheManager.clear()` - Main deletion logic
- Atomic index updates (write to temp, then rename)
- Best-effort file deletion
- Automatic stats calculation
- Built-in dry-run support

## Safety Features

1. **Confirmation for --all**: CLI enforces confirmation prompt
2. **Dry-run by default for scope=all**: Shows impact before deletion
3. **Atomic index updates**: SDK guarantees consistency
4. **Best-effort deletion**: Continues even if some files fail
5. **Index reflects reality**: Always updated to match filesystem

## Scope Examples

**Clear expired (safe, no confirmation)**:
```json
{
  "scope": "expired"
}
```

**Clear by pattern**:
```json
{
  "scope": "pattern",
  "filter": {"pattern": "**/*.md"}
}
```

**Clear all (requires confirmation)**:
```json
{
  "scope": "all",
  "confirmed": true
}
```

**Dry-run first**:
```json
{
  "scope": "all",
  "dry_run": true
}
```

## Cache Regeneration

All deleted entries will be automatically re-fetched when accessed:
- Next `/fractary-codex:fetch` retrieves from source
- Cache repopulated with fresh content
- TTL reset to configured default

## Testing

To test this skill:
```bash
# Ensure CLI installed
npm install -g @fractary/cli

# Populate cache first
fractary codex fetch codex://fractary/codex/README.md

# Test dry-run
USE SKILL: cache-clear
Parameters: {
  "scope": "expired",
  "dry_run": true
}

# Test actual deletion
USE SKILL: cache-clear
Parameters: {
  "scope": "expired"
}
```

## Troubleshooting

If clear fails:
1. Check CLI installation: `fractary --version`
2. Check permissions: Cache directory must be writable
3. Test CLI directly: `fractary codex cache clear --expired`
4. Check cache index: `fractary codex cache list`
5. Run health check: `fractary codex health`
</NOTES>
