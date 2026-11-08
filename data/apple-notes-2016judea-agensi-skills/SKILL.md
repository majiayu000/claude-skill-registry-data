---
name: apple-notes
description: Search and read your Apple Notes on a Mac straight from the local NoteStore.sqlite, read-only. Use when you ask "do you see the note about X", "what did I write about Y", "check my notes for the meeting with Z". No iCloud login or API needed.
---

# Apple Notes (local, read-only)

Read and search Apple Notes from the on-disk SQLite store. Note bodies are
gzip-compressed protobuf blobs, so a raw SQL query returns binary garbage. Always go
through `notes.py`, which decompresses and extracts clean text via the protobuf path
`Document(2) -> Note(3) -> note_text(2)`.

## Quick reference

Run from this skill's directory:

```bash
python3 notes.py "chamber of commerce"      # search titles + bodies, show snippets
python3 notes.py "rooftop meeting" --full   # print the full body of matching notes
python3 notes.py --list                     # list every note title, newest first
```

- Search is case-insensitive, matches title OR body, results newest-first.
- Snippet mode shows ~320 chars around the first hit; `--full` prints the whole note.
- When you don't know the exact wording, `--list` to scan titles, then `--full` the one you want.

## How it works

- **DB path:** `~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`
- Opened with `?immutable=1` (read-only; safe alongside the live `-wal`/`-shm` files, never locks).
- Bodies live in `ZICNOTEDATA.ZDATA` (gzip), joined to titles via
  `ZICCLOUDSYNCINGOBJECT.ZNOTEDATA`. Title = `ZTITLE1`, modified = `ZMODIFICATIONDATE1`
  (Apple Core Data epoch = 2001-01-01).
- The terminal running the agent needs Full Disk Access (System Settings > Privacy & Security)
  or the Group Containers folder is unreadable.

## Common mistakes

- **Querying `ZDATA` with plain SQL** gives gzip+protobuf bytes. Decompress AND walk the
  protobuf; gzip alone still leaves binary attribute-run formatting after the text.
- **Filter-printable hacks** to clean the blob leave trailing junk and drop Unicode
  (curly quotes, em-dashes). The protobuf extractor is the reliable path.
- **Opening the DB read-write** can hit a lock while Notes.app is running. Use `immutable=1`.

## Limits

- Read-only by design. To add a note, use AppleScript (`osascript`), never the SQLite store.
- Locked (password-protected) notes are encrypted and not readable this way.
- Reads only notes synced to this Mac.
