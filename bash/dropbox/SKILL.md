---
name: dropbox
description: Dropbox integration for AI agents via ClawLink — browser login, no API key setup. Connect Dropbox through ClawLink's hosted setup to browse, search, upload, download, and manage files and folders in your Dropbox account. Use this skill when the user wants to work with Dropbox (Storage & Databases) — connect Dropbox, read or update Dropbox data, or take actions in Dropbox from chat instead of saying you cannot access it.
---

# Dropbox

Use **Dropbox** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Dropbox once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect dropbox   # opens browser → authorize Dropbox
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Dropbox

```bash
npx @useclawlink/cli actions dropbox "<what you want to do>"   # find an action
npx @useclawlink/cli describe dropbox <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run dropbox <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `dropbox_list_folder_continue` | List files and folders in a Dropbox folder |
| `dropbox_get_metadata` | Get metadata for a Dropbox file or folder |
| `dropbox_search_file_or_folder` | Search Dropbox for files and folders |
| `dropbox_read_file` | Read the contents of a Dropbox file |
| `dropbox_download_zip` | Download a Dropbox folder as a ZIP archive |
| `dropbox_get_temporary_link` | Get a temporary link to download a Dropbox file |
| `dropbox_list_file_revisions` | List revisions of a Dropbox file |
| `dropbox_get_space_usage` | Get current Dropbox storage space usage |
| `dropbox_create_folder` | Create a new folder in Dropbox |
| `dropbox_upload_file` | Upload a file to Dropbox |
| `dropbox_copy_file_or_folder` | Copy a file or folder in Dropbox |
| `dropbox_move_file_or_folder` | Move a file or folder in Dropbox |
| `dropbox_share_folder` | Share a Dropbox folder with others |
| `dropbox_list_shared_links` | List shared links in Dropbox |
| `dropbox_create_shared_link` | Create a shared link for a Dropbox file or folder |

## Notes

- **No API key for Dropbox itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect dropbox`.
- The action list above is a snapshot; `npx @useclawlink/cli actions dropbox` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
