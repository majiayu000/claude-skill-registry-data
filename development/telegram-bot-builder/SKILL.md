---
name: telegram-bot-builder
description: Build Telegram bots in Node.js. Use when a request mentions Telegram bot, BotFather, bot token, webhook, long polling, commands, inline keyboards, callback queries, or handling Telegram Bot API updates.
---

# Telegram Bot Builder

## Overview

Create production-ready Telegram bots in Node.js with clear setup steps, secure token handling, and reliable update processing. Default to telegraf unless the user specifies another library.

## Workflow

1) Clarify requirements
- Ask for bot token availability (BotFather token) and whether commands are defined.
- Ask for hosting and update mode: webhook or long polling.
- Ask for features: commands, inline keyboards, callbacks, files, or integrations.
- Ask for data storage or state (sessions, database, or in-memory).

2) Choose library and update mode
- Use `telegraf` for modern middleware and strong typing support.
- Use `node-telegram-bot-api` only when explicitly requested.
- Prefer webhooks for production hosting, long polling for local or simple deployments.

3) Implement core bot flow
- Create command handlers and message routing.
- Validate inputs and avoid echoing secrets.
- Add error boundaries and logging.

4) Ship-ready details
- Provide install commands and env vars.
- Include webhook configuration or polling startup instructions.
- Provide quick test steps and sample output.

## Common tasks

### Build a basic bot
- Use `references/telegraf.md` for a minimal bot and message routing.

### Add commands and keyboards
- Define commands in BotFather and mirror them in code.
- Use inline keyboards with callback queries; keep callback data small.

### Webhooks and deployments
- Use `references/webhooks.md` for webhook setup and platform notes.

### Alternate library
- If the user insists on `node-telegram-bot-api`, use `references/node-telegram-bot-api.md`.

## Output expectations

- Provide runnable Node.js code (ESM by default; call out CJS if needed).
- List dependencies and install commands.
- List required env vars, especially `TELEGRAM_BOT_TOKEN`.
- Include a short verification checklist.

## References

- `references/telegraf.md`
- `references/webhooks.md`
- `references/node-telegram-bot-api.md`
