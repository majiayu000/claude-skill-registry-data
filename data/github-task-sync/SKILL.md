---
name: github-task-sync
description: Synchronise task lists with GitHub Projects using the gh CLI. Use this skill when users want to add tasks, to-dos, or action items to a GitHub repository's project board. The skill can extract tasks from markdown files, user messages, or structured data, then create GitHub issues and add them to projects. It intelligently detects the target repository from git remotes when not explicitly specified.
---

# GitHub Task Synchronisation

Synchronise task lists with GitHub Projects by creating issues and adding them to project boards.

## When to Use This Skill

Use this skill when:
- User wants to add tasks to a GitHub project
- User has a task list (markdown, verbal, or structured) that should become GitHub issues
- User wants to sync a to-do list with their repository's project board
- User mentions "sync tasks", "add to project", "create issues from tasks", or similar phrases

## Prerequisites Check

Before using this skill, verify:

1. **gh CLI installation**: Check if gh CLI is installed and authenticated
   ```bash
   gh auth status
   ```
   If not authenticated, inform user to run: `gh auth login`

2. **Git repository**: For auto-detection, ensure the user is in a git repository with a GitHub remote

## Workflow

### Step 1: Extract Tasks

Identify where tasks are coming from:

**From markdown file with checkboxes:**
```markdown
- [ ] Implement user authentication
- [ ] Add database migrations
- [x] Set up CI/CD (skip completed)
```

**From user message:**
"I need to add these tasks: implement login, fix bug #123, update documentation"

**From structured data:**
User provides JSON or explicit list of tasks.

Parse tasks into a structured format. Each task needs:
- `title` (required): The task description
- `body` (optional): Additional details
- `labels` (optional): Array of label names

### Step 2: Determine Target Repository

Check if user specified a repository:
- Explicit: "sync to myorg/myrepo"
- Implicit: User is working in a git repository

If not specified, attempt auto-detection:

```python
# Use the sync_tasks.py script's auto-detection
# It checks 'origin' remote first, then falls back to first available remote
```

If auto-detection fails, ask user:
"Which GitHub repository should these tasks be added to? (Format: owner/repo)"

### Step 3: Determine Target Project

Check if user specified a project:
- Explicit: "add to project 3"
- Implicit: None specified

If not specified, use first available project:

```python
# The script will automatically find the first project
# This works for most single-project repositories
```

If no projects exist, ask user:
"No projects found for this repository. Would you like me to:
1. Create a new project
2. Specify a different project number
3. Just create the issues without adding to a project?"

### Step 4: Execute Synchronisation

Run the sync script based on the task source:

**For markdown file:**
```bash
python3 scripts/sync_tasks.py --tasks-file /path/to/tasks.md [--repo owner/repo] [--project-number N]
```

**For individual tasks:**
```bash
python3 scripts/sync_tasks.py --task "Task 1" --task "Task 2" [--repo owner/repo] [--project-number N]
```

**For JSON tasks:**
```bash
python3 scripts/sync_tasks.py --json-tasks '[{"title":"Task 1","body":"Details"}]' [--repo owner/repo] [--project-number N]
```

**Script behaviour:**
- Auto-detects repo from git remotes if `--repo` not provided
- Auto-selects first project if `--project-number` not provided
- Creates GitHub issues for each task
- Adds issues to the specified project
- Returns JSON with results

### Step 5: Report Results

Parse the script output and present results clearly:

```python
results = {
  "success": true,
  "repo": "owner/repo",
  "project_number": 1,
  "synced_tasks": [
    {
      "task": {"title": "Task 1"},
      "issue_url": "https://github.com/owner/repo/issues/42"
    }
  ],
  "failed_tasks": []
}
```

Present to user:
- Success summary: "✅ Synced 3 tasks to owner/repo project #1"
- Links to created issues
- Any failures with reasons
- Next steps if applicable

## Error Handling

### gh CLI Not Authenticated
```
Error: gh CLI not installed or not authenticated
```
**Action**: Inform user to run `gh auth login` and offer to help with setup.

### No Repository Found
```
Error: Could not determine GitHub repository
```
**Action**: Ask user to specify repository with `--repo owner/repo` or navigate to git repository.

### No Projects Found
```
Error: No projects found for owner/repo
```
**Action**: 
1. Verify repository exists and user has access
2. Check if projects exist via `gh project list --owner OWNER`
3. Offer to create issues without project, or help create project

### Rate Limiting
If GitHub API rate limits are hit, inform user and suggest:
- Wait for rate limit reset
- Use authenticated requests (already done via gh CLI)
- Batch tasks if doing large syncs

## Examples

### Example 1: Sync markdown task list
User: "Sync the tasks in todos.md to my project"

1. Check gh auth status
2. Read and parse todos.md for `- [ ]` items
3. Detect repo from git remote (or ask if not found)
4. Run: `python3 scripts/sync_tasks.py --tasks-file todos.md`
5. Report: "✅ Created 5 issues and added them to project #1"

### Example 2: Explicit repository and project
User: "Add these tasks to myorg/webapp project 2: fix login bug, update README"

1. Check gh auth status
2. Parse tasks from message
3. Run: `python3 scripts/sync_tasks.py --task "Fix login bug" --task "Update README" --repo myorg/webapp --project-number 2`
4. Report results with issue links

### Example 3: No project specified
User: "Create issues for: refactor auth module, add tests"

1. Check gh auth status
2. Detect repo from git remote
3. Find first project (or ask if none)
4. Run sync with auto-detected parameters
5. Report results

## Tips for Best Results

- **Always verify authentication first** - saves time if gh CLI needs setup
- **Parse task titles concisely** - keep titles under 80 characters when possible
- **Use task bodies for details** - move long descriptions to the body field
- **Suggest labels when appropriate** - e.g., "bug", "enhancement", "documentation"
- **Handle completed tasks** - skip `[x]` items in markdown lists
- **Batch operations** - sync multiple tasks in one script call for efficiency
- **Provide clear feedback** - users appreciate seeing what was created and where

## Advanced: Custom Task Parsing

For complex task formats, parse them into the expected structure before calling the script:

```python
tasks = [
    {
        "title": "Implement feature X",
        "body": "- Requirement 1\n- Requirement 2",
        "labels": ["enhancement", "priority:high"]
    }
]
```

Then pass via `--json-tasks` parameter.

## Reference Documentation

For detailed gh CLI commands and GitHub Projects API patterns, see `references/gh_cli_reference.md`.
