---
name: erlang-message-sync
description: Erlang-style message passing via /tmp file system. Use when simulating actor model with actual message synchronization between processes. Provides send/receive primitives with blocking and pattern matching.
allowed-tools: Bash, Read, Write
---

# Erlang Message Synchronization

Provides Erlang-style message passing primitives using `/tmp` file system as a message transport layer.

## Overview

This skill enables true message-passing semantics between simulated Erlang processes:
- **Asynchronous send**: Non-blocking message delivery
- **Blocking receive**: Waits until matching message arrives
- **Pattern matching**: Filter messages by sender
- **Timeout support**: Prevent infinite blocking
- **Message persistence**: Uses filesystem for reliable delivery

## Message Format

Messages are stored as JSON files in `/tmp/erlang-messages/<to-pid>/`:

```
/tmp/erlang-messages/
├── main/
│   ├── worker_1-1704067200000000000.json
│   └── worker_2-1704067201000000000.json
├── worker_1/
│   └── main-1704067199000000000.json
└── coordinator/
    ├── worker_1-1704067202000000000.json
    └── worker_2-1704067203000000000.json
```

## Quick Start

### Sending a Message

Send a message from one process to another (non-blocking):

```bash
# Get the plugin installation path
PLUGIN_PATH="$HOME/.claude/plugins/marketplaces/kokuyouwind-plugins/plugins/code-like-prompt"

# Send message: main -> worker_1
bash "${PLUGIN_PATH}/skills/erlang-message-sync/scripts/send-message.sh" \
    main \
    worker_1 \
    '{"type":"request","from":"main","data":"hello"}'
```

**Output:**
```
Message sent from main to worker_1
Message file: /tmp/erlang-messages/worker_1/main-1704067200000000000.json
Message content: {"type":"request","from":"main","data":"hello"}
```

### Receiving a Message

Receive a message (blocking until message arrives or timeout):

```bash
# Receive any message for worker_1 (30s timeout default)
MESSAGE=$(bash "${PLUGIN_PATH}/skills/erlang-message-sync/scripts/receive-message.sh" worker_1)
echo "Received: ${MESSAGE}"

# Receive only from 'main' with 5s timeout
MESSAGE=$(bash "${PLUGIN_PATH}/skills/erlang-message-sync/scripts/receive-message.sh" \
    worker_1 \
    main \
    5)
```

**Output:**
```
Waiting for message to worker_1 from main (timeout: 5s)...
Received message at worker_1 from main
Message content: {"type":"request","from":"main","data":"hello"}
{"type":"request","from":"main","data":"hello"}
```

## Script Reference

### send-message.sh

**Syntax:**
```bash
send-message.sh <from-pid> <to-pid> <message-json>
```

**Arguments:**
- `from-pid`: Sender's process identifier
- `to-pid`: Recipient's process identifier
- `message-json`: Message content as JSON string

**Behavior:**
- Creates mailbox directory `/tmp/erlang-messages/<to-pid>` if needed
- Writes message to `<to-pid>/<from-pid>-<timestamp>.json`
- Returns immediately (non-blocking)

**Example:**
```bash
bash send-message.sh coordinator worker_1 '{"task":"process","value":42}'
```

### receive-message.sh

**Syntax:**
```bash
receive-message.sh <pid> [from-pid-pattern] [timeout-seconds]
```

**Arguments:**
- `pid`: Receiving process identifier
- `from-pid-pattern` (optional): Filter by sender (glob pattern, default: `*`)
- `timeout-seconds` (optional): Maximum wait time (default: 30)

**Behavior:**
- Polls `/tmp/erlang-messages/<pid>/` every 100ms
- Blocks until matching message found or timeout
- Consumes (deletes) the message file after reading
- Returns message content to stdout
- Exits with code 1 on timeout

**Examples:**
```bash
# Receive any message
MESSAGE=$(bash receive-message.sh main)

# Receive only from worker_1
MESSAGE=$(bash receive-message.sh coordinator worker_1)

# Receive from worker_1 with 10s timeout
MESSAGE=$(bash receive-message.sh coordinator worker_1 10)
```

## Usage Patterns

### Request-Response Pattern

```bash
# Sender (main process)
bash send-message.sh main worker_1 '{"type":"request","data":"compute"}'
RESPONSE=$(bash receive-message.sh main worker_1 10)
echo "Got response: ${RESPONSE}"

# Receiver (worker_1 process)
REQUEST=$(bash receive-message.sh worker_1 main)
# ... process request ...
bash send-message.sh worker_1 main '{"type":"response","result":"done"}'
```

### Multi-Process Coordination

```bash
# Main spawns two workers
bash send-message.sh main worker_1 '{"task":"A"}' &
bash send-message.sh main worker_2 '{"task":"B"}' &

# Workers send results to coordinator
# (In worker_1)
RESULT_1=$(bash receive-message.sh worker_1 main)
bash send-message.sh worker_1 coordinator '{"result":"A_done"}'

# (In worker_2)
RESULT_2=$(bash receive-message.sh worker_2 main)
bash send-message.sh worker_2 coordinator '{"result":"B_done"}'

# Coordinator collects both results
RESULT_A=$(bash receive-message.sh coordinator worker_1)
RESULT_B=$(bash receive-message.sh coordinator worker_2)
bash send-message.sh coordinator main '{"combined":"A_done,B_done"}'
```

### Selective Receive (Pattern Matching)

```bash
# Receive only 'done' messages from any worker
MESSAGE=$(bash receive-message.sh coordinator "worker_*")

# Receive specifically from worker_1
MESSAGE=$(bash receive-message.sh coordinator worker_1)
```

## Important Notes

### Message Ordering
- Messages from the same sender arrive in send order
- Messages from different senders may be received in any order
- Use timestamps in filenames to maintain chronological order

### Cleanup
Messages are automatically deleted when received. To manually clean up:

```bash
rm -rf /tmp/erlang-messages
```

### Error Handling
- Send never fails (fire-and-forget semantics)
- Receive fails with exit code 1 on timeout
- Check exit codes when receiving:

```bash
if MESSAGE=$(bash receive-message.sh main worker_1 5); then
    echo "Received: ${MESSAGE}"
else
    echo "Timeout or error"
fi
```

### Plugin Path Resolution

The scripts are located at:
```
$HOME/.claude/plugins/marketplaces/kokuyouwind-plugins/plugins/code-like-prompt/skills/erlang-message-sync/scripts/
```

When using in commands, always resolve the full path or set a variable:

```bash
SKILL_DIR="$HOME/.claude/plugins/marketplaces/kokuyouwind-plugins/plugins/code-like-prompt/skills/erlang-message-sync"

bash "${SKILL_DIR}/scripts/send-message.sh" main worker_1 '{"msg":"hi"}'
bash "${SKILL_DIR}/scripts/receive-message.sh" worker_1
```

## Limitations

- **Not true concurrency**: Scripts run sequentially unless backgrounded with `&`
- **Filesystem overhead**: Slower than in-memory message passing
- **No mailbox introspection**: Can't check mailbox size without listing directory
- **No message priority**: FIFO order within sender
- **Timeout granularity**: 100ms polling interval

## When to Use This Skill

Use this skill when:
- Testing Erlang-style actor model commands (08-series)
- Need actual blocking receive semantics
- Want to verify message ordering behavior
- Simulating multi-process coordination with real synchronization

**Do not use** when:
- Simple textual simulation is sufficient
- Performance is critical
- Running in sandboxed environment without /tmp access
