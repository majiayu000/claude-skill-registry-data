---
name: Committer
description: This skill should be used when the user asks to "commit", "create a commit", "make a commit", "git commit", "commit these changes", or wants to stage and commit changes to git. Handles staging files, drafting commit messages, following commit conventions, and managing git commits safely.
version: 0.1.0
---

# Committer

This skill provides comprehensive guidance for creating git commits safely and effectively.

## Core Principles

### Git Safety Protocol

**CRITICAL - Always follow these rules:**

- NEVER update the git config
- NEVER run destructive/irreversible git commands (push --force, hard reset, etc.) unless the user explicitly requests them
- NEVER skip hooks (--no-verify, --no-gpg-sign, etc.) unless the user explicitly requests them
- NEVER run force push to main/master, warn the user if they request it
- Avoid git commit --amend. ONLY use --amend when ALL conditions are met:
  1. User explicitly requested amend, OR commit succeeded but hook auto-modified files
  2. HEAD commit was created by you in this conversation (verify: git log -1 --format='%an %ae')
  3. Commit has NOT been pushed to remote (verify: git status shows "Your branch is ahead")
- CRITICAL: If commit FAILED or was REJECTED by hook, NEVER amend - fix the issue and create a NEW commit
- CRITICAL: If you already pushed to remote, NEVER amend unless user explicitly requests it (requires force push)
- NEVER commit changes unless the user explicitly asks for it
- NEVER commit files that likely contain secrets (.env, credentials.json, etc). Warn the user if they specifically request committing those files
- NEVER include any sign, footer, or attribution (like "Co-Authored-By: Claude") in commit messages

### When to Create Commits

Only create git commits when the user explicitly asks, such as:
- "commit these changes"
- "create a commit"
- "make a commit"
- "stage and commit"

Do NOT create commits proactively without user permission.

## Commit Creation Workflow

### Step 1: Analyze Current State

Run these commands in parallel to understand the current state:

```bash
# Check working tree status
git status

# View unstaged changes
git diff

# View staged changes (if any)
git diff --staged

# Check recent commit history for message style
git log --oneline -10
```

### Step 2: Stage Files

Stage the relevant files for commit. Common patterns:

```bash
# Stage all changes
git add .

# Stage specific files
git add path/to/file1 path/to/file2

# Stage by pattern
git add *.js
```

**Important:** Only stage files that are part of the intended commit.

### Step 3: Draft Commit Message

Analyze the staged changes and draft a commit message following these guidelines:

1. **Summarize the nature of the changes:**
   - new feature - Adding wholly new functionality
   - enhancement - Improving existing functionality
   - bug fix - Fixing a bug or issue
   - refactoring - Restructuring code without behavior change
   - test - Adding or modifying tests
   - docs - Documentation changes
   - chore - Maintenance tasks

2. **Format:**
   - Use present tense ("add" not "added")
   - Use imperative mood ("add" not "adds")
   - Focus on "why" rather than "what"
   - Be concise (1-2 sentences for summary)

**Good examples:**
- "Add user authentication with JWT tokens"
- "Fix memory leak in image processing pipeline"
- "Refactor database connection handling for better error recovery"

**Bad examples:**
- "Updated some code" (too vague)
- "Added function to handle clicks" (focuses on what, not why)
- "Fixes bug" (doesn't say which bug or what it did)

3. **Check for sensitive files:**
   - Look for .env, .secrets, credentials.json, keys, etc.
   - Warn user before staging these files

### Step 4: Create the Commit

Use the HEREDOC format for proper message formatting:

```bash
git commit -m "$(cat <<'EOF'
Add user authentication with JWT tokens

Implements secure login using JWT with refresh token rotation.
Includes password validation and session management.
EOF
)"
```

After commit completes, verify success:

```bash
git status
```

### Step 5: Handle Commit Failures

If a commit fails due to pre-commit hooks:

1. **DO NOT amend** the failed commit
2. Read the hook output to understand what failed
3. Fix the issue identified by the hook
4. Stage the fixed files
5. Create a NEW commit with the original message

If hooks auto-modify files after a successful commit:

1. Check if the commit just succeeded
2. Check if the HEAD commit was created by you
3. Check if the commit hasn't been pushed yet
4. If ALL conditions are met, you may amend to include the hook changes

## Pull Request Creation

When the user asks to create a pull request:

### Step 1: Analyze Branch State

Run these commands in parallel:

```bash
# Check branch status and untracked files
git status

# View unstaged changes
git diff

# View staged changes
git diff --staged

# Check if branch tracks remote and is up to date
git branch -vv

# View commit history since divergence from base branch
git log --oneline $(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')..HEAD

# View full diff from base branch
git diff $(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')...HEAD
```

### Step 2: Create PR Summary

Analyze ALL commits in the branch (not just the latest one) to create a comprehensive summary:

1. List main changes across all commits
2. Identify the primary purpose of the PR
3. Note any breaking changes or migration considerations

### Step 3: Push and Create PR

```bash
# Create branch if needed (use current branch name)
git push -u origin HEAD

# Create PR with proper formatting
gh pr create --title "PR title here" --body "$(cat <<'EOF'
## Summary
- First major change
- Second major change
- Third major change

## Test plan
- [ ] Test 1
- [ ] Test 2

EOF
)"
```

## Important Notes

- **Do NOT use the TodoWrite or Task tools** during git operations
- **Do NOT run additional commands** to read or explore code besides git bash commands
- **NEVER use git commands with the -i flag** (interactive mode is not supported)
- **DO NOT push** to the remote repository unless the user explicitly asks for it
- Return the commit hash or PR URL when done so the user can verify

## Common Git Operations

```bash
# View recent commits
git log -5 --oneline

# View commit details
git show <commit-hash>

# Unstage files
git restore --staged <file>

# Discard unstaged changes
git restore <file>
```

## Additional Resources

### Reference Files

- **`references/conventions.md`** - Commit message conventions and examples, including Conventional Commits format and writing guidelines

### Scripts

- **`scripts/analyze-changes.sh`** - Analyze current changes and show commit style reference
