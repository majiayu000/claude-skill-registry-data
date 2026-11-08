---
name: telegram
description: Telegram Bot integration for AI agents via ClawLink — browser login, no API key setup. Connect telegram through ClawLink's hosted setup. Use this skill when the user wants to work with Telegram Bot (Communication) — connect Telegram Bot, read or update Telegram Bot data, or take actions in Telegram Bot from chat instead of saying you cannot access it.
---

# Telegram Bot

Use **Telegram Bot** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Telegram Bot once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect telegram   # opens browser → authorize Telegram Bot
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Telegram Bot

```bash
npx @useclawlink/cli actions telegram "<what you want to do>"   # find an action
npx @useclawlink/cli describe telegram <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run telegram <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `telegram_answer_callback_query` | Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. |
| `telegram_create_chat_invite_link` | Generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. |
| `telegram_delete_message` | Delete a message, including service messages. Limitations: cannot delete messages older than 48 hours in groups, forwarded messages, or content in protected chats (returns 400 'message can’t be deleted'). Bot must have delete/manage rights in the target chat; works reliably only on bot-authored messages in groups. Verify permissions via TELEGRAM_GET_CHAT or TELEGRAM_GET_CHAT_ADMINISTRATORS before calling. On flood control, Telegram returns HTTP 429 with a retry_after field; honor that backoff value. |
| `telegram_edit_message` | Edit text messages sent by the bot. Only bot-authored messages can be edited; editing messages from other users will fail. In groups, the bot must have edit permissions. |
| `telegram_forward_message` | Forward messages of any kind. Service messages can't be forwarded. |
| `telegram_get_chat` | Get up to date information about the chat (current name of the user for one-on-one conversations, current username of a user, group or channel, etc.). The bot must be a member of or have access to the target chat; calls fail if the bot was never added, was removed, or is blocked. |
| `telegram_get_chat_administrators` | Get a list of administrators in a chat. On success, returns an Array of ChatMember objects containing information about all chat administrators except other bots. Only meaningful for supergroups and channels; private chats yield no useful data. The bot must be a member of the chat; if the bot has admin rights, its own entry will appear in the result, useful for verifying its permissions before moderation actions. |
| `telegram_get_chat_history` | Get chat history messages via the getUpdates polling method, filtered by chat_id. Returns only updates from the specified chat. Bot can only retrieve messages sent after it joined the chat; missing older messages is expected. Requires no active webhook — a webhook causes HTTP 409 conflict; delete it before using this tool. Empty result arrays (ok=true) indicate no accessible messages, not a failure. Returned message dates are Unix timestamps in UTC seconds. |
| `telegram_get_chat_member` | Get a chat member's status/role (including the bot itself) to preflight permissions and troubleshoot 403/empty-history issues. Use before sending messages to verify bot membership and permissions. |
| `telegram_get_chat_members_count` | Get the number of members in a chat. The bot must be an administrator in the chat for this to work. Insufficient admin permissions surface as authorization errors, not as a zero or empty count. |
| `telegram_get_me` | Get basic information about the bot using the Bot API getMe method. Returns fields like id, username, first_name, and capabilities. If the response returns ok=false, the bot token is invalid or revoked and must be replaced before any other API calls. Bot name, bio, and profile description are read-only via the Bot API; modify them via BotFather. |
| `telegram_get_updates` | Use this method to receive incoming updates using long polling. An Array of Update objects is returned. IMPORTANT: This method will not work if an outgoing webhook is set up. Webhooks and getUpdates are mutually exclusive — call deleteWebhook first to switch modes (409 Conflict otherwise). Notes: - Only one method (webhook or polling) can be active at a time - Updates available for up to 24 hours if unclaimed - Recalculate offset after each response to avoid duplicates - Empty result array (ok=true) is valid, meaning no new updates - On HTTP 429, honor the retry_after value; keep polling to ~1 request/second - Only chats with updates since the bot joined or last offset appear in results - Update objects vary by type; always check update.message and update.message.text exist before accessing |

## Notes

- **No API key for Telegram Bot itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect telegram`.
- The action list above is a snapshot; `npx @useclawlink/cli actions telegram` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
