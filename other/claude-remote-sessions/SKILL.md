---
name: claude-remote-sessions
category: messaging
description: "Per-channel remote sessions for Claude Code via Discord and Telegram — each channel, thread, or chat gets its own isolated Claude Code session via tmux, with per-channel access control, project-specific workdirs, and automatic CLAUDE.md chain loading. Includes session managers, watchdog daemons (auto-respawn, auto-discover, stale cleanup), thread context injection, session resume, workdir mapping, and launchd boot persistence. Use when: (1) setting up per-channel Discord/Telegram sessions for Claude Code, (2) managing multiple sessions across messaging channels, (3) auto-discovering new channels or threads, (4) spawning thread sessions with parent conversation context, (5) keeping remote agent sessions alive, (6) cleaning up stale sessions, (7) setting up Telegram per-chat sessions. Triggers on 'remote sessions', 'discord sessions', 'telegram sessions', 'per-channel discord', 'discord watchdog', 'telegram watchdog', 'spawn discord session', 'claude remote', 'channel session', 'thread session'."
---

# Claude Remote Sessions

Each Discord channel or thread maps to its own independent Claude Code session running
in a tmux pane. Discord messaging is handled natively by the MCP plugin inside each
session. A watchdog daemon keeps sessions alive and auto-discovers new channels/threads.

## Prerequisites

- Claude Code with `--channels` support (v2.1.80+)
- Discord bot configured: `/discord:configure <token>`
- tmux installed
- Discord bot invited to your server with permissions: View Channels, Send Messages,
  Read History, Attach Files, Add Reactions, Manage Channels, Create Threads

## Setup

### 1. Configure environment

Create `~/.claude/discord-sessions/config.env`:

```bash
# Required
DISCORD_ALLOWED_USER_ID="your-discord-user-id"
DISCORD_GUILD_ID="your-guild-server-id"

# Optional (defaults shown)
DISCORD_SESSION_WORKDIR="$HOME"          # Default workdir for new sessions
DISCORD_WATCHDOG_INTERVAL=30             # Respawn check frequency (seconds)
DISCORD_DISCOVER_INTERVAL=60             # Channel/thread discovery frequency (seconds)
DISCORD_CLEANUP_INTERVAL=300             # Stale session cleanup frequency (seconds)
```

Find your user ID: Discord Settings → Advanced → Enable Developer Mode → right-click your name → Copy User ID.
Find your guild ID: Right-click your server name → Copy Server ID.

### 2. Install scripts

Copy scripts to your project:

```bash
cp scripts/discord-session-manager.sh ~/your-project/scripts/
cp scripts/discord-watchdog.sh ~/your-project/scripts/
chmod +x ~/your-project/scripts/discord-session-manager.sh
chmod +x ~/your-project/scripts/discord-watchdog.sh
```

### 3. Start

```bash
# Discover all channels + threads and spawn sessions
./scripts/discord-session-manager.sh discover-all

# Start the watchdog (auto-respawn + auto-discover every 60s)
./scripts/discord-watchdog.sh --daemon
```

## Session Manager

Script: `scripts/discord-session-manager.sh`

### Spawn

```bash
# Channel session
./scripts/discord-session-manager.sh spawn <channel_id> --name <label> [--workdir <path>]

# Thread session (fetches last 20 parent messages as context)
./scripts/discord-session-manager.sh spawn-thread <thread_id> <parent_id> [--name <label>] [--workdir <path>]

# Fresh session — resets conversation history for a channel
./scripts/discord-session-manager.sh spawn <channel_id> --name <label> --fresh
```

Default workdir comes from `config.env`. Override per-session with `--workdir` to scope
a session to a specific project — it loads that project's CLAUDE.md chain automatically.

Each session gets:
- A tmux session `dc-<id>` running Claude Code with `--channels discord`
- A deterministic `--session-id` (UUID v5 derived from the channel ID) so conversation
  history persists across watchdog respawns
- A per-channel `DISCORD_STATE_DIR` with scoped `access.json`
- A persisted `.session-id` file in the state directory
- A registry entry in `sessions.json`

### Auto-Discovery

```bash
./scripts/discord-session-manager.sh discover           # new channels
./scripts/discord-session-manager.sh discover-threads    # new threads with parent context
./scripts/discord-session-manager.sh discover-all        # both
```

The watchdog runs `discover-all` every 60 seconds. Create a channel or thread on
Discord → a session spawns automatically.

### Create a Channel

```bash
./scripts/discord-session-manager.sh create-channel <name>
```

Creates the Discord channel via API AND spawns its session.

### Stale Session Cleanup

```bash
./scripts/discord-session-manager.sh cleanup-stale
```

Checks each registered session against the Discord API. Kills and deregisters sessions
whose channel has been deleted (HTTP 404) or whose thread has been archived
(`thread_metadata.archived: true`). The watchdog runs this automatically every 5 minutes
(configurable via `DISCORD_CLEANUP_INTERVAL`).

### Manage

```bash
./scripts/discord-session-manager.sh list           # UP/DOWN status
./scripts/discord-session-manager.sh status          # overview
./scripts/discord-session-manager.sh attach <id>     # attach to tmux session
./scripts/discord-session-manager.sh kill <id>       # kill and deregister
./scripts/discord-session-manager.sh kill-all        # kill everything
```

## Watchdog Daemon

Script: `scripts/discord-watchdog.sh`

```bash
./scripts/discord-watchdog.sh --daemon    # start in tmux: dc-watchdog
./scripts/discord-watchdog.sh --stop      # stop
./scripts/discord-watchdog.sh --status    # check if running
```

Every 30s: respawns dead sessions. Every 60s: discovers new channels and threads.
Every 5m: cleans up stale sessions (deleted channels, archived threads).

### Boot Persistence (macOS)

See [references/launchd.md](references/launchd.md) for a launchd plist template
that starts the watchdog on login.

## Session Persistence

Sessions survive watchdog respawns by using Claude Code's `--session-id` flag. When a
session is spawned, a deterministic UUID v5 is generated from a fixed namespace and the
channel/thread ID. This means:

- **Same channel = same session ID** — the conversation resumes where it left off after
  a crash or respawn.
- The UUID is persisted to `$SESSIONS_DIR/<channel_id>/.session-id` so `respawn-dead`
  reads it back and passes it to the new claude process.
- Use `--fresh` when spawning to generate a random UUID v4 instead, resetting the
  conversation history for that channel.

### How it works

1. `spawn` / `spawn-thread` calls `_generate_session_id(channel_id)` which produces a
   deterministic UUID v5 via `python3 -c "uuid.uuid5(namespace, channel_id)"`.
2. The UUID is saved to `<state_dir>/.session-id` and passed as `--session-id <uuid>` to
   the claude command.
3. When the watchdog calls `respawn-dead`, the persisted UUID is read from `.session-id`
   and passed back to `_spawn_tmux`, so claude resumes the same conversation.
4. `--fresh` overrides this with a new random UUID v4, giving the channel a clean slate.

## Thread Detection (In-Session)

When a session receives a message where `chat_id` differs from its assigned channel,
it is a thread message. The session should:

1. Check if a session exists: `./scripts/discord-session-manager.sh list`
2. If not, spawn one: `./scripts/discord-session-manager.sh spawn-thread <chat_id> <channel_id>`
3. Reply acknowledging the handoff

In practice, the watchdog handles this automatically via `discover-threads`.

## Channel-to-Workdir Mapping

By default, all sessions use the `DISCORD_SESSION_WORKDIR` from `config.env`. To assign
different project directories to specific channels, create a mapping file:

**File:** `~/.claude/discord-sessions/workdir-map.json`

```json
{
  "general": "$HOME/myproject",
  "health-os": "$HOME/myproject/apps/healthOS",
  "life": "$HOME/myproject/core/life",
  "design-system": "$HOME/myproject/apps/arcan-glass"
}
```

**How it works:**

- When `discover` or `discover-threads` spawns a new session, it looks up the channel/thread
  name in `workdir-map.json`.
- If a match is found, the session starts in that directory (with that project's CLAUDE.md chain).
- If no match is found, the default `DISCORD_SESSION_WORKDIR` is used.
- If the file does not exist, everything works as before — the feature is fully optional.
- Environment variables in paths (like `$HOME`) are expanded automatically.

You can also use `--workdir` on individual `spawn` / `spawn-thread` commands to override
the mapping for a single session.

**Tip:** After updating `workdir-map.json`, run `kill-all` then `discover-all` to re-spawn
all sessions with the new workdir assignments. Existing sessions are not affected until
they are killed and re-spawned.

## Slash Commands

The slash command daemon provides Discord-native `/command` interaction for managing
sessions without leaving the chat interface.

### Starting the Daemon

The watchdog automatically manages the slash daemon. When the watchdog runs, it checks
for the `dc-slash-daemon` tmux session and spawns it if missing.

```bash
# Manual start (standalone)
cd scripts && bun discord-slash-daemon.ts

# Or let the watchdog handle it
./scripts/discord-watchdog.sh --daemon
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/session status` | Show session info (workdir, uptime, name, tmux session) as an embed |
| `/session restart` | Kill + respawn the session. Use `fresh: true` for a clean conversation |
| `/session refresh` | Kill + respawn with the same session-id (picks up new skills/CLAUDE.md) |
| `/session kill` | Kill the session |
| `/session wake` | Wake a suspended session |
| `/session workdir [path]` | Show current workdir, or change it (kills + respawns with new workdir) |
| `/skills list` | List installed skills for the channel's session |
| `/skills install <name>` | Install a skill via `npx skills add` in the session |
| `/discover` | Trigger channel/thread discovery |
| `/ask <prompt>` | Send a prompt to the channel's Claude session |

### Autocomplete

The `/session workdir` command supports autocomplete. It reads entries from
`~/.claude/discord-sessions/workdir-map.json` and suggests matching paths as
the user types.

### Skills Install + Refresh

`/skills install <name>` sends the install command directly to the tmux session.
After installation completes, use `/session refresh` to kill and respawn the session
so it picks up the newly installed skill.

### Registering Commands

Commands are registered automatically when the daemon starts. To register or update
commands without running the full daemon:

```bash
bun scripts/register-slash-commands.ts           # Register/update commands
bun scripts/register-slash-commands.ts --clear    # Remove all guild commands
```

### Adding Custom Commands

1. Add the command definition to the `SLASH_COMMANDS` array in `discord-slash-daemon.ts`
2. Add a handler function (`handleYourCommand`)
3. Add the routing case in `handleInteraction`
4. Run `bun scripts/register-slash-commands.ts` to update Discord
5. Restart the daemon (or let the watchdog cycle pick it up)

### Prerequisites

The daemon requires:
- `bun` runtime
- `discord.js` v14 (install: `cd scripts && bun install`)
- Bot token at `~/.claude/channels/discord/.env`
- Guild ID in `~/.claude/discord-sessions/config.env`
- The bot must have the `applications.commands` scope in the guild

## Troubleshooting

### Sessions crash immediately after account switch

**Symptom:** After logging into a new Claude account (`claude login`), sessions spawn
but immediately die. Only the first session survives; all subsequent ones exit silently.

**Cause:** Stale `.session-id` files from the previous account. Claude Code's
`--session-id` flag tries to resume a conversation that doesn't exist under the new
account, causing the process to exit.

**Fix:**

```bash
# 1. Kill all sessions
./scripts/discord-session-manager.sh kill-all

# 2. Clear stale session IDs
for d in ~/.claude/discord-sessions/*/; do rm -f "$d/.session-id"; done

# 3. Clear session state
echo '{}' > ~/.claude/discord-sessions/sessions.json

# 4. Update OAuth token in config.env (if using CLAUDE_CODE_OAUTH_TOKEN)
# Edit ~/.claude/discord-sessions/config.env with your new token

# 5. Respawn all sessions
./scripts/discord-session-manager.sh discover-all
```

### Sessions start but Discord messages don't arrive

**Symptom:** Sessions show the Claude Code TUI prompt but no
"Listening for channel messages from: plugin:discord" banner.

**Cause:** The `--channels plugin:discord@claude-plugins-official` flag is missing
from the spawn command. The Discord plugin MCP server only connects when launched
with `--channels`.

**Fix:** Ensure the session manager includes `--channels` in the claude command.
The flag is required even though the plugin is installed globally.

### "You're out of extra usage" rate limit

**Symptom:** Session shows a rate-limit prompt with options to wait, switch to
extra usage, or upgrade.

**Fix:** Use `/session send 2` from Discord to select "Switch to extra usage",
or `/session send 1` to wait for reset.

## Architecture

```
Discord #general   →  tmux: dc-<a>  →  Claude Code (workdir A, CLAUDE.md chain A)
Discord #project-x →  tmux: dc-<b>  →  Claude Code (workdir B, CLAUDE.md chain B)
Thread: "design"   →  tmux: dc-<c>  →  Claude Code (parent context injected)
                      dc-watchdog    →  Respawns dead + discovers new + cleans stale
                      dc-slash-daemon → Handles /session, /skills, /ask, /discover
```
