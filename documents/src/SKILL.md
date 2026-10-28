---
name: nell
description: |
  Read and manage the person's e-book library with Nell, the Omarchy EPUB and
  PDF reader. Use when asked about their books, what they're reading, their
  highlights, notes, bookmarks, or looked-up words, or to add books to Nell.
---

# Nell

Nell is a desktop e-book reader for EPUB and PDF. Its library lives in
`~/.local/share/nell/`; books stay where they are on disk and are never
modified. The `nell` command reads and adds to the library without a display.

## Commands

Every command takes `--json`, exits 0 on success and 1 on failure, and writes
errors to stderr.

- `nell list` — the library, most recently read first: id, progress, title,
  author. `--json` adds path, format, cover, added and opened times, and
  whether the file is missing.
- `nell add <file>...` — add EPUB or PDF files. Adding a book that's already
  there (even moved) finds it again by content, so it is safe to repeat.
- `nell info <book>` — title, author, format, and table of contents of a file
  or a library id. Works on files not in the library.
- `nell notes <book>` — highlights with their notes and colors, grouped by
  chapter, plus bookmarks and looked-up words with definitions. Prints
  Markdown by default; `--json` gives the versioned export: each highlight's
  `text`, `note`, `color`, `section`, and `location` (an EPUB's Kindle-style
  location, a PDF's page; PDFs also have `page`). Works from the saved notes
  when the book file is missing.
- `nell import <file>` — read back a `nell notes --json` export, merged with
  any notes already saved for that book. Only when the person asks to restore
  notes.
- `nell open [book]` — open the reader for the person. It needs their
  desktop, so do not wait on it.

## Working with the person

- Their highlights and notes are their own reading; quote them faithfully and
  don't rewrite them.
- To answer "what was I reading", use `nell list --json` and look at
  `opened` and `progress`.
- Nell never edits book files, and neither should you on its behalf.
