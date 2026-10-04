---
name: rag-drift
description: Detect and fix stale chunks (files that changed or were deleted since last indexing)
triggers:
  - rag drift
  - stale chunks
  - rag outdated
  - drift detection
---

# RAG Drift

**Drift** occurs when the index contains chunks from files that have been deleted or modified since indexing. The retrieval system silently returns outdated or orphaned content without error. Detect and fix drift before it degrades quality.

## What is drift?

Two types of drift corrupt the index:

| Type | Cause | Effect | Fix |
|------|-------|--------|-----|
| **Missing** | File deleted (chunks remain indexed) | Retrieval returns orphaned chunks pointing to nonexistent files | Delete chunks from DB or full rebuild |
| **Modified** | File changed (chunks show old content, sha mismatch) | Queries return stale snippets; content differs from current source | Incremental reindex the modified files |

Drift is **silent.** Retrieval still works, but returns wrong or outdated info.

## Detect drift

Run the report script:

```bash
cd ~/.claude/rag-index
venv/bin/python report.py
```

Read the drift summary:

```bash
cat ~/.claude/rag-index/weekly.md | grep -A 30 "Stale chunks"
```

Example output:
```
Stale chunks by type:
- Missing (deleted): 3 chunks
  ~/.claude/old-skill/SKILL.md (deleted 2024-12-15)
  
- Modified (sha mismatch): 12 chunks
  ~/.claude/standards/old-auth.md (last indexed 2024-12-10, modified 2024-12-18)
  /Volumes/External\ HD/Desenvolvimento/forgekit/src/utils.ts (last indexed 2024-12-15, modified 2024-12-16)
```

**Drift thresholds:**
- <5 stale chunks: normal churn; can wait for next full rebuild
- 5–20 chunks: fix incrementally today
- >20 chunks: full rebuild recommended (faster than 20+ incremental ops)

## Fix missing chunks (deleted files)

For files that no longer exist, delete their orphaned chunks:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite
```

In the sqlite prompt:

```sql
-- View chunks from the deleted file
SELECT COUNT(*), path FROM chunks 
WHERE path LIKE '%old-skill/SKILL.md%'
GROUP BY path;

-- Delete them
DELETE FROM chunks 
WHERE path LIKE '%old-skill/SKILL.md%';

-- Confirm deletion
SELECT COUNT(*) FROM chunks 
WHERE path LIKE '%old-skill/SKILL.md%';
```

Exit sqlite: `.exit`

**Quick delete (one line):**

```bash
sqlite3 ~/.claude/rag-index/index.sqlite \
  "DELETE FROM chunks WHERE path = '~/.claude/old-skill/SKILL.md';"
```

## Fix modified chunks (updated files)

Files that exist but have changed since indexing need incremental reindex:

```bash
cd ~/.claude/rag-index
venv/bin/python build.py --incremental ~/.claude/standards/old-auth.md
```

The incremental reindex will:
1. Delete old chunks from that file
2. Re-embed and insert new chunks with current content
3. Leave all other chunks untouched

## Auto-drift detection

The sessionstart hook (`sessionstart-drift-reindex.sh`) runs at session start:
- Checks for >10 stale chunks
- Recommends full rebuild if drift is significant
- Logs to `~/.claude/rag-index/drift.log`

This skill is for **manual drift intervention.** Use when:
- The auto-detector misses something
- You want granular control (delete vs. reindex vs. rebuild)
- Troubleshooting index corruption

## Prevent drift

- Run `report.py` weekly to catch drift early
- After bulk file deletions, run a full rebuild
- After significant content updates, incremental reindex those files
- Archive old docs instead of deleting; move to `~/.claude/archive/` instead of `rm`

## The `.last-drift-reindex` marker

After fixing drift, optionally update the marker file:

```bash
touch ~/.claude/rag-index/.last-drift-reindex
```

This marks the time drift was last resolved. The sessionstart hook checks this to avoid redundant corrections.

## Troubleshooting

**"Stale chunks count is high but report looks clean"**
- Run `report.py` again to refresh: `venv/bin/python report.py`
- Check the report timestamp: `stat ~/.claude/rag-index/weekly.md`

**"Incremental reindex didn't fix drift"**
- Verify the file path is correct and the file exists
- Run `report.py` again to see if stale count changed
- If still high, use full rebuild

**"Full rebuild but chunks didn't decrease"**
- Check if new files were added at the same time
- Query count may be stable if source repos are unchanged
- Run `inspect` skill to audit what's in the index

## See also

- `adt-rag-index-rebuild` — full or incremental reindex after drift
- `adt-rag-quality` — check retrieval quality; zero-hits may indicate drift
- `adt-rag-inspect` — examine chunks in the database
