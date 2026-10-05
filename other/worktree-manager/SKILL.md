---
name: worktree-manager
description: This skill should be used when the user mentions "worktree", "wt", "new branch workspace", "parallel development", "feature branch setup", "work on multiple branches", "separate workspace for branch", "docker port conflict", "database isolation", "worktreeinclude", "env isolation", or wants to manage git worktrees for parallel feature development.
version: 2.0.0
---

# Git Worktree Manager Skill

Manages git worktrees for parallel development with automatic environment isolation.

## Activation Triggers

This skill activates when the user:
- Asks about "worktree" or "git worktree"
- Mentions "wt" in context of git/branches
- Wants to "work on multiple branches simultaneously"
- Needs a "separate workspace for a feature"
- Asks about "parallel development" setup
- Wants to "set up a new branch workspace"
- Has "docker port conflicts" between branches
- Needs "database isolation" for parallel work
- Asks about ".worktreeinclude" or "env isolation"

## Commands Reference

| Command | Alias | Description |
|---------|-------|-------------|
| `/wt create <branch>` | `/wt c` | Create worktree with full isolation |
| `/wt list` | `/wt ls` | Show all worktrees |
| `/wt remove <branch>` | `/wt rm` | Remove worktree (stops Docker first) |
| `/wt open <branch> [--editor]` | `/wt o` | Open (--cursor\|-c, --agy\|-a, --code\|-v) |

## Naming Convention

Worktrees are created as siblings with `--` separator:

```
~/[PARENT_DIRECTORY]/[REPO_NAME]/              # main repo
~/[PARENT_DIRECTORY]/[REPO_NAME]--[BRANCH_NAME]/   # worktree for [BRANCH_NAME]
```

## Three-Layer Isolation

### Layer 1: `.worktreeinclude` — File Selection

Gitignore-style file at repo root controlling which untracked files to copy. Auto-generated with sensible defaults on first `wt create`.

```ini
.env*
# apps/*/.env*

[rewrite]
auto

[docker]
auto
```

### Layer 2: `[rewrite]` — Env Var Isolation

- **`auto`**: Suffixes DB_NAME, POSTGRES_DB, DATABASE_URL, COMPOSE_PROJECT_NAME with branch slug
- **`{{BRANCH}}`**: Template placeholder for custom vars

### Layer 3: `[docker]` — Docker Compose Env Var Isolation

- Patches compose file with `${WT_PORT_*:-default}` and `${WT_CONTAINER_PREFIX:-default}` syntax
- Writes port/container env vars + `COMPOSE_PROJECT_NAME` to `.env`
- Auto-creates databases in running Postgres

## Auto-Setup Features

When creating a worktree, the following happens automatically:

1. **Branch handling**: Creates new branch or checks out existing (local/remote)
2. **File copying**: Copies files matching `.worktreeinclude` patterns
3. **Env rewriting**: Suffixes database names and URLs with branch slug
4. **Docker isolation**: Patches compose with env var interpolation, writes `.env`
5. **Database creation**: Creates database in running Postgres (idempotent)
6. **Package manager**: Detects bun/pnpm/yarn/npm from lockfiles
7. **Dependencies**: Runs install at root (monorepo-aware)

## Behavioral Expectations

When user asks about worktrees or parallel development:

1. Suggest using `/wt create <branch>` for new worktrees
2. Explain the three-layer isolation if they have Docker/database conflicts
3. Mention `.worktreeinclude` for customizing which files are copied
4. Show the `cd` command output for easy navigation
5. Explain that `wt remove` stops Docker containers but preserves databases

## Example Interactions

**User**: "I need to work on the auth feature while keeping my current work"

**Response**: Use `/wt create feature/auth` to create a parallel workspace. This will:
- Create `project--feature-auth/` as sibling directory
- Copy your `.env` files and rewrite DB names with `_feature_auth` suffix
- Generate Docker port offsets so both worktrees can run simultaneously
- Install dependencies

**User**: "My worktrees are conflicting on port 5432"

**Response**: The `.worktreeinclude` file's `[docker]` section handles this. With `auto` enabled, `wt create` patches your compose file with `${WT_PORT_*:-default}` env var interpolation and writes offset values to `.env`. Each worktree gets a deterministic offset based on the branch name. The compose file defaults still work on main.

**User**: "How do I customize which files are copied to worktrees?"

**Response**: Edit `.worktreeinclude` in your repo root. It uses gitignore-style patterns:
```
.env*
config/local.yml
apps/*/.env*
```
