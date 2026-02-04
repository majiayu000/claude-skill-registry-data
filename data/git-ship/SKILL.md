---
name: git-ship
description: Complete git workflow automation - commit, push, create PR, wait for CI, fetch results, merge. Use when you need to ship changes with proper commits and PR descriptions.
---

# Git Ship Skill

Automate the complete git workflow from commit to merged PR.

## What This Skill Does

- **Review changes** and summarize what's being shipped
- **Create commits** with conventional format
- **Push and create PRs** with structured descriptions
- **Wait for CI** with configurable timeout
- **Fetch results** including CI status, comments, reviews
- **Merge PRs** with strategy selection and branch cleanup

## Commands

| Command | Description |
|---------|-------------|
| `ship` | Workflow: commit → push → PR → CI wait → results |
| `ship full` | Full workflow including merge after CI passes |
| `ship commit` | Review changes and create conventional commit |
| `ship pr` | Push branch and create PR with good description |
| `ship wait` | Wait for CI checks on current PR |
| `ship status` | Fetch CI status and PR comments |
| `ship merge` | Merge PR with strategy selection and cleanup |

## Prerequisites

- Git repository with remote configured
- GitHub CLI (`gh`) installed and authenticated
- Feature branch (not main/master)

## Usage

### Standard Ship Workflow

```bash
bash ${SKILL_DIR}/scripts/ship.sh ship
```

### Full Workflow with Merge

```bash
bash ${SKILL_DIR}/scripts/ship.sh full --merge squash
```

### With Plan Reference (better PR descriptions)

```bash
bash ${SKILL_DIR}/scripts/ship.sh ship --plan plans/my-feature.md
```

### Custom CI Wait Time

```bash
bash ${SKILL_DIR}/scripts/ship.sh ship --wait 10m
```

### Merge Strategies

```bash
# Squash and merge (default)
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy squash

# Create merge commit
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy merge

# Rebase and merge
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy rebase
```

### Auto-Merge (for repos with branch protection)

```bash
bash ${SKILL_DIR}/scripts/ship.sh merge --auto-merge --strategy squash
```

## Process

### 1. Review Changes

First, understand what's being shipped:

```bash
bash ${SKILL_DIR}/scripts/ship.sh commit
```

The script will show:
- Staged changes
- Unstaged changes
- Untracked files

Analyze:
- Files modified, added, deleted
- Logical grouping of changes
- What type of change (feat, fix, docs, etc.)

### 2. Generate Commit Message

Based on the changes, generate a conventional commit message:

```
<type>(<scope>): <description>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** feat, fix, docs, style, refactor, perf, test, build, ci, chore

**Guidelines:**
- Use imperative mood: "add" not "added"
- Keep subject under 50 characters
- Body explains "why" not "what"
- Reference issues if applicable

**Execute:**
```bash
git add .
git commit -m "$(cat <<'EOF'
feat(module): add new capability

Detailed explanation of why this change was made.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 3. Push and Create PR

```bash
# Push branch
BRANCH=$(git branch --show-current)
git push -u origin "$BRANCH"

# Create PR with structured description
gh pr create --title "feat(module): add new capability" --body "$(cat <<'EOF'
## Summary
- What was changed
- Why it was needed
- Key decisions made

## Type of Change
- [x] New feature

## Testing
- Tests added/modified
- Manual testing performed

## Related Issues
Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 4. Wait for CI

```bash
# Wait with default timeout (8 minutes)
bash ${SKILL_DIR}/scripts/ship.sh wait

# Or with custom timeout
bash ${SKILL_DIR}/scripts/ship.sh wait --wait 10m
```

**Exit codes:**
- `0` - All checks passed
- `1` - Checks failed
- `2` - Timeout

### 5. Fetch Results

```bash
bash ${SKILL_DIR}/scripts/ship.sh status
```

Reports:
- CI check status (passed/failed/pending)
- PR comments
- Review status (approved/changes requested/pending)

### 6. Merge PR

```bash
# Squash and merge (default, recommended)
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy squash

# Create merge commit
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy merge

# Rebase and merge
bash ${SKILL_DIR}/scripts/ship.sh merge --strategy rebase

# Enable auto-merge (for branch protection)
bash ${SKILL_DIR}/scripts/ship.sh merge --auto-merge --strategy squash
```

**What happens on merge:**
1. Checks if PR is mergeable (no conflicts)
2. Merges with selected strategy
3. Deletes remote branch (unless --no-delete-branch)
4. Switches to main/master locally
5. Pulls latest changes
6. Deletes local feature branch

## Output Format

### After Ship Complete

```markdown
## Ship Results

**PR:** #123 - https://github.com/org/repo/pull/123
**Branch:** feature/my-feature

### Commit
feat(module): add new capability

### CI Status
✓ build (passed)
✓ test (passed)
✓ lint (passed)

### Reviews
- @reviewer1: APPROVED
- @reviewer2: CHANGES_REQUESTED

### Comments
- [@reviewer2] Please fix the typo on line 42

### Next Steps
- [ ] Address review comments
- [ ] Re-request review after fixes
```

### After Merge Complete

```markdown
## Merge Results

**PR:** #123 - MERGED
**Strategy:** squash
**Branch:** feature/my-feature → deleted

### Cleanup
✓ Remote branch deleted
✓ Switched to main
✓ Pulled latest changes
✓ Local branch deleted

### Summary
Your changes are now on main!
```

## Error Handling

### Not on Feature Branch

```
Error: Cannot ship from main. Create a feature branch first.
Suggestion: git checkout -b feat/my-feature
```

### Push Failed

```
Error: Push failed. Possible causes:
- Remote branch has new commits (git pull --rebase)
- No push access (check permissions)
- Branch protection rules
```

### CI Timeout

```
Warning: CI checks still running after 8 minutes.
Current status:
- build: ✓ passed
- test: ⏳ running (12m elapsed)

Options:
1. Continue waiting: ship wait --wait 15m
2. Check GitHub Actions: gh run view
3. Enable auto-merge: ship merge --auto-merge
```

### Merge Conflicts

```
Error: PR has merge conflicts.

To resolve:
1. git fetch origin
2. git rebase origin/main
3. Resolve conflicts in your editor
4. git add <resolved-files>
5. git rebase --continue
6. git push --force-with-lease
7. ship merge --strategy squash
```

### Auto-Merge Not Available

```
Warning: Auto-merge not available.

Auto-merge requires branch protection rules. Either:
1. Enable branch protection in repo settings
2. Wait for CI manually: ship wait
3. Merge manually: ship merge
```

## Integration

This skill integrates with:
- `/workflows:work` - Used in Phase 4 (Ship It)
- `conventional-commits` hook - Validates commit format
- `pr-comment-resolver` agent - Resolves PR feedback
- `git-worktree` skill - For parallel development

## Troubleshooting

### "No PR found for current branch"

Create a PR first:
```bash
bash ${SKILL_DIR}/scripts/ship.sh pr
```

### "gh CLI not authenticated"

Run:
```bash
gh auth login
```

### Want to skip CI wait?

Just create the PR without waiting:
```bash
bash ${SKILL_DIR}/scripts/ship.sh pr
```

Then check status later:
```bash
bash ${SKILL_DIR}/scripts/ship.sh status
```
