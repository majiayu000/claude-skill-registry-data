---
name: background-tasks
description: Run and manage long-running background tasks in the shell. Use for starting processes in background, monitoring output, listing active tasks, and killing processes. Essential for dev servers, watch modes, builds, and any non-blocking operations.
license: MIT
---

# Background Tasks Skill

Manage long-running shell processes without blocking the terminal. All scripts output JSON for easy parsing.

## Quick Start

```bash
cd .claude/skills/background-tasks/scripts

# Start a task in background
./start.sh "npm run dev" --name "dev-server"

# List running tasks
./list.sh

# Get task output
./output.sh --id <task-id>
# or by name
./output.sh --name "dev-server"

# Kill a task
./kill.sh --id <task-id>
# or by name
./kill.sh --name "dev-server"
```

## Available Scripts

All scripts are in `.claude/skills/background-tasks/scripts/`

### Core Scripts

| Script       | Purpose                         | Key Options                            |
| ------------ | ------------------------------- | -------------------------------------- |
| `start.sh`   | Start a background task         | `--name`, `--cwd`, `--env`             |
| `list.sh`    | List all active tasks           | `--all` (include completed)            |
| `output.sh`  | Get task output (stdout/stderr) | `--id`, `--name`, `--tail`, `--follow` |
| `kill.sh`    | Terminate a task                | `--id`, `--name`, `--signal`           |
| `cleanup.sh` | Remove completed task records   | `--all`                                |

## Script Usage

### start.sh - Start Background Task

```bash
# Basic usage
./start.sh "npm run dev"

# With name for easy reference
./start.sh "npm run dev" --name "dev-server"

# With working directory
./start.sh "cargo build" --name "rust-build" --cwd /path/to/project

# With environment variables
./start.sh "node server.js" --name "api" --env "PORT=3000,NODE_ENV=production"
```

**Output:**

```json
{
  "success": true,
  "id": "bg_1234567890",
  "name": "dev-server",
  "pid": 12345,
  "command": "npm run dev",
  "cwd": "/path/to/project",
  "started_at": "2025-01-15T10:30:00Z",
  "log_file": "/tmp/bg_tasks/bg_1234567890.log"
}
```

### list.sh - List Active Tasks

```bash
# List running tasks
./list.sh

# Include completed/failed tasks
./list.sh --all

# Filter by status
./list.sh --status running
./list.sh --status completed
./list.sh --status failed
```

**Output:**

```json
{
  "success": true,
  "tasks": [
    {
      "id": "bg_1234567890",
      "name": "dev-server",
      "pid": 12345,
      "status": "running",
      "command": "npm run dev",
      "started_at": "2025-01-15T10:30:00Z",
      "duration": "5m 30s"
    }
  ],
  "count": 1
}
```

### output.sh - Get Task Output

```bash
# Get all output by ID
./output.sh --id bg_1234567890

# Get by name
./output.sh --name "dev-server"

# Last N lines only
./output.sh --name "dev-server" --tail 50

# Filter output with grep pattern
./output.sh --name "dev-server" --filter "error|warning"

# Stream output (like tail -f)
./output.sh --name "dev-server" --follow
```

**Output:**

```json
{
  "success": true,
  "id": "bg_1234567890",
  "name": "dev-server",
  "status": "running",
  "output": "Server started on port 3000\nListening...\n",
  "lines": 2
}
```

### kill.sh - Terminate Task

```bash
# Kill by ID
./kill.sh --id bg_1234567890

# Kill by name
./kill.sh --name "dev-server"

# Send specific signal (default: SIGTERM)
./kill.sh --name "dev-server" --signal SIGKILL

# Kill all tasks
./kill.sh --all
```

**Output:**

```json
{
  "success": true,
  "id": "bg_1234567890",
  "name": "dev-server",
  "pid": 12345,
  "signal": "SIGTERM",
  "killed": true
}
```

### cleanup.sh - Remove Completed Task Records

```bash
# Clean up completed tasks older than 1 hour (default)
./cleanup.sh

# Clean up all completed tasks
./cleanup.sh --all

# Clean up tasks older than N minutes
./cleanup.sh --older-than 30
```

## Common Workflows

### Development Server

```bash
# Start dev server in background
./start.sh "npm run dev" --name "frontend" --cwd ./apps/web

# Check if running
./list.sh | jq '.tasks[] | select(.name=="frontend")'

# View logs when debugging
./output.sh --name "frontend" --tail 100

# Restart server
./kill.sh --name "frontend"
./start.sh "npm run dev" --name "frontend" --cwd ./apps/web
```

### Parallel Build Tasks

```bash
# Start multiple builds
./start.sh "npm run build:client" --name "build-client"
./start.sh "npm run build:server" --name "build-server"
./start.sh "npm run build:shared" --name "build-shared"

# Monitor all
./list.sh

# Wait for completion and check results
./output.sh --name "build-client" --filter "error"
./output.sh --name "build-server" --filter "error"
```

### Watch Mode

```bash
# Start test watcher
./start.sh "npm run test:watch" --name "tests"

# Start type checker in watch mode
./start.sh "npx tsc --watch" --name "tsc"

# Check for errors periodically
./output.sh --name "tsc" --filter "error"
```

### Long-Running Processes

```bash
# Start database
./start.sh "docker compose up db" --name "postgres"

# Start API server
./start.sh "npm run api:dev" --name "api" --env "DATABASE_URL=postgres://..."

# Cleanup when done
./kill.sh --all
./cleanup.sh --all
```

## Task States

| Status      | Description                       |
| ----------- | --------------------------------- |
| `running`   | Process is currently executing    |
| `completed` | Process exited with code 0        |
| `failed`    | Process exited with non-zero code |
| `killed`    | Process was terminated by signal  |

## Storage

Task metadata and logs are stored in `/tmp/bg_tasks/`:

- `tasks.json` - Task registry with metadata
- `<task-id>.log` - Combined stdout/stderr for each task

## Error Handling

All scripts return JSON with `success: false` on error:

```json
{
  "success": false,
  "error": "Task not found: dev-server"
}
```

Common errors:

- Task not found (invalid ID or name)
- Task already completed
- Permission denied
- Command not found

## Troubleshooting

### Task shows "running" but process is dead

```bash
# Force refresh task status
./list.sh --refresh
```

### Can't kill zombie process

```bash
# Use SIGKILL
./kill.sh --name "stuck-process" --signal SIGKILL
```

### Log files growing too large

```bash
# Clean up old logs
./cleanup.sh --older-than 60
```

### Find orphaned processes

```bash
# List all processes with their PIDs
./list.sh | jq '.tasks[] | {name, pid}'
# Then verify with: ps -p <pid>
```

## Integration Notes

- All output is JSON to stdout for easy parsing with `jq`
- Exit codes: 0 = success, 1 = error
- Errors output to stderr as JSON
- Task names must be unique; starting a task with existing name fails
- Use `--name` for human-readable references vs auto-generated IDs
