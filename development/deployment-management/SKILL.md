---
name: deployment-management
description: Managing LangGraph Cloud deployments through listing, filtering, and cleanup operations. Use when managing test deployments, cleaning up orphaned resources, filtering by name patterns, or handling bulk deletion. Automatically sources credentials from devcontainer environment.
scope: project
---

# Deployment Management

Manage LangGraph Cloud deployments using the Langstar CLI with focus on test deployment cleanup, filtering, and environment handling.

## Core Capabilities

- List deployments with filtering by name, status, or type
- Filter test deployments by pattern (test-*, langstar-test-*)
- Delete deployments individually or in batch
- Handle environment variables automatically (check first, source if needed)
- Interactive confirmation for destructive operations

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Handling](#environment-handling)
- [Core Workflows](#core-workflows)
- [CLI Reference](#cli-reference)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

## Prerequisites

### Required Credentials

**LangSmith API:**
- `LANGSMITH_API_KEY` - API key for Control Plane authentication
- `LANGSMITH_WORKSPACE_ID` - Workspace ID (optional if using organization)

**Location:** `/workspace/.devcontainer/.env` (gitignored)

### CLI Tool

All operations use `langstar graph` commands:
- `langstar graph list` - List with filtering
- `langstar graph get <id>` - Get details
- `langstar graph delete <id>` - Delete deployment

## Environment Handling

### Critical Pattern: Check Before Sourcing

**Always check if credentials exist BEFORE sourcing:**

```bash
# ✅ CORRECT: Check first
if [ -z "$LANGSMITH_API_KEY" ] || [ -z "$LANGSMITH_WORKSPACE_ID" ]; then
    echo "📋 Sourcing credentials..."
    source /workspace/.devcontainer/.env
fi

# Verify (never expose actual values)
[ -n "$LANGSMITH_API_KEY" ] && echo "✓ LANGSMITH_API_KEY set" || echo "❌ Not set"
```

**Security Rule: Never expose credential values:**

```bash
# ❌ WRONG: Exposes sensitive data
echo "Key: $LANGSMITH_API_KEY"

# ✅ CORRECT: Only check presence
[ -n "$LANGSMITH_API_KEY" ] && echo "Set" || echo "Not set"
```

## Core Workflows

### Workflow 1: List All Deployments

```bash
# Source credentials if needed
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi

# List deployments
langstar graph list --limit 20
```

**Output:**
```
┌────────────────────────────────┬──────────────────────┬────────┐
│ Name                           │ ID                   │ Status │
├────────────────────────────────┼──────────────────────┼────────┤
│ langstar-test-1763668434       │ 97dff6a5-f844-472... │ Ready  │
│ test-deployment-1763666536     │ 8665a96b-4620-407... │ Ready  │
└────────────────────────────────┴──────────────────────┴────────┘
```

### Workflow 2: Filter by Name Pattern

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi

# Filter by substring
langstar graph list --name-contains "test"
langstar graph list --name-contains "langstar-test"

# Combine filters
langstar graph list --name-contains "test" --status READY --limit 100
```

### Workflow 3: Delete Single Deployment

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi

# Interactive deletion (prompts for confirmation)
langstar graph delete <deployment-id>

# Skip confirmation
langstar graph delete <deployment-id> --yes
```

### Workflow 4: Batch Cleanup of Test Deployments

**Recommended: Interactive review before each deletion**

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi

# List test deployments to review
langstar graph list --name-contains "test" --limit 100

# Get deployment IDs
deployment_ids=$(langstar graph list --name-contains "test" --limit 100 --format json | jq -r '.resources[].id')

# Delete with confirmation for each
for id in $deployment_ids; do
    echo "Deployment: $id"
    langstar graph get "$id" | jq '{name, status, created_at}'
    read -p "Delete? (y/n): " confirm
    [ "$confirm" = "y" ] && langstar graph delete "$id" --yes && echo "✓ Deleted"
done
```

**Alternative: Bulk deletion (use with caution)**

See [examples/batch-cleanup.md](references/batch-cleanup.md) for non-interactive scripts.

### Workflow 5: Filter by Status or Type

**Available filters:**
- **Status:** `READY`, `AWAITING_DATABASE`, `UNUSED`, `AWAITING_DELETE`
- **Type:** `dev_free`, `dev`, `prod`

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi

# Filter by status
langstar graph list --status READY
langstar graph list --status UNUSED

# Filter by type
langstar graph list --deployment-type dev_free

# Combine filters
langstar graph list --name-contains "test" --status READY
```

## CLI Reference

### list - List deployments

```bash
langstar graph list [OPTIONS]

Options:
  -l, --limit <N>              Max to return [default: 20]
      --offset <N>             Pagination offset [default: 0]
      --name-contains <STR>    Filter by name substring
      --status <STATUS>        Filter: READY, AWAITING_DATABASE, UNUSED, etc.
      --deployment-type <TYPE> Filter: dev_free, dev, prod
  -f, --format <FORMAT>        Output: text, json [default: text]
```

### get - Get deployment details

```bash
langstar graph get <DEPLOYMENT_ID>
```

Returns full deployment JSON including source config, status, timestamps, and revisions.

### delete - Delete deployment

```bash
langstar graph delete <DEPLOYMENT_ID> [OPTIONS]

Options:
  -y, --yes    Skip confirmation prompt
```

## Best Practices

### Environment Variables

✅ **Check before sourcing**
```bash
if [ -z "$LANGSMITH_API_KEY" ]; then
    source /workspace/.devcontainer/.env
fi
```

✅ **Never expose values**
```bash
[ -n "$LANGSMITH_API_KEY" ] && echo "✓ Set" || echo "✗ Not set"
```

### Deployment Deletion

✅ **Review before deleting**
```bash
# List first, verify, then delete
langstar graph list --name-contains "test"
langstar graph delete <id> --yes
```

✅ **Interactive confirmation for batch**
```bash
# Confirm each deletion
for id in $ids; do
    read -p "Delete $id? (y/n): " confirm
    [ "$confirm" = "y" ] && langstar graph delete "$id" --yes
done
```

### Filtering

✅ **Use specific patterns**
```bash
# Specific reduces false matches
langstar graph list --name-contains "langstar-test-"
```

✅ **Combine filters for precision**
```bash
langstar graph list --name-contains "test" --status READY --deployment-type dev_free
```

## Common Use Cases

### Clean Up After Integration Tests

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi

# List test deployments
langstar graph list --name-contains "langstar-test"
langstar graph list --name-contains "test-deployment"

# Delete each
langstar graph delete <id-1> --yes
langstar graph delete <id-2> --yes
```

### Find Unused Deployments

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi

# List unused
langstar graph list --status UNUSED --limit 100

# Review and delete manually
langstar graph list --limit 100 --format json | \
    jq '.resources[] | select(.status == "UNUSED") | {name, id, created_at, status}'
```

### Filter by User/CI Pattern

```bash
# Source credentials
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi

# Filter by username/CI prefix
langstar graph list --name-contains "alice-"
langstar graph list --name-contains "ci-build-"
langstar graph list --name-contains "pr-"
```

## Troubleshooting

### "Authentication failed"

**Diagnosis:**
```bash
[ -n "$LANGSMITH_API_KEY" ] && echo "Set" || echo "Not set"
[ -n "$LANGSMITH_WORKSPACE_ID" ] && echo "Set" || echo "Not set"
```

**Solution:**
```bash
source /workspace/.devcontainer/.env
# Verify
[ -n "$LANGSMITH_API_KEY" ] && echo "Set" || echo "Not set"
```

### "Deployment not found"

**Cause:** Deployment deleted or incorrect ID.

**Solution:**
```bash
# Verify ID from list
langstar graph list --limit 100
langstar graph list --name-contains "<name-fragment>"
```

### No Deployments Returned

**Solution:**
```bash
# Try without filters
langstar graph list --limit 100

# Try broader patterns
langstar graph list --name-contains "test"
```

## Additional Resources

- **[Batch Cleanup Examples](references/batch-cleanup.md)** - Non-interactive deletion scripts
- **[CLI Command Reference](references/cli-reference.md)** - Detailed command documentation
- **Issue #188** - Original feature request
- **Issue #186** - Context for orphaned deployments
- **SDK** - `sdk/src/deployments.rs` - Full API client
- **CLI** - `cli/src/commands/graph.rs` - Implementation

## Integration

### With test-runner-worktree Skill

Clean up after test runs:

```bash
# After integration tests
cd /workspace/wip/<worktree-name>
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi
langstar graph list --name-contains "langstar-test"
```

### With git-worktrees Skill

Works in any location - credentials source the same:

```bash
# Works in main or worktree
cd /workspace
# or
cd /workspace/wip/claude-188-deployment-management

# Source once
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi
langstar graph list
```

## Quick Reference Templates

### Environment Check

```bash
if [ -z "$LANGSMITH_API_KEY" ] || [ -z "$LANGSMITH_WORKSPACE_ID" ]; then
    source /workspace/.devcontainer/.env
fi
[ -n "$LANGSMITH_API_KEY" ] && echo "✓" || echo "✗"
```

### List Test Deployments

```bash
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi
langstar graph list --name-contains "test" --limit 100
```

### Interactive Batch Delete

```bash
if [ -z "$LANGSMITH_API_KEY" ]; then source /workspace/.devcontainer/.env; fi
for id in $(langstar graph list --name-contains "test" --format json | jq -r '.resources[].id'); do
    langstar graph get "$id" | jq '{name, status, created_at}'
    read -p "Delete? (y/n): " confirm
    [ "$confirm" = "y" ] && langstar graph delete "$id" --yes
done
```

## Key Takeaways

1. Check environment variables before sourcing
2. Never expose credential values
3. Review deployments before batch deletion
4. Use specific name patterns
5. Combine filters for precision
6. Interactive confirmation prevents accidents
7. CLI handles all operations - no direct API calls needed
