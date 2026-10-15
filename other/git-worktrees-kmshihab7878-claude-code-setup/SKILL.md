---
name: Git Worktrees
description: Guidance for isolated Git worktree workflows and parallel branch development.
---

# Git Worktrees

> Isolated development environments. Parallel work without branch switching. Clean separation.

## Triggers

- Need to work on multiple features simultaneously
- Subagent work that modifies overlapping files
- Experimental changes that should not touch the main working directory
- Running tests on one branch while developing on another
- Agent isolation via `EnterWorktree` / `ExitWorktree` tools

## When to Use Worktrees vs Branches

| Scenario | Use |
|----------|-----|
| Sequential feature work | Branch (simpler) |
| Parallel feature work | Worktree (isolated) |
| Quick hotfix while mid-feature | Worktree (no stash needed) |
| Subagent isolation | Worktree (via `isolation: "worktree"` on Agent tool) |
| Spike/experiment alongside main work | Worktree (disposable) |
| Code review while developing | Worktree (separate checkout) |

## Worktree Workflow

### Creating a Worktree

```bash
# Create a worktree for a new branch
git worktree add ../project-feature-name -b feature/feature-name

# Create a worktree for an existing branch
git worktree add ../project-hotfix hotfix/urgent-fix

# List active worktrees
git worktree list
```

**Directory naming**: Use `../<project>-<purpose>` to keep worktrees adjacent to the main repo.

### Working in a Worktree

```bash
# Each worktree is a full checkout — cd into it and work normally
cd ../project-feature-name
# Run tests, edit files, commit — all isolated from main worktree

# Install dependencies if needed (they're NOT shared)
npm install  # or pip install -r requirements.txt, etc.
```

### Cleaning Up

```bash
# When done with a worktree
cd /path/to/main/repo
git worktree remove ../project-feature-name

# Prune stale worktree references
git worktree prune
```

## Agent Tool Integration

When spawning subagents, use `isolation: "worktree"` to give each agent its own copy:

```
Agent tool parameters:
  isolation: "worktree"
  prompt: "Implement feature X in the isolated worktree..."
```

The worktree is automatically cleaned up if the agent makes no changes. If changes are made, the worktree path and branch are returned in the result.

## Baseline Verification

After creating a worktree, **always verify the baseline**:

```bash
# Ensure tests pass in the clean worktree before making changes
cd ../project-worktree
# Run the project's test suite
# If tests fail here, the problem is pre-existing — do not mask it
```

## Dependency Detection

Some worktrees need dependency installation:

| Project Type | Check For | Install Command |
|-------------|-----------|-----------------|
| Node.js | `package.json` | `npm install` or `bun install` |
| Python | `requirements.txt` / `pyproject.toml` | `pip install -r requirements.txt` or `uv sync` |
| Rust | `Cargo.toml` | `cargo build` |
| Go | `go.mod` | `go mod download` |

## Rules

1. **Never delete** worktrees with uncommitted changes — commit or stash first
2. **Never checkout** the same branch in multiple worktrees
3. **Always clean up** worktrees when done to avoid disk bloat
4. **Always verify baseline** tests pass before starting work
