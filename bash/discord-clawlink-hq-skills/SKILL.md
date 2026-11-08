---
name: discord
description: Discord integration for AI agents via ClawLink — browser login, no API key setup. Connect discord through ClawLink's hosted setup. Use this skill when the user wants to work with Discord (Communication) — connect Discord, read or update Discord data, or take actions in Discord from chat instead of saying you cannot access it.
---

# Discord

Use **Discord** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Discord once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect discord   # opens browser → authorize Discord
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Discord

```bash
npx @useclawlink/cli actions discord "<what you want to do>"   # find an action
npx @useclawlink/cli describe discord <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run discord <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `discord_consume_entitlement` | Marks a one-time purchase consumable entitlement as consumed for a given application. Only applicable to entitlements backed by one-time purchase consumable SKUs. |
| `discord_delete_test_entitlement` | Deletes a currently active test entitlement for a given application. Use this to clean up test entitlements that are no longer needed. |
| `discord_delete_user_application_role_connection` | Deletes the current user's application role connection for the specified application. Removes the platform metadata and linked role connection. |
| `discord_edit_application_command_permissions` | Edits the permissions for a specific application command in a guild. Requires OAuth2 Bearer token (bot tokens will error). The authorizing user must have MANAGE_GUILD and MANAGE_ROLES permissions in the target guild. |
| `discord_get_application_command_permissions` | Retrieves the permissions for a specific application command in a guild. Requires OAuth2 Bearer token (bot tokens will error). The authorizing user must have MANAGE_GUILD and MANAGE_ROLES permissions in the target guild. |
| `discord_get_batch_application_command_permissions` | Retrieves permissions for all commands of an application in a guild. Returns a list of permission objects for each command. Requires OAuth2 Bearer token (Bot tokens will error). |
| `discord_get_current_user_application_entitlements` | Tool to retrieve entitlements for the current user for a given application. Use when you need to check what premium offerings or subscriptions the authenticated user has access to. |
| `discord_get_gateway` | Tool to retrieve a valid WebSocket (wss) URL for establishing a Gateway connection to Discord. Use when you need to connect to the Discord Gateway for real-time events. |
| `discord_get_guild_template` | Tool to retrieve information about a Discord guild template using its unique template code. Use when you need to get details about a guild template for creating new servers. |
| `discord_get_guild_widget` | Tool to retrieve the guild widget in JSON format. Use when you need to get public information about a Discord guild's widget that can be displayed on external websites. The widget must be enabled in the guild's server settings. |
| `discord_get_guild_widget_png` | Tool to retrieve a PNG image widget for a Discord guild. Use when you need a visual representation of the guild widget that can be displayed on external websites. The widget must be enabled in the guild's server settings. |
| `discord_get_my_guild_member` | Retrieves the guild member object for the currently authenticated user within a specified guild, including roles, nickname, join date, and permissions. |

## Notes

- **No API key for Discord itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect discord`.
- The action list above is a snapshot; `npx @useclawlink/cli actions discord` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
