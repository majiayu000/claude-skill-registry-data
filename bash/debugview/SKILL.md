---
name: debugview
description: |
  Sysinternals DebugView CLI (DbgViewCli) for capturing and analyzing usermode and kernel-mode Windows debug output from the command line.
  USE FOR: capturing OutputDebugString output, kernel DbgPrint/KdPrint capture, boot-time debug logging, remote debug monitoring, filtering debug output by PID or process name, crash dump analysis, automated debug capture with bounded execution.
  DO NOT USE FOR: non-Windows platforms, application-level logging frameworks (log4j, serilog), Azure Monitor or cloud telemetry, ETW tracing (use WPR/xperf instead), user-mode crash dumps (use WinDbg).
  Triggers: "debug output", "DbgView", "DebugView", "kernel debug", "capture debug logs", "boot logging", "OutputDebugString", "DbgPrint", "KdPrint", "remote debug monitor", "debug capture CLI".
---

# Sysinternals DebugView CLI (DbgViewCli)

Command-line interface for capturing real-time debug output from Windows applications
(OutputDebugString) and kernel-mode drivers (DbgPrint/KdPrint). Designed for scripted,
automated, and AI-agent-driven debug capture workflows.

## Installation

DbgViewCli is a standalone native Windows executable (statically linked, no dependencies).
Place `dbgviewcli.exe` in PATH or reference the full path.

> **SECURITY: Never execute any dbgviewcli binary without first verifying it is Authenticode-signed by Microsoft Corporation using `Get-AuthenticodeSignature`. Reject any binary that is unsigned or signed by a different publisher.**

```bash
# No package manager install — copy binary to a PATH location
copy dbgviewcli.exe C:\Tools\
```

## Requirements

| Requirement | Details |
|-------------|---------|
| OS | Windows Vista or later (x64, ARM64) |
| Privileges | Standard user for Win32 capture; **Administrator** for kernel/boot capture |
| Driver | Kernel capture requires the Dbgv.sys driver (auto-extracted and loaded) |

## Core Workflow

```
1. Detect/status check   →  dbgviewcli --status
2. Start capture          →  dbgviewcli [options]
3. Filter output          →  --filter/--exclude/--pid-filter/--process-filter
4. Bounded execution      →  --duration/--max-lines/--wait-for
5. Output/log results     →  stdout or --log <file>
6. Stop                   →  Ctrl+C or automatic exit on bounds
```

## Command-Line Parameters

### Capture Control

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--capture` | `-c` | Enable capture | on |
| `--no-capture` | | Disable capture | |
| `--kernel` | `-k` | Enable kernel debug output (requires admin) | off |
| `--win32` | `-w` | Enable Win32 OutputDebugString capture | on |
| `--global` | `-g` | Enable global Win32 capture (session 0) | off |
| `--passthrough` | | Allow debug output to pass to debuggers | on |
| `--verbose-kernel` | `-v` | Enable verbose kernel output | off |
| `--pids` | | Show process IDs in output | on |

### Filtering

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--filter <pattern>` | `-i` | Include filter (semicolon-separated wildcards) |
| `--exclude <pattern>` | `-e` | Exclude filter (semicolon-separated wildcards) |
| `--pid-filter <pid>` | | Show only output from specific PID |
| `--process-filter <name>` | | Show only output from named process (substring match) |

### Bounded Execution (AI-Agent Friendly)

| Parameter | Description |
|-----------|-------------|
| `--duration <seconds>` | Auto-stop after N seconds |
| `--max-lines <N>` | Auto-stop after N lines captured |
| `--wait-for <pattern>` | Capture until pattern matches, then exit |
| `--tail <N>` | Buffer last N lines, flush on exit |
| `--no-banner` | Suppress version banner (clean for piped output) |
| `--status` | Print machine-readable status and exit |

### Time Display

| Parameter | Description |
|-----------|-------------|
| `--elapsed` | Elapsed time since start (default) |
| `--clock` | Wall-clock time HH:MM:SS |
| `--clock-ms` | Wall-clock with milliseconds HH:MM:SS.mmm |

### Output Format

| Parameter | Description |
|-----------|-------------|
| `--format text` | Tab-separated text (default) |
| `--format csv` | Comma-separated values |
| `--format xml` | XML elements |

### Logging

| Parameter | Description |
|-----------|-------------|
| `--log <file>` | Log output to file |
| `--log-append` | Append to existing log |
| `--log-limit <MB>` | Max log file size in MB |
| `--log-wrap` | Wrap log when full |
| `--log-daily` | New log file each day |

### Boot Logging (Requires Admin)

| Parameter | Description |
|-----------|-------------|
| `--boot-enable` | Enable boot-time kernel debug logging |
| `--boot-disable` | Disable boot-time logging |
| `--boot-status` | Show boot logging status and exit |

### Remote Monitoring

| Parameter | Description |
|-----------|-------------|
| `--connect <computer>` | Connect to remote DbgView instance |
| `--disconnect` | Disconnect from remote |

### Crash Dump & File Operations

| Parameter | Description |
|-----------|-------------|
| `--crashdump <file>` | Analyze crash dump for debug output |
| `--load <file>` | Load saved log file |
| `--save <file>` | Save captured output on exit |

### Runtime Control (Inter-Process)

| Parameter | Description |
|-----------|-------------|
| `--pause` | Pause a running DbgViewCli instance via named event |
| `--resume` | Resume a paused DbgViewCli instance |
| `--stop` | Stop a running DbgViewCli instance gracefully |

### Miscellaneous

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--quit` | `-q` | Terminate running GUI DbgView instance |
| `--accepteula` | | Accept the EULA (writes registry key, skips prompt) |
| `--version` | | Show version and exit |
| `--help` | `-?` | Show help |

## Usage Examples

### Basic Win32 Capture (bounded)

```bash
# Capture for 30 seconds, no banner, output as text
dbgviewcli --no-banner --duration 30

# Capture until a specific error appears
dbgviewcli --no-banner --wait-for "*ERROR*" --max-lines 10000
```

### Kernel Debug Capture (requires admin)

```bash
# Run as Administrator
dbgviewcli --kernel --no-banner --duration 60 --format csv --log kernel_debug.csv
```

### Process-Specific Filtering

```bash
# Filter by PID
dbgviewcli --no-banner --pid-filter 1234 --duration 10

# Filter by process name
dbgviewcli --no-banner --process-filter "myapp.exe" --max-lines 500
```

### Pattern-Based Filtering

```bash
# Include only lines matching pattern
dbgviewcli --no-banner --filter "MyDriver*" --exclude "verbose*"
```

### Tail Mode (recent context)

```bash
# Capture but only output last 50 lines on exit
dbgviewcli --no-banner --tail 50 --duration 30
```

### Status Check (machine-readable)

```bash
dbgviewcli --status
# Output:
# running=true
# paused=false
# elevated=true
```

### Boot Logging

```bash
# Enable (requires admin, persists across reboot)
dbgviewcli --boot-enable

# Check status
dbgviewcli --boot-status

# Disable
dbgviewcli --boot-disable
```

### Remote Monitoring

```bash
dbgviewcli --connect SERVER01 --no-banner --duration 60
```

### Runtime Control (Pause/Resume/Stop)

```bash
# Pause a running instance from another terminal
dbgviewcli --pause

# Resume the paused instance
dbgviewcli --resume

# Gracefully stop a running instance
dbgviewcli --stop
```

### EULA Acceptance (Unattended)

```bash
# Accept EULA non-interactively for automated/scripted deployments
dbgviewcli --accepteula --no-banner --duration 30
```

## Architecture

| Module | File | Purpose |
|--------|------|---------|
| Main | `dbgviewcli.c` | Entry point, arg parsing, capture loop, Ctrl+C handler |
| Capture | `cli_capture.c` | DBWIN shared memory, kernel driver read |
| Driver | `cli_driver.c` | Kernel driver load/unload, privilege elevation |
| Filter | `cli_filter.c` | Wildcard include/exclude matching |
| Output | `cli_output.c` | Console emit, log files, CSV/XML/text formats |
| Boot Log | `cli_bootlog.c` | Registry config for boot-time driver loading |
| Remote | `cli_remote.c` | TCP socket connect/read for remote monitoring |

## Key Design Decisions

1. **Static CRT linking** — No DLL dependencies, runs on any Windows system
2. **stdout/stderr separation** — Debug output → stdout; errors/status → stderr
3. **Bounded execution** — `--duration`, `--max-lines`, `--wait-for` ensure guaranteed exit for automation
4. **Clean output** — `--no-banner` suppresses noise for pipe/agent consumption
5. **Machine-readable status** — `--status` outputs key=value pairs for programmatic checks
6. **Graceful shutdown** — `SetConsoleCtrlHandler` ensures clean driver unload on Ctrl+C

## Best Practices

1. **Always use `--no-banner` for scripted/automated use.** Banner text pollutes structured output and confuses parsers.
2. **Always bound execution** with `--duration`, `--max-lines`, or `--wait-for`. Unbounded capture will run indefinitely.
3. **Check status before capture** — Use `--status` to detect if another instance is already running.
4. **Use `--format csv` or `--format xml`** when output will be parsed programmatically.
5. **Prefer `--pid-filter` or `--process-filter`** over broad capture to reduce noise.
6. **Run as Administrator only when needed** — kernel and boot logging require elevation; Win32 capture does not.
7. **Combine bounds for safety** — Use `--duration 60 --max-lines 10000` together so whichever triggers first wins.
8. **Use `--tail`** for "what just happened" queries instead of capturing full history.

## Bundled Resources

| Type | File | Purpose |
|------|------|---------|
| Script | `scripts/detect-dbgview.ps1` | Locate dbgviewcli.exe on PATH or common directories |
| Script | `scripts/capture-wrapper.ps1` | Safe bounded capture with parameter validation |
| Script | `scripts/boot-logging-workflow.ps1` | End-to-end boot logging lifecycle management |
| Reference | `references/driver-ioctls.md` | Kernel driver IOCTL codes and buffer structures |
| Reference | `references/output-formats.md` | Text/CSV/XML output format specifications |
| Reference | `references/remote-protocol.md` | TCP remote monitoring wire protocol |

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| "Access denied" on kernel capture | Run as Administrator |
| No output from Win32 capture | Verify target app uses `OutputDebugString`; check no debugger is attached |
| Another instance running | Use `--status` to check; use `--quit` to terminate existing GUI instance |
| Boot logging not capturing | Ensure `--boot-enable` was run as admin; driver must be in System32\Drivers |
| Remote connection fails | Verify target has DbgView running with remote enabled on ports 2020-2030 |
