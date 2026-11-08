---
name: onedrive
description: Microsoft OneDrive integration for AI agents via ClawLink — browser login, no API key setup. Connect Microsoft OneDrive through ClawLink's hosted setup to browse drives, search files and folders, download and upload files, create folders, manage sharing links, and inspect file metadata. Use this skill when the user wants to work with Microsoft OneDrive (Microsoft Apps) — connect Microsoft OneDrive, read or update Microsoft OneDrive data, or take actions in Microsoft OneDrive from chat instead of saying you cannot access it.
---

# Microsoft OneDrive

Use **Microsoft OneDrive** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Microsoft OneDrive once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect onedrive   # opens browser → authorize Microsoft OneDrive
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Microsoft OneDrive

```bash
npx @useclawlink/cli actions onedrive "<what you want to do>"   # find an action
npx @useclawlink/cli describe onedrive <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run onedrive <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `one_drive_list_drives` | List drives available to the connected OneDrive account |
| `one_drive_get_drive` | Get a OneDrive drive by ID |
| `one_drive_get_root` | Get the root folder of a OneDrive drive |
| `one_drive_list_folder_children` | List files and folders inside a OneDrive folder |
| `one_drive_get_item` | Get OneDrive file or folder metadata by ID |
| `one_drive_search_items` | Search OneDrive files and folders |
| `one_drive_get_recent_items` | Get recently accessed OneDrive items |
| `one_drive_onedrive_find_file` | Find a OneDrive file by name |
| `one_drive_onedrive_find_folder` | Find a OneDrive folder by name |
| `one_drive_download_file` | Download a OneDrive file |
| `one_drive_onedrive_create_folder` | Create a new folder in OneDrive |
| `one_drive_copy_item` | Copy a OneDrive file or folder |
| `one_drive_move_item` | Move a OneDrive file or folder |
| `one_drive_create_link` | Create a sharing link for a OneDrive file or folder |
| `one_drive_onedrive_upload_file` | Upload a file to OneDrive |

## Notes

- **No API key for Microsoft OneDrive itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect onedrive`.
- The action list above is a snapshot; `npx @useclawlink/cli actions onedrive` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
