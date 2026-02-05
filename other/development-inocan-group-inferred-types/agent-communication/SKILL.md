---
name: agent-communication
description: Use when user explicitly requests to coordinate with other Claude Code agents, join an agent chat, or communicate across multiple repositories/projects
---

# Multi-Agent Communication

## Overview

Enable multiple Claude Code instances to communicate and coordinate work across different repositories using a lightweight socket-based chat system.

## When to Use

Use this skill when:
- User explicitly asks to "coordinate with other agents"
- User wants to "join agent chat" or "communicate with other Claude instances"
- User mentions working across multiple repositories that need coordination
- User asks to "broadcast a message to other agents"

## When NOT to Use

Do NOT use this skill for:
- Single-repository work
- Communication with external services/APIs
- User asking about other forms of collaboration (git, PRs, etc.)

## Components

Two components work together:

1. **agent.py** - Your agent daemon (one per Claude instance, runs in background)
2. **chat.py** - CLI for interaction (runs in foreground, synchronous)

When new messages arrive from other agents, you will be automatically notified by the plugin. You don't need to monitor any files or poll for messages - the system handles this automatically.

## Script Path Construction

**IMPORTANT**: Always use full paths to call scripts. Do NOT use `cd` to change to the scripts directory.

The skill is located at: **Base directory for this skill** (shown at the top when skill loads)

To call scripts, concatenate:
- **Skill base directory** + `/scripts/` + **script name**

Example:
```bash
# If skill base is: /home/agus/workspace/asermax/claude-plugins/superpowers/skills/agent-communication
# Then agent.py is at:
/home/agus/workspace/asermax/claude-plugins/superpowers/skills/agent-communication/scripts/agent.py
```

In the examples below, we use `scripts/agent.py` as shorthand, but you should replace `scripts/` with the full path to the scripts directory based on the skill's base directory.

## Background Execution Requirements

**CRITICAL**: `agent.py` automatically runs in the background via plugin hook.

`chat.py` typically runs in foreground, but **receive** should run in background using `run_in_background: true` to allow continuous message listening while doing other work.

## The Process

### Step 1: Generate Agent Identity

Before joining, generate your identity based on context:

**Name**: Derive from your role and working directory
- Examples: "backend-agent", "frontend-agent", "docs-agent", "scheduler-api-agent"
- Pattern: `{role}-agent` or `{project}-agent`

**Context**: Your working directory or project
- Use `pwd` to get current directory
- Or derive from CLAUDE.md or git remote
- Examples: "filadd/scheduler-api", "myproject/docs", "/home/user/repos/backend"

**Presentation**: Brief description of what you manage
- 1-2 sentences
- What code/project you're working on
- Current focus or task
- Example: "I manage the backend API for the scheduler service. Currently implementing the new scheduling endpoint for recurring tasks."

### Step 2: Start Your Agent

Start the agent daemon:

```bash
scripts/agent.py --name "your-agent-name" \
                 --context "your/project/path" \
                 --presentation "Your description..."
```

**Note**: The agent automatically detects your working directory from where the command is run. If you need to override the location, you can use `--cwd /path/to/directory`.

**On success:**
- Agent daemon runs in background
- You'll see: "Joined chat. N member(s) present."
- Agent name is displayed

### Step 3: Interact via chat.py

Now you can use the foreground CLI to interact:

**Send a message to all agents:**
```bash
scripts/chat.py --agent your-agent-name send "Hello! I'm working on the authentication module."
```

Output on success (all agents reachable):
```json
{
  "status": "ok",
  "message": "Message sent",
  "delivered_to": ["backend-agent", "frontend-agent"]
}
```

Output with unreachable agents:
```json
{
  "status": "ok",
  "message": "Message sent",
  "delivered_to": ["backend-agent"],
  "warnings": {
    "frontend-agent": "Connection refused"
  }
}
```

**Receive messages from other agents:**
```bash
# Waits indefinitely for messages (for background use with run_in_background: true)
scripts/chat.py --agent your-agent-name receive
```

Output if messages available:
```json
{
  "status": "ok",
  "messages": [
    {
      "id": "backend-agent-2025-11-29T12:00:00Z",
      "timestamp": "2025-11-29T12:00:00Z",
      "type": "message",
      "sender": {
        "name": "backend-agent",
        "context": "filadd/scheduler-api",
        "presentation": "I manage the backend..."
      },
      "content": "I just updated the API schema, heads up!"
    }
  ]
}
```

**Wait for message notifications:**
```bash
# Waits indefinitely until a message arrives, then returns count without consuming
scripts/chat.py --agent your-agent-name notify
```

Output when message(s) arrive:
```json
{"status": "ok", "count": 2}
```

This is useful for background monitoring - notify returns when messages arrive, then use `receive` to actually get them.

**Send a message and wait for response:**
```bash
scripts/chat.py --agent your-agent-name ask "What's the API format?"
```

Output if responses received:
```json
{
  "status": "ok",
  "messages": [
    {
      "id": "other-agent-2025-11-29T12:00:00Z",
      "timestamp": "2025-11-29T12:00:00Z",
      "type": "message",
      "sender": {
        "name": "other-agent",
        "context": "project/backend"
      },
      "content": "The API format is JSON with these fields..."
    }
  ]
}
```

**Check who's connected:**
```bash
scripts/chat.py --agent your-agent-name status
```

Output:
```json
{
  "status": "ok",
  "data": {
    "agent": {
      "name": "frontend-agent",
      "context": "filadd/web-ui"
    },
    "members": {
      "backend-agent": {
        "name": "backend-agent",
        "context": "filadd/scheduler-api",
        "presentation": "I manage the backend API...",
        "joined_at": "2025-11-29T12:00:00Z"
      },
      ...
    },
    "queue_size": 2
  }
}
```

### Step 4: Communication Pattern

**IMPORTANT**: Use conversational back-and-forth communication. Always use the `ask` command to send a message and wait for response. Continue the conversation until both agents agree it's complete.

**The Pattern:**
1. **Initiate with ask** - Use `scripts/chat.py --agent X ask "message"`
2. **Wait for response** - The ask command automatically waits
3. **Respond with ask** - When you receive a message, respond using ask (not just send)
4. **Continue until done** - Keep the conversation going until both agents agree to end
5. **Explicit completion** - End with something like "Thanks, conversation complete!" or "Got it, all done!"

**Why ask instead of send?**
- Ensures fluid back-and-forth conversation
- You see responses immediately
- Prevents messages getting lost or ignored
- Creates natural request-response flow

**When to use send:**
- Broadcasting announcements to all agents (no response needed)
- Fire-and-forget notifications

**Example conversational workflow:**

```bash
# Agent A initiates
scripts/chat.py --agent backend-agent ask "I've updated the /api/schedule endpoint. Can you review the new schema?"

# Receives response from frontend-agent, then continues conversation
scripts/chat.py --agent backend-agent ask "The date field is ISO8601 format. Does that work for your UI components?"

# Receives confirmation, closes conversation
scripts/chat.py --agent backend-agent ask "Perfect! Integration looks good. All done on my end."

# Other agent confirms completion, conversation ends
```

**Bad pattern (don't do this):**
```bash
# Sends message but doesn't wait - other agent might not see it
scripts/chat.py --agent backend-agent send "Updated the API"

# Meanwhile continues working, misses response
vim other-file.ts
```

**Alternative: Background notify loop**

For long-running work where you want to stay responsive but not block on responses, use background notify (see "Background Notify Pattern" below).

### Background Notify Pattern

**Recommended workflow**: Keep a background notify running at all times to stay responsive.

1. **Start background notify** after joining:
   ```bash
   scripts/chat.py --agent your-name notify
   ```
   (use with `run_in_background: true`)

2. **Continue with other work** - the notify runs in background, waiting for messages

3. **Detect completion with TaskOutput** - Use the TaskOutput tool to detect when the notify task completes (indicating messages have arrived):
   ```bash
   # When notify task completes, TaskOutput will return the result
   ```
   Do not try to read the task output file directly - use the TaskOutput tool

4. **Read messages**:
   ```bash
   scripts/chat.py --agent your-name receive
   ```

5. **Process and respond** - Handle messages, send responses

6. **Restart notify loop** - Start background notify again to wait for next message

**When to use background notify:**
- Working on time-consuming tasks (coding, testing, debugging)
- Want to stay responsive to other agents without blocking
- Coordinating across repos where responses may come anytime

**When to use `ask` instead:**
- Active conversation with quick back-and-forth
- Waiting for a specific response you need immediately

## Message Types You'll See

### Join Messages

When a new agent joins:

```json
{
  "id": "docs-agent-2025-11-29T12:00:00Z",
  "timestamp": "2025-11-29T12:00:00Z",
  "type": "join",
  "sender": {
    "name": "docs-agent",
    "context": "project/docs",
    "presentation": "I manage the documentation..."
  },
  "content": "I manage the documentation..."
}
```

**What to do**: Welcome the new agent, share context if relevant

### Leave Messages

When an agent leaves:

```json
{
  "id": "backend-agent-2025-11-29T12:00:00Z",
  "timestamp": "2025-11-29T12:00:00Z",
  "type": "leave",
  "sender": {
    "name": "backend-agent",
    "context": "filadd/scheduler-api",
    "presentation": "I manage the backend API..."
  },
  "content": ""
}
```

**What to do**: Note that agent is no longer available

### Regular Messages

Broadcast messages from other agents:

```json
{
  "id": "backend-agent-2025-11-29T12:05:00Z",
  "timestamp": "2025-11-29T12:05:00Z",
  "type": "message",
  "sender": {
    "name": "backend-agent",
    "context": "filadd/scheduler-api",
    "presentation": "I manage the backend API..."
  },
  "content": "Just pushed changes to the auth module"
}
```

**What to do**: Process content, respond if relevant

## Error Handling

### Agent Name Already In Use

**Error**: Agent fails with "Agent name already in use"

**Solution**: Choose a different agent name or check if there's a stale agent process

### Agent Not Running

**Error**: chat.py fails with "No agent running"

**Solution**: Start your agent first (see Step 2)

### File Permissions

If you encounter file permission errors, check that your user has access to the runtime directory

## Practical Example

**Scenario**: Coordinating backend and frontend work

**Backend agent (you)**:
```bash
# Join chat
scripts/agent.py --name "backend-agent" \
                 --context "filadd/scheduler-api" \
                 --presentation "I manage the backend API. Working on new scheduling endpoint."

# Do work
vim src/routes/schedule.ts

# Initiate conversation with ask
scripts/chat.py --agent backend-agent ask "New /api/schedule endpoint ready. Schema: {date, recurrence, callback_url}. Can you review?"
# Receives frontend's question about recurrence format

# Continue conversation
scripts/chat.py --agent backend-agent ask "Recurrence format: {type: 'daily'|'weekly'|'monthly', interval: number}. Example: {type: 'weekly', interval: 2} for every 2 weeks. Does this work for your UI?"
# Receives confirmation

# Close conversation
scripts/chat.py --agent backend-agent ask "Great! Let me know if you need any changes after testing."
# Receives "All good, thanks!" - conversation complete
```

**Frontend agent (other Claude instance)** - responds to each ask:
```bash
# Join chat
scripts/agent.py --name "frontend-agent" \
                 --context "filadd/web-ui" \
                 --presentation "I manage the web UI. Working on schedule creation form."

# Wait for backend's message
scripts/chat.py --agent frontend-agent receive
# Sees backend's ask about reviewing endpoint

# Respond with ask
scripts/chat.py --agent frontend-agent ask "What's the format for recurrence? Daily/weekly/monthly?"
# Receives format details

# Continue conversation
scripts/chat.py --agent frontend-agent ask "Perfect! That format works great for my dropdown. Starting implementation now."
# Receives backend's offer to help

# Close conversation
scripts/chat.py --agent frontend-agent ask "All good, thanks!"
# Conversation complete
```

## Agent Lifecycle

### Leaving the Chat

**Recommended**: Use the `leave` command to exit gracefully.

```bash
scripts/chat.py --agent your-agent-name leave
```

This command will:
1. Broadcast a leave message to all other agents
2. Remove the agent from the registry
3. Clean up the socket file
4. Shut down the agent daemon cleanly

Output on success:
```json
{"status": "ok", "message": "Left chat successfully"}
```

### Stopping an Agent Manually (Fallback)

If the `leave` command doesn't work or the agent is stuck, you can manually stop it using SIGTERM.

**IMPORTANT**: Only use this as a fallback. Always try the `leave` command first.

**Manual stop procedure:**
```bash
# 1. Find running agents
ps aux | grep 'agent.py' | grep -v grep

# 2. Kill by pattern (replace with actual agent name) - use SIGTERM, not SIGKILL
pkill -TERM -f 'agent.py --name "agent-name"'

# 3. Wait a moment for cleanup
sleep 1

# 4. Verify stopped
ps aux | grep 'agent.py --name "agent-name"' | grep -v grep
# (no output = successfully stopped)
```

**How to check if agents are running:**
```bash
# List all agent processes
ps aux | grep 'agent.py' | grep -v grep

# Check specific agent
ps aux | grep 'agent.py --name "your-agent-name"' | grep -v grep
```

## Tips

1. **Background notify loop**: After joining, start a background notify to stay responsive:
   - Use `run_in_background: true` on the Bash tool
   - Use TaskOutput tool to detect when notify task completes
   - When notify completes, read messages with `receive`
   - Process, respond, restart background notify
2. **Use ask for conversations**: Always use `ask` instead of `send` when you expect a response. This creates natural back-and-forth flow.
3. **Explicit completion**: End conversations clearly with phrases like "All done!", "Thanks, conversation complete!", or "Got it, closing this thread."
4. **Agent naming**: Use descriptive names that indicate role/project
5. **Presentations**: Be specific about what you manage and current focus
6. **Don't interrupt flow**: When using `ask`, don't do other work while waiting - focus on the conversation
7. **Document decisions**: Important decisions should also go in code/docs, not just chat
8. **Messages are memory-only**: Messages are stored in memory and will be lost if an agent restarts. This is by design for simplicity and performance.

## Human CLI Tool

For humans who want to join the agent chat interactively, use `human-cli.py`:

### Usage

```bash
scripts/human-cli.py [--name NAME] [--context CONTEXT] [--presentation TEXT]
```

### Options

- `--name`: Agent name (default: `human-{username}`)
- `--context`: Your context/project (default: `human-terminal`)
- `--presentation`: Brief description of yourself (default: `Human operator joining the chat`)

### Interactive Commands

Once in the REPL:

- `/help` - Show available commands
- `/status` - Show agent status and queue size
- `/members` - List all connected agents with their contexts
- `/quit` or `/exit` - Exit the chat gracefully

Anything else you type will be sent as a message to all agents.

### Features

- **Real-time messages**: Messages from agents appear immediately, interrupting the prompt
- **Colored output**: Different colors for joins, leaves, and messages (when terminal supports it)
- **Embedded daemon**: Automatically starts and stops the agent daemon for you
- **Full participation**: You join as a real agent, can send and receive just like Claude agents

### Example Session

```bash
# Start the human CLI
scripts/human-cli.py --name human-alice --context "myproject/docs"

# You'll see:
# Starting agent daemon...
# Connected as: human-alice
# Context: myproject/docs
# Type /help for commands
#
# >

# Check who's connected
/members

# Send a message
Hello agents! I'm here to help coordinate.

# Messages from agents will appear automatically:
# [15:30:45] backend-agent: Hi Alice! We're working on the API refactor.

# Exit when done
/quit
```

## Quick Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `scripts/agent.py --name X --context Y --presentation Z` | Start your agent | Background process |
| `scripts/chat.py --agent X send "msg"` | Broadcast message | JSON status |
| `scripts/chat.py --agent X receive` | Wait for and consume messages | JSON array |
| `scripts/chat.py --agent X notify` | Wait for message notification (doesn't consume) | JSON count |
| `scripts/chat.py --agent X ask "question"` | Send and wait for response | JSON array |
| `scripts/chat.py --agent X status` | Show members and state | JSON status |
| `scripts/chat.py --agent X leave` | Leave chat gracefully | JSON status |

Remember: Replace `scripts/` with the full path based on the skill's base directory (see "Script Path Construction" section above).

