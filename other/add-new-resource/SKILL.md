---
name: add-new-resource
argument-hint: [path to file or pasted content]
description: 'Ingest a file into the knowledge base: copy into /raw, evaluate, index in /wiki. Use when handed a document, transcript, export, or text dump to add to the workspace.'
---

# Add New Resource

Ingest one resource into the knowledge base. `$ARGUMENTS` is either a file path
or pasted raw content. If empty, ask for one.

## Process

1. **Acquire.** If given a path, read the file. If given pasted content, use it
   directly. If the content is unreadable or empty, stop and say so.
2. **Copy into `/raw`.** Write it to `raw/YYYY-MM-DD_<source>_<topic>.md` using
   today's date, a short source slug (e.g. `meeting`, `export`, `notes`), and a
   2-4 word topic slug. Never overwrite an existing raw file — suffix `-2` if
   the name collides. Do not modify the original content beyond adding a
   one-line provenance header (`> Source: <original path or "pasted">, added
   YYYY-MM-DD`).
3. **Evaluate.** Read the content and extract:
   - One-line summary (under 120 chars)
   - 2-5 tags
   - Any recurring mistakes, decisions, goals, or skill opportunities it reveals
4. **Index in `/wiki`.** Add a row to the **Resources** table in
   `wiki/index.md` (date, relative file link, source, summary, tags).
5. **Update topic pages.** If the resource matches an existing `wiki/<topic>.md`
   page, append its key points there with a link back to the raw file. If 3+
   indexed entries now share a theme with no topic page, create one and
   register it in the **Topic Pages** table.
6. **Report.** Tell the user the raw filename, the summary, and which wiki
   entries were touched.

## Rules

- Raw files are append-only: never edit or delete existing files in `/raw`
- Never skip indexing — an unindexed raw file is invisible to the system
- Do not commit unless the user asks
