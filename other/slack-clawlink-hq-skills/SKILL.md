---
name: slack
description: Slack integration for AI agents via ClawLink — browser login, no API key setup. Connect Slack through ClawLink's hosted setup to send messages, search conversations, manage channels, and automate workflows from your Slack workspace. Use this skill when the user wants to work with Slack (Communication) — connect Slack, read or update Slack data, or take actions in Slack from chat instead of saying you cannot access it.
---

# Slack

Use **Slack** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Slack once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect slack   # opens browser → authorize Slack
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Slack

```bash
npx @useclawlink/cli actions slack "<what you want to do>"   # find an action
npx @useclawlink/cli describe slack <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run slack <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `slack_send_message` | Send a message to a Slack channel or DM |
| `slack_schedule_message` | Schedule a message to be sent later |
| `slack_update_message` | Update an existing Slack message |
| `slack_deletes_a_message_from_a_chat` | Delete a message from a Slack conversation |
| `slack_send_ephemeral_message` | Send an ephemeral message visible only to a specific user |
| `slack_fetch_conversation_history` | Fetch message history from a Slack conversation |
| `slack_fetch_message_thread_from_a_conversation` | Fetch a message thread from a Slack conversation |
| `slack_find_channels` | Find Slack channels by name |
| `slack_find_user_by_email_address` | Find a Slack user by email address |
| `slack_find_users` | Search for Slack users |
| `slack_list_all_channels` | List all Slack channels |
| `slack_list_all_users` | List all Slack users in the workspace |
| `slack_list_conversations` | List Slack conversations |
| `slack_list_files_with_filters_in_slack` | List Slack files with filters |
| `slack_list_pinned_items` | List pinned items in a Slack channel |
| `slack_list_scheduled_messages` | List scheduled messages in Slack |
| `slack_list_user_groups` | List Slack user groups |
| `slack_create_channel` | Create a new Slack channel |
| `slack_archive_conversation` | Archive a Slack conversation |
| `slack_invite_user_to_channel` | Invite a user to a Slack channel |
| `slack_join_an_existing_conversation` | Join an existing Slack conversation |
| `slack_leave_conversation` | Leave a Slack conversation |
| `slack_pin_item` | Pin an item in a Slack channel |
| `slack_unpin_item` | Unpin an item from a Slack channel |
| `slack_upload_or_create_a_file_in_slack` | Upload or create a file in Slack |
| `slack_download_slack_file` | Download a file from Slack |
| `slack_delete_file` | Delete a file from Slack |
| `slack_add_reaction_to_an_item` | Add an emoji reaction to a Slack message |
| `slack_remove_reaction_from_item` | Remove an emoji reaction from a Slack message |
| `slack_create_a_reminder` | Create a Slack reminder |
| `slack_list_reminders` | List Slack reminders |
| `slack_search_messages` | Search Slack messages |
| `slack_retrieve_conversation_information` | Retrieve information about a Slack conversation |
| `slack_retrieve_conversation_members_list` | Retrieve members of a Slack conversation |
| `slack_retrieve_user_profile_information` | Retrieve a Slack user's profile |
| `slack_get_bot_user` | Get the bot user identity in Slack |

## Notes

- **No API key for Slack itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect slack`.
- The action list above is a snapshot; `npx @useclawlink/cli actions slack` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
