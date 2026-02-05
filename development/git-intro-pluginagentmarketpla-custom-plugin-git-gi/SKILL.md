---
name: git-intro
description: Introduction to Git version control - what, why, and first steps
sasmp_version: "1.3.0"
bonded_agent: git-mentor
bond_type: PRIMARY_BOND
category: learning
version: "2.0.0"
triggers:
  - what is git
  - git introduction
  - start with git
  - git for beginners
---

# Git Introduction Skill

> **Production-Grade Learning Skill** | Version 2.0.0

**Your first steps into the world of version control.**

## Skill Contract

### Input Schema
```yaml
input:
  type: object
  properties:
    topic:
      type: string
      enum: [what-is-git, why-use-git, installation, first-setup, first-repo]
      default: what-is-git
    os:
      type: string
      enum: [macos, windows, linux, unknown]
      default: unknown
    experience_level:
      type: string
      enum: [complete-beginner, some-coding, used-other-vcs]
      default: complete-beginner
  validation:
    custom: true
    rules:
      - if_unknown_os: detect_from_environment
```

### Output Schema
```yaml
output:
  type: object
  required: [explanation, success]
  properties:
    explanation:
      type: string
      format: markdown
    success:
      type: boolean
    visual_aid:
      type: string
      description: ASCII diagram if applicable
    next_steps:
      type: array
      items:
        type: string
    commands_to_try:
      type: array
      items:
        type: object
        properties:
          command: string
          description: string
          safe: boolean
```

## Error Handling

### Validation Rules
```yaml
parameter_validation:
  topic:
    required: false
    sanitize: lowercase_trim
    fallback: what-is-git
  os:
    required: false
    auto_detect: true
    detection_command: uname -s || ver
```

### Retry Logic
```yaml
retry_config:
  max_attempts: 2
  backoff_ms: [1000, 2000]
  retryable_scenarios:
    - command_timeout
    - os_detection_failed
```

### Fallback Strategy
```yaml
fallback:
  - scenario: installation_failed
    action: provide_manual_instructions
  - scenario: command_not_found
    action: check_path_and_suggest
```

---

## What is Git?

```
    Without Git                    With Git
    ──────────                     ─────────

    report_v1.doc                  report.doc
    report_v2.doc                     │
    report_final.doc                  ├─ commit 1: "Initial draft"
    report_final_v2.doc               ├─ commit 2: "Added intro"
    report_REALLY_final.doc           ├─ commit 3: "Fixed typos"
    report_final_final.doc            └─ commit 4: "Final version"

    Chaos!                         Clean history!
```

## Why Use Git?

| Problem | Git Solution |
|---------|--------------|
| "Which version is latest?" | Single file, full history |
| "I broke everything!" | Time travel to any point |
| "Who changed this?" | Blame/log shows author |
| "Can't work together" | Branches, merge, resolve |
| "Lost my work!" | Every commit is backup |

## Key Concepts

### The Three Areas
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Working Directory    Staging Area      Repository         │
│   (Your Workspace)     (Ready Room)      (Safe Storage)     │
│                                                             │
│       📁 ──────────► 📦 ──────────────► 🏠               │
│              git add        git commit                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Commits = Save Points
```
commit 3 ← (HEAD - You are here)
    ↓
commit 2 ← You can go back
    ↓
commit 1 ← Or even further back!
```

## Installation

### macOS
```bash
# Option 1: Xcode Command Line Tools (recommended)
xcode-select --install

# Option 2: Homebrew
brew install git
```

### Windows
```bash
# Option 1: Git for Windows (recommended)
# Download from https://git-scm.com/download/windows

# Option 2: winget
winget install --id Git.Git -e --source winget
```

### Linux
```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

### Verify Installation
```bash
git --version
# Expected: git version 2.42.0 (or similar)
```

## First-Time Setup

```bash
# Tell Git who you are (REQUIRED)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Optional but recommended
git config --global init.defaultBranch main
git config --global core.editor "code --wait"  # VS Code

# Verify your settings
git config --list
```

## Your First Repository

```bash
# 1. Create a folder
mkdir my-first-project
cd my-first-project

# 2. Initialize Git (creates .git folder)
git init
# Output: Initialized empty Git repository in .../my-first-project/.git/

# 3. Create a file
echo "# My Project" > README.md

# 4. Check status
git status
# Output: Untracked files: README.md

# 5. Stage the file
git add README.md

# 6. Commit (save!)
git commit -m "Initial commit: Add README"

# 7. View history
git log --oneline
```

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                    GIT CHEAT SHEET                         │
├────────────────────────────────────────────────────────────┤
│ START                                                      │
│   git init              Create new repo                    │
│   git clone <url>       Download existing repo             │
│                                                            │
│ DAILY WORK                                                 │
│   git status            What's going on?                   │
│   git add <file>        Stage file                         │
│   git add .             Stage all                          │
│   git commit -m "msg"   Save with message                  │
│                                                            │
│ HISTORY                                                    │
│   git log               View commits                       │
│   git log --oneline     Compact view                       │
│   git diff              See changes                        │
└────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting Guide

### Debug Checklist
```
□ 1. Is Git installed? → git --version
□ 2. Correct version? → Should be 2.x or higher
□ 3. User configured? → git config user.name
□ 4. Editor set? → git config core.editor
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "command not found: git" | Not installed or not in PATH | Reinstall or add to PATH |
| "Author identity unknown" | User not configured | Run git config commands |
| "not a git repository" | Missing .git folder | Run git init |

### Log Patterns
```bash
# Successful init
Initialized empty Git repository in /path/.git/

# Successful commit
[main abc1234] Your message
 1 file changed, 1 insertion(+)
```

---

## Unit Test Template

```bash
#!/bin/bash
# test_git_intro.sh

test_git_installed() {
  git --version > /dev/null 2>&1
  assertEquals 0 $?
}

test_user_configured() {
  name=$(git config user.name)
  assertNotNull "$name"
}

test_init_creates_git_folder() {
  tmpdir=$(mktemp -d)
  cd "$tmpdir"
  git init
  assertTrue "[ -d .git ]"
  rm -rf "$tmpdir"
}
```

---

## Observability

```yaml
logging:
  level: INFO
  events:
    - skill_invoked
    - installation_checked
    - config_verified
    - first_commit_created

metrics:
  - installation_success_rate
  - time_to_first_commit
  - common_error_types
```

---

## Next Steps

After mastering this skill, proceed to:
1. **basic-workflow** - Daily Git operations
2. **git-basics** - Deeper understanding
3. **branching** - Work in parallel

---

*"Every expert was once a beginner. Welcome to Git!"*
