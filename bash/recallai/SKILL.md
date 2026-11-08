---
name: recallai
description: Recall.ai integration for AI agents via ClawLink — browser login, no API key setup. Connect recallai through ClawLink's hosted setup. Use this skill when the user wants to work with Recall.ai (AI & ML) — connect Recall.ai, read or update Recall.ai data, or take actions in Recall.ai from chat instead of saying you cannot access it.
---

# Recall.ai

Use **Recall.ai** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Recall.ai once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect recallai   # opens browser → authorize Recall.ai
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Recall.ai

```bash
npx @useclawlink/cli actions recallai "<what you want to do>"   # find an action
npx @useclawlink/cli describe recallai <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run recallai <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `recallai_create_bot` | Create a new bot to join and record a meeting. This action creates a meeting bot that can join Zoom, Google Meet, Microsoft Teams, and other supported platforms to record audio, video, and capture transcriptions. For production use, schedule bots at least 10 minutes in advance using the join_at parameter to ensure the bot joins on time. |
| `recallai_create_calendar` | Tool to create a new calendar integration with Google Calendar or Microsoft Outlook. Use when you need to connect a calendar platform to enable automatic bot scheduling for meetings. |
| `recallai_create_calendar_authenticate` | Tool to generate an authentication token for calendar APIs, scoped to the user. Use when you need to authenticate calendar operations for a specific user. Each token has an expiry of 1 day from time of creation. |
| `recallai_create_google_login` | Tool to create a new Google Login credential within a login group. Use when you need to add a new Google account that bots can use to authenticate and join Google Meet meetings. |
| `recallai_create_google_login_group` | Tool to create a new Google Login Group for managing bot authentication. Use when you need to create a group of Google login credentials that bots can use to join Google Meet meetings. |
| `recallai_create_meeting_direct_connect` | Tool to create a Meeting Direct Connect for Google Meet or Zoom. Use when you need to connect directly to a meeting platform's media stream via Google Meet Media API or Zoom RTMS. Either google_meet_media_api or zoom_rtms credentials must be provided, but not both. |
| `recallai_create_sdk_upload` | Create a new Desktop SDK upload. Use this to generate an upload token that can be used with the Recall.ai Desktop SDK to upload recordings directly from desktop applications. |
| `recallai_create_zoom_oauth_app` | Tool to create a new Zoom OAuth App integration with Recall.ai. Use when you need to configure Zoom OAuth credentials to enable bots to join Zoom meetings. |
| `recallai_delete_bot` | Delete a scheduled bot by ID. This can only be used for scheduled bots that have not yet joined a call. If the bot is already in a call or about to join (less than 10 minutes before join time), use the REMOVE_BOT_FROM_CALL action instead. |
| `recallai_delete_bot_media` | Deletes bot media stored by Recall AI. This operation is irreversible and permanently removes all media files associated with the specified bot. |
| `recallai_delete_calendar` | Delete a calendar by ID. This will disconnect the calendar from Recall.ai. Use this when you need to remove a calendar integration. |
| `recallai_destroy_calendar_user` | Delete calendar user and disconnect any connected calendars. This is a destructive operation that permanently removes the calendar user account and disconnects all associated calendar platform connections (Google, Microsoft, etc.). |

## Notes

- **No API key for Recall.ai itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect recallai`.
- The action list above is a snapshot; `npx @useclawlink/cli actions recallai` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
