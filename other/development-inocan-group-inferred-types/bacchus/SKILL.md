---
name: bacchus
description: Multi-agent coordination CLI for codebases. Use when orchestrating parallel agents, claiming tasks, detecting symbol conflicts, or notifying stakeholders of breaking changes. Invoke when user mentions coordination, parallel agents, multiple agents, task claiming, or conflict detection.
---

# Bacchus - Worktree-Based Agent Coordination

Lightweight coordination for parallel agent work. Uses git worktrees for isolation and integrates with beads for task management.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/vu1n/bacchus/main/scripts/install.sh | bash
```

## Core Workflow

```
next/claim → work in worktree → release
```

### 1. Get Work

**Option A: Claim next ready bead**
```bash
bacchus next agent-1
```
Queries beads DB for ready tasks and claims the highest-priority one.

**Option B: Claim a specific bead**
```bash
bacchus claim PROJ-42 agent-1
```
Claims a specific bead by ID (useful when assigning specific tasks to agents).

Both commands:
- Create isolated worktree at `.bacchus/worktrees/{bead_id}/`
- Record the claim in bacchus DB
- Update bead status to `in_progress`

Output:
```json
{
  "success": true,
  "bead_id": "PROJ-42",
  "title": "Implement user auth",
  "worktree_path": ".bacchus/worktrees/PROJ-42",
  "branch": "bacchus/PROJ-42"
}
```

### 2. Do Work

Work in the worktree. All changes are isolated on branch `bacchus/{bead_id}`.

> **Warning**: Never `cd` into a worktree from your main session. Worktrees are ephemeral and get deleted on release. Use `git -C` instead:

```bash
# Use -C flag to operate in worktree without changing cwd
git -C .bacchus/worktrees/PROJ-42 status
git -C .bacchus/worktrees/PROJ-42 add .
git -C .bacchus/worktrees/PROJ-42 commit -m "Implement auth"

# Or spawn a sub-agent (Task tool) that works in the worktree
# Sub-agents are isolated - their cwd dying doesn't affect parent
```

### 3. Release

```bash
# Success - merge to main, cleanup worktree, close bead
bacchus release PROJ-42 --status done

# Blocked - keep worktree for later, mark bead blocked
bacchus release PROJ-42 --status blocked

# Failed - discard changes, reset bead to open
bacchus release PROJ-42 --status failed
```

## Stale Detection

Find and cleanup abandoned claims:

```bash
# List stale claims (>30 min old)
bacchus stale --minutes 30

# Auto-cleanup: remove worktrees, reset beads to open
bacchus stale --minutes 30 --cleanup
```

## List Active Claims

See all active claims and worktrees:

```bash
bacchus list
```

Output:
```json
{
  "claims": [
    {
      "bead_id": "PROJ-42",
      "agent_id": "agent-1",
      "worktree_path": ".bacchus/worktrees/PROJ-42",
      "branch_name": "bacchus/PROJ-42",
      "age_minutes": 5
    }
  ],
  "total": 1
}
```

## Code Search

Index and search symbols:

```bash
# Index a directory
bacchus index src/

# Search for symbols
bacchus symbols --pattern "User*" --kind class
bacchus symbols --file "src/auth.ts"
```

## Status

```bash
bacchus status
```

Shows active claims, worktree locations, and indexed symbol count.

## Context

Generate a markdown summary of the current environment to ground the agent:

```bash
bacchus context
```

- **Global Mode** (at root): Shows all active claims and ready work.
- **Task Mode** (in worktree): Shows specific objectives for the current task.

## Relationship to Beads

```
beads    → What work needs to be done (issues, deps, status)
bacchus  → Who's doing what right now (claims, worktrees)
```

Bacchus reads from beads to find ready work and updates bead status on claim/release. Use beads for any workflow. Add bacchus when multiple agents work in parallel to ensure isolation via worktrees.

## Merge Conflict Handling

When `release --status done` encounters a conflict:

```bash
# Option 1: Resolve manually, then complete
# (fix conflicts in files, git add them)
bacchus resolve PROJ-42

# Option 2: Abort merge, keep working
bacchus abort PROJ-42

# Option 3: Discard all work
bacchus release PROJ-42 --status failed
```

## Orchestrator Pattern

Main agent has broad context (project overview, all tasks). Sub-agents have focused context (single task + worktree).

### Using Claude Code Task Tool (Primary)

1. **Claim task**:
   ```bash
   bacchus next worker-1
   # Returns: { bead_id, title, description, worktree_path }
   ```

2. **Spawn sub-agent**:
   ```
   Task tool:
     subagent_type: "general-purpose"
     prompt: |
       Work in {worktree_path} on task {bead_id}: {title}

       {description}

       Commit changes when done.
     run_in_background: true
   ```

3. **Monitor**: `TaskOutput(task_id)`

4. **Release**: `bacchus release {bead_id} --status done|failed`

5. **Repeat** as needed - scale up/down based on workload

### Why Sequential Claiming Works

```
bacchus next worker-1  → claims BEAD-1, marks in_progress
bacchus next worker-2  → BEAD-1 taken, gets BEAD-2
bacchus next worker-3  → BEAD-1,2 taken, gets BEAD-3
```

No race conditions. Each `next` call atomically claims the highest-priority ready bead.

### Using Terminal Multiplexer (Human Monitoring)

For visual debugging with zellij or tmux:

```bash
# Each pane runs an isolated agent
zellij run -- claude --print "Work on BEAD-1 in .bacchus/worktrees/BEAD-1"
zellij run -- claude --print "Work on BEAD-2 in .bacchus/worktrees/BEAD-2"
```

Each pane shows real-time agent output. Useful for debugging but main agent can't easily read structured results.

## Directory Structure

```
project/
├── .bacchus/
│   ├── bacchus.db          # Claims database
│   └── worktrees/
│       ├── PROJ-42/        # Isolated worktree for PROJ-42
│       └── PROJ-43/        # Another agent's worktree
└── .beads/
    └── beads.db            # Task/issue database
```
