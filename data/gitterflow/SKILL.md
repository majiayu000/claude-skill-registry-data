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

If you are a sub-agent spawned by GitterFlow, run `gf ready` when your task is complete:

```bash
gf ready
```

This command:
1. **Auto-commits** any uncommitted changes with an AI-generated message
2. **Marks your work as ready** for the brain to merge
3. **Exits successfully** - you're done!

**IMPORTANT - Do NOT use `gf finish`!** The brain agent will handle merging.

### Why `gf ready` instead of `gf finish`?

You can't see what other sub-agents are doing. If you try to merge directly:
- You might conflict with another agent's recent merge
- You lack context to resolve conflicts correctly
- You could corrupt the base branch for everyone

The brain agent coordinates all merges because it has full visibility into all agents' work.

### After running `gf ready`:
- Your status changes to `ready`
- The brain sees you're ready via `gf status`
- The brain merges your work at the right time
- The brain handles any conflicts with full context

## For Brain Agents: Merging Sub-Agent Work

When you are the orchestrating "brain" agent coordinating sub-agents:

### 1. Monitor Progress
```bash
gf status
```
Look for agents with `ready` status - these have completed their work and are awaiting merge.

### 2. Merge Ready Branches
For each ready branch, go to the base branch directory and merge:

```bash
# In the main repo (not a worktree)
git checkout main
git pull origin main
git merge <branch-name>
```

If merge succeeds, the agent's work is now in the base branch.

### 3. Handle Conflicts
If a merge conflicts:
1. You're left in the base branch with conflict markers
2. Review both sides - you have context from ALL agents
3. Resolve based on your understanding of the full picture
4. Complete the merge: `git add . && git commit`

### 4. Merge Order Considerations
- Independent features: any order works
- Overlapping changes: merge simpler/foundation changes first
- If unsure, review diffs before deciding order

### 5. Update Agent Status (Future Enhancement)
After successful merge, update the agent's status:
```bash
# This will be automated in future versions
# For now, the worktree can be cleaned up manually:
git worktree remove <worktree-path>
git branch -d <branch-name>
```

## Plan Mode (Plan-Then-Execute Workflow)

> **Note**: This feature is in design phase. See `docs/PLAN-APPROVAL-DESIGN.md`.

### Overview

Plan mode enables a two-phase workflow where subagents write an implementation plan before executing. The brain agent reviews and approves/rejects plans before any code is written.

### For Brain Agents: Spawning with Plan Mode

```bash
# Spawn subagent in plan-first mode
gf new --task "Implement feature X" --plan-first --autonomous
```

This will:
1. Start the subagent with `--permission-mode plan` (read-only)
2. Subagent analyzes codebase and writes plan
3. Subagent sets status to `awaiting_approval` and exits
4. Brain reviews plan and runs `gf approve` or `gf reject`

### For Brain Agents: Plan Review Protocol

When subagents are in `awaiting_approval` status:

1. **Check status**: `gf status` shows agents awaiting approval
2. **Read plan**: Plan is at `.gitterflow/agents/{branch}/plan.md`
3. **Evaluate**:
   - Does the approach align with overall architecture?
   - Are there conflicts with other agents' plans?
   - Is the scope appropriate?
4. **Decide**:
   - `gf approve <branch>` - Plan is good, start execution
   - `gf reject <branch> --message "feedback"` - Needs revision

### For Sub-Agents: Plan Mode Instructions

If you were spawned with `--plan-first`, you are in **plan mode**:

1. **Analyze only** - You have read-only access (Read, Glob, Grep, WebSearch)
2. **Write your plan** to: `.gitterflow/agents/{your-branch}/plan.md`
3. **Update status**: Run `gf status --write "awaiting_approval"`
4. **Exit** - Do NOT implement anything yet

**Plan file format:**
```markdown
# Implementation Plan: {task summary}

## Analysis
- Examined files: [list]
- Key findings: [summary]

## Approach
1. Step one
2. Step two

## Files to Modify
| File | Changes |
|------|---------|
| src/foo.ts | Add new function |

## Files to Create
- src/new-feature.ts - Main implementation

## Risks and Considerations
- Risk 1: mitigation

## Questions for Brain (if any)
- Should we use approach A or B?
```

### Plan Approval Commands (Placeholder)

```bash
# Approve a plan and start execution phase
gf approve <branch>
gf approve <branch> --message "Looks good, proceed"

# Reject a plan with feedback
gf reject <branch> --message "Use exponential backoff instead"
```

## Important Notes

- Sub-agents merge to **your current branch** (the branch you were on when spawning)
- Each sub-agent is completely independent - they cannot communicate with each other
- Monitor `gf status` to track progress of all agents
- Keep tasks independent to avoid merge conflicts
- Brain agents should handle ALL merges - sub-agents should only use `gf ready`
- **Plan mode** prevents wasted work by validating approach before implementation
