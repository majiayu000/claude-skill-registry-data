---
name: apple-notes
description: Use when asked to check, search or read Apple Notes, or to find a document, PDF, scan or image attached to a note. READ ONLY — no creating or modifying notes.
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.2.0"
---

# Apple Notes (Read Only)

Read notes via Notes.app AppleScript, and list their attachments by reading the
Notes database. **No creating, updating, or deleting notes.**

## Prerequisites

- Notes.app running and synced
- Automation permissions granted (System Settings → Privacy & Security → Automation → Terminal/Claude Code → Notes)
- If first access attempt times out, ask user to check for macOS permission dialog
- `list-attachments.sh` does *not* use AppleScript — it reads the Notes database
  directly, so it needs **Full Disk Access** for the terminal instead of
  Automation. It keeps working when the AppleScript bridge is wedged.

## Reliability: always wrap osascript with timeout + retry

Notes.app's AppleScript bridge hangs intermittently. AppleScript-internal `with timeout of N seconds` does NOT kill a wedged osascript process — wrap with shell-level `timeout` and retry.

```bash
notes_query() {
  local script="$1" attempt
  for attempt in 1 2 3; do
    result=$(timeout 15 osascript -e "$script" 2>&1) && { echo "$result"; return 0; }
    sleep 2
  done
  echo "ERROR: Notes query failed after 3 attempts" >&2
  return 1
}
```

Reasonable defaults: **15s timeout, 3 retries, 2s sleep**. Bump to 30s for full-text search across many notes. If all retries fail, report and move on.

## Scripts

### List folders

```bash
${CLAUDE_SKILL_DIR}/scripts/list-folders.sh              # All folders across all accounts
${CLAUDE_SKILL_DIR}/scripts/list-folders.sh iCloud       # Only iCloud folders
```

### List notes in a folder

```bash
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh                        # iCloud/Notes (default)
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh "Shopping"             # iCloud/Shopping
${CLAUDE_SKILL_DIR}/scripts/list-notes.sh "Notes" "Gmail"        # Gmail/Notes
```

Output: `note name | modification date` (one per line)

### Read a note

```bash
${CLAUDE_SKILL_DIR}/scripts/read-note.sh "Shopping List"             # Search all accounts
${CLAUDE_SKILL_DIR}/scripts/read-note.sh "Meeting Notes" "iCloud"    # Specific account
```

Returns metadata header + HTML body.

### List attachments on a note

```bash
${CLAUDE_SKILL_DIR}/scripts/list-attachments.sh "Recipe Ideas"           # what is attached
${CLAUDE_SKILL_DIR}/scripts/list-attachments.sh "Recipe Ideas" --paths   # + on-disk file paths
```

Output: `[note] type | title | identifying text`, one per line.

**Read this before concluding a note doesn't contain something.** See below.

### Search notes by name

```bash
${CLAUDE_SKILL_DIR}/scripts/search-notes.sh "recipe"                 # Search all accounts
${CLAUDE_SKILL_DIR}/scripts/search-notes.sh "recipe" "iCloud"        # Specific account
```

Output: `note name | account/folder | modification date` (one per line)

## Direct Commands

For quick one-off access without scripts:

```bash
# List all iCloud folders
osascript -e 'tell application "Notes" to get name of every folder of account "iCloud"'

# List all note names in a folder
osascript -e 'tell application "Notes" to get name of every note in folder "Notes" of account "iCloud"'

# Read a note body (returns HTML)
osascript -e 'tell application "Notes" to get body of note "Note Name"'

# Count all notes
osascript -e 'tell application "Notes" to count every note'
```

## A note's body is not its contents

**A note body does not include its attachments.** PDFs, scans and images are
separate rows in the Notes database, linked back to the note — so reading the
body, by AppleScript or any other route, cannot see them. Every other script in
this skill reads bodies. That means:

> **A body search returning nothing is evidence about the search, not about the
> note.** If someone says a document is on a note and you can't find it, list the
> attachments before concluding it isn't there. Never substitute a similar file
> found somewhere else — a plausible substitute is worse than an empty result,
> because nothing downstream can tell it was the wrong one.

Two properties make this trap easy to fall into:

- **Scanned documents are all titled literally `PDF`.** Anything scanned in the
  app (`com.apple.paper.doc.pdf`) has the title `PDF` and no filename — measured
  at 17 of 17 in one real library. A note with four scanned recipes shows four
  identical rows. Filtering attachments *by title* finds nothing while looking
  thorough.
- **Ordinary attachments do carry real titles** (`Trailer-Manual-EN.pdf`), so
  partial success here is misleading: the file-picker attachments look fine and
  only the scanned ones are anonymous.

`list-attachments.sh` solves this by printing each attachment's **OCR/summary
text**, so the distinguishing first line is usually a column lookup rather than a
PDF extraction.

**Which attachments carry that text is not uniform, and the two gaps cover for
each other.** Measured across one real library:

| Attachment | Has a real title? | Has OCR text? |
|---|---|---|
| Scanned document (`com.apple.paper.doc.*`) | ✗ — always `PDF` | ✓ 31 of 32 |
| PDF added from the file picker (`com.adobe.pdf`) | ✓ | ✗ **0 of 179** |
| Image (jpeg/png/heic/…) | usually ✗ | ✓ ~100% |

Notes recognises text in what it renders itself — scans and photos — and never
in a PDF file you attached. So identify a *scanned* document by its OCR text and
a *file* PDF by its name, and treat an empty text column as normal rather than
as "nothing here". When it is empty and the name is unhelpful, fall back to
extracting the file:

```bash
# 1. What is actually attached?
list-attachments.sh "Recipe Ideas"
#    -> paper.doc.pdf | PDF | Tomato Soup / A simple weeknight soup with…

# 2. Get the file, then read it properly.
list-attachments.sh "Recipe Ideas" --paths
pdftotext -layout "<the path>" -
```

### Where attachments live on disk

Under `~/Library/Group Containers/group.com.apple.notes/Accounts/<account>/`:

| Kind | Path |
|---|---|
| Scanned document | `FallbackPDFs/<attachment-id>/<generation>/FallbackPDF.pdf` |
| Everything else | `Media/<media-row-id>/<filename>` |

⚠️ The `Media` path is keyed by the **linked media row's** identifier, not the
attachment's, and the real filename lives on that row too — the attachment row's
own `ZFILENAME` is always null. Joining the wrong row silently yields no path.

A missing file is normal and does not mean the attachment is missing: iCloud
downloads lazily, so the row can exist while the bytes have not arrived.

## Notes

- Note bodies are returned as **HTML** — use for display or pipe through a converter for plain text
- Note names are **case-sensitive** in AppleScript queries
- Searching large numbers of notes can be slow — scope to a specific account when possible
- The `whose name contains` filter is case-insensitive
- Notes.app must be running — scripts will launch it if needed, but sync may take a moment
