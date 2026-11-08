---
name: zoom
description: Zoom integration for AI agents via ClawLink — browser login, no API key setup. Connect Zoom through ClawLink's hosted setup to create and manage meetings, webinars, recordings, whiteboards, and participants. Use this skill when the user wants to work with Zoom (Communication) — connect Zoom, read or update Zoom data, or take actions in Zoom from chat instead of saying you cannot access it.
---

# Zoom

Use **Zoom** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Zoom once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect zoom   # opens browser → authorize Zoom
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Zoom

```bash
npx @useclawlink/cli actions zoom "<what you want to do>"   # find an action
npx @useclawlink/cli describe zoom <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run zoom <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `zoom_create_a_meeting` | Create a Zoom meeting |
| `zoom_list_meetings` | List upcoming or recent Zoom meetings |
| `zoom_get_a_meeting` | Get details for a specific Zoom meeting |
| `zoom_update_a_meeting` | Update a Zoom meeting |
| `zoom_delete_a_meeting` | Delete a Zoom meeting |
| `zoom_add_a_meeting_registrant` | Register a participant for a Zoom meeting |
| `zoom_get_meeting_recordings` | Get recordings for a Zoom meeting |
| `zoom_get_past_meeting_participants` | Get participants from a past Zoom meeting |
| `zoom_create_whiteboard` | Create a new Zoom whiteboard |
| `zoom_list_whiteboards` | List all Zoom whiteboards |

## Notes

- **No API key for Zoom itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect zoom`.
- The action list above is a snapshot; `npx @useclawlink/cli actions zoom` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
