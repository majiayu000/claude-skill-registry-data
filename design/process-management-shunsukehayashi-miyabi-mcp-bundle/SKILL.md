---
name: process-management
description: Process management including listing, finding, killing processes and managing tmux sessions. Use when managing running processes, investigating resource usage, or working with terminal multiplexers.
allowed-tools: Bash, Read
mcp_tools:
  - "process_list"
  - "process_find"
  - "process_kill"
  - "process_tree"
  - "process_ports"
  - "process_env"
  - "process_files"
  - "process_limits"
  - "process_memory_map"
  - "process_threads"
  - "process_priority"
  - "process_wait"
  - "process_signal"
  - "process_cwd"
  - "tmux_list_sessions"
  - "tmux_list_windows"
  - "tmux_send_keys"
  - "tmux_capture_pane"
  - "tmux_create_session"
  - "tmux_kill_session"
  - "tmux_new_window"
  - "tmux_select_window"
  - "tmux_split_pane"
  - "tmux_resize_pane"
---

# Process Management Skill

**Version**: 1.0.0
**Purpose**: Process and tmux session management

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Process | "list processes", "find process", "プロセス一覧" |
| Kill | "kill process", "stop process", "プロセス停止" |
| Ports | "which process on port", "ポート確認" |
| Tmux | "tmux sessions", "create session", "Tmux操作" |

---

## Integrated MCP Tools

### Process Operations

| Tool | Purpose |
|------|---------|
| `process_list` | List all processes |
| `process_find` | Find by name/pattern |
| `process_kill` | Terminate process |
| `process_tree` | Process tree view |
| `process_ports` | Processes by port |
| `process_env` | Environment variables |
| `process_files` | Open file descriptors |
| `process_limits` | Resource limits |
| `process_memory_map` | Memory mapping |
| `process_threads` | Thread list |
| `process_priority` | Process priority (nice) |
| `process_wait` | Wait for completion |
| `process_signal` | Send signal |
| `process_cwd` | Working directory |

### Tmux Operations

| Tool | Purpose |
|------|---------|
| `tmux_list_sessions` | Active sessions |
| `tmux_list_windows` | Windows in session |
| `tmux_send_keys` | Send keystrokes |
| `tmux_capture_pane` | Capture pane content |
| `tmux_create_session` | Create new session |
| `tmux_kill_session` | Terminate session |
| `tmux_new_window` | Add window |
| `tmux_select_window` | Switch window |
| `tmux_split_pane` | Split pane |
| `tmux_resize_pane` | Resize pane |

---

## Workflow: Process Investigation

### Phase 1: Discovery

#### Step 1.1: List Processes
```
Use process_list with:
- sort: "cpu" or "memory"
- limit: 20
```

#### Step 1.2: Find Specific Process
```
Use process_find with:
- name: Process name pattern
- user: Specific user (optional)
```

### Phase 2: Analysis

#### Step 2.1: Process Tree
```
Use process_tree to see parent/child relationships
```

#### Step 2.2: Resource Usage
```
Use process_limits to check:
- Max open files
- Max processes
- Memory limits
```

### Phase 3: Port Investigation

#### Step 3.1: Find by Port
```
Use process_ports with:
- port: Port number

Identifies which process is using the port
```

---

## Workflow: Tmux Management

### Step 1: List Sessions
```
Use tmux_list_sessions to see all sessions
```

### Step 2: Create Session
```
Use tmux_create_session with:
- session_name: Descriptive name
- window_name: Initial window name
```

### Step 3: Send Commands
```
Use tmux_send_keys with:
- session: Session name
- keys: Command to execute
```

### Step 4: Capture Output
```
Use tmux_capture_pane with:
- session: Session name
- pane: Pane number
```

---

## Common Signals

| Signal | Number | Purpose |
|--------|--------|---------|
| SIGTERM | 15 | Graceful termination |
| SIGKILL | 9 | Force kill |
| SIGHUP | 1 | Hangup/reload |
| SIGINT | 2 | Interrupt (Ctrl+C) |
| SIGSTOP | 19 | Pause process |
| SIGCONT | 18 | Resume process |

---

## Best Practices

✅ GOOD:
- Use SIGTERM before SIGKILL
- Check process tree before killing
- Name tmux sessions descriptively
- Use tmux for long-running tasks

❌ BAD:
- SIGKILL as first option
- Kill without investigation
- Leave orphan processes
- Unnamed tmux sessions

---

## Checklist

- [ ] Process identified (PID/name)
- [ ] Resource usage checked
- [ ] Port conflicts resolved
- [ ] Graceful termination attempted
- [ ] Tmux sessions organized
