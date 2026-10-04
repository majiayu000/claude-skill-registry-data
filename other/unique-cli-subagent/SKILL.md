---
name: unique-cli-subagent
description: >-
  Invoke connected Unique spaces/subagents through the unique-cli subagent
  command. Use when the workspace exposes connected-space tools and you need
  to delegate a question or task to one of those configured assistants.
---

# Unique CLI -- Connected Spaces / Subagents

Use this skill to call a connected Unique space as a tool. Each connected
space is configured by the platform in `.unique-subagents.json`; call it by
the tool name shown in the generated connected-space skill.

## Usage

```bash
unique-cli subagent "<tool_name>" "<message>" \
  --chat-id "$UNIQUE_CHAT_ID" \
  --assistant-id "$UNIQUE_ASSISTANT_ID"
```

Omit `--message-id`: the CLI resolves the current turn's assistant message ID
from `$UNIQUE_TURN_IDENTITY_FILE` automatically.

## Rules

1. Use the exact tool name from the connected-space skill or from
   `.unique-subagents.json`.
2. Send a focused message that contains the subagent-specific task and the
   relevant context.
3. Treat the returned text as the connected space's answer. Do not invent
   details that are not in the response.
4. If the connected space has references in its text, preserve them exactly.

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `<tool_name>` | required | Name of the configured connected-space tool. |
| `<message>` | required | Prompt sent to the connected space. |
| `--reset-chat` | off | Start from a fresh subagent chat instead of reusing the saved chat. |
| `--json` | off | Print the raw response JSON. |
| `--config` | `.unique-subagents.json` | Override the config path. |

## Prerequisites

The platform sets these environment variables automatically:

```bash
UNIQUE_USER_ID
UNIQUE_COMPANY_ID
UNIQUE_CHAT_ID
UNIQUE_TURN_IDENTITY_FILE
UNIQUE_ASSISTANT_ID
UNIQUE_API_KEY
UNIQUE_APP_ID
```
