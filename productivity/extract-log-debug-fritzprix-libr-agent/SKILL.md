---
name: extract-log-debug
description: Extract and analyze LibrAgent debug logs with pattern matching and context. Use when debugging LibrAgent issues, analyzing agent workflows, investigating tool execution problems, or extracting specific log patterns like errors, warnings, planning operations, MCP tool calls, or browser automation traces. Supports extracting last N lines or searching for patterns with surrounding context.
---

# Extract Log Debug

Extract and analyze LibrAgent debug logs for troubleshooting and analysis.

## Quick Start

Extract logs using the Python script:

```bash
# Extract last 100 lines
python scripts/extract_logs.py -n 100

# Extract all errors with 5 lines of context
python scripts/extract_logs.py --pattern "[ERROR]" --context 5

# Extract planning logs
python scripts/extract_logs.py --pattern "PLANNING" -n 5000

# Save to custom file
python scripts/extract_logs.py --pattern "[WARN]" -o warnings.txt
```

## Log File Location

LibrAgent stores logs in platform-specific directories:

- **Windows**: `%LOCALAPPDATA%\com.fritzprix.libragent\logs\libragent.log`
- **macOS**: `~/Library/Logs/com.fritzprix.libragent/libragent.log`
- **Linux**: `~/.local/share/com.fritzprix.libragent/logs/libragent.log`

The script automatically detects and uses the correct path.

## Common Patterns

### Error Extraction

```bash
python scripts/extract_logs.py --pattern "[ERROR]" --context 10
```

### Component-Specific Logs

```bash
# Agent workflow logs
python scripts/extract_logs.py --pattern "agent_" -n 5000

# MCP tool execution
python scripts/extract_logs.py --pattern "MCPServiceProxy" --context 10

# Planning operations
python scripts/extract_logs.py --pattern "PLANNING" --context 5

# Browser automation
python scripts/extract_logs.py --pattern "BrowserServer" --context 10
```

### Recent Activity

```bash
# Last 500 lines for quick check
python scripts/extract_logs.py -n 500

# Last 5000 lines for detailed analysis
python scripts/extract_logs.py -n 5000
```

## Pattern Reference

For comprehensive list of log patterns and search strategies, see [log_patterns.md](references/log_patterns.md).

Key pattern categories:

- Error patterns (`[ERROR]`, `Failed to`, `panic`)
- Component logs (`agent_`, `MCPServiceProxy`, `BrowserServer`)
- Workflow phases (`Think phase`, `Act phase`, `Observe phase`)
- Tool operations (`call_tool`, `list_tools`)
- Performance indicators (`Duration:`, `elapsed`)

## Debugging Workflows

### 1. Investigate Error

```bash
# Extract errors
python scripts/extract_logs.py --pattern "[ERROR]" --context 10 -o errors.txt

# Review errors.txt for:
# - Error message and stack trace
# - Preceding operations (context lines above)
# - Affected component (agent, MCP, builtin server)
# - Session ID for tracking
```

### 2. Analyze Agent Workflow

```bash
# Extract workflow logs
python scripts/extract_logs.py --pattern "agent_" -n 5000 -o workflow.txt

# Review workflow.txt for:
# - Session lifecycle (create, start, stop)
# - Workflow phases (Think, Act, Observe)
# - Tool execution sequences
# - Loop iterations and completion
```

### 3. Debug Tool Execution

```bash
# Extract tool logs
python scripts/extract_logs.py --pattern "call_tool" --context 10 -o tools.txt

# Review tools.txt for:
# - Tool name and arguments
# - Routing (builtin vs external)
# - Execution results or errors
# - Response structure
```

### 4. Track Session Activity

```bash
# Extract specific session logs (replace <session-id> with actual ID)
python scripts/extract_logs.py --pattern "<session-id>" --context 5 -o session.txt

# Review session.txt for:
# - Session initialization
# - Tool calls made during session
# - Workflow status changes
# - Errors specific to session
```

## Output Format

### Pattern Match Output

When using `--pattern`, output includes:

- Match count and line ranges
- Line numbers with markers (`>` for matching lines)
- Context lines before and after matches
- Merged ranges for adjacent matches

Example:

```
=== Match 1: Lines 1234-1244 ===
  1234   [DEBUG] Starting operation
  1235 > [ERROR] Failed to execute tool
  1236   Stack trace: ...
  1237   at module.rs:123
```

### Full Line Output

Without `--pattern`, outputs raw log lines preserving original format.

## Tips

- Use wider context (10-20 lines) for workflow analysis
- Use narrower context (3-5 lines) for quick error checks
- Combine `-n` with `--pattern` to search recent logs only
- Check [log_patterns.md](references/log_patterns.md) for component-specific patterns
- For performance issues, search for "Duration:" or "elapsed" patterns
