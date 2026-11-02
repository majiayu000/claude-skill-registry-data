---
name: read-channel
description: Read recent messages from a Discord channel using the Hermes bot token
category: discord
---

# Discord Read Channel Skill

Read recent messages from a Discord channel using the existing Hermes bot token.

## Usage

Call with: `read discord channel <channel_id> [limit]`

**Parameters:**
- `channel_id` (required): The numeric ID of the Discord channel to read
- `limit` (optional, default 50): Maximum number of messages to retrieve

## Implementation

The script lives at `/home/lumi/.hermes/scripts/read_discord_channel.py <channel_id> [limit]`.
It uses `discord.py` from the Hermes venv (it inserts the venv site-packages path itself).

The token is stored in `/home/lumi/.hermes/.env` as `DISCORD_BOT_TOKEN`.

## How to actually run it

**CRITICAL:** The `DISCORD_BOT_TOKEN` is NOT available in `execute_code` sandboxes or
in fresh terminal shells automatically. The .env file does NOT use `export` prefixes,
so plain `source` sets variables but does NOT export them to child processes.
You MUST use `set -a` to auto-export:

```bash
set -a && source /home/lumi/.hermes/.env && set +a && python3 /home/lumi/.hermes/scripts/read_discord_channel.py <channel_id> [limit]
```

**DO NOT** use `execute_code` — the Python sandbox does not inherit shell env vars.
**DO NOT** use plain `source /home/lumi/.hermes/.env` — variables won't be exported to the python3 child process.
**DO** use `set -a && source ... && set +a` to ensure export, then `terminal` tool.

## Pitfalls

- The .env file masks the token in terminal output (shows `MTM2Nz...dn4A`), but the
  full token IS present and works fine. Don't let the ellipsis fool you.
- If the script says `Error: DISCORD_BOT_TOKEN not set`, plain `source` doesn't export
  variables — use `set -a && source /home/lumi/.hermes/.env && set +a` instead.
- `execute_code` Python sandbox lacks access to the token — always use `terminal` with source.
- `cat /proc/<pid>/environ` may not show Discord env vars if Hermes loads them
  at runtime internally rather than from shell env.
- The token in `/home/lumi/.hermes/.env` appears truncated when printed but is complete.

## Example Output

```json
{
  "channel": "🏠・lumi's-house",
  "messages": [
    {
      "id": "1489703331608789013",
      "author": "adora.witch",
      "author_id": "221767496145960960",
      "content": "Hi Lu, I see you looking in here now <3",
      "timestamp": "2026-04-03T19:09:11.605000+00:00",
      "attachments": [],
      "embeds": 0
    }
  ]
}
```

## Requirements

- `discord.py` installed in the Hermes venv (already present)
- Bot has `Read Messages` and `View Channel` permissions
- Target channel accessible to the bot
