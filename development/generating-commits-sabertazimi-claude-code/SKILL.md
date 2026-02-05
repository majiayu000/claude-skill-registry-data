---
name: generating-commits
description: Generates Conventional Commits messages, then commits changes. Use when the user says "commit", "git commit", or asks to commit changes, wants to create a commit, or when work is complete and ready to commit.
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*), Bash(git commit:*)
license: MIT
---

# Generating Commits

Generate Conventional Commits messages and commit changes.

## When to Use This Skill

Activate this skill when:

- The user types "commit" or "git commit" (with or without slash command)
- The user says "commit this" or "let's commit"
- The user asks to create a commit message
- Work is complete and ready to commit
- The user mentions committing or pushing changes

## Critical Rules

**MUST NEVER** add co-author or mention Claude Code in commit messages

## Workflow

### 1. Check Project Preferences

Read `CLAUDE.md` for commit preferences. Look for sections mentioning:

- Commit format/style guidelines
- Scope requirements (required/optional/omitted)
- Body requirements (required/optional/omitted)
- Preferred type values

If no preferences defined, use default Conventional Commits format.

### 2. Gather Context

Collect information about the current git state:

```bash
# Current git status
git status

# Current git diff (staged changes)
git diff --staged

# Recent commits for context
git log --oneline -10

# Current branch
git branch --show-current
```

### 3. Generate Message Candidates

Analyze the diff content to understand the nature and purpose of the changes.
Generate 3 commit message candidates based on the changes:

- Each candidate should be concise, clear, and capture the essence of the changes
- Follow Conventional Commits format, **adapting to user preferences discovered in step 1** (scope, body, type requirements)

**Format:**

```gitcommit
type(scope): concise subject line describing what changed

[Summary of the modifications]
```

### 4. Execute Commit

**IMPORTANT: Do not use `git add -A` or `git add .`**
Commit only the files that are already staged and understood.

Select best candidate, explain reasoning of your choice, then commit with heredoc (for multi-line messages):

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line

[modifications summary]
EOF
)"
```

## Important Notes

- **Use heredoc for multi-line commits** - Ensures proper formatting
- **Be specific** in summaries
- **Think about the reader** - someone explaining this code repository in 6 months
- **No co-authors** - Never add "Co-Authored-By" or mention Claude Code
