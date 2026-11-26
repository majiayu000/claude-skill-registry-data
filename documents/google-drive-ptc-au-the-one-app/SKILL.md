---
name: google-drive
description: Read before finding, uploading, renaming, moving or trashing files in the person's Google Drive.
metadata:
  title: "Google Drive"
  subtitle: "Your Drive files"
  about: "Your AI finds, uploads, renames, moves and trashes files in your Google Drive."
  category: Connectors
---

Google Drive is the person's Drive, through Drive's own API (v3) by its own names. Signing in is the skill
`google-account`'s.

- `files_list` finds files with Drive's `q` search (name contains 'budget' and trashed = false). `files_get`
  gives one. Answers have the fields asked for, and `fields` asks for more. A shared drive's files are only listed
  with `corpora: "drive"` and its `driveId`, which `drives_list` finds by name (`q: "name = 'PTC Systems'"`).
- `files_create` makes a folder, `files_upload` uploads a file (`upload`, the name the `upload` tool gave it,
  or `data` in base64 for a small one), and `files_update` renames, moves (addParents, removeParents) or trashes
  one. `generate_ids` gives ids to make files with, so a retry never makes two.
- A Google Doc, Sheet or Slides presentation's contents are read with `google-docs`, `google-sheets` and `google-slides`.
- With several accounts, each tool takes `account`. `google-account_accounts` lists them.
