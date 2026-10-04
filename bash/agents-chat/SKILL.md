---
name: agents-chat
description: >
    Test a Frontline agent end-to-end from the terminal using frontline agents chat
    (Overview/Playground channel). Use when the user wants to send a test message,
    open a test conversation, continue one, or close one. Distinct from Max chat
    and from reading conversation transcripts.
allowed-tools: Bash(frontline:*)
---

# Agent Test Chat

`frontline agents chat` talks to an agent the same way the in-app **Overview / Playground** does: it runs the agent and its active or draft flow. Use it to validate flows end-to-end after building or deploying.

> This is a **test channel**, not production LiveChat/WhatsApp traffic.

## Prerequisites

- Authenticate with `frontline auth login <api-key>`.
- Select an agent: `frontline agents use <agent-id>` (or pass `--agent-id` per command).
- The agent should have a flow with a Start node configured.

## Commands

### Open a new test conversation

```bash
frontline agents chat
```

Opens a conversation and runs the agent's Start flow (no user message).

### Send a message (new or continued)

```bash
# New conversation + first message
frontline agents chat --message "Hello"

# Continue an existing conversation
frontline agents chat --message "My name is Juan" --conversation-id 123
```

| Flag                     | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `--agent-id <id>`        | Agent ID (defaults to active agent)                           |
| `--message <text>`       | Message to send                                               |
| `--conversation-id <id>` | Continue an existing test conversation (requires `--message`) |
| `--contact-id <id>`      | Link the conversation to a People record                      |

### Close a test conversation

```bash
frontline agents chat close <conversationId>
```

## Output

Default (JSON, scripting-friendly):

```json
{
  "ok": true,
  "data": {
    "conversation_id": 123,
    "messages": [...]
  }
}
```

The CLI normalizes all success responses to `{ ok: true, data: … }`. Use `jq '.data.conversation_id'` and `jq '.data.messages'`.

With `--pretty`, stdout is human-readable: `conversation_id` plus the latest assistant message (no JSON envelope).

## vs other chat commands

| Command                                   | Purpose                                                          |
| ----------------------------------------- | ---------------------------------------------------------------- |
| `frontline agents chat`                   | **Test** an agent — runs active/draft flow (Playground)          |
| `max chat` / `max "…"`                    | Chat with the **Max** AI assistant (not an agent flow)           |
| `frontline agents conversations list/get` | **Read** production conversation transcripts (no flow execution) |

## Typical workflow

```bash
frontline agents use <agent-id>
frontline agents chat --message "I need help with my order"
# Note conversation_id from output: jq '.data.conversation_id'
frontline agents chat --message "Order #12345" --conversation-id <id>
frontline agents chat close <id>
```

After editing a flow, re-run `frontline agents chat` to validate the updated graph before deploying.

## Troubleshooting

| Error                | Cause                                                                  |
| -------------------- | ---------------------------------------------------------------------- |
| `agent_not_selected` | No active agent — run `frontline agents use <id>` or pass `--agent-id` |
| `missing_message`    | `--conversation-id` requires `--message` to continue                   |

## See also

- `frontline-agents` skill — list, inspect, and manage agents
- `agent-builder` skill — create and deploy agents step by step
- `max-chat` skill — chat with Max (different product surface)
- [CLI reference: agents chat](https://docs.getfrontline.ai/cli/frontline/agents)
