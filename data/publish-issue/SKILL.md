---
name: publish-issue
description: Publish a plan as a GitHub Issue and create a branch to start implementation
---

# Ship - Publish Plan to GitHub Issue

Convert a finalized plan into a GitHub Issue and set up the branch for implementation.

## When to Use

- After plan mode is complete and user approves the plan
- Claude should run this AUTOMATICALLY when a plan is approved
- Can also be invoked manually with `/ship`

## Workflow

### Step 1: Find the Plan File

Look for the current plan file in `~/.claude/plans/` or check the conversation context for the plan content.

### Step 2: Determine Issue Title

Extract a concise title from the plan. Format: `feat: {brief description}` or `fix: {brief description}`

### Step 3: Create GitHub Issue

```bash
gh issue create \
  --title "feat: {title}" \
  --body "## Summary
{brief 1-2 sentence summary}

## Implementation Plan
{plan content - files to modify, approach, etc.}

## Files to Modify
- path/to/file1.ts
- path/to/file2.ts
" \
  --assignee @me \
  --label "status:in-progress"
```

### Step 4: Parse Issue Number

The `gh issue create` command outputs the issue URL. Extract the issue number from it.

### Step 5: Create Branch

```bash
# Create branch with naming convention
git checkout -b {PROJECT_PREFIX}/issue-{N}-{slug}

# Push to remote
git push -u origin {PROJECT_PREFIX}/issue-{N}-{slug}
```

Branch naming:
- Format: `{PROJECT_PREFIX}/issue-{number}-{brief-slug}`
- Slug: lowercase, hyphens, max 30 chars
- Example: `myproject/issue-15-dark-mode`

### Step 6: Create Worktree (Optional)

If the project uses SQLite databases or parallel development is needed, create a worktree:

```bash
# Use the global worktree CLI (npx auto-installs if needed)
npx @builtby.win/worktree create {N} {slug} --start-server --branch-prefix={PROJECT_PREFIX}
```

Alternatively, if the worktree CLI is installed globally:
```bash
worktree create {N} {slug} --start-server --branch-prefix={PROJECT_PREFIX}
```

If worktree was created, it will:
- Create `.worktrees/issue-{N}-{slug}/` directory
- Snapshot SQLite database(s) for isolated state
- Assign next available port (e.g., 4322)
- Start dev server automatically
- Symlink node_modules to save disk space

### Step 7: Clean Up Plan File

```bash
# Delete the local plan file (now lives in GitHub)
rm ~/.claude/plans/{plan-file}.md
```

### Step 8: Announce

Output:
```
Created issue #{N}: feat: {title}
{Issue URL}

Branch: {PROJECT_PREFIX}/issue-{N}-{slug}
Status: in-progress

Ready to implement!
```

If worktree was created, also include:
```
Worktree created:
  Path: .worktrees/issue-{N}-{slug}
  Port: {PORT}
  Dev server: http://localhost:{PORT} (started)
  Database: {N} snapshot(s)

Navigate to worktree:
  cd .worktrees/issue-{N}-{slug}
```

If worktree was NOT created (user didn't request it), mention availability:
```
💡 Tip: For parallel development with isolated databases, use worktrees:
   npx @builtby.win/worktree create {N} {slug} --start-server
```

## For Existing Issues

If working on an existing issue (user said "work on #N"), update that issue instead:

```bash
# Append plan to existing issue body
gh issue edit {N} --body "$(gh issue view {N} --json body -q '.body')

---

## Implementation Plan (added by Claude)
{plan content}

## Files to Modify
- path/to/file1.ts
"

# Add in-progress label
gh issue edit {N} --add-label "status:in-progress"

# Create branch
git checkout -b {PROJECT_PREFIX}/issue-{N}-{slug}
git push -u origin {PROJECT_PREFIX}/issue-{N}-{slug}

# Create worktree (if project supports it)
# Project-specific command here
```

Output:
```
Updated issue #{N} with implementation plan.
Branch: {PROJECT_PREFIX}/issue-{N}-{slug}
Status: in-progress

Ready to implement!
```

## Configuration

In your project's `CLAUDE.md`, set:

```markdown
## GitHub Workflow Configuration
PROJECT_PREFIX=your-project-name
```

Example configurations:
- `PROJECT_PREFIX=myapp`
- `PROJECT_PREFIX=builtby-win-web`
