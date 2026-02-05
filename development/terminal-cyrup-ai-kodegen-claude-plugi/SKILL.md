---
name: terminal
description: >
  Execute shell commands in persistent, stateful VT100 terminal sessions.
  WHEN: User needs to "run a command", "execute shell", "build project", "run tests", "deploy", system administration.
  WHEN NOT: Simple file operations (use fs_* tools), reading known files (use fs_read_file).
version: 0.1.0
---

# terminal - Shell Command Execution

## Core Concept

`mcp__plugin_kg_kodegen__terminal` executes shell commands in persistent VT100 terminal sessions. Terminals maintain environment variables, working directory, and shell state across commands. Use different terminal numbers for parallel work.

## Actions

| Action | Description | Required Parameters |
|--------|-------------|---------------------|
| `EXEC` | Execute command (default) | `command` |
| `READ` | Get current buffer snapshot | None |
| `LIST` | Show all active terminals | None |
| `KILL` | Gracefully shutdown terminal | None |

## Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `"EXEC"` | Action to perform |
| `terminal` | number | 0 | Terminal instance (0, 1, 2...) |
| `command` | string | null | Command to execute (EXEC only) |
| `await_completion_ms` | number | 300000 | Max wait time (5 min default) |
| `clear` | boolean | true | Clear buffer before command |
| `tail` | number | 2000 | Max output lines to return |

## Usage Examples

### Execute Command (default action)
```json
{ "command": "ls -la" }
```

### Execute in Specific Terminal
```json
{ "terminal": 1, "command": "cargo build --release" }
```

### Background Execution (fire-and-forget)
```json
{
  "command": "npm run build",
  "await_completion_ms": 0
}
```

### Execute with Timeout
```json
{
  "command": "cargo test",
  "await_completion_ms": 60000
}
```

### Read Current Buffer
```json
{ "action": "READ", "terminal": 0 }
```

### List All Terminals
```json
{ "action": "LIST" }
```

### Kill Terminal
```json
{ "action": "KILL", "terminal": 0 }
```

## Response Format

```json
{
  "terminal": 0,
  "exit_code": 0,
  "cwd": "/project/path",
  "duration_ms": 1234,
  "completed": true
}
```

## Parallel Work Pattern

Use different terminal numbers for concurrent tasks:

```json
// Terminal 0: Build
{ "terminal": 0, "command": "cargo build" }

// Terminal 1: Tests (parallel)
{ "terminal": 1, "command": "cargo test" }

// Terminal 2: Watch logs
{ "terminal": 2, "command": "tail -f app.log" }
```

## Background Execution

For long-running commands:

1. **Fire-and-forget**: `await_completion_ms: 0`
2. **Check progress**: `{ "action": "READ", "terminal": N }`
3. **Wait with timeout**: If timeout occurs, command continues in background

## Important Notes

- **Persistent sessions**: Environment and working directory preserved
- **VT100 emulation**: Actual rendered terminal output, not raw bytes
- **Automatic cleanup**: Terminals cleaned up on connection close
- **State preservation**: `cd` commands persist across calls

## Remember

- Terminals are numbered 0, 1, 2... - use different numbers for parallel work
- Default action is EXEC - just provide `command`
- Use `await_completion_ms: 0` for background tasks
- Use `action: "READ"` to check on background commands
- Working directory persists - `cd` works across commands
- For simple file operations, prefer `fs_*` tools (faster, safer)
