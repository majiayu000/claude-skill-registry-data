---
name: discord-rest-api
description: >-
  Call the Discord REST API from scripts and cron — message posting, thread
  creation, guild/channel discovery, and the critical User-Agent header fix
  that prevents 40333 errors. Covers curl and Python patterns for bots.
version: 1.0.0
metadata:
  hermes:
    tags: [discord, rest-api, bot, thread, integration]
    triggers:
      - post to discord
      - create discord thread
      - discord rest api
      - discord 40333
      - internal network error discord
---

# Discord REST API Integration

Call the Discord REST API from curl or Python scripts. Covers the auth pattern,
the critical User-Agent header fix, and common operations.

## Authentication

The bot token goes in the `Authorization` header:

```bash
Authorization: Bot MTUwMjcwNjc1Nzg1MDYyODE5Nw.XXXXXX.XXXXXXXX
```

The token is stored at `~/AppData/Local/hermes/.env` as `DISCORD_BOT_TOKEN`.
Source it with: `source ~/AppData/Local/hermes/.env`

## CRITICAL: User-Agent Header

**Without a User-Agent header, the Discord API returns:**
```json
{"message": "internal network error", "code": 40333}
```

This is NOT a network error — it's Discord rejecting the request for not
identifying itself. The fix is always the same:

**curl:**
```bash
-H "User-Agent: DiscordBot (https://your-domain.example, 1.0)"
```

**Python urllib:**
```python
req = urllib.request.Request(url, headers={
    "User-Agent": "DiscordBot (https://your-domain.example, 1.0)",
    "Authorization": f"Bot {token}"
})
```

The exact User-Agent string matters less than having one — it just needs to
identify the caller. `"DiscordBot (https://your-domain.com, 1.0)"` works.

## Guild & Channel Discovery

### Get guilds the bot is in:
```bash
curl -s -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/users/@me/guilds" \
  | python -c "import sys,json; [print(f'{g[\"id\"]} — {g[\"name\"]}') for g in json.load(sys.stdin)]"
```

### Get channels in a guild:
```bash
curl -s -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/guilds/{guild_id}/channels" \
  | python -c "import sys,json; [print(f'{ch[\"id\"]} #{ch[\"name\"]} type={ch[\"type\"]}') for ch in json.load(sys.stdin) if ch.get('type')==0]"
```

### Get channel permissions:
```bash
curl -s -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/channels/{channel_id}"
```

## Thread Creation (2-Step Process)

Threads require TWO API calls:

### Step 1 — Post a starter message
```bash
MSG=$(curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/channels/{channel_id}/messages" \
  -d '{"content": "🧠 **Thread topic** — starter message"}')

MSG_ID=$(echo "$MSG" | python -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
```

### Step 2 — Create thread from that message
```bash
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/channels/{channel_id}/messages/$MSG_ID/threads" \
  -d '{"name": "Thread-Name", "auto_archive_duration": 1440}'
```

Thread type is 11 (public thread) when created from a message. The response's
`id` is the thread ID. Link format:
```
https://discord.com/channels/{guild_id}/{thread_id}
```

### Known Guild IDs (the operator)
- **Automation Team:** `<discord-channel-id>`
- **AI Sharp:** `<discord-channel-id>`

## Sending Messages

### Post a simple message:
```bash
curl -s -X POST \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: DiscordBot (https://your-domain.example, 1.0)" \
  "https://discord.com/api/v10/channels/{channel_id}/messages" \
  -d '{"content": "Your message here"}'
```

### Send an embed:
```json
{
  "embeds": [{
    "title": "Title",
    "description": "Description",
    "color": 5763719,
    "fields": [
      {"name": "Field", "value": "Value", "inline": true}
    ]
  }]
}
```

## Pitfalls

- **User-Agent is required for all REST API calls.** Without it → 40333.
  The gateway's WebSocket connection (discord.py) sets its own UA, so this
  only affects REST API calls from curl or Python scripts.
- **Rate limits:** Standard Discord rate limiting applies. Check the
  `x-ratelimit-remaining` header. Bot accounts get higher limits (30 req/sec
  per route vs 5 for user accounts).
- **Bot permissions depend on role assignments in the guild.** If the bot
  has no roles, it inherits @everyone permissions. If it can't post in a
  specific channel, check for channel-specific permission overwrites.
- **Threads from messages vs empty threads.** `POST /channels/{id}/threads`
  creates an empty thread (no starter message). `POST .../messages/{id}/threads`
  creates a thread with a starter message — preferred for visibility.
  The message-first approach requires `SEND_MESSAGES` permission in the
  parent channel; empty thread creation requires `CREATE_PUBLIC_THREADS`.
