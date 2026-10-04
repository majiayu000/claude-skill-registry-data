---
name: rag-inspect
description: Examine what's actually stored in the index for specific items
triggers:
  - rag inspect
  - inspect chunks
  - what's indexed
  - chunk inspection
  - rag debug
---

# RAG Inspect

Query the index database directly to understand chunk counts, sizes, metadata, and content. Use when you need to diagnose index health, find what's missing, or audit coverage.

## Quick index summary

```bash
sqlite3 ~/.claude/rag-index/index.sqlite "SELECT COUNT(*) FROM chunks;"
```

Expected: ~14,355 chunks

## Chunks by source type

See how the corpus is distributed across different content categories:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT source_type, COUNT(*) as chunk_count, 
       ROUND(AVG(LENGTH(text)), 0) as avg_size
FROM chunks
GROUP BY source_type
ORDER BY COUNT(*) DESC;
EOF
```

**Example output:**
```
source_type        chunk_count  avg_size
skills             539          245
handoffs           259          312
code               1847         218
standards          54           401
plans              198          267
...
```

**Healthy baselines:**
- `skills`: ≥500 chunks (comprehensive coverage)
- `handoffs`: ≥200 chunks
- `standards`, `codex`: ≥50 chunks combined
- `code`: scales with repo size

## Chunks by repository

Find which repos are well-indexed and which are thin:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT repo, COUNT(*) as chunk_count
FROM chunks
WHERE repo IS NOT NULL
GROUP BY repo
ORDER BY COUNT(*) DESC;
EOF
```

Repos with <50 chunks likely have gaps.

## Chunks for a specific file

Find all chunks extracted from a single source file:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT id, start_line, end_line, LENGTH(text) as size
FROM chunks
WHERE path LIKE '%filename%'
ORDER BY start_line;
EOF
```

Replace `%filename%` with part of the file path. Example:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite \
  "SELECT id, start_line, end_line, LENGTH(text) FROM chunks WHERE path LIKE '%SKILL.md%' LIMIT 5;"
```

## View chunk text

Read the actual content of a chunk:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT text FROM chunks
WHERE path LIKE '%standards/code.md%'
LIMIT 3;
EOF
```

Replace the path and limit to control output size.

## Find chunks by size

Too small (<80 chars) = truncated or useless. Too large (>2000 chars) = too coarse for retrieval.

**Tiny chunks (potential truncation):**

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT path, LENGTH(text) as size, text
FROM chunks
WHERE LENGTH(text) < 80
ORDER BY LENGTH(text)
LIMIT 10;
EOF
```

**Giant chunks (too coarse):**

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT path, LENGTH(text) as size
FROM chunks
WHERE LENGTH(text) > 2000
ORDER BY LENGTH(text) DESC
LIMIT 10;
EOF
```

**Ideal chunk size distribution:**

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT 
  CASE 
    WHEN LENGTH(text) < 100 THEN 'tiny (<100)'
    WHEN LENGTH(text) < 300 THEN 'small (100-300)'
    WHEN LENGTH(text) < 800 THEN 'medium (300-800)'
    ELSE 'large (800+)'
  END as size_bucket,
  COUNT(*) as chunk_count,
  ROUND(AVG(LENGTH(text)), 0) as avg_size
FROM chunks
GROUP BY size_bucket
ORDER BY avg_size;
EOF
```

Goal: Most chunks in the 200–800 range.

## Count chunks with missing metadata

Check if chunks have embeddings (nullable field):

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT COUNT(*) as no_embedding FROM chunks WHERE embedding IS NULL;
EOF
```

Zero is healthy. If >0, re-embed those chunks.

## Chunks from a specific source type + repo combo

Combine filters to find niche coverage:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT COUNT(*) FROM chunks
WHERE source_type = 'code' AND repo = 'forgekit';
EOF
```

Replace `source_type` and `repo` with values from earlier queries.

## Check for duplicate chunks

Identical content in two chunks = potential index error:

```bash
sqlite3 ~/.claude/rag-index/index.sqlite << 'EOF'
SELECT text, COUNT(*) as occurrences
FROM chunks
GROUP BY text
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
EOF
```

If you find duplicates, note the paths and consider a full rebuild.

## Good chunks vs. bad chunks

| Attribute | Good | Bad |
|-----------|------|-----|
| Size | 200–800 chars | <80 or >2000 |
| Content | Coherent unit (paragraph, function, section) | Truncated mid-sentence or entire doc |
| Metadata | path, start_line, end_line, source_type all set | Missing fields |
| Language | Clear, keyword-rich | Noise, filler, or context-less |

## Troubleshooting

**"Chunk count is much lower than expected"**
- Verify the index file exists: `ls -lh ~/.claude/rag-index/index.sqlite`
- Check if a full rebuild is in progress
- Run `report.py` to see the latest index state

**"Many chunks are <100 chars"**
- Run the `adt-rag-index-rebuild` skill with `--full` to re-chunk
- Or check `build.py` chunk size configuration

**"A repo has 0 chunks but has source files"**
- Verify the repo path is in `build.py`'s source list
- Run incremental reindex for that repo: `build.py --incremental /path/to/repo/**/*.py`

## See also

- `adt-rag-coverage` — audit corpus distribution by type and repo
- `adt-rag-quality` — find zero-hit queries and weak retrievals
- `adt-rag-index-rebuild` — reindex after findings require changes
