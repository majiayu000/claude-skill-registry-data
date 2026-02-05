---
name: update-github-issue-project-status
description: Update GitHub issue project statuses for single or multiple issues using the GitHub Projects V2 API. Use when needing to programmatically set issue statuses (todo, in_progress, done) in GitHub Projects, especially when the user wants to update project board status or when handling multiple issues at once. Requires GITHUB_PROJECT_PAT or GH_PROJECT_PAT environment variable with project permissions.
---

# Update GitHub Issue Project Status

## Overview

This skill automates updating GitHub issue statuses in GitHub Projects V2. It handles single issues or batch updates for multiple issues simultaneously, managing issue assignment and project status transitions through the GitHub GraphQL API.

## When to Use This Skill

Use this skill when:
- User requests updating issue status in a GitHub Project (e.g., "mark issue 17 as in progress")
- User wants to bulk-update multiple issue statuses (e.g., "mark issues 15, 16, and 17 as done")
- User needs to assign issues while updating status
- User is working with GitHub Projects V2 and needs programmatic status updates
- Local execution requires project permissions that the default token lacks

## Quick Start

### Prerequisites

This skill uses **two separate tokens** with different scopes:

1. **Environment Variables Required:**
   ```bash
   export GITHUB_PROJECT_PAT="ghp_xxxx"      # Classic PAT with project scope (required)
   export GITHUB_PAT="github_pat_xxxx"       # Fine-grained PAT with repo scope (optional)
   ```

2. **Token Scopes:**
   - `GITHUB_PROJECT_PAT` (classic PAT) - Requires `project` scope for project operations
   - `GITHUB_PAT` (fine-grained PAT) - Requires `repo` scope for issue assignment (optional)

3. **Why Two Tokens?**
   GitHub doesn't provide a single token type that supports both project and repository operations:
   - Classic PATs can have `project` scope but can't be fine-grained to a single repo
   - Fine-grained PATs can be repo-specific with `repo` scope but don't support `project` scope

   The script uses `GITHUB_PROJECT_PAT` for all project operations and `GITHUB_PAT` for issue assignment.

4. **Setup Location:**
   Configure in `.devcontainer/.env` (gitignored):
   ```bash
   GITHUB_PROJECT_PAT=your_classic_token_here
   GITHUB_PAT=your_fine_grained_token_here
   ```

### Basic Usage

```bash
# Update single issue to in_progress
./scripts/update-issue-status.sh 17 in_progress codekiln

# Update single issue to done
./scripts/update-issue-status.sh 17 done

# Batch update multiple issues
./scripts/update-issue-status.sh 15,16,17 done

# Set issue back to todo
./scripts/update-issue-status.sh 17 todo
```

## Task Workflows

### Task 1: Update Single Issue Status

When user requests updating a single issue:

1. **Verify environment setup:**
   ```bash
   # Check if required token is set
   if [ -z "$GITHUB_PROJECT_PAT" ] && [ -z "$GH_PROJECT_PAT" ]; then
     echo "Need to set GITHUB_PROJECT_PAT or GH_PROJECT_PAT"
   fi

   # Check if optional token is set (for assignment)
   if [ -z "$GITHUB_PAT" ]; then
     echo "Note: GITHUB_PAT not set - issue assignment will be skipped"
   fi
   ```

2. **Execute the script:**
   ```bash
   cd /workspace/.claude/skills/update-github-issue-project-status
   ./scripts/update-issue-status.sh <issue_number> <status> [assignee]
   ```

3. **Status values:**
   - `todo` - Move to Todo column
   - `in_progress` - Move to In Progress column (optionally assign)
   - `done` - Move to Done column

4. **Example scenarios:**
   - User: "Mark issue 17 as in progress and assign to me"
     ```bash
     ./scripts/update-issue-status.sh 17 in_progress codekiln
     ```

   - User: "Set issue 17 status to done"
     ```bash
     ./scripts/update-issue-status.sh 17 done
     ```

### Task 2: Batch Update Multiple Issues

When user requests updating multiple issues at once:

1. **Format issue numbers as comma-separated list:**
   ```bash
   ./scripts/update-issue-status.sh 15,16,17 done
   ```

2. **The script will:**
   - Process each issue sequentially
   - Report progress for each issue
   - Provide summary of successes and failures
   - Exit with error code if any updates failed

3. **Example output:**
   ```
   Updating issue #15...
     ✓ Successfully updated issue #15

   Updating issue #16...
     ✓ Successfully updated issue #16

   Updating issue #17...
     ✓ Successfully updated issue #17

   ================================
   Summary:
     ✓ Successful: 3
   ================================
   ```

### Task 3: Troubleshooting Authentication

When the script fails with permission errors:

1. **Check token availability:**
   ```bash
   echo "GITHUB_PROJECT_PAT: ${GITHUB_PROJECT_PAT:0:10}..."
   echo "GITHUB_PAT: ${GITHUB_PAT:0:10}..."
   ```

2. **Verify token scopes:**

   **GITHUB_PROJECT_PAT (required):**
   - Type: Classic Personal Access Token
   - Scope: `project`
   - Create at: https://github.com/settings/tokens

   **GITHUB_PAT (optional, for issue assignment):**
   - Type: Fine-grained Personal Access Token
   - Scope: `repo` (or `public_repo` for public repos only)
   - Create at: https://github.com/settings/personal-access-tokens/new

3. **Common errors and solutions:**
   - `"Error: No project token found"` → Set GITHUB_PROJECT_PAT or GH_PROJECT_PAT
   - `"Resource not accessible by personal access token"` → Token lacks required scope
   - `"Skipping assignment (GITHUB_PAT not set)"` → Set GITHUB_PAT if you want issue assignment
   - Assignment fails but project update succeeds → GITHUB_PAT is not set or lacks repo scope

### Task 4: Verifying Updates

After updating issue statuses, verify the changes:

```bash
# Check issue status
gh issue view <issue_number> --json projectItems,assignees

# View project board (web UI)
# Navigate to: https://github.com/users/<owner>/projects/<project_number>
```

## Script Details

### Location

```
/workspace/.claude/skills/update-github-issue-project-status/scripts/update-issue-status.sh
```

### Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| issue_number(s) | Yes | Single issue or comma-separated list | `17` or `15,16,17` |
| status | Yes | Target status | `todo`, `in_progress`, or `done` |
| assignee | No | GitHub username (for in_progress) | `codekiln` |

### Environment Variables

The script uses two separate tokens for different operations:

**For Project Operations (required):**
1. `GITHUB_PROJECT_PAT` (recommended) - Classic PAT with `project` scope
2. `GH_PROJECT_PAT` (alternative name)

**For Issue Assignment (optional):**
- `GITHUB_PAT` - Fine-grained PAT with `repo` scope

**Repository:**
- Hardcoded to `codekiln/langstar` in the script

### What the Script Does

1. **Validates environment** - Ensures required tokens are set
2. **Processes each issue:**
   - Assigns issue using `GITHUB_PAT` (if status is in_progress, assignee provided, and token available)
   - Retrieves issue node ID via GraphQL using `GITHUB_PROJECT_PAT`
   - Finds existing project item or adds issue to project using `GITHUB_PROJECT_PAT`
   - Updates project status field via GraphQL mutation using `GITHUB_PROJECT_PAT`
3. **Reports results** - Shows success/failure for each issue with summary

### Script Behavior

- **Idempotent** - Safe to run multiple times with same parameters
- **Automatic project addition** - Adds issues to project if not already present
- **Atomic per issue** - Each issue update is independent
- **Error handling** - Continues processing remaining issues if one fails
- **Exit code** - Returns non-zero if any updates failed

## Project Configuration

### Hardcoded Project IDs

The script contains hardcoded IDs for the langstar project:

```bash
PROJECT_ID="PVT_kwHOAAImgs4BGe4B"
STATUS_FIELD_ID="PVTSSF_lAHOAAImgs4BGe4Bzg3g-NQ"
STATUS_TODO="f75ad846"
STATUS_IN_PROGRESS="47fc9ee4"
STATUS_DONE="98236657"
```

### Updating for Different Projects

To use this skill with a different GitHub Project:

1. **Find your project IDs** - See `references/project-configuration.md` for GraphQL queries
2. **Edit the script** - Update the ID constants at the top of `scripts/update-issue-status.sh`
3. **Test with a single issue** - Verify before batch updates

For detailed instructions on finding these IDs, load `references/project-configuration.md` into context.

## Integration with GitHub Actions

This skill complements the automated GitHub Actions workflow:

- **GitHub Actions** - Automatically updates status when `@claude` is mentioned or issue closes
- **This Skill** - Manually update statuses for any issue(s) at any time

The script uses the same logic as the GitHub Actions automation but provides manual control and batch capabilities.

## Common Use Cases

### Use Case 1: Starting Work on an Issue

User says: "I'm starting work on issue 17"

Execute:
```bash
./scripts/update-issue-status.sh 17 in_progress $USER
```

### Use Case 2: Closing Multiple Related Issues

User says: "Mark issues 15, 16, and 17 as done"

Execute:
```bash
./scripts/update-issue-status.sh 15,16,17 done
```

### Use Case 3: Resetting Issue Status

User says: "Move issue 17 back to todo"

Execute:
```bash
./scripts/update-issue-status.sh 17 todo
```

### Use Case 4: Project Board Cleanup

User says: "All issues in the 20-25 range are done"

Execute:
```bash
./scripts/update-issue-status.sh 20,21,22,23,24,25 done
```

## Tips for Effective Usage

1. **Set both tokens** - Set GITHUB_PROJECT_PAT (required) and GITHUB_PAT (optional for assignment)
2. **Check environment first** - Verify tokens are set before running
3. **Test with single issue** - Validate configuration before batch updates
4. **Use batch updates carefully** - Double-check issue numbers in comma-separated lists
5. **Assignment requires GITHUB_PAT** - Project updates work without it, but assignment needs it
6. **Verify after updates** - Use `gh issue view` to confirm changes
7. **Keep project IDs updated** - If project is recreated, update the script IDs

## References

This skill includes reference documentation:

- `references/project-configuration.md` - Detailed project configuration, API usage, and how to find/update project IDs

Load reference files into context when needing detailed configuration information or troubleshooting guidance.
