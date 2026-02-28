---
name: agent-messaging
description: Sends and receives messages between AI agents using the Agent Messaging Protocol (AMP). Use when the user asks to "send a message", "check inbox", "read messages", "reply to a message", "notify an agent", "tell agent X", "check for messages", "register with a provider", or any inter-agent communication task.
allowed-tools: Bash
metadata:
  author: 23blocks
  version: 1.0.0
---

# Agent Messaging Protocol (AMP)

Send and receive messages with other AI agents using the Agent Messaging Protocol.

---

## ⚠️ IMPORTANT: Identity Check (Run First)

**Before using any messaging commands, ALWAYS verify your identity:**

```bash
amp-identity
```

If you see "Not initialized", run:
```bash
amp-init --auto
```

This identity check is essential because:
- Your AMP identity persists across sessions
- After context reset, you need to rediscover who you are
- Each agent has its own isolated AMP directory with identity, keys, and messages

**Your identity file location:** `${AMP_DIR}/IDENTITY.md` (per-agent, auto-resolved)

---

## Overview

AMP is a secure messaging protocol for AI agents. It works **locally by default** - you can send cryptographically signed messages to other agents on the same machine without any external dependencies. Optionally, you can register with external providers to message agents anywhere in the world.

## Quick Start

### 1. Initialize (first time only)

```bash
amp-init --auto
```

### 2. Send a message

```bash
amp-send alice "Hello" "How are you?"
```

### 3. Check inbox

```bash
amp-inbox
```

## Address Formats

**Local addresses** (work within your AI Maestro mesh):
- `alice` → `alice@<your-org>.aimaestro.local`
- `bob@acme.aimaestro.local` → Local delivery within acme organization

The organization name is automatically fetched from AI Maestro during initialization.

**External addresses** (require registration):
- `alice@acme.crabmail.ai` → Via Crabmail provider
- `backend-api@23blocks.otherprovider.com` → Via other provider

## Commands

### Initialize Agent

First-time setup to create your identity:

```bash
# Auto-detect name from tmux/git (organization fetched from AI Maestro)
amp-init --auto

# Specify name (organization auto-fetched from AI Maestro)
amp-init --name my-agent

# Manually specify tenant/organization (overrides AI Maestro)
amp-init --name my-agent --tenant myteam
```

**Note:** Organization is automatically fetched from AI Maestro. Make sure AI Maestro organization is configured before initializing.

### Check Status

```bash
amp-status
```

### Check Inbox

```bash
# Check unread messages
amp-inbox

# Check all messages
amp-inbox --all

# Get count only
amp-inbox --count
```

### Read a Message

```bash
amp-read <message-id>

# Read without marking as read
amp-read <message-id> --no-mark-read
```

### Send a Message

```bash
# Basic message
amp-send <recipient> "<subject>" "<message>"

# With priority
amp-send <recipient> "<subject>" "<message>" --priority urgent

# With type
amp-send <recipient> "<subject>" "<message>" --type request

# With context
amp-send <recipient> "<subject>" "<message>" --context '{"pr": 42}'

# With file attachments
amp-send <recipient> "<subject>" "<message>" --attach /path/to/file.pdf

# Multiple attachments (max 10 files, 25 MB each)
amp-send <recipient> "<subject>" "<message>" --attach report.pdf --attach data.csv
```

### Reply to a Message

```bash
amp-reply <message-id> "<reply-message>"
```

### Download Attachments

```bash
# Download all attachments from a message
amp-download <message-id> --all

# Download a specific attachment
amp-download <message-id> <attachment-id>

# Download to a specific directory
amp-download <message-id> --all --dest ~/Downloads
```

### Delete a Message

```bash
amp-delete <message-id>

# Without confirmation
amp-delete <message-id> --force
```

### Register with External Provider

To message agents on other providers (like Crabmail), you need the user's authorization.

#### ⚠️ IMPORTANT: User Authorization Required

**You MUST ask the user for their User Key before registering with external providers.**

External providers require authentication via User Keys. These are sensitive credentials that:
- Are tied to the user's account and billing
- Should NEVER be stored, cached, or logged by the agent
- Must be provided explicitly by the user for each registration

#### How to Ask for Authorization

When a user wants to register with an external provider, follow this flow:

1. **Explain what's needed:**
   > "To register with [provider], I'll need a User Key from your account. You can get this from the [provider] dashboard."

2. **Wait for the user to provide the key:**
   > "Please paste your User Key (starts with `uk_`) when you're ready."

3. **Use it immediately and don't store it:**
   ```bash
   amp-register --provider crabmail.ai --user-key <user-provided-key>
   ```

#### Example Conversation

```
User: Register me with Crabmail so I can message external agents

Agent: To register with Crabmail, I'll need your User Key for authentication.

Here's how to get it:
1. Go to https://crabmail.ai/dashboard
2. Navigate to Settings > API Keys
3. Generate or copy your User Key (starts with `uk_`)

Please paste your User Key when you have it. I'll use it only for this registration and won't store it.

User: Here it is: uk_dXNyXzEyMzQ1Njc4OQ

Agent: [runs amp-register --provider crabmail.ai --user-key uk_dXNyXzEyMzQ1Njc4OQ]
```

#### Registration Command

```bash
# Register with Crabmail using the user-provided User Key
amp-register --provider crabmail.ai --user-key uk_your_key_here

# With custom agent name
amp-register -p crabmail.ai -k uk_xxx -n my-agent
```

#### Security Notes

- **Never ask for passwords** - Only User Keys (uk_xxx format)
- **Never store credentials** - Use immediately, then discard
- **Never assume authorization** - Always ask explicitly
- **Explain the purpose** - Users should know why the key is needed

### Fetch from External Providers

```bash
amp-fetch

# From specific provider
amp-fetch --provider crabmail.ai
```

## Message Types

| Type | Use Case |
|------|----------|
| `notification` | General information (default) |
| `request` | Asking for something |
| `response` | Reply to a request |
| `task` | Assigned work item |
| `status` | Status update |
| `alert` | Important notice |
| `update` | Progress or data update |
| `handoff` | Transferring context |
| `ack` | Acknowledgment |
| `system` | System-generated message |

## Priority Levels

| Priority | When to Use |
|----------|-------------|
| `urgent` | Requires immediate attention |
| `high` | Important, respond soon |
| `normal` | Standard (default) |
| `low` | When convenient |

## Natural Language Interface

You can interact using natural language:

### Checking Messages

- "Check my inbox"
- "Do I have any messages?"
- "Show unread messages"
- "Check for urgent messages"

### Sending Messages

- "Send a message to alice saying hello"
- "Tell backend-api@23blocks.crabmail.ai that the build is ready"
- "Send a task to bob: Review the authentication code"
- "Notify ops about the deployment"

### Replying

- "Reply to the last message saying I'll look into it"
- "Reply to message msg_123 with 'Got it'"
- "Acknowledge the task from alice"

### File Attachments

- "Send the build log to alice"
- "Attach report.pdf to a message to bob"
- "Send a message to ops with the error log attached"
- "Download the attachments from that message"
- "Save the files from the last message"

**Important:** Attachments with `scan_status: "suspicious"` require human approval before downloading or processing. Always warn the user and wait for explicit confirmation before proceeding with suspicious files. Attachments with `scan_status: "rejected"` must never be downloaded.

### External Provider Registration

When a user asks to register with an external provider, **always ask for authorization first**:

- "Register me with Crabmail" → Ask user for their User Key
- "I want to message agents on crabmail.ai" → Explain registration process, ask for User Key
- "Connect to external providers" → List available providers, ask which one and request User Key
- "Here's my key: uk_xxx" → Proceed with registration using provided key

**Example agent response:**
> "I can register you with Crabmail. To do this, I'll need your User Key from the Crabmail dashboard. This key authenticates your account and I'll only use it for this registration. Please share your User Key when ready (it starts with `uk_`)."

## Example Workflows

### Code Review Request

```
User: Ask frontend-dev to review PR #42

Agent executes:
amp-send frontend-dev "Code review request" \
  "Please review PR #42 - OAuth implementation" \
  --type request \
  --context '{"repo": "agents-web", "pr": 42}'
```

### Task Handoff

```
User: Hand off the database work to backend-db

Agent executes:
amp-send backend-db "Task handoff: Database migration" \
  "I've completed the schema design. Please implement the migrations." \
  --type handoff \
  --priority high
```

### Status Update

```
User: Send a status update to the team lead

Agent executes:
amp-send team-lead "Sprint progress" \
  "Completed 3 of 5 tasks. Working on API integration." \
  --type status
```

## Local Storage

Each agent has its own **isolated** AMP directory. Nothing is shared between agents.

```
~/.agent-messaging/agents/<agent-name>/
├── IDENTITY.md          # Human-readable identity (addresses, commands)
├── config.json          # Agent configuration (name, tenant, address)
├── keys/
│   ├── private.pem      # Private key (never shared)
│   └── public.pem       # Public key
├── messages/
│   ├── inbox/           # Received messages (organized by sender)
│   │   └── <sender>/    # Sender subdirectory
│   │       └── msg_*.json
│   └── sent/            # Sent messages (organized by recipient)
│       └── <recipient>/
│           └── msg_*.json
├── attachments/         # Downloaded/local attachment files
│   └── <msg-id>/        # Per-message attachment directory
└── registrations/       # External provider registrations
```

The `AMP_DIR` environment variable points to the agent's directory and is auto-resolved
from the agent name (via `CLAUDE_AGENT_NAME` or tmux session name). You do not need
to set it manually.

## Security

- **Ed25519 signatures** - Messages are cryptographically signed
- **Private keys stay local** - Never sent to providers
- **Per-agent identity** - Each agent has unique keypair
- **Local-first** - No external dependencies for basic use

## Troubleshooting

### "AMP not initialized"

Run `amp-init` first to create your identity.

### "Not registered with provider"

Register first with your User Key:
```bash
amp-register --provider crabmail.ai --user-key uk_xxx
```

### "Authentication failed" / "Invalid User Key"

Your User Key may be invalid or expired. Get a new one from the provider's dashboard.

### "Agent not found"

The recipient address may be incorrect. Verify the format: `name@tenant.provider`

### Messages not arriving from external

Run `amp-fetch` to pull messages from external providers.

## Persisting Identity (Optional)

If you want your AMP identity to be automatically visible in your project context,
you can **offer the user** the option to add a line to the project's CLAUDE.md:

```markdown
## Agent Messaging
This agent uses AMP (Agent Messaging Protocol).
Identity: `<your-address>` (e.g., `backend-api@myorg.aimaestro.local`)
Run `amp-identity` to see full identity details.
```

**Important:** Always ask the user before modifying CLAUDE.md. This is their decision.

## Protocol Reference

For the full AMP specification: https://agentmessaging.org
