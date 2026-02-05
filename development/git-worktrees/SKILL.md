---
name: git-worktrees
description: |
  Manage git worktrees for parallel branch development and PR reviews.
  Use when asked about: worktrees, working on multiple branches, parallel development,
  PR review without switching, testing without committing, multiple features simultaneously,
  long-running builds, comparing branches side-by-side.
  Integrates with: feature workflow, Azure DevOps work items, GitHub PRs.
---

# Git Worktrees Skill

Manage git worktrees to enable parallel development across multiple branches without stashing or losing context.

## Quick Start

```bash
# Create worktree for work item
worktree create feature 1234

# Create worktree for PR review
worktree create pr 5678

# List all worktrees
worktree list

# Remove worktree
worktree remove <name>

# Clean up merged worktrees
worktree cleanup --merged
```

## Core Concepts

### Base Branch Detection

Worktrees automatically detect the correct base branch for your repository:

- **GitFlow repos** (with `develop` branch): Uses `develop` as base
- **GitHub Flow repos** (with `main` or `master`): Uses `main`/`master` as base

This prevents the common mistake of creating feature branches off `main` when you should be branching from `develop`.

**How it works:**
1. First worktree creation auto-detects and saves to config
2. Subsequent creations use the saved configuration
3. Override per-repo with: `worktree config baseBranch <branch>`
4. Override per-command with: `--base <branch>`

**Example output:**
```
✓ Auto-detected GitFlow workflow → using 'develop' as base
→ Saved to config. Change with: worktree config baseBranch <branch>
```

### What are Git Worktrees?

Git worktrees allow multiple working directories attached to the same repository. Each worktree:
- Has its own working directory and index
- Can have a different branch checked out
- Shares the same `.git` database (no duplication)
- Maintains independent uncommitted changes

**Example:**
```
~/source/projects/
└── my-repo/                              # Main worktree (project directory stays clean)

~/.worktrees/                             # Centralized worktree storage
├── my-repo--feature-AB#1234-add-auth/    # Feature worktree
├── my-repo--review-pr-5678/              # Review worktree
└── other-repo--fix-AB#999-bug/           # From another repo
```

### When to Suggest Worktrees

Claude should **proactively suggest** worktrees when:

1. **User has uncommitted changes and wants to switch context**
   ```
   User: "I need to review PR #5678"
   [Detect: git status shows uncommitted changes]

   Claude: "I see you have uncommitted changes. Instead of stashing, I can create
            a worktree for reviewing PR #5678. This keeps your current work intact.

            Command: worktree create pr 5678"
   ```

2. **User mentions parallel work**
   ```
   User: "I need to work on feature A and B simultaneously"

   Claude: "Perfect use case for worktrees! I'll create separate worktrees for each:

            worktree create feature 1234  # Feature A
            worktree create feature 1235  # Feature B

            You can work on both in different terminal/IDE windows."
   ```

3. **Long-running operations mentioned**
   ```
   User: "The integration tests take 20 minutes and I can't code while they run"

   Claude: "Use worktrees to run tests in one workspace while coding in another:

            worktree create main tests
            cd ../my-repo-tests && npm test &
            cd -  # Back to your main workspace"
   ```

4. **Risky experiments**
   ```
   User: "I want to try refactoring but I'm not sure it'll work"

   Claude: "Create an experimental worktree so your main work stays safe:

            worktree create branch experiment-refactor
            # Try the refactor
            # If it works, merge it; if not, just delete the worktree"
   ```

5. **Branch comparison needed**
   ```
   User: "I need to compare the old implementation with the new one"

   Claude: "Create a worktree for the old version for side-by-side comparison:

            worktree create branch old-implementation
            # Open both in split-screen editors
            diff -r main/ old-implementation/"
   ```

## Common Workflows

### Workflow 1: Parallel Feature Development

**Scenario:** Working on feature A, need to start feature B.

```bash
# Currently on feature/A with uncommitted changes
worktree create feature 1234
# Creates: ../my-repo-feature-AB#1234-feature-b/

# Open in new IDE window
cd ../my-repo-feature-AB#1234-feature-b
code .

# Both features progress independently
# Original window still has feature A with uncommitted changes
```

**Claude's Role:**
- Detect user is on a feature branch with uncommitted changes
- Suggest worktree instead of stashing
- Create worktree and open in IDE
- Remind user they can work in parallel

### Workflow 2: PR Review

**Scenario:** Review a PR without disrupting current work.

```bash
# On feature branch with uncommitted work
worktree create pr 5678
# Creates: ../my-repo-review-pr-5678/

cd ../my-repo-review-pr-5678
# Review, test, comment
npm test
gh pr review 5678 --comment "LGTM"

# Clean up
cd -
worktree remove review-pr-5678
```

**Claude's Role:**
- Detect PR review request
- Suggest worktree to preserve current work
- Fetch PR branch automatically
- Install dependencies in review worktree
- Guide through review process
- Auto-cleanup after review

### Workflow 3: Emergency Hotfix

**Scenario:** Production bug while in middle of feature.

```bash
# On feature/AB#1234 with extensive uncommitted changes
worktree create fix 9999 --base production
# Creates: ../my-repo-fix-AB#9999-from-production/

cd ../my-repo-fix-AB#9999-critical-bug
# Fix bug, test, deploy
feature pr

# Return to feature work (still intact)
cd -

# After hotfix merged
worktree remove fix-AB#9999
```

**Claude's Role:**
- Recognize urgency (keywords: "urgent", "production", "hotfix")
- Create worktree from production branch
- Guide through fix, test, deploy
- Remind user feature work is untouched
- Clean up after merge

### Workflow 4: Monorepo Multi-Service

**Scenario:** Developing multiple services simultaneously.

```bash
# Create worktrees for each service
worktree create feature 1234  # API changes
worktree create feature 1235  # UI changes
worktree create feature 1236  # Worker changes

# Terminal 1: API
cd ../my-repo-feature-AB#1234-api
npm run dev

# Terminal 2: UI (calls API locally)
cd ../my-repo-feature-AB#1235-ui
npm run dev

# Terminal 3: Worker
cd ../my-repo-feature-AB#1236-worker
npm run dev

# All services run simultaneously, test integration
```

**Claude's Role:**
- Recognize monorepo multi-service scenario
- Create worktrees for each service
- Suggest terminal/IDE organization
- Guide through integration testing
- Coordinate PR creation for all services

## Command Reference

### `worktree create <type> <identifier> [options]`

Creates a new worktree with smart defaults.

**Types:**
- `feature <work-item-id>` - Create from Azure DevOps work item
- `fix <work-item-id>` - Create fix branch from work item
- `pr <pr-id>` - Create from PR (GitHub or Azure DevOps)
- `branch <branch-name>` - Create from arbitrary branch
- `base [name]` - Create additional worktree from base branch (develop/main)

**Options:**
- `--path <path>` - Custom path (default: auto-generated)
- `--base <branch>` - Override base branch (default: auto-detected)
- `--no-deps` - Skip dependency installation
- `--ide <ide>` - Open in IDE (code, rider, idea, pycharm, webstorm, goland, auto, none)

**Examples:**

```bash
# From work item (fetches title from Azure DevOps)
worktree create feature 1234

# For PR review
worktree create pr 5678

# From specific branch
worktree create branch release/v2.0

# Custom path and no deps
worktree create feature 1234 --path ~/workspace/auth --no-deps
```

**Integration with Feature Workflow:**
- Uses same `feature_workflow.py` to fetch work item titles
- Creates branches with same naming: `feature/AB#1234-title`
- Pre-commit hooks work automatically in all worktrees
- `feature pr` works from any worktree

### `worktree list [options]`

Lists all worktrees with status.

**Options:**
- `--verbose, -v` - Show detailed information
- `--json` - Output as JSON
- `--stale` - Show only stale worktrees

**Example Output:**

```
Current worktrees:
  main                          [main] (clean)
    /Users/sean/source/my-repo

  feature-AB#1234-auth          [feature/AB#1234-add-authentication] (3 uncommitted)
    /Users/sean/source/my-repo-feature-AB#1234-auth
    Work Item: AB#1234
    Ahead: 2 commits | Behind: 0 commits

  review-pr-5678               [pr/5678-fix-validation] (clean)
    /Users/sean/source/my-repo-review-pr-5678
    PR: #5678
    Age: 2 days
```

**Claude's Role:**
- Parse output to understand current worktree state
- Suggest cleanup for stale worktrees
- Identify which worktree user is currently in

### `worktree remove <name> [options]`

Removes a worktree with safety checks.

**Options:**
- `--force` - Force removal even with uncommitted changes
- `--keep-branch` - Don't delete the branch

**Safety Checks:**
1. Warns if uncommitted changes exist
2. Warns if unpushed commits exist
3. Offers to commit, stash, or create backup branch
4. Confirms before deletion

**Claude's Role:**
- Guide user through safety prompts
- Suggest committing valuable work
- Create backup branches for important work
- Track which worktrees have been removed

### `worktree cleanup [options]`

Cleans up stale worktrees.

**Options:**
- `--dry-run` - Show what would be removed
- `--merged` - Remove worktrees for merged branches
- `--stale <days>` - Remove worktrees inactive for N days
- `--all` - Remove all non-main worktrees

**Example:**

```bash
# See what would be cleaned
worktree cleanup --dry-run

# Remove merged worktrees
worktree cleanup --merged

# Remove worktrees untouched for 7+ days
worktree cleanup --stale 7
```

**Claude's Role:**
- Periodically suggest cleanup (e.g., after PR merges)
- Show dry-run first for transparency
- Confirm before bulk deletions
- Report what was cleaned up

### `worktree status [name]`

Shows detailed status of a worktree.

**Example Output:**

```
Worktree: feature-AB#1234-add-authentication
Path: /Users/sean/source/my-repo-feature-AB#1234-auth
Branch: feature/AB#1234-add-authentication
Work Item: AB#1234 - Add authentication system

Status:
  3 files modified
  1 file staged
  0 untracked files

Commits:
  2 ahead of main
  0 behind main

Remote:
  Up to date with origin/feature/AB#1234-add-authentication

Dependencies:
  node_modules: 1234 packages (shared with main)
  .venv: Python 3.11 (isolated)

Disk usage: 45 MB (excluding shared)
Last active: 2 hours ago
Created: 2025-12-15 14:30
```

### `worktree sync <name> [options]`

Synchronizes a worktree with its remote.

**Options:**
- `--rebase` - Use rebase instead of merge
- `--all` - Sync all worktrees

**Claude's Role:**
- Suggest syncing before starting work
- Detect when worktrees are behind
- Handle merge conflicts gracefully
- Report sync results

### `worktree open <name> [options]`

Opens a worktree in an IDE.

**Options:**
- `--ide <ide>` - IDE to use (code, idea, pycharm, auto)
- `--new-window` - Force new window

**Supported IDEs:**
- `code` - Visual Studio Code
- `idea` - IntelliJ IDEA
- `pycharm` - PyCharm
- `rider` - JetBrains Rider

**Claude's Role:**
- Auto-detect IDE from project markers (`.vscode`, `.idea`)
- Open worktrees in new windows for clarity
- Suggest IDE layout for multi-worktree workflows

## Claude Integration Patterns

### 1. Context Detection

**Before any worktree operation, Claude should check:**

```bash
# Current repository state
git rev-parse --show-toplevel

# Uncommitted changes
git status --porcelain

# Current branch
git rev-parse --abbrev-ref HEAD

# Existing worktrees
worktree list --json
```

**Use this to:**
- Determine if worktrees are appropriate
- Suggest worktree vs. stash vs. commit
- Identify which worktree user is in

### 2. Proactive Suggestions

**When to suggest worktrees:**

```python
# Pseudo-code for Claude's decision logic

if user.mentions("review PR") and git.has_uncommitted_changes():
    suggest("Create a worktree for PR review to preserve your work")
    command("worktree create pr <PR_ID>")

if user.mentions("multiple features", "parallel work"):
    suggest("Use worktrees for independent development")
    command("worktree create feature <ID_1>")
    command("worktree create feature <ID_2>")

if user.mentions("experiment", "try something", "not sure"):
    suggest("Create an experimental worktree for safe exploration")
    command("worktree create branch experiment-<name>")

if user.mentions("hotfix", "urgent", "production bug") and on_feature_branch():
    suggest("Create a hotfix worktree from production")
    command("worktree create fix <ID> --base production")
```

### 3. Progress Tracking

**For long-running operations, provide progress:**

```
→ Creating worktree for AB#1234...
  ✓ Fetched work item: "Add authentication system"
  ✓ Created worktree at: ../my-repo-feature-AB#1234-add-authentication
  ✓ Checked out branch: feature/AB#1234-add-authentication
  → Installing dependencies (this may take a minute)...
  ✓ Installed 1,234 packages
  ✓ Opened in VS Code

Done! Your worktree is ready.

Next steps:
  cd ../my-repo-feature-AB#1234-add-authentication
  # Make your changes
  git commit -am "Your message"  # AB#1234 auto-appended
  feature pr  # Create pull request
```

### 4. Error Recovery

**Common errors and Claude's responses:**

**Error: Path already exists**
```
Error: Path '/path/to/worktree' already exists

Claude: "That worktree path is occupied. I can:
         1. Use a different name: worktree create feature 1234 --path custom-name
         2. Remove existing: worktree remove <name>
         3. List existing: worktree list

         What would you prefer?"
```

**Error: Branch doesn't exist**
```
Error: Branch 'feature/AB#9999' not found

Claude: "That branch doesn't exist yet. I'll create a new one:
         worktree create feature 9999

         This will fetch the work item title from Azure DevOps and create
         the branch."
```

**Error: Uncommitted changes in target path**
```
Error: Cannot create worktree - path has uncommitted changes

Claude: "The target path has uncommitted changes from a previous worktree.
         Let me clean that up:

         worktree cleanup --stale

         Then I'll create the new worktree."
```

### 5. Teaching Opportunities

**After successful operations, educate users:**

```
✓ Worktree created successfully!

Pro tip: You can now work on this feature in one terminal/IDE window while
keeping your main branch available in another. No more stashing or losing context!

To switch back: cd -
To see all worktrees: worktree list
To clean up when done: worktree remove <name>
```

**When user struggles with stashing:**
```
"I notice you're using git stash frequently. Worktrees might simplify your workflow.

Instead of:
  git stash          # Save changes
  git checkout other-branch
  # ... work ...
  git checkout -
  git stash pop      # Restore changes

You could:
  worktree create branch other-branch
  cd ../other-branch
  # ... work ...
  cd -               # Still has your changes!

Would you like me to show you how?"
```

## Safety Guidelines

### What Claude Should Always Check

1. **Before creating worktree:**
   - Repository is valid git repo
   - Enough disk space available
   - Path doesn't already exist
   - Branch exists or can be created

2. **Before removing worktree:**
   - Uncommitted changes are handled
   - Unpushed commits are safe
   - User confirms deletion
   - Branch fate is decided (keep or delete)

3. **Before cleanup:**
   - Show what will be removed
   - Dry-run first for transparency
   - Confirm bulk operations
   - Preserve important work

### What Claude Should Never Do

1. **Never force-delete without warning:**
   - Always show what will be lost
   - Offer alternatives (commit, stash, backup branch)
   - Require explicit user confirmation

2. **Never create worktrees in inappropriate locations:**
   - Validate path is outside existing worktrees
   - Check parent directory exists
   - Ensure no naming conflicts

3. **Never proceed with broken state:**
   - Detect and repair broken worktrees first
   - Clean up stale entries before creating new ones
   - Validate git state is consistent

## Configuration

### Default Configuration

Located at `.git/worktree/config.json` (shared across worktrees):

```json
{
  "version": "1.0",
  "basePath": "~/.worktrees",
  "baseBranch": null,
  "branchingStrategy": null,
  "defaultIDE": "auto",
  "autoInstallDeps": true,
  "autoCleanup": false,
  "staleThresholdDays": 7,
  "sharedDeps": ["node_modules", ".npm"],
  "isolatedDeps": [".venv", "venv", "target", "bin", "obj"]
}
```

**Key settings:**
- `baseBranch` - The default branch for new worktrees (auto-detected on first use)
- `branchingStrategy` - Detected workflow: "gitflow", "github-flow", or "trunk"

### Get/Set Configuration

```bash
# View all settings
worktree config

# Set base branch (for GitFlow repos)
worktree config baseBranch develop

# Set base branch (for GitHub Flow repos)
worktree config baseBranch main

# View current base branch setting
worktree config baseBranch

# Set default IDE
worktree config defaultIDE rider

# Enable auto-cleanup
worktree config autoCleanup true

# Set stale threshold
worktree config staleThresholdDays 14
```

## Troubleshooting

### Common Issues

**Issue: "Worktree already exists"**
```
Cause: Worktree path is occupied
Fix: worktree list  # Find existing worktrees
     worktree remove <name>  # Remove old one
     worktree create ...  # Try again
```

**Issue: "Branch not found"**
```
Cause: Branch doesn't exist locally
Fix: git fetch  # Fetch from remote
     worktree create branch <name>  # Try again
```

**Issue: "Index locked"**
```
Cause: Git operation in progress in worktree
Fix: Complete or abort the operation:
     cd /path/to/worktree
     git status  # Check what's happening
     git rebase --abort  # Or git merge --abort
```

**Issue: Broken worktrees after manual deletion**
```
Cause: Worktree directory deleted outside of git
Fix: git worktree prune  # Clean up broken references
```

### When to Use Repair Commands

```bash
# Detect broken worktrees
git worktree list
# Look for: "(missing)" or "(error)"

# Prune broken references
git worktree prune

# Verify cleanup
git worktree list
```

## Integration with Existing Workflows

### Feature Workflow

**Seamless integration:**
```bash
# Start feature with worktree
worktree create feature 1234
cd ../my-repo-feature-AB#1234-add-auth

# Work normally
git commit -am "Add login endpoint"
# Pre-commit hook auto-appends AB#1234

# Create PR (feature command works in worktree)
feature pr

# After merge, cleanup
worktree cleanup --merged
```

### Azure DevOps

**Work item integration:**
- Fetches work item titles automatically
- Links work items via pre-commit hooks
- Creates PRs with work item references
- Uses same `.ado/config.json`

### GitHub

**PR integration:**
- Fetches PR branches via `gh` CLI
- Creates review worktrees
- Leaves comments from review worktree
- Cleans up after PR merge

## Best Practices

### When to Use Each Approach

**Use Worktrees:**
✅ Parallel work on multiple features
✅ PR reviews without disrupting work
✅ Long-running operations (builds, tests)
✅ Side-by-side branch comparison
✅ Multiple stable environments

**Use Stash:**
⚠️ Quick, temporary branch switches
⚠️ Single-file quick fixes

**Use New Clone:**
⚠️ Different remote repositories
⚠️ Complete isolation needed

### Directory Organization

**Centralized structure (default):**
```
~/source/projects/                # Your project directories stay clean
├── my-repo/                      # Main worktree only
├── other-repo/
└── another-project/

~/.worktrees/                     # All worktrees in one hidden location
├── my-repo--feature-AB#1234/     # Format: {repo}--{worktree-name}
├── my-repo--review-pr-5678/
├── other-repo--fix-AB#999/
└── another-project--experiment/
```

**Benefits:**
- Project directories stay clean (no clutter)
- All worktrees in one place for easy cleanup
- Hidden from normal file browsing
- Clear naming shows which repo each belongs to

**Custom location:** Set `WORKTREES_BASE` environment variable to change the base directory.

### Dependency Management

**Guidelines:**
- **Isolate by default:** Safest approach
- **Share for short-lived reviews:** Saves disk space
- **Never share virtual environments:** Python `.venv`, Ruby `.bundle`
- **Share package caches:** npm cache, pip cache, NuGet

**Example:**
```bash
# Long-lived feature worktree: Isolate
worktree create feature 1234
# → Full dependency install

# Short-lived PR review: Share (optional)
worktree create pr 5678
# → Can symlink node_modules for speed
```

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════════════╗
║                   GIT WORKTREES QUICK REFERENCE                  ║
╚══════════════════════════════════════════════════════════════════╝

CREATE WORKTREES:
  worktree create feature <ID>          From work item (auto-detects base)
  worktree create pr <ID>               For PR review
  worktree create branch <name>         From branch
  worktree create base stable           Extra copy of base branch

MANAGE WORKTREES:
  worktree list                         List all
  worktree list --stale                 Show cleanup candidates
  worktree status [name]                Detailed status
  worktree sync [name]                  Pull latest changes

CLEAN UP:
  worktree remove <name>                Remove one
  worktree cleanup --merged             Remove merged
  worktree cleanup --stale 7            Remove old (7+ days)

IDE INTEGRATION:
  worktree open <name>                  Open in IDE
  worktree open <name> --ide code       Open in VS Code

CONFIGURE BASE BRANCH:
  worktree config baseBranch            Show current setting
  worktree config baseBranch develop    Set to develop (GitFlow)
  worktree config baseBranch main       Set to main (GitHub Flow)
  worktree create feature 1234 --base main  One-time override

COMMON WORKFLOWS:
  # Parallel features
  worktree create feature 1234
  cd ../my-repo-feature-AB#1234-*

  # PR review
  worktree create pr 5678
  # Review, test
  worktree remove review-pr-5678

  # Emergency hotfix
  worktree create fix 9999 --base production
  # Fix, deploy
  worktree remove fix-AB#9999

INTEGRATION:
  feature pr                            Works in any worktree
  git commit -m "msg"                   AB#ID auto-appended
  worktree cleanup --merged             After PR merges

HELP:
  worktree --help                       Full command help

╚══════════════════════════════════════════════════════════════════╝
```

## Documentation

### Full Documentation

- **Architecture:** `docs/architecture.md` - Design rationale, use cases, tradeoffs
- **Implementation:** `docs/implementation-guide.md` - Command specs, code patterns
- **User Guide:** `docs/user-guide.md` - End-user tutorials and examples
- **Troubleshooting:** `docs/troubleshooting.md` - Common issues and solutions

### Support

For issues or questions:
1. Check `docs/troubleshooting.md`
2. Run `worktree status` to diagnose
3. Use `git worktree list` to see git's view
4. Ask Claude: "Help me debug my worktree setup"

---

**Remember:** Worktrees are powerful but not always necessary. Use them when parallel work provides clear value. For simple branch switches, `git checkout` is still fine.
