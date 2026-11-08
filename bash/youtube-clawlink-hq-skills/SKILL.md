---
name: youtube
description: YouTube integration for AI agents via ClawLink — browser login, no API key setup. Connect YouTube through ClawLink's hosted setup to manage videos, playlists, channels, comments, and view analytics without manual credential setup. Use this skill when the user wants to work with YouTube (Social Media) — connect YouTube, read or update YouTube data, or take actions in YouTube from chat instead of saying you cannot access it.
---

# YouTube

Use **YouTube** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect YouTube once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect youtube   # opens browser → authorize YouTube
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using YouTube

```bash
npx @useclawlink/cli actions youtube "<what you want to do>"   # find an action
npx @useclawlink/cli describe youtube <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run youtube <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `youtube_list_channel_videos` | List YouTube videos for a channel |
| `youtube_list_user_playlists` | List YouTube playlists |
| `youtube_get_channel_activities` | List YouTube channel activities |
| `youtube_create_playlist` | Create a YouTube playlist |
| `youtube_update_playlist` | Update a YouTube playlist |
| `youtube_delete_playlist` | Delete a YouTube playlist |
| `youtube_delete_playlist_item` | Delete items from a YouTube playlist |
| `youtube_upload_video` | Upload a video to YouTube |
| `youtube_multipart_upload_video` | Upload a large video to YouTube via multipart |
| `youtube_get_video_details_batch` | Get YouTube video metadata |
| `youtube_update_video` | Update YouTube video metadata |
| `youtube_get_channel_statistics` | Get YouTube channel statistics |
| `youtube_list_comment_threads2` | List YouTube comment threads |
| `youtube_list_comments` | List YouTube comments |
| `youtube_create_comment_reply` | Reply to a YouTube comment |
| `youtube_post_comment` | Post a comment on a YouTube video |
| `youtube_rate_video` | Rate a YouTube video |
| `youtube_subscribe_channel` | Subscribe to a YouTube channel |
| `youtube_unsubscribe_channel` | Unsubscribe from a YouTube channel |
| `youtube_search_you_tube` | Search YouTube videos and channels |
| `youtube_add_video_to_playlist` | Add a video to a YouTube playlist |

## Notes

- **No API key for YouTube itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect youtube`.
- The action list above is a snapshot; `npx @useclawlink/cli actions youtube` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
