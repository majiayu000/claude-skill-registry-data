---
name: commit
description: Create a git commit with proper message formatting. Use when asked to commit changes, handles sandbox heredoc limitations.
---

# Create Git Commit

Create a git commit with a properly formatted message, working around sandbox heredoc limitations.

## Instructions

### 1. Check what to commit

```bash
# See status
git status

# See staged changes
git diff --cached --stat

# See recent commits for style reference
git log --oneline -5

# Extract Linear ticket ID from branch name (if present)
git branch --show-current | grep -oiE 'thr-[0-9]+' | tr '[:lower:]' '[:upper:]'
```

### 2. Write the commit message to a temp file

The sandbox blocks heredocs, so write the message to a file first using printf:

```bash
# Single-line message
printf '%s\n' 'type: short description' > /tmp/claude/commit-msg.txt

# Multi-line message (each line as a separate argument)
printf '%s\n' \
  'type: short description' \
  '' \
  '- Detail 1' \
  '- Detail 2' \
  '' \
  '🤖 Generated with [Claude Code](https://claude.com/claude-code)' \
  '' \
  'Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>' \
  > /tmp/claude/commit-msg.txt
```

### 3. Stage and commit

```bash
# Stage specific files (never use git add .)
git add path/to/file1.ts path/to/file2.ts

# Commit using the file
git commit -F /tmp/claude/commit-msg.txt
```

### 4. Clean up

```bash
rm /tmp/claude/commit-msg.txt
```

## Commit Message Format

Follow conventional commits with Linear ticket ID when available:

- `feat(THR-XX):` - New feature
- `fix(THR-XX):` - Bug fix
- `refactor(THR-XX):` - Code restructuring
- `docs(THR-XX):` - Documentation
- `test(THR-XX):` - Tests
- `chore(THR-XX):` - Maintenance

If no Linear ticket exists, omit the parenthetical: `feat: description`

Always include the Claude Code attribution at the end:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Common Issues

**Heredoc fails with "can't create temp file":**
This is expected in sandbox mode. Use printf approach instead.

**Special characters in message:**
Use single quotes to prevent shell expansion. For apostrophes, end the quote, add escaped apostrophe, restart quote:

```bash
printf '%s\n' 'Don'\''t do this' > /tmp/claude/commit-msg.txt
```

## Examples

**Simple commit:**

```bash
printf '%s\n' 'fix: correct typo in README' '' '🤖 Generated with [Claude Code](https://claude.com/claude-code)' '' 'Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>' > /tmp/claude/commit-msg.txt
git add README.md && git commit -F /tmp/claude/commit-msg.txt
```

**Multi-line commit:**

```bash
printf '%s\n' \
  'refactor: extract helper function' \
  '' \
  '- Moved validation logic to separate function' \
  '- Added unit tests' \
  '- Updated callers' \
  '' \
  '🤖 Generated with [Claude Code](https://claude.com/claude-code)' \
  '' \
  'Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>' \
  > /tmp/claude/commit-msg.txt
git add src/utils.ts src/utils.test.ts && git commit -F /tmp/claude/commit-msg.txt
```
