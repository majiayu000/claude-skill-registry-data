---
name: cursor-docmgr
description: Use the docmgr CLI to manage ticketed docs (create tickets, add docs, relate code files with file-note, update changelog, and search). Use when the user asks how to use docmgr, wants a docmgr command sequence, or needs docmgr best practices (file-note, quoting, doctor).
---

# Cursor Docmgr

## Overview

Provide a reliable, copy/paste-friendly docmgr workflow for creating and maintaining structured ticket documentation.

## Quick start

### Shell safety: backticks
- Never paste markdown backticks (`` `...` ``) into your shell unquoted.
  - Preferred: remove backticks.
  - Alternative: wrap the arg in quotes.

### Core workflow (per ticket)
- Create a ticket: `docmgr ticket create-ticket --ticket TICKET --title "..." --topics a,b`
- Add a doc: `docmgr doc add --ticket TICKET --doc-type design-doc --title "..."` (or `analysis`/`reference`/`playbook`)
- Relate code files (notes required): `docmgr doc relate --ticket TICKET --file-note "/abs/path:why it matters"`
- Update changelog: `docmgr changelog update --ticket TICKET --entry "..." --file-note "/abs/path:reason"`
- Validate: `docmgr doctor --ticket TICKET`

## Search patterns
- Full-text: `docmgr doc search --query "..." [--topics ...] [--doc-type ...]`
- Reverse lookup by file: `docmgr doc search --file path/to/file.go`
- Directory lookup: `docmgr doc search --dir path/to/dir/`

## Reference
- Full workflow + conventions live in `references/docmgr.md`.
