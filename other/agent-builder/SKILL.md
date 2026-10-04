---
name: agent-builder
allowed-tools: Bash(frontline:*)
description: Build and configure Frontline agents from the CLI, including creation, active context, deployment status, theme, agent settings, and channel settings.
---

## Prerequisites

- Authenticate with a USER API key: `frontline auth login <api-key>`.
- Mutations require USER API keys because ownership, billing, and account checks use the API key user context.

## Create And Select An Agent

```bash
frontline agents create --name "Support Agent"
frontline agents describe
frontline agents use <agentId>
```

`create` saves the new agent as the active agent by default. Pass `--no-use` to
avoid changing context. Any agent-scoped command can use `--agent-id <id>` to
override the active context.

## Basic CRUD

```bash
frontline agents list --status ACTIVE
frontline agents describe
frontline agents update --name "Support Agent v2"
frontline agents delete
```

Delete is a soft delete through the assistant manager, preserving platform side
effects and cleanup behavior.

## Deployment

```bash
frontline agents deploy --offline false  # publish
frontline agents deploy --offline true   # pause
```

Publishing runs the same billing checks as the internal assistant manager.

## Validate with test chat

After deploying, smoke-test the flow from the terminal:

```bash
frontline agents chat --message "Hello, I need help"
```

See the `agents-chat` skill for continuing conversations, linking contacts,
and closing test sessions.

## Agent Setting

Use `agent-setting` for instructions, model, tools, connected accounts, system
tools, and selected tables.

```bash
frontline ai-models list --type TEXT --table
frontline agents agent-setting get
frontline agents agent-setting update --data '{"instructions":"Answer concisely.","temperature":0.2,"aiModelId":-29}'
```

The CLI **merges** `--data` with the current agent setting before sending the
PUT. You can send only the fields you want to change, for example:

```bash
frontline agents agent-setting update --data '{"instructions":"New prompt only"}'
```

The API still validates the merged payload. Include `aiModelId`, `temperature`,
and `instructions` when calling the Public API directly without the CLI merge
helper.

**Field constraints (validated by the API):**

| Field           | Type    | Constraints                                                        |
| --------------- | ------- | ------------------------------------------------------------------ |
| `temperature`   | number  | min `0`, max `1`. Use one decimal place (e.g. `0.2`, `0.7`, `1.0`) |
| `maxIterations` | integer | min `3`, max `30`. Default `10`                                    |
| `aiModelId`     | integer | non-zero integer from `frontline ai-models list --type TEXT`       |

Use a TEXT model ID for `aiModelId`. The update command performs reference
preflight in the same execution for resources exposed by Public API, including
`aiModelId` and `customToolIds`; it then sends the
mutation. The backend still performs final validation for all referenced objects,
including connected accounts and ownership.

Resolve `connectedAccountId` values with `frontline integrations list --table` (USER API key). Channels (WhatsApp/Instagram/Messenger) are listed with `frontline channels list`.

## Theme

```bash
frontline agents theme get
frontline agents theme update --data '{"title":"Support","initialMessage":"Hi! How can I help?","placeholder":"Type your message...","avatar":null,"bubbleImage":null,"bubbleColor":"#111827","userMessageColor":"#2563eb","agentMessageColor":"#f3f4f6","bubbleAlignment":"RIGHT","progressIndicator":"DYNAMIC","verticalPositionInPixels":24}'
```

The first public builder cut does not upload image files. Use existing image
URLs or `null` for `avatar` and `bubbleImage`.

## Channel Settings

Supported channel names are `livechat`, `whatsapp`, `instagram`, and
`messenger`.

```bash
frontline agents settings get
frontline agents settings get livechat
frontline agents settings update whatsapp --data '{"splitMessages":true,"splitCharacterLimit":500,"conversationClose":"NEVER","closeAfter":null,"timeUnit":null,"sendCloseMessage":false,"closeMessageType":"STATIC","closeMessage":null,"closeInstruction":null}'
frontline agents settings list-channels --table
```

Channel payloads are validated with the internal channel-specific schemas, so
required fields differ by channel. Start from `settings get <channel>`, edit the
JSON, then send it back with `settings update <channel> --data`.

---

## See also

- `agents-chat` skill — test flows end-to-end after deploy
- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
