---
name: gitflow
description: "Git Flow branching model - a philosophy for versioned releases, implemented with pure git commands (no tools required)"
---

# Git Flow

> **Note on Branch Names**: Examples use default Git Flow naming (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`).
> If your `.gitflow` config uses custom names (e.g., `dev` instead of `develop`), substitute accordingly.

## Philosophy: Branching Model, NOT a Tool

Git Flow is a **branching strategy protocol** - a set of conventions for how to organize your branches. It is NOT dependent on any specific tool.

```
┌─────────────────────────────────────────────────────────┐
│  Git Flow 理念  →  用原生 git实现  ✓                      │
│  Git Flow 工具  →  可选，非必须  (optional)              │
└─────────────────────────────────────────────────────────┘
```

### Core Branch Structure

| Branch | Purpose | Lifetime |
|--------|---------|----------|
| `main`/`master` | Production-ready code | Indefinite |
| `develop` | Integration branch for features | Indefinite |
| `feature/*` | Develop new features | Short-term |
| `release/*` | Prepare production release | Short-term |
| `hotfix/*` | Fix critical production bugs | Short-term |

### Why Pure Git?

The git-flow-avh CLI tool is just a wrapper around native git commands. Understanding the underlying git commands gives you:
- **No dependencies** - works anywhere git is installed
- **Full control** - understand and customize each operation
- **Debugging** - know exactly what's happening
- **Portability** - not tied to a specific tool

## Quick Start

**For new repository setup:** See "Initialize Repository" below

**For daily workflow:** Use the workflow decision tree to determine which operation to perform

## Workflow Decision Tree

```
Need to work on Git Flow repository?
│
├─ New feature? → Feature Workflow
├─ Prepare release? → Release Workflow
├─ Fix production bug? → Hotfix Workflow
└─ New repository? → Initialize Repository
```

## Initialize Repository

Set up a new repository with Git Flow branches:

### Pure Git Method (Recommended)

```bash
# 1. Ensure you're on main/master
git checkout main

# 2. Create develop branch from main
git checkout -b develop

# 3. Push both branches to remote
git push -u origin main
git push -u origin develop
```

### Using Helper Script

```bash
bash scripts/setup_gitflow.sh
```

### Optional: git-flow-avh Tool

If you have git-flow-avh installed:

```bash
git flow init      # Interactive setup
git flow init -d   # Use defaults
```

**After initialization, you should be on the `develop` branch.**

## Feature Workflow

Use feature branches for developing new features for upcoming releases.

### Start a Feature

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br>git checkout develop<br>git checkout -b feature/<name><br>``` | ```bash<br>git flow feature start <name><br>``` |

**Example (Pure Git):**
```bash
git checkout develop
git checkout -b feature/user-authentication
```

This creates `feature/user-authentication` from `develop`.

### Finish a Feature

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br>git checkout develop<br>git merge --no-ff feature/<name><br>git branch -d feature/<name><br>``` | ```bash<br>git flow feature finish <name><br>``` |

**Example (Pure Git):**
```bash
git checkout develop
git merge --no-ff feature/user-authentication
git branch -d feature/user-authentication
```

This:
- Merges `feature/user-authentication` to `develop` using `--no-ff`
- Deletes the feature branch
- Switches back to `develop`

**Note:** `--no-ff` (no fast-forward) preserves feature history in the graph.

### Publish a Feature (Team Collaboration)

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br>git push -u origin feature/<name><br>``` | ```bash<br>git flow feature publish <name><br>``` |

**Checkout remote feature:**
```bash
git fetch origin
git checkout feature/<name>
```

**Pull latest changes:**
```bash
git pull origin feature/<name>
```

## Release Workflow

Use release branches when preparing for a new production release. This allows bug fixes and version bumping.

### Start a Release

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br>git checkout develop<br>git checkout -b release/<version><br>``` | ```bash<br>git flow release start <version><br>``` |

**Example (Pure Git):**
```bash
git checkout develop
git checkout -b release/1.2.0
```

This creates `release/1.2.0` from `develop`.

### Publish a Release

```bash
git push -u origin release/<version>
```

### Finish a Release

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br># Merge to main and tag<br>git checkout main<br>git merge --no-ff release/<version><br>git tag -a <version> -m "Release <version>"<br><br># Merge back to develop<br>git checkout develop<br>git merge --no-ff release/<version><br><br># Cleanup<br>git branch -d release/<version><br>``` | ```bash<br>git flow release finish <version><br>``` |

**Example (Pure Git):**
```bash
# Merge to main and tag
git checkout main
git merge --no-ff release/1.2.0
git tag -a 1.2.0 -m "Release version 1.2.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/1.2.0

# Cleanup
git branch -d release/1.2.0
```

This:
- Merges `release/1.2.0` to `main` using `--no-ff`
- Tags the merge with version name
- Merges `release/1.2.0` back to `develop` using `--no-ff`
- Deletes the release branch
- Switches back to `develop`

**Push tags to remote:**
```bash
git push origin main
git push origin develop
git push origin <version>  # Push the tag
```

## Hotfix Workflow

Use hotfix branches to fix critical production bugs immediately.

### Start a Hotfix

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br>git checkout main<br>git checkout -b hotfix/<version><br>``` | ```bash<br>git flow hotfix start <version><br>``` |

**Example (Pure Git):**
```bash
git checkout main
git checkout -b hotfix/1.2.1
```

This creates `hotfix/1.2.1` from `main/master`.

### Finish a Hotfix

| Pure Git | git-flow Tool (Optional) |
|----------|--------------------------|
| ```bash<br># Merge to main and tag<br>git checkout main<br>git merge --no-ff hotfix/<version><br>git tag -a <version> -m "Hotfix <version>"<br><br># Merge back to develop<br>git checkout develop<br>git merge --no-ff hotfix/<version><br><br># Cleanup<br>git branch -d hotfix/<version><br>``` | ```bash<br>git flow hotfix finish <version><br>``` |

**Example (Pure Git):**
```bash
# Merge to main and tag
git checkout main
git merge --no-ff hotfix/1.2.1
git tag -a 1.2.1 -m "Hotfix: Fix critical login bug"

# Merge back to develop
git checkout develop
git merge --no-ff hotfix/1.2.1

# Cleanup
git branch -d hotfix/1.2.1
```

This:
- Merges `hotfix/1.2.1` to `main/master` using `--no-ff`
- Tags the merge with version name
- Merges `hotfix/1.2.1` back to `develop` using `--no-ff`
- Deletes the hotfix branch
- Switches back to `develop`

**Exception:** If a release branch exists, merge the hotfix into that release branch instead of develop.

## Helper Scripts

This skill includes helper scripts for common Git Flow operations:

**All scripts use pure git commands - no git-flow-avh dependency required.**

- `scripts/gitflow_helper.sh` - Interactive menu for all Git Flow operations
- `scripts/setup_gitflow.sh` - Initialize Git Flow repository (pure git)
- `scripts/gitflow_status.sh` - Show current Git Flow status (pure git)

**Usage:**

```bash
# Run interactive helper
bash scripts/gitflow_helper.sh

# Check Git Flow status
bash scripts/gitflow_status.sh

# Setup new Git Flow repository
bash scripts/setup_gitflow.sh
```

## Branch Summary

| Branch Type | Branch From | Merge To | Naming Convention | Lifetime |
|-------------|-------------|----------|-------------------|----------|
| **main/master** | - | - | `main` or `master` | Indefinite |
| **develop** | - | - | `develop` | Indefinite |
| **feature** | `develop` | `develop` | `feature/*` | Short-term |
| **release** | `develop` | `develop`, `main` | `release/*` | Short-term |
| **hotfix** | `main` | `develop`, `main` | `hotfix/*` | Short-term |

## Best Practices

1. **Always use `--no-ff`** when merging - preserves feature history and enables easy reversion
2. **Keep feature branches focused** - one feature per branch
3. **Write descriptive commit messages** - explain what and why, not just how
4. **Tag releases** - use semantic versioning (e.g., `1.2.0`)
5. **Pull before starting** - ensure `develop` is up-to-date before starting features
6. **Understand the git commands** - the git-flow tool is optional; knowledge of pure git commands is universal

## Quick Reference: Pure Git Commands

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Git Flow: Pure Git Cheat Sheet                  │
├─────────────────────────────────────────────────────────────────────────┤
│ FEATURE START:   git checkout develop && git checkout -b feature/<name> │
│ FEATURE FINISH:  git checkout develop && git merge --no-ff feature/<name│
│                  && git branch -d feature/<name>                        │
├─────────────────────────────────────────────────────────────────────────┤
│ RELEASE START:   git checkout develop && git checkout -b release/<ver>  │
│ RELEASE FINISH:  git checkout main && git merge --no-ff release/<ver>   │
│                  && git tag -a <ver> -m "Release <ver>"                 │
│                  && git checkout develop && git merge --no-ff release/<ver│
│                  && git branch -d release/<ver>                         │
├─────────────────────────────────────────────────────────────────────────┤
│ HOTFIX START:    git checkout main && git checkout -b hotfix/<ver>      │
│ HOTFIX FINISH:   git checkout main && git merge --no-ff hotfix/<ver>    │
│                  && git tag -a <ver> -m "Hotfix <ver>"                  │
│                  && git checkout develop && git merge --no-ff hotfix/<ver│
│                  && git branch -d hotfix/<ver>                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Common Issues

**Issue:** "Not a gitflow repository" (when using git-flow tool)
- **Solution:** Run `git flow init` first, or just create the branches manually with pure git

**Issue:** Merge conflicts during finish
- **Solution:** Resolve conflicts, then `git add` the files, `git commit` to complete the merge

**Issue:** Feature branch name contains invalid characters
- **Solution:** Use alphanumeric and hyphens only (e.g., `user-auth` not `user_auth`)

**Issue:** develop branch doesn't exist
- **Solution:** Create it from main: `git checkout main && git checkout -b develop`

## When NOT to Use Git Flow

Git Flow is NOT ideal for:
- **Continuous delivery** teams - consider GitHub Flow or trunk-based development instead
- **Single developer** projects - overhead may not be justified
- **Web services** with frequent deployments - simpler workflows work better

Git Flow IS ideal for:
- Versioned software releases
- Projects with scheduled release cycles
- Teams supporting multiple production versions
- Mobile apps with app store review processes

## References

See [references/workflow.md](references/workflow.md) for detailed workflow diagrams and advanced patterns.
