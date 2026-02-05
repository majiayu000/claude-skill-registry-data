---
name: process-github-issues
description: Automatically process open GitHub bug reports by spawning subagents that use the frontend-debug skill to fix each issue in isolated branches. This skill should be used when the user wants to systematically address multiple GitHub Issues without context pollution in the main session. Ideal for batch bug-fixing workflows.
---

# Process GitHub Issues Skill

## Overview

This skill automates the processing of open GitHub bug reports by fetching all open issues labeled as "bug" from the current repository, creating a dedicated git branch for each issue, spawning a subagent to fix each issue using the frontend-debug skill, and committing the fixes automatically. This approach keeps the main Claude Code session context clean and focused, allowing efficient processing of multiple issues without context degradation.

## When to Use This Skill

Use this skill when:
- There are multiple open bug reports in GitHub Issues that need to be addressed
- Batch processing of bugs is desired rather than manual one-by-one fixing
- Keeping the main session context clean is important for ongoing work
- Automated branch creation and commit workflow is preferred
- The frontend-debug skill is appropriate for the issues (frontend/UI bugs)

Do NOT use this skill when:
- Issues are not frontend-related (backend, infrastructure, documentation)
- Issues require human judgment or design decisions
- Working directory has uncommitted changes that would conflict
- GitHub CLI is not installed or authenticated

## Prerequisites

Before using this skill, verify:
1. GitHub CLI (`gh`) is installed and authenticated (`gh auth status`)
2. Current directory is a git repository with GitHub remote
3. Working directory is clean (no uncommitted changes)
4. Frontend-debug skill is available at `~/.claude/skills/frontend-debug/`
5. Issues in the repository are labeled with "bug" for bugs

## Main Workflow

### Step 1: Fetch Open Bug Issues

Execute `scripts/get_github_issues.sh` to retrieve all open bug reports:

```bash
bash scripts/get_github_issues.sh
```

The script outputs format: `issue_number|title` (one per line), sorted by issue number.

If no issues are found, report success and exit. Otherwise, proceed to Step 2.

### Step 2: Process Each Issue Sequentially

For each issue returned from Step 1, perform the following sub-steps:

#### 2a. Generate Branch Name

Execute the branch name generator:

```bash
bash scripts/generate_branch_name.sh <issue_number> <title>
```

This produces a sanitized branch name in format: `bug-{number}-{sanitized-title}`

Example: `bug-42-fix-login-button-styling`

#### 2b. Create Git Branch

Ensure the working directory is still clean, then create and checkout the branch:

```bash
git checkout -b <branch_name>
```

Confirm branch creation was successful before continuing.

#### 2c. Fetch Full Issue Details

Execute GitHub CLI to get the complete issue description:

```bash
gh issue view <issue_number>
```

Extract the issue body, comments, and any additional context needed for the fix.

#### 2d. Spawn Subagent to Fix Issue

Use the Task tool to spawn a subagent with the following configuration:

```
description: "Fix GitHub Issue #{number}: {title}"

prompt: "You are a specialized debugging agent tasked with fixing GitHub Issue #{number}.

Issue Title: {title}

Issue Details:
{full_issue_body_from_gh_issue_view}

Your task:
1. Invoke the frontend-debug skill to diagnose and fix this issue
2. You are currently on branch: {branch_name}
3. Make all necessary code changes to resolve the issue
4. Test your changes if applicable
5. When complete, stage all changes with: git add .
6. Commit your changes with: git commit -m \"Fix #{number}: {title}\"
7. Report back when done

Important: Stay focused on this single issue. The main session will handle moving to the next issue."
```

#### 2e. Wait for Subagent Completion

Monitor subagent progress through the Task tool response. The subagent should complete when it has committed changes.

#### 2f. Verify and Return to Main Branch

After subagent completion:

1. Verify commit was made: `git log -1 --oneline`
2. Return to main branch: `git checkout main` (or `git checkout master`)
3. Log completion: "✅ Issue #{number} processed successfully"

Repeat Step 2 for each remaining issue.

### Step 3: Report Summary

After all issues are processed, provide a summary:

```
Summary:
- Total issues processed: {count}
- Branches created: {list of branch names}
- All issues fixed and committed

Next steps:
- Review branches for quality: git branch --list 'bug-*'
- Push branches: git push origin <branch_name>
- Create pull requests: gh pr create --head <branch_name>
```

## Error Handling

### GitHub CLI Issues

- If `gh` not found: Report error with installation instructions (https://cli.github.com/)
- If not authenticated: Report error and suggest running `gh auth login`
- If no repository found: Report error and verify git remote configuration

### Branch Creation Issues

- If working directory dirty: Report error, suggest `git stash` or commit changes first
- If branch exists: Report warning, skip issue or delete and recreate based on context
- If checkout fails: Log error, skip issue, continue to next

### Subagent Issues

- If frontend-debug skill unavailable: Report error, skip issue, continue to next
- If subagent fails: Log failure message with details, skip issue, continue to next
- If no commit made by subagent: Log warning, skip issue, continue to next

**Always continue processing remaining issues unless a critical error occurs.**

## Helper Scripts

### `scripts/get_github_issues.sh`

Fetches open bug reports from GitHub Issues.

- **Arguments**: None
- **Requirements**: Must be run from within repository directory
- **Output**: `issue_number|title` format (one per line), sorted by issue number
- **Exit code**: 0 on success, 1 on error

### `scripts/generate_branch_name.sh`

Generates standardized branch name from issue.

- **Arguments**: `<issue_number> <issue_title>`
- **Output**: Sanitized branch name in format `bug-{number}-{title}`
- **Behavior**: Handles special characters, limits length to 80 chars
- **Exit code**: 0 on success, 1 on error

## Reference Documentation

For detailed workflow information, troubleshooting, and best practices, refer to:

- `references/workflow_guide.md` - Comprehensive workflow documentation with examples

Load this reference when:
- Encountering errors that need detailed troubleshooting
- Need examples of GitHub CLI commands
- Want to understand the complete workflow in depth

## Best Practices

1. **Start with Clean State**: Always verify working directory is clean before starting
2. **One Issue at a Time**: Process issues sequentially to avoid branch conflicts
3. **Preserve Context**: Keep main session focused on orchestration, delegate debugging to subagents
4. **Verify Commits**: Always verify subagent made commits before moving to next issue
5. **Branch Naming**: Use consistent branch names for easy tracking and PR creation
6. **Status Updates**: Provide clear progress updates after each issue completion
7. **Summary Report**: Always provide final summary of work completed

## Limitations

- Only processes issues labeled as "bug"
- Assumes frontend-debug skill is appropriate for all bugs
- Requires clean working directory to start
- Processes issues sequentially (not parallel)
- Requires manual PR creation after processing
- Does not automatically close issues (user should verify fixes first)

## Integration with Other Skills

This skill is designed to work with:
- **frontend-debug**: Primary skill used by subagents for debugging
- **commit**: Could be used for enhanced commit message generation (optional)
- **worktree-management**: For parallel processing in future versions (not yet implemented)
