---
name: azure-devops
description: On-demand Azure DevOps operations (PRs, work items, pipelines, repos) using context-efficient patterns. Loaded only when needed to avoid polluting Claude context with 50+ MCP tools.
---

# Azure DevOps (On-Demand)

Context-efficient Azure DevOps operations without loading all MCP tools into context.

## Core Concept

Use REST API helpers and Python scripts to interact with Azure DevOps only when needed. Results are filtered before returning to context.

## Prerequisites

Environment variables must be set:
```bash
export AZURE_DEVOPS_PAT="your-personal-access-token"
export AZURE_DEVOPS_ORGANIZATION="emstas"
export AZURE_DEVOPS_PROJECT="Program Unify"
```

## Available Operations

### Pull Request Operations

```python
from scripts.ado_pr_helper import ADOHelper

ado = ADOHelper()

# Get PR details
pr = ado.get_pr(5860)
print(pr["title"])
print(pr["mergeStatus"])

# Check for merge conflicts
conflicts = ado.get_pr_conflicts(5860)
if conflicts.get("value"):
    print(f"Found {len(conflicts['value'])} conflicts")

# Get PR discussion threads
threads = ado.get_pr_threads(5860)

# Get PR commits
commits = ado.get_pr_commits(5860)
```

### CLI Usage

```bash
# Get PR details and check conflicts
python3 .claude/skills/mcp-code-execution/scripts/ado_pr_helper.py 5860
```

## Context Efficiency

**Without this approach:**
- Loading ADO MCP server → 50+ tools in context
- Each tool definition → 200-500 tokens
- Total: 10,000-25,000 tokens just for tool definitions

**With this approach:**
- Only load specific helper when needed
- Filter results before returning to context
- Return summaries instead of full data
- Total: 500-2,000 tokens for actual work

## Common Workflows

### Review and Fix PR Conflicts

```python
# 1. Get PR details and conflicts
ado = ADOHelper()
pr = ado.get_pr(pr_id)
conflicts = ado.get_pr_conflicts(pr_id)

# 2. Filter to only conflict info (don't load full PR data)
conflict_files = [c["conflictPath"] for c in conflicts.get("value", [])]

# 3. Return summary to context
print(f"PR {pr_id}: {pr['mergeStatus']}")
print(f"Conflicts in: {', '.join(conflict_files)}")
```

### Query Work Items

```python
# TODO: Add work item helper functions
```

### Pipeline Operations

```python
# TODO: Add pipeline helper functions
```

## Extending Functionality

To add more ADO operations:

1. Add methods to `ado_pr_helper.py` or create new helper files
2. Follow the pattern: fetch → filter → return summary
3. Use REST API directly for maximum efficiency
4. Document new operations in this skill file

## REST API Reference

Base URL: `https://dev.azure.com/{organization}/{project}/_apis/`

API Version: `7.1`

Authentication: Basic auth with PAT

See: https://learn.microsoft.com/en-us/rest/api/azure/devops/
