---
name: file-operations
description: Read, write, search, and edit files across the workspace. Enforces the
  READ-BEFORE-WRITE rule, batch file reads, atomic SEARCH/REPLACE blocks, and file
  discovery via grep and glob rather than terminal commands.
argument-hint: <file path or search pattern>
---

<!-- Generated from skills/file-operations.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: File Operations

## Purpose
Read, write, search, and edit files in the filesystem with maximum efficiency and minimal token waste. _Source: Cursor (Category D)_

## Tools Required
- readFile / readMultipleFiles
- write / fsWrite
- append / fsAppend
- edit / strReplace / search_replace
- grep / grepSearch
- glob / fileSearch / glob_file_search
- delete / deleteFile
- list_dir / listDirectory

## General Principles
- Prefer batch reads (readMultipleFiles) over sequential single-file reads _Source: Amp (Category C)_
- Read entire files when practical — partial reads force extra roundtrips _Source: Cursor (Category D)_
- Search first (grep/glob) before reading when you don't know exact file location _Source: Cursor (Category H)_
- Never print file contents to user — use edit/write tools instead _Source: Qoder (Category E)_
- Never generate binary, hashes, or non-textual content _Source: Cursor (Category E)_

## Reading Files

### Single File
- Use `readFile` with known absolute path _Source: Kiro (Category D)_
- For large files (>500 lines), read in chunks with offset/limit _Source: Cursor (Category D)_
- Prefer reading a large meaningful section over many small sequential reads _Source: Amp (Category H)_

### Multiple Files
```python
# Preferred: batch related files in one call
readMultipleFiles(paths=[...])
```

### File Discovery
1. Use `glob` / `fileSearch` when you know part of the filename _Source: Cursor (Category D)_
2. Use `grep` / `grepSearch` when searching for content patterns _Source: Cursor (Category D)_
3. Use `listDirectory` for understanding structure _Source: Kiro (Category D)_
4. NEVER use shell `find`, `grep`, `cat` for file operations — use dedicated tools _Source: Kiro (Category C)_

## Writing Files

### Creating New Files
- Use `write` / `fsWrite` for new files or complete rewrites _Source: Kiro (Category D)_
- For files >50 lines, prefer write + follow-up appends _Source: Cursor (Category D)_
- Always create with complete, immediately runnable content _Source: Qoder (Category E)_
- Include all imports, dependencies, and types _Source: Aider (Category Q)_

### Appending to Existing Files
- Use `append` / `fsAppend` when adding to the end of a file _Source: Kiro (Category D)_
- File must already exist

### Editing Existing Files (SEARCH/REPLACE)
- Use `edit` / `strReplace` / `search_replace` for targeted edits _Source: Kiro (Category D)_
- CRITICAL: `oldString` / `SEARCH` block must match EXACTLY — character for character, including whitespace _Source: Aider (Category D)_
- Include 2-5 lines of surrounding context to ensure uniqueness _Source: Cline (Category D)_
- Break large edits into a series of smaller, targeted SEARCH/REPLACE blocks _Source: Cline (Category D)_
- Each block should change a focused section — don't edit half a file at once _Source: Cline (Category D)_

```python
# GOOD: precise with context
edit(
    filePath="src/app.py",
    oldString="def old_function():\n    return x + 1\n\ndef another():\n    pass",
    newString="def new_function():\n    return x * 2\n\ndef another():\n    pass"
)

# BAD: too little context (may match multiple places)
edit(
    filePath="src/app.py",
    oldString="return x + 1",
    newString="return x * 2"
)
```

### Partial Write for Large Files (Lovable pattern)
- For large files where only small sections change, use `// keep existing code` markers _Source: Lovable (Category D)_
- The unchanged code stays as a comment placeholder _Source: Lovable (Category D)_
- Only applies when the tooling supports this pattern _Source: Lovable (Category D)_

## Deleting Files
- Use `deleteFile` / `delete` with explanation _Source: Kiro (Category D)_
- Handles non-existent files gracefully _Source: Cursor (Category D)_

## Searching

### Content Search (grep)
- Use `grep` / `grepSearch` for regex pattern matching across files _Source: Cursor (Category D)_
- Rust regex syntax — escape special characters: `(`, `)`, `[`, `]`, `{`, `}`, `+`, `*`, `?`, `^`, `$`, `|`, `.`, `\` _Source: Cursor (Category D)_
- Include patterns to filter file types when possible _Source: Cursor (Category D)_
- Results capped at 50 — refine query if results fill up _Source: Cursor (Category D)_

### File Search (glob)
- Use `glob` / `fileSearch` when you know part of the filename _Source: Cursor (Category D)_
- Glob patterns like `**/*.ts`, `src/**/*.py`

## Directory Listing
- Use `listDirectory` / `list_dir` with optional depth parameter _Source: Kiro (Category D)_
- Use for understanding project structure before diving in _Source: Amp (Category H)_

## Batch Editing Rule (Windsurf pattern)
- When making multiple edits to the same file, combine ALL changes into a SINGLE edit call _Source: Windsurf (Category E)_
- This minimizes roundtrips and token overhead _Source: Amp (Category I)_
- Only split into multiple calls when edits are in completely unrelated sections _Source: Windsurf (Category E)_

## Post-Edit Verification
- After editing, check for linter errors by running lint tools _Source: Cursor (Category E)_
- If errors introduced, fix them (max 3 fix cycles per file) _Source: Cursor (Category E)_
- Verify imports are complete and correct _Source: Aider (Category Q)_
