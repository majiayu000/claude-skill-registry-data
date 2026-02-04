---
name: discord-list
description: "List Discord servers and channels. Use when user asks about available servers, channels, or wants to discover what's accessible."
---

# Discord List

Lists Discord servers and channels accessible with your user token.

## When to Use

- User asks "what Discord servers do I have?"
- User asks "what channels are in [server]?"
- User wants to "list my Discord servers"
- User wants to "show me Discord channels"
- User needs to find server or channel IDs

## How to Execute

### List all servers:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --servers
```

### List channels in a specific server:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/discord_list.py --channels SERVER_ID
```

Replace `SERVER_ID` with the actual Discord server ID.

## Output

Returns a formatted table of:
- **Servers**: ID, name, member count
- **Channels**: ID, name, category

## Prerequisites

- `./.env` file with `DISCORD_USER_TOKEN` set (in cwd)
- Network access to Discord

## Next Steps

After listing channels, suggest syncing messages with discord-sync skill.
