---
name: facebook
description: Facebook integration for AI agents via ClawLink — browser login, no API key setup. Connect Facebook through ClawLink's hosted setup to manage your Facebook Page — post content, read engagement, manage comments and messages, and view insights. Use this skill when the user wants to work with Facebook (Social Media) — connect Facebook, read or update Facebook data, or take actions in Facebook from chat instead of saying you cannot access it.
---

# Facebook

Use **Facebook** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Facebook once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect facebook   # opens browser → authorize Facebook
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Facebook

```bash
npx @useclawlink/cli actions facebook "<what you want to do>"   # find an action
npx @useclawlink/cli describe facebook <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run facebook <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `facebook_get_page_details` | Get Facebook Page details |
| `facebook_list_managed_pages` | List Facebook Pages you manage |
| `facebook_get_page_posts` | List posts from a Facebook Page |
| `facebook_get_post` | Get a single Facebook Page post |
| `facebook_get_post_insights` | Get insights for a Facebook Page post |
| `facebook_get_post_reactions` | Get reactions on a Facebook Page post |
| `facebook_get_comments` | List comments on a Facebook Page post |
| `facebook_get_page_insights` | Get Facebook Page insights |
| `facebook_get_page_conversations` | List conversations on a Facebook Page |
| `facebook_create_post` | Create a post on a Facebook Page |
| `facebook_create_photo_post` | Create a photo post on a Facebook Page |
| `facebook_create_comment` | Comment on a Facebook Page post |
| `facebook_send_message` | Send a message from a Facebook Page |
| `facebook_delete_post` | Delete a Facebook Page post |
| `facebook_update_post` | Update a Facebook Page post |

## Notes

- **No API key for Facebook itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect facebook`.
- The action list above is a snapshot; `npx @useclawlink/cli actions facebook` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
