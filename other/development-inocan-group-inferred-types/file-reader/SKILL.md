---
name: file-reader
description: Read a small snippet of a text file using file_read.
allowed-tools:
  - file_read
---

## When to use
- User asks to inspect a local file (docs/code/config).

## Procedure
1) Determine the target path (prefer relative to `AEVATAR_DEMO_ROOT`).
2) Call `file_read` with:
   - `path`
   - optional `startLine` / `maxLines`
3) Summarize what you read, and cite key lines by their line numbers from the tool output.


