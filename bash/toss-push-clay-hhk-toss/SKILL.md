---
name: toss-push
description: Push local files to a Toss recipient using natural language. Extracts files, recipient, and optional message from the user's intent.
tags: [toss, push, files, sharing]
---

# Toss Push

Push one or more local files to a recipient via the Toss CLI.

## When to Use

Trigger when the user says things like:
- "push report.md to xiaoming"
- "send these files to #zhangsan"
- "toss this to alice with a note saying check this"
- "push data.csv and notes.md to bob"
- "发给 xiaoming: report.pdf"

## Workflow

### Step 1: Extract Intent

Parse the user's message to identify:
- **Files**: file paths or names mentioned (e.g. `report.md`, `./data/output.csv`)
- **Recipient**: alias name or `#github_username`
- **Message**: optional note to attach (after "with a note", "saying", "-m", "附言", "备注")

If files are ambiguous (e.g. "this file"), look at the current working directory context or ask the user to clarify.

### Step 2: Validate Files Exist

Before running, verify each file path exists:

```bash
ls <file_path>
```

If a file does not exist, report it clearly and stop — do not proceed with a broken path.

### Step 3: Run Push

```bash
toss push <file1> [file2 ...] <recipient> [-m "message"]
```

Examples:
```bash
# Single file, alias recipient
toss push report.md xiaoming

# Multiple files, GitHub username
toss push data.csv notes.md #zhangsan

# With message
toss push report.pdf alice -m "check this before Monday"
```

### Step 4: Report Result

Show what was pushed:
- File name(s)
- Recipient
- File size(s) from the CLI output
- Any failures with the error detail

## Edge Cases

- If the user gives a relative path, run from the current working directory
- If recipient starts with `#`, pass it as-is (strip the `#`); otherwise pass the alias directly
- If multiple files fail, report each failure separately and continue with the rest
- If not logged in, suggest running `toss login` first

## Notes

- The CLI already handles duplicate filenames on the server side
- Supported file types: `.md`, `.txt`, `.json`, `.yaml`, `.py`, `.ts`, `.js`, `.html`, `.css`, `.csv`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.zip` — others sent as `application/octet-stream`
