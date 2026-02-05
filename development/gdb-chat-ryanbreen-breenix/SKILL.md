---
name: gdb-chat
description: Conversational GDB debugging for Breenix kernel. Use for interactive debugging sessions - set breakpoints, inspect registers, examine memory, step through code, investigate crashes.
---

# Breenix GDB Chat

Conversational GDB debugging interface for Breenix kernel development.

## When to Use This Skill

Use this skill when you need **interactive, stateful GDB debugging**:

- Investigating crashes, page faults, or exceptions
- Stepping through syscall execution
- Examining register state at specific points
- Setting breakpoints and watchpoints
- Analyzing memory contents
- Tracing context switches

## Quick Reference

```bash
# Start a debug session
breenix-gdb-chat/scripts/start_session.py

# Execute GDB commands
breenix-gdb-chat/scripts/gdb_cmd.py --session SESSION_ID --command "info registers"
breenix-gdb-chat/scripts/gdb_cmd.py --session SESSION_ID -c "break main" -c "continue"

# Stop session
breenix-gdb-chat/scripts/stop_session.py --session SESSION_ID

# List active sessions
breenix-gdb-chat/scripts/list_sessions.py
```

## Workflow Example

### Investigating a Page Fault

```bash
# 1. Start session
$ breenix-gdb-chat/scripts/start_session.py
{"session_id": "gdb_20251204_151030", "status": "connected"}

# 2. Set breakpoint
$ breenix-gdb-chat/scripts/gdb_cmd.py --session gdb_20251204_151030 \
    --command "break page_fault_handler"
{"success": true, "output": "Breakpoint 1 at 0xffffffff80003450"}

# 3. Continue to breakpoint
$ breenix-gdb-chat/scripts/gdb_cmd.py --session gdb_20251204_151030 \
    --command "continue"
{"success": true, "output": "Breakpoint 1, page_fault_handler()"}

# 4. Check faulting address (CR2)
$ breenix-gdb-chat/scripts/gdb_cmd.py --session gdb_20251204_151030 \
    --command "print/x \$cr2"
{"success": true, "output": "0x0000000000000008"}

# 5. Get backtrace
$ breenix-gdb-chat/scripts/gdb_cmd.py --session gdb_20251204_151030 \
    --command "backtrace"
{"success": true, "output": [{"function": "page_fault_handler", ...}]}

# 6. Check local variables
$ breenix-gdb-chat/scripts/gdb_cmd.py --session gdb_20251204_151030 \
    -c "frame 1" -c "info locals"

# 7. Stop session
$ breenix-gdb-chat/scripts/stop_session.py --session gdb_20251204_151030
```

## Available Commands

### Execution Control

| Command | Description |
|---------|-------------|
| `continue` / `c` | Continue execution |
| `step` / `s` | Step one source line |
| `stepi` / `si` | Step one instruction |
| `next` / `n` | Step over function calls |
| `nexti` / `ni` | Step over one instruction |
| `finish` | Run until function returns |

### Breakpoints

| Command | Description |
|---------|-------------|
| `break LOCATION` | Set breakpoint (function, file:line, *address) |
| `hbreak LOCATION` | Hardware breakpoint (works before paging) |
| `tbreak LOCATION` | Temporary breakpoint (deletes after hit) |
| `watch EXPR` | Break when memory is written |
| `rwatch EXPR` | Break when memory is read |
| `info breakpoints` | List all breakpoints |
| `delete N` | Delete breakpoint N |

### Registers

| Command | Description |
|---------|-------------|
| `info registers` | Show general-purpose registers |
| `print/x $REG` | Show specific register (e.g., `$rip`, `$rax`) |
| `print/x $cr2` | Page fault address |
| `print/x $cr3` | Current page table |
| `show-segments` | Show segment registers (custom) |
| `show-control` | Show control registers (custom) |

### Memory

| Command | Description |
|---------|-------------|
| `x/Nxg ADDR` | Examine N 8-byte values at ADDR |
| `x/Nxw ADDR` | Examine N 4-byte values |
| `x/Ni ADDR` | Disassemble N instructions |
| `x/s ADDR` | Show string at ADDR |
| `disassemble` | Disassemble current function |
| `disassemble FUNC` | Disassemble specific function |

### Stack & Frames

| Command | Description |
|---------|-------------|
| `backtrace` / `bt` | Show call stack |
| `backtrace full` | Show stack with locals |
| `frame N` | Select frame N |
| `info locals` | Show local variables |
| `info args` | Show function arguments |

## Kernel-Specific Tips

### Page Fault Investigation
```bash
--command "print/x \$cr2"     # Faulting address
--command "print/x \$rip"     # Faulting instruction
--command "x/i \$rip"         # Show faulting instruction
--command "backtrace"         # Call stack
```

### Syscall Debugging
```bash
--command "break rust_syscall_handler"
--command "continue"
--command "print/x \$rax"     # Syscall number
--command "print/x \$rdi"     # First argument
--command "step"              # Step into handler
```

### Timer/Interrupt Analysis
```bash
--command "break timer_interrupt_handler"
--command "continue"
--command "info registers"    # See state at interrupt
--command "finish"            # Complete handler
```

### Context Switch Tracing
```bash
--command "break check_need_resched_and_switch"
--command "continue"
--command "info locals"       # See scheduler state
```

## Script Options

### start_session.py
```
--mode uefi|bios    Boot mode (default: uefi)
--timeout SECONDS   Session timeout (default: 300)
--kernel PATH       Kernel binary path (auto-detected)
--debug             Print debug output
```

### gdb_cmd.py
```
--session ID        Session ID (required)
--command CMD       GDB command (can specify multiple with -c)
--timeout SECONDS   Command timeout (default: 30)
--format json|text  Output format (default: json)
```

### stop_session.py
```
--session ID        Session ID (required)
--force             Force kill without cleanup
```

### list_sessions.py
```
--format json|text  Output format (default: json)
--cleanup           Remove dead sessions
```

## Session State

Sessions are stored in `/tmp/breenix_gdb_sessions/`:
- `SESSION_ID.json` - Session metadata
- `SESSION_ID.log` - GDB command log
- `SESSION_ID.qemu.log` - QEMU output

## Troubleshooting

### Session not found
```bash
# List all sessions
breenix-gdb-chat/scripts/list_sessions.py

# Clean up dead sessions
breenix-gdb-chat/scripts/list_sessions.py --cleanup

# Start fresh session
breenix-gdb-chat/scripts/start_session.py
```

### Command timeout
The target may be hung. Try:
```bash
# Force stop and restart
breenix-gdb-chat/scripts/stop_session.py --session ID --force
breenix-gdb-chat/scripts/start_session.py
```

### Cannot connect to QEMU
Check QEMU started correctly:
```bash
cat /tmp/breenix_gdb_sessions/SESSION_ID.qemu.log
```
