---
name: repo-management
description: "Manage git repositories across teams using repo-manager.sh. Use when syncing repos, checking repo status, creating branches, or when user mentions 'repo sync', 'repo status', 'clone repos', 'setup repos', 'create branch across repos'."
allowed-tools: Read, Bash, Glob
---

# Repository Management

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Wrapper for `scripts/repo-manager.sh` to manage git repositories across teams.

## Commands

- `/repo setup {team|--all}` - Clone all repos for a team
- `/repo sync {team|--all}` - Pull latest changes
- `/repo status {team|--all}` - Check repo status
- `/repo verify {team|--all}` - Verify repos are cloned
- `/repo list {team|--all}` - List repos for team
- `/repo teams` - List all teams
- `/repo branch {team} {type/name}` - Create branch across repos
- `/repo merge {team}` - Merge current to active branch
- `/repo cleanup {team} [--dry-run] [--remote]` - Delete merged branches

## Branch Strategy

All teams use `develop` as active branch, `main`/`master` is production-only.
Full SOP: `docs/system/sops/branch-strategy.md`

The `sync` command automatically enforces this: repos on `main`/`master` get switched to `develop`.
The `status` command shows `[WARN: should be on develop]` for repos on the wrong branch.

## Available Contexts

Contexts are defined in `pos.yaml` under the `contexts:` key. Run `/repo teams` to list all registered contexts with repositories.

## Process

### Execute Command

All commands execute the repo-manager.sh script:

```bash
scripts/repo-manager.sh {command} {args}
```

### `/repo setup {team}`

Clones all repositories for a team from the platform registry.

```bash
./scripts/repo-manager.sh setup {team}
# Or for all teams:
./scripts/repo-manager.sh setup --all
```

**What it does:**
1. Reads platform-registry.yaml for team repos
2. Clones each repo to `{teams_dir}/{team}/repos/`
3. Checks out the active branch (if different from default)
4. Reports success/failure for each repo

### `/repo sync {team}`

Pulls latest changes for all team repos.

```bash
./scripts/repo-manager.sh sync {team}
```

**What it does:**
1. For each repo in team
2. `git fetch --all --prune`
3. `git pull` (if on tracking branch)
4. Reports ahead/behind status

### `/repo status {team}`

Shows git status for all team repos.

```bash
./scripts/repo-manager.sh status {team}
```

**Output includes:**
- Current branch
- Uncommitted changes count
- Ahead/behind remote count
- Last commit message

### `/repo branch {team} {type/name}`

Creates a branch across ALL team repos.

```bash
./scripts/repo-manager.sh branch {team} feature/my-feature
```

**Branch types:**
- `feature/` - New features
- `fix/` - Bug fixes
- `chore/` - Maintenance
- `hotfix/` - Urgent fixes
- `release/` - Release prep

### `/repo merge {team}`

Merges current branch back to active branch.

```bash
./scripts/repo-manager.sh merge {team}
```

### `/repo cleanup {team}`

Deletes merged branches.

```bash
# Preview deletions
./scripts/repo-manager.sh cleanup {team} --dry-run

# Delete local branches
./scripts/repo-manager.sh cleanup {team}

# Delete local AND remote branches
./scripts/repo-manager.sh cleanup {team} --remote
```

## Registry Reference

Repos are defined in the platform registry file referenced by `scripts/repo-manager.sh`. Each context lists its repositories, default branch, and active branch.

```yaml
contexts:
  my-project:
    default_branch: main        # Production branch (protected)
    active_branch: develop      # Development branch (all work here)
    repos:
      - name: my-project-core
      - name: my-project-api
```

## Examples

```bash
# Clone all repos for a context
/repo setup my-project

# Sync all contexts
/repo sync --all

# Check repo status for a context
/repo status my-project

# Create feature branch across a context
/repo branch my-project feature/add-webhooks

# Clean up merged branches (preview)
/repo cleanup my-project --dry-run
```

## Notes

- Registry file: referenced by `scripts/repo-manager.sh` (configurable per installation)
- Branch strategy: `docs/system/sops/branch-strategy.md`
- Script location: `scripts/repo-manager.sh`
- Repos are cloned to: `contexts/{context}/projects/`
- Supports SSH and HTTPS cloning
- Supports both GitLab and GitHub

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
