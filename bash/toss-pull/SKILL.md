---
name: toss-pull
description: Pull pending documents from Toss inbox using natural language. Downloads all pending files or lists inbox without downloading.
tags: [toss, pull, inbox, files, sharing]
---

# Toss Pull

Pull pending documents from the Toss inbox or inspect what is waiting.

## When to Use

Trigger when the user says things like:
- "pull my inbox"
- "download files from toss"
- "check what's in my toss inbox"
- "拉取 toss 里的文件"
- "save incoming files to ./downloads"
- "what did people send me?"
- "list my inbox"
- "show pending toss files"

## Workflow

### Variant A: List Only (no download)

When the user wants to *see* what is waiting without downloading, run:

```bash
toss inbox
```

Report the table output: filename, sender, size, message, time.

### Variant B: Pull (download files)

When the user wants to *download* files:

```bash
# Pull to current directory
toss pull

# Pull to a specific directory
toss pull --to <dest_dir>
```

If the user specifies a destination (e.g. "save to ./downloads", "pull into /tmp"), extract it and pass via `--to`.

### Step: Report Result

After pulling, summarize:
- How many files were downloaded
- File names and senders
- Destination directory
- Any individual failures

If inbox is empty, say so clearly.

## Decision Tree

```
User says "list" / "show" / "check" / "what's waiting" → toss inbox
User says "pull" / "download" / "get" / "fetch" / "save" → toss pull [--to <dir>]
```

## Edge Cases

- If the destination directory does not exist, `toss pull` creates it automatically
- If a filename conflicts, the CLI auto-renames with a counter suffix (e.g. `report_1.md`)
- If not logged in, suggest running `toss login` first
- If the user says "pull to current folder", omit `--to` (defaults to `.`)
