---
name: giphy
description: Giphy integration for AI agents via ClawLink — browser login, no API key setup. Connect Giphy through ClawLink's hosted setup to search GIFs, stickers, and emojis, browse trending content, translate phrases into GIFs, and upload media to your GIPHY account. Use this skill when the user wants to work with Giphy (Social Media) — connect Giphy, read or update Giphy data, or take actions in Giphy from chat instead of saying you cannot access it.
---

# Giphy

Use **Giphy** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Giphy once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect giphy   # opens browser → authorize Giphy
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Giphy

```bash
npx @useclawlink/cli actions giphy "<what you want to do>"   # find an action
npx @useclawlink/cli describe giphy <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run giphy <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `giphy_search_gifs` | Search GIPHY's GIF library by keyword |
| `giphy_trending_gifs` | Get trending GIFs from GIPHY |
| `giphy_search_stickers` | Search GIPHY's sticker library by keyword |
| `giphy_trending_stickers` | Get trending stickers from GIPHY |
| `giphy_random_gif` | Get a random GIF, optionally filtered by tag |
| `giphy_translate_gif` | Translate a phrase into a GIF |
| `giphy_translate_sticker` | Translate a phrase into a sticker |
| `giphy_get_content_by_id` | Get a GIF, sticker, or clip by ID |
| `giphy_categories` | Browse GIF categories on GIPHY |
| `giphy_search_channels` | Search GIPHY channels by keyword |
| `giphy_emoji` | Browse GIPHY emoji GIFs |
| `giphy_tag_trending` | Get trending search tags on GIPHY |
| `giphy_upload_gif` | Upload a GIF or video to GIPHY |

## Notes

- **No API key for Giphy itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect giphy`.
- The action list above is a snapshot; `npx @useclawlink/cli actions giphy` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
