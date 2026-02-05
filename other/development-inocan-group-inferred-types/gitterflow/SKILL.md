---
name: gitterflow
description: Spawn and coordinate parallel Claude Code sub-agents using git worktrees. Use this skill when you need to parallelize work across multiple independent tasks, delegate subtasks to sub-agents, or orchestrate complex multi-part implementations.
---

# GitterFlow: Agent Orchestration

Use GitterFlow to spawn sub-agents that work in parallel on independent tasks. Each sub-agent runs in an isolated git worktree and automatically merges back when complete.

## When to Use

Use GitterFlow when you have:
- **Multiple independent features** that don't conflict with each other
- **Large refactoring** that can be split into parallel workstreams
- **Bug fixes + tests** where implementation and testing can happen simultaneously
- **Documentation + code** tasks that can proceed in parallel

Do NOT use GitterFlow for:
- Tasks that depend on each other's output
- Changes to the same files (will cause merge conflicts)
- Quick single-file fixes (overhead not worth it)

## Commands

### Spawn a Sub-Agent

```bash
gf new --task "Detailed task description" --autonomous
```

This creates a new worktree, spawns Claude Code with the task, and automatically merges when complete.

**Example:**
```bash
gf new --task "Implement shell completions for bash, zsh, and fish" --autonomous
gf new --task "Add retry logic with exponential backoff to API client" --autonomous
gf new --task "Write comprehensive unit tests for the auth module" --autonomous
```

### Check Status

```bash
gf status
```

Shows all running, completed, and failed sub-agents.

### Manual Worktree (Non-Autonomous)

```bash
gf new feature-branch --task "Add new feature"
```

Creates worktree and starts Claude, but requires manual `gf finish` when done.

## How It Works

1. **Isolation**: Each sub-agent gets its own git worktree (separate directory)
2. **Pre-trusted**: Worktrees are automatically trusted (no permission dialogs)
3. **Auto-merge**: Autonomous agents run `gf finish` when Claude exits
4. **Failure handling**: Failed agents leave worktree intact for inspection

## Task Description Best Practices

Write clear, self-contained task descriptions:

**Good:**
```bash
gf new --task "Add a --verbose flag to all CLI commands. The flag should:
1. Enable detailed logging of git operations
2. Show timing information for each step
3. Be configurable via GITTERFLOW_VERBOSE env var
Include tests for the new functionality." --autonomous
```

**Bad:**
```bash
gf new --task "Add verbose mode" --autonomous  # Too vague
```

## Parallel Execution Pattern

When orchestrating multiple sub-agents:

```bash
# 1. Spawn all sub-agents at once
gf new --task "Implement feature A with tests" --autonomous
gf new --task "Implement feature B with tests" --autonomous
gf new --task "Update documentation for A and B" --autonomous

# 2. Monitor progress
gf status

# 3. Handle any failures
# Failed agents have status: failed
# Inspect worktree: cd ../branch-name
# Fix issues and run: gf finish
```

## Handling Merge Conflicts

If a sub-agent completes but has merge conflicts:
1. Status shows `conflict` state
2. Navigate to the worktree: `cd ../branch-name`
3. Resolve conflicts manually
4. Run `gf finish` to complete the merge

## For Sub-Agents: Completing Your Task

If you are a sub-agent spawned by GitterFlow, follow these steps when your task is complete:

1. **Commit your changes**: Use `gf snap` to commit with an AI-generated message, or `git commit -m "message"`
2. **Finish and merge**: Run `gf finish` to merge your work back to the base branch
3. **Verify success**: The finish command will handle the merge and cleanup

**Important**: Always run `gf finish` when you complete your task. This merges your changes back to the parent branch and cleans up the worktree.

If `gf finish` fails due to merge conflicts:
- Resolve the conflicts manually
- Stage the resolved files: `git add .`
- Run `gf finish` again

## Important Notes

- Sub-agents merge to **your current branch** (the branch you were on when spawning)
- Each sub-agent is completely independent - they cannot communicate with each other
- Monitor `gf status` to track progress of all agents
- Keep tasks independent to avoid merge conflicts
