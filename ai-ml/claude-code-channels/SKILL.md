---
name: claude-code-channels
category: messaging
description: Set up Claude Code messaging channels for Telegram and Discord — bot creation, plugin installation, token configuration, access control (pairing, allowlists, guild channels), and troubleshooting. Use when the user asks to connect Claude Code to Telegram or Discord, configure a messaging bot, set up channel access, enable guild channels or threads, troubleshoot MCP server failures, or manage channel permissions. Triggers on "telegram channel", "discord channel", "claude code channels", "messaging bot", "set up telegram", "set up discord", "pairing code", "discord bot", "telegram bot", "channel access", "--channels".
---

# Claude Code Channels Setup

Claude Code Channels pushes messages from external platforms (Telegram, Discord) into a running Claude Code session via MCP server plugins.

## Prerequisites

- Claude Code v2.1.80+
- [Bun](https://bun.sh) runtime
- A claude.ai account (not API key mode)

## Platform Selection

Ask which platform(s) the user wants, then follow the relevant reference:

- **Telegram**: See [references/telegram.md](references/telegram.md)
- **Discord**: See [references/discord.md](references/discord.md)

Both can run simultaneously:
```bash
claude --channels plugin:telegram@claude-plugins-official,plugin:discord@claude-plugins-official
```

## Universal Workflow

Regardless of platform, setup follows 6 steps:

1. **Create bot** on the platform's developer portal
2. **Install plugin**: `/plugin install <platform>@claude-plugins-official`
3. **Configure token**: `/<platform>:configure <token>`
4. **Launch session**: `claude --channels plugin:<platform>@claude-plugins-official`
5. **Pair account**: DM the bot, get a code, run `/<platform>:access pair <code>`
6. **Lock down**: `/<platform>:access policy allowlist`

## Troubleshooting

### MCP Server Shows "failed" on Startup

Known race condition — server may fail on cold start but reconnect fine.

**Fix**: Run `/mcp`, navigate to the failed server, select **Reconnect**.

**Persistent failures** — verify the bot token:
```bash
# Telegram
TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.claude/channels/telegram/.env | cut -d= -f2)
curl -s "https://api.telegram.org/bot$TOKEN/getMe"

# Discord
TOKEN=$(grep DISCORD_BOT_TOKEN ~/.claude/channels/discord/.env | cut -d= -f2)
curl -s -H "Authorization: Bot $TOKEN" https://discord.com/api/v10/users/@me
```

If unauthorized/401, regenerate the token and update `~/.claude/channels/<platform>/.env`.

### Plugin Not Found

Add the official marketplace first:
```bash
/plugin marketplace add anthropics/claude-plugins-official
```

### Bot Not Responding

1. Session must be running with `--channels` flag
2. `/mcp` must show the server as "connected"
3. Telegram: verify token with BotFather
4. Discord: enable **Message Content Intent** in Developer Portal → Bot → Privileged Gateway Intents

### Dependency Issues

Pre-install manually:
```bash
cd ~/.claude/plugins/cache/claude-plugins-official/<platform>/<version>
bun install --no-summary
```

## Running as Background Service (tmux)

```bash
# Start
tmux new-session -d -s claude-<platform> \
  'claude --dangerously-skip-permissions --channels plugin:<platform>@claude-plugins-official'

# Attach / Detach
tmux attach -t claude-<platform>   # Ctrl+b then d to detach

# After startup, if MCP failed: /mcp → select server → Reconnect
```

## Access Control

Both platforms share the same model. Replace `<platform>` with `telegram` or `discord`.

| Command | Effect |
|---|---|
| `/<platform>:access` | Show current state |
| `/<platform>:access pair <code>` | Approve pairing |
| `/<platform>:access deny <code>` | Reject pairing |
| `/<platform>:access allow <id>` | Add user by ID |
| `/<platform>:access remove <id>` | Remove user |
| `/<platform>:access policy <mode>` | `pairing` / `allowlist` / `disabled` |
| `/<platform>:access group add <id>` | Enable group/channel |
| `/<platform>:access group add <id> --no-mention` | Enable without requiring @mention |
| `/<platform>:access group rm <id>` | Disable group/channel |
| `/<platform>:access set <key> <value>` | Configure delivery settings |

## State Files

```
~/.claude/channels/<platform>/
├── .env          # Bot token (mode 0o600)
├── access.json   # Policy, allowlist, groups, pending
├── approved/     # Approved user ID → chat ID mapping
└── inbox/        # Downloaded attachments
```
