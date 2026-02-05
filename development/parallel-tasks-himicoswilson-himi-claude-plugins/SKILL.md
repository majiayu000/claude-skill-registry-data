---
name: parallel-tasks
description: Creates multiple git worktrees and launches parallel Claude sessions for simultaneous task execution. Maximum 3 tasks.
allowed-tools: Bash, AskUserQuestion
---

# Parallel Tasks

Create git worktrees for parallel task execution with separate Claude sessions (macOS only).

## Script

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/wt-parallel.sh" \
  --branches "branch1|branch2" \
  --prompts "prompt1|prompt2"
```

## Workflow

1. **Parse tasks** from user request (maximum 3)
2. **Generate branch names**: `prefix/description` (max 50 chars)
   - Prefixes: `feature/` (default), `bugfix/`, `hotfix/`, `release/`
3. **Confirm with user** via AskUserQuestion before creating anything:
   - Task descriptions
   - Branch names
   - Initial prompts for each Claude session
4. **Execute script** after approval
5. **Report results** - which tasks succeeded/failed

## Examples

**Input**: "Implement user auth and product search at the same time"

**Parsed**:
- Task 1: `feature/user-auth` → "Implement user authentication..."
- Task 2: `feature/product-search` → "Implement product search..."

**Input**: "Fix the login bug and cart calculation issue in parallel"

**Parsed**:
- Task 1: `bugfix/login` → "Fix the login bug..."
- Task 2: `bugfix/cart-calculation` → "Fix the cart calculation issue..."
