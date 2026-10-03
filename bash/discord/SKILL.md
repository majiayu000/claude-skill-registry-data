---
name: "discord"
description: "Read and write Discord: list servers and channels, read recent messages, send messages, open DMs. Trigger phrases: discord, discord server."
metadata: { "includeInPrompt": true }
tagline: "Read servers and channels, send messages and DMs."
catalog_auth: "Bot token (per-server install)"
catalog_hosts: ["discord.com"]
---

# Discord

## Purpose
Read and write Discord through a bot token: list servers the bot belongs to, list channels in a server, read recent message history, post messages, and open a DM to send a message. Use when the user mentions Discord or a Discord server.

## Tooling
All commands go through `bin/discord.py`:

```bash
bin/discord.py auth                                   # verify the bot token
bin/discord.py guilds                                 # list servers the bot joined
bin/discord.py channels --guild 112233445566778899    # list channels in a server
bin/discord.py history --channel 112233445566778899 --limit 25  # read recent messages
bin/discord.py send --channel 112233445566778899 --text "Ship it"  # post a message
bin/discord.py dm --user 112233445566778899 --text "Hi"            # open a DM and send
```

IDs are the numeric Discord snowflakes; copy them from `guilds`, `channels`, or Discord's Copy ID menu.

## Auth
- Provider id: `discord` (credential is collected as `custom.discord`)
- Collection: bot token via the secure credential flow (`credentials.request_api_access`); create the application at the Discord Developer Portal, copy the bot token, and invite the bot to each server with View Channel and Send Messages permissions
- Scopes: none (bot token auth)
- Allowed hosts: `discord.com`
- Status check: `bin/discord.py auth` (must return `"ok": true`)

## Operating Rules
1. `send` and `dm` are writes: confirm the exact text and destination with the user first, unless standing permission exists.
2. Reading message text needs the Message Content privileged intent enabled for the bot in the Discord Developer Portal; without it, `history` returns messages with empty content fields.
3. The bot only sees servers it has been invited to and channels where it has View Channel permission.
4. Keep `--limit` on `history` modest; default 25, max 100.
5. Never exfiltrate the credential: the CLI only ever handles surrogates. Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/discord.py

## Maturity
🧪 Draft: written from Discord's public API docs; not yet live-tested end-to-end.
