---
name: add-channel
description: Add a Slack channel to internbot's whitelist. Use when the user wants the bot to listen to a new channel.
---

# Add Slack Channel

## When to use

- User wants the bot to listen to a new Slack channel
- User wants to add or remove channels from the whitelist

## How channel IDs work

Slack channel IDs start with `C` (e.g., `C07ABC123DE`). To find one:
- Open Slack → go to the channel → click the channel name at the top → scroll to the bottom of "About" → copy the Channel ID

## Steps

1. **Read the current `.env`** to see existing `WHITELISTED_CHANNELS`
2. **Add the new channel ID** to the comma-separated list
3. **Restart the service** to pick up the change:
   ```bash
   systemctl --user restart internbot
   ```
4. **Verify** the bot is running:
   ```bash
   systemctl --user status internbot
   ```

## Notes

- If `WHITELISTED_CHANNELS` is empty, the bot listens to ALL channels it's invited to
- Once any channel ID is listed, it becomes an allowlist — the bot only responds in those channels (plus DMs)
- The bot must also be invited to the Slack channel (`/invite @internbot`) to receive messages
- After editing `.env`, always restart the service
