---
name: read
description: >
  Run at the start of every task, right after the user confirms it and before any
  edit, plan, or answer about the code. Read every relevant doc and source file
  completely, not by grep or partial scan, then state what was read.
---

# Read

Reading means the whole file, top to bottom. Grep, keyword search, and
offset/limit reads are for locating files only, never as the reading itself.

## Steps

1. List the files the task touches: the plan/doc for the feature, the files to
   change, their direct callers and callees, and their existing tests.
2. Read each one in full. If a file is over the Read limit, keep reading in
   consecutive chunks until the end. No file is skipped because it looks familiar.
   Skip only a file already read in full earlier in this session and unchanged since.
3. Say in one line which files you read. Name any you did not and why.
4. Only then plan or edit. If a later step pulls in a new file, read it in full too.
