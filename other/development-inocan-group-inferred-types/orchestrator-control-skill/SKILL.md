---
name: orchestrator-control-skill
description: Master orchestrator control for PR lifecycle management with multi-agent coordination
allowed-tools: Bash,Read,Write,Edit
version: "1.1.0"
---

# Orchestrator Control Skill

This skill spawns a control thread that manages the entire orchestrator, PR shepherds, and multi-agent coordination.

## When to Use

Activate this skill when the user wants to:
- Start the orchestrator in control mode
- Manage PR lifecycle with multiple agents
- Watch PRs with automatic conflict resolution and comment handling
- Coordinate autonomous multi-agent workflows

## Capabilities

### Orchestrator Control
- Spawn a master control thread
- Manage orchestrator daemon lifecycle
- Monitor system health and thread status
- Handle escalations from sub-agents

### PR Lifecycle Management
- Watch PRs with full lifecycle management
- Automatic merge conflict resolution
- Review comment handling (respond + resolve)
- Configurable auto-merge behavior

### Multi-Agent Spawning
- PR Shepherd agents per PR
- Merge Conflict Resolver agents
- Review Comment Handler agents
- All working in isolated worktrees

## Essential Commands

```bash
# Start orchestrator control thread
ct control start [--interactive] [--auto-merge]

# Check control status
ct control status

# Stop control
ct control stop

# Watch a PR with full lifecycle management
ct pr watch <number> [--auto-merge] [--interactive] [--poll-interval 30]

# Check PR lifecycle status
ct pr status <number>

# View PR comment status
ct pr comments <number>

# List all watched PRs
ct pr list
```

## Configuration Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--auto-merge` | Auto-merge when all criteria met | notify only |
| `--interactive` | Confirm actions before executing | autonomous |
| `--poll-interval` | Seconds between PR status polls | 30 |

## PR Completion Criteria

A PR is considered "done" when ALL are true:
- CI passing (all checks green)
- No merge conflicts
- All review comments RESPONDED
- All review comments RESOLVED (threads closed)
- Required approvals received

## Proactive Review State Detection

**CRITICAL**: Do NOT use "pending" states that wait passively. Always check proactively:

```bash
# Check IMMEDIATELY after Copilot review arrives
UNRESOLVED=$(gh api graphql -f query='query {
  repository(owner: "hanibalsk", name: "property-management") {
    pullRequest(number: <PR_NUMBER>) {
      reviewThreads(first: 100) { nodes { isResolved } }
    }
  }
}' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length')

if [ "$UNRESOLVED" -gt 0 ]; then
  # Spawn review-comment-handler agent IMMEDIATELY
  # Do NOT mark as "pending" and wait
fi
```

### Auto-Approval Workflow

Use the GitHub Actions workflows for approval:

```bash
# Trigger auto-approve (waits for CI, checks conditions)
gh workflow run auto-approve.yml -f pr_number=<PR_NUMBER>

# Direct approval (with options)
gh workflow run approve-pr.yml -f pr_number=<PR_NUMBER> [-f skip_ci_check=false]
```

### When Orchestrating PRs

1. **On PR Creation**: Start monitoring CI
2. **On CI Complete**: Check for Copilot review
3. **On Copilot Review**: IMMEDIATELY check unresolved threads
4. **If Unresolved > 0**: Spawn review-comment-handler agent
5. **If Unresolved == 0**: Trigger auto-approve workflow
6. **On Merge Conflict**: Spawn merge-conflict-resolver agent
7. **After All Resolved**: Trigger auto-approve workflow

## Multi-Agent Architecture

```
Control Thread (ct control start)
    |
    +-- Git Poller (polls PR status)
    |
    +-- PR Shepherd (per watched PR)
            |
            +-- Merge Conflict Agent (on conflict)
            |
            +-- Comment Handler Agent (per comment)
```

## Example Workflows

### Watch a PR with Auto-Merge
```bash
# Start orchestrator control
ct control start --auto-merge

# Watch a specific PR
ct pr watch 123 --auto-merge

# The system will:
# 1. Poll PR status every 30 seconds
# 2. Detect and auto-resolve merge conflicts
# 3. Handle all review comments (respond + resolve)
# 4. Auto-merge when all criteria are met
```

### Interactive Mode
```bash
# Start in interactive mode
ct control start --interactive

# You'll be asked to confirm:
# - Spawning new PR shepherds
# - Auto-merging PRs
# - Handling escalations
```

### Monitor Multiple PRs
```bash
ct control start

ct pr watch 123
ct pr watch 124
ct pr watch 125

# Check status of all
ct pr list

# Detailed status
ct pr status 123
```

## Event Types

### Published by Control Thread
- `ORCHESTRATOR_STARTED` - Control thread started
- `SHEPHERD_SPAWNED` - New PR shepherd spawned
- `SYSTEM_STATUS` - Periodic status update

### Published by PR Shepherd
- `PR_STATE_CHANGED` - State machine transition
- `MERGE_CONFLICT_DETECTED` - Conflict needs resolution
- `REVIEW_COMMENTS_PENDING` - Comments need handling
- `PR_READY_FOR_MERGE` - All criteria met

### Published by Sub-Agents
- `MERGE_CONFLICT_RESOLVED` - Conflict fixed
- `COMMENT_RESPONDED` - Reply posted
- `COMMENT_RESOLVED` - Thread closed

## Integration with Existing Skills

This skill extends the `threads` skill with:
- Higher-level orchestration
- PR lifecycle management
- Multi-agent coordination
- Conflict and comment handling

Use alongside:
- `bmad-autopilot` for epic development
- `thread-spawner` for parallel thread creation

## Base + Fork Pattern

Sub-agents use memory-efficient fork worktrees:

```
PR Base Worktree (created when watching PR)
    │
    ├── Fork: conflict-resolver (on conflict)
    │   └── Shares git objects with base
    │
    ├── Fork: comment-handler-1 (per comment)
    │   └── Shares git objects with base
    │
    └── Fork: comment-handler-2
        └── Shares git objects with base

After each fork completes:
1. Merge fork back to base
2. Remove fork
3. Push from base (once for all)
```

### Fork Commands

```bash
# Create fork for sub-agent
ct worktree fork 123 conflict-fix fix/conflict conflict_resolution

# After sub-agent completes
ct worktree merge-back conflict-fix
ct worktree remove-fork conflict-fix

# Push from base
cd $(ct worktree base-path 123)
git push
```

## Distributed Deployment

Run orchestrator on central server with remote workers:

```bash
# Central server
ct api start --bind 0.0.0.0 --token $TOKEN

# Worker machines
ct remote connect central:31337 --token $TOKEN
ct spawn epic-7a --template bmad-developer.md
```

## Error Recovery

### Handle Fork Merge Conflicts

```bash
if ! ct worktree merge-back my-fork; then
  # Retry with fresh fork
  ct worktree remove-fork my-fork --force
  ct worktree base-update 123
  # Re-fork and retry
fi
```

### Reconcile Database with Filesystem

```bash
# Check for inconsistencies
ct worktree reconcile

# Auto-fix orphans
ct worktree reconcile --fix
```

## Documentation

- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - System architecture
- [AGENT-COORDINATION.md](../../docs/AGENT-COORDINATION.md) - Coordination patterns
- [WORKTREE-GUIDE.md](../../docs/WORKTREE-GUIDE.md) - Base + fork details
- [EVENT-REFERENCE.md](../../docs/EVENT-REFERENCE.md) - Event types
- [MULTI-INSTANCE.md](../../docs/MULTI-INSTANCE.md) - Distributed deployment
