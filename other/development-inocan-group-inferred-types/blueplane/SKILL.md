---
name: blueplane
description: Manage Blueplane telemetry server using server_ctl.py for starting, stopping, restarting, viewing logs, and checking system status. Essential for development workflow and debugging.
---

# Blueplane Server Management

## Overview

The Blueplane telemetry processing server is controlled via `scripts/server_ctl.py`. This skill covers all server lifecycle operations, log monitoring, and status checking.

## Quick Reference

```bash
# Start/Stop/Restart
python scripts/server_ctl.py start              # Start in foreground
python scripts/server_ctl.py start --daemon     # Start in background (daemon)
python scripts/server_ctl.py stop               # Graceful shutdown
python scripts/server_ctl.py stop --force       # Force kill
python scripts/server_ctl.py restart            # Stop then start
python scripts/server_ctl.py restart --daemon   # Restart as daemon

# Status & Monitoring
python scripts/server_ctl.py status             # Check if running
python scripts/server_ctl.py status --verbose   # Detailed status

# View Logs
tail -f ~/.blueplane/server.log                 # Live log monitoring
tail -n 100 ~/.blueplane/server.log             # Last 100 lines
```

## Commands

### `start` - Start Server

Starts the Blueplane telemetry processing server.

**Usage:**
```bash
python scripts/server_ctl.py start [--daemon] [--verbose]
```

**Options:**
- `--daemon, -d`: Run server in background (daemon mode)
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
# Start in foreground (good for debugging)
python scripts/server_ctl.py start

# Start as daemon (good for production)
python scripts/server_ctl.py start --daemon
python scripts/server_ctl.py start -d

# Start with verbose output
python scripts/server_ctl.py start -d -v
```

**When to Use:**
- **Foreground**: When debugging, testing, or need immediate feedback
- **Daemon**: For long-running operation, production, or background processing

### `stop` - Stop Server

Gracefully stops the running server with optional force kill.

**Usage:**
```bash
python scripts/server_ctl.py stop [--force] [--timeout TIMEOUT] [--verbose]
```

**Options:**
- `--force, -f`: Force kill if graceful shutdown fails
- `--timeout TIMEOUT, -t TIMEOUT`: Timeout in seconds (default: 30)
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
# Graceful shutdown (preferred)
python scripts/server_ctl.py stop

# Force kill if stuck
python scripts/server_ctl.py stop --force
python scripts/server_ctl.py stop -f

# Custom timeout
python scripts/server_ctl.py stop --timeout 60

# Verbose stop with force fallback
python scripts/server_ctl.py stop -v -f
```

**Shutdown Process:**
1. Sends SIGTERM (graceful shutdown signal)
2. Waits for timeout period (default 30s)
3. If `--force` specified and still running, sends SIGKILL
4. Cleans up PID file

### `restart` - Restart Server

Stops the server (if running) and starts it again.

**Usage:**
```bash
python scripts/server_ctl.py restart [--daemon] [--force] [--timeout TIMEOUT] [--verbose]
```

**Options:**
- Combines all options from `stop` and `start`
- `--daemon, -d`: Restart in daemon mode
- `--force, -f`: Force kill during stop if needed
- `--timeout TIMEOUT, -t TIMEOUT`: Stop timeout in seconds
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
# Restart in foreground
python scripts/server_ctl.py restart

# Restart as daemon (most common)
python scripts/server_ctl.py restart --daemon
python scripts/server_ctl.py restart -d

# Force restart with custom timeout
python scripts/server_ctl.py restart -d -f -t 60

# Verbose restart
python scripts/server_ctl.py restart -d -v
```

**When to Restart:**
- After code changes
- After configuration updates
- After Redis schema changes
- When server is unresponsive but `stop` alone won't work

### `status` - Check Server Status

Check if the server is running and get health information.

**Usage:**
```bash
python scripts/server_ctl.py status [--verbose]
```

**Options:**
- `--verbose, -v`: Show detailed status information

**Examples:**
```bash
# Basic status check
python scripts/server_ctl.py status

# Detailed status with health checks
python scripts/server_ctl.py status --verbose
python scripts/server_ctl.py status -v
```

**Output Includes:**
- Process status (running/stopped)
- PID information
- Server uptime
- **Verbose mode adds:**
  - Redis connection status
  - Database file status
  - Consumer group information
  - Recent activity metrics

## Log Management

### Log File Location

```bash
~/.blueplane/server.log
```

### Common Log Commands

```bash
# Watch logs in real-time (best for monitoring)
tail -f ~/.blueplane/server.log

# Last N lines
tail -n 50 ~/.blueplane/server.log      # Last 50 lines
tail -n 100 ~/.blueplane/server.log     # Last 100 lines

# Search logs
grep "ERROR" ~/.blueplane/server.log
grep "Claude Code" ~/.blueplane/server.log
grep -i "redis" ~/.blueplane/server.log  # Case insensitive

# Filter by component
grep "event_consumer" ~/.blueplane/server.log
grep "jsonl_monitor" ~/.blueplane/server.log
grep "database_monitor" ~/.blueplane/server.log

# View logs with timestamps
tail -f ~/.blueplane/server.log | grep "$(date +%Y-%m-%d)"

# Count errors
grep -c "ERROR" ~/.blueplane/server.log
grep -c "WARNING" ~/.blueplane/server.log
```

### Log Levels

Logs use Python logging levels:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical failures

### Background Log Monitoring

```bash
# Run tail in background and monitor periodically
tail -f ~/.blueplane/server.log &

# Kill background tail
pkill -f "tail -f.*server.log"
```

## System Health Checks

### Check Redis Streams

```bash
# Check stream lengths
redis-cli XLEN telemetry:message_queue
redis-cli XLEN telemetry:message_queue
redis-cli XLEN cdc:events

# Check consumer groups
redis-cli XINFO GROUPS telemetry:message_queue
redis-cli XINFO GROUPS cdc:events

# Check pending messages
redis-cli XPENDING telemetry:message_queue processors
```

### Check Database

```bash
# Check database file
ls -lh ~/.blueplane/telemetry.db

# SQLite query examples
sqlite3 ~/.blueplane/telemetry.db "SELECT COUNT(*) FROM claude_raw_traces;"
sqlite3 ~/.blueplane/telemetry.db "SELECT COUNT(*) FROM cursor_raw_traces;"
```

### Check Process

```bash
# Check if process is running
ps aux | grep server.py

# Check PID file
cat ~/.blueplane/server.pid

# Check resource usage
ps aux | grep server.py | awk '{print $3, $4, $11}'  # CPU, MEM, COMMAND
```

## Typical Workflows

### Development Workflow

```bash
# 1. Make code changes
# 2. Restart server to pick up changes
python scripts/server_ctl.py restart --daemon

# 3. Monitor logs for issues
tail -f ~/.blueplane/server.log

# 4. Check status
python scripts/server_ctl.py status --verbose
```

### Debugging Issues

```bash
# 1. Check if server is running
python scripts/server_ctl.py status -v

# 2. View recent logs
tail -n 200 ~/.blueplane/server.log | grep -i error

# 3. Stop server
python scripts/server_ctl.py stop

# 4. Clear any stale state (optional)
rm ~/.blueplane/server.pid

# 5. Start in foreground to see live output
python scripts/server_ctl.py start

# 6. Once working, restart as daemon
python scripts/server_ctl.py restart -d
```

### Production Deployment

```bash
# 1. Stop existing server gracefully
python scripts/server_ctl.py stop --timeout 60

# 2. Verify stopped
python scripts/server_ctl.py status

# 3. Start as daemon
python scripts/server_ctl.py start --daemon

# 4. Verify running
python scripts/server_ctl.py status --verbose

# 5. Monitor logs briefly
tail -n 50 ~/.blueplane/server.log
```

### After Configuration Changes

```bash
# Changes to config files in ~/.blueplane/ or config/
python scripts/server_ctl.py restart --daemon

# Monitor to ensure clean restart
tail -f ~/.blueplane/server.log
# Look for "Server started successfully" message
```

## Important Files & Directories

```
~/.blueplane/
├── server.log          # Main log file
├── server.pid          # PID file (JSON format with metadata)
├── telemetry.db        # SQLite database
├── config.yaml         # Configuration (if present)
└── workspace_cache.db  # Workspace mappings cache

scripts/
├── server_ctl.py       # Server control CLI (this skill)
└── start_server.py     # Actual server implementation
```

## Troubleshooting

### Server Won't Start

```bash
# Check if already running
python scripts/server_ctl.py status

# Check for stale PID file
cat ~/.blueplane/server.pid
ps aux | grep $(cat ~/.blueplane/server.pid | jq -r .pid)

# Force cleanup
python scripts/server_ctl.py stop --force
rm ~/.blueplane/server.pid

# Try starting again
python scripts/server_ctl.py start
```

### Server Won't Stop

```bash
# Try force stop
python scripts/server_ctl.py stop --force

# If still stuck, manual kill
kill -9 $(cat ~/.blueplane/server.pid | jq -r .pid)
rm ~/.blueplane/server.pid
```

### Server Running But Not Processing

```bash
# Check status with verbose
python scripts/server_ctl.py status --verbose

# Check Redis connection
redis-cli PING

# Check consumer groups
redis-cli XINFO GROUPS telemetry:message_queue

# Restart server
python scripts/server_ctl.py restart --daemon
```

### High CPU/Memory Usage

```bash
# Check resource usage
ps aux | grep server.py

# Check stream lengths (may be backlog)
redis-cli XLEN telemetry:message_queue
redis-cli XLEN cdc:events

# Check logs for errors
grep -i "error\|warning" ~/.blueplane/server.log | tail -50

# Consider restarting
python scripts/server_ctl.py restart --daemon
```

## Best Practices

1. **Always use daemon mode for long-running operation**
   ```bash
   python scripts/server_ctl.py restart --daemon
   ```

2. **Use foreground mode when debugging**
   ```bash
   python scripts/server_ctl.py start  # No --daemon
   ```

3. **Check status after restart**
   ```bash
   python scripts/server_ctl.py restart -d && sleep 2 && python scripts/server_ctl.py status -v
   ```

4. **Monitor logs after changes**
   ```bash
   python scripts/server_ctl.py restart -d && tail -f ~/.blueplane/server.log
   ```

5. **Graceful shutdown preferred over force**
   ```bash
   # Good
   python scripts/server_ctl.py stop

   # Only if stuck
   python scripts/server_ctl.py stop --force
   ```

6. **Use verbose mode for detailed debugging**
   ```bash
   python scripts/server_ctl.py status --verbose
   ```

## Integration with Development

### Git Workflow

After pulling changes:
```bash
git pull
python scripts/server_ctl.py restart --daemon
tail -f ~/.blueplane/server.log
```

### Testing Changes

```bash
# Stop server
python scripts/server_ctl.py stop

# Run tests
pytest tests/

# Restart server
python scripts/server_ctl.py start --daemon
```

### Pre-commit

Before committing changes that affect the server:
```bash
# Restart to verify changes work
python scripts/server_ctl.py restart --daemon

# Check logs for errors
tail -n 100 ~/.blueplane/server.log | grep -i error

# Commit if clean
git add . && git commit
```

## Database Overview

Blueplane uses a hybrid storage approach with SQLite for persistent storage and Redis for message queuing and real-time metrics.

### Storage Architecture

```
~/.blueplane/
├── telemetry.db        # SQLite database (primary storage)
├── server.log          # Server logs
├── server.pid          # Process ID file
└── config.yaml         # User configuration (optional)
```

### SQLite Database Schema

The SQLite database (`~/.blueplane/telemetry.db`) contains the following main tables:

#### 1. `claude_raw_traces` - Claude Code Events

Stores all events from Claude Code JSONL transcripts.

**Key Fields:**
- `sequence` - Auto-incrementing primary key
- `event_id` - Unique event identifier
- `external_id` - Claude session/conversation ID
- `event_type` - Type of event (message, tool_use, system_event, etc.)
- `platform` - Always 'claude_code'
- `timestamp` - Event timestamp
- `uuid` - Claude event UUID (for threading)
- `parent_uuid` - Parent event UUID (for threading)
- `workspace_hash` - Workspace identifier
- `project_name` - Human-readable project name
- `message_role` - user/assistant (for message events)
- `message_model` - Model used (e.g., claude-sonnet-4.5)
- `input_tokens`, `output_tokens` - Token usage
- `event_data` - Compressed full event (zlib)

#### 2. `cursor_raw_traces` - Cursor Events

Stores all events from Cursor database monitoring.

**Key Fields:**
- `sequence` - Auto-incrementing primary key
- `event_id` - Unique event identifier
- `external_session_id` - Cursor session ID
- `event_type` - Type of event
- `timestamp` - Event timestamp
- `workspace_hash` - Workspace identifier
- `database_table` - Source table in Cursor DB
- `generation_uuid` - AI generation identifier
- `composer_id` - Composer session identifier
- `bubble_id` - Chat bubble identifier
- `event_data` - Compressed full event (zlib)

#### 3. `conversations` - Unified Conversations Table

Tracks conversations across both platforms.

**Key Fields:**
- `id` - Internal conversation ID (UUID)
- `session_id` - NULL for Claude Code, references cursor_sessions.id for Cursor
- `external_id` - Platform-specific external ID
- `platform` - 'claude_code' or 'cursor'
- `workspace_hash` - Workspace identifier
- `workspace_name` - Human-readable workspace name
- `started_at` - Conversation start timestamp
- `ended_at` - Conversation end timestamp (NULL if active)
- `interaction_count` - Number of interactions
- `acceptance_rate` - Code acceptance rate
- `total_tokens` - Total tokens used
- `total_changes` - Total code changes

**Important Platform Differences:**
- **Claude Code**: `session_id` is always NULL (sessions = conversations)
- **Cursor**: `session_id` references a `cursor_sessions` entry

#### 4. `cursor_sessions` - Cursor IDE Sessions

Stores Cursor IDE window sessions (Cursor only, no Claude Code sessions).

**Key Fields:**
- `id` - Internal session ID (UUID)
- `external_session_id` - Session ID from Cursor extension
- `workspace_hash` - Workspace identifier
- `workspace_name` - Human-readable workspace name
- `workspace_path` - Full workspace path
- `started_at` - Session start timestamp
- `ended_at` - Session end timestamp (NULL if active)

### Redis Streams

Redis streams are used for message queuing and event processing:

- `telemetry:message_queue` - Main event stream (from capture → processing)
- `telemetry:message_queue` - Legacy stream name
- `cdc:events` - Change data capture events (database updates)

### Decompressing Event Data

The `event_data` field in raw trace tables is compressed with zlib. To decompress and view full event data:

```python
import sqlite3
import zlib
import json
from pathlib import Path

db_path = Path.home() / '.blueplane' / 'telemetry.db'
conn = sqlite3.connect(str(db_path))

# Get an event
cursor = conn.execute("""
    SELECT event_data FROM claude_raw_traces
    WHERE sequence = ?
""", (1,))

row = cursor.fetchone()
if row:
    compressed_data = row[0]
    decompressed = zlib.decompress(compressed_data)
    event = json.loads(decompressed)
    print(json.dumps(event, indent=2))
```

## See Also

- **Redis Streams**: Check stream health and consumer groups
- **Database Schema**: Check SQLite database for data integrity
- **Configuration**: `~/.blueplane/config.yaml` or `config/config.yaml`
- **Log Analysis**: Search and filter logs for specific issues
- **Session & Conversation Schema**: See `docs/SESSION_CONVERSATION_SCHEMA.md` for detailed schema design
