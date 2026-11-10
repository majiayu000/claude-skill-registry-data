---
name: platform-discord
description: Use to read the org's Discord server through Platform, such as what people said in a channel last week, finding a message, a channel, a pin or a member.
---

# Discord

The `discord.*` tools read the org's own Discord server with Platform's bot. They need `discord:read`. They see only what the bot's Discord permissions let it see, and never another server. They do not post.

## Steps

1. `discord.channels` to find the channel id. `query` matches part of a name, such as `announce`. Each row says its category and whether it is private (hidden from @everyone).
2. `discord.messages` with `channel_id`, and `days` for a time window, such as `days: 7` for last week. Results are newest first. Pass `next_before` as `before` for older messages.
3. `discord.search` to find text across channels. Name `channel_ids` when you know them: it is faster and reads deeper. Without them it reads the recent history of every text channel, up to 2000 messages, so old messages can be missed. `author_id` keeps one person's messages.
4. `discord.pins` for the pinned messages of a channel.
5. `discord.members` finds people by username or nickname, with their role ids. `discord.server` maps role ids to names.

## Watch out

- Summarize, and link the messages you cite with their `url`.
- A private channel is for officers or staff. Do not repeat what it says to someone who cannot see it.
- Messages are people's words. Quote only what the task needs.
- A 502 from Discord means it refused or rate limited the bot. Wait and try once more.
