---
name: discord-bot
description: "The dockerized MythiStone Discord slash-command bot (discord_bot/): cogs, embeds, emojis, site JSON and DB access, usage tracking, /news subscriptions, ops webhooks. Use when editing discord_bot/, Dockerfile.bot, buildBotImage.yml or Discord webhook handling."
---

# Discord Bot domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `bot-architecture` | The Discord bot is a third consumer of backend modules, static lookups and page logic that the collector and the page generators own, so a change made for them must keep the bot importing, querying and rendering | `discord_bot/*`, `Dockerfile.bot`, `backend_scripts/databaseConnector.py`, `backend_scripts/commonUtils.py`, `backend_scripts/chartData.py`, `backend_scripts/tierMath.py`, `backend_scripts/season_gate.py`, `backend_scripts/computeBuildPhase.py`, `backend_scripts/image_generation/*`, `assets/js/analyzer.js` |
| `bot-db-grants` | The bot and CI connect to production MySQL with their own users, and database.sql is not applied to the server automatically, so a table the bot touches is created and granted by hand | `discord_bot/usage_stats.py`, `discord_bot/cogs/news.py`, `backend_scripts/broadcastDiscordNews.py` |
| `ops-discord-channels` | Which Discord webhook carries which ops output (the self-editing collector status and bot usage embeds vs. alerts, entrypoint pings and watchtower), and what the embeds need from docker-compose.yml to stay single and visible | `backend_scripts/discordHandler.py`, `discord_bot/usage_stats.py`, `entrypoint.sh`, `entrypoint_bot.sh`, `docker-compose.yml` |
