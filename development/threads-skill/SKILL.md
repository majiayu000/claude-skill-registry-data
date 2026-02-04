---
name: threads-skill
description: Multi-agent thread orchestration skill for Claude Code
allowed-tools: Bash,Read
version: "1.2.1"
---

# Threads Skill

This skill provides thread orchestration capabilities for managing multiple Claude agents.

## When to Use

Activate this skill when the user wants to:
- Create and manage multiple Claude agent threads
- Run agents in parallel or background
- Coordinate between agents using events
- Schedule periodic agent tasks
- Monitor agent execution status
- Resume interrupted agent sessions

## Capabilities

### Thread Lifecycle Management
- Create threads with different modes (automatic, semi-auto, interactive, sleeping)
- Create threads with isolated git worktrees for parallel development
- Start, stop, pause, and resume threads
- Query thread status and view logs
- Delete completed threads

### Git Worktree Isolation
- Each thread can have its own isolated git worktree
- Multiple threads can work on different branches simultaneously
- Automatic worktree cleanup when threads complete
- Push changes from worktree to remote

### Event-Driven Coordination
- Publish events to the blackboard
- Subscribe to events from other threads
- Send direct messages between threads
- Share artifacts between threads

### Orchestration
- Run orchestrator daemon in background
- Monitor all threads from single point
- Handle thread scheduling
- Manage concurrent execution limits

## Essential Commands

```bash
# Initialize claude-threads in project
ct init

# Thread operations
ct thread create <name> --mode <mode> --template <template>
ct thread create <name> --mode automatic --worktree  # With isolated worktree
ct thread create <name> --worktree --worktree-base develop  # Custom base branch
ct thread list [status]
ct thread start <id>
ct thread stop <id>
ct thread status <id>
ct thread logs <id>
ct thread resume <id>

# Worktree management
ct worktree list           # List active worktrees
ct worktree status <id>    # Show worktree details
ct worktree cleanup        # Remove orphaned worktrees

# Orchestrator
ct orchestrator start
ct orchestrator stop
ct orchestrator status

# PR Shepherd
ct pr watch <pr_number>    # Watch PR with worktree isolation
ct pr status               # Show all watched PRs
ct pr daemon               # Run as background daemon

# Events
ct event list
ct event publish <type> '<json>'
```

## Thread Modes

| Mode | Use Case |
|------|----------|
| `automatic` | Fully autonomous background tasks |
| `semi-auto` | Autonomous with user approval for critical steps |
| `interactive` | Step-by-step user confirmation |
| `sleeping` | Scheduled or event-triggered tasks |

## Example Workflows

### Parallel Epic Development with Worktrees

```bash
# Create threads with isolated worktrees for true parallel development
ct thread create epic-7a-dev --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "7A"}'
ct thread create epic-8a-dev --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "8A"}'

# Each thread has its own branch and working directory
# No conflicts between parallel development

# Start orchestrator to manage them
ct orchestrator start

# Monitor progress
ct thread list running
ct worktree list
```

### Scheduled PR Monitoring

```bash
# Create sleeping thread that wakes every 5 minutes
ct thread create pr-monitor --mode sleeping --template pr-monitor.md --schedule '{"interval": 300}'
ct thread start pr-monitor
```

### Event-Driven Review

```bash
# Thread that triggers on DEVELOPMENT_COMPLETED event
ct thread create reviewer --mode semi-auto --template reviewer.md --trigger DEVELOPMENT_COMPLETED
```

## State Locations

- Database: `.claude-threads/threads.db`
- Logs: `.claude-threads/logs/`
- Config: `.claude-threads/config.yaml`
- Templates: `.claude-threads/templates/`
- Worktrees: `.claude-threads/worktrees/`

## Integration Points

### PR Shepherd (Automatic PR Feedback Loop)
```bash
# Watch a PR for CI failures and review changes
# Creates isolated worktree for fix operations
ct pr watch 123

# The shepherd will automatically:
# - Create isolated worktree for PR fixes
# - Detect CI failures and spawn fix threads in worktree
# - Address review change requests
# - Push fixes from worktree
# - Wait for approval and optionally auto-merge
# - Cleanup worktree when PR is merged/closed

# Check status
ct pr status 123

# Run as daemon
ct pr daemon
```

### GitHub Webhooks
```bash
ct webhook start --port 31338
# Configure GitHub to send to http://server:31338/webhook
```

### n8n API
```bash
ct api start --port 31337
# Use REST endpoints for automation
```

## Error Handling

If a thread becomes blocked:
1. Check status: `ct thread status <id>`
2. View logs: `ct thread logs <id>`
3. Resume manually: `ct thread resume <id>`
4. Or restart: `ct thread stop <id> && ct thread start <id>`
