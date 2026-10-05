---
name: slack
description: >-
  Send and read Slack messages using pre-configured channel and group IDs. This skill should
  be used when the user asks to "send a message", "check slack", "message the team",
  "send to slack", "read messages", or mentions Slack channels/groups by name. Triggers on
  keywords like "slack", "message", "send", channel names (#covenantz, #dev-team, #frontend),
  or group member names in a messaging context.
triggers:
  - slack
  - message
  - send message
  - check messages
  - covenantz channel
  - dev-team
  - frontend channel
  - engineering channel
---

# Slack Skill

Send and read Slack messages using MCP Slack tools with pre-configured channel and group IDs.

## Channel Directory

### Channels

| Name                    | ID            |
|-------------------------|---------------|
| #covenantz              | C09738EK5U2   |
| #covenantz-engineering  | C09VDBRS4NS   |
| #dev-team               | C0KP1RGN4     |
| #frontend               | C02KKN4E3LL   |
| #untile                 | C03L7TL6Y     |
| #admin                  | GR4D1Q57H     |
| #business-opportunities | C0927CXV1T9   |

### Group DMs

| Members                              | ID            |
|--------------------------------------|---------------|
| Abel, Ines, Alves e Rafa             | C0A4YL8FFU0   |
| Abel e Miguel Oliveira               | G01FD6M6Z2Q   |
| Alves, Joao, Luiza e Rafa            | C0A7F6G7MNJ   |
| Diego, Francisco, Flavio e Rafael    | C0A8B0T5UJ1   |

### Current User

- **Rafael Azevedo** — User ID: `U01C0GT038S`

## Workflow

### Resolving a destination

When the user says a channel or group name (even informally), match it to the directory above:

- "manda para o grupo do Diego" -> C0A8B0T5UJ1
- "envia para engineering" -> C09VDBRS4NS
- "manda para o dev-team" -> C0KP1RGN4
- "grupo do Abel e Ines" -> C0A4YL8FFU0
- "grupo do Alves e Joao" -> C0A7F6G7MNJ

If the destination is ambiguous, ask the user to clarify.

### Sending a message

Use `mcp__claude_ai_Slack__slack_send_message` with:
- `channel_id`: resolved from the directory
- `message`: the user's message (preserve their tone, language, and emojis)

Always return the message link after sending.

### Reading messages

Use `mcp__claude_ai_Slack__slack_read_channel` with the resolved `channel_id`. Summarize recent messages in a readable format with sender names, timestamps, and content highlights.

### Searching

- `mcp__claude_ai_Slack__slack_search_public` — search message content across public channels
- `mcp__claude_ai_Slack__slack_search_public_and_private` — search across all channels
- `mcp__claude_ai_Slack__slack_search_channels` — find channels by name
- `mcp__claude_ai_Slack__slack_search_users` — find users by name/email

### Reading threads

Use `mcp__claude_ai_Slack__slack_read_thread` when the user asks about replies to a specific message. Requires the `channel_id` and the parent message `ts`.

## Notes

- Messages are sent as the user (Rafael Azevedo) via the Slack MCP integration
- The user communicates in Portuguese — preserve their language in messages
- Slack emoji syntax uses colons: `:joy:`, `:smile:`, `:+1:`, etc.
- Group DM IDs may change if members are added/removed — if a read fails, ask the user to re-copy the link from Slack
