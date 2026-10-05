---
name: s32ds-mi-debug-commands
description: Guide for using execute_action(action_name="runMiDebugCommand", ...) to execute raw GDB Machine Interface (MI) and CLI commands on active debug sessions. Covers when to use MI commands vs the dedicated Debugger MCP server, available MI command categories (breakpoints, execution, memory, registers, stack, variables), S32Debugger-specific commands, and error handling. The Debugger MCP server should be the primary tool - MI commands are the fallback for S32Debugger launches or when the debugger REST server is unavailable.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  tags: '[s32ds, debug, mi-commands, gdb, s32-debugger, fallback, machine-interface]'
---
# MI Debug Commands

## Goal
Execute raw GDB Machine Interface (MI) and CLI commands on active debug sessions using `execute_action(action_name="runMiDebugCommand", ...)`, understanding when this tool is appropriate versus the dedicated Debugger MCP server.

## Tools Used
- `search_actions` - call FIRST to discover available actions; the returned catalog includes each action's input schema
- `execute_action` - invoke any discovered action via `execute_action(action_name="X", params={...})`; the static `start_tool` action brings the IDE up if it is not running
- The `waitForJob` action (via `execute_action`) - blocks until a named async job completes

##  Before You Start
Call `search_actions(query="...")` first to discover all available actions, their descriptions, and input schemas (a parameterless `search_actions()` browses everything). Use the returned catalog to determine correct action names and required/optional parameters before calling `execute_action`.

## Prerequisites
- [ ] An active debug session is running (started via `execute_action(action_name="startDebug", ...)` + the `waitForJob` action)
- [ ] The exact launch configuration name is known (required as the `launch` parameter)
- [ ] The target is halted (most MI commands require a stopped target)

## Guardrails

**Destructive actions**
- Memory/register writes (`-data-write-memory-bytes`, `-gdb-set $reg=...`) and `monitor reset`/`monitor halt`/`monitor flash_download` change target state. Confirm the exact address/register/value (and file for flash) before sending.

**Resource limits**
- Do not issue destructive or execution commands in tight loops; poll target state between steps instead.

## When to Use (Decision Priority)


### PRIMARY: Use the Debugger MCP Server
The dedicated Debugger MCP server (debugger REST API tools like `gdb_execute`, `gdb_set_breakpoint`, `gdb_read_memory`, etc.) should **always** be the first choice for debug interactions. It provides:
- Structured, typed responses
- Better error handling
- Higher-level abstractions
- Session management

### FALLBACK: Use `execute_action(action_name="runMiDebugCommand", ...)`
Only use `execute_action(action_name="runMiDebugCommand", ...)` when:

1. **The launch is an S32Debugger launch** - S32Debugger (NXP's proprietary debug engine) uses a specialized debug protocol not fully supported by the standard Debugger MCP server. Launch configs ending in `_S32DP` or using S32 Debug Probe are S32Debugger launches.

2. **The Debugger REST server is not available/connected** - If the debugger MCP server is not running, not connected, or returns connection errors, fall back to MI commands through S32DS.

3. **S32Debugger-specific commands** - Some commands (e.g., flash-related, secure debug, multicore thread control via S32Debugger) are only available through the S32DS MI interface.

```
Decision Tree:
─────────────
Is the Debugger MCP server available and connected?
├─ YES -> Is this an S32Debugger launch (_S32DP suffix)?
│   ├─ YES -> Use execute_action(action_name="runMiDebugCommand", ...) (fallback)
│   └─ NO  -> Use Debugger MCP server tools (primary) ✓
└─ NO -> Use execute_action(action_name="runMiDebugCommand", ...) (fallback)
```

## Tool Signature

```python
execute_action(action_name="runMiDebugCommand", params={"launch": "<name>", "command": "<mi_command>"})
```

**Parameters:**
- `action_name` (REQUIRED): Must be `"runMiDebugCommand"`
- `params.launch` (REQUIRED): The exact name of the active debug launch configuration (e.g., `"MyProject_Debug_S32DP"`)
- `params.command` (REQUIRED): The GDB MI or CLI command string to execute

**Returns:**
- Success: `{ "result": "<output>", "msg": "<status>" }`
- Failure: `{ "error": "<error message>" }`

## Available MI Commands Reference

### Execution Control
| Command | Description |
|---------|-------------|
| `-exec-run` | Start program execution |
| `-exec-continue` | Resume execution after halt |
| `-exec-step` | Step into (source line) |
| `-exec-next` | Step over (source line) |
| `-exec-step-instruction` | Step into (single instruction) |
| `-exec-next-instruction` | Step over (single instruction) |
| `-exec-finish` | Run until current function returns |
| `-exec-until <location>` | Run until specified location |
| `-exec-interrupt` | Halt execution (async) on sync MANDATORY use execute_action(action_name="executeCommand", params={"commandId": "org.eclipse.debug.ui.commands.Suspend"})|

### Breakpoints
| Command | Description |
|---------|-------------|
| `-break-insert <location>` | Set breakpoint (function, file:line, or address) |
| `-break-insert -t <location>` | Set temporary breakpoint (auto-delete after hit) |
| `-break-insert -h *<address>` | Set hardware breakpoint at address |
| `-break-delete <id>` | Delete breakpoint by number |
| `-break-disable <id>` | Disable breakpoint |
| `-break-enable <id>` | Enable breakpoint |
| `-break-list` | List all breakpoints |
| `-break-condition <id> <expr>` | Set conditional breakpoint |
| `-break-watch <expr>` | Set watchpoint on expression |

### Registers
| Command | Description |
|---------|-------------|
| `-data-list-register-names` | List all register names |
| `-data-list-register-values x` | Read all register values (hex) |
| `-data-list-register-values x <regNo>` | Read specific register (by index) |
| `-data-list-changed-registers` | List registers changed since last stop |
| `-gdb-set $<reg>=<value>` | Write a register value |

### Memory
| Command | Description |
|---------|-------------|
| `-data-read-memory-bytes <addr> <count>` | Read memory bytes |
| `-data-read-memory <addr> x 4 1 <count>` | Read memory as 32-bit hex words |
| `-data-write-memory-bytes <addr> <hex>` | Write memory bytes |
| `-data-evaluate-expression *((int*)<addr>)` | Read a single word at address |

### Stack & Frames
| Command | Description |
|---------|-------------|
| `-stack-list-frames` | List all stack frames (backtrace) |
| `-stack-list-frames 0 5` | List top 5 frames |
| `-stack-info-depth` | Get stack depth |
| `-stack-select-frame <n>` | Select frame number |
| `-stack-list-locals 1` | List local variables in current frame |
| `-stack-list-arguments 1` | List function arguments |

### Variables & Expressions
| Command | Description |
|---------|-------------|
| `-data-evaluate-expression <expr>` | Evaluate C expression |
| `-var-create - * <expr>` | Create variable object for watching |
| `-var-update *` | Update all variable objects |
| `-var-list-children <name>` | List struct/array children |
| `-var-delete <name>` | Delete variable object |
| `-symbol-info-functions` | List all functions |

### Thread/Core Control (Multicore)
| Command | Description |
|---------|-------------|
| `-thread-info` | List all threads (cores in multicore) |
| `-thread-select <id>` | Switch to thread/core |
| `info threads` | CLI: show all threads with status |
| `thread <id>` | CLI: switch to thread |
| `set scheduler-locking on` | Only current thread runs on step |
| `set scheduler-locking off` | All threads run on step |

### Program Info
| Command | Description |
|---------|-------------|
| `-file-exec-and-symbols <path>` | Load symbol file |
| `-data-disassemble -s <addr> -e <addr> -- 0` | Disassemble address range |
| `info functions <regex>` | Search functions by name |
| `info variables <regex>` | Search global variables |
| `info address <symbol>` | Get address of symbol |
| `print <expression>` | Print/evaluate expression (CLI) |
| `x/<N><fmt> <addr>` | Examine memory (CLI format) |

### S32Debugger-Specific Commands
| Command | Description |
|---------|-------------|
| `monitor reset` | Reset the target |
| `monitor halt` | Force-halt the target |
| `monitor flash_download <path>` | Flash an ELF file to target |
| `monitor get_state` | Get target state |
| `monitor secure_debug unlock` | Unlock secure debug (if supported); for a full SDAF password / challenge-response unlock flow use the `s32sdaf-secure-debug-session` skill |
| `set mem inaccessible-by-default off` | Allow access to unmapped memory |

## Usage Examples

### Example 1: Read all registers
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-data-list-register-values x"}
)
```

### Example 2: Set a breakpoint at a function
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-break-insert main"}
)
```

### Example 3: Read 64 bytes of memory at address 0x20000000
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-data-read-memory-bytes 0x20000000 64"}
)
```

### Example 4: Step and check PC
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-exec-step"}
)
# Then read PC register (index varies by architecture, typically reg 15 for ARM)
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-data-list-register-values x 15"}
)
```

### Example 5: Evaluate a variable
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "-data-evaluate-expression myGlobalVar"}
)
```

### Example 6: Reset the target (S32Debugger only)
```
execute_action(
    action_name="runMiDebugCommand",
    params={"launch": "MyProject_Debug_S32DP", "command": "monitor reset"}
)
```

## Error Catalog

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `"error": "No active debug session"` | Debug session not started or already terminated | Start debug with `execute_action(action_name="startDebug", ...)` first |
| `"error": "Parameter 'launch' is required"` | Empty or missing launch name | Provide the exact launch config name |
| `"Cannot execute command: target running"` | Target is not halted | Send `-exec-interrupt` first, then retry |
| `"No symbol table loaded"` | ELF not loaded or stripped | Ensure build was done with debug info (`-g`) |
| `"Cannot access memory at address 0x..."` | Invalid/protected memory region | Check address is valid for this core's memory map |
| `"Unknown thread <id>"` | Invalid thread/core ID | Use `-thread-info` to list valid thread IDs |
| MI command returns empty result | Command succeeded but no output | This is normal for some commands (e.g., `-exec-continue`) |

## Anti-Patterns
-  Using `execute_action(action_name="runMiDebugCommand", ...)` when the Debugger MCP server is available and the launch is NOT S32Debugger - always prefer the dedicated MCP tools
-  Sending execution commands (`-exec-continue`, `-exec-step`) without waiting for the target to stop - check state first
-  Forgetting the `-` prefix for MI commands (e.g., writing `exec-step` instead of `-exec-step`)
-  Mixing MI and CLI syntax incorrectly - MI commands start with `-`, CLI commands are plain text (e.g., `print`, `info`, `monitor`)
-  Sending commands to a terminated session - verify the session is still active
-  Using `monitor` commands on non-S32Debugger launches - `monitor` commands are probe-specific

## Related Skills
- `s32ds-multicore-debug` - multicore debugging with thread/core control
- `s32ds-build-and-debug` - starting a debug session (prerequisite)
- `s32ds-setup-debug-config` - finding and configuring launch configurations
- `s32ds-flash-target` - flashing firmware to the target
- `s32sdaf-secure-debug-session` - unlock a secured device (SDAF password / challenge-response) before debugging

## Notes
- **MI vs CLI**: Commands prefixed with `-` are MI commands (machine-readable output). Commands without prefix are CLI commands (human-readable output). Both work with `execute_action(action_name="runMiDebugCommand", ...)`.
- **Async commands**: Execution commands (`-exec-continue`, `-exec-run`) return immediately. The target state change comes as an async notification. Poll with `-thread-info` or `-data-evaluate-expression $pc` to check if halted.
- **S32Debugger specifics**: S32Debugger extends GDB with `monitor` commands for target-specific operations (flash, reset, secure debug). These are NOT available on standard GDB/OpenOCD launches.
- **Response format**: MI responses follow the GDB MI output syntax. Success records start with `^done`, error records with `^error`. The tool wraps these into JSON.
- **Performance**: Each MI command is a round-trip to the debug session. For bulk operations (reading large memory regions), prefer single commands with larger ranges over multiple small commands.
