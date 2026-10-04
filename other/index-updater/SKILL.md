---
name: index-updater
description: Keeps the 3-layer codebase index fresh after file edits. Performs incremental updates by recomputing hashes and re-extracting metadata for only changed files.
---

# Index Updater - Incremental Index Maintenance

Keeps `.claude/crew-index.json` and `.claude/crew-symbols.json` up-to-date after code changes without rebuilding the entire index.

## When to Activate

- After any agent makes file edits (triggered by afterFileEdit hook or agent self-reporting)
- When an agent notices the index is stale (hash mismatch)
- Manually via `/crew reindex` for full rebuild

## Incremental Update Process

### Step 1: Identify changed files
The agent that made changes should report which files were modified. Alternatively, check file hashes:

```
For each file in crew-index.json:
  1. Compute current hash: shasum -a 256 <filepath>
  2. Compare with stored hash
  3. If different → mark for update
  4. If file deleted → mark for removal
```

### Step 2: Update Layer 1 (crew-index.json)
For each changed file:
1. Read the file
2. Recompute: hash, size, lines, exports, imports, functions, classes
3. Regenerate summary
4. Replace the file's entry in crew-index.json

For deleted files:
1. Remove the file's entry from crew-index.json

For new files (detected via Glob that aren't in index):
1. Read and extract full metadata
2. Add new entry to crew-index.json

### Step 3: Update Layer 2 (crew-symbols.json)
For each changed file:
1. Re-extract all symbols (functions, classes, methods) with signatures and line ranges
2. Re-scan for calls to known symbols
3. Update calledBy relationships for affected symbols in other files
4. Replace all symbols for this file in crew-symbols.json
5. Rebuild affected callGraph entries

### Step 4: Update global metadata
1. Recompute contentHash from all file hashes
2. Update stats (totalFiles, totalLines)
3. Update lastIndexed timestamp

## Performance Rules

- **Never rebuild entire index** for a single file change
- **Batch updates**: If 3+ files changed in one edit cycle, update all at once
- **Skip non-source files**: Don't index changes to .json, .md, .yml unless they're in the monitored set
- **Lazy callGraph**: Only rebuild callGraph edges that involve the changed file

## Agent Self-Reporting Protocol

Every agent prompt includes this instruction:
```
After making any file changes, report them for index update:
"FILES_MODIFIED: src/parser.js, src/scraper.js"
The orchestrator will trigger incremental index update for these files.
```

This is more efficient than hash-checking every file after every edit.

## Staleness Detection

If an agent reads the index and finds information that doesn't match reality:
1. The symbol doesn't exist at the listed line range
2. A file listed in the index doesn't exist
3. A function's signature has changed

Then: trigger incremental update for that specific file before proceeding.

## Batch Update from Orchestrator

When called by the execution-orchestrator with a list of modified files after task completion:

**Input**: Deduplicated list of file paths reported by agents via `FILES_MODIFIED`

**Process**:
1. For each file in the list:
   - **If file exists**: Re-read the file, recompute SHA-256 hash, re-extract metadata (exports, imports, functions, classes, lines, summary). Replace the file's entry in `crew-index.json` (Layer 1) and re-extract all symbols with signatures and line ranges for `crew-symbols.json` (Layer 2).
   - **If file was deleted**: Remove the file's entry from both `crew-index.json` and `crew-symbols.json`.
   - **If file is new** (not in index): Read and extract full metadata, add new entry to both Layer 1 and Layer 2.
2. Rebuild affected `callGraph` edges — only edges involving the changed files, not the entire graph
3. Update `calledBy` relationships for symbols in other files that reference changed symbols
4. Update global metadata: recompute `contentHash` from all file hashes, update `stats.totalFiles`, `stats.totalLines`, set `lastIndexed` to current timestamp

**Output**: Report `"{N} files updated, {M} new, {K} removed"` back to the orchestrator

**Performance**: This should complete quickly for typical task outputs (1-10 files). For 10+ files, consider batching the Layer 2 symbol re-extraction.
