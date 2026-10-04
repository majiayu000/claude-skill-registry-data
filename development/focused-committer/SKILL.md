---
name: focused-committer
description: Smart grouping of files for focused commits with detailed conventional commit messages
disable-model-invocation: true
allowed-tools: Bash(git *) Read Grep
---

# Focused Committer

Analyze changes and intelligently group files into focused, well-documented commits. Ensures each commit addresses a single logical concern following conventional commit standards.

## Invocation

- `/focused-committer` - Analyze and commit all changes
- `/focused-committer staged` - Only analyze already-staged changes
- "commit my changes" or "help me commit these files"

## Core Principles

### Commit Scope Rules
- **Single logical change per commit** - all files must contribute to one concern
- **Never bundle unrelated changes** - separate features, fixes, and refactors
- **Tests with implementations** - test files can be grouped with the code they test
- **Prefer smaller commits** - when in doubt, split into multiple commits

### Conventional Commit Format
```
<type>(<scope>): <description>

<body with bullet points>
```

**Types** (in order of precedence):
- `feat` - New feature or enhancement
- `fix` - Bug fix
- `refactor` - Code restructure without functionality change
- `perf` - Performance improvement
- `style` - Formatting, whitespace changes
- `test` - Test-related changes only
- `docs` - Documentation updates
- `build` - Build system or dependency changes
- `chore` - Maintenance tasks

**Message Rules**:
- Use imperative mood: "add" not "added"
- Start with lowercase letter
- No period at end of subject line

## Instructions

### 1. Configure Git Identity

```bash
git config user.name "<Your Name>"
git config user.email "<your@email.com>"
```

### 2. Analyze All Changes

```bash
git branch --show-current
git status --porcelain
git diff --name-only
git diff --staged --name-only
```

### 3. Identify Logical Groupings

**Same Commit** (related changes):
- Component + its test file
- Module + components using it
- Type definition + implementation using it

**Separate Commits** (unrelated changes):
- Bug fix + unrelated new feature
- Dependency updates + feature work
- Formatting changes + logic changes

### 4. Present Proposed Commit Groups

For each group, show: type, scope, files, proposed message, and reasoning.

### 5. Get User Approval

**CRITICAL: Always ask before committing.**

Options for each group:
- "Commit as proposed"
- "Edit message"
- "Split this group"
- "Skip"
- "Merge with next"

### 6. Execute Approved Commits

```bash
git add <specific-files>
git commit -m "$(cat <<'EOF'
type(scope): description

- Bullet point details
EOF
)"
```

### 7. Report Summary

Show all commits created with hashes, descriptions, and file counts.

## What NOT To Do

- Don't commit unrelated files together
- Don't use vague messages like "fix stuff" or "updates"
- Don't skip user approval
- Don't include secrets (.env, API keys, credentials)
- Don't commit broken code
