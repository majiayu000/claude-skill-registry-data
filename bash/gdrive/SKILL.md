---
name: gdrive
category: productivity
description: Browse, search, and manage Google Drive files and folders. Use when the user shares a drive.google.com URL, asks what is in a folder, wants a file found, downloaded, uploaded, updated in place, moved, copied, or renamed, wants a Google file exported to PDF, Markdown, or CSV, wants comments read or added, wants sharing and permissions checked or changed, or wants Drive activity watched. Don't use for editing the contents of a Doc, Sheet, or Slides deck.
---

# Google Drive

Work with the Drive files and folders the user names or links to. Most commands
take a **file ID** — the segment after `/d/` or `/folders/` in a
`https://drive.google.com/...` URL.

> [!CAUTION]
>
> `mutate empty-trash` permanently deletes every trashed file and cannot be
> undone. Never run it, or any other destructive command, unless the user asks
> explicitly.

## Setup and Authentication

`gdrive auth status` is the only way to tell whether you are logged in. Do not
run `--help`, search the filesystem or environment for tokens, check another
plugin's login, or run an operational command before logging in. Follow these
steps exactly.

**1. Register and check.** Run this skill's script with `auth status`. It
downloads the CLI, registers `gdrive` on the agent's `PATH` (not the user's
shell), and reports whether you are logged in:

```bash
<path/to/this/skill>/scripts/gdrive auth status
```

```powershell
# Windows (PowerShell)
& "<path\to\this\skill>\scripts\gdrive.cmd" auth status
```

Every later call is just `gdrive`. Never ask the user to run it; they cannot. If
it reports `Logged in`, you are ready.

**2. Log in for the user.** Start this as a background command:

```bash
gdrive auth login
```

It prints an authorization URL and exits on its own once the user approves. Read
the URL from the task's log, open it in the user's browser or hand them the
link, then stop and wait. Confirm with `gdrive auth status`.

## Usage

Do every Drive operation — listing, searching, downloading, uploading, sharing —
through `gdrive`. Every command sits under one of two namespaces:

-   `readonly` browses, searches, reads, and exports without changing anything.
-   `mutate` uploads, edits, creates, deletes, and changes permissions.

So the commands read `gdrive readonly ls` and `gdrive mutate upload`. Run
`gdrive --help`, or `gdrive <namespace> <command> --help`, to confirm the exact
flags of any command below.

The split exists so the namespace can be allowlisted as a prefix. A terminal
permission rule can admit every `readonly` command outright and still prompt
before anything mutates, which only holds if you never reach for a command
outside its namespace.

Two rules the CLI's own help will not tell you:

-   **Reach for `readonly` first, and never run a `mutate` command the user did
    not ask for.** Deleting a file and widening a sharing setting are both
    one-way doors: a delete costs the user their data, and a share can expose it
    to people they never intended.
-   **Check where a file is going before you move it.** Moving a file out of a
    shared folder silently strips the access everyone else had through that
    folder, and nothing in the output will tell you it happened.

## Recipes

**Browse and search (readonly):**

```bash
gdrive readonly ls                          # list root (unlimited by default)
gdrive readonly ls FOLDER_ID --max 50       # limit results to 50 items
gdrive readonly ls --trashed                # list trashed items
gdrive readonly search --name-contains "quarterly report"
gdrive readonly search --content-contains "annual budget"   # search inside file content
gdrive readonly search --parent-id FOLDER_ID --modified-after 2024-01-01T00:00:00Z --type spreadsheet
gdrive readonly search --name-contains "quarterly report" --include-trashed
gdrive readonly recent --max 10
gdrive readonly starred
gdrive readonly info FILE_ID
gdrive readonly capabilities FILE_ID
gdrive readonly capabilities FILE_ID --filter canEdit,canComment   # narrow the output
gdrive readonly url FILE_ID                 # print web URL
gdrive readonly tree FOLDER_ID              # recursive folder tree
gdrive readonly count FOLDER_ID             # count items in folder
```

**File operations:**

```bash
gdrive readonly download FILE_ID --out /tmp/file.pdf   # download without converting
gdrive mutate upload /tmp/file.txt --parent FOLDER_ID
gdrive mutate upload /tmp/notebook.ipynb --mime-type "application/vnd.google.colaboratory" --parent FOLDER_ID
gdrive mutate update FILE_ID /tmp/updated.ipynb        # replace content, keep ID/link/permissions
gdrive mutate mkdir "New Folder" --parent FOLDER_ID
gdrive mutate create-shortcut FILE_ID FOLDER_ID        # shortcut inherits the original name
gdrive mutate cp FILE_ID "Copy of File" --parent FOLDER_ID
gdrive mutate mv FILE_ID NEW_PARENT_ID
gdrive mutate rename FILE_ID "New Name"
gdrive readonly export FILE_ID /tmp/doc.md --format md    # Docs to pdf/docx/txt/md/html
gdrive readonly export FILE_ID /tmp/sheet.tsv --format tsv # Sheets to pdf/xlsx/csv/tsv
gdrive readonly export FILE_ID /tmp/deck.pdf --format pdf  # Slides to pdf/pptx/txt
gdrive mutate trash FILE_ID
gdrive mutate untrash FILE_ID
gdrive mutate empty-trash --confirm
```

**Sharing and permissions:**

> [!WARNING]
>
> `mutate share --type anyone` makes a file readable by anyone with the link.
> Only use it when the user asks for a public link in so many words.

```bash
gdrive mutate share FILE_ID --email user@example.com --role writer
gdrive mutate share FILE_ID --email user@example.com --role reader --notify=false
gdrive readonly permissions FILE_ID
gdrive mutate remove-permission FILE_ID PERMISSION_ID
gdrive readonly audit-permissions FOLDER_ID            # recursive permission audit
```

**Comments:**

```bash
gdrive readonly list-comments FILE_ID
gdrive readonly list-comments FILE_ID --author user@example.com
gdrive readonly list-comments FILE_ID --mentioned user@example.com
gdrive readonly list-comments FILE_ID --assignee user@example.com
gdrive mutate add-comment FILE_ID 'Nice work!'
gdrive mutate reply-comment FILE_ID COMMENT_ID "Done"
gdrive mutate resolve-comment FILE_ID COMMENT_ID "Resolved."
```

**Other:**

```bash
gdrive readonly quota
gdrive readonly revisions FILE_ID
gdrive readonly shared-drives
gdrive mutate batch -f ops.json
```

**Watching Drive activity:**

`readonly watch` runs an event-driven background watcher that reacts to Drive
activity. It defaults to `events` mode, which uses the Workspace Events API and
Pub/Sub and needs a configured GCP project, resolved automatically or through
`--project_id`. Fall back to polling when that setup is unavailable.

```bash
gdrive readonly watch --watch_actions=commented,edited
gdrive readonly watch --watch_mode=poll --watch_actions=commented,edited
gdrive readonly watch --mime_type=docs --watch_actions=commented,edited
gdrive readonly watch --actor user@example.com --watch_actions=commented,edited
```

Pass `--json` to stream newline-delimited event objects to `stdout`, which is
what a pipeline or a sidecar wants:

```bash
gdrive readonly watch --json --watch_actions=commented | while read -r EVENT_JSON; do
  echo "Received: ${EVENT_JSON}"
done
```

## Commands

| Command                      | Description                                   |
| ---------------------------- | --------------------------------------------- |
| `readonly ls`                | List files with auto-pagination (unlimited by |
:                              : default; pass `--max N` to limit results;     :
:                              : supports `--trashed`)                         :
| `readonly count`             | Count files in folder with pagination         |
| `readonly search`            | Search files (supports `--trashed`)           |
| `readonly info`              | Get file info                                 |
| `readonly url`               | Print web URL                                 |
| `readonly download`          | Download file                                 |
| `mutate upload`              | Upload file (supports `--mime-type`)          |
| `mutate update`              | Update file content in-place (preserves ID,   |
:                              : link, permissions; supports `--mime-type`)    :
| `mutate mkdir`               | Create folder                                 |
| `mutate create-shortcut`     | Create a shortcut to a file in a folder       |
| `mutate cp`                  | Copy file (supports `--parent`)               |
| `mutate mv`                  | Move file                                     |
| `mutate rename`              | Rename file                                   |
| `readonly export`            | Export Google Workspace document (supports    |
:                              : `--format=pdf` / `docx` / `xlsx` / `pptx` /   :
:                              : `csv` / `tsv` / `txt` / `md` / `html`)        :
| `mutate trash`               | Trash file                                    |
| `mutate untrash`             | Restore file                                  |
| `mutate empty-trash`         | Empty trash                                   |
| `mutate share`               | Share file (`--notify=false` to suppress      |
:                              : email)                                        :
| `readonly permissions`       | List permissions                              |
| `mutate remove-permission`   | Remove permission                             |
| `readonly audit-permissions` | Recursive permission audit                    |
| `readonly capabilities`      | List file capabilities (supports `--filter`)  |
| `readonly recent`            | Recent files                                  |
| `readonly starred`           | Starred files                                 |
| `readonly quota`             | Show quota                                    |
| `readonly revisions`         | List file revisions                           |
| `readonly shared-drives`     | List shared drives                            |
| `readonly tree`              | Display folder tree                           |
| `readonly list-comments`     | List comments (supports `--author`,           |
:                              : `--mentioned`, `--assignee`)                  :
| `mutate add-comment`         | Add a comment                                 |
| `mutate reply-comment`       | Reply to a specific comment thread            |
| `mutate resolve-comment`     | Resolve a comment thread                      |
| `mutate batch`               | Execute batch ops                             |
| `readonly watch`             | Start a background watcher for Drive activity |

## Tips

-   `readonly ls` paginates across every page and is unlimited by default
    (`--max 0`). Pass `--max N` on a large or unfamiliar folder so the listing
    does not flood your context window.
-   Omit the file extension when searching for a native Google file by exact
    name. Write `readonly search --name-exact "Q3 Budget"`, not `"Q3
    Budget.gsheet"`. Extensions belong only in exact-name searches for uploads
    such as `report.pdf`.
-   `--mime-type` overrides the extension-based detection on `mutate upload` and
    `mutate update`. A `.ipynb` file has to be registered as
    `application/vnd.google.colaboratory` to render as a Colab notebook and to
    resolve when referenced elsewhere.
-   `readonly capabilities --filter` returns only the capabilities you name,
    which keeps large responses out of your context. `canEdit`, `canComment`,
    and `canShare` are the common ones. The full set is in the
    [Drive API file resource](https://developers.google.com/workspace/drive/api/reference/rest/v3/files#resource:-file).
-   `mutate reply-comment` and `mutate resolve-comment` want the **thread ID**,
    which is the ID of the original comment, not the ID of a reply.
-   `mutate add-comment` and `mutate reply-comment` check access when the
    comment text contains Drive links. The command fails when an @mentioned user
    cannot open a linked file, and warns on stderr when another collaborator
    cannot. Pass `--ignore-sharing-checks` to skip the check.
-   In `events` mode, `watch` prints `Drive Event Watcher Active` and then
    `[Discovery] Created WES subscription: ...` for each file it picks up. Treat
    those two lines as the confirmation that the subscription took.
-   Always pass `--mime_type` when watching one kind of document, so discovery
    and subscriptions stay scoped: `docs`, `sheets`, `slides`, `folder`,
    `colab`, or `pdf`.

## Global Flags

-   `--json` — output as JSON (works with all read commands)
-   `-v`, `--version` — print the CLI build version
