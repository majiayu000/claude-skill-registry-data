---
name: thread-orchestrator-skill
description: Multi-agent thread orchestration and coordination
allowed-tools: Bash,Read
version: "1.3.0"
---

# Thread Orchestrator Skill

This skill provides orchestration capabilities for managing multiple Claude agent threads with git worktree isolation.

## When to Use

Activate this skill when the user wants to:
- Run multiple Claude agents in parallel with isolated worktrees
- Coordinate complex workflows across multiple threads
- Manage thread lifecycle (create, start, stop, resume)
- Handle inter-thread communication via events
- Monitor and manage PR feedback loops

## Core Capabilities

### Thread Lifecycle Management
- Create threads with different modes (automatic, semi-auto, interactive, sleeping)
- Create threads with isolated git worktrees
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

### PR Shepherd Integration
- Watch PRs with isolated worktrees
- Automatic CI failure detection and fix
- Review change request handling
- Worktree-per-PR isolation

## Essential Commands

### Thread Operations

```bash
# Initialize claude-threads in project
ct init

# Create a thread
ct thread create <name> --mode <mode> --template <template>

# Create thread with isolated worktree
ct thread create <name> --mode automatic --worktree
ct thread create <name> --worktree --worktree-base develop

# List threads
ct thread list [status]

# Start/stop/resume threads
ct thread start <id>
ct thread stop <id>
ct thread resume <id>

# View thread status and logs
ct thread status <id>
ct thread logs <id>
```

### Worktree Management

```bash
# List all active worktrees
ct worktree list

# Show worktree details
ct worktree status <id>

# Cleanup orphaned worktrees
ct worktree cleanup
```

### Orchestrator Control

```bash
# Start/stop orchestrator daemon
ct orchestrator start
ct orchestrator stop
ct orchestrator status
ct orchestrator restart
```

### PR Shepherd

```bash
# Watch PR with worktree isolation
ct pr watch <pr_number>

# Check status
ct pr status [pr_number]
ct pr list

# Stop watching
ct pr stop <pr_number>

# Run as daemon
ct pr daemon
```

### Event Operations

```bash
# List recent events
ct event list

# Publish event
ct event publish <type> '<json>'
```

## Thread Modes

| Mode | Use Case |
|------|----------|
| `automatic` | Fully autonomous background tasks |
| `semi-auto` | Autonomous with user approval for critical steps |
| `interactive` | Step-by-step user confirmation |
| `sleeping` | Scheduled or event-triggered tasks |

## Workflow Patterns

### Parallel Epic Development

```bash
# Create threads with isolated worktrees
ct thread create epic-7a --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "7A"}'
ct thread create epic-8a --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "8A"}'

# Start orchestrator
ct orchestrator start

# Monitor
ct thread list running
ct worktree list
```

### PR Fix Pipeline

```bash
# Watch PR - creates isolated worktree
ct pr watch 123

# Shepherd automatically:
# - Creates worktree for PR branch
# - Spawns fix threads when CI fails
# - Pushes fixes from worktree
# - Cleans up when PR merges

ct pr status 123
```

### Coordinated Review

```bash
# Create reviewer thread that triggers on development completion
ct thread create reviewer --mode semi-auto --template reviewer.md --trigger DEVELOPMENT_COMPLETED

# Events flow: STORY_COMPLETED -> DEVELOPMENT_COMPLETED -> reviewer wakes
```

## Event Types

| Event | Description |
|-------|-------------|
| `THREAD_STARTED` | Thread began execution |
| `THREAD_COMPLETED` | Thread finished |
| `THREAD_BLOCKED` | Thread encountered a blocker |
| `WORKTREE_CREATED` | Isolated worktree created |
| `WORKTREE_PUSHED` | Changes pushed from worktree |
| `WORKTREE_DELETED` | Worktree cleaned up |
| `STORY_STARTED` | Developer starting story |
| `STORY_COMPLETED` | Story implementation done |
| `DEVELOPMENT_COMPLETED` | All stories finished |
| `REVIEW_COMPLETED` | Code review done |
| `PR_CREATED` | Pull request opened |
| `CI_PASSED` / `CI_FAILED` | CI status update |
| `PR_APPROVED` | PR approved |
| `PR_MERGED` | PR merged successfully |

## Configuration

In `.claude-threads/config.yaml`:

```yaml
threads:
  max_concurrent: 5
  default_max_turns: 80

orchestrator:
  poll_interval: 1
  idle_poll_interval: 10
  idle_threshold: 30

worktrees:
  enabled: true
  max_age_days: 7
  auto_cleanup: true
  default_base_branch: main
  auto_push: true

pr_shepherd:
  max_fix_attempts: 5
  ci_poll_interval: 30
  auto_merge: false
```

## State Locations

- Database: `.claude-threads/threads.db`
- Logs: `.claude-threads/logs/`
- Config: `.claude-threads/config.yaml`
- Templates: `.claude-threads/templates/`
- Worktrees: `.claude-threads/worktrees/`

## Error Handling

If a thread becomes blocked:

```bash
# Check status
ct thread status <id>

# View logs
ct thread logs <id>

# Resume manually
ct thread resume <id>

# Or restart
ct thread stop <id> && ct thread start <id>
```

## Base + Fork Pattern (Memory Efficient)

For PR lifecycle management, use the base + fork pattern:

```bash
# Create base worktree when watching a PR (once)
ct worktree base-create 123 feature/my-pr main

# Fork from base for each sub-agent (shares git objects, ~1MB vs ~100MB)
ct worktree fork 123 conflict-fix fix/conflict conflict_resolution

# After sub-agent completes, merge fork back
ct worktree merge-back conflict-fix

# Cleanup fork
ct worktree remove-fork conflict-fix

# When PR is done, cleanup base
ct worktree base-remove 123
```

### Benefits
- Forks share git objects with base (memory efficient)
- Fast creation and removal
- Centralized push from base worktree
- Easy coordination of parallel fixes

## Coordination Patterns

### Pattern 1: Sequential Chain
```
A ─► B ─► C ─► Done
```
Use: Tasks with dependencies

### Pattern 2: Parallel Fan-Out
```
    Orchestrator
    ┌─┬─┬─┬─┬─┐
    ▼ ▼ ▼ ▼ ▼ ▼
    1 2 3 4 5 6
```
Use: Independent parallel tasks (max 5)

### Pattern 3: Fan-Out/Fan-In (PR Lifecycle)
```
PR Shepherd
├── Fork → Conflict Resolver → Merge Back
├── Fork → Comment Handler 1 → Merge Back
└── Fork → Comment Handler 2 → Merge Back
Then: Push from base
```

## Cross-Instance Orchestration

Connect external Claude Code instances:

```bash
# On orchestrator machine
ct api start --token $TOKEN

# On worker machine
ct remote connect orchestrator:31337 --token $TOKEN
ct spawn epic-7a --template bmad-developer.md
```

## Best Practices

1. Use worktrees for parallel development to avoid conflicts
2. Use base + fork pattern for PR sub-agents (memory efficient)
3. Start orchestrator before creating automatic threads
4. Monitor events for workflow progress
5. Use PR Shepherd for automatic CI/review handling
6. Clean up orphaned worktrees periodically
7. Publish events for all significant state changes
8. Use checkpoints for long-running agents

## Documentation

- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - System architecture
- [AGENT-COORDINATION.md](../../docs/AGENT-COORDINATION.md) - Coordination patterns
- [WORKTREE-GUIDE.md](../../docs/WORKTREE-GUIDE.md) - Worktree management
- [EVENT-REFERENCE.md](../../docs/EVENT-REFERENCE.md) - Event types
- [MULTI-INSTANCE.md](../../docs/MULTI-INSTANCE.md) - Distributed deployment
