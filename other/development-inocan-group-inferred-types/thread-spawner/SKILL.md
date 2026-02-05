---
name: thread-spawner
description: Spawn threads on running claude-threads orchestrator
allowed-tools: Bash,Read
version: "1.2.3"
---

# Thread Spawner Skill

Spawn and manage threads on a running claude-threads orchestrator. Enables parallel execution of epics, stories, or any tasks from within a Claude Code session.

## When to Use

- Spawn parallel threads for epics/stories during BMAD workflow
- Create background tasks from current Claude Code session
- Coordinate multiple Claude Code instances
- Run parallel implementations with isolated git worktrees

## Prerequisites

1. **API Server Running**: The orchestrator API must be running
   ```bash
   ct api start --token <your-token>
   ```

2. **Environment Variable**: Set the API token
   ```bash
   export CT_API_TOKEN=<your-token>
   ```

## Quick Start

### Connect to Orchestrator

```bash
# Auto-discover running orchestrator
ct remote discover

# Or connect explicitly
ct remote connect localhost:31337 --token $CT_API_TOKEN

# Check connection status
ct remote status
```

### Spawn Threads

**Note:** Remote threads ALWAYS use isolated git worktrees by default.

```bash
# Basic spawn (creates worktree automatically for remote)
ct spawn epic-7a --template bmad-developer.md

# Spawn with custom worktree base branch
ct spawn epic-7a --template bmad-developer.md --worktree-base develop

# Spawn with custom context
ct spawn story-123 --template developer.md --context '{"story_id":"123","title":"Add login"}'

# Spawn and wait for completion
ct spawn fix-ci --template fixer.md --wait
```

### Multiple Parallel Threads

```bash
# Spawn multiple epics in parallel
ct spawn epic-7a --template bmad-developer.md --worktree --context '{"epic_id":"7A"}'
ct spawn epic-8a --template bmad-developer.md --worktree --context '{"epic_id":"8A"}'
ct spawn epic-9a --template bmad-developer.md --worktree --context '{"epic_id":"9A"}'
```

## Commands Reference

### Remote Connection

| Command | Description |
|---------|-------------|
| `ct remote connect <host:port>` | Connect to orchestrator API |
| `ct remote disconnect` | Disconnect from remote |
| `ct remote status` | Show connection status |
| `ct remote discover` | Auto-discover running orchestrator |

### Spawn

```
ct spawn <name> [options]
```

| Option | Description |
|--------|-------------|
| `--template, -t <file>` | Prompt template file |
| `--mode, -m <mode>` | Thread mode (automatic, semi-auto, interactive) |
| `--context, -c <json>` | Thread context as JSON |
| `--worktree, -w` | Create with isolated git worktree (DEFAULT for remote) |
| `--no-worktree` | Disable worktree isolation (not recommended) |
| `--worktree-base <branch>` | Base branch for worktree (default: main) |
| `--wait` | Wait for thread completion |
| `--remote` | Force use of remote API |
| `--local` | Force use of local database |

## Use Cases

### 1. Parallel Epic Implementation (BMAD)

When the orchestrator assigns multiple epics, spawn them in parallel:

```bash
# Connect to orchestrator
ct remote connect localhost:31337 --token $CT_API_TOKEN

# Read epic assignments from artifacts
for epic_id in 7A 8A 9A; do
    ct spawn "epic-${epic_id}" \
        --template bmad-developer.md \
        --worktree \
        --worktree-base develop \
        --context "{\"epic_id\":\"${epic_id}\"}"
done
```

### 2. CI Fix Spawning

When CI fails, spawn a fixer thread:

```bash
ct spawn ci-fix-pr-123 \
    --template bmad-fixer.md \
    --worktree \
    --context '{"pr_number":"123","failure":"test:lint"}'
```

### 3. Story Implementation

Spawn threads for individual stories:

```bash
ct spawn story-add-logout \
    --template developer.md \
    --context '{"story_title":"Add logout button","acceptance_criteria":["Button in header","Clears session"]}'
```

### 4. Monitoring Spawned Threads

```bash
# List all threads
ct thread list

# Check specific thread status
ct thread status <thread-id>

# View thread logs
ct thread logs <thread-id>
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CT_API_TOKEN` | Authentication token for API |
| `CT_API_URL` | API URL for auto-discovery |
| `N8N_API_TOKEN` | Alternative token variable |

## Architecture

```
External Claude Code Instance
     │
     ├── ct remote connect ──────────┐
     │                               │
     └── ct spawn ───────────────────┤
                                     │
                                     ▼
                           ┌─────────────────┐
                           │   API Server    │
                           │  (port 31337)    │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │   Orchestrator  │
                           │   (threads.db)  │
                           └────────┬────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
    │   Thread 1    │      │   Thread 2    │      │   Thread 3    │
    │  (worktree)   │      │  (worktree)   │      │  (worktree)   │
    └───────────────┘      └───────────────┘      └───────────────┘
```

## Security

- All API requests require `Authorization: Bearer <token>` header
- Token is stored in `.claude-threads/remote.json` after connecting
- Token can be set via `CT_API_TOKEN` or `--token` flag
- API server binds to localhost by default

## See Also

- [MULTI-INSTANCE.md](../../docs/MULTI-INSTANCE.md) - Full multi-instance documentation
- [threads.md](../../commands/threads.md) - Thread command reference
- [thread-orchestrator](../thread-orchestrator/SKILL.md) - Orchestrator skill
