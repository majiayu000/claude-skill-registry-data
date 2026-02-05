---
name: git-basics
description: Git fundamentals - init, add, commit, status, log, and core concepts
sasmp_version: "1.3.0"
bonded_agent: git-mentor
bond_type: PRIMARY_BOND
category: learning
version: "2.0.0"
triggers:
  - git basics
  - git init
  - git commands
---

# Git Basics Skill

> **Production-Grade Learning Skill** | Version 2.0.0

**Essential Git operations for version control mastery.**

## Skill Contract

### Input Schema
```yaml
input:
  type: object
  properties:
    command_focus:
      type: string
      enum: [init, add, commit, status, log, diff, config, all]
      default: all
    detail_level:
      type: string
      enum: [quick, standard, deep]
      default: standard
    include_examples:
      type: boolean
      default: true
  validation:
    sanitize_strings: true
```

### Output Schema
```yaml
output:
  type: object
  required: [content, success]
  properties:
    content:
      type: string
      format: markdown
    success:
      type: boolean
    commands_covered:
      type: array
      items:
        type: object
        properties:
          name: string
          syntax: string
          examples: array
          common_flags: array
    diagrams:
      type: array
      items:
        type: string
```

## Error Handling

### Retry Logic
```yaml
retry_config:
  max_attempts: 2
  backoff_ms: [1000, 2000]
  retryable:
    - timeout
    - network_error
```

### Parameter Validation
```yaml
validation_rules:
  command_focus:
    type: enum
    fallback: all
  detail_level:
    type: enum
    fallback: standard
```

---

## Core Commands Reference

### Repository Initialization

```bash
# Create new repository
git init

# What it creates:
.git/
├── HEAD              # Current branch pointer
├── config            # Repository config
├── hooks/            # Git hooks
├── objects/          # Git object store
└── refs/             # Branch/tag references
```

### File Tracking

```bash
# Check repository status
git status

# Short status format
git status -s
# M  modified
# A  added
# ?? untracked
# D  deleted

# Add files to staging
git add file.txt           # Single file
git add .                  # All files
git add *.js               # Pattern
git add -p                 # Interactive (patch mode)
```

### Committing Changes

```bash
# Commit with message
git commit -m "Add feature"

# Commit with detailed message (opens editor)
git commit

# Amend last commit
git commit --amend

# Skip staging (tracked files only)
git commit -am "Quick fix"
```

### Viewing History

```bash
# Full log
git log

# One line per commit
git log --oneline

# With graph visualization
git log --oneline --graph --all

# Last N commits
git log -5

# File history
git log --follow -- file.txt

# Search commits
git log --grep="bug"
git log --author="Name"
git log --since="2 weeks ago"
```

### Viewing Changes

```bash
# Working directory changes
git diff

# Staged changes
git diff --staged

# Between commits
git diff abc123 def456

# Specific file
git diff HEAD~3 -- file.txt

# Statistics only
git diff --stat
```

## Command Quick Reference

| Command | Purpose | Common Flags | Example |
|---------|---------|--------------|---------|
| `git init` | Create repo | - | `git init` |
| `git clone` | Copy repo | `--depth`, `--branch` | `git clone URL` |
| `git status` | Check state | `-s`, `-b` | `git status -s` |
| `git add` | Stage files | `-p`, `-A` | `git add .` |
| `git commit` | Save changes | `-m`, `--amend` | `git commit -m "msg"` |
| `git log` | View history | `--oneline`, `--graph` | `git log --oneline` |
| `git diff` | See changes | `--staged`, `--stat` | `git diff --staged` |
| `git show` | Show commit | - | `git show abc123` |

## Understanding Git Objects

```
┌─────────────────────────────────────────────────────────┐
│                    GIT OBJECTS                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   BLOB     ─ File content (compressed)                  │
│   TREE     ─ Directory listing (blob + tree refs)       │
│   COMMIT   ─ Snapshot + metadata + parent link          │
│   TAG      ─ Named pointer to commit                    │
│                                                         │
│   commit ─┬─► tree ─┬─► blob (file1.txt)               │
│           │         ├─► blob (file2.txt)               │
│           │         └─► tree (subdir/) ─► blob         │
│           │                                             │
│           └─► parent commit                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuration

### Essential Setup
```bash
# Identity (required)
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# Editor
git config --global core.editor "code --wait"

# Default branch
git config --global init.defaultBranch main

# View all settings
git config --list
git config --global --list
```

### Useful Aliases
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph"
```

## File States

```
┌─────────────────────────────────────────────────────────┐
│                    FILE LIFECYCLE                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Untracked ──────────────────────────────────────►     │
│       │                                                 │
│       │ git add                                         │
│       ▼                                                 │
│   Staged ─────────────────────────────────────────►     │
│       │                                                 │
│       │ git commit                                      │
│       ▼                                                 │
│   Committed/Unmodified ───────────────────────────►     │
│       │                                                 │
│       │ edit file                                       │
│       ▼                                                 │
│   Modified ──────► git add ──► Staged ──► Committed     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## .gitignore Patterns

```gitignore
# Ignore specific file
secret.txt

# Ignore by extension
*.log
*.tmp

# Ignore directory
node_modules/
.cache/

# Negation (don't ignore)
!important.log

# Pattern matching
**/build/       # Any directory named build
doc/**/*.pdf    # PDFs in doc subdirectories
```

---

## Troubleshooting Guide

### Debug Checklist
```
□ 1. Inside repo? → git rev-parse --git-dir
□ 2. Clean state? → git status
□ 3. On right branch? → git branch
□ 4. Files tracked? → git ls-files
```

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| "nothing to commit" | No changes staged | Check git status, use git add |
| "untracked files" | New files not added | git add <files> |
| "Changes not staged" | Modified but not added | git add <files> |
| "detached HEAD" | Checked out commit | git checkout main |

### Log Patterns
```bash
# Normal add output
# (no output = success)

# Normal commit output
[main abc1234] Your message
 2 files changed, 10 insertions(+), 3 deletions(-)
```

---

## Unit Test Template

```bash
#!/bin/bash
# test_git_basics.sh

test_init_works() {
  tmpdir=$(mktemp -d)
  cd "$tmpdir"
  git init
  assertTrue "[ -d .git ]"
  rm -rf "$tmpdir"
}

test_add_stages_file() {
  tmpdir=$(mktemp -d)
  cd "$tmpdir"
  git init
  echo "test" > file.txt
  git add file.txt
  staged=$(git diff --cached --name-only)
  assertEquals "file.txt" "$staged"
  rm -rf "$tmpdir"
}

test_commit_creates_history() {
  tmpdir=$(mktemp -d)
  cd "$tmpdir"
  git init
  git config user.email "test@test.com"
  git config user.name "Test"
  echo "test" > file.txt
  git add file.txt
  git commit -m "test"
  count=$(git log --oneline | wc -l)
  assertEquals 1 "$count"
  rm -rf "$tmpdir"
}
```

---

## Observability

```yaml
logging:
  level: INFO
  events:
    - command_executed
    - file_staged
    - commit_created
    - error_occurred

metrics:
  - commands_per_session
  - staging_patterns
  - commit_frequency
  - error_types
```

---

## Best Practices

1. **Commit Often**: Small, focused commits
2. **Write Clear Messages**: What and why
3. **Review Before Commit**: `git diff --staged`
4. **Use .gitignore**: Keep repo clean
5. **Don't Commit Secrets**: Never!

---

*"Git basics are the foundation of all version control."*
