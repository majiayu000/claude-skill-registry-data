---
name: mee6
# A skill for controlling the Mee6 Discord bot (leveling, moderation, custom commands).
description: "Mee6 operations via Discord message tool (channel=discord)."
metadata:
  { "openclaw": { "emoji": "🤖", "requires": { "config": ["channels.discord.token"] } } }
---

# Mee6 (Discord bot)

Use the `message` tool exactly like the `discord` skill, but target the Mee6
bot when issuing commands. This skill exists purely to give the agent a
reference for common Mee6 actions and any bot-specific quirks.

* Always set `channel: "discord"`.
* Start messages with the server's prefix (usually `!`).
* Mention Mee6 by ID or @Mee6 when required.
* Gating is handled via the same `channels.discord.actions.*` config as the
  `discord` skill; no additional permissions are needed.

## Common commands

- **Check level** – `!level @user`
- **Give xp** – `!give-xp @user <amount>`
- **Create role** – `!role create <rolename>`
- **Enable plugin** – `!plugins enable <plugin-name>`
- **Disable plugin** – `!plugins disable <plugin-name>`
- **Set prefix** – `!prefix <new-prefix>`

> The agent should only emit Mee6 commands when the user explicitly requests
> interaction with the Mee6 bot. Avoid sending raw commands for unrelated
> Discord actions; use the generic `discord` skill for everything else.
