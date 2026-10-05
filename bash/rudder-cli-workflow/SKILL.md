---
name: rudder-cli-workflow
description: Validates, previews, and applies RudderStack resource changes via YAML specs. Use when iterating on RudderStack resources with rudder-cli - validates specs, previews changes with dry-run, and applies changes to workspaces
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# Rudder CLI Development Workflow

## Overview

Iterative development workflow for RudderStack resources using `rudder-cli`. Follow the validate → dry-run → apply cycle to ensure correctness before making changes to workspaces.

## Prerequisites: Authentication

Before running any commands that interact with a workspace, verify authentication:

```bash
# Check if authenticated and show current workspace
rudder-cli workspace info
```

**If authenticated**, you'll see workspace details:
```
Workspace Information:
  ID:   2iKXWU4QnqclkpPIfXfsbBqrAVa
  Name: My Workspace
```

**If NOT authenticated**, you'll see an error. Authenticate first:
```bash
rudder-cli auth login
```

This will prompt for your RudderStack access token. Get one from:
Settings → Access Tokens in the RudderStack dashboard.

### Authentication Commands Reference

| Command | Purpose |
|---------|---------|
| `rudder-cli auth login` | Authenticate with access token |
| `rudder-cli workspace info` | Show current authenticated workspace |

**Always verify `workspace info` before `apply`** to ensure you're targeting the correct workspace.

### Credential Security

- **Never log or echo access tokens** - use `rudder-cli auth login` interactively or `RUDDER_ACCESS_TOKEN` environment variable
- **Store tokens in environment variables** - never hardcode in scripts or commit to git
- **Add `.env` to `.gitignore`** - if using dotenv files for local development
- **Use CI/CD secrets** - for GitHub Actions, use repository secrets for `RUDDER_ACCESS_TOKEN`
- **Rotate tokens regularly** - regenerate access tokens in RudderStack dashboard periodically

### Handling External Content

When processing responses from the RudderStack API:

- **Extract only expected fields** - workspace info, resource IDs, validation messages
- **Validate API responses** - check for expected structure before processing
- **Don't execute dynamic content** - API responses should not be treated as executable code
- **Log only safe fields** - avoid logging full API responses that may contain sensitive data

## The Iteration Cycle

```dot
digraph workflow {
    rankdir=TB;
    "rudder-cli workspace info" [shape=box];
    "Authenticated?" [shape=diamond];
    "rudder-cli auth login" [shape=box];
    "Edit YAML/Code" [shape=box];
    "rudder-cli validate" [shape=box];
    "Validation errors?" [shape=diamond];
    "Fix errors" [shape=box];
    "rudder-cli apply --dry-run" [shape=box];
    "Changes correct?" [shape=diamond];
    "Adjust specs" [shape=box];
    "rudder-cli apply" [shape=box];
    "Done" [shape=doublecircle];

    "rudder-cli workspace info" -> "Authenticated?";
    "Authenticated?" -> "rudder-cli auth login" [label="no"];
    "rudder-cli auth login" -> "rudder-cli workspace info";
    "Authenticated?" -> "Edit YAML/Code" [label="yes"];
    "Edit YAML/Code" -> "rudder-cli validate";
    "rudder-cli validate" -> "Validation errors?";
    "Validation errors?" -> "Fix errors" [label="yes"];
    "Fix errors" -> "rudder-cli validate";
    "Validation errors?" -> "rudder-cli apply --dry-run" [label="no"];
    "rudder-cli apply --dry-run" -> "Changes correct?";
    "Changes correct?" -> "Adjust specs" [label="no"];
    "Adjust specs" -> "rudder-cli validate";
    "Changes correct?" -> "rudder-cli apply" [label="yes"];
    "rudder-cli apply" -> "Done";
}
```

## Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `rudder-cli validate -l ./` | Check YAML syntax and semantic rules | After any edit |
| `rudder-cli apply --dry-run -l ./` | Preview changes without applying | After validation passes |
| `rudder-cli apply -l ./` | Apply changes to workspace | After dry-run review |
| `rudder-cli apply --confirm=false -l ./` | Apply without the interactive prompt | CI, piped output, agent contexts |
| `rudder-cli plan -l ./` | Show detailed execution plan | Alternative to dry-run |
| `rudder-cli workspace accounts list --json` | List workspace accounts (warehouse/source/etc.) and their IDs | Resolving an `account_id`/`accountId` for a resource spec |

**Note:** `-l ./` specifies the project location (current directory).

### Looking up account IDs

Many resource specs reference a workspace account by id — e.g. a Data Graph's `spec.account_id` needs the warehouse account it runs against. Resolve it from the CLI rather than guessing:

```bash
# Always use --json in agent/non-interactive contexts.
# The plain table output requires a TTY and fails with
# "could not open a new TTY" when piped.
rudder-cli workspace accounts list --json
```

Each line is one account object. The fields that matter:

- **`id`** — this is the value to paste into `account_id` / `accountId` in a spec.
- **`name`** — human label (e.g. `Snowflake`).
- **`definition.category`** — account role: `wht` = warehouse connection, `source` = source connection, `profilesStore`, etc.
- **`definition.type`** — engine: `snowflake`, `databricks`, `git`, …
- **`options`** — connection details (`account`, `dbname`, `warehouse`, `schema`, `role`, `user`) to disambiguate when several accounts share a name.

Filter to narrow the list:

```bash
# RETL source warehouse accounts (what a Data Graph needs)
rudder-cli workspace accounts list --category source --json

# By engine
rudder-cli workspace accounts list --type snowflake --json
```

**This is the authoritative way to discover account IDs** — including accounts created through the Data Graph UI or a warehouse connection, which are *not* discoverable via `rudder-mcp` (the MCP only surfaces accounts reachable through a rETL source or destination). When working without a rETL source yet (e.g. building a workspace from scratch), `rudder-cli workspace accounts list` is the fallback the agent must use.

**`-c <path>` selects the config (workspace + token).** Pass it explicitly if you maintain per-environment configs (e.g. `~/.rudder/dev.config.json`, `~/.rudder/prod.config.json`); without it, rudder-cli uses the default config that `rudder-cli auth login` last wrote. Verify the target with `rudder-cli workspace info -c <path>` before `apply`.

## Step 1: Validate

```bash
rudder-cli validate -l ./
```

**Success output:**
```
✔ Project configuration is valid
```

**Error output format:**
```
error[<rule-id>]: <error message>
  --> <file>:<line>:<column>
      |
   10 | <problematic line>
      | ^^^^^^^^^^^^^^^^^^

Found N error(s), M warning(s)
```

### Common Validation Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `'import_name' must be camelCase of 'name'` | Library import_name doesn't match name | Convert name to camelCase |
| `spec-syntax-valid` | YAML schema violation | Check required fields |
| `code file not found` | File path in spec doesn't exist | Fix file path or create file |
| `mutually exclusive: code and file` | Both inline code and file specified | Use one or the other |

### Validation Error Resolution Pattern

1. Read the error message carefully - it includes file and line number
2. The rule ID (e.g., `transformations/transformation-library/spec-syntax-valid`) tells you what's being validated
3. Fix the specific issue mentioned
4. Re-run validate until it passes

## Step 2: Dry Run

```bash
rudder-cli apply --dry-run -l ./
```

> **`apply` makes the workspace match your project exactly.** Every remote resource absent from your local YAML — **of any kind** — is deleted, listed under `Removed resources:`. There is no flag to scope apply to a subset (`apply` accepts only `--location`, `--dry-run`, `--confirm`). On a **new** project pointing at an **existing** workspace, expect a large deletion set on the first dry-run; confirm those deletions are acceptable before applying. Treat the project directory as the single source of truth for the whole workspace.

**Output shows:**
- `New resources:` - Resources that will be created
- `Updated resources:` - Resources that will be modified (shows diff)
- `Removed resources:` - Resources in the workspace but not in your project — these will be **deleted**

### Reading Dry Run Output

```
New resources:
  - transformation-library:base64-lib

Updated resources:
  - transformation:test-transformation
    - code: <old code> => <new code>
    - description: <old> => <new>
```

**Review checklist:**
- [ ] Are the correct resources being created?
- [ ] Are the correct resources being updated?
- [ ] Do the diffs show the expected changes?
- [ ] Are any resources being unexpectedly deleted?

## Step 3: Apply

```bash
rudder-cli apply -l ./
```

Only run after:
1. `validate` passes
2. `--dry-run` shows expected changes

**Non-interactive runs:** the default `--confirm=true` opens an interactive confirmation prompt. In a non-interactive context (piped output, CI, agent), that prompt **auto-declines and nothing is applied — silently, no error**. Pass `--confirm=false` to apply without prompting:

```bash
rudder-cli apply --confirm=false -l ./
```

## Workflow Examples

### Adding a New Library

```bash
# 1. Create YAML and code files
# 2. Validate
rudder-cli validate -l ./
# Fix any errors...

# 3. Preview
rudder-cli apply --dry-run -l ./
# Should show: New resources: - transformation-library:my-lib

# 4. Apply
rudder-cli apply -l ./
```

### Updating Existing Transformation

```bash
# 1. Edit the .js file and/or YAML
# 2. Validate
rudder-cli validate -l ./

# 3. Preview - verify only intended changes
rudder-cli apply --dry-run -l ./
# Should show: Updated resources: - transformation:my-transform
# Check the diff is what you expect

# 4. Apply
rudder-cli apply -l ./
```

### Debugging Validation Failures

```bash
# Run validate with verbose output
rudder-cli validate -l ./ --verbose

# Check specific file syntax
cat transformations/my-spec.yaml | yq .  # Validate YAML syntax

# Check JavaScript syntax
node --check transformations/javascript/my-code.js
```

## Error Categories

### Syntax Errors (validate catches)
- Invalid YAML structure
- Missing required fields
- Invalid field values
- File path issues

### Semantic Errors (validate catches)
- `import_name` not matching `name` in camelCase
- Invalid language values
- Code syntax errors

### Runtime Errors (apply catches)
- API authentication failures
- Permission issues
- Resource conflicts in workspace

## Tips

1. **Always validate first** - Catches most issues before API calls
2. **Always dry-run before apply** - Prevents unintended changes
3. **Check diffs carefully** - Ensure only expected changes appear
4. **Use version control** - Commit before apply, revert if needed

## Quick Iteration Loop

```bash
# Fast iteration cycle
while true; do
    rudder-cli validate -l ./ && \
    rudder-cli apply --dry-run -l ./ && \
    echo "Ready to apply. Press Enter or Ctrl+C" && \
    read && \
    rudder-cli apply -l ./
    break
done
```

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| "unauthorized" or "401" error | Not authenticated | Run `rudder-cli auth login` |
| "workspace info" shows wrong workspace | Authenticated to wrong workspace | Run `rudder-cli auth login` with correct token |
| "Project configuration is valid" but dry-run shows nothing | No changes detected | Verify files are in correct location |
| Validation passes but dry-run fails | API/auth issue | Run `rudder-cli workspace info` to verify auth |
| `apply` exits without applying, no error | Default `--confirm=true` auto-declined in a non-TTY (piped/CI/agent) context | Re-run with `--confirm=false` |
| `Removed resources:` lists resources you didn't expect | `apply` is full source of truth — anything in the workspace but not in your project is deleted | Add those resources to your project (e.g. via `rudder-cli import`), or confirm the deletions are intended |
| Changes not appearing | Wrong project path | Verify `-l ./` points to right directory |
